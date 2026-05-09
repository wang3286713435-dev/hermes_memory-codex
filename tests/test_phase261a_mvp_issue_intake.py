from __future__ import annotations

import importlib.util
import json
from pathlib import Path

MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "phase261a_mvp_issue_intake.py"
SPEC = importlib.util.spec_from_file_location("phase261a_mvp_issue_intake", MODULE_PATH)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)

build_issue_template = MODULE.build_issue_template
evaluate_issue_payload = MODULE.evaluate_issue_payload
main = MODULE.main


def _issue(**overrides):
    base = build_issue_template()
    base.update(
        {
            "issue_id": "issue-1",
            "severity": "P2",
            "query": "围绕 @主标书 回答",
            "expected_behavior": "only target document evidence",
            "actual_behavior": "citation display incomplete",
            "operator_judgement": "partial",
        }
    )
    base.update(overrides)
    return base


def test_new_template_contains_all_fields_and_safety_flags():
    template = build_issue_template()

    for field in [
        "issue_id",
        "created_at",
        "operator",
        "session_id",
        "severity",
        "query",
        "target_alias",
        "target_document_id",
        "target_version_id",
        "expected_behavior",
        "actual_behavior",
        "returned_document_ids",
        "evidence_chunk_ids",
        "citation_present",
        "missing_evidence",
        "third_document_contamination",
        "facts_as_answer",
        "snapshot_as_answer",
        "metadata_as_answer",
        "transcript_as_fact",
        "operator_judgement",
        "recommended_owner",
        "notes",
    ]:
        assert field in template

    assert template["dry_run"] is True
    assert template["read_only"] is True
    assert template["destructive_actions"] == []
    assert template["db_or_index_written"] is False
    assert template["external_issue_created"] is False
    assert template["repair_attempted"] is False
    assert template["production_rollout"] is False


def test_single_p2_issue_is_ready():
    report = evaluate_issue_payload(_issue(severity="P2"))

    assert report["status"] == "ready"
    assert report["issue_count"] == 1
    assert report["severity_counts"]["P2"] == 1
    assert report["recommended_next_owner"] == "Codex B"
    assert report["validation_errors"] == []


def test_p1_issue_is_pause():
    report = evaluate_issue_payload(_issue(severity="P1"))

    assert report["status"] == "pause"
    assert report["p1_count"] == 1
    assert report["recommended_next_owner"] == "Codex B"


def test_p0_issue_is_no_go_and_routes_to_codex_b():
    report = evaluate_issue_payload(_issue(severity="P0"))

    assert report["status"] == "no_go"
    assert report["p0_count"] == 1
    assert report["recommended_next_owner"] == "Codex B"


def test_facts_as_answer_true_forces_no_go_even_for_p2():
    report = evaluate_issue_payload(_issue(severity="P2", facts_as_answer=True))

    assert report["status"] == "no_go"
    assert any(error["field"] == "facts_as_answer" for error in report["validation_errors"])


def test_missing_operator_judgement_is_pause():
    report = evaluate_issue_payload(_issue(operator_judgement=""))

    assert report["status"] == "pause"
    assert any(error["field"] == "operator_judgement" for error in report["validation_errors"])


def test_batch_input_counts_all_severities():
    payload = {
        "issues": [
            _issue(issue_id="p0", severity="P0"),
            _issue(issue_id="p1", severity="P1"),
            _issue(issue_id="p2", severity="P2"),
            _issue(issue_id="p3", severity="P3"),
        ]
    }

    report = evaluate_issue_payload(payload)

    assert report["status"] == "no_go"
    assert report["issue_count"] == 4
    assert report["severity_counts"] == {"P0": 1, "P1": 1, "P2": 1, "P3": 1}


def test_output_json_only_writes_explicit_path(tmp_path, capsys):
    output = tmp_path / "issue_template.json"

    exit_code = main(["--new-template", "--output-json", str(output)])

    captured = capsys.readouterr()
    assert exit_code == 0
    assert output.exists()
    assert json.loads(output.read_text(encoding="utf-8"))["dry_run"] is True
    assert json.loads(captured.out)["dry_run"] is True


def test_fixed_safety_fields_in_summary_are_never_mutating():
    report = evaluate_issue_payload(_issue())

    assert report["phase"] == "Phase 2.61a Internal MVP Issue Intake"
    assert report["dry_run"] is True
    assert report["read_only"] is True
    assert report["destructive_actions"] == []
    assert report["db_or_index_written"] is False
    assert report["external_issue_created"] is False
    assert report["repair_attempted"] is False
    assert report["production_rollout"] is False
