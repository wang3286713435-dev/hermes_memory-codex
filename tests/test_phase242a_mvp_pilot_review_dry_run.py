import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.phase242a_mvp_pilot_review_dry_run import build_review_report, main


def safe_input(**overrides):
    payload = {
        "pilot_round": "day-1",
        "reviewer": "codex-b",
        "source_sessions": ["session-1"],
        "p0_items": [],
        "p1_items": [{"id": "p1", "human_review_required": True}],
        "p2_items": [],
        "p3_items": [],
        "evidence_policy": {
            "facts_as_answer": False,
            "transcript_as_fact": False,
            "snapshot_as_answer": False,
        },
        "citation_summary": {"document_id_present": 3},
        "missing_evidence": [{"field": "price_ceiling", "human_reviewed": True}],
        "not_claimable_confirmed": ["production rollout"],
        "known_risks": ["deep-field recall remains partial"],
        "next_phase_candidates": ["Phase 2.42b"],
    }
    payload.update(overrides)
    return payload


def write_json(path: Path, payload: dict) -> Path:
    path.write_text(json.dumps(payload), encoding="utf-8")
    return path


def assert_safety_constants(report: dict) -> None:
    assert report["dry_run"] is True
    assert report["production_rollout"] is False
    assert report["repair_authorized"] is False
    assert report["destructive_actions"] == []
    assert report["data_mutation"] is False
    assert report["facts_as_answer"] is False
    assert report["transcript_as_fact"] is False
    assert report["snapshot_as_answer"] is False


def test_p0_input_outputs_no_go():
    report = build_review_report(safe_input(p0_items=[{"id": "p0"}]))

    assert report["decision"] == "no_go"
    assert report["p0_count"] == 1
    assert_safety_constants(report)


def test_unsafe_evidence_policy_outputs_no_go():
    payload = safe_input(
        evidence_policy={
            "facts_as_answer": True,
            "transcript_as_fact": False,
            "snapshot_as_answer": False,
        }
    )

    report = build_review_report(payload)

    assert report["decision"] == "no_go"
    assert "unsafe_evidence_policy:facts_as_answer" in report["unsafe_reasons"]
    assert_safety_constants(report)


def test_p1_reviewable_can_go_but_keeps_human_review():
    report = build_review_report(safe_input(missing_evidence=[]))

    assert report["decision"] == "go"
    assert report["human_review_required"] is True
    assert report["p1_manual_review_required"] is True
    assert "internal controlled MVP Pilot" in report["decision_reason"]
    assert_safety_constants(report)


def test_missing_evidence_without_review_pauses():
    report = build_review_report(
        safe_input(missing_evidence=[{"field": "qualification_grade", "human_reviewed": False}])
    )

    assert report["decision"] == "pause"
    assert report["missing_evidence_summary"]["unreviewed_count"] == 1
    assert "Missing Evidence" in report["decision_reason"]
    assert_safety_constants(report)


def test_rollout_repair_and_destructive_actions_force_no_go():
    report = build_review_report(
        safe_input(
            production_rollout_claimed=True,
            repair_authorized=True,
            destructive_actions=["delete_report"],
        )
    )

    assert report["decision"] == "no_go"
    assert "production_rollout_claimed" in report["unsafe_reasons"]
    assert "repair_authorized_input" in report["unsafe_reasons"]
    assert "destructive_actions_input" in report["unsafe_reasons"]
    assert_safety_constants(report)


def test_output_dir_writes_json_and_markdown_with_required_disclaimers(tmp_path, capsys):
    input_path = write_json(tmp_path / "input.json", safe_input(missing_evidence=[]))
    output_dir = tmp_path / "out"

    exit_code = main(["--input", str(input_path), "--output-dir", str(output_dir), "--json"])
    report = json.loads(capsys.readouterr().out)

    assert exit_code == 0
    json_path = Path(report["written_outputs"]["json"])
    markdown_path = Path(report["written_outputs"]["markdown"])
    assert json_path.exists()
    assert markdown_path.exists()
    markdown = markdown_path.read_text(encoding="utf-8")
    assert "This is not production rollout approval" in markdown
    assert "This is not repair authorization" in markdown
    assert "Human review required" in markdown
    assert "Missing Evidence must be manually reviewed" in markdown


def test_script_requires_explicit_input_and_does_not_default_scan_reports():
    script = Path(__file__).resolve().parents[1] / "scripts" / "phase242a_mvp_pilot_review_dry_run.py"

    result = subprocess.run(
        [sys.executable, str(script), "--json"],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode != 0
    assert "--input" in result.stderr
