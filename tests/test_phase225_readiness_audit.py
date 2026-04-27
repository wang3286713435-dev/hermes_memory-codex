import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.phase225_readiness_audit import (
    REPORT_REVIEW_ACTION,
    ReadinessAuditor,
    build_audit_summary,
    make_check,
    qdrant_collection_config_check,
    report_review_audit_check,
    stale_facts_check,
    summarize_section,
)


def test_summary_aggregation_marks_warn_and_keeps_dry_run_destructive_empty():
    sections = {
        "services": summarize_section(
            [
                make_check("postgres", "pass", "ok"),
                make_check("qdrant", "warn", "collection mismatch"),
            ]
        ),
        "facts_governance": summarize_section([make_check("facts", "pass", "ok")]),
    }

    summary = build_audit_summary(sections, ["inspect qdrant collection"])

    assert summary["status"] == "warn"
    assert summary["checks_total"] == 3
    assert summary["passed"] == 2
    assert summary["warnings"] == 1
    assert summary["failed"] == 0
    assert summary["destructive_actions"] == []
    assert summary["dry_run"] is True


def test_summary_aggregation_marks_fail_when_any_check_fails():
    sections = {
        "services": summarize_section([make_check("postgres", "fail", "down")]),
        "eval_readiness": summarize_section([make_check("import", "pass", "ok")]),
    }

    summary = build_audit_summary(sections, [])

    assert summary["status"] == "fail"
    assert summary["failed"] == 1


def test_qdrant_collection_config_detects_wrong_collection():
    check = qdrant_collection_config_check("hermes_gate_chunks")

    assert check["status"] == "fail"
    assert check["details"]["expected"] == "hermes_chunks"
    assert check["details"]["actual"] == "hermes_gate_chunks"
    assert check["details"]["impact"] == "dense_eval_false_failure_or_wrong_collection"


def test_qdrant_collection_config_passes_for_expected_collection():
    check = qdrant_collection_config_check("hermes_chunks")

    assert check["status"] == "pass"


def test_stale_facts_diagnostic_format_contains_latest_version():
    check = stale_facts_check(
        [
            {
                "fact_id": "fact-stale",
                "source_document_id": "doc-1",
                "source_version_id": "v1",
                "latest_version_id": "v2",
            },
            {
                "fact_id": "fact-current",
                "source_document_id": "doc-1",
                "source_version_id": "v2",
                "latest_version_id": "v2",
            },
        ]
    )

    assert check["status"] == "warn"
    assert check["details"]["count"] == 1
    assert check["details"]["examples"] == [
        {
            "fact_id": "fact-stale",
            "source_document_id": "doc-1",
            "source_version_id": "v1",
            "latest_version_id": "v2",
        }
    ]


def test_stale_facts_diagnostic_passes_without_stale_rows():
    check = stale_facts_check(
        [
            {
                "fact_id": "fact-current",
                "source_document_id": "doc-1",
                "source_version_id": "v2",
                "latest_version_id": "v2",
            }
        ]
    )

    assert check["status"] == "pass"
    assert check["details"]["count"] == 0


def test_report_review_audit_missing_event_is_warning_not_failure():
    check = report_review_audit_check([])

    assert check["status"] == "warn"
    assert check["details"]["event_type"] == REPORT_REVIEW_ACTION
    assert check["details"]["count"] == 0


def test_report_review_audit_accepts_sanitized_report_level_payload():
    check = report_review_audit_check(
        [
            {
                "audit_id": "audit-1",
                "request_json": {
                    "source": "review_record",
                    "report_hash": "sha256:abc",
                    "report_type": "repair_plan",
                    "review_status": "approved_for_manual_action",
                    "reviewed_at": "2026-04-27T00:00:00+00:00",
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
        ]
    )

    assert check["status"] == "pass"
    assert check["details"]["unsafe_count"] == 0


def test_report_review_audit_flags_sensitive_or_item_level_payload():
    check = report_review_audit_check(
        [
            {
                "audit_id": "audit-unsafe",
                "request_json": {
                    "source": "review_record",
                    "report_hash": "sha256:abc",
                    "report_type": "repair_plan",
                    "review_status": "approved_for_manual_action",
                    "reviewed_at": "2026-04-27T00:00:00+00:00",
                    "report_path": "/Users/example/private/report.json",
                },
                "result_json": {
                    "summary": {"items_total": 1},
                    "executable": False,
                    "approved_for_manual_action_is_execution": False,
                    "sanitized": True,
                    "item_decisions": [{"fact_id": "fact-secret", "reason": "private"}],
                },
            }
        ]
    )

    assert check["status"] == "fail"
    assert check["details"]["unsafe_count"] == 1
    encoded = str(check["details"]["examples"])
    assert "report_path" in encoded
    assert "item_decisions" in encoded
    assert "fact_id" in encoded


def test_audit_logs_skip_service_check_is_warning_not_failure():
    auditor = ReadinessAuditor(document_ids=[], skip_service_check=True)

    section = auditor._check_audit_logs()

    assert section["status"] == "warn"
    assert section["failed"] == 0
    assert section["warnings"] == 1
