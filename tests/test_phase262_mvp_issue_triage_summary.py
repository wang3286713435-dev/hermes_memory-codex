from __future__ import annotations

import importlib.util
import json
from pathlib import Path

MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "phase262_mvp_issue_triage_summary.py"
SPEC = importlib.util.spec_from_file_location("phase262_mvp_issue_triage_summary", MODULE_PATH)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)

PHASE261A_PATH = Path(__file__).resolve().parents[1] / "scripts" / "phase261a_mvp_issue_intake.py"
PHASE261A_SPEC = importlib.util.spec_from_file_location("phase261a_mvp_issue_intake_for_262_tests", PHASE261A_PATH)
assert PHASE261A_SPEC and PHASE261A_SPEC.loader
PHASE261A = importlib.util.module_from_spec(PHASE261A_SPEC)
PHASE261A_SPEC.loader.exec_module(PHASE261A)

build_issue_template = PHASE261A.build_issue_template
build_summary = MODULE.build_summary
main = MODULE.main


def _issue(**overrides):
    issue = build_issue_template()
    issue.update(
        {
            "issue_id": "issue-1",
            "severity": "P2",
            "query": "围绕 @主标书 回答真实问题",
            "target_alias": "@主标书",
            "expected_behavior": "only target document evidence",
            "actual_behavior": "citation display incomplete",
            "operator_judgement": "partial",
            "recommended_owner": "Codex B",
            "notes": "local operator note with sensitive context",
            "citation_present": True,
        }
    )
    issue.update(overrides)
    return issue


def _write_json(path: Path, payload):
    path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")


def test_single_p2_issue_is_ready_and_redacted(tmp_path):
    issue_path = tmp_path / "issue.json"
    _write_json(issue_path, _issue())

    summary = build_summary(input_json_paths=[issue_path])

    assert summary["phase"] == "Phase 2.62 Internal MVP Issue Triage Summary"
    assert summary["status"] == "ready"
    assert summary["issue_count"] == 1
    assert summary["severity_counts"]["P2"] == 1
    assert summary["recommended_next_owner"] == "Codex B"
    assert summary["issue_refs"] == [
        {
            "issue_id": "issue-1",
            "severity": "P2",
            "target_alias": "@主标书",
            "recommended_owner": "Codex B",
            "source_file_name": "issue.json",
            "citation_present": True,
            "missing_evidence": False,
            "third_document_contamination": False,
            "facts_as_answer": False,
            "snapshot_as_answer": False,
            "metadata_as_answer": False,
            "transcript_as_fact": False,
        }
    ]
    serialized = json.dumps(summary, ensure_ascii=False)
    assert "围绕 @主标书" not in serialized
    assert "local operator note" not in serialized
    assert "only target document evidence" not in serialized
    assert "citation display incomplete" not in serialized


def test_p1_issue_is_pause(tmp_path):
    issue_path = tmp_path / "p1.json"
    _write_json(issue_path, _issue(severity="P1"))

    summary = build_summary(input_json_paths=[issue_path])

    assert summary["status"] == "pause"
    assert summary["severity_counts"]["P1"] == 1


def test_p0_issue_is_no_go(tmp_path):
    issue_path = tmp_path / "p0.json"
    _write_json(issue_path, _issue(severity="P0"))

    summary = build_summary(input_json_paths=[issue_path])

    assert summary["status"] == "no_go"
    assert summary["severity_counts"]["P0"] == 1


def test_dangerous_fields_force_no_go_and_are_counted(tmp_path):
    issue_path = tmp_path / "danger.json"
    _write_json(issue_path, _issue(facts_as_answer=True, third_document_contamination=True))

    summary = build_summary(input_json_paths=[issue_path])

    assert summary["status"] == "no_go"
    assert summary["dangerous_field_counts"]["facts_as_answer"] == 1
    assert summary["dangerous_field_counts"]["third_document_contamination"] == 1


def test_issue_refs_never_include_raw_sensitive_fields(tmp_path):
    issue_path = tmp_path / "sensitive.json"
    _write_json(issue_path, _issue())

    summary = build_summary(input_json_paths=[issue_path])
    ref = summary["issue_refs"][0]

    assert "query" not in ref
    assert "notes" not in ref
    assert "expected_behavior" not in ref
    assert "actual_behavior" not in ref
    assert "returned_document_ids" not in ref
    assert "evidence_chunk_ids" not in ref


def test_input_dir_reads_only_json_files(tmp_path):
    _write_json(tmp_path / "one.json", _issue(issue_id="one"))
    _write_json(tmp_path / "two.json", _issue(issue_id="two", severity="P3"))
    (tmp_path / "README.md").write_text("# ignored", encoding="utf-8")
    (tmp_path / "note.md").write_text("ignored", encoding="utf-8")
    (tmp_path / "screenshot.png").write_bytes(b"fake")

    summary = build_summary(input_dir=tmp_path)

    assert summary["input_file_count"] == 2
    assert summary["valid_file_count"] == 2
    assert summary["issue_count"] == 2
    assert {ref["source_file_name"] for ref in summary["issue_refs"]} == {"one.json", "two.json"}


def test_invalid_json_pauses_without_crashing(tmp_path):
    bad = tmp_path / "bad.json"
    bad.write_text("{not-json", encoding="utf-8")

    summary = build_summary(input_json_paths=[bad])

    assert summary["status"] == "pause"
    assert summary["input_file_count"] == 1
    assert summary["valid_file_count"] == 0
    assert summary["invalid_file_count"] == 1
    assert summary["invalid_files"][0]["source_file_name"] == "bad.json"


def test_output_json_only_writes_explicit_path(tmp_path, capsys):
    issue_path = tmp_path / "issue.json"
    output_path = tmp_path / "summary.json"
    _write_json(issue_path, _issue())

    exit_code = main(["--input-json", str(issue_path), "--output-json", str(output_path)])

    captured = capsys.readouterr()
    assert exit_code == 0
    assert output_path.exists()
    assert json.loads(output_path.read_text(encoding="utf-8"))["status"] == "ready"
    assert json.loads(captured.out)["status"] == "ready"
    assert not (tmp_path / "default-summary.json").exists()


def test_fixed_safety_fields_are_read_only(tmp_path):
    issue_path = tmp_path / "issue.json"
    _write_json(issue_path, _issue())

    summary = build_summary(input_json_paths=[issue_path])

    assert summary["dry_run"] is True
    assert summary["read_only"] is True
    assert summary["destructive_actions"] == []
    assert summary["db_or_index_written"] is False
    assert summary["external_issue_created"] is False
    assert summary["repair_attempted"] is False
    assert summary["production_rollout"] is False


def test_empty_directory_is_ready(tmp_path):
    summary = build_summary(input_dir=tmp_path)

    assert summary["status"] == "ready"
    assert summary["input_file_count"] == 0
    assert summary["issue_count"] == 0
    assert summary["operator_next_steps"][0] == "No local issue JSON files found for triage."
