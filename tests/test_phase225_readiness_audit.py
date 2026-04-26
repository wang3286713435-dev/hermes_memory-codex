import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.phase225_readiness_audit import (
    build_audit_summary,
    make_check,
    qdrant_collection_config_check,
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
