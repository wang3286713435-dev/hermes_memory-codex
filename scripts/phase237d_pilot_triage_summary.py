#!/usr/bin/env python
from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any


_INTAKE_PATH = Path(__file__).resolve().with_name("phase237a_pilot_issue_intake.py")
_INTAKE_SPEC = importlib.util.spec_from_file_location("phase237a_pilot_issue_intake", _INTAKE_PATH)
if _INTAKE_SPEC is None or _INTAKE_SPEC.loader is None:
    raise RuntimeError(f"Unable to load intake helper from {_INTAKE_PATH}")
issue_intake = importlib.util.module_from_spec(_INTAKE_SPEC)
sys.modules[_INTAKE_SPEC.name] = issue_intake
_INTAKE_SPEC.loader.exec_module(issue_intake)


GO_PAUSE_ACTIONS = {
    "pause": "Pause or narrow the pilot. Escalate P0 items to Codex B and user review before any fix planning.",
    "continue_with_manual_review": "Continue the pilot with manual review. P1 items may enter bounded fix planning only after human review.",
    "continue": "Continue the pilot. Batch P2/P3 items into backlog, runbook, UX, or polish planning.",
}

WORKFLOW_BLOCKER_TYPES = {
    "retrieval_recall",
    "alias_session",
    "contamination_false_positive",
    "answer_boundary",
}


def _json_dump(payload: Any) -> str:
    return json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True)


def _records_from_json(path: Path) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    warnings: list[dict[str, Any]] = []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [], [
            {
                "path": str(path),
                "issue_id": None,
                "warning": "malformed_json",
                "errors": [str(exc)],
            }
        ]

    if isinstance(data, list):
        raw_records = data
    elif isinstance(data, dict) and isinstance(data.get("issues"), list):
        raw_records = data["issues"]
    elif isinstance(data, dict):
        raw_records = [data]
    else:
        return [], [
            {
                "path": str(path),
                "issue_id": None,
                "warning": "unsupported_json_shape",
                "errors": [f"expected object, list, or object.issues list; got {type(data).__name__}"],
            }
        ]

    records: list[dict[str, Any]] = []
    for index, item in enumerate(raw_records):
        if isinstance(item, dict):
            records.append(item)
        else:
            warnings.append(
                {
                    "path": str(path),
                    "issue_id": None,
                    "warning": "non_object_issue_record",
                    "errors": [f"record_index:{index}:type:{type(item).__name__}"],
                }
            )
    return records, warnings


def load_valid_issue_records(input_dir: Path) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    records: list[dict[str, Any]] = []
    warnings: list[dict[str, Any]] = []

    if not input_dir.exists():
        return [], []

    for path in sorted(input_dir.glob("*.json")):
        loaded_records, load_warnings = _records_from_json(path)
        warnings.extend(load_warnings)
        for record in loaded_records:
            result = issue_intake.validate_issue_record(record)
            if result.valid:
                records.append(record)
            else:
                warnings.append(
                    {
                        "path": str(path),
                        "issue_id": result.issue_id,
                        "warning": "invalid_issue_record",
                        "errors": result.errors,
                    }
                )

    return records, warnings


def _compact_item(record: dict[str, Any]) -> dict[str, Any]:
    return {
        "issue_id": record.get("issue_id"),
        "priority": record.get("priority"),
        "issue_type": record.get("issue_type"),
        "status": record.get("status"),
        "query": record.get("query"),
        "document_ids": record.get("document_ids", []),
        "version_ids": record.get("version_ids", []),
        "citations": record.get("citations", []),
        "safety_boundary": record.get("safety_boundary", []),
        "expected_behavior": record.get("expected_behavior"),
        "actual_behavior": record.get("actual_behavior"),
        "suggested_next_action": record.get("suggested_next_action"),
        "human_review_required": record.get("human_review_required", True),
    }


def _text_contains_missing_evidence(record: dict[str, Any]) -> bool:
    fields = [
        record.get("expected_behavior", ""),
        record.get("actual_behavior", ""),
        record.get("suggested_next_action", ""),
        record.get("notes", ""),
    ]
    haystack = " ".join(str(value) for value in fields).lower()
    boundaries = record.get("safety_boundary", [])
    if isinstance(boundaries, str):
        boundaries = [boundaries]
    return (
        record.get("issue_type") == "missing_evidence_expected"
        or "missing evidence" in haystack
        or "missing_evidence" in boundaries
    )


def build_triage_summary(
    records: list[dict[str, Any]],
    warnings: list[dict[str, Any]] | None = None,
    summary_date: str | None = None,
) -> dict[str, Any]:
    warnings = warnings or []
    summary_date = summary_date or datetime.now().strftime("%Y-%m-%d")

    by_priority = Counter(record["priority"] for record in records)
    by_issue_type = Counter(record["issue_type"] for record in records)
    p0_items = [_compact_item(record) for record in records if record.get("priority") == "P0"]
    p1_items = [_compact_item(record) for record in records if record.get("priority") == "P1"]
    missing_evidence_items = [_compact_item(record) for record in records if _text_contains_missing_evidence(record)]
    workflow_blockers = [
        _compact_item(record)
        for record in records
        if record.get("priority") in {"P0", "P1"} and record.get("issue_type") in WORKFLOW_BLOCKER_TYPES
    ]

    if by_priority.get("P0", 0):
        recommendation = "pause"
    elif by_priority.get("P1", 0):
        recommendation = "continue_with_manual_review"
    else:
        recommendation = "continue"

    return {
        "dry_run": True,
        "destructive_actions": [],
        "writes_db": False,
        "creates_external_issue": False,
        "repairs_issue": False,
        "rollout_approved": False,
        "summary_date": summary_date,
        "source_issue_count": len(records),
        "skipped_issue_count": len(warnings),
        "warnings": warnings,
        "counts_by_priority": {priority: by_priority.get(priority, 0) for priority in issue_intake.PRIORITIES},
        "counts_by_issue_type": {
            issue_type: by_issue_type.get(issue_type, 0) for issue_type in issue_intake.ISSUE_TYPES
        },
        "p0_items": p0_items,
        "p1_items": p1_items,
        "missing_evidence_items": missing_evidence_items,
        "workflow_blockers": workflow_blockers,
        "go_pause_recommendation": recommendation,
        "suggested_next_action": GO_PAUSE_ACTIONS[recommendation],
        "human_review_required": True,
    }


def render_markdown(summary: dict[str, Any]) -> str:
    lines = [
        f"# Pilot Issue Triage Summary - {summary['summary_date']}",
        "",
        "This is not a repair result.",
        "This is not rollout approval.",
        "P1 requires human review before bounded fix planning.",
        "Missing Evidence must not be hidden or rewritten as a conclusion.",
        "",
        "## Recommendation",
        "",
        f"- go_pause_recommendation: `{summary['go_pause_recommendation']}`",
        f"- suggested_next_action: {summary['suggested_next_action']}",
        f"- human_review_required: `{str(summary['human_review_required']).lower()}`",
        f"- writes_db: `{str(summary['writes_db']).lower()}`",
        f"- creates_external_issue: `{str(summary['creates_external_issue']).lower()}`",
        f"- repairs_issue: `{str(summary['repairs_issue']).lower()}`",
        f"- rollout_approved: `{str(summary['rollout_approved']).lower()}`",
        "",
        "## Counts By Priority",
        "",
    ]
    for priority, count in summary["counts_by_priority"].items():
        lines.append(f"- {priority}: {count}")

    lines.extend(["", "## Counts By Issue Type", ""])
    for issue_type, count in summary["counts_by_issue_type"].items():
        lines.append(f"- {issue_type}: {count}")

    lines.extend(["", "## P0 Items", ""])
    lines.extend(_markdown_items(summary["p0_items"]))
    lines.extend(["", "## P1 Items", ""])
    lines.extend(_markdown_items(summary["p1_items"]))
    lines.extend(["", "## Missing Evidence Items", ""])
    lines.extend(_markdown_items(summary["missing_evidence_items"]))
    lines.extend(["", "## Workflow Blockers", ""])
    lines.extend(_markdown_items(summary["workflow_blockers"]))
    lines.extend(["", "## Warnings", ""])
    if summary["warnings"]:
        for warning in summary["warnings"]:
            lines.append(f"- {warning.get('path')}: {warning.get('warning')} {warning.get('errors', [])}")
    else:
        lines.append("- none")
    lines.append("")
    return "\n".join(lines)


def _markdown_items(items: list[dict[str, Any]]) -> list[str]:
    if not items:
        return ["- none"]
    lines: list[str] = []
    for item in items:
        lines.append(
            "- "
            f"`{item.get('issue_id')}` "
            f"[{item.get('priority')} / {item.get('issue_type')}] "
            f"{item.get('query')}"
        )
        lines.append(f"  - next: {item.get('suggested_next_action')}")
    return lines


def output_paths(output_dir: Path, summary_date: str) -> dict[str, Path]:
    safe_date = summary_date.replace("-", "")
    base = f"{safe_date}_pilot_triage_summary"
    return {
        "json": output_dir / f"{base}.json",
        "md": output_dir / f"{base}.md",
    }


def write_outputs(summary: dict[str, Any], output_dir: Path, output_format: str) -> list[str]:
    output_dir.mkdir(parents=True, exist_ok=True)
    paths = output_paths(output_dir, summary["summary_date"])
    written: list[str] = []
    if output_format in {"json", "both"}:
        paths["json"].write_text(_json_dump(summary) + "\n", encoding="utf-8")
        written.append(str(paths["json"]))
    if output_format in {"md", "both"}:
        paths["md"].write_text(render_markdown(summary), encoding="utf-8")
        written.append(str(paths["md"]))
    return written


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Phase 2.37d local Pilot issue triage summary generator.")
    parser.add_argument("--input-dir", type=Path, default=Path("reports/pilot_issues"))
    parser.add_argument("--output-dir", type=Path, default=Path("reports/pilot_triage"))
    parser.add_argument("--date", help="Summary date in YYYY-MM-DD format. Defaults to local today.")
    parser.add_argument("--dry-run-preview", action="store_true", help="Print summary only; do not write output files.")
    parser.add_argument("--format", choices=["json", "md", "both"], default="both")
    parser.add_argument("--strict", action="store_true", help="Return non-zero when any issue record is malformed.")
    parser.add_argument("--json", action="store_true", help="Print JSON output. Kept for explicit CLI readability.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    records, warnings = load_valid_issue_records(args.input_dir)
    summary = build_triage_summary(records, warnings, args.date)

    if args.dry_run_preview:
        summary["output_files"] = []
    else:
        summary["output_files"] = write_outputs(summary, args.output_dir, args.format)

    print(_json_dump(summary))

    if args.strict and warnings:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
