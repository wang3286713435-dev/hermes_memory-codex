#!/usr/bin/env python
from __future__ import annotations

import argparse
import json
import statistics
import sys
from dataclasses import asdict, dataclass, field
from datetime import datetime
from hashlib import sha256
from time import perf_counter
from typing import Any

from opensearchpy import OpenSearch
from sqlalchemy import text

from app.core.config import settings
from app.db.session import SessionLocal
from app.models.audit import AuditLog
from app.models.chunk import Chunk
from app.models.document import Document, DocumentVersion
from app.schemas.retrieval import RetrievalFilter, SearchRequest, SearchResponse
from app.services.indexing.opensearch import OpenSearchChunkIndexer
from app.services.retrieval.service import RetrievalService


MAIN_TENDER_DOC_ID = "869d4684-0a98-4825-bc72-ada65c15cfc9"
QA_DOC_ID = "1db84714-d49f-48a2-8fa9-c6f73424dd32"
DELIVERY_OLD_DOC_ID = "46372530-ea3d-4442-bd67-23efeb0b70df"
COMPARE_TENDER_DOC_ID = "a47a409f-cb8a-4d29-b938-43c10767802d"
MEETING_DOC_ID = "92051cc6-56b5-4930-bdf0-119163c83a75"
EXCEL_DOC_ID = "976d7376-6fd1-4285-9e8f-5772210d6558"
PPTX_DOC_ID = "ecf7583c-0180-46f9-a013-88480bbcdc3e"
GOV_OPEN_DOC_ID = "phase220-gov-open-doc"
GOV_OPEN_VERSION_ID = "phase220-gov-open-v1"
GOV_OPEN_CHUNK_ID = "phase220-gov-open-chunk-0"
GOV_ALLOW_DOC_ID = "phase220-gov-allow-doc"
GOV_ALLOW_VERSION_ID = "phase220-gov-allow-v1"
GOV_ALLOW_CHUNK_ID = "phase220-gov-allow-chunk-0"
GOV_DENY_DOC_ID = "phase220-gov-deny-doc"
GOV_DENY_VERSION_ID = "phase220-gov-deny-v1"
GOV_DENY_CHUNK_ID = "phase220-gov-deny-chunk-0"
GOV_VERSION_DOC_ID = "phase220-gov-version-doc"
GOV_VERSION_V1_ID = "phase220-gov-version-v1"
GOV_VERSION_V2_ID = "phase220-gov-version-v2"
GOV_VERSION_V1_CHUNK_ID = "phase220-gov-version-v1-chunk-0"
GOV_VERSION_V2_CHUNK_ID = "phase220-gov-version-v2-chunk-0"


@dataclass(frozen=True)
class EvalCase:
    id: str
    query: str
    filters: dict[str, Any]
    group: str = "core"
    user_id: str | None = None
    expected_document_ids: list[str] = field(default_factory=list)
    forbidden_document_ids: list[str] = field(default_factory=list)
    expected_version_ids: list[str] = field(default_factory=list)
    forbidden_version_ids: list[str] = field(default_factory=list)
    required_trace_flags: dict[str, Any] = field(default_factory=dict)
    required_audit_flags: dict[str, Any] = field(default_factory=dict)
    required_citation_fields: list[str] = field(default_factory=list)
    required_dense_status: str | None = None
    min_dense_returned: int | None = None
    required_sparse_status: str | None = None
    min_sparse_returned: int | None = None
    required_candidate_pool_fields: list[str] = field(default_factory=list)
    top_k: int = 5
    retrieval_mode: str = "sparse"
    enable_dense: bool = False
    enable_sparse: bool = True
    enable_hybrid: bool = False
    skip_reason: str | None = None


@dataclass
class EvalResult:
    id: str
    group: str
    passed: bool
    skipped: bool
    latency_ms: float
    returned_document_ids: list[str] = field(default_factory=list)
    returned_version_ids: list[str] = field(default_factory=list)
    expected_document_ids: list[str] = field(default_factory=list)
    expected_version_ids: list[str] = field(default_factory=list)
    missing_expected_document_ids: list[str] = field(default_factory=list)
    missing_expected_version_ids: list[str] = field(default_factory=list)
    unexpected_document_ids: list[str] = field(default_factory=list)
    forbidden_version_ids: list[str] = field(default_factory=list)
    forbidden_document_ids: list[str] = field(default_factory=list)
    missing_citation_fields: list[str] = field(default_factory=list)
    failed_trace_flags: dict[str, dict[str, Any]] = field(default_factory=dict)
    failed_audit_flags: dict[str, dict[str, Any]] = field(default_factory=dict)
    failed_dense_hybrid_checks: dict[str, dict[str, Any]] = field(default_factory=dict)
    policy_decision: str | None = None
    denied_document_ids: list[str] = field(default_factory=list)
    audit_event_written: bool | None = None
    evidence_version_ids: list[str] = field(default_factory=list)
    stale_version: bool | None = None
    latest_version_id: str | None = None
    error: str | None = None


def builtin_eval_cases() -> list[EvalCase]:
    return [
        EvalCase(
            id="tender_main_basic_info_snapshot",
            group="core",
            query="工程地点、建设单位、代建单位分别是什么？",
            filters={"document_id": MAIN_TENDER_DOC_ID, "source_type": "tender", "document_type": "tender"},
            expected_document_ids=[MAIN_TENDER_DOC_ID],
            forbidden_document_ids=[MEETING_DOC_ID, COMPARE_TENDER_DOC_ID],
            required_trace_flags={
                "metadata_snapshot_used": True,
                "snapshot_as_answer": False,
                "evidence_required": True,
            },
            retrieval_mode="hybrid",
            enable_dense=True,
            enable_sparse=True,
            enable_hybrid=True,
            required_dense_status="executed",
            min_dense_returned=1,
            required_sparse_status="executed",
            min_sparse_returned=1,
            required_candidate_pool_fields=["dense_returned", "sparse_returned", "deduped_count"],
        ),
        EvalCase(
            id="qa_doc_single_file_scope",
            group="core",
            query="答疑补遗文件中说明了哪些补充内容？",
            filters={"document_id": QA_DOC_ID, "source_type": "tender", "document_type": "tender"},
            expected_document_ids=[QA_DOC_ID],
            forbidden_document_ids=[MAIN_TENDER_DOC_ID, DELIVERY_OLD_DOC_ID, MEETING_DOC_ID],
        ),
        EvalCase(
            id="delivery_standard_old_scope",
            group="core",
            query="数字化交付标准有哪些主要要求？",
            filters={"document_id": DELIVERY_OLD_DOC_ID, "source_type": "tender", "document_type": "tender"},
            expected_document_ids=[DELIVERY_OLD_DOC_ID],
            forbidden_document_ids=[QA_DOC_ID, MAIN_TENDER_DOC_ID, MEETING_DOC_ID],
        ),
        EvalCase(
            id="main_tender_schedule_no_compare_pollution",
            group="core",
            query="总工期和关键节点怎么要求？",
            filters={"document_id": MAIN_TENDER_DOC_ID, "source_type": "tender", "document_type": "tender"},
            expected_document_ids=[MAIN_TENDER_DOC_ID],
            forbidden_document_ids=[COMPARE_TENDER_DOC_ID, MEETING_DOC_ID],
            retrieval_mode="hybrid",
            enable_dense=True,
            enable_sparse=True,
            enable_hybrid=True,
            required_dense_status="executed",
            min_dense_returned=1,
            required_sparse_status="executed",
            min_sparse_returned=1,
            required_candidate_pool_fields=["dense_returned", "sparse_returned", "deduped_count"],
        ),
        EvalCase(
            id="compare_tender_schedule_no_main_pollution",
            group="core",
            query="总工期和关键节点怎么要求？",
            filters={"document_id": COMPARE_TENDER_DOC_ID, "source_type": "tender", "document_type": "tender"},
            expected_document_ids=[COMPARE_TENDER_DOC_ID],
            forbidden_document_ids=[MAIN_TENDER_DOC_ID, MEETING_DOC_ID],
            retrieval_mode="hybrid",
            enable_dense=True,
            enable_sparse=True,
            enable_hybrid=True,
            required_dense_status="executed",
            min_dense_returned=1,
            required_sparse_status="executed",
            min_sparse_returned=1,
            required_candidate_pool_fields=["dense_returned", "sparse_returned", "deduped_count"],
        ),
        EvalCase(
            id="excel_sheet_cell_citation",
            group="core",
            query="投标总价 付款比例",
            filters={"document_id": EXCEL_DOC_ID, "document_type": "xlsx"},
            expected_document_ids=[EXCEL_DOC_ID],
            forbidden_document_ids=[MAIN_TENDER_DOC_ID, PPTX_DOC_ID],
            required_citation_fields=["sheet_name", "cell_range"],
        ),
        EvalCase(
            id="pptx_slide_citation",
            group="core",
            query="智慧建筑脑机系统这一页讲了什么？",
            filters={"document_id": PPTX_DOC_ID, "document_type": "pptx"},
            expected_document_ids=[PPTX_DOC_ID],
            forbidden_document_ids=[EXCEL_DOC_ID, MAIN_TENDER_DOC_ID],
            required_citation_fields=["slide_number", "slide_title"],
        ),
        EvalCase(
            id="meeting_action_items",
            group="core",
            query="会议里有哪些行动项？",
            filters={"document_id": MEETING_DOC_ID, "source_type": "meeting", "document_type": "meeting"},
            expected_document_ids=[MEETING_DOC_ID],
            forbidden_document_ids=[MAIN_TENDER_DOC_ID, QA_DOC_ID],
            required_trace_flags={
                "meeting_transcript_used": True,
                "transcript_as_fact": False,
                "evidence_required": True,
            },
            required_citation_fields=["action_item", "source_chunk_id"],
        ),
        EvalCase(
            id="meeting_decisions",
            group="core",
            query="会议里形成了哪些决策？",
            filters={"document_id": MEETING_DOC_ID, "source_type": "meeting", "document_type": "meeting"},
            expected_document_ids=[MEETING_DOC_ID],
            forbidden_document_ids=[MAIN_TENDER_DOC_ID, QA_DOC_ID],
            required_trace_flags={
                "meeting_transcript_used": True,
                "transcript_as_fact": False,
                "evidence_required": True,
            },
            required_citation_fields=["decision", "source_chunk_id"],
        ),
        EvalCase(
            id="meeting_risks",
            group="core",
            query="会议中提到哪些风险？",
            filters={"document_id": MEETING_DOC_ID, "source_type": "meeting", "document_type": "meeting"},
            expected_document_ids=[MEETING_DOC_ID],
            forbidden_document_ids=[MAIN_TENDER_DOC_ID, QA_DOC_ID],
            required_trace_flags={
                "meeting_transcript_used": True,
                "transcript_as_fact": False,
                "evidence_required": True,
            },
            required_citation_fields=["risk", "source_chunk_id"],
        ),
        EvalCase(
            id="meeting_hybrid_dense_smoke",
            group="core",
            query="会议纪要 行动项 决策 风险",
            filters={"document_id": MEETING_DOC_ID, "source_type": "meeting", "document_type": "meeting"},
            expected_document_ids=[MEETING_DOC_ID],
            forbidden_document_ids=[MAIN_TENDER_DOC_ID, QA_DOC_ID],
            retrieval_mode="hybrid",
            enable_dense=True,
            enable_sparse=True,
            enable_hybrid=True,
            required_dense_status="executed",
            min_dense_returned=1,
            required_sparse_status="executed",
            min_sparse_returned=1,
            required_candidate_pool_fields=["dense_returned", "sparse_returned", "deduped_count"],
        ),
        EvalCase(
            id="gov_access_no_acl_not_configured_allow",
            group="governance",
            query="phase220 open access keyword",
            filters={"document_id": GOV_OPEN_DOC_ID, "source_type": "phase220", "document_type": "txt"},
            expected_document_ids=[GOV_OPEN_DOC_ID],
            expected_version_ids=[GOV_OPEN_VERSION_ID],
            required_trace_flags={
                "access_policy.policy_decision": "not_configured_allow",
                "access_policy.denied_document_ids": [],
            },
            required_audit_flags={
                "request_json.requester_id": "local_dev",
                "result_json.policy_decision": "not_configured_allow",
                "result_json.returned_document_ids": [GOV_OPEN_DOC_ID],
                "result_json.evidence_chunk_ids": [GOV_OPEN_CHUNK_ID],
                "result_json.evidence_version_ids": [GOV_OPEN_VERSION_ID],
            },
        ),
        EvalCase(
            id="gov_access_requester_allow",
            group="governance",
            query="phase220 requester allow keyword",
            user_id="phase220-user",
            filters={
                "document_id": GOV_ALLOW_DOC_ID,
                "source_type": "phase220",
                "document_type": "txt",
                "extra": {"tenant_id": "phase220-tenant", "role": "staff"},
            },
            expected_document_ids=[GOV_ALLOW_DOC_ID],
            expected_version_ids=[GOV_ALLOW_VERSION_ID],
            required_trace_flags={
                "access_policy.policy_decision": "allow",
                "access_policy.denied_document_ids": [],
            },
            required_audit_flags={
                "request_json.requester_id": "phase220-user",
                "result_json.policy_decision": "allow",
                "result_json.returned_document_ids": [GOV_ALLOW_DOC_ID],
                "result_json.evidence_chunk_ids": [GOV_ALLOW_CHUNK_ID],
                "result_json.evidence_version_ids": [GOV_ALLOW_VERSION_ID],
            },
        ),
        EvalCase(
            id="gov_access_tenant_mismatch_deny",
            group="governance",
            query="phase220 tenant deny keyword",
            user_id="phase220-user",
            filters={
                "document_id": GOV_DENY_DOC_ID,
                "source_type": "phase220",
                "document_type": "txt",
                "extra": {"tenant_id": "other-tenant", "role": "staff"},
            },
            forbidden_document_ids=[GOV_DENY_DOC_ID],
            forbidden_version_ids=[GOV_DENY_VERSION_ID],
            required_trace_flags={
                "access_policy.policy_decision": "deny",
                "access_policy.denied_document_ids": [GOV_DENY_DOC_ID],
                "access_policy.returned_document_ids": [],
            },
            required_audit_flags={
                "request_json.requester_id": "phase220-user",
                "result_json.policy_decision": "deny",
                "result_json.denied_document_ids": [GOV_DENY_DOC_ID],
                "result_json.returned_document_ids": [],
                "result_json.evidence_chunk_ids": [],
                "result_json.evidence_version_ids": [],
            },
        ),
        EvalCase(
            id="gov_version_default_latest_only",
            group="governance",
            query="phase220 version governance keyword",
            filters={"document_id": GOV_VERSION_DOC_ID, "source_type": "phase220", "document_type": "txt"},
            expected_document_ids=[GOV_VERSION_DOC_ID],
            expected_version_ids=[GOV_VERSION_V2_ID],
            forbidden_version_ids=[GOV_VERSION_V1_ID],
            required_trace_flags={
                "version_policy": "latest_only",
                "version_scope.stale_version": False,
            },
            required_audit_flags={
                "result_json.returned_document_ids": [GOV_VERSION_DOC_ID],
                "result_json.evidence_version_ids": [GOV_VERSION_V2_ID],
            },
        ),
        EvalCase(
            id="gov_version_explicit_old_version",
            group="governance",
            query="phase220 version governance keyword",
            filters={
                "document_id": GOV_VERSION_DOC_ID,
                "source_type": "phase220",
                "document_type": "txt",
                "extra": {"version_id": GOV_VERSION_V1_ID},
            },
            expected_document_ids=[GOV_VERSION_DOC_ID],
            expected_version_ids=[GOV_VERSION_V1_ID],
            forbidden_version_ids=[GOV_VERSION_V2_ID],
            required_trace_flags={
                "version_policy": "explicit_history_version",
                "version_scope.stale_version": True,
                "version_scope.latest_version_id": GOV_VERSION_V2_ID,
            },
            required_audit_flags={
                "result_json.returned_document_ids": [GOV_VERSION_DOC_ID],
                "result_json.evidence_version_ids": [GOV_VERSION_V1_ID],
            },
        ),
        EvalCase(
            id="missing_alias_suppress_cli_only",
            group="cli_only",
            query="围绕 @不存在的别名 回答",
            filters={},
            skip_reason="CLI-only: alias state and suppress_retrieval live in Hermes session layer.",
        ),
    ]


def evaluate_case_response(
    case: EvalCase,
    response: SearchResponse,
    latency_ms: float,
    audit_event: AuditLog | None = None,
) -> EvalResult:
    returned_ids = _unique(result.document_id for result in response.results)
    returned_version_ids = _unique(result.version_id for result in response.results)
    expected = list(case.expected_document_ids)
    expected_versions = list(case.expected_version_ids)
    missing_expected = [document_id for document_id in expected if document_id not in returned_ids]
    missing_expected_versions = [version_id for version_id in expected_versions if version_id not in returned_version_ids]
    forbidden_hits = [document_id for document_id in case.forbidden_document_ids if document_id in returned_ids]
    forbidden_version_hits = [version_id for version_id in case.forbidden_version_ids if version_id in returned_version_ids]
    unexpected = [document_id for document_id in returned_ids if expected and document_id not in expected]
    missing_fields = _missing_citation_fields(response, case.required_citation_fields)
    failed_trace_flags = _failed_trace_flags(response.trace or {}, case.required_trace_flags)
    failed_audit_flags = _failed_audit_flags(audit_event, case.required_audit_flags)
    failed_dense_hybrid_checks = _failed_dense_hybrid_checks(response, case)
    access_policy = _dict_value(response.trace, "access_policy")
    version_scope = _dict_value(response.trace, "version_scope")
    audit_result = audit_event.result_json if audit_event and isinstance(audit_event.result_json, dict) else {}
    passed = not (
        missing_expected
        or missing_expected_versions
        or forbidden_hits
        or forbidden_version_hits
        or unexpected
        or missing_fields
        or failed_trace_flags
        or failed_audit_flags
        or failed_dense_hybrid_checks
    )
    return EvalResult(
        id=case.id,
        group=case.group,
        passed=passed,
        skipped=False,
        latency_ms=latency_ms,
        returned_document_ids=returned_ids,
        returned_version_ids=returned_version_ids,
        expected_document_ids=expected,
        expected_version_ids=expected_versions,
        missing_expected_document_ids=missing_expected,
        missing_expected_version_ids=missing_expected_versions,
        unexpected_document_ids=unexpected,
        forbidden_document_ids=forbidden_hits,
        forbidden_version_ids=forbidden_version_hits,
        missing_citation_fields=missing_fields,
        failed_trace_flags=failed_trace_flags,
        failed_audit_flags=failed_audit_flags,
        failed_dense_hybrid_checks=failed_dense_hybrid_checks,
        policy_decision=access_policy.get("policy_decision"),
        denied_document_ids=access_policy.get("denied_document_ids") or [],
        audit_event_written=audit_event is not None,
        evidence_version_ids=audit_result.get("evidence_version_ids") or access_policy.get("version_ids") or [],
        stale_version=version_scope.get("stale_version"),
        latest_version_id=version_scope.get("latest_version_id"),
    )


def run_eval_cases(cases: list[EvalCase] | None = None) -> dict[str, Any]:
    cases = cases or builtin_eval_cases()
    environment = check_dependencies()
    if not environment["ok"]:
        return {
            "environment": environment,
            "total": len(cases),
            "passed": 0,
            "failed": len([case for case in cases if not case.skip_reason]),
            "skipped": len([case for case in cases if case.skip_reason]),
            "latency_ms": {"p50": None, "p95": None},
            "cases": [],
        }

    db = SessionLocal()
    try:
        if any(case.group == "governance" for case in cases):
            prepare_governance_fixtures(db)
        service = RetrievalService(db)
        results: list[EvalResult] = []
        for case in cases:
            if case.skip_reason:
                results.append(EvalResult(id=case.id, group=case.group, passed=False, skipped=True, latency_ms=0.0, error=case.skip_reason))
                continue
            started = perf_counter()
            try:
                response = service.search(
                    SearchRequest(
                        query=case.query,
                        user_id=case.user_id,
                        top_k=case.top_k,
                        retrieval_mode=case.retrieval_mode,  # type: ignore[arg-type]
                        enable_dense=case.enable_dense,
                        enable_sparse=case.enable_sparse,
                        enable_hybrid=case.enable_hybrid,
                        filters=RetrievalFilter(**case.filters),
                        include_citations=True,
                    )
                )
                elapsed_ms = (perf_counter() - started) * 1000
                audit_event = _audit_event_for_trace(db, response.trace.get("trace_id"))
                results.append(evaluate_case_response(case, response, elapsed_ms, audit_event))
            except Exception as exc:  # pragma: no cover - exercised by live failure only
                elapsed_ms = (perf_counter() - started) * 1000
                results.append(EvalResult(id=case.id, group=case.group, passed=False, skipped=False, latency_ms=elapsed_ms, error=repr(exc)))
    finally:
        db.close()

    executed = [result for result in results if not result.skipped]
    passed = len([result for result in executed if result.passed])
    failed = len([result for result in executed if not result.passed])
    latencies = [result.latency_ms for result in executed]
    return {
        "environment": environment,
        "total": len(cases),
        "passed": passed,
        "failed": failed,
        "skipped": len([result for result in results if result.skipped]),
        "latency_ms": {
            "p50": _percentile(latencies, 50),
            "p95": _percentile(latencies, 95),
        },
        "groups": _group_stats(results),
        "cases": [asdict(result) for result in results],
    }


def prepare_governance_fixtures(db) -> None:
    indexer = OpenSearchChunkIndexer()
    fixtures = [
        {
            "document_id": GOV_OPEN_DOC_ID,
            "version_id": GOV_OPEN_VERSION_ID,
            "chunk_id": GOV_OPEN_CHUNK_ID,
            "title": "Phase 2.20 governance eval open acl",
            "text": "phase220 open access keyword evidence for not configured allow.",
            "metadata": {},
            "is_latest": True,
        },
        {
            "document_id": GOV_ALLOW_DOC_ID,
            "version_id": GOV_ALLOW_VERSION_ID,
            "chunk_id": GOV_ALLOW_CHUNK_ID,
            "title": "Phase 2.20 governance eval requester allow",
            "text": "phase220 requester allow keyword evidence for requester allow.",
            "metadata": {"allowed_requester_ids": ["phase220-user"], "tenant_id": "phase220-tenant"},
            "is_latest": True,
        },
        {
            "document_id": GOV_DENY_DOC_ID,
            "version_id": GOV_DENY_VERSION_ID,
            "chunk_id": GOV_DENY_CHUNK_ID,
            "title": "Phase 2.20 governance eval tenant deny",
            "text": "phase220 tenant deny keyword evidence that must be denied for other tenant.",
            "metadata": {"tenant_id": "phase220-tenant-a"},
            "is_latest": True,
        },
        {
            "document_id": GOV_VERSION_DOC_ID,
            "version_id": GOV_VERSION_V1_ID,
            "chunk_id": GOV_VERSION_V1_CHUNK_ID,
            "title": "Phase 2.20 governance eval version fixture",
            "text": "phase220 version governance keyword old version amount 100.",
            "metadata": {"version_status": "superseded", "superseded_by_version_id": GOV_VERSION_V2_ID},
            "is_latest": False,
        },
        {
            "document_id": GOV_VERSION_DOC_ID,
            "version_id": GOV_VERSION_V2_ID,
            "chunk_id": GOV_VERSION_V2_CHUNK_ID,
            "title": "Phase 2.20 governance eval version fixture",
            "text": "phase220 version governance keyword latest version amount 200.",
            "metadata": {"version_status": "active"},
            "is_latest": True,
        },
    ]
    for item in fixtures:
        document = _upsert_document(
            db,
            document_id=item["document_id"],
            title=item["title"],
            metadata=item["metadata"] if item["document_id"] != GOV_VERSION_DOC_ID else {"current_version_id": GOV_VERSION_V2_ID},
        )
        version = _upsert_version(
            db,
            document_id=item["document_id"],
            version_id=item["version_id"],
            is_latest=item["is_latest"],
            metadata=item["metadata"],
        )
        chunk = _upsert_chunk(
            db,
            document_id=item["document_id"],
            version_id=item["version_id"],
            chunk_id=item["chunk_id"],
            text=item["text"],
        )
        db.commit()
        indexer.index_chunk(chunk, document, version)


def _upsert_document(db, *, document_id: str, title: str, metadata: dict[str, Any]) -> Document:
    document = db.get(Document, document_id)
    if document is None:
        document = Document(id=document_id)
        db.add(document)
    document.title = title
    document.source_type = "phase220"
    document.source_uri = f"{document_id}.txt"
    document.storage_uri = f"phase220://{document_id}.txt"
    document.document_type = "txt"
    document.status = "active"
    document.confidentiality_level = "internal"
    document.metadata_json = metadata
    return document


def _upsert_version(db, *, document_id: str, version_id: str, is_latest: bool, metadata: dict[str, Any]) -> DocumentVersion:
    version = db.get(DocumentVersion, version_id)
    if version is None:
        version = DocumentVersion(id=version_id, document_id=document_id)
        db.add(version)
    version.document_id = document_id
    version.version_name = "v2" if is_latest else "v1"
    version.version_number = "2" if is_latest else "1"
    version.file_hash = sha256(version_id.encode("utf-8")).hexdigest()
    version.content_hash = sha256(f"{document_id}:{version_id}".encode("utf-8")).hexdigest()
    version.is_latest = is_latest
    version.parse_status = "completed"
    version.effective_at = datetime.utcnow()
    version.expired_at = None if is_latest else datetime.utcnow()
    version.metadata_json = metadata
    return version


def _upsert_chunk(db, *, document_id: str, version_id: str, chunk_id: str, text: str) -> Chunk:
    chunk = db.get(Chunk, chunk_id)
    if chunk is None:
        chunk = Chunk(id=chunk_id, document_id=document_id, version_id=version_id)
        db.add(chunk)
    chunk.document_id = document_id
    chunk.version_id = version_id
    chunk.chunk_index = 0
    chunk.text = text
    chunk.heading_path = ["Phase 2.20 governance eval"]
    chunk.title_path = ["Phase 2.20 governance eval"]
    chunk.section_path = ["Phase 2.20 governance eval"]
    chunk.page_start = None
    chunk.page_end = None
    chunk.char_count = len(text)
    chunk.content_hash = sha256(text.encode("utf-8")).hexdigest()
    chunk.token_count = len(text)
    chunk.source_type = "phase220"
    chunk.metadata_json = {"source_chunk_id": chunk_id}
    chunk.permission_tags = []
    return chunk


def check_dependencies() -> dict[str, Any]:
    status = {"ok": True, "db": "ok", "opensearch": "ok", "errors": []}
    try:
        db = SessionLocal()
        try:
            db.execute(text("SELECT 1"))
        finally:
            db.close()
    except Exception as exc:
        status["ok"] = False
        status["db"] = "failed"
        status["errors"].append({"layer": "db", "error": repr(exc)})

    try:
        client = OpenSearch(settings.opensearch_url, timeout=3)
        if not client.ping():
            raise RuntimeError("OpenSearch ping returned false")
    except Exception as exc:
        status["ok"] = False
        status["opensearch"] = "failed"
        status["errors"].append({"layer": "opensearch", "error": repr(exc)})
    return status


def _missing_citation_fields(response: SearchResponse, required_fields: list[str]) -> list[str]:
    if not required_fields:
        return []
    return [field for field in required_fields if not _field_present(response, field)]


def _field_present(response: SearchResponse, field: str) -> bool:
    for result in response.results:
        metadata = result.metadata or {}
        value = _get_path(metadata, field)
        if _non_empty(value):
            return True
    for citation in response.citations or []:
        if _non_empty(_get_path(citation, field)):
            return True
        metadata = citation.get("metadata") if isinstance(citation, dict) else None
        if isinstance(metadata, dict) and _non_empty(_get_path(metadata, field)):
            return True
    return False


def _failed_trace_flags(trace: dict[str, Any], required_flags: dict[str, Any]) -> dict[str, dict[str, Any]]:
    failed = {}
    for path, expected in required_flags.items():
        actual = _get_path(trace, path)
        if actual != expected:
            failed[path] = {"expected": expected, "actual": actual}
    return failed


def _failed_audit_flags(audit_event: AuditLog | None, required_flags: dict[str, Any]) -> dict[str, dict[str, Any]]:
    if not required_flags:
        return {}
    if audit_event is None:
        return {
            path: {"expected": expected, "actual": None, "error": "audit_event_missing"}
            for path, expected in required_flags.items()
        }
    audit_payload = {
        "trace_id": audit_event.trace_id,
        "user_id": audit_event.user_id,
        "action": audit_event.action,
        "resource_type": audit_event.resource_type,
        "resource_id": audit_event.resource_id,
        "request_json": audit_event.request_json or {},
        "result_json": audit_event.result_json or {},
    }
    failed = {}
    for path, expected in required_flags.items():
        actual = _get_path(audit_payload, path)
        if actual != expected:
            failed[path] = {"expected": expected, "actual": actual}
    return failed


def _failed_dense_hybrid_checks(response: SearchResponse, case: EvalCase) -> dict[str, dict[str, Any]]:
    failed: dict[str, dict[str, Any]] = {}
    trace = response.trace or {}
    dense_trace = trace.get("dense") if isinstance(trace.get("dense"), dict) else {}
    sparse_trace = trace.get("sparse") if isinstance(trace.get("sparse"), dict) else {}
    candidate_pool = trace.get("candidate_pool") if isinstance(trace.get("candidate_pool"), dict) else {}

    if case.required_dense_status is not None and response.dense_status != case.required_dense_status:
        failed["dense_status"] = {"expected": case.required_dense_status, "actual": response.dense_status}
    dense_returned = _int_value(dense_trace.get("returned"), candidate_pool.get("dense_returned"))
    if case.min_dense_returned is not None and dense_returned < case.min_dense_returned:
        failed["dense_returned"] = {"expected_min": case.min_dense_returned, "actual": dense_returned}

    if case.required_sparse_status is not None and response.sparse_status != case.required_sparse_status:
        failed["sparse_status"] = {"expected": case.required_sparse_status, "actual": response.sparse_status}
    sparse_returned = _int_value(sparse_trace.get("returned"), candidate_pool.get("sparse_returned"))
    if case.min_sparse_returned is not None and sparse_returned < case.min_sparse_returned:
        failed["sparse_returned"] = {"expected_min": case.min_sparse_returned, "actual": sparse_returned}

    for field in case.required_candidate_pool_fields:
        if not _non_empty(_get_path(candidate_pool, field)):
            failed[f"candidate_pool.{field}"] = {"expected": "present", "actual": _get_path(candidate_pool, field)}
    return failed


def _int_value(*values: Any) -> int:
    for value in values:
        if value is None:
            continue
        try:
            return int(value)
        except (TypeError, ValueError):
            continue
    return 0


def _get_path(data: dict[str, Any], path: str) -> Any:
    current: Any = data
    for part in path.split("."):
        if not isinstance(current, dict) or part not in current:
            return None
        current = current[part]
    return current


def _dict_value(data: dict[str, Any], path: str) -> dict[str, Any]:
    value = _get_path(data, path)
    return value if isinstance(value, dict) else {}


def _audit_event_for_trace(db, trace_id: str | None) -> AuditLog | None:
    if not trace_id:
        return None
    return (
        db.query(AuditLog)
        .filter(AuditLog.trace_id == trace_id)
        .filter(AuditLog.action == "retrieval.query")
        .order_by(AuditLog.created_at.desc())
        .first()
    )


def _group_stats(results: list[EvalResult]) -> dict[str, dict[str, int]]:
    stats: dict[str, dict[str, int]] = {}
    for result in results:
        group = result.group or "core"
        item = stats.setdefault(group, {"total": 0, "passed": 0, "failed": 0, "skipped": 0})
        item["total"] += 1
        if result.skipped:
            item["skipped"] += 1
        elif result.passed:
            item["passed"] += 1
        else:
            item["failed"] += 1
    return stats


def _non_empty(value: Any) -> bool:
    return value not in (None, "", [], {})


def _unique(values: Any) -> list[str]:
    output: list[str] = []
    for value in values:
        if value and value not in output:
            output.append(str(value))
    return output


def _percentile(values: list[float], percentile: int) -> float | None:
    if not values:
        return None
    if len(values) == 1:
        return round(values[0], 3)
    sorted_values = sorted(values)
    if percentile == 50:
        return round(float(statistics.median(sorted_values)), 3)
    rank = (len(sorted_values) - 1) * percentile / 100
    lower = int(rank)
    upper = min(lower + 1, len(sorted_values) - 1)
    weight = rank - lower
    return round(float(sorted_values[lower] * (1 - weight) + sorted_values[upper] * weight), 3)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run Phase 2.14 deterministic regression eval.")
    parser.add_argument("--json", action="store_true", help="Print JSON summary. Kept for explicit script usage.")
    parser.add_argument(
        "--group",
        action="append",
        default=[],
        help="Run only cases in the given group. Can be repeated, e.g. --group core --group governance.",
    )
    args = parser.parse_args(argv)
    cases = builtin_eval_cases()
    if args.group:
        allowed_groups = set(args.group)
        cases = [case for case in cases if case.group in allowed_groups]
    summary = run_eval_cases(cases)
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0 if summary["environment"]["ok"] and summary["failed"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
