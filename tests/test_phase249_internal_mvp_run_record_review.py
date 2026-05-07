import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.phase242a_mvp_pilot_review_dry_run import build_review_report
from scripts.phase249_internal_mvp_run_record_review import build_output, build_review_payload, main


def safe_run_record(**overrides):
    payload = {
        "record_type": "internal_mvp_pilot_run_record",
        "date": "2026-05-07",
        "run_window": "Day 1-2",
        "operator": "operator",
        "recorder": "codex-a",
        "reviewer": "codex-b",
        "source_sessions": ["session-1"],
        "alias_summary": [
            {
                "alias": "@主标书",
                "status": "pass",
                "document_id": "doc-main",
                "version_id": "ver-main",
                "alias_missing": False,
                "retrieval_suppressed": False,
            }
        ],
        "daily_query_summary": [
            {
                "query_area": "main_tender_basic_fields",
                "result": "pass",
                "evidence_document_ids": ["doc-main"],
                "citation_summary": "C1",
                "missing_evidence_visible": True,
                "facts_as_answer": False,
                "transcript_as_fact": False,
                "snapshot_as_answer": False,
                "third_document_contamination": False,
                "session_id": "session-1",
            }
        ],
        "issue_summary": {"p0_count": 0, "p1_count": 0, "p2_count": 0, "p3_count": 0, "issues": []},
        "decision": {
            "status": "Go",
            "reviewer": "codex-b",
            "not_production_rollout": True,
            "not_customer_delivery": True,
            "not_automatic_tender_review": True,
            "not_automatic_bid": True,
            "not_automatic_business_decision": True,
        },
        "boundaries": {
            "not_production_rollout": True,
            "not_customer_delivery": True,
            "not_automatic_tender_review": True,
            "not_automatic_bid": True,
            "not_automatic_business_decision": True,
            "not_repair_cleanup_backfill_reindex_delete": True,
            "no_db_facts_document_versions_auditlogs_opensearch_qdrant_mutation": True,
        },
    }
    payload.update(overrides)
    return payload


def write_json(path: Path, payload: dict) -> Path:
    path.write_text(json.dumps(payload), encoding="utf-8")
    return path


def assert_fixed_safety_flags(payload: dict) -> None:
    assert payload["dry_run"] is True
    assert payload["production_rollout"] is False
    assert payload["repair_authorized"] is False
    assert payload["destructive_actions"] == []
    assert payload["data_mutation"] is False


def test_safe_run_record_builds_go_compatible_payload():
    payload = build_review_payload(safe_run_record())
    report = build_review_report(payload)

    assert payload["decision_hint"] == "go"
    assert payload["p0_items"] == []
    assert payload["source_sessions"] == ["session-1"]
    assert payload["citation_summary"]["queries_with_citations"] == 1
    assert report["decision"] == "go"
    assert_fixed_safety_flags(payload)


def test_facts_as_answer_becomes_unsafe_no_go():
    record = safe_run_record(
        daily_query_summary=[
            {
                "query_area": "facts_policy",
                "result": "pass",
                "facts_as_answer": True,
                "transcript_as_fact": False,
                "snapshot_as_answer": False,
                "third_document_contamination": False,
            }
        ]
    )

    payload = build_review_payload(record)
    report = build_review_report(payload)

    assert payload["decision_hint"] == "no_go"
    assert payload["evidence_policy"]["facts_as_answer"] is True
    assert payload["p0_items"][0]["issue_type"] == "evidence_policy_violation"
    assert report["decision"] == "no_go"
    assert_fixed_safety_flags(payload)


def test_transcript_as_fact_becomes_unsafe_no_go():
    record = safe_run_record(
        daily_query_summary=[
            {
                "query_area": "meeting",
                "result": "pass",
                "facts_as_answer": False,
                "transcript_as_fact": True,
                "snapshot_as_answer": False,
                "third_document_contamination": False,
            }
        ]
    )

    payload = build_review_payload(record)

    assert payload["decision_hint"] == "no_go"
    assert payload["evidence_policy"]["transcript_as_fact"] is True
    assert payload["p0_items"][0]["id"] == "meeting-transcript_as_fact"


def test_third_document_contamination_becomes_p0_no_go():
    record = safe_run_record(
        daily_query_summary=[
            {
                "query_area": "compare",
                "result": "fail",
                "facts_as_answer": False,
                "transcript_as_fact": False,
                "snapshot_as_answer": False,
                "third_document_contamination": True,
            }
        ]
    )

    payload = build_review_payload(record)

    assert payload["decision_hint"] == "no_go"
    assert payload["evidence_policy"]["third_document_contamination"] is True
    assert any(item["issue_type"] == "contamination" for item in payload["p0_items"])


def test_alias_missing_pauses_unless_reviewed_workaround():
    unreviewed = build_review_payload(
        safe_run_record(
            alias_summary=[
                {
                    "alias": "@主标书",
                    "status": "fail",
                    "alias_missing": True,
                    "retrieval_suppressed": True,
                }
            ]
        )
    )
    reviewed = build_review_payload(
        safe_run_record(
            alias_summary=[
                {
                    "alias": "@主标书",
                    "status": "fail",
                    "alias_missing": True,
                    "retrieval_suppressed": True,
                    "manual_workaround": "rebind alias",
                    "review_status": "reviewed",
                }
            ]
        )
    )

    assert unreviewed["decision_hint"] == "pause"
    assert unreviewed["p1_items"][0]["blocking"] is True
    assert reviewed["decision_hint"] == "go"
    assert reviewed["p1_items"][0]["blocking"] is False


def test_hidden_missing_evidence_pauses():
    record = safe_run_record(
        daily_query_summary=[
            {
                "query_area": "price_ceiling",
                "result": "partial",
                "missing_evidence_visible": False,
                "facts_as_answer": False,
                "transcript_as_fact": False,
                "snapshot_as_answer": False,
                "third_document_contamination": False,
            }
        ]
    )

    payload = build_review_payload(record)

    assert payload["decision_hint"] == "pause"
    assert payload["evidence_policy"]["missing_evidence_hidden"] is True
    assert payload["missing_evidence"][0]["human_reviewed"] is False
    assert any(item["issue_type"] == "missing_evidence_hidden" for item in payload["p1_items"])


def test_script_requires_explicit_input_run_record_and_does_not_scan_reports():
    script = Path(__file__).resolve().parents[1] / "scripts" / "phase249_internal_mvp_run_record_review.py"

    result = subprocess.run(
        [sys.executable, str(script), "--json"],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode != 0
    assert "--input-run-record" in result.stderr
    assert "reports" not in result.stderr.lower()


def test_optional_output_writes_only_to_explicit_tmp_output_dir(tmp_path, capsys):
    input_path = write_json(tmp_path / "run_record.json", safe_run_record())
    output_dir = tmp_path / "out"

    exit_code = main(
        [
            "--input-run-record",
            str(input_path),
            "--output-dir",
            str(output_dir),
            "--review-report",
            "--json",
        ]
    )
    output = json.loads(capsys.readouterr().out)

    assert exit_code == 0
    written = output["written_outputs"]
    assert Path(written["payload_json"]).is_file()
    assert Path(written["payload_markdown"]).is_file()
    assert Path(written["review_report_json"]).is_file()
    assert Path(written["review_report_markdown"]).is_file()
    assert all(str(path).startswith(str(output_dir)) for path in written.values())
    assert output["review_report"]["decision"] == "go"


def test_build_output_can_include_phase242a_review_report():
    output = build_output(safe_run_record(), include_review_report=True)

    assert output["review_payload"]["decision_hint"] == "go"
    assert output["review_report"]["decision"] == "go"
    assert output["review_report"]["not_production_rollout_approval"] is True


def test_issue_summary_p0_count_only_becomes_placeholder_no_go():
    payload = build_review_payload(
        safe_run_record(issue_summary={"p0_count": 1, "p1_count": 0, "p2_count": 0, "p3_count": 0, "issues": []})
    )
    report = build_review_report(payload)

    assert payload["decision_hint"] == "no_go"
    assert payload["p0_items"]
    assert payload["p0_items"][0]["issue_type"] == "issue_summary_count_only"
    assert payload["p0_items"][0]["severity"] == "P0"
    assert report["decision"] == "no_go"
    assert_fixed_safety_flags(payload)


def test_repair_boundary_false_becomes_no_go_without_changing_fixed_safety_flags():
    payload = build_review_payload(
        safe_run_record(
            boundaries={
                "not_production_rollout": True,
                "not_customer_delivery": True,
                "not_automatic_tender_review": True,
                "not_automatic_bid": True,
                "not_automatic_business_decision": True,
                "not_repair_cleanup_backfill_reindex_delete": False,
                "no_db_facts_document_versions_auditlogs_opensearch_qdrant_mutation": True,
            }
        )
    )
    report = build_review_report(payload)

    assert payload["decision_hint"] == "no_go"
    assert payload["evidence_policy"]["repair_authorized"] is True
    assert any(item["id"] == "boundary-not_repair_cleanup_backfill_reindex_delete" for item in payload["p0_items"])
    assert report["decision"] == "no_go"
    assert_fixed_safety_flags(payload)


def test_data_mutation_boundary_false_becomes_no_go_without_changing_fixed_safety_flags():
    payload = build_review_payload(
        safe_run_record(
            boundaries={
                "not_production_rollout": True,
                "not_customer_delivery": True,
                "not_automatic_tender_review": True,
                "not_automatic_bid": True,
                "not_automatic_business_decision": True,
                "not_repair_cleanup_backfill_reindex_delete": True,
                "no_db_facts_document_versions_auditlogs_opensearch_qdrant_mutation": False,
            }
        )
    )
    report = build_review_report(payload)

    assert payload["decision_hint"] == "no_go"
    assert payload["evidence_policy"]["data_mutation"] is True
    assert any(
        item["id"] == "boundary-no_db_facts_document_versions_auditlogs_opensearch_qdrant_mutation"
        for item in payload["p0_items"]
    )
    assert report["decision"] == "no_go"
    assert_fixed_safety_flags(payload)


def test_issue_summary_count_placeholders_preserve_p1_p2_p3_counts():
    payload = build_review_payload(
        safe_run_record(issue_summary={"p0_count": 0, "p1_count": 1, "p2_count": 1, "p3_count": 1, "issues": []})
    )

    assert payload["decision_hint"] == "pause"
    assert payload["p1_items"][0]["blocking"] is True
    assert payload["p2_items"][0]["blocking"] is False
    assert payload["p3_items"][0]["blocking"] is False
