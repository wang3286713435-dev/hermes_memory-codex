import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.phase226b_archive_audit_reports import (
    archive_report,
    build_manifest_entry,
    build_report_filename,
    trend_diff,
)


def repair_report(*, status="warn", warnings=1, critical=0, stale_facts=1, entity_ids=None):
    return {
        "status": status,
        "summary": {
            "warnings": warnings,
            "critical": critical,
            "failures": critical,
            "stale_facts": stale_facts,
            "missing_sources": 0,
            "index_inconsistencies": 0,
        },
        "items": [{"entity_id": entity_id} for entity_id in (entity_ids or [])],
    }


def test_report_filename_contains_timestamp_status_and_commit():
    report = {"status": "warn"}

    filename = build_report_filename(
        "repair_plan",
        report,
        git_commit="abc1234",
        generated_at="2026-04-27T01:02:03+00:00",
    )

    assert filename == "20260427_010203_warn_abc1234.json"


def test_manifest_entry_extracts_summary_counters(tmp_path):
    report = repair_report(warnings=2, critical=1, stale_facts=3)
    path = tmp_path / "repair_plan" / "report.json"

    entry = build_manifest_entry(
        report_type="repair_plan",
        report=report,
        path=path,
        reports_dir=tmp_path,
        git_commit="abc1234",
        source_command=["cmd"],
        generated_at="2026-04-27T01:02:03+00:00",
    )

    assert entry["report_type"] == "repair_plan"
    assert entry["status"] == "warn"
    assert entry["path"] == "repair_plan/report.json"
    assert entry["summary"]["warnings"] == 2
    assert entry["summary"]["critical"] == 1
    assert entry["summary"]["stale_facts"] == 3


def test_archive_writes_report_manifest_and_latest_shape(tmp_path):
    report = repair_report(entity_ids=["fact-1"])

    result = archive_report(
        report_type="repair_plan",
        report=report,
        reports_dir=tmp_path,
        source_command=["repair"],
        git_commit="abc1234",
        generated_at="2026-04-27T01:02:03+00:00",
    )

    assert result["path"] == "repair_plan/20260427_010203_warn_abc1234.json"
    assert (tmp_path / result["path"]).exists()
    manifest = json.loads((tmp_path / "manifest.json").read_text())
    latest = json.loads((tmp_path / "latest.json").read_text())
    assert manifest["entries"][0]["path"] == result["path"]
    assert latest["latest_repair_plan_report"] == result["path"]
    assert latest["latest_readiness_report"] is None


def test_trend_diff_reports_deltas_and_item_changes():
    old = repair_report(warnings=1, critical=0, stale_facts=1, entity_ids=["old-fact", "same-fact"])
    new = repair_report(status="fail", warnings=2, critical=1, stale_facts=2, entity_ids=["same-fact", "new-fact"])

    diff = trend_diff(old, new)

    assert diff["status_changed"] is True
    assert diff["warnings_delta"] == 1
    assert diff["critical_delta"] == 1
    assert diff["failures_delta"] == 1
    assert diff["stale_facts_delta"] == 1
    assert diff["new_item_ids"] == ["new-fact"]
    assert diff["resolved_item_ids"] == ["old-fact"]


def test_dry_run_preview_does_not_write_files(tmp_path):
    report = repair_report()

    result = archive_report(
        report_type="readiness",
        report=report,
        reports_dir=tmp_path,
        source_command=["readiness"],
        git_commit="abc1234",
        generated_at="2026-04-27T01:02:03+00:00",
        dry_run_preview=True,
    )

    assert result["would_write"] is True
    assert result["path"] == "readiness/20260427_010203_warn_abc1234.json"
    assert not (tmp_path / "readiness").exists()
    assert not (tmp_path / "manifest.json").exists()
    assert not (tmp_path / "latest.json").exists()


def test_reports_gitignore_policy_ignores_runtime_json():
    gitignore = Path(__file__).resolve().parents[1] / "reports" / ".gitignore"
    content = gitignore.read_text()

    assert "**/*.json" in content
    assert "latest.json" in content
    assert "manifest.json" in content
