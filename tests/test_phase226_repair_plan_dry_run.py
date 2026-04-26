import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.phase226_repair_plan_dry_run import (
    build_repair_plan,
    exit_code_for_summary,
    index_inconsistency_item,
    missing_source_item,
    service_warning_item,
    stale_fact_item,
    version_inconsistency_item,
)


def test_repair_plan_summary_and_invariants():
    summary = build_repair_plan(
        [
            stale_fact_item(
                fact_id="fact-1",
                source_document_id="doc-1",
                source_version_id="v1",
                latest_version_id="v2",
            ),
            version_inconsistency_item(
                document_id="doc-2",
                version_id=None,
                issue="zero_latest_version",
                reason="no latest version",
            ),
        ],
        generated_at="2026-04-26T00:00:00+00:00",
    )

    assert summary["dry_run"] is True
    assert summary["destructive_actions"] == []
    assert summary["executable"] is False
    assert summary["status"] == "fail"
    assert summary["summary"]["items_total"] == 2
    assert summary["summary"]["warnings"] == 1
    assert summary["summary"]["critical"] == 1
    assert all(item["executable"] is False for item in summary["items"])


def test_stale_confirmed_fact_item_format_is_conservative():
    item = stale_fact_item(
        fact_id="fact-stale",
        source_document_id="doc",
        source_version_id="old",
        latest_version_id="latest",
    ).as_dict()

    assert item["item_type"] == "stale_fact"
    assert item["severity"] == "warning"
    assert item["entity_type"] == "fact"
    assert item["entity_id"] == "fact-stale"
    assert item["source_document_id"] == "doc"
    assert item["source_version_id"] == "old"
    assert item["latest_version_id"] == "latest"
    assert item["recommended_action"] == "revalidate_against_latest"
    assert item["executable"] is False


def test_missing_source_item_format_is_critical_and_non_destructive():
    item = missing_source_item(
        fact_id="fact-missing",
        source_document_id="doc",
        source_version_id="version",
        source_chunk_id="chunk",
        missing_fields=["source_chunk_id"],
    ).as_dict()

    assert item["item_type"] == "missing_source"
    assert item["severity"] == "critical"
    assert item["recommended_action"] == "mark_needs_review"
    assert "source_chunk_id" in item["reason"]
    assert item["executable"] is False


def test_version_and_index_inconsistency_items_are_plans_only():
    version_item = version_inconsistency_item(
        document_id="doc",
        version_id="version",
        issue="superseded_version_marked_active_or_latest",
        reason="bad version state",
    ).as_dict()
    index_item = index_inconsistency_item(
        document_id="doc",
        version_id="version",
        issue="opensearch_superseded_version_latest_leak",
        recommended_action="reindex_opensearch_payload",
        reason="old index payload leaked",
        severity="critical",
    ).as_dict()

    assert version_item["item_type"] == "version_inconsistency"
    assert version_item["recommended_action"] == "mark_version_needs_review"
    assert version_item["executable"] is False
    assert index_item["item_type"] == "index_inconsistency"
    assert index_item["recommended_action"] == "reindex_opensearch_payload"
    assert index_item["executable"] is False


def test_fail_on_critical_exit_behavior():
    summary = build_repair_plan(
        [
            service_warning_item(
                service="postgres",
                issue="database_unavailable",
                reason="down",
                severity="critical",
            )
        ]
    )

    assert exit_code_for_summary(summary, fail_on_critical=False) == 0
    assert exit_code_for_summary(summary, fail_on_critical=True) == 1


def test_service_unavailable_outputs_service_warning_without_crash_shape():
    item = service_warning_item(
        service="opensearch",
        issue="service_unavailable",
        reason="connection refused",
    ).as_dict()

    assert item["item_type"] == "service_warning"
    assert item["entity_type"] == "service"
    assert item["entity_id"] == "opensearch"
    assert item["recommended_action"] == "inspect_service"
    assert item["executable"] is False
