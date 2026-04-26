#!/usr/bin/env python
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]


def short_git_commit() -> str:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        return result.stdout.strip() or "unknown"
    except Exception:  # noqa: BLE001 - report archiving must still work outside git.
        return "unknown"


def timestamp_for_filename(value: str | None = None) -> str:
    if value:
        try:
            dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError:
            dt = datetime.now(timezone.utc)
    else:
        dt = datetime.now(timezone.utc)
    return dt.strftime("%Y%m%d_%H%M%S")


def status_of(report: dict[str, Any]) -> str:
    return str(report.get("status") or "unknown").lower().replace("/", "_")


def summary_counters(report: dict[str, Any]) -> dict[str, int]:
    summary = report.get("summary") if isinstance(report.get("summary"), dict) else {}
    return {
        "warnings": _as_int(summary.get("warnings", report.get("warnings", 0))),
        "critical": _as_int(summary.get("critical", 0)),
        "failures": _as_int(summary.get("failures", report.get("failed", 0))),
        "stale_facts": _as_int(summary.get("stale_facts", 0)),
        "missing_sources": _as_int(summary.get("missing_sources", 0)),
        "index_inconsistencies": _as_int(summary.get("index_inconsistencies", 0)),
    }


def build_report_filename(report_type: str, report: dict[str, Any], *, git_commit: str, generated_at: str | None = None) -> str:
    stamp = timestamp_for_filename(generated_at or report.get("generated_at"))
    return f"{stamp}_{status_of(report)}_{git_commit}.json"


def build_manifest_entry(
    *,
    report_type: str,
    report: dict[str, Any],
    path: Path,
    reports_dir: Path,
    git_commit: str,
    source_command: list[str],
    generated_at: str,
) -> dict[str, Any]:
    return {
        "generated_at": generated_at,
        "report_type": report_type,
        "status": status_of(report),
        "path": _display_path(path, reports_dir),
        "git_commit": git_commit,
        "summary": summary_counters(report),
        "source_command": source_command,
    }


def archive_report(
    *,
    report_type: str,
    report: dict[str, Any],
    reports_dir: Path,
    source_command: list[str],
    git_commit: str | None = None,
    generated_at: str | None = None,
    dry_run_preview: bool = False,
) -> dict[str, Any]:
    git_commit = git_commit or short_git_commit()
    generated_at = generated_at or datetime.now(timezone.utc).isoformat()
    subdir = reports_dir / ("readiness" if report_type == "readiness" else "repair_plan")
    path = subdir / build_report_filename(report_type, report, git_commit=git_commit, generated_at=generated_at)
    entry = build_manifest_entry(
        report_type=report_type,
        report=report,
        path=path,
        reports_dir=reports_dir,
        git_commit=git_commit,
        source_command=source_command,
        generated_at=generated_at,
    )
    if not dry_run_preview:
        subdir.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        update_manifest(reports_dir, entry, generated_at=generated_at)
        update_latest(reports_dir, report_type=report_type, report_path=path, generated_at=generated_at)
    return {
        "report_type": report_type,
        "path": _display_path(path, reports_dir),
        "status": entry["status"],
        "summary": entry["summary"],
        "would_write": dry_run_preview,
        "manifest_entry": entry,
    }


def update_manifest(reports_dir: Path, entry: dict[str, Any], *, generated_at: str) -> None:
    reports_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = reports_dir / "manifest.json"
    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    else:
        manifest = {"generated_at": generated_at, "entries": []}
    manifest["generated_at"] = generated_at
    manifest.setdefault("entries", []).append(entry)
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def update_latest(reports_dir: Path, *, report_type: str, report_path: Path, generated_at: str) -> None:
    reports_dir.mkdir(parents=True, exist_ok=True)
    latest_path = reports_dir / "latest.json"
    if latest_path.exists():
        latest = json.loads(latest_path.read_text(encoding="utf-8"))
    else:
        latest = {
            "latest_readiness_report": None,
            "latest_repair_plan_report": None,
            "updated_at": generated_at,
        }
    key = "latest_readiness_report" if report_type == "readiness" else "latest_repair_plan_report"
    latest[key] = _display_path(report_path, reports_dir)
    latest["updated_at"] = generated_at
    latest_path.write_text(json.dumps(latest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def load_json_report(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def run_report_script(command: list[str]) -> dict[str, Any]:
    result = subprocess.run(command, cwd=ROOT, check=False, capture_output=True, text=True)
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"failed to parse JSON from {' '.join(command)}: {exc}; stderr={result.stderr}") from exc


def default_readiness_command() -> list[str]:
    return [sys.executable, str(ROOT / "scripts" / "phase225_readiness_audit.py"), "--json"]


def default_repair_plan_command(document_ids: list[str]) -> list[str]:
    command = [sys.executable, str(ROOT / "scripts" / "phase226_repair_plan_dry_run.py"), "--json"]
    for document_id in document_ids:
        command.extend(["--document-id", document_id])
    return command


def item_ids(report: dict[str, Any]) -> set[str]:
    ids: set[str] = set()
    for item in report.get("items") or []:
        if isinstance(item, dict) and item.get("entity_id"):
            ids.add(str(item["entity_id"]))
    return ids


def trend_diff(old_report: dict[str, Any], new_report: dict[str, Any]) -> dict[str, Any]:
    old = summary_counters(old_report)
    new = summary_counters(new_report)
    old_ids = item_ids(old_report)
    new_ids = item_ids(new_report)
    return {
        "old_status": status_of(old_report),
        "new_status": status_of(new_report),
        "status_changed": status_of(old_report) != status_of(new_report),
        "warnings_delta": new["warnings"] - old["warnings"],
        "critical_delta": new["critical"] - old["critical"],
        "failures_delta": new["failures"] - old["failures"],
        "stale_facts_delta": new["stale_facts"] - old["stale_facts"],
        "missing_sources_delta": new["missing_sources"] - old["missing_sources"],
        "index_inconsistencies_delta": new["index_inconsistencies"] - old["index_inconsistencies"],
        "new_item_ids": sorted(new_ids - old_ids),
        "resolved_item_ids": sorted(old_ids - new_ids),
    }


def _as_int(value: Any) -> int:
    try:
        return int(value or 0)
    except (TypeError, ValueError):
        return 0


def _display_path(path: Path, reports_dir: Path) -> str:
    try:
        return path.relative_to(reports_dir).as_posix()
    except ValueError:
        try:
            return path.relative_to(ROOT).as_posix()
        except ValueError:
            return str(path)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Archive Phase 2.25/2.26 dry-run audit reports.")
    parser.add_argument("--archive-readiness", action="store_true", help="Archive readiness audit JSON.")
    parser.add_argument("--archive-repair-plan", action="store_true", help="Archive repair plan dry-run JSON.")
    parser.add_argument("--readiness-file", type=Path, help="Existing readiness JSON to archive.")
    parser.add_argument("--repair-plan-file", type=Path, help="Existing repair plan JSON to archive.")
    parser.add_argument("--reports-dir", type=Path, default=ROOT / "reports", help="Report archive directory.")
    parser.add_argument("--document-id", action="append", default=[], help="Document id passed to repair plan dry-run.")
    parser.add_argument("--diff", nargs=2, type=Path, metavar=("OLD_JSON", "NEW_JSON"), help="Compare two reports without writing.")
    parser.add_argument("--json", action="store_true", help="Print JSON summary.")
    parser.add_argument("--dry-run-preview", action="store_true", help="Preview archive paths without writing files.")
    args = parser.parse_args(argv)

    if args.diff:
        old_report = load_json_report(args.diff[0])
        new_report = load_json_report(args.diff[1])
        print(json.dumps({"dry_run": True, "trend_diff": trend_diff(old_report, new_report)}, ensure_ascii=False, indent=2))
        return 0

    generated_at = datetime.now(timezone.utc).isoformat()
    git_commit = short_git_commit()
    archived = []

    if args.archive_readiness:
        command = ["readiness-file", str(args.readiness_file)] if args.readiness_file else default_readiness_command()
        report = load_json_report(args.readiness_file) if args.readiness_file else run_report_script(command)
        archived.append(
            archive_report(
                report_type="readiness",
                report=report,
                reports_dir=args.reports_dir,
                source_command=command,
                git_commit=git_commit,
                generated_at=generated_at,
                dry_run_preview=args.dry_run_preview,
            )
        )
    if args.archive_repair_plan:
        command = ["repair-plan-file", str(args.repair_plan_file)] if args.repair_plan_file else default_repair_plan_command(args.document_id)
        report = load_json_report(args.repair_plan_file) if args.repair_plan_file else run_report_script(command)
        archived.append(
            archive_report(
                report_type="repair_plan",
                report=report,
                reports_dir=args.reports_dir,
                source_command=command,
                git_commit=git_commit,
                generated_at=generated_at,
                dry_run_preview=args.dry_run_preview,
            )
        )

    summary = {
        "dry_run": True,
        "destructive_actions": [],
        "archive_preview": args.dry_run_preview,
        "reports_dir": str(args.reports_dir),
        "archived": archived,
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
