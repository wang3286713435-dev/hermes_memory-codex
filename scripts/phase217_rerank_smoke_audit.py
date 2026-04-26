#!/usr/bin/env python
from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass, field
from time import perf_counter
from typing import Any

from sqlalchemy import text

from app.core.config import settings
from app.db.session import SessionLocal
from app.schemas.retrieval import RetrievalFilter, SearchRequest
from app.services.retrieval.service import RetrievalService


MAIN_TENDER_DOC_ID = "869d4684-0a98-4825-bc72-ada65c15cfc9"
QA_DOC_ID = "1db84714-d49f-48a2-8fa9-c6f73424dd32"
EXCEL_DOC_ID = "976d7376-6fd1-4285-9e8f-5772210d6558"
PPTX_DOC_ID = "ecf7583c-0180-46f9-a013-88480bbcdc3e"
MEETING_DOC_ID = "92051cc6-56b5-4930-bdf0-119163c83a75"


@dataclass(frozen=True)
class RerankSmokeCase:
    id: str
    query: str
    filters: dict[str, Any]
    route_type: str | None = None
    top_k: int = 5
    expect_policy_match: bool = False
    allow_skipped: bool = False


@dataclass
class RerankSmokeResult:
    id: str
    passed: bool
    latency_ms: float
    rerank_status: str | None = None
    rerank_provider: str | None = None
    rerank_model: str | None = None
    rerank_returned: int = 0
    rerank_latency_ms: float = 0.0
    fail_open: bool = False
    fail_open_reason: str | None = None
    error_type: str | None = None
    api_key_source: str | None = None
    policy_reason: str | None = None
    policy_enabled: bool = False
    matched_keywords: list[str] = field(default_factory=list)
    candidate_count: int = 0
    result_document_ids: list[str] = field(default_factory=list)
    error: str | None = None


def builtin_cases() -> list[RerankSmokeCase]:
    return [
        RerankSmokeCase(
            id="main_tender_basic_info",
            query="招标工程地点和建设单位要求是什么？",
            filters={"document_id": MAIN_TENDER_DOC_ID, "source_type": "tender", "document_type": "tender"},
            route_type="tender_query",
            expect_policy_match=True,
        ),
        RerankSmokeCase(
            id="main_tender_schedule",
            query="总工期和关键节点有什么要求？",
            filters={"document_id": MAIN_TENDER_DOC_ID, "source_type": "tender", "document_type": "tender"},
            route_type="tender_query",
            expect_policy_match=True,
        ),
        RerankSmokeCase(
            id="qa_doc_temporary_work",
            query="答疑补遗中有哪些临时性紧急工作要求？",
            filters={"document_id": QA_DOC_ID, "source_type": "tender", "document_type": "tender"},
            route_type="tender_query",
            expect_policy_match=True,
        ),
        RerankSmokeCase(
            id="excel_pptx_structured_file",
            query="投标总价和付款比例，以及智慧建筑脑机系统页面讲了什么？",
            filters={"document_id": EXCEL_DOC_ID, "document_type": "xlsx"},
            allow_skipped=True,
        ),
        RerankSmokeCase(
            id="meeting_action_decision_risk",
            query="会议里有哪些行动项、决策和风险？",
            filters={"document_id": MEETING_DOC_ID, "source_type": "meeting", "document_type": "meeting"},
            allow_skipped=True,
        ),
    ]


def run_smoke(cases: list[RerankSmokeCase] | None = None) -> dict[str, Any]:
    cases = cases or builtin_cases()
    original = {
        "rerank_enabled": settings.rerank_enabled,
        "rerank_provider": settings.rerank_provider,
        "rerank_default_enablement_enabled": settings.rerank_default_enablement_enabled,
    }
    settings.rerank_enabled = True
    settings.rerank_provider = "aliyun"
    settings.rerank_default_enablement_enabled = True

    db = SessionLocal()
    try:
        db.execute(text("SELECT 1"))
        service = RetrievalService(db)
        results = [run_case(service, case) for case in cases]
    except Exception as exc:
        results = [RerankSmokeResult(id=case.id, passed=False, latency_ms=0.0, error=repr(exc)) for case in cases]
    finally:
        db.close()
        settings.rerank_enabled = original["rerank_enabled"]
        settings.rerank_provider = original["rerank_provider"]
        settings.rerank_default_enablement_enabled = original["rerank_default_enablement_enabled"]

    return summarize_results(results)


def run_case(service: RetrievalService, case: RerankSmokeCase) -> RerankSmokeResult:
    started = perf_counter()
    try:
        response = service.search(
            SearchRequest(
                query=case.query,
                route_type=case.route_type,
                retrieval_mode="hybrid",
                top_k=case.top_k,
                filters=RetrievalFilter(**case.filters),
            )
        )
        latency_ms = round((perf_counter() - started) * 1000, 3)
        return evaluate_rerank_response(case, response.trace or {}, response.results, latency_ms)
    except Exception as exc:  # pragma: no cover - live failure path.
        return RerankSmokeResult(id=case.id, passed=False, latency_ms=round((perf_counter() - started) * 1000, 3), error=repr(exc))


def evaluate_rerank_response(case: RerankSmokeCase, trace: dict[str, Any], results: list[Any], latency_ms: float) -> RerankSmokeResult:
    rerank = trace.get("rerank") if isinstance(trace.get("rerank"), dict) else {}
    policy = trace.get("rerank_policy") if isinstance(trace.get("rerank_policy"), dict) else {}
    status = trace.get("rerank_status") or rerank.get("status")
    policy_enabled = bool(policy.get("enabled"))
    fail_open = bool(rerank.get("fail_open"))
    error_type = rerank.get("error_type")
    output_count = int(rerank.get("output_count") or rerank.get("candidate_count_out") or 0)
    if status == "executed":
        passed = output_count > 0
    elif status == "failed_open":
        passed = fail_open and bool(rerank.get("reason") or error_type)
    elif status == "skipped":
        passed = case.allow_skipped and bool(rerank.get("reason_if_skipped") or policy.get("reason"))
    else:
        passed = False
    if case.expect_policy_match and status == "skipped":
        passed = False
    if case.expect_policy_match and not policy_enabled and status != "failed_open":
        passed = False

    return RerankSmokeResult(
        id=case.id,
        passed=passed,
        latency_ms=latency_ms,
        rerank_status=str(status or "unknown"),
        rerank_provider=rerank.get("provider"),
        rerank_model=rerank.get("model"),
        rerank_returned=output_count,
        rerank_latency_ms=float(rerank.get("elapsed_ms") or 0.0),
        fail_open=fail_open,
        fail_open_reason=rerank.get("reason") if fail_open else None,
        error_type=error_type,
        api_key_source=rerank.get("api_key_source"),
        policy_reason=policy.get("reason") or rerank.get("policy_reason"),
        policy_enabled=policy_enabled,
        matched_keywords=list(policy.get("matched_keywords") or []),
        candidate_count=int(policy.get("candidate_count") or rerank.get("input_count") or 0),
        result_document_ids=sorted({str(result.document_id) for result in results if getattr(result, "document_id", None)}),
    )


def summarize_results(results: list[RerankSmokeResult]) -> dict[str, Any]:
    executed = [result for result in results if result.rerank_status == "executed"]
    skipped = [result for result in results if result.rerank_status == "skipped"]
    failed_open = [result for result in results if result.rerank_status == "failed_open"]
    failed = [result for result in results if not result.passed]
    return {
        "total": len(results),
        "passed": len([result for result in results if result.passed]),
        "failed": len(failed),
        "executed": len(executed),
        "skipped": len(skipped),
        "failed_open": len(failed_open),
        "cases": [asdict(result) for result in results],
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run Phase 2.17 rerank smoke audit.")
    parser.add_argument("--json", action="store_true", help="Print JSON summary. Kept for explicit script usage.")
    parser.parse_args(argv)
    summary = run_smoke()
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0 if summary["failed"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
