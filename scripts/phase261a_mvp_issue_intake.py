#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

PHASE = "Phase 2.61a Internal MVP Issue Intake"
SEVERITIES = ("P0", "P1", "P2", "P3")
DANGEROUS_BOOLEAN_FIELDS = (
    "facts_as_answer",
    "snapshot_as_answer",
    "metadata_as_answer",
    "transcript_as_fact",
    "third_document_contamination",
    "repair_attempted",
    "db_or_index_written",
    "production_rollout",
)


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def fixed_safety_fields() -> dict[str, Any]:
    return {
        "dry_run": True,
        "read_only": True,
        "destructive_actions": [],
        "db_or_index_written": False,
        "external_issue_created": False,
        "repair_attempted": False,
        "production_rollout": False,
    }


def build_issue_template() -> dict[str, Any]:
    return {
        "issue_id": "",
        "created_at": utc_now(),
        "operator": "",
        "session_id": "",
        "severity": "P2",
        "query": "",
        "target_alias": "",
        "target_document_id": "",
        "target_version_id": "",
        "expected_behavior": "",
        "actual_behavior": "",
        "returned_document_ids": [],
        "evidence_chunk_ids": [],
        "citation_present": False,
        "missing_evidence": False,
        "third_document_contamination": False,
        "facts_as_answer": False,
        "snapshot_as_answer": False,
        "metadata_as_answer": False,
        "transcript_as_fact": False,
        "operator_judgement": "",
        "recommended_owner": "Codex B",
        "notes": "",
        **fixed_safety_fields(),
        "external_issue_created": False,
    }


def normalize_issues(payload: Any) -> tuple[list[dict[str, Any]], list[dict[str, str]]]:
    if isinstance(payload, dict) and isinstance(payload.get("issues"), list):
        issues = payload["issues"]
    elif isinstance(payload, dict):
        issues = [payload]
    else:
        return [], [{"issue_index": "payload", "field": "payload", "message": "Input must be an issue object or an object with issues[]."}]

    errors: list[dict[str, str]] = []
    normalized: list[dict[str, Any]] = []
    for index, issue in enumerate(issues):
        if not isinstance(issue, dict):
            errors.append({"issue_index": str(index), "field": "issue", "message": "Issue must be an object."})
            continue
        normalized.append(issue)
    return normalized, errors


def validate_issue(issue: dict[str, Any], index: int) -> list[dict[str, str]]:
    errors: list[dict[str, str]] = []
    severity = issue.get("severity")
    if severity not in SEVERITIES:
        errors.append(
            {
                "issue_index": str(index),
                "field": "severity",
                "message": "severity must be one of P0, P1, P2, P3.",
            }
        )

    if not str(issue.get("operator_judgement") or "").strip():
        errors.append(
            {
                "issue_index": str(index),
                "field": "operator_judgement",
                "message": "operator_judgement is required.",
            }
        )

    for field in DANGEROUS_BOOLEAN_FIELDS:
        if issue.get(field) is True:
            errors.append(
                {
                    "issue_index": str(index),
                    "field": field,
                    "message": f"{field}=true requires no_go escalation.",
                }
            )

    if issue.get("destructive_actions"):
        errors.append(
            {
                "issue_index": str(index),
                "field": "destructive_actions",
                "message": "destructive_actions must be empty.",
            }
        )
    if issue.get("external_issue_created") is True:
        errors.append(
            {
                "issue_index": str(index),
                "field": "external_issue_created",
                "message": "external_issue_created=true is outside Phase 2.61a.",
            }
        )

    return errors


def compute_status(issues: list[dict[str, Any]], errors: list[dict[str, str]]) -> str:
    if any(error["field"] in DANGEROUS_BOOLEAN_FIELDS or error["field"] in {"destructive_actions", "external_issue_created"} for error in errors):
        return "no_go"
    if any(issue.get("severity") == "P0" for issue in issues):
        return "no_go"
    if errors:
        return "pause"
    if any(issue.get("severity") == "P1" for issue in issues):
        return "pause"
    return "ready"


def build_operator_next_steps(status: str, p0_count: int, p1_count: int) -> list[str]:
    if status == "no_go":
        return [
            "Stop internal MVP use for this issue path.",
            "Escalate to Codex B / human owner before any further action.",
            "Do not repair, backfill, reindex, upload, or create external issues automatically.",
        ]
    if status == "pause" or p1_count:
        return [
            "Pause affected workflow and request Codex B triage.",
            "Keep issue records local and ignored unless explicitly approved.",
            "Do not expand into repair or rollout.",
        ]
    return [
        "Keep issue record for Codex B review.",
        "Continue internal controlled use if Phase 2.60 readiness remains go.",
    ]


def evaluate_issue_payload(payload: Any) -> dict[str, Any]:
    issues, validation_errors = normalize_issues(payload)
    for index, issue in enumerate(issues):
        validation_errors.extend(validate_issue(issue, index))

    severity_counts = {severity: 0 for severity in SEVERITIES}
    for issue in issues:
        severity = issue.get("severity")
        if severity in severity_counts:
            severity_counts[severity] += 1

    status = compute_status(issues, validation_errors)
    p0_count = severity_counts["P0"]
    p1_count = severity_counts["P1"]

    return {
        "phase": PHASE,
        **fixed_safety_fields(),
        "external_issue_created": False,
        "status": status,
        "issue_count": len(issues),
        "severity_counts": severity_counts,
        "p0_count": p0_count,
        "p1_count": p1_count,
        "validation_errors": validation_errors,
        "recommended_next_owner": "Codex B",
        "operator_next_steps": build_operator_next_steps(status, p0_count, p1_count),
    }


def read_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2)
        handle.write("\n")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Phase 2.61a local MVP issue intake dry-run helper.")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--new-template", action="store_true", help="Generate a local issue intake template.")
    mode.add_argument("--input-json", type=Path, help="Validate and summarize an issue JSON file.")
    parser.add_argument("--output-json", type=Path, help="Optional explicit output path.")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    if args.new_template:
        payload = build_issue_template()
    else:
        payload = evaluate_issue_payload(read_json(args.input_json))

    if args.output_json:
        write_json(args.output_json, payload)

    json.dump(payload, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
