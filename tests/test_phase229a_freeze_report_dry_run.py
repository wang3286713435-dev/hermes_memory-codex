import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.phase229a_freeze_report_dry_run import build_freeze_report, main


def write_json(path: Path, payload: dict) -> Path:
    path.write_text(json.dumps(payload), encoding="utf-8")
    return path


def passing_report(**extra):
    payload = {"status": "pass", "summary": {"total": 3, "passed": 3, "failed": 0, "warnings": 0}}
    payload.update(extra)
    return payload


def test_freeze_report_passes_with_required_explicit_evidence(tmp_path):
    eval_path = write_json(tmp_path / "phase214.json", passing_report())
    readiness_path = write_json(tmp_path / "readiness.json", passing_report(dry_run=True, destructive_actions=[]))
    repair_path = write_json(tmp_path / "repair.json", passing_report(dry_run=True, destructive_actions=[]))

    report = build_freeze_report(
        eval_summary_paths=[eval_path],
        readiness_report_path=readiness_path,
        repair_plan_path=repair_path,
        linkage_summary_path=None,
        generated_at="2026-04-27T00:00:00+00:00",
    )

    assert report["status"] == "pass"
    assert report["go_no_go"]["mvp_freeze_candidate"] is True
    assert report["rollout_ready"] is False
    assert report["production_rollout"] is False
    assert report["repair_executed"] is False
    assert report["destructive_actions"] == []


def test_missing_required_evidence_warns_without_scanning_directories():
    report = build_freeze_report(
        eval_summary_paths=[],
        readiness_report_path=None,
        repair_plan_path=None,
        linkage_summary_path=None,
        generated_at="2026-04-27T00:00:00+00:00",
    )

    assert report["status"] == "warn"
    assert report["go_no_go"]["mvp_freeze_candidate"] is False
    missing = [item["id"] for item in report["checklist"] if item["status"] == "warn"]
    assert missing == ["eval_summary", "readiness_report", "repair_plan"]
    assert report["evidence_inputs"] == []


def test_warning_input_makes_report_warn(tmp_path):
    eval_path = write_json(tmp_path / "phase214.json", passing_report(summary={"warnings": 1}))
    readiness_path = write_json(tmp_path / "readiness.json", passing_report(dry_run=True, destructive_actions=[]))
    repair_path = write_json(tmp_path / "repair.json", passing_report(dry_run=True, destructive_actions=[]))

    report = build_freeze_report(
        eval_summary_paths=[eval_path],
        readiness_report_path=readiness_path,
        repair_plan_path=repair_path,
        linkage_summary_path=None,
        generated_at="2026-04-27T00:00:00+00:00",
    )

    assert report["status"] == "warn"
    assert "one or more evidence inputs reported warnings" in report["risks"]


def test_unsafe_evidence_input_fails(tmp_path):
    eval_path = write_json(tmp_path / "phase214.json", passing_report())
    readiness_path = write_json(tmp_path / "readiness.json", passing_report(dry_run=False, destructive_actions=[]))
    repair_path = write_json(tmp_path / "repair.json", passing_report(dry_run=True, destructive_actions=[]))

    report = build_freeze_report(
        eval_summary_paths=[eval_path],
        readiness_report_path=readiness_path,
        repair_plan_path=repair_path,
        linkage_summary_path=None,
        generated_at="2026-04-27T00:00:00+00:00",
    )

    assert report["status"] == "fail"
    readiness = [item for item in report["evidence_inputs"] if item["type"] == "readiness_report"][0]
    assert readiness["unsafe_issues"] == ["dry_run_false"]


def test_explicit_linkage_summary_is_optional_and_recorded(tmp_path):
    eval_path = write_json(tmp_path / "phase214.json", passing_report())
    readiness_path = write_json(tmp_path / "readiness.json", passing_report(dry_run=True, destructive_actions=[]))
    repair_path = write_json(tmp_path / "repair.json", passing_report(dry_run=True, destructive_actions=[]))
    linkage_path = write_json(tmp_path / "linkage.json", passing_report())

    report = build_freeze_report(
        eval_summary_paths=[eval_path],
        readiness_report_path=readiness_path,
        repair_plan_path=repair_path,
        linkage_summary_path=linkage_path,
        generated_at="2026-04-27T00:00:00+00:00",
    )

    assert report["status"] == "pass"
    assert [item["type"] for item in report["evidence_inputs"]] == [
        "eval_summary",
        "readiness_report",
        "repair_plan",
        "linkage_summary",
    ]


def test_output_file_not_written_in_dry_run_preview(tmp_path):
    output_path = tmp_path / "freeze.json"

    exit_code = main(["--output-file", str(output_path), "--dry-run-preview", "--json"])

    assert exit_code == 0
    assert not output_path.exists()


def test_fail_on_warn_returns_nonzero_for_missing_evidence():
    assert main(["--fail-on-warn", "--json"]) == 1


def test_output_file_written_only_when_explicit(tmp_path):
    output_path = tmp_path / "freeze.json"

    exit_code = main(["--output-file", str(output_path), "--json"])

    assert exit_code == 0
    assert output_path.exists()
    report = json.loads(output_path.read_text())
    assert report["dry_run"] is True
    assert report["destructive_actions"] == []
