#!/usr/bin/env python3
"""Offline scorer for reviewed Phase 2 evaluation inventory results.

This script is intentionally pure stdlib and offline. It never imports Hermes
runtime modules and never connects to DB, NAS, Gateway, OpenSearch, Qdrant, or
MinIO.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


MANIFEST_SCHEMA_VERSION = "phase2_eval_inventory_manifest.v1"
RESULTS_SCHEMA_VERSION = "phase2_eval_results.v1"
OUTPUT_SCHEMA_VERSION = "phase2_metric_scoring_pack.v1"

DEFAULT_MANIFEST_PATH = Path("eval/phase2_inventory/phase2_eval_inventory_manifest.json")

REQUIRED_CASE_FIELDS = {
    "case_id",
    "group",
    "question",
    "expected_evidence_mode",
    "expected_document_refs",
    "expected_citation_fields",
    "forbidden_behaviors",
    "metric_eligible",
}

ALLOWED_RESULT_FIELDS = {
    "case_id",
    "top5_hit",
    "citation_ok",
    "forbidden_behaviors_observed",
    "notes",
}

UNSAFE_RESULT_FIELDS = {
    "raw_text",
    "raw_answer",
    "raw_answer_text",
    "raw_rows",
    "nas_path",
    "storage_path",
    "local_path",
    "secret",
    "token",
    "api_key",
}


class MetricScoringError(ValueError):
    """Raised when an offline scoring input is invalid or unsafe."""


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise MetricScoringError(message)


def load_json(path: Path) -> dict[str, Any]:
    try:
        with path.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
    except json.JSONDecodeError as exc:
        raise MetricScoringError(f"invalid JSON in {path}: {exc}") from exc
    except OSError as exc:
        raise MetricScoringError(f"cannot read {path}: {exc}") from exc

    _require(isinstance(data, dict), f"{path} must contain a JSON object")
    return data


def _validate_case(case: Any, index: int) -> dict[str, Any]:
    _require(isinstance(case, dict), f"manifest case at index {index} must be an object")
    missing_fields = sorted(REQUIRED_CASE_FIELDS - set(case))
    _require(not missing_fields, f"manifest case at index {index} missing fields: {missing_fields}")
    _require(isinstance(case["case_id"], str) and case["case_id"], "case_id must be a string")
    _require(isinstance(case["metric_eligible"], bool), "metric_eligible must be a boolean")
    _require(
        isinstance(case["expected_document_refs"], list),
        f"{case['case_id']} expected_document_refs must be a list",
    )
    _require(
        isinstance(case["expected_citation_fields"], list),
        f"{case['case_id']} expected_citation_fields must be a list",
    )
    _require(
        isinstance(case["forbidden_behaviors"], list),
        f"{case['case_id']} forbidden_behaviors must be a list",
    )
    return case


def validate_manifest(manifest: dict[str, Any]) -> list[dict[str, Any]]:
    _require(
        manifest.get("schema_version") == MANIFEST_SCHEMA_VERSION,
        f"manifest schema_version must be {MANIFEST_SCHEMA_VERSION}",
    )
    cases = manifest.get("cases")
    _require(isinstance(cases, list) and cases, "manifest cases must be a non-empty list")

    validated_cases = [_validate_case(case, index) for index, case in enumerate(cases)]
    case_ids = [case["case_id"] for case in validated_cases]
    _require(len(set(case_ids)) == len(case_ids), "manifest case_id values must be unique")
    return validated_cases


def _validate_result(result: Any, index: int) -> dict[str, Any]:
    _require(isinstance(result, dict), f"result at index {index} must be an object")
    unknown_fields = sorted(set(result) - ALLOWED_RESULT_FIELDS)
    unsafe_fields = sorted((set(result) & UNSAFE_RESULT_FIELDS) | set(unknown_fields))
    _require(not unsafe_fields, f"unsafe result field(s) at index {index}: {unsafe_fields}")

    _require(isinstance(result.get("case_id"), str) and result["case_id"], "result case_id must be a string")
    _require(
        isinstance(result.get("forbidden_behaviors_observed"), list),
        f"{result['case_id']} forbidden_behaviors_observed must be a list",
    )
    for behavior in result["forbidden_behaviors_observed"]:
        _require(
            isinstance(behavior, str),
            f"{result['case_id']} forbidden_behaviors_observed entries must be strings",
        )
    if "notes" in result:
        _require(isinstance(result["notes"], str), f"{result['case_id']} notes must be a string")
    return result


def validate_results(results: dict[str, Any]) -> list[dict[str, Any]]:
    _require(
        results.get("schema_version") == RESULTS_SCHEMA_VERSION,
        f"results schema_version must be {RESULTS_SCHEMA_VERSION}",
    )
    rows = results.get("results")
    _require(isinstance(rows, list), "results must be a list")

    validated_results = [_validate_result(result, index) for index, result in enumerate(rows)]
    case_ids = [result["case_id"] for result in validated_results]
    _require(len(set(case_ids)) == len(case_ids), "result case_id values must be unique")
    return validated_results


def _validate_eligible_result(result: dict[str, Any]) -> None:
    case_id = result["case_id"]
    _require(isinstance(result.get("top5_hit"), bool), f"{case_id} top5_hit must be a boolean")
    _require(isinstance(result.get("citation_ok"), bool), f"{case_id} citation_ok must be a boolean")


def _rate(count: int, denominator: int) -> float:
    if denominator == 0:
        return 0.0
    return round(count / denominator, 4)


def score_metric_pack(manifest: dict[str, Any], results: dict[str, Any]) -> dict[str, Any]:
    cases = validate_manifest(manifest)
    result_rows = validate_results(results)

    case_by_id = {case["case_id"]: case for case in cases}
    result_by_id = {result["case_id"]: result for result in result_rows}
    unknown_result_case_ids = sorted(set(result_by_id) - set(case_by_id))
    _require(not unknown_result_case_ids, f"unknown result case_id values: {unknown_result_case_ids}")

    eligible_case_ids = [case["case_id"] for case in cases if case["metric_eligible"]]
    ineligible_case_ids = [case["case_id"] for case in cases if not case["metric_eligible"]]
    missing_result_case_ids = [case_id for case_id in eligible_case_ids if case_id not in result_by_id]
    scored_case_ids = [case_id for case_id in eligible_case_ids if case_id in result_by_id]

    top5_hit_count = 0
    citation_ok_count = 0
    forbidden_violation_case_ids = [
        case["case_id"]
        for case in cases
        if case["case_id"] in result_by_id
        and result_by_id[case["case_id"]]["forbidden_behaviors_observed"]
    ]

    for case_id in scored_case_ids:
        result = result_by_id[case_id]
        _validate_eligible_result(result)
        if result["top5_hit"]:
            top5_hit_count += 1
        if result["citation_ok"]:
            citation_ok_count += 1

    if forbidden_violation_case_ids:
        status = "blocked_for_review"
    elif missing_result_case_ids:
        status = "incomplete"
    else:
        status = "scored"

    eligible_count = len(eligible_case_ids)
    manifest_summary = manifest.get("summary") if isinstance(manifest.get("summary"), dict) else {}

    return {
        "schema_version": OUTPUT_SCHEMA_VERSION,
        "manifest_case_count": len(cases),
        "metric_eligible_case_count": eligible_count,
        "metric_ineligible_case_count": len(ineligible_case_ids),
        "results_case_count": len(result_rows),
        "scored_case_count": len(scored_case_ids),
        "missing_result_case_ids": missing_result_case_ids,
        "excluded_case_ids": ineligible_case_ids,
        "top5_hit_count": top5_hit_count,
        "top5_hit_rate": _rate(top5_hit_count, eligible_count),
        "citation_ok_count": citation_ok_count,
        "citation_ok_rate": _rate(citation_ok_count, eligible_count),
        "forbidden_violation_count": len(forbidden_violation_case_ids),
        "forbidden_violation_case_ids": forbidden_violation_case_ids,
        "status": status,
        "phase2_closeout_readiness": False,
        "prd_100_target_status": manifest_summary.get("prd_100_target_status", "not_satisfied"),
        "roadmap_300_target_status": manifest_summary.get("roadmap_300_target_status", "not_satisfied"),
    }


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    except OSError as exc:
        raise MetricScoringError(f"cannot write {path}: {exc}") from exc


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Score reviewed Phase 2 eval inventory results.")
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST_PATH)
    parser.add_argument("--results", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        summary = score_metric_pack(load_json(args.manifest), load_json(args.results))
        if args.output:
            _write_json(args.output, summary)
        else:
            print(json.dumps(summary, ensure_ascii=False, indent=2))
    except MetricScoringError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
