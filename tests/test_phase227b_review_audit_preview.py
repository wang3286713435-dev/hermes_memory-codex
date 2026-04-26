import json
import sys
from pathlib import Path

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import scripts.phase227b_review_audit_preview as preview_module
from app.db.base import Base
from app.models.audit import AuditLog
from scripts.phase227b_review_audit_preview import (
    audit_log_payload,
    build_audit_preview,
    main,
    unsafe_payload_keys,
)


def sample_review_record(**overrides):
    record = {
        "review_id": "review-123",
        "report_path": "/Users/example/private/reports/repair.json",
        "report_type": "repair_plan",
        "report_hash": "sha256:abc123",
        "reviewer": "reviewer-a",
        "reviewed_at": "2026-04-27T01:02:03+00:00",
        "status": "approved_for_manual_action",
        "notes": "sensitive review note",
        "item_decisions": [
            {
                "item_id": "item-1",
                "entity_id": "fact-secret",
                "item_type": "stale_fact",
                "decision": "approved_for_manual_action",
                "reason": "sensitive reason",
                "approved_action": "manual revalidation",
                "executable": False,
            }
        ],
        "summary": {
            "items_total": 1,
            "decisions_total": 1,
            "approved_count": 1,
            "rejected_count": 0,
            "deferred_count": 0,
            "needs_review_count": 0,
            "executable": False,
        },
        "executable": False,
        "dry_run": True,
        "destructive_actions": [],
    }
    record.update(overrides)
    return record


def test_sanitized_payload_shape():
    payload = build_audit_preview(sample_review_record())

    assert payload == {
        "dry_run": True,
        "event_type": "report.review.created",
        "review_id": "review-123",
        "report_hash": "sha256:abc123",
        "report_type": "repair_plan",
        "review_status": "approved_for_manual_action",
        "reviewer": "reviewer-a",
        "reviewed_at": "2026-04-27T01:02:03+00:00",
        "summary": {
            "items_total": 1,
            "approved_count": 1,
            "rejected_count": 0,
            "deferred_count": 0,
            "needs_review_count": 0,
        },
        "executable": False,
        "would_write_audit_logs": False,
    }


def test_sensitive_review_fields_do_not_enter_payload():
    payload = build_audit_preview(sample_review_record())
    encoded = json.dumps(payload, ensure_ascii=False)

    assert "sensitive review note" not in encoded
    assert "sensitive reason" not in encoded
    assert "manual revalidation" not in encoded
    assert "item_decisions" not in encoded
    assert "report_path" not in encoded
    assert "/Users/example/private" not in encoded
    assert "fact-secret" not in encoded
    assert unsafe_payload_keys(payload) == set()


def test_invariant_fields_are_stable():
    payload = build_audit_preview(sample_review_record())

    assert payload["dry_run"] is True
    assert payload["executable"] is False
    assert payload["would_write_audit_logs"] is False


@pytest.mark.parametrize(
    ("override", "error"),
    [
        ({"executable": True}, "executable must be false"),
        ({"dry_run": False}, "dry_run must be true"),
        ({"destructive_actions": ["repair"]}, "destructive_actions must be empty"),
    ],
)
def test_unsafe_review_record_is_rejected(override, error):
    with pytest.raises(ValueError, match=error):
        build_audit_preview(sample_review_record(**override))


def test_summary_can_be_derived_without_summary_block():
    record = sample_review_record()
    record.pop("summary")
    record["item_decisions"].extend(
        [
            {"decision": "rejected"},
            {"decision": "deferred"},
            {"decision": "needs_review"},
        ]
    )

    payload = build_audit_preview(record)

    assert payload["summary"]["items_total"] == 4
    assert payload["summary"]["approved_count"] == 1
    assert payload["summary"]["rejected_count"] == 1
    assert payload["summary"]["deferred_count"] == 1
    assert payload["summary"]["needs_review_count"] == 1


def test_approved_for_manual_action_is_not_described_as_executed():
    payload = build_audit_preview(sample_review_record(status="approved_for_manual_action"))
    encoded = json.dumps(payload).lower()

    assert payload["review_status"] == "approved_for_manual_action"
    assert "executed" not in encoded
    assert payload["executable"] is False


def test_cli_preview_outputs_sanitized_payload(tmp_path, capsys):
    record_path = tmp_path / "review.json"
    record_path.write_text(json.dumps(sample_review_record()), encoding="utf-8")

    assert main(["--review-record", str(record_path), "--json", "--fail-on-unsafe-field"]) == 0
    output = capsys.readouterr().out

    assert "report.review.created" in output
    assert "sensitive review note" not in output
    assert "item_decisions" not in output
    assert "fact-secret" not in output


def test_preview_only_default_does_not_write_audit(tmp_path, monkeypatch, capsys):
    record_path = tmp_path / "review.json"
    record_path.write_text(json.dumps(sample_review_record()), encoding="utf-8")

    def fail_if_called(*_args, **_kwargs):
        raise AssertionError("audit write should not be called")

    monkeypatch.setattr(preview_module, "write_audit_event", fail_if_called)

    assert main(["--review-record", str(record_path), "--json"]) == 0
    output = json.loads(capsys.readouterr().out)

    assert output["would_write_audit_logs"] is False
    assert "audit_written" not in output


def test_write_audit_inserts_sanitized_report_level_event(tmp_path, capsys):
    record_path = tmp_path / "review.json"
    db_path = tmp_path / "audit.db"
    record_path.write_text(json.dumps(sample_review_record()), encoding="utf-8")

    assert main(["--review-record", str(record_path), "--json", "--write-audit", "--db-url", f"sqlite:///{db_path}"]) == 0
    output = json.loads(capsys.readouterr().out)

    assert output["would_write_audit_logs"] is True
    assert output["audit_written"] is True
    assert output["audit_event_id"]

    engine = create_engine(f"sqlite:///{db_path}")
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    event = db.query(AuditLog).one()
    encoded_event = json.dumps(
        {
            "request_json": event.request_json,
            "result_json": event.result_json,
        },
        ensure_ascii=False,
    )

    assert event.action == "report.review.created"
    assert event.resource_type == "report_review"
    assert event.resource_id == "review-123"
    assert event.user_id == "reviewer-a"
    assert event.request_json == {
        "source": "review_record",
        "report_hash": "sha256:abc123",
        "report_type": "repair_plan",
        "review_status": "approved_for_manual_action",
        "reviewed_at": "2026-04-27T01:02:03+00:00",
    }
    assert event.result_json == {
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
    }
    assert "sensitive review note" not in encoded_event
    assert "sensitive reason" not in encoded_event
    assert "manual revalidation" not in encoded_event
    assert "item_decisions" not in encoded_event
    assert "fact-secret" not in encoded_event
    assert "/Users/example/private" not in encoded_event


def test_audit_log_payload_is_report_level_only():
    payload = build_audit_preview(sample_review_record())
    db_payload = audit_log_payload(payload)
    encoded = json.dumps(db_payload, ensure_ascii=False)

    assert db_payload["action"] == "report.review.created"
    assert db_payload["resource_type"] == "report_review"
    assert "item_decisions" not in encoded
    assert "fact-secret" not in encoded
    assert "document_id" not in encoded
    assert "source_chunk_id" not in encoded
    assert unsafe_payload_keys(db_payload, forbidden_keys=preview_module.FORBIDDEN_WRITE_KEYS) == set()


def test_write_audit_failure_fails_open(tmp_path, monkeypatch, capsys):
    record_path = tmp_path / "review.json"
    record_path.write_text(json.dumps(sample_review_record()), encoding="utf-8")

    def fail_write(*_args, **_kwargs):
        raise RuntimeError("database path /Users/example/private/audit.db unavailable")

    monkeypatch.setattr(preview_module, "write_audit_event", fail_write)

    assert main(["--review-record", str(record_path), "--json", "--write-audit"]) == 0
    output_text = capsys.readouterr().out
    output = json.loads(output_text)

    assert output["would_write_audit_logs"] is True
    assert output["audit_written"] is False
    assert output["audit_warning"] == "audit write failed: RuntimeError"
    assert "/Users/example/private" not in output_text


def test_unsafe_record_does_not_write_audit(tmp_path, monkeypatch, capsys):
    record_path = tmp_path / "review.json"
    record_path.write_text(json.dumps(sample_review_record(executable=True)), encoding="utf-8")
    called = {"value": False}

    def record_call(*_args, **_kwargs):
        called["value"] = True
        return "audit-id"

    monkeypatch.setattr(preview_module, "write_audit_event", record_call)

    assert main(["--review-record", str(record_path), "--json", "--write-audit"]) == 1
    assert called["value"] is False
    assert "executable must be false" in capsys.readouterr().err


def test_cli_rejects_unsafe_record(tmp_path, capsys):
    record_path = tmp_path / "review.json"
    record_path.write_text(json.dumps(sample_review_record(executable=True)), encoding="utf-8")

    assert main(["--review-record", str(record_path), "--json"]) == 1
    error = capsys.readouterr().err

    assert "executable must be false" in error
