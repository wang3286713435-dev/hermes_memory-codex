from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from statistics import mean, median

import httpx
import yaml

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.core.config import settings
from app.schemas.retrieval import RetrievalFilter, SearchRequest
from app.services.evaluation import RetrievalEvalCase
from app.services.retrieval.service import RetrievalService


def _load_cases(path: Path) -> list[RetrievalEvalCase]:
    payload = yaml.safe_load(path.read_text()) or []
    return [
        RetrievalEvalCase(
            case_id=item.get("id"),
            query=item["query"],
            expected_chunk_ids={item["expected_chunk_id"]} if item.get("expected_chunk_id") else set(),
            expected_document_ids={item["expected_document_id"]} if item.get("expected_document_id") else set(),
            notes=item.get("notes"),
        )
        for item in payload
    ]


def _percentile(values: list[float], percentile: int) -> float:
    if not values:
        return 0.0
    if len(values) == 1:
        return values[0]
    index = min(len(values) - 1, round((percentile / 100) * (len(values) - 1)))
    return values[index]


def _summarize(records: list[dict]) -> dict:
    total = len(records)
    executed = [record for record in records if record["rerank_status"] == "executed"]
    failed_open = [record for record in records if record["rerank_status"] == "failed_open"]
    skipped = [record for record in records if record["rerank_status"] == "skipped"]
    policy_hits = [record for record in records if record["policy_enabled"]]
    timeout_records = [record for record in records if record.get("error_type") == "timeout"]
    dense_failed = [record for record in records if record.get("dense_status") == "failed"]
    sparse_failed = [record for record in records if record.get("sparse_status") == "failed"]
    exec_latencies = sorted(float(record["elapsed_ms"]) for record in executed)

    return {
        "total_queries": total,
        "rerank_hit_count": len(executed),
        "rerank_hit_rate": round(len(executed) / total, 4) if total else 0.0,
        "rerank_policy_hit_count": len(policy_hits),
        "rerank_policy_hit_rate": round(len(policy_hits) / total, 4) if total else 0.0,
        "rerank_skip_count": len(skipped),
        "rerank_skip_rate": round(len(skipped) / total, 4) if total else 0.0,
        "fail_open_count": len(failed_open),
        "fail_open_rate": round(len(failed_open) / total, 4) if total else 0.0,
        "timeout_count": len(timeout_records),
        "dense_failed_count": len(dense_failed),
        "sparse_failed_count": len(sparse_failed),
        "latency_avg_ms": round(mean(exec_latencies), 3) if exec_latencies else 0.0,
        "latency_p50_ms": round(median(exec_latencies), 3) if exec_latencies else 0.0,
        "latency_p95_ms": round(_percentile(exec_latencies, 95), 3) if exec_latencies else 0.0,
        "latency_p99_ms": round(_percentile(exec_latencies, 99), 3) if exec_latencies else 0.0,
        "policy_reasons": _count_field(records, "policy_reason"),
        "error_types": _count_field(records, "error_type"),
    }


def _count_field(records: list[dict], field: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    for record in records:
        value = record.get(field)
        if not value:
            continue
        counts[str(value)] = counts.get(str(value), 0) + 1
    return counts


def _run_scenario(
    *,
    name: str,
    cases: list[RetrievalEvalCase],
    rerank_enabled: bool,
    local_enablement_enabled: bool,
    timeout_ms: int,
) -> dict:
    settings.rerank_enabled = rerank_enabled
    settings.rerank_provider = "aliyun"
    settings.rerank_default_enablement_enabled = local_enablement_enabled
    settings.aliyun_rerank_timeout_ms = timeout_ms

    service = RetrievalService(db=None)  # type: ignore[arg-type]
    service._write_log = lambda *a, **k: None  # type: ignore[method-assign]
    service._database_fallback_search = lambda *a, **k: []  # type: ignore[method-assign]
    sparse_backend_available = _check_opensearch()
    dense_backend_available = _check_qdrant()
    if not sparse_backend_available:
        service._sparse_search = lambda *a, **k: []  # type: ignore[method-assign]

    records = []
    for case in cases:
        request = _build_request(case)
        response = service.search(request)
        rerank = response.trace.get("rerank", {})
        policy = response.trace.get("rerank_policy", {})
        records.append(
            {
                "case_id": case.case_id,
                "query": case.query,
                "notes": case.notes,
                "request_route_type": request.route_type,
                "request_source_type": request.filters.source_type,
                "backend": response.backend,
                "dense_status": response.dense_status,
                "sparse_status": response.sparse_status,
                "rerank_status": response.trace.get("rerank_status"),
                "policy_enabled": bool(policy.get("enabled")),
                "policy_reason": policy.get("reason"),
                "provider": rerank.get("provider"),
                "model": rerank.get("model"),
                "elapsed_ms": float(rerank.get("elapsed_ms") or 0.0),
                "fail_open": bool(rerank.get("fail_open")),
                "error_type": rerank.get("error_type"),
                "matched_keywords": policy.get("matched_keywords") or [],
                "route_type": policy.get("route_type"),
                "candidate_source_types": policy.get("candidate_source_types") or [],
            }
        )
    return {
        "scenario": name,
        "environment": {
            "qdrant_available": dense_backend_available,
            "opensearch_available": sparse_backend_available,
        },
        "summary": _summarize(records),
        "records": records,
    }


def _check_opensearch() -> bool:
    try:
        response = httpx.get(settings.opensearch_url, timeout=1.5)
        return response.status_code < 500
    except Exception:
        return False


def _check_qdrant() -> bool:
    try:
        response = httpx.get(settings.qdrant_url, timeout=1.5)
        return response.status_code < 500
    except Exception:
        return False


def _build_request(case: RetrievalEvalCase) -> SearchRequest:
    notes = case.notes or ""
    is_tender = notes.startswith("招标资料")
    route_type = "tender_query" if is_tender else None
    source_type = "tender" if is_tender else None
    return SearchRequest(
        query=case.query,
        route_type=route_type,
        retrieval_mode="hybrid",
        top_k=5,
        filters=RetrievalFilter(source_type=source_type),
    )


def main() -> None:
    golden_path = Path("eval/golden_queries/rerank_phase23.yaml")
    cases = _load_cases(golden_path)
    original = {
        "rerank_enabled": settings.rerank_enabled,
        "rerank_provider": settings.rerank_provider,
        "rerank_default_enablement_enabled": settings.rerank_default_enablement_enabled,
        "aliyun_rerank_timeout_ms": settings.aliyun_rerank_timeout_ms,
    }
    try:
        result = {
            "query_count": len(cases),
            "gray_enabled": _run_scenario(
                name="gray_enabled",
                cases=cases,
                rerank_enabled=True,
                local_enablement_enabled=True,
                timeout_ms=600,
            ),
            "global_disabled": _run_scenario(
                name="global_disabled",
                cases=cases,
                rerank_enabled=False,
                local_enablement_enabled=True,
                timeout_ms=600,
            ),
            "local_disabled": _run_scenario(
                name="local_disabled",
                cases=cases,
                rerank_enabled=True,
                local_enablement_enabled=False,
                timeout_ms=600,
            ),
            "timeout_drill": _run_scenario(
                name="timeout_drill",
                cases=cases,
                rerank_enabled=True,
                local_enablement_enabled=True,
                timeout_ms=1,
            ),
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))
    finally:
        settings.rerank_enabled = original["rerank_enabled"]
        settings.rerank_provider = original["rerank_provider"]
        settings.rerank_default_enablement_enabled = original["rerank_default_enablement_enabled"]
        settings.aliyun_rerank_timeout_ms = original["aliyun_rerank_timeout_ms"]


if __name__ == "__main__":
    main()
