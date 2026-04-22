from __future__ import annotations

import json
import os
import sys
from pathlib import Path

import yaml

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.core.config import settings
from app.schemas.retrieval import SearchRequest
from app.services.evaluation import RetrievalEvalCase, evaluate_retrieval_response, summarize_retrieval_spike
from app.services.retrieval.service import RetrievalService


def _load_cases(path: Path) -> list[RetrievalEvalCase]:
    payload = yaml.safe_load(path.read_text()) or []
    cases: list[RetrievalEvalCase] = []
    for item in payload:
        cases.append(
            RetrievalEvalCase(
                case_id=item.get("id"),
                query=item["query"],
                expected_chunk_ids={item["expected_chunk_id"]} if item.get("expected_chunk_id") else set(),
                expected_document_ids={item["expected_document_id"]} if item.get("expected_document_id") else set(),
                notes=item.get("notes"),
            )
        )
    return cases


def _run_variant(*, rerank_enabled: bool, rerank_provider: str, cases: list[RetrievalEvalCase]) -> dict:
    settings.rerank_enabled = rerank_enabled
    settings.rerank_provider = rerank_provider

    service = RetrievalService(db=None)  # type: ignore[arg-type]
    service._write_log = lambda *a, **k: None  # type: ignore[method-assign]

    reports = []
    for case in cases:
        response = service.search(SearchRequest(query=case.query, retrieval_mode="hybrid", top_k=5))
        report = evaluate_retrieval_response(case, response)
        report["result_chunk_ids"] = [item.chunk_id for item in response.results]
        report["result_texts"] = [item.text for item in response.results]
        report["trace"] = {
            "rerank_status": response.trace.get("rerank_status"),
            "provider": response.trace.get("rerank", {}).get("provider"),
            "fail_open": response.trace.get("rerank", {}).get("fail_open"),
            "elapsed_ms": response.trace.get("rerank", {}).get("elapsed_ms"),
            "api_key_source": response.trace.get("rerank", {}).get("api_key_source"),
        }
        reports.append(report)
    return {"summary": summarize_retrieval_spike(reports), "reports": reports}


def main() -> None:
    golden_path = Path("eval/golden_queries/rerank_phase23.yaml")
    cases = _load_cases(golden_path)
    baseline = _run_variant(rerank_enabled=False, rerank_provider="noop", cases=cases)
    experiment = _run_variant(rerank_enabled=True, rerank_provider="aliyun", cases=cases)
    print(
        json.dumps(
            {
                "golden_query_count": len(cases),
                "baseline": baseline,
                "experiment": experiment,
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
