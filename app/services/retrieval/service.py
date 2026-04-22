import re
from collections import Counter
from dataclasses import dataclass, field
from time import perf_counter
from typing import Any
from uuid import uuid4

from sqlalchemy import and_, or_
from opensearchpy import OpenSearch
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.logging import get_logger
from app.models.chunk import Chunk
from app.models.document import Document, DocumentVersion
from app.models.retrieval import RetrievalLog
from app.schemas.retrieval import SearchRequest, SearchResponse, SearchResult
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
    def __init__(self, db: Session) -> None:
        self.db = db
        self.dense = self._build_dense_retriever()
        self.reranker = self._build_reranker()

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
                sparse_candidates = self._sparse_search(request, applied_filters)
                sparse_status = "executed"
                sparse_trace = {"backend": "opensearch", "returned": len(sparse_candidates)}
            except Exception:
                logger.exception("opensearch_search_failed_falling_back_to_db")
                backend = "database_fallback" if retrieval_mode == "sparse" else "hybrid_with_database_fallback"
                sparse_candidates = self._database_fallback_search(request, applied_filters)
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

        rerank_outcome = self._rerank_candidates(
            request=request,
            trace_id=trace_id,
            retrieval_mode=retrieval_mode,
            applied_filters=applied_filters,
            candidates=candidate_pool.candidates,
        )
        final_results = rerank_outcome.results[: request.top_k]
        self._write_log(trace_id, request, len(final_results), backend, "success")
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
                "hybrid": {
                    "merged": candidate_pool.trace.get("deduped_count", len(candidate_pool.candidates)),
                    "dedupe_key": "chunk_id",
                    "fusion": "score_sum_by_source",
                } if retrieval_mode == "hybrid" else {},
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

        for field in ("source_type", "document_id", "document_type", "is_latest"):
            value = getattr(filters, field, None)
            if value is not None:
                applied[field] = value

        unsupported = {
            "project_id": filters.project_id,
            "customer_id": filters.customer_id,
            "confidentiality_level": filters.confidentiality_level,
            "permission_tags": filters.permission_tags or None,
            **(filters.extra or {}),
            **(getattr(filters, "model_extra", None) or {}),
        }
        ignored = {key: value for key, value in unsupported.items() if value not in (None, [], {})}
        return applied, ignored

    def _dense_search(self, request: SearchRequest, applied_filters: dict) -> DenseSearchOutcome:
        return self.dense.search(request, applied_filters)

    def _sparse_search(self, request: SearchRequest, applied_filters: dict) -> list[SearchResult]:
        client = OpenSearch(settings.opensearch_url, timeout=5)
        filters: list[dict] = [{"term": {"status": "active"}}]
        if "source_type" in applied_filters:
            filters.append({"term": {"source_type": applied_filters["source_type"]}})
        if "document_id" in applied_filters:
            filters.append({"term": {"document_id": applied_filters["document_id"]}})
        if "document_type" in applied_filters:
            filters.append({"term": {"document_type": applied_filters["document_type"]}})
        if "is_latest" in applied_filters:
            filters.append({"term": {"is_latest": applied_filters["is_latest"]}})

        response = client.search(
            index=settings.opensearch_index_chunks,
            body={
                "size": request.top_k,
                "query": {
                    "bool": {
                        "must": [{"match": {"text": request.query}}],
                        "filter": filters,
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
                    section_path=source.get("heading_path") or [],
                    page_start=source.get("page_start"),
                    page_end=source.get("page_end"),
                    metadata=source.get("metadata_json") or {},
                    retrieval_sources=["sparse"],
                    scores={"sparse": score},
                )
            )
        return results

    def _database_fallback_search(self, request: SearchRequest, applied_filters: dict | None = None) -> list[SearchResult]:
        applied_filters = applied_filters or {}
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
                    metadata=chunk.metadata_json or {},
                    retrieval_sources=["database_fallback"],
                    scores={"database_fallback": 1.0},
                )
            )
        return results

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
    ) -> None:
        self.db.add(
            RetrievalLog(
                trace_id=trace_id,
                user_id=request.user_id,
                query=request.query,
                top_k=request.top_k,
                filters_json=request.filters.model_dump(),
                result_count=result_count,
                backend=backend,
                status=status,
            )
        )
        self.db.commit()
