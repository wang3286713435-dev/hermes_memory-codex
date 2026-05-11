from __future__ import annotations

import importlib.util
import json
from pathlib import Path

MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "phase263_mvp_operator_daily_summary.py"
SPEC = importlib.util.spec_from_file_location("phase263_mvp_operator_daily_summary", MODULE_PATH)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)

PHASE261A_PATH = Path(__file__).resolve().parents[1] / "scripts" / "phase261a_mvp_issue_intake.py"
PHASE261A_SPEC = importlib.util.spec_from_file_location("phase261a_mvp_issue_intake_for_263_tests", PHASE261A_PATH)
assert PHASE261A_SPEC and PHASE261A_SPEC.loader
PHASE261A = importlib.util.module_from_spec(PHASE261A_SPEC)
PHASE261A_SPEC.loader.exec_module(PHASE261A)

build_issue_template = PHASE261A.build_issue_template
build_daily_summary = MODULE.build_daily_summary
build_markdown_summary = MODULE.build_markdown_summary
build_summary_from_inputs = MODULE.build_summary_from_inputs
main = MODULE.main


def _write_json(path: Path, payload):
    path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")


def _issue(**overrides):
    issue = build_issue_template()
    issue.update(
        {
            "issue_id": "issue-263",
            "severity": "P2",
            "query": "围绕 @主标书 的敏感原始问题",
            "target_alias": "@主标书",
            "expected_behavior": "sensitive expected behavior",
            "actual_behavior": "sensitive actual behavior",
            "operator_judgement": "partial",
            "recommended_owner": "Codex B",
            "notes": "sensitive local operator note",
            "returned_document_ids": ["doc-sensitive"],
            "evidence_chunk_ids": ["chunk-sensitive"],
            "citation_present": True,
        }
    )
    issue.update(overrides)
    return issue


def _phase262_summary(**overrides):
    payload = {
        "phase": "Phase 2.62 Internal MVP Issue Triage Summary",
        "status": "ready",
        "input_file_count": 1,
        "valid_file_count": 1,
        "invalid_file_count": 0,
        "issue_count": 1,
        "severity_counts": {"P0": 0, "P1": 0, "P2": 1, "P3": 0},
        "p0_count": 0,
        "p1_count": 0,
        "issue_refs": [
            {
                "issue_id": "issue-263",
                "severity": "P2",
                "target_alias": "@主标书",
                "recommended_owner": "Codex B",
                "source_file_name": "issue.json",
                "citation_present": True,
                "missing_evidence": False,
                "query": "must not leak",
                "notes": "must not leak",
            }
        ],
        "dangerous_field_counts": {"facts_as_answer": 0},
    }
    payload.update(overrides)
    return payload


def test_builds_daily_summary_from_phase262_summary_json(tmp_path):
    summary_path = tmp_path / "summary.json"
    _write_json(summary_path, _phase262_summary())

    daily = build_summary_from_inputs(issue_summary_json=summary_path)

    assert daily["phase"] == "Phase 2.63 Internal MVP Operator Daily Summary"
    assert daily["decision"] == "ready"
    assert daily["severity_counts"]["P2"] == 1
    assert daily["codex_b_review_needed"] is False
    assert daily["issue_refs"][0]["issue_id"] == "issue-263"
    serialized = json.dumps(daily, ensure_ascii=False)
    assert "must not leak" not in serialized


def test_input_dir_reuses_phase262_summary(tmp_path):
    _write_json(tmp_path / "issue.json", _issue())

    daily = build_summary_from_inputs(input_dir=tmp_path)

    assert daily["decision"] == "ready"
    assert daily["source_summary"]["input_file_count"] == 1
    assert daily["issue_refs"][0]["source_file_name"] == "issue.json"


def test_p0_decision_is_no_go():
    daily = build_daily_summary(_phase262_summary(status="no_go", severity_counts={"P0": 1, "P1": 0, "P2": 0, "P3": 0}))

    assert daily["decision"] == "no_go"
    assert daily["codex_b_review_needed"] is True
    assert "p0_issue_present" in daily["blocked_by"]
    assert "Stop internal MVP use" in daily["recommended_actions"][0]


def test_p1_decision_is_pause():
    daily = build_daily_summary(_phase262_summary(status="pause", severity_counts={"P0": 0, "P1": 1, "P2": 0, "P3": 0}))

    assert daily["decision"] == "pause"
    assert daily["codex_b_review_needed"] is True
    assert "p1_issue_present" in daily["blocked_by"]


def test_p2_p3_clean_decision_is_ready():
    daily = build_daily_summary(
        _phase262_summary(
            status="ready",
            severity_counts={"P0": 0, "P1": 0, "P2": 2, "P3": 1},
            issue_count=3,
        )
    )

    assert daily["decision"] == "ready"
    assert daily["codex_b_review_needed"] is False
    assert daily["blocked_by"] == []


def test_invalid_issue_json_pauses(tmp_path):
    (tmp_path / "bad.json").write_text("{bad-json", encoding="utf-8")

    daily = build_summary_from_inputs(input_dir=tmp_path)

    assert daily["decision"] == "pause"
    assert "invalid_issue_json" in daily["blocked_by"]


def test_markdown_output_redacts_sensitive_fields_and_values(tmp_path):
    issue_path = tmp_path / "issue.json"
    _write_json(issue_path, _issue())
    daily = build_summary_from_inputs(input_json_paths=[issue_path])

    markdown = build_markdown_summary(daily)

    assert "raw query" not in markdown
    assert "query" not in markdown
    assert "notes" not in markdown
    assert "expected_behavior" not in markdown
    assert "actual_behavior" not in markdown
    assert "doc-sensitive" not in markdown
    assert "chunk-sensitive" not in markdown
    assert "围绕 @主标书" not in markdown
    assert "sensitive local operator note" not in markdown


def test_output_files_are_only_written_when_explicit(tmp_path, capsys):
    issue_path = tmp_path / "issue.json"
    json_path = tmp_path / "daily.json"
    md_path = tmp_path / "daily.md"
    _write_json(issue_path, _issue())

    exit_code = main(["--input-json", str(issue_path), "--output-json", str(json_path), "--output-md", str(md_path)])

    captured = capsys.readouterr()
    assert exit_code == 0
    assert json_path.exists()
    assert md_path.exists()
    assert json.loads(captured.out)["decision"] == "ready"
    assert not (tmp_path / "default-daily.json").exists()
    assert not (tmp_path / "default-daily.md").exists()


def test_fixed_safety_fields_are_safe(tmp_path):
    issue_path = tmp_path / "issue.json"
    _write_json(issue_path, _issue())

    daily = build_summary_from_inputs(input_json_paths=[issue_path])

    assert daily["dry_run"] is True
    assert daily["read_only"] is True
    assert daily["production_rollout"] is False
    assert daily["repair_attempted"] is False
    assert daily["external_issue_created"] is False
    assert daily["db_or_index_written"] is False
