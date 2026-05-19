import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.phase2102b_metric_scoring_pack import (
    MetricScoringError,
    score_metric_pack,
)


def _case(case_id: str, *, eligible: bool = True) -> dict:
    return {
        "case_id": case_id,
        "group": "core",
        "question": f"Question for {case_id}",
        "expected_evidence_mode": "document",
        "expected_document_refs": ["doc-a"],
        "expected_citation_fields": ["document_id"],
        "forbidden_behaviors": ["wrong_document"],
        "metric_eligible": eligible,
    }


def _manifest() -> dict:
    return {
        "schema_version": "phase2_eval_inventory_manifest.v1",
        "cases": [
            _case("eligible-1"),
            _case("eligible-2"),
            _case("eligible-3"),
            _case("excluded-1", eligible=False),
        ],
    }


def _result(case_id: str, *, top5: bool = True, citation: bool = True, forbidden=None) -> dict:
    return {
        "case_id": case_id,
        "top5_hit": top5,
        "citation_ok": citation,
        "forbidden_behaviors_observed": list(forbidden or []),
        "notes": "sanitized optional note",
    }


def test_full_eligible_fixture_computes_rates() -> None:
    results = {
        "schema_version": "phase2_eval_results.v1",
        "results": [
            _result("eligible-1", top5=True, citation=True),
            _result("eligible-2", top5=True, citation=False),
            _result("eligible-3", top5=False, citation=True),
        ],
    }

    summary = score_metric_pack(_manifest(), results)

    assert summary["schema_version"] == "phase2_metric_scoring_pack.v1"
    assert summary["manifest_case_count"] == 4
    assert summary["metric_eligible_case_count"] == 3
    assert summary["metric_ineligible_case_count"] == 1
    assert summary["scored_case_count"] == 3
    assert summary["top5_hit_count"] == 2
    assert summary["top5_hit_rate"] == 0.6667
    assert summary["citation_ok_count"] == 2
    assert summary["citation_ok_rate"] == 0.6667
    assert summary["status"] == "scored"
    assert summary["phase2_closeout_readiness"] is False
    assert summary["prd_100_target_status"] == "not_satisfied"
    assert summary["roadmap_300_target_status"] == "not_satisfied"


def test_clean_ineligible_cases_are_excluded_from_denominator() -> None:
    results = {
        "schema_version": "phase2_eval_results.v1",
        "results": [
            _result("eligible-1", top5=True, citation=True),
            _result("eligible-2", top5=True, citation=True),
            _result("eligible-3", top5=True, citation=True),
            _result("excluded-1", top5=False, citation=False),
        ],
    }

    summary = score_metric_pack(_manifest(), results)

    assert summary["results_case_count"] == 4
    assert summary["scored_case_count"] == 3
    assert summary["excluded_case_ids"] == ["excluded-1"]
    assert summary["top5_hit_rate"] == 1.0
    assert summary["citation_ok_rate"] == 1.0
    assert summary["forbidden_violation_count"] == 0


def test_ineligible_forbidden_behavior_blocks_review_without_changing_denominator() -> None:
    results = {
        "schema_version": "phase2_eval_results.v1",
        "results": [
            _result("eligible-1", top5=True, citation=True),
            _result("eligible-2", top5=True, citation=True),
            _result("eligible-3", top5=True, citation=True),
            _result("excluded-1", top5=False, citation=False, forbidden=["wrong_document"]),
        ],
    }

    summary = score_metric_pack(_manifest(), results)

    assert summary["status"] == "blocked_for_review"
    assert summary["metric_eligible_case_count"] == 3
    assert summary["scored_case_count"] == 3
    assert summary["top5_hit_rate"] == 1.0
    assert summary["citation_ok_rate"] == 1.0
    assert summary["forbidden_violation_count"] == 1
    assert summary["forbidden_violation_case_ids"] == ["excluded-1"]


def test_missing_eligible_result_marks_incomplete() -> None:
    results = {
        "schema_version": "phase2_eval_results.v1",
        "results": [
            _result("eligible-1", top5=True, citation=True),
            _result("eligible-3", top5=True, citation=True),
        ],
    }

    summary = score_metric_pack(_manifest(), results)

    assert summary["status"] == "incomplete"
    assert summary["missing_result_case_ids"] == ["eligible-2"]
    assert summary["scored_case_count"] == 2


def test_forbidden_behavior_takes_precedence_over_missing_results() -> None:
    results = {
        "schema_version": "phase2_eval_results.v1",
        "results": [
            _result("eligible-1", top5=True, citation=True),
            _result("eligible-3", top5=True, citation=True),
            _result("excluded-1", top5=False, citation=False, forbidden=["wrong_document"]),
        ],
    }

    summary = score_metric_pack(_manifest(), results)

    assert summary["status"] == "blocked_for_review"
    assert summary["missing_result_case_ids"] == ["eligible-2"]
    assert summary["forbidden_violation_case_ids"] == ["excluded-1"]


def test_forbidden_behavior_blocks_for_review() -> None:
    results = {
        "schema_version": "phase2_eval_results.v1",
        "results": [
            _result("eligible-1", top5=True, citation=True),
            _result("eligible-2", top5=True, citation=True, forbidden=["wrong_document"]),
            _result("eligible-3", top5=True, citation=True),
        ],
    }

    summary = score_metric_pack(_manifest(), results)

    assert summary["status"] == "blocked_for_review"
    assert summary["forbidden_violation_count"] == 1
    assert summary["forbidden_violation_case_ids"] == ["eligible-2"]


def test_invalid_manifest_schema_raises_clear_error() -> None:
    manifest = {"schema_version": "wrong", "cases": [_case("eligible-1")]}
    results = {"schema_version": "phase2_eval_results.v1", "results": []}

    with pytest.raises(MetricScoringError, match="manifest schema_version"):
        score_metric_pack(manifest, results)


def test_output_rejects_raw_text_storage_paths_and_secrets() -> None:
    results = {
        "schema_version": "phase2_eval_results.v1",
        "results": [
            {
                **_result("eligible-1", top5=True, citation=True),
                "raw_answer_text": "do not keep raw answer text",
            },
            _result("eligible-2", top5=True, citation=True),
            _result("eligible-3", top5=True, citation=True),
        ],
    }

    with pytest.raises(MetricScoringError, match="unsafe result field"):
        score_metric_pack(_manifest(), results)
