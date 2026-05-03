from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "phase237d_pilot_triage_summary.py"
SPEC = importlib.util.spec_from_file_location("phase237d_pilot_triage_summary", SCRIPT_PATH)
assert SPEC is not None
assert SPEC.loader is not None
triage = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = triage
SPEC.loader.exec_module(triage)


def _issue(**overrides):
    record = triage.issue_intake.issue_template()
    record.update(overrides)
    return record


def _write_issue(path: Path, **overrides) -> None:
    path.write_text(json.dumps(_issue(**overrides), ensure_ascii=False), encoding="utf-8")


def test_empty_input_dir_continues(tmp_path):
    records, warnings = triage.load_valid_issue_records(tmp_path)
    summary = triage.build_triage_summary(records, warnings, "2026-05-03")

    assert summary["source_issue_count"] == 0
    assert summary["go_pause_recommendation"] == "continue"
    assert summary["destructive_actions"] == []
    assert summary["human_review_required"] is True


def test_p0_issue_pauses_pilot(tmp_path):
    _write_issue(tmp_path / "p0.json", issue_id="p0", priority="P0", issue_type="answer_boundary")

    records, warnings = triage.load_valid_issue_records(tmp_path)
    summary = triage.build_triage_summary(records, warnings, "2026-05-03")

    assert summary["counts_by_priority"]["P0"] == 1
    assert summary["go_pause_recommendation"] == "pause"
    assert summary["p0_items"][0]["issue_id"] == "p0"


def test_p1_without_p0_requires_manual_review(tmp_path):
    _write_issue(tmp_path / "p1.json", issue_id="p1", priority="P1", issue_type="retrieval_recall")

    records, warnings = triage.load_valid_issue_records(tmp_path)
    summary = triage.build_triage_summary(records, warnings, "2026-05-03")

    assert summary["counts_by_priority"]["P1"] == 1
    assert summary["go_pause_recommendation"] == "continue_with_manual_review"
    assert "manual review" in summary["suggested_next_action"]


def test_only_p2_p3_continues_and_counts_issue_types(tmp_path):
    _write_issue(tmp_path / "p2.json", issue_id="p2", priority="P2", issue_type="latency")
    _write_issue(tmp_path / "p3.json", issue_id="p3", priority="P3", issue_type="documentation")

    records, warnings = triage.load_valid_issue_records(tmp_path)
    summary = triage.build_triage_summary(records, warnings, "2026-05-03")

    assert summary["go_pause_recommendation"] == "continue"
    assert summary["counts_by_priority"]["P2"] == 1
    assert summary["counts_by_priority"]["P3"] == 1
    assert summary["counts_by_issue_type"]["latency"] == 1
    assert summary["counts_by_issue_type"]["documentation"] == 1


def test_missing_evidence_items_are_extracted(tmp_path):
    _write_issue(
        tmp_path / "missing.json",
        issue_id="missing",
        actual_behavior="Missing Evidence was correctly returned for absent amount.",
        safety_boundary=["missing_evidence", "evidence_required"],
    )

    records, warnings = triage.load_valid_issue_records(tmp_path)
    summary = triage.build_triage_summary(records, warnings, "2026-05-03")

    assert [item["issue_id"] for item in summary["missing_evidence_items"]] == ["missing"]


def test_dry_run_preview_does_not_write_files(tmp_path, capsys):
    input_dir = tmp_path / "issues"
    output_dir = tmp_path / "triage"
    input_dir.mkdir()
    _write_issue(input_dir / "p1.json", issue_id="p1", priority="P1")

    exit_code = triage.main(
        [
            "--input-dir",
            str(input_dir),
            "--output-dir",
            str(output_dir),
            "--date",
            "2026-05-03",
            "--dry-run-preview",
        ]
    )
    payload = json.loads(capsys.readouterr().out)

    assert exit_code == 0
    assert payload["output_files"] == []
    assert not output_dir.exists()


def test_writes_json_and_markdown_outputs_to_requested_directory(tmp_path, capsys):
    input_dir = tmp_path / "issues"
    output_dir = tmp_path / "triage"
    input_dir.mkdir()
    _write_issue(input_dir / "p1.json", issue_id="p1", priority="P1")

    exit_code = triage.main(
        [
            "--input-dir",
            str(input_dir),
            "--output-dir",
            str(output_dir),
            "--date",
            "2026-05-03",
            "--format",
            "both",
        ]
    )
    payload = json.loads(capsys.readouterr().out)
    json_path = output_dir / "20260503_pilot_triage_summary.json"
    md_path = output_dir / "20260503_pilot_triage_summary.md"

    assert exit_code == 0
    assert json_path.exists()
    assert md_path.exists()
    assert str(json_path) in payload["output_files"]
    markdown = md_path.read_text(encoding="utf-8")
    assert "This is not a repair result." in markdown
    assert "This is not rollout approval." in markdown
    assert "Missing Evidence must not be hidden" in markdown


def test_malformed_records_warn_and_strict_returns_nonzero(tmp_path, capsys):
    (tmp_path / "bad.json").write_text("{bad", encoding="utf-8")

    non_strict_exit = triage.main(["--input-dir", str(tmp_path), "--dry-run-preview"])
    non_strict_payload = json.loads(capsys.readouterr().out)
    strict_exit = triage.main(["--input-dir", str(tmp_path), "--dry-run-preview", "--strict"])
    strict_payload = json.loads(capsys.readouterr().out)

    assert non_strict_exit == 0
    assert non_strict_payload["skipped_issue_count"] == 1
    assert non_strict_payload["warnings"][0]["warning"] == "malformed_json"
    assert strict_exit == 1
    assert strict_payload["skipped_issue_count"] == 1


def test_reports_pilot_triage_ignore_policy_exists():
    ignore_path = Path(__file__).resolve().parents[1] / "reports" / "pilot_triage" / ".gitignore"
    content = ignore_path.read_text(encoding="utf-8")

    assert "*.json" in content
    assert "*.md" in content
    assert "!README.md" in content
