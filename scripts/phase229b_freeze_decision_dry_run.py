#!/usr/bin/env python
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]


def load_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"expected JSON object: {_display_path(path)}")
    return data


def build_decision_record(
    *,
    freeze_report: dict[str, Any],
    freeze_report_path: Path | None = None,
    reviewer: str = "",
    notes: str = "",
    reviewed_at: str | None = None,
) -> dict[str, Any]:
    reviewed_at = reviewed_at or datetime.now(timezone.utc).isoformat()
    freeze_status = str(freeze_report.get("status") or "unknown").lower()
    unsafe = unsafe_conditions(freeze_report)

    if unsafe:
        decision_status = "no_go"
        mvp_freeze_candidate = False
        manual_review_required = True
    elif freeze_status == "pass":
        decision_status = "approved_for_mvp_freeze_candidate"
        mvp_freeze_candidate = True
        manual_review_required = False
    elif freeze_status == "warn":
        decision_status = "needs_manual_review"
        mvp_freeze_candidate = False
        manual_review_required = True
    else:
        decision_status = "no_go"
        mvp_freeze_candidate = False
        manual_review_required = True

    return {
        "phase": "Phase 2.29b",
        "dry_run": True,
        "decision_status": decision_status,
        "mvp_freeze_candidate": mvp_freeze_candidate,
        "manual_review_required": manual_review_required,
        "production_rollout": False,
        "repair_approved": False,
        "destructive_actions": [],
        "freeze_report_status": freeze_status,
        "freeze_report_path": _display_path(freeze_report_path) if freeze_report_path else "",
        "go_no_go_reasons": decision_reasons(freeze_status, unsafe),
        "reviewer": reviewer,
        "reviewed_at": reviewed_at,
        "notes": notes,
        "unsafe_conditions": unsafe,
        "next_steps": next_steps(decision_status),
    }


def unsafe_conditions(freeze_report: dict[str, Any]) -> list[str]:
    conditions: list[str] = []
    if freeze_report.get("production_rollout") is True:
        conditions.append("production_rollout_true")
    if freeze_report.get("repair_executed") is True:
        conditions.append("repair_executed_true")
    if freeze_report.get("destructive_actions"):
        conditions.append("destructive_actions_present")
    return conditions


def decision_reasons(freeze_status: str, unsafe: list[str]) -> list[str]:
    reasons = [
        "production rollout remains out of scope",
        "repair executor remains out of scope",
    ]
    if unsafe:
        reasons.append(f"unsafe freeze report fields detected: {', '.join(unsafe)}")
        return reasons
    if freeze_status == "pass":
        reasons.append("freeze report passed; eligible for MVP freeze candidate review only")
    elif freeze_status == "warn":
        reasons.append("freeze report warned; manual confirmation is required before MVP freeze candidate")
    elif freeze_status == "fail":
        reasons.append("freeze report failed; No-Go")
    else:
        reasons.append(f"unsupported freeze report status: {freeze_status}")
    return reasons


def next_steps(decision_status: str) -> list[str]:
    if decision_status == "approved_for_mvp_freeze_candidate":
        return ["Codex B review", "prepare MVP freeze candidate baseline decision"]
    if decision_status == "needs_manual_review":
        return ["collect manual reviewer confirmation", "rerun decision dry-run after evidence is resolved"]
    return ["do not enter MVP freeze candidate", "inspect freeze report and unsafe conditions"]


def _display_path(path: Path | None) -> str:
    if path is None:
        return ""
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.name


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build a Phase 2.29b readiness freeze decision dry-run record.")
    parser.add_argument("--freeze-report", type=Path, required=True, help="Explicit Phase 2.29a freeze report JSON path.")
    parser.add_argument("--reviewer", default="", help="Reviewer name or id.")
    parser.add_argument("--notes", default="", help="Optional review note. Do not include sensitive source text.")
    parser.add_argument("--json", action="store_true", help="Print JSON output.")
    parser.add_argument("--output-file", type=Path, help="Optional output path. Defaults to stdout only.")
    parser.add_argument("--dry-run-preview", action="store_true", help="Preview output without writing --output-file.")
    args = parser.parse_args(argv)

    freeze_report = load_json(args.freeze_report)
    record = build_decision_record(
        freeze_report=freeze_report,
        freeze_report_path=args.freeze_report,
        reviewer=args.reviewer,
        notes=args.notes,
    )

    if args.output_file and not args.dry_run_preview:
        args.output_file.parent.mkdir(parents=True, exist_ok=True)
        args.output_file.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(json.dumps(record, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
