#!/usr/bin/env python3
from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path
from typing import Any

PHASE = "Phase 2.63 Internal MVP Operator Daily Summary"
SAFE_DECISIONS = ("ready", "pause", "no_go")
SENSITIVE_MARKDOWN_FIELDS = (
    "query",
    "notes",
    "expected_behavior",
    "actual_behavior",
    "returned_document_ids",
    "evidence_chunk_ids",
    "local_full_path",
    "target_document_id",
    "target_version_id",
)


def _load_phase262_module():
    module_path = Path(__file__).resolve().parent / "phase262_mvp_issue_triage_summary.py"
    spec = importlib.util.spec_from_file_location("phase262_mvp_issue_triage_summary", module_path)
    if spec is None or spec.loader is None:
        raise RuntimeError("Unable to load Phase 2.62 issue triage summary module.")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


PHASE262 = _load_phase262_module()


def _fixed_safety_fields() -> dict[str, Any]:
    return {
        "dry_run": True,
        "read_only": True,
        "production_rollout": False,
        "repair_attempted": False,
        "external_issue_created": False,
        "db_or_index_written": False,
    }


def _read_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2)
        handle.write("\n")


def _write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _safe_count(value: Any) -> int:
    try:
        return int(value or 0)
    except (TypeError, ValueError):
        return 0


def _normalize_severity_counts(summary: dict[str, Any]) -> dict[str, int]:
    raw = summary.get("severity_counts")
    counts = {severity: 0 for severity in ("P0", "P1", "P2", "P3")}
    if isinstance(raw, dict):
        for severity in counts:
            counts[severity] = _safe_count(raw.get(severity))
    return counts


def _decision_from_summary(summary: dict[str, Any]) -> str:
    status = str(summary.get("status") or summary.get("decision") or "").strip()
    if status in SAFE_DECISIONS:
        return status

    counts = _normalize_severity_counts(summary)
    if counts["P0"]:
        return "no_go"
    if counts["P1"] or summary.get("invalid_file_count") or summary.get("validation_errors"):
        return "pause"
    return "ready"


def _blocked_by(summary: dict[str, Any], decision: str, counts: dict[str, int]) -> list[str]:
    blockers: list[str] = []
    if counts["P0"]:
        blockers.append("p0_issue_present")
    if counts["P1"]:
        blockers.append("p1_issue_present")
    if summary.get("invalid_file_count"):
        blockers.append("invalid_issue_json")
    if summary.get("validation_errors"):
        blockers.append("issue_validation_errors")

    dangerous_counts = summary.get("dangerous_field_counts")
    if isinstance(dangerous_counts, dict):
        for field, count in sorted(dangerous_counts.items()):
            if _safe_count(count) > 0:
                blockers.append(f"dangerous_flag:{field}")

    if decision == "ready" and not blockers:
        return []
    return blockers or [f"decision:{decision}"]


def _recommended_actions(decision: str) -> list[str]:
    if decision == "no_go":
        return [
            "Stop internal MVP use for affected workflow.",
            "Require human owner and Codex B review before further action.",
            "Do not treat this as production-ready and do not repair automatically.",
        ]
    if decision == "pause":
        return [
            "Continue only with manual review.",
            "Keep issue records local and ignored.",
            "Do not treat the result as production-ready.",
        ]
    return [
        "Continue controlled internal MVP use.",
        "Record new issues locally with the Phase 2.61c ignored issue record policy.",
        "Review daily summary before expanding usage.",
    ]


def _operator_summary(decision: str, counts: dict[str, int], issue_count: int, blocked_by: list[str]) -> str:
    if issue_count == 0:
        return "No local issues were summarized; controlled MVP use can continue if readiness remains go."
    if decision == "no_go":
        return f"No-Go: {counts['P0']} P0 issue(s) or dangerous flag(s) require immediate human review."
    if decision == "pause":
        return f"Pause: {counts['P1']} P1 issue(s), invalid input, or validation gaps require Codex B review."
    if blocked_by:
        return "Ready with notes: no P0/P1 blockers, but review the listed diagnostics."
    return "Ready: only P2/P3 or no blocking issues were found."


def _safe_issue_refs(summary: dict[str, Any]) -> list[dict[str, Any]]:
    refs = summary.get("issue_refs")
    if not isinstance(refs, list):
        return []

    safe_refs: list[dict[str, Any]] = []
    allowed_fields = {
        "issue_id",
        "severity",
        "target_alias",
        "recommended_owner",
        "source_file_name",
        "citation_present",
        "missing_evidence",
        "third_document_contamination",
        "facts_as_answer",
        "snapshot_as_answer",
        "metadata_as_answer",
        "transcript_as_fact",
    }
    for ref in refs:
        if not isinstance(ref, dict):
            continue
        safe_refs.append({field: ref.get(field) for field in allowed_fields})
    return safe_refs


def build_daily_summary(summary: dict[str, Any]) -> dict[str, Any]:
    counts = _normalize_severity_counts(summary)
    decision = _decision_from_summary(summary)
    p0_count = counts["P0"]
    p1_count = counts["P1"]
    issue_count = _safe_count(summary.get("issue_count"))
    blockers = _blocked_by(summary, decision, counts)

    return {
        "phase": PHASE,
        **_fixed_safety_fields(),
        "decision": decision,
        "severity_counts": counts,
        "p0_count": p0_count,
        "p1_count": p1_count,
        "operator_summary": _operator_summary(decision, counts, issue_count, blockers),
        "codex_b_review_needed": decision != "ready",
        "codex_c_validation_needed": False,
        "recommended_actions": _recommended_actions(decision),
        "blocked_by": blockers,
        "issue_refs": _safe_issue_refs(summary),
        "source_summary": {
            "phase": summary.get("phase") or "",
            "status": summary.get("status") or summary.get("decision") or "",
            "input_file_count": _safe_count(summary.get("input_file_count")),
            "valid_file_count": _safe_count(summary.get("valid_file_count")),
            "invalid_file_count": _safe_count(summary.get("invalid_file_count")),
            "issue_count": issue_count,
        },
    }


def build_summary_from_inputs(
    issue_summary_json: Path | None = None,
    input_json_paths: list[Path] | None = None,
    input_dir: Path | None = None,
) -> dict[str, Any]:
    if issue_summary_json:
        raw = _read_json(issue_summary_json)
        if not isinstance(raw, dict):
            raise ValueError("Issue summary JSON must be an object.")
        return build_daily_summary(raw)

    source_summary = PHASE262.build_summary(input_json_paths=input_json_paths or [], input_dir=input_dir)
    return build_daily_summary(source_summary)


def build_markdown_summary(payload: dict[str, Any]) -> str:
    lines = [
        "# Internal MVP Daily Summary",
        "",
        f"- Phase: {payload.get('phase', '')}",
        f"- Decision: {payload.get('decision', '')}",
        f"- P0: {payload.get('p0_count', 0)}",
        f"- P1: {payload.get('p1_count', 0)}",
        f"- Codex B review needed: {str(payload.get('codex_b_review_needed')).lower()}",
        f"- Codex C validation needed: {str(payload.get('codex_c_validation_needed')).lower()}",
        "",
        "## Operator Summary",
        "",
        str(payload.get("operator_summary", "")),
        "",
        "## Recommended Actions",
    ]
    for action in payload.get("recommended_actions", []):
        lines.append(f"- {action}")

    blocked_by = payload.get("blocked_by") or []
    lines.extend(["", "## Blocked By"])
    if blocked_by:
        lines.extend(f"- {item}" for item in blocked_by)
    else:
        lines.append("- none")

    lines.extend(["", "## Issue References"])
    issue_refs = payload.get("issue_refs") or []
    if not issue_refs:
        lines.append("- none")
    for ref in issue_refs:
        if not isinstance(ref, dict):
            continue
        lines.append(
            "- "
            + " | ".join(
                [
                    f"id={ref.get('issue_id') or ''}",
                    f"severity={ref.get('severity') or ''}",
                    f"alias={ref.get('target_alias') or ''}",
                    f"owner={ref.get('recommended_owner') or ''}",
                    f"source={ref.get('source_file_name') or ''}",
                ]
            )
        )

    rendered = "\n".join(lines).rstrip() + "\n"
    for field in SENSITIVE_MARKDOWN_FIELDS:
        if field in rendered:
            raise ValueError(f"Unsafe markdown output contains sensitive field name: {field}")
    return rendered


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Phase 2.63 internal MVP operator daily summary runner.")
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--issue-summary-json", type=Path, help="Phase 2.62 summary JSON file.")
    source.add_argument("--input-dir", type=Path, help="Directory containing local issue JSON files.")
    source.add_argument("--input-json", type=Path, action="append", default=[], help="Issue JSON file. Can be repeated.")
    parser.add_argument("--output-json", type=Path, help="Optional explicit JSON output path.")
    parser.add_argument("--output-md", type=Path, help="Optional explicit sanitized Markdown output path.")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    payload = build_summary_from_inputs(
        issue_summary_json=args.issue_summary_json,
        input_json_paths=args.input_json,
        input_dir=args.input_dir,
    )
    if args.output_json:
        _write_json(args.output_json, payload)
    if args.output_md:
        _write_text(args.output_md, build_markdown_summary(payload))

    json.dump(payload, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
