#!/usr/bin/env python
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any


REQUIRED_FIELDS = [
    "issue_id",
    "source",
    "source_phase",
    "reported_at",
    "reporter",
    "query",
    "aliases",
    "expected_behavior",
    "actual_behavior",
    "document_ids",
    "version_ids",
    "citations",
    "trace_flags",
    "issue_type",
    "priority",
    "safety_boundary",
    "human_review_required",
    "suggested_next_action",
    "status",
    "notes",
]

ISSUE_TYPES = [
    "retrieval_recall",
    "trace_ux",
    "latency",
    "alias_session",
    "contamination_false_positive",
    "missing_evidence_expected",
    "answer_boundary",
    "environment",
    "documentation",
]

PRIORITIES = ["P0", "P1", "P2", "P3"]

STATUSES = [
    "new",
    "triaged",
    "needs_codex_b_review",
    "needs_codex_c_validation",
    "accepted_backlog",
    "deferred",
    "closed_expected_missing_evidence",
]

SAFETY_BOUNDARIES = [
    "evidence_required",
    "missing_evidence",
    "no_fabrication",
    "facts_not_answer",
    "transcript_not_fact",
    "no_cross_document_contamination",
    "permission_boundary",
    "no_automatic_decision",
    "no_repair_rollout",
    "not_applicable",
]

LIST_FIELDS = {"aliases", "document_ids", "version_ids", "citations"}


@dataclass(frozen=True)
class ValidationResult:
    valid: bool
    issue_id: str | None
    errors: list[str]

    def as_dict(self) -> dict[str, Any]:
        return {
            "valid": self.valid,
            "issue_id": self.issue_id,
            "errors": self.errors,
        }


def issue_template() -> dict[str, Any]:
    return {
        "issue_id": "pilot-issue-001",
        "source": "codex_c_terminal_validation",
        "source_phase": "Phase 2.37",
        "reported_at": "2026-05-01T00:00:00+08:00",
        "reporter": "codex-c",
        "query": "围绕 @主标书 提取最高投标限价",
        "aliases": ["@主标书"],
        "expected_behavior": "Return cited evidence or Missing Evidence when no concrete amount exists.",
        "actual_behavior": "Missing Evidence returned; no concrete amount citation found.",
        "document_ids": ["869d4684-0a98-4825-bc72-ada65c15cfc9"],
        "version_ids": ["43558ba9-2813-42ff-b11b-3fbb4448a5bb"],
        "citations": [],
        "trace_flags": {
            "snapshot_as_answer": False,
            "facts_as_answer": False,
            "transcript_as_fact": False,
        },
        "issue_type": "retrieval_recall",
        "priority": "P1",
        "safety_boundary": ["missing_evidence", "evidence_required"],
        "human_review_required": True,
        "suggested_next_action": "Keep as Missing Evidence and review source document manually.",
        "status": "new",
        "notes": "Local dry-run template. Do not treat as an automatic repair task.",
    }


def validate_issue_record(record: dict[str, Any]) -> ValidationResult:
    errors: list[str] = []
    issue_id = record.get("issue_id") if isinstance(record.get("issue_id"), str) else None

    for field in REQUIRED_FIELDS:
        if field not in record:
            errors.append(f"missing_required_field:{field}")

    for field in LIST_FIELDS:
        if field in record and not isinstance(record[field], list):
            errors.append(f"invalid_type:{field}:expected_list")

    if "trace_flags" in record and not isinstance(record["trace_flags"], (dict, list)):
        errors.append("invalid_type:trace_flags:expected_object_or_list")

    if "human_review_required" in record and not isinstance(record["human_review_required"], bool):
        errors.append("invalid_type:human_review_required:expected_bool")

    if record.get("issue_type") not in ISSUE_TYPES:
        errors.append(f"invalid_enum:issue_type:{record.get('issue_type')}")

    if record.get("priority") not in PRIORITIES:
        errors.append(f"invalid_enum:priority:{record.get('priority')}")

    if record.get("status") not in STATUSES:
        errors.append(f"invalid_enum:status:{record.get('status')}")

    if "safety_boundary" in record:
        boundaries = record["safety_boundary"]
        if isinstance(boundaries, str):
            boundaries = [boundaries]
        if not isinstance(boundaries, list):
            errors.append("invalid_type:safety_boundary:expected_string_or_list")
        else:
            invalid = [value for value in boundaries if value not in SAFETY_BOUNDARIES]
            if invalid:
                errors.append(f"invalid_enum:safety_boundary:{','.join(map(str, invalid))}")

    return ValidationResult(valid=not errors, issue_id=issue_id, errors=errors)


def recommendation_for_priorities(priorities: Counter[str]) -> str:
    if priorities.get("P0", 0) > 0:
        return "pause"
    if priorities.get("P1", 0) > 0:
        return "continue_with_manual_review"
    return "continue"


def build_triage_summary(records: list[dict[str, Any]]) -> dict[str, Any]:
    validations = [validate_issue_record(record) for record in records]
    valid_records = [record for record, result in zip(records, validations, strict=True) if result.valid]
    invalid_records = [result.as_dict() for result in validations if not result.valid]

    by_priority = Counter(record["priority"] for record in valid_records)
    by_issue_type = Counter(record["issue_type"] for record in valid_records)
    by_status = Counter(record["status"] for record in valid_records)

    return {
        "dry_run": True,
        "destructive_actions": [],
        "writes_db": False,
        "creates_external_issue": False,
        "repairs_issue": False,
        "total": len(records),
        "valid_records": len(valid_records),
        "invalid_records": invalid_records,
        "invalid_count": len(invalid_records),
        "by_priority": {priority: by_priority.get(priority, 0) for priority in PRIORITIES},
        "by_issue_type": {issue_type: by_issue_type.get(issue_type, 0) for issue_type in ISSUE_TYPES},
        "by_status": {status: by_status.get(status, 0) for status in STATUSES},
        "p0_count": by_priority.get("P0", 0),
        "p1_count": by_priority.get("P1", 0),
        "go_pause_recommendation": recommendation_for_priorities(by_priority),
    }


def load_issue_records(input_file: Path | None, input_dir: Path | None) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    if input_file is not None:
        records.extend(_records_from_json(input_file))
    if input_dir is not None:
        for path in sorted(input_dir.glob("*.json")):
            records.extend(_records_from_json(path))
    return records


def _records_from_json(path: Path) -> list[dict[str, Any]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, list):
        return [item for item in data if isinstance(item, dict)]
    if isinstance(data, dict):
        if isinstance(data.get("issues"), list):
            return [item for item in data["issues"] if isinstance(item, dict)]
        return [data]
    return []


def _json_dump(data: Any) -> str:
    return json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Phase 2.37a local pilot issue intake dry-run.")
    parser.add_argument("--input", type=Path, help="Read one JSON issue record or JSON list.")
    parser.add_argument("--input-dir", type=Path, help="Read all *.json issue records from a directory.")
    parser.add_argument("--print-template", action="store_true", help="Print an empty issue record template.")
    parser.add_argument("--strict", action="store_true", help="Return non-zero when any issue record is invalid.")
    parser.add_argument("--json", action="store_true", help="Print JSON output. Kept for explicit CLI readability.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    if args.print_template:
        print(_json_dump(issue_template()))
        return 0

    records = load_issue_records(args.input, args.input_dir)
    summary = build_triage_summary(records)
    print(_json_dump(summary))
    if args.strict and summary["invalid_count"] > 0:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
