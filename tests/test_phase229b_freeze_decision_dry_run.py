import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.phase229b_freeze_decision_dry_run import build_decision_record, main


def write_json(path: Path, payload: dict) -> Path:
    path.write_text(json.dumps(payload), encoding="utf-8")
    return path


def assert_constants(record: dict) -> None:
    assert record["phase"] == "Phase 2.29b"
    assert record["dry_run"] is True
    assert record["production_rollout"] is False
    assert record["repair_approved"] is False
    assert record["destructive_actions"] == []


def test_pass_maps_to_mvp_freeze_candidate():
    record = build_decision_record(
        freeze_report={"status": "pass"},
        reviewer="codex-b",
        notes="reviewed",
        reviewed_at="2026-04-27T00:00:00+00:00",
    )

    assert record["decision_status"] == "approved_for_mvp_freeze_candidate"
    assert record["mvp_freeze_candidate"] is True
    assert record["manual_review_required"] is False
    assert record["reviewer"] == "codex-b"
    assert record["notes"] == "reviewed"
    assert_constants(record)


def test_warn_maps_to_manual_review():
    record = build_decision_record(
        freeze_report={"status": "warn"},
        reviewed_at="2026-04-27T00:00:00+00:00",
    )

    assert record["decision_status"] == "needs_manual_review"
    assert record["mvp_freeze_candidate"] is False
    assert record["manual_review_required"] is True
    assert_constants(record)


def test_fail_maps_to_no_go():
    record = build_decision_record(
        freeze_report={"status": "fail"},
        reviewed_at="2026-04-27T00:00:00+00:00",
    )

    assert record["decision_status"] == "no_go"
    assert record["mvp_freeze_candidate"] is False
    assert record["manual_review_required"] is True
    assert_constants(record)


def test_production_rollout_true_forces_no_go():
    record = build_decision_record(
        freeze_report={"status": "pass", "production_rollout": True},
        reviewed_at="2026-04-27T00:00:00+00:00",
    )

    assert record["decision_status"] == "no_go"
    assert record["mvp_freeze_candidate"] is False
    assert record["unsafe_conditions"] == ["production_rollout_true"]
    assert_constants(record)


def test_repair_executed_true_forces_no_go():
    record = build_decision_record(
        freeze_report={"status": "pass", "repair_executed": True},
        reviewed_at="2026-04-27T00:00:00+00:00",
    )

    assert record["decision_status"] == "no_go"
    assert record["unsafe_conditions"] == ["repair_executed_true"]
    assert_constants(record)


def test_destructive_actions_force_no_go():
    record = build_decision_record(
        freeze_report={"status": "pass", "destructive_actions": ["delete_fact"]},
        reviewed_at="2026-04-27T00:00:00+00:00",
    )

    assert record["decision_status"] == "no_go"
    assert record["unsafe_conditions"] == ["destructive_actions_present"]
    assert_constants(record)


def test_dry_run_preview_does_not_write_output_file(tmp_path):
    freeze_report_path = write_json(tmp_path / "freeze.json", {"status": "pass"})
    output_path = tmp_path / "decision.json"

    exit_code = main(
        [
            "--freeze-report",
            str(freeze_report_path),
            "--output-file",
            str(output_path),
            "--dry-run-preview",
            "--json",
        ]
    )

    assert exit_code == 0
    assert not output_path.exists()


def test_output_file_written_only_when_explicit(tmp_path):
    freeze_report_path = write_json(tmp_path / "freeze.json", {"status": "pass"})
    output_path = tmp_path / "decision.json"

    exit_code = main(["--freeze-report", str(freeze_report_path), "--output-file", str(output_path), "--json"])

    assert exit_code == 0
    assert output_path.exists()
    record = json.loads(output_path.read_text())
    assert record["decision_status"] == "approved_for_mvp_freeze_candidate"
    assert_constants(record)
