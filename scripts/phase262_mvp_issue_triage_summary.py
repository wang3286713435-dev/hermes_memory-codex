#!/usr/bin/env python3
from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path
from typing import Any

PHASE = "Phase 2.62 Internal MVP Issue Triage Summary"
REDACTED_FIELDS = [
    "query",
    "notes",
    "expected_behavior",
    "actual_behavior",
    "returned_document_ids",
    "evidence_chunk_ids",
    "target_document_id",
    "target_version_id",
    "local_full_path",
    "customer_context",
    "project_context",
]
ISSUE_REF_FIELDS = [
    "issue_id",
    "severity",
    "target_alias",
    "recommended_owner",
    "citation_present",
    "missing_evidence",
    "third_document_contamination",
    "facts_as_answer",
    "snapshot_as_answer",
    "metadata_as_answer",
    "transcript_as_fact",
]


def _load_phase261a_module():
    module_path = Path(__file__).resolve().parent / "phase261a_mvp_issue_intake.py"
    spec = importlib.util.spec_from_file_location("phase261a_mvp_issue_intake", module_path)
    if spec is None or spec.loader is None:
        raise RuntimeError("Unable to load Phase 2.61a issue intake module.")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


PHASE261A = _load_phase261a_module()
DANGEROUS_BOOLEAN_FIELDS = tuple(PHASE261A.DANGEROUS_BOOLEAN_FIELDS)


def _fixed_safety_fields() -> dict[str, Any]:
    return {
        "dry_run": True,
        "read_only": True,
        "destructive_actions": [],
        "db_or_index_written": False,
        "external_issue_created": False,
        "repair_attempted": False,
        "production_rollout": False,
    }


def _read_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2)
        handle.write("\n")


def _collect_input_files(
    input_json_paths: list[Path] | None = None,
    input_dir: Path | None = None,
) -> list[Path]:
    files: list[Path] = []
    if input_json_paths:
        files.extend(input_json_paths)
    if input_dir:
        files.extend(sorted(path for path in input_dir.iterdir() if path.is_file() and path.suffix == ".json"))
    return files


def _build_issue_ref(issue: dict[str, Any], source_file_name: str) -> dict[str, Any]:
    ref = {field: issue.get(field) for field in ISSUE_REF_FIELDS}
    ref["source_file_name"] = source_file_name
    return {
        "issue_id": ref.get("issue_id") or "",
        "severity": ref.get("severity") or "",
        "target_alias": ref.get("target_alias") or "",
        "recommended_owner": ref.get("recommended_owner") or "",
        "source_file_name": source_file_name,
        "citation_present": bool(ref.get("citation_present")),
        "missing_evidence": bool(ref.get("missing_evidence")),
        "third_document_contamination": bool(ref.get("third_document_contamination")),
        "facts_as_answer": bool(ref.get("facts_as_answer")),
        "snapshot_as_answer": bool(ref.get("snapshot_as_answer")),
        "metadata_as_answer": bool(ref.get("metadata_as_answer")),
        "transcript_as_fact": bool(ref.get("transcript_as_fact")),
    }


def _status_rank(status: str) -> int:
    return {"ready": 0, "pause": 1, "no_go": 2}.get(status, 1)


def _operator_next_steps(status: str, p0_count: int, p1_count: int, issue_count: int) -> list[str]:
    if issue_count == 0 and status == "ready":
        return [
            "No local issue JSON files found for triage.",
            "Continue controlled use only if Phase 2.60 readiness remains go.",
        ]
    return PHASE261A.build_operator_next_steps(status, p0_count, p1_count)


def build_summary(
    input_json_paths: list[Path] | None = None,
    input_dir: Path | None = None,
) -> dict[str, Any]:
    input_files = _collect_input_files(input_json_paths=input_json_paths, input_dir=input_dir)
    severity_counts = {severity: 0 for severity in PHASE261A.SEVERITIES}
    dangerous_field_counts = {field: 0 for field in DANGEROUS_BOOLEAN_FIELDS}
    issue_refs: list[dict[str, Any]] = []
    validation_errors: list[dict[str, Any]] = []
    invalid_files: list[dict[str, str]] = []
    valid_file_count = 0
    status = "ready"
    issue_count = 0

    for path in input_files:
        source_file_name = path.name
        try:
            payload = _read_json(path)
        except (OSError, json.JSONDecodeError) as exc:
            invalid_files.append({"source_file_name": source_file_name, "message": str(exc)})
            status = "pause" if _status_rank(status) < _status_rank("pause") else status
            continue

        valid_file_count += 1
        report = PHASE261A.evaluate_issue_payload(payload)
        status = max([status, report["status"]], key=_status_rank)
        issue_count += int(report.get("issue_count", 0))
        for severity, count in report.get("severity_counts", {}).items():
            if severity in severity_counts:
                severity_counts[severity] += int(count)
        for error in report.get("validation_errors", []):
            validation_errors.append({"source_file_name": source_file_name, **error})

        issues, _errors = PHASE261A.normalize_issues(payload)
        for issue in issues:
            issue_refs.append(_build_issue_ref(issue, source_file_name))
            for field in DANGEROUS_BOOLEAN_FIELDS:
                if issue.get(field) is True:
                    dangerous_field_counts[field] += 1

    p0_count = severity_counts["P0"]
    p1_count = severity_counts["P1"]
    if invalid_files and _status_rank(status) < _status_rank("pause"):
        status = "pause"

    return {
        "phase": PHASE,
        **_fixed_safety_fields(),
        "input_file_count": len(input_files),
        "valid_file_count": valid_file_count,
        "invalid_file_count": len(invalid_files),
        "issue_count": issue_count,
        "severity_counts": severity_counts,
        "p0_count": p0_count,
        "p1_count": p1_count,
        "status": status,
        "recommended_next_owner": "Codex B",
        "operator_next_steps": _operator_next_steps(status, p0_count, p1_count, issue_count),
        "redacted_fields": REDACTED_FIELDS,
        "dangerous_field_counts": dangerous_field_counts,
        "issue_refs": issue_refs,
        "validation_errors": validation_errors,
        "invalid_files": invalid_files,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Phase 2.62 local MVP issue triage summary runner.")
    parser.add_argument("--input-json", type=Path, action="append", default=[], help="Issue JSON file. Can be repeated.")
    parser.add_argument("--input-dir", type=Path, help="Directory containing local issue JSON files.")
    parser.add_argument("--output-json", type=Path, help="Optional explicit output path.")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if not args.input_json and not args.input_dir:
        raise SystemExit("Provide --input-json or --input-dir.")

    payload = build_summary(input_json_paths=args.input_json, input_dir=args.input_dir)
    if args.output_json:
        _write_json(args.output_json, payload)

    json.dump(payload, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
