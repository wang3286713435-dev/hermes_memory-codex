#!/usr/bin/env python
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from uuid import uuid4

ROOT = Path(__file__).resolve().parents[1]

REPORT_STATUSES = {
    "pending_review",
    "acknowledged",
    "approved_for_manual_action",
    "rejected",
    "deferred",
}
ITEM_DECISIONS = {
    "needs_review",
    "acknowledged",
    "approved_for_manual_action",
    "rejected",
    "deferred",
}


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return f"sha256:{digest.hexdigest()}"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_status(status: str) -> str:
    if status not in REPORT_STATUSES:
        raise ValueError(f"invalid review status: {status}")
    return status


def validate_item_decision(decision: str) -> str:
    if decision not in ITEM_DECISIONS:
        raise ValueError(f"invalid item decision: {decision}")
    return decision


def infer_report_type(report: dict[str, Any], report_path: Path) -> str:
    if report.get("report_type"):
        return str(report["report_type"])
    if "items" in report:
        return "repair_plan"
    if "services" in report or "checks_total" in report:
        return "readiness"
    name = report_path.name.lower()
    if "repair" in name:
        return "repair_plan"
    if "readiness" in name:
        return "readiness"
    return "unknown"


def normalize_item_decision(item: dict[str, Any]) -> dict[str, Any]:
    decision = validate_item_decision(str(item.get("decision") or "needs_review"))
    return {
        "item_id": item.get("item_id"),
        "entity_id": item.get("entity_id"),
        "item_type": item.get("item_type"),
        "decision": decision,
        "reason": item.get("reason") or "",
        "recommended_next_step": item.get("recommended_next_step"),
        "approved_action": item.get("approved_action"),
        "executable": False,
    }


def skeleton_decisions_from_report(report: dict[str, Any]) -> list[dict[str, Any]]:
    decisions = []
    for idx, item in enumerate(report.get("items") or [], start=1):
        if not isinstance(item, dict):
            continue
        decisions.append(
            normalize_item_decision(
                {
                    "item_id": item.get("item_id") or item.get("id") or f"item-{idx}",
                    "entity_id": item.get("entity_id"),
                    "item_type": item.get("item_type"),
                    "decision": "needs_review",
                    "reason": "Generated skeleton decision; human review required.",
                    "recommended_next_step": item.get("recommended_action"),
                    "approved_action": None,
                }
            )
        )
    return decisions


def load_decisions(decision_file: Path | None, report: dict[str, Any]) -> list[dict[str, Any]]:
    if decision_file is None:
        return skeleton_decisions_from_report(report)
    data = load_json(decision_file)
    raw_decisions = data.get("item_decisions") if isinstance(data, dict) else data
    return [normalize_item_decision(item) for item in (raw_decisions or [])]


def decision_summary(item_decisions: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "items_total": len(item_decisions),
        "decisions_total": len(item_decisions),
        "approved_count": sum(1 for item in item_decisions if item["decision"] == "approved_for_manual_action"),
        "rejected_count": sum(1 for item in item_decisions if item["decision"] == "rejected"),
        "deferred_count": sum(1 for item in item_decisions if item["decision"] == "deferred"),
        "needs_review_count": sum(1 for item in item_decisions if item["decision"] == "needs_review"),
        "executable": False,
    }


def build_review_record(
    *,
    report_path: Path,
    report: dict[str, Any],
    reviewer: str,
    status: str,
    notes: str,
    item_decisions: list[dict[str, Any]],
    reviewed_at: str | None = None,
) -> dict[str, Any]:
    status = validate_status(status)
    reviewed_at = reviewed_at or datetime.now(timezone.utc).isoformat()
    return {
        "review_id": f"review-{uuid4()}",
        "report_path": str(report_path),
        "report_type": infer_report_type(report, report_path),
        "report_hash": file_sha256(report_path),
        "reviewer": reviewer,
        "reviewed_at": reviewed_at,
        "status": status,
        "notes": notes,
        "item_decisions": item_decisions,
        "summary": decision_summary(item_decisions),
        "executable": False,
        "dry_run": True,
        "destructive_actions": [],
    }


def review_filename(record: dict[str, Any]) -> str:
    reviewed_at = datetime.fromisoformat(record["reviewed_at"].replace("Z", "+00:00"))
    timestamp = reviewed_at.strftime("%Y%m%d_%H%M%S")
    return f"{timestamp}_{record['report_type']}_{record['status']}.json"


def write_review_record(record: dict[str, Any], output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / review_filename(record)
    path.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return path


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Create local Phase 2.27a report review records.")
    parser.add_argument("--report", type=Path, required=True, help="Readiness or repair plan report JSON.")
    parser.add_argument("--reviewer", required=True, help="Reviewer name or local identity.")
    parser.add_argument("--status", default="pending_review", help="Report-level review status.")
    parser.add_argument("--notes", default="", help="Review notes.")
    parser.add_argument("--decision-file", type=Path, help="Optional item decision JSON file.")
    parser.add_argument("--output-dir", type=Path, default=ROOT / "reviews", help="Directory for local review records.")
    parser.add_argument("--json", action="store_true", help="Print JSON summary.")
    parser.add_argument("--dry-run-preview", action="store_true", help="Print review record without writing.")
    args = parser.parse_args(argv)

    report = load_json(args.report)
    decisions = load_decisions(args.decision_file, report)
    record = build_review_record(
        report_path=args.report,
        report=report,
        reviewer=args.reviewer,
        status=args.status,
        notes=args.notes,
        item_decisions=decisions,
    )
    output_path = args.output_dir / review_filename(record)
    if not args.dry_run_preview:
        output_path = write_review_record(record, args.output_dir)

    summary = {
        "dry_run": True,
        "destructive_actions": [],
        "would_write": args.dry_run_preview,
        "output_path": str(output_path),
        "review": record,
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
