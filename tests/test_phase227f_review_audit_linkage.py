import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.phase227f_review_audit_linkage import build_linkage_summary, main


def sample_manifest(**overrides):
    manifest = {
        "reports": [
            {
                "report_hash": "sha256:report-123",
                "report_type": "repair_plan",
                "path": "/Users/example/private/reports/repair.json",
            }
        ]
    }
    manifest.update(overrides)
    return manifest


def sample_review(**overrides):
    review = {
        "review_id": "review-123",
        "report_path": "/Users/example/private/reviews/review.json",
        "report_type": "repair_plan",
        "report_hash": "sha256:report-123",
        "reviewer": "reviewer-a",
        "reviewed_at": "2026-04-27T01:02:03+00:00",
        "status": "approved_for_manual_action",
        "notes": "sensitive review note",
        "item_decisions": [
            {
                "item_id": "item-1",
                "entity_id": "fact-secret",
                "decision": "approved_for_manual_action",
                "reason": "sensitive reason",
                "approved_action": "manual action",
            }
        ],
        "executable": False,
        "dry_run": True,
        "destructive_actions": [],
    }
    review.update(overrides)
    return review


def sample_audit(**overrides):
    audit = {
        "trace_id": "report_review:review-123",
        "action": "report.review.created",
        "resource_type": "report_review",
        "resource_id": "review-123",
        "request_json": {
            "source": "review_record",
            "report_hash": "sha256:report-123",
            "report_type": "repair_plan",
            "review_status": "approved_for_manual_action",
        },
        "result_json": {
            "summary": {
                "items_total": 1,
                "approved_count": 1,
                "rejected_count": 0,
                "deferred_count": 0,
                "needs_review_count": 0,
            },
            "executable": False,
            "approved_for_manual_action_is_execution": False,
            "sanitized": True,
        },
    }
    audit.update(overrides)
    return audit


def test_archive_review_audit_linkage_passes():
    summary = build_linkage_summary(
        archive_manifest=sample_manifest(),
        review_record=sample_review(),
        audit_event=sample_audit(),
    )

    assert summary["status"] == "pass"
    assert summary["archive_review"]["report_hash_matched"] is True
    assert summary["review_audit"]["review_id_matched"] is True
    assert summary["review_audit"]["trace_id_matched"] is True
    assert summary["end_to_end"]["linkage_complete"] is True
    assert summary["end_to_end"]["executable"] is False
    assert summary["end_to_end"]["repair_executed"] is False
    assert summary["destructive_actions"] == []


def test_archive_missing_warns_without_failure():
    summary = build_linkage_summary(
        archive_manifest=None,
        review_record=sample_review(),
        audit_event=sample_audit(),
    )

    assert summary["status"] == "warn"
    assert summary["archive_review"]["status"] == "warn"
    assert summary["failures"] == []
    assert summary["warnings"][0]["code"] == "archive_manifest_missing"


def test_audit_event_missing_warns_without_failure():
    summary = build_linkage_summary(
        archive_manifest=sample_manifest(),
        review_record=sample_review(),
        audit_event=None,
    )

    assert summary["status"] == "warn"
    assert summary["review_audit"]["status"] == "warn"
    assert summary["failures"] == []
    assert summary["warnings"][0]["code"] == "audit_event_missing"


def test_invalid_audit_event_type_fails():
    summary = build_linkage_summary(
        archive_manifest=sample_manifest(),
        review_record=sample_review(),
        audit_event=sample_audit(action="report.review.executed"),
    )

    assert summary["status"] == "fail"
    assert any(item["code"] == "invalid_audit_event_type" for item in summary["failures"])


def test_unsafe_audit_fields_fail():
    audit = sample_audit()
    audit["result_json"]["notes"] = "private"
    audit["result_json"]["approved_action"] = "repair"

    summary = build_linkage_summary(
        archive_manifest=sample_manifest(),
        review_record=sample_review(),
        audit_event=audit,
    )

    assert summary["status"] == "fail"
    assert any(item["code"] == "unsafe_audit_fields" for item in summary["failures"])


def test_item_level_entity_details_fail():
    audit = sample_audit()
    audit["request_json"]["document_id"] = "doc-secret"
    audit["result_json"]["fact_id"] = "fact-secret"

    summary = build_linkage_summary(
        archive_manifest=sample_manifest(),
        review_record=sample_review(),
        audit_event=audit,
    )

    assert summary["status"] == "fail"
    unsafe = next(item for item in summary["failures"] if item["code"] == "unsafe_audit_fields")
    assert any("document_id" in path or "fact_id" in path for path in unsafe["paths"])


def test_top_level_document_id_fails_without_leaking_value():
    summary = build_linkage_summary(
        archive_manifest=sample_manifest(),
        review_record=sample_review(),
        audit_event=sample_audit(document_id="doc-secret"),
    )
    encoded = json.dumps(summary, ensure_ascii=False)

    assert summary["status"] == "fail"
    unsafe = next(item for item in summary["failures"] if item["code"] == "unsafe_audit_top_level_fields")
    assert "$.document_id" in unsafe["paths"]
    assert "doc-secret" not in encoded


def test_top_level_fact_id_fails_without_leaking_value():
    summary = build_linkage_summary(
        archive_manifest=sample_manifest(),
        review_record=sample_review(),
        audit_event=sample_audit(fact_id="fact-secret"),
    )
    encoded = json.dumps(summary, ensure_ascii=False)

    assert summary["status"] == "fail"
    unsafe = next(item for item in summary["failures"] if item["code"] == "unsafe_audit_top_level_fields")
    assert "$.fact_id" in unsafe["paths"]
    assert "fact-secret" not in encoded


def test_top_level_absolute_path_fails_without_leaking_path():
    summary = build_linkage_summary(
        archive_manifest=sample_manifest(),
        review_record=sample_review(),
        audit_event=sample_audit(report_path="/Users/example/private/audit.json"),
    )
    encoded = json.dumps(summary, ensure_ascii=False)

    assert summary["status"] == "fail"
    unsafe = next(item for item in summary["failures"] if item["code"] == "unsafe_audit_top_level_fields")
    assert "$.report_path" in unsafe["paths"]
    assert "/Users/example/private" not in encoded


def test_sensitive_review_fields_and_absolute_paths_do_not_enter_output():
    summary = build_linkage_summary(
        archive_manifest=sample_manifest(),
        review_record=sample_review(),
        audit_event=sample_audit(),
    )
    encoded = json.dumps(summary, ensure_ascii=False)

    assert "sensitive review note" not in encoded
    assert "sensitive reason" not in encoded
    assert "manual action" not in encoded
    assert "item_decisions" not in encoded
    assert "report_path" not in encoded
    assert "/Users/example/private" not in encoded
    assert "fact-secret" not in encoded


def test_unsafe_review_record_is_rejected():
    summary = build_linkage_summary(
        archive_manifest=sample_manifest(),
        review_record=sample_review(executable=True, dry_run=False, destructive_actions=["repair"]),
        audit_event=sample_audit(),
    )

    assert summary["status"] == "fail"
    codes = {item["code"] for item in summary["failures"]}
    assert "review_executable_not_false" in codes
    assert "review_dry_run_not_true" in codes
    assert "review_destructive_actions_not_empty" in codes


def test_cli_outputs_json_summary(tmp_path, capsys):
    manifest_path = tmp_path / "manifest.json"
    review_path = tmp_path / "review.json"
    audit_path = tmp_path / "audit.json"
    manifest_path.write_text(json.dumps(sample_manifest()), encoding="utf-8")
    review_path.write_text(json.dumps(sample_review()), encoding="utf-8")
    audit_path.write_text(json.dumps(sample_audit()), encoding="utf-8")

    assert main(
        [
            "--archive-manifest",
            str(manifest_path),
            "--review-record",
            str(review_path),
            "--audit-event-file",
            str(audit_path),
            "--json",
        ]
    ) == 0
    output = json.loads(capsys.readouterr().out)

    assert output["status"] == "pass"
    assert output["dry_run"] is True
    assert output["destructive_actions"] == []
