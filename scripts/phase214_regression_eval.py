#!/usr/bin/env python
from __future__ import annotations

import argparse
import json
import statistics
import sys
from dataclasses import asdict, dataclass, field
from time import perf_counter
from typing import Any

from opensearchpy import OpenSearch
from sqlalchemy import text

from app.core.config import settings
from app.db.session import SessionLocal
from app.schemas.retrieval import RetrievalFilter, SearchRequest, SearchResponse
from app.services.retrieval.service import RetrievalService


MAIN_TENDER_DOC_ID = "869d4684-0a98-4825-bc72-ada65c15cfc9"
QA_DOC_ID = "1db84714-d49f-48a2-8fa9-c6f73424dd32"
DELIVERY_OLD_DOC_ID = "46372530-ea3d-4442-bd67-23efeb0b70df"
COMPARE_TENDER_DOC_ID = "a47a409f-cb8a-4d29-b938-43c10767802d"
MEETING_DOC_ID = "92051cc6-56b5-4930-bdf0-119163c83a75"
EXCEL_DOC_ID = "976d7376-6fd1-4285-9e8f-5772210d6558"
PPTX_DOC_ID = "ecf7583c-0180-46f9-a013-88480bbcdc3e"


@dataclass(frozen=True)
class EvalCase:
    id: str
    query: str
    filters: dict[str, Any]
    expected_document_ids: list[str] = field(default_factory=list)
    forbidden_document_ids: list[str] = field(default_factory=list)
    required_trace_flags: dict[str, Any] = field(default_factory=dict)
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
    passed: bool
    skipped: bool
    latency_ms: float
    returned_document_ids: list[str] = field(default_factory=list)
    expected_document_ids: list[str] = field(default_factory=list)
    missing_expected_document_ids: list[str] = field(default_factory=list)
    unexpected_document_ids: list[str] = field(default_factory=list)
    forbidden_document_ids: list[str] = field(default_factory=list)
    missing_citation_fields: list[str] = field(default_factory=list)
    failed_trace_flags: dict[str, dict[str, Any]] = field(default_factory=dict)
    failed_dense_hybrid_checks: dict[str, dict[str, Any]] = field(default_factory=dict)
    error: str | None = None


def builtin_eval_cases() -> list[EvalCase]:
    return [
        EvalCase(
            id="tender_main_basic_info_snapshot",
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
            query="答疑补遗文件中说明了哪些补充内容？",
            filters={"document_id": QA_DOC_ID, "source_type": "tender", "document_type": "tender"},
            expected_document_ids=[QA_DOC_ID],
            forbidden_document_ids=[MAIN_TENDER_DOC_ID, DELIVERY_OLD_DOC_ID, MEETING_DOC_ID],
        ),
        EvalCase(
            id="delivery_standard_old_scope",
            query="数字化交付标准有哪些主要要求？",
            filters={"document_id": DELIVERY_OLD_DOC_ID, "source_type": "tender", "document_type": "tender"},
            expected_document_ids=[DELIVERY_OLD_DOC_ID],
            forbidden_document_ids=[QA_DOC_ID, MAIN_TENDER_DOC_ID, MEETING_DOC_ID],
        ),
        EvalCase(
            id="main_tender_schedule_no_compare_pollution",
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
            query="投标总价 付款比例",
            filters={"document_id": EXCEL_DOC_ID, "document_type": "xlsx"},
            expected_document_ids=[EXCEL_DOC_ID],
            forbidden_document_ids=[MAIN_TENDER_DOC_ID, PPTX_DOC_ID],
            required_citation_fields=["sheet_name", "cell_range"],
        ),
        EvalCase(
            id="pptx_slide_citation",
            query="智慧建筑脑机系统这一页讲了什么？",
            filters={"document_id": PPTX_DOC_ID, "document_type": "pptx"},
            expected_document_ids=[PPTX_DOC_ID],
            forbidden_document_ids=[EXCEL_DOC_ID, MAIN_TENDER_DOC_ID],
            required_citation_fields=["slide_number", "slide_title"],
        ),
        EvalCase(
            id="meeting_action_items",
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
            id="missing_alias_suppress_cli_only",
            query="围绕 @不存在的别名 回答",
            filters={},
            skip_reason="CLI-only: alias state and suppress_retrieval live in Hermes session layer.",
        ),
    ]


def evaluate_case_response(case: EvalCase, response: SearchResponse, latency_ms: float) -> EvalResult:
    returned_ids = _unique(result.document_id for result in response.results)
    expected = list(case.expected_document_ids)
    missing_expected = [document_id for document_id in expected if document_id not in returned_ids]
    forbidden_hits = [document_id for document_id in case.forbidden_document_ids if document_id in returned_ids]
    unexpected = [document_id for document_id in returned_ids if expected and document_id not in expected]
    missing_fields = _missing_citation_fields(response, case.required_citation_fields)
    failed_trace_flags = _failed_trace_flags(response.trace or {}, case.required_trace_flags)
    failed_dense_hybrid_checks = _failed_dense_hybrid_checks(response, case)
    passed = not (
        missing_expected
        or forbidden_hits
        or unexpected
        or missing_fields
        or failed_trace_flags
        or failed_dense_hybrid_checks
    )
    return EvalResult(
        id=case.id,
        passed=passed,
        skipped=False,
        latency_ms=latency_ms,
        returned_document_ids=returned_ids,
        expected_document_ids=expected,
        missing_expected_document_ids=missing_expected,
        unexpected_document_ids=unexpected,
        forbidden_document_ids=forbidden_hits,
        missing_citation_fields=missing_fields,
        failed_trace_flags=failed_trace_flags,
        failed_dense_hybrid_checks=failed_dense_hybrid_checks,
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
        service = RetrievalService(db)
        results: list[EvalResult] = []
        for case in cases:
            if case.skip_reason:
                results.append(EvalResult(id=case.id, passed=False, skipped=True, latency_ms=0.0, error=case.skip_reason))
                continue
            started = perf_counter()
            try:
                response = service.search(
                    SearchRequest(
                        query=case.query,
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
                results.append(evaluate_case_response(case, response, elapsed_ms))
            except Exception as exc:  # pragma: no cover - exercised by live failure only
                elapsed_ms = (perf_counter() - started) * 1000
                results.append(EvalResult(id=case.id, passed=False, skipped=False, latency_ms=elapsed_ms, error=repr(exc)))
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
        "cases": [asdict(result) for result in results],
    }


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
    args = parser.parse_args(argv)
    summary = run_eval_cases()
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0 if summary["environment"]["ok"] and summary["failed"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
