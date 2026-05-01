from __future__ import annotations

import json
import importlib.util
import sys
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "phase237a_pilot_issue_intake.py"
SPEC = importlib.util.spec_from_file_location("phase237a_pilot_issue_intake", SCRIPT_PATH)
assert SPEC is not None
assert SPEC.loader is not None
intake = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = intake
SPEC.loader.exec_module(intake)


def _valid_issue(**overrides):
    record = intake.issue_template()
    record.update(overrides)
    return record


def test_valid_issue_record_passes():
    result = intake.validate_issue_record(_valid_issue(issue_id="issue-valid"))

    assert result.valid is True
    assert result.issue_id == "issue-valid"
    assert result.errors == []


def test_missing_required_field_is_invalid():
    record = _valid_issue()
    del record["query"]

    result = intake.validate_issue_record(record)

    assert result.valid is False
    assert "missing_required_field:query" in result.errors


def test_invalid_enum_is_invalid():
    result = intake.validate_issue_record(
        _valid_issue(issue_type="automatic_repair", priority="P9", status="executed")
    )

    assert result.valid is False
    assert "invalid_enum:issue_type:automatic_repair" in result.errors
    assert "invalid_enum:priority:P9" in result.errors
    assert "invalid_enum:status:executed" in result.errors


def test_p0_summary_pauses():
    summary = intake.build_triage_summary(
        [
            _valid_issue(issue_id="p0", priority="P0"),
            _valid_issue(issue_id="p2", priority="P2"),
        ]
    )

    assert summary["p0_count"] == 1
    assert summary["go_pause_recommendation"] == "pause"
    assert summary["destructive_actions"] == []
    assert summary["writes_db"] is False
    assert summary["creates_external_issue"] is False
    assert summary["repairs_issue"] is False


def test_p1_only_summary_requires_manual_review():
    summary = intake.build_triage_summary([_valid_issue(issue_id="p1", priority="P1")])

    assert summary["p0_count"] == 0
    assert summary["p1_count"] == 1
    assert summary["go_pause_recommendation"] == "continue_with_manual_review"


def test_p2_p3_summary_continues():
    summary = intake.build_triage_summary(
        [
            _valid_issue(issue_id="p2", priority="P2"),
            _valid_issue(issue_id="p3", priority="P3"),
        ]
    )

    assert summary["p0_count"] == 0
    assert summary["p1_count"] == 0
    assert summary["go_pause_recommendation"] == "continue"


def test_print_template_outputs_all_required_fields(capsys):
    exit_code = intake.main(["--print-template"])
    payload = json.loads(capsys.readouterr().out)

    assert exit_code == 0
    assert set(intake.REQUIRED_FIELDS).issubset(payload)


def test_directory_input_aggregates_multiple_issue_records(tmp_path):
    (tmp_path / "one.json").write_text(
        json.dumps(_valid_issue(issue_id="one", priority="P1")),
        encoding="utf-8",
    )
    (tmp_path / "two.json").write_text(
        json.dumps({"issues": [_valid_issue(issue_id="two", priority="P2")]}),
        encoding="utf-8",
    )

    records = intake.load_issue_records(None, tmp_path)
    summary = intake.build_triage_summary(records)

    assert len(records) == 2
    assert summary["total"] == 2
    assert summary["by_priority"]["P1"] == 1
    assert summary["by_priority"]["P2"] == 1


def test_strict_invalid_record_returns_nonzero(tmp_path, capsys):
    invalid = _valid_issue()
    del invalid["actual_behavior"]
    issue_path = tmp_path / "invalid.json"
    issue_path.write_text(json.dumps(invalid), encoding="utf-8")

    exit_code = intake.main(["--input", str(issue_path), "--strict"])
    summary = json.loads(capsys.readouterr().out)

    assert exit_code == 1
    assert summary["invalid_count"] == 1
    assert summary["invalid_records"][0]["errors"] == [
        "missing_required_field:actual_behavior"
    ]
