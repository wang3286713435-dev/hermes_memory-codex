import inspect
import re
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
from time import perf_counter
from typing import Any
from uuid import uuid4

from sqlalchemy import and_, or_
from opensearchpy import OpenSearch
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.logging import get_logger
from app.models.audit import AuditLog
from app.models.chunk import Chunk
from app.models.document import Document, DocumentVersion
from app.models.retrieval import RetrievalLog
from app.schemas.retrieval import SearchRequest, SearchResponse, SearchResult
from app.services.meeting_transcript import enrich_meeting_metadata, meeting_trace
from app.services.retrieval.dense import (
    DenseSearchOutcome,
    ExistingVectorStoreDenseRetriever,
    QdrantDenseRetriever,
)
from app.services.retrieval.rerank import (
    AliyunTextReranker,
    NoopReranker,
    RerankOutcome,
    RerankRequest,
)
from app.services.retrieval.tender_metadata import (
    build_tender_metadata_snapshot,
    concrete_deep_field_missing_reason,
    has_concrete_deep_field_evidence,
    infer_tender_metadata_fields,
    snapshot_trace,
)

logger = get_logger(__name__)


@dataclass(frozen=True)
class CandidatePool:
    candidates: list[SearchResult]
    trace: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class RerankPolicyDecision:
    enabled: bool
    reason: str
    trace: dict[str, Any] = field(default_factory=dict)


class RetrievalService:
    def __init__(self, db: Session | None) -> None:
        self.db = db
        self.dense = self._build_dense_retriever()
        self.reranker = self._build_reranker()
        self._opensearch_filter_field_cache: dict[str, str] = {}

    def _build_dense_retriever(self):
        if settings.vector_store_provider == "qdrant":
            return QdrantDenseRetriever()
        return ExistingVectorStoreDenseRetriever()

    def _build_reranker(self):
        if settings.rerank_enabled and settings.rerank_provider == "aliyun":
            return AliyunTextReranker()
        return NoopReranker()

    def search(self, request: SearchRequest) -> SearchResponse:
        trace_id = str(uuid4())
        applied_filters, ignored_filters = self._normalize_filters(request)
        document_scope_trace = self._infer_document_scope(request.query, applied_filters)
        version_scope_trace = self._infer_version_scope(applied_filters)
        section_scope_trace = self._infer_section_scope(request.query)
        if document_scope_trace.get("document_id"):
            applied_filters["document_id"] = document_scope_trace["document_id"]
        if document_scope_trace.get("document_type") and "document_type" not in applied_filters:
            applied_filters["document_type"] = document_scope_trace["document_type"]
        metadata_snapshot_trace = self._infer_tender_metadata_scope(request.query, applied_filters)
        section_scope_trace = self._with_metadata_guidance(section_scope_trace, metadata_snapshot_trace)
        deep_field_trace = self._build_deep_field_trace(metadata_snapshot_trace, section_scope_trace)
        retrieval_mode = self._resolve_mode(request)
        backend = retrieval_mode
        dense_outcome = DenseSearchOutcome(status="skipped", trace={"reason": "dense disabled"})
        sparse_candidates: list[SearchResult] = []
        sparse_status = "skipped"
        sparse_trace: dict = {}

        if retrieval_mode in {"dense", "hybrid"} and request.enable_dense:
            dense_outcome = self._dense_search(request, applied_filters)

        if retrieval_mode in {"sparse", "hybrid"} and request.enable_sparse:
            try:
                sparse_candidates = self._execute_sparse_search(request, applied_filters, section_scope_trace)
                sparse_status = "executed"
                sparse_trace = {
                    "backend": "opensearch",
                    "returned": len(sparse_candidates),
                    "query_profile": section_scope_trace.get("query_profile", "default"),
                }
            except Exception:
                logger.exception("opensearch_search_failed_falling_back_to_db")
                backend = "database_fallback" if retrieval_mode == "sparse" else "hybrid_with_database_fallback"
                sparse_candidates = self._database_fallback_search(request, applied_filters, section_scope_trace)
                sparse_status = "failed"
                sparse_trace = {
                    "backend": "database_fallback",
                    "returned": len(sparse_candidates),
                    "fallback_reason": "opensearch_search_failed",
                }

        if retrieval_mode == "dense":
            candidate_pool = self._build_candidate_pool(
                retrieval_mode=retrieval_mode,
                dense_candidates=dense_outcome.results,
                sparse_candidates=[],
            )
            backend = dense_outcome.trace.get("backend") or "dense"
        elif retrieval_mode == "sparse":
            candidate_pool = self._build_candidate_pool(
                retrieval_mode=retrieval_mode,
                dense_candidates=[],
                sparse_candidates=sparse_candidates,
            )
            if backend == "sparse":
                backend = "opensearch"
        else:
            candidate_pool = self._build_candidate_pool(
                retrieval_mode=retrieval_mode,
                dense_candidates=dense_outcome.results,
                sparse_candidates=sparse_candidates,
            )
            if backend == "hybrid":
                backend = "hybrid"

        candidate_pool, access_policy_trace = self._apply_access_policy(
            request=request,
            trace_id=trace_id,
            candidate_pool=candidate_pool,
        )
        rerank_outcome = self._rerank_candidates(
            request=request,
            trace_id=trace_id,
            retrieval_mode=retrieval_mode,
            applied_filters=applied_filters,
            candidates=candidate_pool.candidates,
        )
        final_results = rerank_outcome.results[: request.top_k]
        deep_field_trace = self._with_final_deep_field_evidence(deep_field_trace, final_results)
        metadata_snapshot_trace = {
            **metadata_snapshot_trace,
            "deep_field_missing_reason": deep_field_trace["deep_field_missing_reason"],
            "deep_field_diagnostics": deep_field_trace["deep_field_diagnostics"],
        }
        meeting_transcript_trace = meeting_trace(final_results)
        access_policy_trace = {
            **access_policy_trace,
            "returned_document_ids": self._unique(result.document_id for result in final_results),
            "evidence_chunk_ids": self._unique(result.chunk_id for result in final_results),
            "version_ids": self._unique(result.version_id for result in final_results),
        }
        self._write_log(
            trace_id,
            request,
            len(final_results),
            backend,
            "success",
            access_policy_trace=access_policy_trace,
            results=final_results,
        )
        return SearchResponse(
            query=request.query,
            results=final_results,
            items=final_results,
            backend=backend,
            retrieval_mode=retrieval_mode,
            dense_status=dense_outcome.status,
            sparse_status=sparse_status,
            dense_retrieval_status=dense_outcome.status,
            applied_filters=applied_filters,
            ignored_filters=ignored_filters,
            trace={
                "trace_id": trace_id,
                "route_type": request.route_type,
                "retrieval_mode": retrieval_mode,
                "dense": dense_outcome.trace,
                "sparse": sparse_trace,
                "document_scope": document_scope_trace,
                "version_scope": version_scope_trace,
                "version_policy": version_scope_trace.get("version_policy", "latest_only"),
                "section_scope": section_scope_trace,
                "metadata_snapshot": metadata_snapshot_trace,
                "metadata_snapshot_used": metadata_snapshot_trace.get("metadata_snapshot_used", False),
                "metadata_snapshot_status": metadata_snapshot_trace.get("metadata_snapshot_status", "unavailable"),
                "metadata_fields_matched": metadata_snapshot_trace.get("metadata_fields_matched", []),
                "metadata_source_chunk_ids": metadata_snapshot_trace.get("metadata_source_chunk_ids", []),
                "metadata_guided_query_profile": metadata_snapshot_trace.get("metadata_guided_query_profile", "default"),
                "metadata_deep_field_profile": deep_field_trace["metadata_deep_field_profile"],
                "deep_field_profile": deep_field_trace["deep_field_profile"],
                "deep_field_section_hints": deep_field_trace["deep_field_section_hints"],
                "deep_field_query_aliases": deep_field_trace["deep_field_query_aliases"],
                "deep_field_missing_reason": deep_field_trace["deep_field_missing_reason"],
                "deep_field_diagnostics": deep_field_trace["deep_field_diagnostics"],
                **meeting_transcript_trace,
                "evidence_required": True,
                "snapshot_as_answer": False,
                "hybrid": {
                    "merged": candidate_pool.trace.get("deduped_count", len(candidate_pool.candidates)),
                    "dedupe_key": "chunk_id",
                    "fusion": "score_sum_by_source",
                } if retrieval_mode == "hybrid" else {},
                "access_policy": access_policy_trace,
                "candidate_pool": candidate_pool.trace,
                "rerank_policy": rerank_outcome.trace.get("policy", {}),
                "rerank": rerank_outcome.trace,
                "rerank_status": rerank_outcome.status,
            },
        )

    def _resolve_mode(self, request: SearchRequest) -> str:
        if request.retrieval_mode == "hybrid" and not request.enable_hybrid:
            if request.enable_sparse:
                return "sparse"
            if request.enable_dense:
                return "dense"
        if request.retrieval_mode == "dense" and not request.enable_dense:
            return "sparse" if request.enable_sparse else "dense"
        if request.retrieval_mode == "sparse" and not request.enable_sparse:
            return "dense" if request.enable_dense else "sparse"
        return request.retrieval_mode

    def _normalize_filters(self, request: SearchRequest) -> tuple[dict, dict]:
        filters = request.filters
        applied: dict = {}
        ignored: dict = {}

        extra_filters = {
            **(filters.extra or {}),
            **(getattr(filters, "model_extra", None) or {}),
        }
        version_id = extra_filters.get("version_id")
        if version_id:
            applied["version_id"] = version_id

        for field in ("source_type", "document_id", "document_type", "is_latest"):
            if field == "is_latest" and version_id:
                continue
            value = getattr(filters, field, None)
            if value is not None:
                applied[field] = value

        unsupported = {
            "project_id": filters.project_id,
            "customer_id": filters.customer_id,
            "confidentiality_level": filters.confidentiality_level,
            "permission_tags": filters.permission_tags or None,
            **extra_filters,
        }
        unsupported.pop("version_id", None)
        ignored = {key: value for key, value in unsupported.items() if value not in (None, [], {})}
        return applied, ignored

    def _dense_search(self, request: SearchRequest, applied_filters: dict) -> DenseSearchOutcome:
        return self.dense.search(request, applied_filters)

    def _execute_sparse_search(
        self,
        request: SearchRequest,
        applied_filters: dict,
        section_scope_trace: dict[str, Any],
    ) -> list[SearchResult]:
        # Some regression tests monkeypatch _sparse_search with the older
        # two-argument shape. Keep that compatibility while the public
        # retrieval contract remains unchanged.
        if len(inspect.signature(self._sparse_search).parameters) <= 2:
            return self._sparse_search(request, applied_filters)  # type: ignore[misc]
        return self._sparse_search(request, applied_filters, section_scope_trace)

    def _sparse_search(
        self,
        request: SearchRequest,
        applied_filters: dict,
        section_scope: dict[str, Any] | None = None,
    ) -> list[SearchResult]:
        client = OpenSearch(settings.opensearch_url, timeout=5)
        filters: list[dict] = []
        if "version_id" not in applied_filters:
            filters.append({"term": {self._resolve_opensearch_filter_field(client, "status"): "active"}})
        if "source_type" in applied_filters:
            filters.append(
                {"term": {self._resolve_opensearch_filter_field(client, "source_type"): applied_filters["source_type"]}}
            )
        if "document_id" in applied_filters:
            filters.append(
                {"term": {self._resolve_opensearch_filter_field(client, "document_id"): applied_filters["document_id"]}}
            )
        if "document_type" in applied_filters:
            filters.append(
                {"term": {self._resolve_opensearch_filter_field(client, "document_type"): applied_filters["document_type"]}}
            )
        if "version_id" in applied_filters:
            filters.append(
                {"term": {self._resolve_opensearch_filter_field(client, "version_id"): applied_filters["version_id"]}}
            )
        if "is_latest" in applied_filters:
            filters.append({"term": {"is_latest": applied_filters["is_latest"]}})

        section_scope = section_scope or {"status": "no_section_signal"}
        query_profile = section_scope.get("query_profile", "default")
        alias_text_boost = 1.6
        alias_heading_boost = 3.5
        target_heading_boost = 6.0
        target_title_boost = 5.0
        if query_profile == "commercial_scope":
            alias_text_boost = 4.0
            alias_heading_boost = 6.0
            target_heading_boost = 10.0
            target_title_boost = 8.0
        elif query_profile == "schedule_scope":
            alias_text_boost = 2.0
            alias_heading_boost = 4.0
            target_heading_boost = 7.0
            target_title_boost = 6.0

        should_clauses = [
            {"match": {"text": {"query": request.query, "boost": 1.0}}},
            {"match": {"source_name": {"query": request.query, "boost": 1.5}}},
            {"match": {"heading_path": {"query": request.query, "boost": 2.0}}},
        ]
        for alias in section_scope.get("query_aliases", []):
            should_clauses.append({"match": {"text": {"query": alias, "boost": alias_text_boost}}})
            should_clauses.append({"match_phrase": {"text": {"query": alias, "boost": alias_text_boost + 2.5}}})
            should_clauses.append({"match": {"heading_path": {"query": alias, "boost": alias_heading_boost}}})
            should_clauses.append({"match": {"title_path": {"query": alias, "boost": alias_heading_boost - 0.5}}})
            should_clauses.append({"match": {"section_path": {"query": alias, "boost": alias_heading_boost - 0.5}}})
        for section in section_scope.get("target_sections", []):
            should_clauses.append({"match": {"heading_path": {"query": section, "boost": target_heading_boost}}})
            should_clauses.append({"match": {"title_path": {"query": section, "boost": target_title_boost}}})
            should_clauses.append({"match": {"section_path": {"query": section, "boost": target_title_boost}}})
            should_clauses.append({"match_phrase": {"text": {"query": section, "boost": target_title_boost}}})
        metadata_source_chunk_ids = list(section_scope.get("metadata_source_chunk_ids") or [])
        if metadata_source_chunk_ids:
            should_clauses.append(
                {
                    "constant_score": {
                        "filter": {
                            "terms": {
                                self._resolve_opensearch_filter_field(client, "chunk_id"): metadata_source_chunk_ids
                            }
                        },
                        "boost": 5000.0,
                    }
                }
            )
        if query_profile == "schedule_scope":
            schedule_parameter_phrases = {
                "工期要求": 14.0,
                "总工期": 10.0,
                "计划开工日期": 9.0,
                "计划竣工日期": 9.0,
                "合同工期": 8.0,
                "日历天": 6.0,
                "竣工验收合格": 4.0,
            }
            for phrase, boost in schedule_parameter_phrases.items():
                should_clauses.append({"match_phrase": {"text": {"query": phrase, "boost": boost}}})
        elif query_profile == "pricing_scope":
            pricing_parameter_phrases = {
                "最高投标限价": 16.0,
                "招标控制价": 16.0,
                "最高限价": 13.0,
                "投标报价上限": 12.0,
                "投标限价": 11.0,
                "限价明细": 8.0,
                "不得超过": 7.0,
            }
            for phrase, boost in pricing_parameter_phrases.items():
                should_clauses.append({"match_phrase": {"text": {"query": phrase, "boost": boost}}})
        elif query_profile == "qualification_scope":
            qualification_parameter_phrases = {
                "投标人资格要求": 16.0,
                "资格条件": 14.0,
                "资质等级": 13.0,
                "项目经理": 12.0,
                "注册建造师": 10.0,
                "安全生产考核": 10.0,
                "联合体投标": 10.0,
                "类似工程业绩": 10.0,
                "人员配备": 8.0,
                "项目管理机构": 8.0,
            }
            for phrase, boost in qualification_parameter_phrases.items():
                should_clauses.append({"match_phrase": {"text": {"query": phrase, "boost": boost}}})
        for phrase, boost in self._meeting_query_boosts(request.query, applied_filters).items():
            should_clauses.append({"match_phrase": {"text": {"query": phrase, "boost": boost}}})

        response = client.search(
            index=settings.opensearch_index_chunks,
            body={
                "size": max(request.top_k, request.top_k * 2 if section_scope.get("target_sections") else request.top_k),
                "query": {
                    "bool": {
                        "should": should_clauses,
                        "filter": filters,
                        "minimum_should_match": 1,
                    }
                },
            },
        )
        results: list[SearchResult] = []
        for hit in response.get("hits", {}).get("hits", []):
            source = hit.get("_source", {})
            score = float(hit.get("_score") or 0.0)
            results.append(
                SearchResult(
                    chunk_id=source["chunk_id"],
                    document_id=source["document_id"],
                    version_id=source["version_id"],
                    chunk_index=source.get("chunk_index"),
                    text=source.get("text", ""),
                    score=score,
                    source_name=source.get("source_name"),
                    source_uri=source.get("source_uri"),
                    source_type=source.get("source_type"),
                    version_name=source.get("version_name"),
                    heading_path=source.get("heading_path") or [],
                    section_path=source.get("section_path") or source.get("title_path") or source.get("heading_path") or [],
                    page_start=source.get("page_start"),
                    page_end=source.get("page_end"),
                    metadata=self._result_metadata(
                        text=source.get("text", ""),
                        metadata=source.get("metadata_json") or {},
                        source_type=source.get("source_type"),
                        document_type=source.get("document_type"),
                        source_name=source.get("source_name"),
                        source_uri=source.get("source_uri"),
                        source_location=" > ".join(
                            source.get("section_path") or source.get("title_path") or source.get("heading_path") or []
                        ),
                        source_chunk_id=source.get("chunk_id"),
                    ),
                    retrieval_sources=["sparse"],
                    scores={"sparse": score},
                )
            )
        return results

    def _infer_section_scope(self, query: str) -> dict[str, Any]:
        normalized = self._normalize_document_reference(query)
        if not normalized:
            return {"status": "no_section_signal", "target_sections": [], "query_aliases": [], "query_profile": "default"}

        section_rules = [
            (
                ("资质", "资格", "项目经理", "建造师", "b证", "安全考核", "项目负责人", "联合体", "业绩", "人员要求", "人员配备", "项目管理机构"),
                ["投标人须知前附表", "资格审查", "资信标", "资格后审", "项目管理机构", "联合体投标", "类似工程业绩", "人员要求"],
                [
                    "资质要求",
                    "资格条件",
                    "项目经理",
                    "项目负责人",
                    "注册建造师",
                    "安全考核证",
                    "资格审查文件",
                    "联合体投标",
                    "类似工程业绩",
                    "人员配备",
                ],
                "qualification_scope",
            ),
            (
                ("工期", "工期天数", "关键节点", "关键工期节点", "里程碑", "计划开工日期", "计划竣工日期", "竣工日期"),
                [
                    "投标人须知前附表",
                    "合同专用条款",
                    "施工工期",
                    "工期要求",
                    "计划开工日期",
                    "计划竣工日期",
                    "竣工日期",
                    "关键工期节点",
                    "招标人对招标文件及合同范本的补充/修改",
                ],
                [
                    "计划工期",
                    "关键节点",
                    "关键工期节点",
                    "里程碑",
                    "总工期",
                    "施工工期",
                    "工期要求",
                    "计划开工日期",
                    "计划竣工日期",
                    "工期延误",
                ],
                "schedule_scope",
            ),
            (
                ("付款", "支付比例", "结算", "质保金", "保留金", "缺陷责任期", "误期", "赔偿", "违约"),
                [
                    "合同专用条款",
                    "工程款支付",
                    "进度款支付",
                    "竣工结算",
                    "最终结清",
                    "质量保证金",
                    "缺陷责任期",
                    "违约责任",
                    "工期延误",
                    "招标人对招标文件及合同范本的补充/修改",
                ],
                [
                    "付款",
                    "工程款支付",
                    "进度款支付",
                    "支付比例",
                    "结算",
                    "竣工结算",
                    "最终结清",
                    "质保金",
                    "质量保证金",
                    "保留金",
                    "缺陷责任期",
                    "误期赔偿",
                    "违约责任",
                    "工期延误",
                ],
                "commercial_scope",
            ),
            (
                ("工程名称", "项目名称", "工程地点", "建设地点", "项目地点", "招标人", "建设单位", "代建单位", "项目编号", "招标编号", "标段"),
                ["招标公告", "投标人须知前附表", "工程概况", "项目概况", "招标范围"],
                [
                    "工程名称",
                    "项目名称",
                    "工程地点",
                    "建设地点",
                    "招标人",
                    "建设单位",
                    "代建单位",
                    "项目编号",
                    "标段",
                ],
                "tender_basic_info",
            ),
            (
                ("工程量清单", "限价", "最高投标限价", "招标控制价", "投标报价上限", "最高报价", "报价上限", "控制价", "不平衡报价"),
                ["招标公告", "投标人须知前附表", "工程量清单", "限价明细", "最高投标限价", "招标控制价", "投标报价要求", "评标"],
                ["工程量清单", "最高投标限价", "招标控制价", "最高限价", "投标报价上限", "不平衡报价", "投标报价要求", "商务标定性评审表"],
                "pricing_scope",
            ),
        ]

        matched_sections: list[str] = []
        query_aliases: list[str] = []
        query_profile = "default"
        profile_priority = {
            "default": 0,
            "tender_basic_info": 1,
            "schedule_scope": 2,
            "pricing_scope": 3,
            "qualification_scope": 3,
            "commercial_scope": 3,
        }
        for triggers, sections, aliases, profile in section_rules:
            if any(self._normalize_document_reference(trigger) in normalized for trigger in triggers):
                for section in sections:
                    if section not in matched_sections:
                        matched_sections.append(section)
                for alias in aliases:
                    if alias not in query_aliases:
                        query_aliases.append(alias)
                if profile_priority.get(profile, 0) > profile_priority.get(query_profile, 0):
                    query_profile = profile

        if not matched_sections:
            return {"status": "no_section_signal", "target_sections": [], "query_aliases": [], "query_profile": "default"}

        return {
            "status": "section_scope_inferred",
            "target_sections": matched_sections,
            "query_aliases": query_aliases,
            "query_profile": query_profile,
            "deep_field_profile": query_profile,
        }

    def _infer_tender_metadata_scope(self, query: str, applied_filters: dict[str, Any]) -> dict[str, Any]:
        matched_fields = infer_tender_metadata_fields(query)
        if not matched_fields:
            return {
                "metadata_snapshot_used": False,
                "metadata_snapshot_status": "no_basic_info_intent",
                "metadata_fields_matched": [],
                "metadata_source_chunk_ids": [],
                "source_chunk_ids": [],
                "evidence_required": True,
                "snapshot_as_answer": False,
            }
        document_id = applied_filters.get("document_id")
        if not document_id:
            trace = snapshot_trace(None, matched_fields)
            trace["metadata_snapshot_status"] = "document_scope_required"
            return trace
        if self.db is None:
            trace = snapshot_trace(None, matched_fields)
            trace["metadata_snapshot_status"] = "db_unavailable"
            return trace
        if not self._is_tender_scope(applied_filters):
            trace = snapshot_trace(None, matched_fields)
            trace["metadata_snapshot_status"] = "not_tender_scope"
            return trace

        chunks = (
            self.db.query(Chunk)
            .filter(Chunk.document_id == document_id)
            .order_by(Chunk.chunk_index.asc())
            .limit(1500)
            .all()
        )
        snapshot = build_tender_metadata_snapshot(str(document_id), chunks)
        return snapshot_trace(snapshot, matched_fields)

    def _with_metadata_guidance(self, section_scope: dict[str, Any], metadata_trace: dict[str, Any]) -> dict[str, Any]:
        if not metadata_trace.get("metadata_snapshot_used"):
            return section_scope
        guided = dict(section_scope or {})
        guided["metadata_snapshot_used"] = True
        guided["metadata_source_chunk_ids"] = list(metadata_trace.get("metadata_source_chunk_ids") or [])
        guided["metadata_fields_matched"] = list(metadata_trace.get("metadata_fields_matched") or [])
        guided["query_profile"] = metadata_trace.get("metadata_guided_query_profile") or "tender_basic_info"
        target_sections = list(guided.get("target_sections") or [])
        guided_sections = {
            "tender_basic_info": ("招标公告", "投标人须知前附表", "工程概况", "项目概况"),
            "pricing_scope": ("招标公告", "投标人须知前附表", "工程量清单", "限价明细", "最高投标限价", "招标控制价", "投标报价要求"),
            "schedule_scope": ("招标公告", "投标人须知前附表", "工期要求", "计划开工日期", "计划竣工日期", "关键工期节点"),
            "qualification_scope": ("投标人须知前附表", "资格审查", "资格后审", "资信标", "项目管理机构", "联合体投标", "类似工程业绩", "人员要求"),
        }
        for section in guided_sections.get(guided["query_profile"], guided_sections["tender_basic_info"]):
            if section not in target_sections:
                target_sections.append(section)
        guided["target_sections"] = target_sections
        aliases = list(guided.get("query_aliases") or [])
        guided_aliases = {
            "tender_basic_info": ("工程名称", "工程地点", "建设单位", "招标人", "代建单位", "项目编号", "标段", "最高投标限价", "工期"),
            "pricing_scope": ("最高投标限价", "招标控制价", "最高限价", "投标报价上限", "投标限价", "限价明细"),
            "schedule_scope": ("工期", "总工期", "计划工期", "计划开工日期", "计划竣工日期", "关键工期节点"),
            "qualification_scope": ("资质要求", "资格条件", "项目经理", "注册建造师", "安全考核证", "联合体投标", "类似工程业绩", "人员配备"),
        }
        for alias in guided_aliases.get(guided["query_profile"], guided_aliases["tender_basic_info"]):
            if alias not in aliases:
                aliases.append(alias)
        guided["query_aliases"] = aliases
        guided["deep_field_profile"] = guided["query_profile"]
        guided["metadata_deep_field_profile"] = metadata_trace.get("metadata_deep_field_profile", "default")
        guided["status"] = "metadata_guided_section_scope"
        return guided

    def _build_deep_field_trace(
        self,
        metadata_trace: dict[str, Any],
        section_scope: dict[str, Any],
    ) -> dict[str, Any]:
        metadata_profile = metadata_trace.get("metadata_deep_field_profile") or "default"
        section_profile = section_scope.get("query_profile") or section_scope.get("deep_field_profile") or "default"
        deep_field_profile = section_profile if section_profile != "default" else metadata_profile
        section_hints = list(section_scope.get("target_sections") or [])
        query_aliases = list(section_scope.get("query_aliases") or [])
        metadata_diagnostics = dict(metadata_trace.get("deep_field_diagnostics") or {})
        intent_fields = list(
            metadata_trace.get("metadata_intent_fields")
            or metadata_diagnostics.get("intent_fields")
            or metadata_trace.get("metadata_fields_matched")
            or []
        )
        matched_fields = list(
            metadata_trace.get("metadata_fields_matched")
            or metadata_diagnostics.get("matched_fields")
            or []
        )
        missing_reason = metadata_trace.get("deep_field_missing_reason") or metadata_diagnostics.get("missing_reason")
        diagnostics = {
            **metadata_diagnostics,
            "profile": deep_field_profile,
            "metadata_deep_field_profile": metadata_profile,
            "section_targets_attempted": section_hints,
            "query_aliases_used": query_aliases,
            "boosted_phrases_used": self._deep_field_boosted_phrases(deep_field_profile),
            "metadata_source_chunk_ids": list(metadata_trace.get("metadata_source_chunk_ids") or []),
            "intent_fields": intent_fields,
            "matched_fields": matched_fields,
            "evidence_required": True,
            "snapshot_as_answer": False,
        }
        if not diagnostics.get("status"):
            diagnostics["status"] = "section_diagnostics_only" if section_hints or query_aliases else "no_deep_field_signal"
        if "concrete_evidence_required" not in diagnostics:
            diagnostics["concrete_evidence_required"] = False
        diagnostics["concrete_evidence_present"] = (
            diagnostics.get("concrete_evidence_required") is True
            and not diagnostics.get("concrete_evidence_missing_fields")
        )
        diagnostics["missing_reason"] = missing_reason
        return {
            "metadata_deep_field_profile": metadata_profile,
            "deep_field_profile": deep_field_profile,
            "deep_field_section_hints": section_hints,
            "deep_field_query_aliases": query_aliases,
            "deep_field_missing_reason": missing_reason,
            "deep_field_diagnostics": diagnostics,
        }

    def _with_final_deep_field_evidence(
        self,
        deep_field_trace: dict[str, Any],
        final_results: list[SearchResult],
    ) -> dict[str, Any]:
        diagnostics = dict(deep_field_trace.get("deep_field_diagnostics") or {})
        required_fields = list(diagnostics.get("concrete_evidence_required_fields") or [])
        if not required_fields:
            return deep_field_trace

        matched_fields = list(diagnostics.get("concrete_evidence_matched_fields") or [])
        final_matched_fields = [
            field_name
            for field_name in required_fields
            if any(has_concrete_deep_field_evidence(field_name, result.text or "") for result in final_results)
        ]
        final_missing_fields = [field_name for field_name in required_fields if field_name not in final_matched_fields]
        missing_reasons = [
            reason
            for field_name in final_missing_fields
            if (reason := concrete_deep_field_missing_reason(field_name))
        ]
        diagnostics.update(
            {
                "concrete_evidence_matched_fields": final_matched_fields,
                "concrete_evidence_missing_fields": final_missing_fields,
                "concrete_evidence_present": bool(required_fields) and not final_missing_fields,
                "final_retrieval_evidence_checked": True,
                "metadata_matched_fields_before_final_evidence_check": matched_fields,
            }
        )
        if final_missing_fields:
            diagnostics["status"] = "missing_concrete_evidence"
            diagnostics["missing_reasons"] = missing_reasons
            diagnostics["missing_reason"] = missing_reasons[0] if len(missing_reasons) == 1 else (missing_reasons or None)
            diagnostics["diagnostic_consistency"] = "metadata_anchor_without_final_concrete_evidence"
        else:
            diagnostics["status"] = "concrete_evidence_found"
            diagnostics["missing_reasons"] = []
            diagnostics["missing_reason"] = None
            diagnostics["diagnostic_consistency"] = "final_concrete_evidence_confirmed"

        if "project_manager_requirement" in required_fields:
            project_manager_level_explicit = "project_manager_requirement" in final_matched_fields
            diagnostics["project_manager_level_explicit"] = project_manager_level_explicit
            if not project_manager_level_explicit:
                diagnostics["project_manager_level_missing_reason"] = (
                    "electronic_certificate_format_is_not_role_level_requirement"
                )
            else:
                diagnostics.pop("project_manager_level_missing_reason", None)

        return {
            **deep_field_trace,
            "deep_field_missing_reason": diagnostics.get("missing_reason"),
            "deep_field_diagnostics": diagnostics,
        }

    def _deep_field_boosted_phrases(self, query_profile: str) -> list[str]:
        phrases_by_profile = {
            "pricing_scope": [
                "最高投标限价",
                "招标控制价",
                "最高限价",
                "投标报价上限",
                "投标限价",
                "限价明细",
                "不得超过",
            ],
            "qualification_scope": [
                "投标人资格要求",
                "资格条件",
                "资质等级",
                "项目经理",
                "注册建造师",
                "安全生产考核",
                "联合体投标",
                "类似工程业绩",
                "人员配备",
                "项目管理机构",
            ],
            "schedule_scope": [
                "工期要求",
                "总工期",
                "计划开工日期",
                "计划竣工日期",
                "合同工期",
                "日历天",
                "竣工验收合格",
            ],
        }
        return phrases_by_profile.get(query_profile, [])

    def _is_tender_scope(self, applied_filters: dict[str, Any]) -> bool:
        if applied_filters.get("source_type") == "tender" or applied_filters.get("document_type") == "tender":
            return True
        if applied_filters.get("source_type") or applied_filters.get("document_type"):
            return False
        document_id = applied_filters.get("document_id")
        if not document_id or self.db is None:
            return False
        document = self.db.query(Document).filter(Document.id == document_id).first()
        return bool(document and (document.source_type == "tender" or document.document_type == "tender"))

    def _meeting_query_boosts(self, query: str, applied_filters: dict[str, Any]) -> dict[str, float]:
        if applied_filters.get("source_type") != "meeting" and applied_filters.get("document_type") != "meeting":
            return {}
        normalized = self._normalize_document_reference(query)
        boosts: dict[str, float] = {}
        if any(token in normalized for token in ("行动项", "待办", "负责人", "跟进", "截止")):
            boosts.update({"行动计划": 16.0, "行动项": 14.0, "负责": 10.0, "跟进": 8.0, "截止": 8.0})
        if any(token in normalized for token in ("决策", "决定", "结论", "确认")):
            boosts.update({"会议结论": 16.0, "决定": 12.0, "确认": 10.0, "结论": 10.0, "核心逻辑": 6.0})
        if any(token in normalized for token in ("风险", "隐患", "问题", "待确认")):
            boosts.update({"风险": 16.0, "隐患": 14.0, "待确认": 12.0, "问题一": 11.0, "问题二": 11.0, "合规": 8.0, "监管": 8.0})
        return boosts

    def _resolve_opensearch_filter_field(self, client: OpenSearch, field: str) -> str:
        cached = self._opensearch_filter_field_cache.get(field)
        if cached:
            return cached
        try:
            mapping = client.indices.get_mapping(index=settings.opensearch_index_chunks)
            props = ((mapping.get(settings.opensearch_index_chunks) or {}).get("mappings") or {}).get("properties") or {}
            field_def = props.get(field) or {}
            if field_def.get("type") == "text" and (field_def.get("fields") or {}).get("keyword"):
                resolved = f"{field}.keyword"
            else:
                resolved = field
        except Exception:
            resolved = field
        self._opensearch_filter_field_cache[field] = resolved
        return resolved

    def _infer_document_scope(self, query: str, applied_filters: dict[str, Any]) -> dict[str, Any]:
        if applied_filters.get("document_id"):
            return {
                "status": "explicit_document_id",
                "document_id": applied_filters["document_id"],
            }

        normalized_query = self._normalize_document_reference(query)
        if not normalized_query:
            return {"status": "no_query_signal"}

        if self.db is None:
            return {
                "status": "db_unavailable",
                "reason": "document_scope_requires_db",
            }

        doc_query = self.db.query(Document).filter(Document.status == "active")
        if "source_type" in applied_filters:
            doc_query = doc_query.filter(Document.source_type == applied_filters["source_type"])
        if "document_type" in applied_filters:
            doc_query = doc_query.filter(Document.document_type == applied_filters["document_type"])

        candidates = doc_query.all()
        matches: list[tuple[Document, int]] = []
        for document in candidates:
            aliases = self._document_reference_aliases(document)
            matched_aliases = [alias for alias in aliases if alias and alias in normalized_query]
            if matched_aliases:
                matches.append((document, max(len(alias) for alias in matched_aliases)))

        if not matches:
            return {
                "status": "no_unique_document_match",
                "candidate_count": len(candidates),
                "matched_count": 0,
            }

        matches.sort(
            key=lambda item: (
                item[1],
                getattr(item[0], "created_at", None) or 0,
                getattr(item[0], "updated_at", None) or 0,
            ),
            reverse=True,
        )
        top_score = matches[0][1]
        top_matches = [document for document, score in matches if score == top_score]
        matched = sorted(
            top_matches,
            key=lambda document: (
                getattr(document, "created_at", None) or 0,
                getattr(document, "updated_at", None) or 0,
            ),
            reverse=True,
        )[0]
        status = "inferred_from_query"
        if len(matches) > 1:
            status = "inferred_from_query_latest_match"
        return {
            "status": status,
            "document_id": matched.id,
            "document_type": matched.document_type,
            "source_name": matched.title,
            "matched_count": len(matches),
        }

    def _infer_version_scope(self, applied_filters: dict[str, Any]) -> dict[str, Any]:
        version_id = applied_filters.get("version_id")
        if not version_id:
            return {
                "status": "latest_only",
                "version_policy": "latest_only",
                "stale_version": False,
            }
        trace: dict[str, Any] = {
            "status": "explicit_version_id",
            "version_policy": "explicit_history_version",
            "version_id": version_id,
            "stale_version": False,
        }
        if self.db is None:
            trace["status"] = "explicit_version_id_db_unavailable"
            return trace
        version = self.db.query(DocumentVersion).filter(DocumentVersion.id == version_id).first()
        if version is None:
            trace["status"] = "explicit_version_id_not_found"
            trace["stale_version"] = True
            return trace
        trace["document_id"] = version.document_id
        trace["is_latest"] = version.is_latest
        if version.is_latest:
            return trace
        latest = (
            self.db.query(DocumentVersion)
            .filter(DocumentVersion.document_id == version.document_id)
            .filter(DocumentVersion.is_latest.is_(True))
            .first()
        )
        trace["stale_version"] = True
        trace["latest_version_id"] = latest.id if latest else None
        trace["superseded_by_version_id"] = (version.metadata_json or {}).get("superseded_by_version_id")
        return trace

    def _document_reference_aliases(self, document: Document) -> list[str]:
        aliases = [
            self._normalize_document_reference(document.title),
            self._normalize_document_reference(Path(document.source_uri or "").stem),
            self._normalize_document_reference(document.source_uri or ""),
        ]
        deduped: list[str] = []
        for alias in aliases:
            if alias and alias not in deduped:
                deduped.append(alias)
        return deduped

    def _normalize_document_reference(self, value: str) -> str:
        text = (value or "").strip()
        if not text:
            return ""
        text = re.sub(r"\.(docx?|pdf|txt|md)$", "", text, flags=re.IGNORECASE)
        text = text.replace("围绕", " ").replace("回答", " ").replace("文件", " ")
        text = re.sub(r"[《》\"'“”‘’（）()【】\[\]\s]+", "", text)
        text = re.sub(r"[^0-9A-Za-z\u4e00-\u9fff]+", "", text)
        return text.lower()

    def _database_fallback_search(
        self,
        request: SearchRequest,
        applied_filters: dict | None = None,
        section_scope: dict[str, Any] | None = None,
    ) -> list[SearchResult]:
        applied_filters = applied_filters or {}
        if self.db is None:
            return []
        section_scope = section_scope or {}
        anchor_results = self._metadata_anchor_results(section_scope, applied_filters)
        query = (
            self.db.query(Chunk, Document, DocumentVersion)
            .join(Document, Chunk.document_id == Document.id)
            .join(DocumentVersion, Chunk.version_id == DocumentVersion.id)
            .filter(Document.status == "active")
        )
        keyword_terms = self._simplify_query_terms(request.query)
        if keyword_terms:
            query = query.filter(
                and_(
                    *[
                        or_(
                            Chunk.text.ilike(f"%{term}%"),
                            Document.title.ilike(f"%{term}%"),
                        )
                        for term in keyword_terms
                    ]
                )
            )
        else:
            query = query.filter(
                or_(
                    Chunk.text.ilike(f"%{request.query}%"),
                    Document.title.ilike(f"%{request.query}%"),
                )
            )
        if "source_type" in applied_filters:
            query = query.filter(Chunk.source_type == applied_filters["source_type"])
        if "document_id" in applied_filters:
            query = query.filter(Document.id == applied_filters["document_id"])
        if "document_type" in applied_filters:
            query = query.filter(Document.document_type == applied_filters["document_type"])
        if "version_id" in applied_filters:
            query = query.filter(DocumentVersion.id == applied_filters["version_id"])
        if "is_latest" in applied_filters:
            query = query.filter(DocumentVersion.is_latest == applied_filters["is_latest"])

        rows = query.limit(request.top_k).all()
        results: list[SearchResult] = []
        for chunk, document, version in rows:
            results.append(
                SearchResult(
                    chunk_id=chunk.id,
                    document_id=document.id,
                    version_id=version.id,
                    chunk_index=chunk.chunk_index,
                    text=chunk.text,
                    score=1.0,
                    source_name=document.title,
                    source_uri=document.source_uri,
                    source_type=chunk.source_type,
                    version_name=version.version_name,
                    heading_path=chunk.heading_path or [],
                    section_path=chunk.section_path or [],
                    page_start=chunk.page_start,
                    page_end=chunk.page_end,
                    metadata=self._result_metadata(
                        text=chunk.text,
                        metadata=chunk.metadata_json or {},
                        source_type=chunk.source_type,
                        document_type=document.document_type,
                        source_name=document.title,
                        source_uri=document.source_uri,
                        source_location=" > ".join(chunk.section_path or chunk.title_path or chunk.heading_path or [])
                        or f"chunk_index={chunk.chunk_index}",
                        source_chunk_id=chunk.id,
                    ),
                    retrieval_sources=["database_fallback"],
                    scores={"database_fallback": 1.0},
                )
            )
        return self._dedupe_preserve_order([*anchor_results, *results])[: request.top_k]

    def _metadata_anchor_results(self, section_scope: dict[str, Any], applied_filters: dict[str, Any]) -> list[SearchResult]:
        chunk_ids = list(section_scope.get("metadata_source_chunk_ids") or [])
        if not chunk_ids or self.db is None:
            return []
        query = (
            self.db.query(Chunk, Document, DocumentVersion)
            .join(Document, Chunk.document_id == Document.id)
            .join(DocumentVersion, Chunk.version_id == DocumentVersion.id)
            .filter(Document.status == "active")
            .filter(Chunk.id.in_(chunk_ids))
        )
        if "document_id" in applied_filters:
            query = query.filter(Document.id == applied_filters["document_id"])
        if "source_type" in applied_filters:
            query = query.filter(Chunk.source_type == applied_filters["source_type"])
        if "document_type" in applied_filters:
            query = query.filter(Document.document_type == applied_filters["document_type"])
        if "version_id" in applied_filters:
            query = query.filter(DocumentVersion.id == applied_filters["version_id"])
        if "is_latest" in applied_filters:
            query = query.filter(DocumentVersion.is_latest == applied_filters["is_latest"])
        rows = query.all()
        row_by_chunk_id = {chunk.id: (chunk, document, version) for chunk, document, version in rows}
        results: list[SearchResult] = []
        for index, chunk_id in enumerate(chunk_ids):
            row = row_by_chunk_id.get(chunk_id)
            if row is None:
                continue
            chunk, document, version = row
            score = 20.0 - (index * 0.01)
            results.append(
                SearchResult(
                    chunk_id=chunk.id,
                    document_id=document.id,
                    version_id=version.id,
                    chunk_index=chunk.chunk_index,
                    text=chunk.text,
                    score=score,
                    source_name=document.title,
                    source_uri=document.source_uri,
                    source_type=chunk.source_type,
                    version_name=version.version_name,
                    heading_path=chunk.heading_path or [],
                    section_path=chunk.section_path or [],
                    page_start=chunk.page_start,
                    page_end=chunk.page_end,
                    metadata={
                        **self._result_metadata(
                            text=chunk.text,
                            metadata=chunk.metadata_json or {},
                            source_type=chunk.source_type,
                            document_type=document.document_type,
                            source_name=document.title,
                            source_uri=document.source_uri,
                            source_location=" > ".join(chunk.section_path or chunk.title_path or chunk.heading_path or [])
                            or f"chunk_index={chunk.chunk_index}",
                            source_chunk_id=chunk.id,
                        ),
                        "metadata_snapshot_anchor": True,
                        "snapshot_as_answer": False,
                        "evidence_required": True,
                    },
                    retrieval_sources=["metadata_anchor"],
                    scores={"metadata_anchor": score},
                )
            )
        return results

    def _result_metadata(
        self,
        *,
        text: str,
        metadata: dict[str, Any],
        source_type: str | None,
        document_type: str | None,
        source_name: str | None,
        source_uri: str | None,
        source_location: str | None,
        source_chunk_id: str | None,
    ) -> dict[str, Any]:
        return enrich_meeting_metadata(
            text=text,
            metadata=metadata,
            source_type=source_type,
            document_type=document_type,
            source_name=source_name,
            source_uri=source_uri,
            source_location=source_location,
            source_chunk_id=source_chunk_id,
        )

    def _dedupe_preserve_order(self, candidates: list[SearchResult]) -> list[SearchResult]:
        seen: set[str] = set()
        deduped: list[SearchResult] = []
        for candidate in candidates:
            if candidate.chunk_id in seen:
                continue
            seen.add(candidate.chunk_id)
            deduped.append(candidate)
        return deduped

    def _simplify_query_terms(self, query: str) -> list[str]:
        text = (query or "").strip()
        if not text:
            return []

        normalized = re.sub(r"[，。；：、“”\"'‘’（）()【】\[\]、,.;:!?？]+", " ", text)
        normalized = normalized.replace("里的", " ").replace("里面", " ").replace("相关", " ")
        for stop in ("请查一下", "查一下", "请问", "帮我", "帮忙", "告诉我", "给我", "是什么", "有没有", "是否"):
            normalized = normalized.replace(stop, " ")

        phrase_candidates: list[str] = []
        project_matches = re.findall(r"([\u4e00-\u9fffA-Za-z0-9]{2,12}项目)", normalized)
        phrase_candidates.extend(project_matches)
        if "投标截止日期" in text:
            phrase_candidates.append("投标截止日期")
        if "招标资料" in text:
            phrase_candidates.append("招标资料")
        if "截止日期" in text:
            phrase_candidates.append("截止日期")

        raw_terms = re.findall(r"[A-Za-z0-9]{2,}|[\u4e00-\u9fff]{2,8}", normalized)
        stop_terms = {
            "这个", "那个", "什么", "哪些", "怎么", "如何", "一下", "内容", "资料",
            "文档", "文件", "请查", "请问", "帮忙", "关于", "里面", "里的", "相关",
        }
        terms: list[str] = []
        for term in raw_terms:
            if term in stop_terms:
                continue
            if len(term) < 2:
                continue
            if term not in terms:
                terms.append(term)

        merged = []
        for term in [*phrase_candidates, *terms]:
            if term not in merged:
                merged.append(term)

        return merged[:4]

    def _merge_candidates(
        self,
        dense_candidates: list[SearchResult],
        sparse_candidates: list[SearchResult],
    ) -> list[SearchResult]:
        by_chunk: dict[str, SearchResult] = {}
        for candidate in [*dense_candidates, *sparse_candidates]:
            if candidate.chunk_id in by_chunk:
                existing = by_chunk[candidate.chunk_id]
                sources = list(dict.fromkeys([*existing.retrieval_sources, *candidate.retrieval_sources]))
                scores = {**existing.scores, **candidate.scores}
                existing.retrieval_sources = sources
                existing.scores = scores
                existing.score = sum(scores.values())
                continue
            by_chunk[candidate.chunk_id] = candidate
        return sorted(by_chunk.values(), key=lambda item: item.score, reverse=True)

    def _build_candidate_pool(
        self,
        retrieval_mode: str,
        dense_candidates: list[SearchResult],
        sparse_candidates: list[SearchResult],
    ) -> CandidatePool:
        raw_candidates = [*dense_candidates, *sparse_candidates]
        source_counter: Counter[str] = Counter()
        for candidate in raw_candidates:
            if candidate.retrieval_sources:
                source_counter.update(candidate.retrieval_sources)
            else:
                source_counter["unknown"] += 1

        if retrieval_mode == "hybrid":
            candidates = self._merge_candidates(dense_candidates, sparse_candidates)
        else:
            candidates = sorted(raw_candidates, key=lambda item: item.score, reverse=True)

        return CandidatePool(
            candidates=candidates,
            trace={
                "status": "built",
                "retrieval_mode": retrieval_mode,
                "dense_returned": len(dense_candidates),
                "sparse_returned": len(sparse_candidates),
                "before_dedupe": len(raw_candidates),
                "after_dedupe": len(candidates),
                "raw_count": len(raw_candidates),
                "deduped_count": len(candidates),
                "source_counts": dict(source_counter),
                "dedupe_key": "chunk_id" if retrieval_mode == "hybrid" else None,
                "score_policy": "score_sum_by_source" if retrieval_mode == "hybrid" else "score_desc",
            },
        )

    def _apply_access_policy(
        self,
        *,
        request: SearchRequest,
        trace_id: str,
        candidate_pool: CandidatePool,
    ) -> tuple[CandidatePool, dict[str, Any]]:
        identity = self._resolve_request_identity(request)
        if not candidate_pool.candidates:
            trace = {
                **identity,
                "trace_id": trace_id,
                "access_policy_mode": "soft_acl_placeholder",
                "policy_decision": "not_configured_allow",
                "policy_reason": "no_candidates",
                "denied_document_ids": [],
                "returned_document_ids": [],
                "evidence_chunk_ids": [],
                "version_ids": [],
                "permission_trace_missing": self.db is None,
                "document_decisions": {},
            }
            return candidate_pool, trace

        document_ids = self._unique(candidate.document_id for candidate in candidate_pool.candidates)
        document_acl = self._load_document_acl(document_ids)
        allowed_candidates: list[SearchResult] = []
        denied_document_ids: list[str] = []
        document_decisions: dict[str, dict[str, Any]] = {}

        for document_id in document_ids:
            decision = self._decide_document_access(document_acl.get(document_id), identity)
            document_decisions[document_id] = decision
            if decision["decision"] == "deny":
                denied_document_ids.append(document_id)

        denied = set(denied_document_ids)
        for candidate in candidate_pool.candidates:
            if candidate.document_id in denied:
                continue
            allowed_candidates.append(candidate)

        policy_decision = self._aggregate_policy_decision(document_decisions, bool(candidate_pool.candidates))
        trace = {
            **identity,
            "trace_id": trace_id,
            "access_policy_mode": "soft_acl_placeholder",
            "policy_decision": policy_decision,
            "policy_reason": self._access_policy_reason(document_decisions, policy_decision),
            "candidate_document_ids": document_ids,
            "denied_document_ids": denied_document_ids,
            "returned_document_ids": [],
            "evidence_chunk_ids": [],
            "version_ids": [],
            "permission_trace_missing": any(
                decision.get("reason") in {"acl_not_configured", "acl_metadata_missing"}
                for decision in document_decisions.values()
            ),
            "document_decisions": document_decisions,
        }
        filtered_trace = {
            **candidate_pool.trace,
            "access_before_filter": len(candidate_pool.candidates),
            "access_after_filter": len(allowed_candidates),
            "access_denied_document_ids": denied_document_ids,
        }
        return CandidatePool(candidates=allowed_candidates, trace=filtered_trace), trace

    def _resolve_request_identity(self, request: SearchRequest) -> dict[str, Any]:
        extra = self._request_metadata(request)
        requester_id = request.user_id or extra.get("requester_id") or extra.get("user_id") or "local_dev"
        tenant_id = extra.get("tenant_id") or "local_dev"
        role = extra.get("role") or extra.get("requester_role") or extra.get("user_role") or "local_dev"
        return {
            "requester_id": str(requester_id),
            "tenant_id": str(tenant_id),
            "requester_role": str(role),
        }

    def _request_metadata(self, request: SearchRequest) -> dict[str, Any]:
        filters = request.filters
        metadata: dict[str, Any] = {}
        metadata.update(filters.extra or {})
        metadata.update(getattr(filters, "model_extra", None) or {})
        return metadata

    def _load_document_acl(self, document_ids: list[str]) -> dict[str, dict[str, Any] | None]:
        if not document_ids or self.db is None:
            return {document_id: None for document_id in document_ids}
        rows = self.db.query(Document).filter(Document.id.in_(document_ids)).all()
        metadata_by_id = {document.id: document.metadata_json or {} for document in rows}
        return {document_id: metadata_by_id.get(document_id) for document_id in document_ids}

    def _decide_document_access(
        self,
        metadata: dict[str, Any] | None,
        identity: dict[str, Any],
    ) -> dict[str, Any]:
        if metadata is None:
            return {"decision": "allow", "reason": "acl_metadata_missing", "policy_decision": "not_configured_allow"}

        allowed_requester_ids = self._as_list(metadata.get("allowed_requester_ids"))
        allowed_roles = self._as_list(metadata.get("allowed_roles"))
        tenant_id = metadata.get("tenant_id")
        acl_configured = bool(allowed_requester_ids or allowed_roles or tenant_id)

        if not acl_configured:
            return {"decision": "allow", "reason": "acl_not_configured", "policy_decision": "not_configured_allow"}

        if tenant_id and str(tenant_id) != identity["tenant_id"]:
            return {"decision": "deny", "reason": "tenant_mismatch", "policy_decision": "deny"}

        if allowed_requester_ids and identity["requester_id"] in allowed_requester_ids:
            return {"decision": "allow", "reason": "requester_id_allowed", "policy_decision": "allow"}

        if allowed_roles and identity["requester_role"] in allowed_roles:
            return {"decision": "allow", "reason": "role_allowed", "policy_decision": "allow"}

        if allowed_requester_ids or allowed_roles:
            return {"decision": "deny", "reason": "acl_no_match", "policy_decision": "deny"}

        return {"decision": "allow", "reason": "tenant_match", "policy_decision": "allow"}

    def _aggregate_policy_decision(self, document_decisions: dict[str, dict[str, Any]], had_candidates: bool) -> str:
        if not had_candidates:
            return "not_configured_allow"
        if document_decisions and all(decision["decision"] == "deny" for decision in document_decisions.values()):
            return "deny"
        if any(decision.get("policy_decision") == "allow" for decision in document_decisions.values()):
            return "allow"
        return "not_configured_allow"

    def _access_policy_reason(self, document_decisions: dict[str, dict[str, Any]], policy_decision: str) -> str:
        reasons = sorted({decision.get("reason", "unknown") for decision in document_decisions.values()})
        if not reasons:
            return "no_candidates"
        if policy_decision == "deny":
            return ",".join(reasons)
        if any(reason not in {"acl_not_configured", "acl_metadata_missing"} for reason in reasons):
            return ",".join(reasons)
        return "acl_not_configured"

    def _as_list(self, value: Any) -> list[str]:
        if value in (None, "", [], {}):
            return []
        if isinstance(value, list):
            return [str(item) for item in value if item not in (None, "")]
        if isinstance(value, (tuple, set)):
            return [str(item) for item in value if item not in (None, "")]
        return [str(value)]

    def _unique(self, values) -> list[str]:
        seen: set[str] = set()
        unique_values: list[str] = []
        for value in values:
            if value is None or value in seen:
                continue
            seen.add(value)
            unique_values.append(value)
        return unique_values

    def _rerank_candidates(
        self,
        request: SearchRequest,
        trace_id: str,
        retrieval_mode: str,
        applied_filters: dict[str, Any],
        candidates: list[SearchResult],
    ) -> RerankOutcome:
        policy = self._decide_rerank_policy(
            request=request,
            retrieval_mode=retrieval_mode,
            applied_filters=applied_filters,
            candidates=candidates,
        )
        rerank_request = RerankRequest(
            query=request.query,
            candidates=candidates,
            top_k=request.top_k,
            retrieval_mode=retrieval_mode,
            trace_id=trace_id,
        )
        active_reranker = self.reranker if policy.enabled else NoopReranker()
        started_at = perf_counter()
        try:
            outcome = active_reranker.rerank(rerank_request)
            return self._with_policy_trace(outcome, policy)
        except Exception as exc:
            elapsed_ms = round((perf_counter() - started_at) * 1000, 3)
            logger.exception("rerank_failed_falling_back_to_candidate_pool")
            fallback_results = sorted(candidates, key=lambda item: item.score, reverse=True)[: request.top_k]
            return self._with_policy_trace(
                RerankOutcome(
                results=fallback_results,
                status="failed_open",
                provider=getattr(active_reranker, "provider", active_reranker.__class__.__name__),
                trace={
                    "provider": getattr(active_reranker, "provider", active_reranker.__class__.__name__),
                    "status": "failed_open",
                    "reason": "rerank_exception",
                    "reason_if_skipped": None,
                    "fail_open": True,
                    "elapsed_ms": elapsed_ms,
                    "error": str(exc),
                    "input_count": len(candidates),
                    "output_count": len(fallback_results),
                    "candidate_count_in": len(candidates),
                    "candidate_count_out": len(fallback_results),
                    "top_k": request.top_k,
                    "retrieval_mode": retrieval_mode,
                },
                ),
                policy,
            )

    def _decide_rerank_policy(
        self,
        *,
        request: SearchRequest,
        retrieval_mode: str,
        applied_filters: dict[str, Any],
        candidates: list[SearchResult],
    ) -> RerankPolicyDecision:
        source_types = self._split_csv(settings.rerank_default_enablement_source_types)
        route_types = self._split_csv(settings.rerank_default_enablement_route_types)
        keywords = self._split_csv(settings.rerank_default_enablement_keywords)
        candidate_source_types = sorted(
            {
                candidate.source_type
                for candidate in candidates
                if candidate.source_type
            }
        )
        matched_keywords = [keyword for keyword in keywords if keyword in request.query]
        source_type_match = bool(applied_filters.get("source_type") in source_types)
        route_type_match = bool(request.route_type and request.route_type in route_types)
        min_candidates_met = len(candidates) >= settings.rerank_default_enablement_min_candidates
        eligible = min_candidates_met and bool(matched_keywords) and (source_type_match or route_type_match)

        if not settings.rerank_enabled:
            return self._policy_decision(
                enabled=False,
                reason="rerank_globally_disabled",
                retrieval_mode=retrieval_mode,
                request=request,
                applied_filters=applied_filters,
                candidates=candidates,
                candidate_source_types=candidate_source_types,
                matched_keywords=matched_keywords,
                source_type_match=source_type_match,
                route_type_match=route_type_match,
                min_candidates_met=min_candidates_met,
                strategy_active=False,
            )

        if settings.rerank_provider != "aliyun":
            return self._policy_decision(
                enabled=False,
                reason="unsupported_rerank_provider",
                retrieval_mode=retrieval_mode,
                request=request,
                applied_filters=applied_filters,
                candidates=candidates,
                candidate_source_types=candidate_source_types,
                matched_keywords=matched_keywords,
                source_type_match=source_type_match,
                route_type_match=route_type_match,
                min_candidates_met=min_candidates_met,
                strategy_active=False,
            )

        if not settings.rerank_default_enablement_enabled:
            return self._policy_decision(
                enabled=False,
                reason="local_default_enablement_disabled",
                retrieval_mode=retrieval_mode,
                request=request,
                applied_filters=applied_filters,
                candidates=candidates,
                candidate_source_types=candidate_source_types,
                matched_keywords=matched_keywords,
                source_type_match=source_type_match,
                route_type_match=route_type_match,
                min_candidates_met=min_candidates_met,
                strategy_active=False,
            )

        if not min_candidates_met:
            return self._policy_decision(
                enabled=False,
                reason="candidate_pool_below_min_threshold",
                retrieval_mode=retrieval_mode,
                request=request,
                applied_filters=applied_filters,
                candidates=candidates,
                candidate_source_types=candidate_source_types,
                matched_keywords=matched_keywords,
                source_type_match=source_type_match,
                route_type_match=route_type_match,
                min_candidates_met=min_candidates_met,
                strategy_active=True,
            )

        if eligible:
            return self._policy_decision(
                enabled=True,
                reason="local_default_enablement_matched",
                retrieval_mode=retrieval_mode,
                request=request,
                applied_filters=applied_filters,
                candidates=candidates,
                candidate_source_types=candidate_source_types,
                matched_keywords=matched_keywords,
                source_type_match=source_type_match,
                route_type_match=route_type_match,
                min_candidates_met=min_candidates_met,
                strategy_active=True,
            )

        return self._policy_decision(
            enabled=False,
            reason="local_default_enablement_not_matched",
            retrieval_mode=retrieval_mode,
            request=request,
            applied_filters=applied_filters,
            candidates=candidates,
            candidate_source_types=candidate_source_types,
            matched_keywords=matched_keywords,
            source_type_match=source_type_match,
            route_type_match=route_type_match,
            min_candidates_met=min_candidates_met,
            strategy_active=True,
        )

    def _policy_decision(
        self,
        *,
        enabled: bool,
        reason: str,
        retrieval_mode: str,
        request: SearchRequest,
        applied_filters: dict[str, Any],
        candidates: list[SearchResult],
        candidate_source_types: list[str],
        matched_keywords: list[str],
        source_type_match: bool,
        route_type_match: bool,
        min_candidates_met: bool,
        strategy_active: bool,
    ) -> RerankPolicyDecision:
        return RerankPolicyDecision(
            enabled=enabled,
            reason=reason,
            trace={
                "strategy": "phase25_local_default_enablement",
                "strategy_active": strategy_active,
                "enabled": enabled,
                "reason": reason,
                "provider": settings.rerank_provider,
                "global_enabled": settings.rerank_enabled,
                "local_default_enablement_enabled": settings.rerank_default_enablement_enabled,
                "retrieval_mode": retrieval_mode,
                "route_type": request.route_type,
                "applied_source_type": applied_filters.get("source_type"),
                "configured_source_types": self._split_csv(settings.rerank_default_enablement_source_types),
                "configured_route_types": self._split_csv(settings.rerank_default_enablement_route_types),
                "configured_keywords": self._split_csv(settings.rerank_default_enablement_keywords),
                "candidate_source_types": candidate_source_types,
                "matched_keywords": matched_keywords,
                "source_type_match": source_type_match,
                "route_type_match": route_type_match,
                "min_candidates_met": min_candidates_met,
                "candidate_count": len(candidates),
                "min_candidate_threshold": settings.rerank_default_enablement_min_candidates,
            },
        )

    def _with_policy_trace(self, outcome: RerankOutcome, policy: RerankPolicyDecision) -> RerankOutcome:
        trace = {
            **outcome.trace,
            "policy": policy.trace,
            "policy_enabled": policy.enabled,
            "policy_reason": policy.reason,
        }
        if not policy.enabled and outcome.status == "skipped":
            trace["reason"] = policy.reason
            trace["reason_if_skipped"] = policy.reason
        return RerankOutcome(
            results=outcome.results,
            status=outcome.status,
            provider=outcome.provider,
            trace=trace,
        )

    def _split_csv(self, value: str) -> list[str]:
        return [item.strip() for item in value.split(",") if item.strip()]

    def _write_log(
        self,
        trace_id: str,
        request: SearchRequest,
        result_count: int,
        backend: str,
        status: str,
        access_policy_trace: dict[str, Any] | None = None,
        results: list[SearchResult] | None = None,
    ) -> None:
        if self.db is None:
            return
        access_policy_trace = access_policy_trace or {}
        results = results or []
        try:
            self.db.add(
                RetrievalLog(
                    trace_id=trace_id,
                    user_id=access_policy_trace.get("requester_id") or request.user_id,
                    query=request.query,
                    top_k=request.top_k,
                    filters_json=request.filters.model_dump(),
                    result_count=result_count,
                    backend=backend,
                    status=status,
                )
            )
            self._add_audit_event(
                trace_id=trace_id,
                request=request,
                backend=backend,
                status=status,
                access_policy_trace=access_policy_trace,
                results=results,
            )
            self.db.commit()
        except Exception:
            logger.warning("retrieval_audit_log_write_failed", exc_info=True)
            self.db.rollback()

    def _add_audit_event(
        self,
        *,
        trace_id: str,
        request: SearchRequest,
        backend: str,
        status: str,
        access_policy_trace: dict[str, Any],
        results: list[SearchResult],
    ) -> None:
        if self.db is None:
            return
        requester_id = access_policy_trace.get("requester_id") or request.user_id or "local_dev"
        self.db.add(
            AuditLog(
                trace_id=trace_id,
                user_id=requester_id,
                action="retrieval.query",
                resource_type="retrieval",
                resource_id=trace_id,
                request_json={
                    "query": request.query,
                    "filters": request.filters.model_dump(),
                    "top_k": request.top_k,
                    "retrieval_mode": request.retrieval_mode,
                    "requester_id": requester_id,
                    "tenant_id": access_policy_trace.get("tenant_id"),
                    "role": access_policy_trace.get("requester_role"),
                },
                result_json={
                    "backend": backend,
                    "status": status,
                    "returned_document_ids": access_policy_trace.get("returned_document_ids", []),
                    "evidence_chunk_ids": access_policy_trace.get("evidence_chunk_ids", []),
                    "version_ids": access_policy_trace.get("version_ids", []),
                    "evidence_version_ids": access_policy_trace.get("version_ids", []),
                    "policy_decision": access_policy_trace.get("policy_decision"),
                    "policy_reason": access_policy_trace.get("policy_reason"),
                    "denied_document_ids": access_policy_trace.get("denied_document_ids", []),
                    "result_count": len(results),
                },
            )
        )
