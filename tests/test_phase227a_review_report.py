import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.phase227a_review_report import (
    build_review_record,
    decision_summary,
    file_sha256,
    normalize_item_decision,
    review_filename,
    skeleton_decisions_from_report,
    validate_status,
    write_review_record,
)


def write_report(tmp_path: Path, data: dict) -> Path:
    path = tmp_path / "repair_report.json"
    path.write_text(json.dumps(data), encoding="utf-8")
    return path


def sample_report():
    return {
        "status": "warn",
        "items": [
            {
                "item_id": "item-1",
                "entity_id": "fact-1",
                "item_type": "stale_fact",
                "recommended_action": "revalidate_against_latest",
            }
        ],
    }


def test_review_record_schema_and_invariants(tmp_path):
    report = sample_report()
    report_path = write_report(tmp_path, report)
    decisions = skeleton_decisions_from_report(report)

    record = build_review_record(
        report_path=report_path,
        report=report,
        reviewer="reviewer-a",
        status="pending_review",
        notes="needs human review",
        item_decisions=decisions,
        reviewed_at="2026-04-27T01:02:03+00:00",
    )

    assert record["review_id"].startswith("review-")
    assert record["report_type"] == "repair_plan"
    assert record["report_hash"].startswith("sha256:")
    assert record["reviewer"] == "reviewer-a"
    assert record["status"] == "pending_review"
    assert record["executable"] is False
    assert record["dry_run"] is True
    assert record["destructive_actions"] == []
    assert record["item_decisions"][0]["executable"] is False


def test_report_hash_is_stable(tmp_path):
    report_path = write_report(tmp_path, {"status": "pass"})

    first = file_sha256(report_path)
    second = file_sha256(report_path)

    assert first == second
    assert first.startswith("sha256:")


def test_status_validation_rejects_unknown_value():
    with pytest.raises(ValueError):
        validate_status("executed")


def test_item_decision_summary_counts_decisions():
    decisions = [
        normalize_item_decision({"decision": "approved_for_manual_action", "entity_id": "a"}),
        normalize_item_decision({"decision": "rejected", "entity_id": "b"}),
        normalize_item_decision({"decision": "deferred", "entity_id": "c"}),
        normalize_item_decision({"decision": "needs_review", "entity_id": "d"}),
    ]

    summary = decision_summary(decisions)

    assert summary["decisions_total"] == 4
    assert summary["approved_count"] == 1
    assert summary["rejected_count"] == 1
    assert summary["deferred_count"] == 1
    assert summary["needs_review_count"] == 1
    assert summary["executable"] is False


def test_skeleton_decisions_are_needs_review_not_approved():
    decisions = skeleton_decisions_from_report(sample_report())

    assert decisions[0]["decision"] == "needs_review"
    assert decisions[0]["approved_action"] is None
    assert decisions[0]["executable"] is False


def test_dry_run_preview_equivalent_does_not_write_file(tmp_path):
    report = sample_report()
    report_path = write_report(tmp_path, report)
    record = build_review_record(
        report_path=report_path,
        report=report,
        reviewer="reviewer-a",
        status="acknowledged",
        notes="preview only",
        item_decisions=[],
        reviewed_at="2026-04-27T01:02:03+00:00",
    )
    output_path = tmp_path / "reviews" / review_filename(record)

    assert not output_path.exists()


def test_write_review_record_writes_only_local_json(tmp_path):
    report = sample_report()
    report_path = write_report(tmp_path, report)
    record = build_review_record(
        report_path=report_path,
        report=report,
        reviewer="reviewer-a",
        status="acknowledged",
        notes="write local record",
        item_decisions=[],
        reviewed_at="2026-04-27T01:02:03+00:00",
    )

    path = write_review_record(record, tmp_path / "reviews")

    assert path.name == "20260427_010203_repair_plan_acknowledged.json"
    assert json.loads(path.read_text())["executable"] is False
