#!/usr/bin/env python
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

REPORT_REVIEW_ACTION = "report.review.created"
FORBIDDEN_KEYS = {
    "notes",
    "reason",
    "approved_action",
    "item_decisions",
    "report_path",
    "item_id",
    "entity_id",
    "fact_id",
    "document_id",
    "source_document_id",
    "source_version_id",
    "source_chunk_id",
    "version_id",
    "chunk_id",
    "executed",
}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def build_linkage_summary(
    *,
    archive_manifest: dict[str, Any] | None,
    review_record: dict[str, Any],
    audit_event: dict[str, Any] | None,
) -> dict[str, Any]:
    archive_review = check_archive_review(archive_manifest, review_record)
    review_audit = check_review_audit(review_record, audit_event)
    warnings = [*archive_review["warnings"], *review_audit["warnings"]]
    failures = [*archive_review["failures"], *review_audit["failures"]]
    linkage_complete = archive_review["status"] == "pass" and review_audit["status"] == "pass"
    end_to_end_status = "fail" if failures else "pass" if linkage_complete else "warn"
    summary = {
        "dry_run": True,
        "destructive_actions": [],
        "status": "fail" if failures else "pass" if linkage_complete else "warn",
        "archive_review": {
            "status": archive_review["status"],
            "report_hash_matched": archive_review["report_hash_matched"],
            "report_type_matched": archive_review["report_type_matched"],
        },
        "review_audit": {
            "status": review_audit["status"],
            "review_id_matched": review_audit["review_id_matched"],
            "trace_id_matched": review_audit["trace_id_matched"],
            "event_type": review_audit["event_type"],
            "sanitized": review_audit["sanitized"],
        },
        "end_to_end": {
            "status": end_to_end_status,
            "linkage_complete": linkage_complete,
            "executable": False,
            "repair_executed": False,
        },
        "warnings": warnings,
        "failures": failures,
    }
    unsafe = unsafe_payload_paths(summary)
    if unsafe:
        summary["status"] = "fail"
        summary["end_to_end"]["status"] = "fail"
        summary["failures"].append({"code": "unsafe_output", "paths": unsafe})
    return summary


def check_archive_review(archive_manifest: dict[str, Any] | None, review_record: dict[str, Any]) -> dict[str, Any]:
    warnings: list[dict[str, Any]] = []
    failures: list[dict[str, Any]] = []

    if review_record.get("executable") is not False:
        failures.append({"code": "review_executable_not_false", "message": "Review record executable must be false."})
    if review_record.get("dry_run") is not True:
        failures.append({"code": "review_dry_run_not_true", "message": "Review record dry_run must be true."})
    if review_record.get("destructive_actions") not in ([], None):
        failures.append({"code": "review_destructive_actions_not_empty", "message": "Review record destructive_actions must be empty."})

    if archive_manifest is None:
        return {
            "status": "fail" if failures else "warn",
            "report_hash_matched": False,
            "report_type_matched": False,
            "warnings": [{"code": "archive_manifest_missing", "message": "Archive manifest not provided."}],
            "failures": failures,
        }

    review_hash = review_record.get("report_hash")
    review_type = review_record.get("report_type")
    report_entry = find_manifest_entry(archive_manifest, review_hash=review_hash, review_type=review_type)
    report_hash_matched = bool(report_entry and report_entry.get("report_hash") == review_hash)
    report_type_matched = bool(report_entry and report_entry.get("report_type") == review_type)
    if not report_entry:
        warnings.append({"code": "archive_report_not_found", "message": "No archived report entry matched review report hash/type."})
    if report_entry and not report_hash_matched:
        failures.append({"code": "report_hash_mismatch", "message": "Review report_hash does not match archive entry."})
    if report_entry and not report_type_matched:
        failures.append({"code": "report_type_mismatch", "message": "Review report_type does not match archive entry."})
    unsafe = unsafe_payload_paths({"archive_entry": report_entry or {}, "review_record_summary": review_summary_for_check(review_record)})
    if unsafe:
        failures.append({"code": "unsafe_archive_review_fields", "paths": unsafe})

    return {
        "status": "fail" if failures else "pass" if report_hash_matched and report_type_matched else "warn",
        "report_hash_matched": report_hash_matched,
        "report_type_matched": report_type_matched,
        "warnings": warnings,
        "failures": failures,
    }


def check_review_audit(review_record: dict[str, Any], audit_event: dict[str, Any] | None) -> dict[str, Any]:
    if audit_event is None:
        return {
            "status": "warn",
            "review_id_matched": False,
            "trace_id_matched": False,
            "event_type": None,
            "sanitized": False,
            "warnings": [{"code": "audit_event_missing", "message": "Audit event not provided."}],
            "failures": [],
        }

    review_id = review_record.get("review_id")
    action = audit_event.get("action") or audit_event.get("event_type")
    trace_id = audit_event.get("trace_id")
    request_json = _dict_or_empty(audit_event.get("request_json"))
    result_json = _dict_or_empty(audit_event.get("result_json"))
    resource_id = audit_event.get("resource_id")
    review_id_matched = resource_id == review_id
    trace_id_matched = trace_id == f"report_review:{review_id}"
    sanitized = result_json.get("sanitized") is True
    warnings: list[dict[str, Any]] = []
    failures: list[dict[str, Any]] = []

    if action != REPORT_REVIEW_ACTION:
        failures.append({"code": "invalid_audit_event_type", "message": "Audit event must be report.review.created."})
    if not review_id_matched:
        failures.append({"code": "review_id_mismatch", "message": "Audit event resource_id must match review_id."})
    if not trace_id_matched:
        failures.append({"code": "trace_id_mismatch", "message": "Audit event trace_id must be report_review:<review_id>."})
    if result_json.get("executable") is not False:
        failures.append({"code": "audit_executable_not_false", "message": "Audit result_json.executable must be false."})
    if result_json.get("approved_for_manual_action_is_execution") is not False:
        failures.append(
            {
                "code": "approved_for_manual_action_execution_flag_not_false",
                "message": "approved_for_manual_action must not be represented as execution.",
            }
        )
    if not sanitized:
        failures.append({"code": "audit_not_sanitized", "message": "Audit event must mark sanitized=true."})
    unsafe_top_level = unsafe_audit_top_level_paths(audit_event)
    if unsafe_top_level:
        failures.append({"code": "unsafe_audit_top_level_fields", "paths": unsafe_top_level})
    unsafe = unsafe_payload_paths({"request_json": request_json, "result_json": result_json})
    if unsafe:
        failures.append({"code": "unsafe_audit_fields", "paths": unsafe})

    return {
        "status": "fail" if failures else "pass",
        "review_id_matched": review_id_matched,
        "trace_id_matched": trace_id_matched,
        "event_type": action,
        "sanitized": sanitized,
        "warnings": warnings,
        "failures": failures,
    }


def find_manifest_entry(
    archive_manifest: dict[str, Any],
    *,
    review_hash: str | None,
    review_type: str | None,
) -> dict[str, Any] | None:
    candidates: list[Any] = []
    for key in ("reports", "entries", "items"):
        value = archive_manifest.get(key)
        if isinstance(value, list):
            candidates.extend(value)
    latest = archive_manifest.get("latest") if isinstance(archive_manifest.get("latest"), dict) else None
    if latest:
        candidates.append(latest)

    for item in candidates:
        if not isinstance(item, dict):
            continue
        report_hash = item.get("report_hash") or item.get("hash")
        report_type = item.get("report_type")
        if report_hash == review_hash and (review_type is None or report_type == review_type):
            return {
                "report_hash": report_hash,
                "report_type": report_type,
            }
    return None


def review_summary_for_check(review_record: dict[str, Any]) -> dict[str, Any]:
    return {
        "review_id": review_record.get("review_id"),
        "report_hash": review_record.get("report_hash"),
        "report_type": review_record.get("report_type"),
        "status": review_record.get("status"),
        "executable": review_record.get("executable"),
        "dry_run": review_record.get("dry_run"),
        "destructive_actions": review_record.get("destructive_actions"),
    }


def unsafe_payload_paths(value: Any, path: str = "$") -> list[str]:
    found: list[str] = []
    if isinstance(value, dict):
        for key, nested in value.items():
            child_path = f"{path}.{key}"
            if key in FORBIDDEN_KEYS:
                found.append(child_path)
            if key == "executable" and nested is not False:
                found.append(f"{child_path}:not_false")
            if key == "repair_executed" and nested is not False:
                found.append(f"{child_path}:not_false")
            found.extend(unsafe_payload_paths(nested, child_path))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            found.extend(unsafe_payload_paths(item, f"{path}[{index}]"))
    elif isinstance(value, str):
        lowered = value.strip().lower()
        if _looks_like_absolute_path(value):
            found.append(f"{path}:absolute_path")
        if lowered == "executed" or lowered == "repair_executed":
            found.append(f"{path}:executed_value")
    return found


def unsafe_audit_top_level_paths(audit_event: dict[str, Any]) -> list[str]:
    found: list[str] = []
    for key, nested in audit_event.items():
        if key in {"request_json", "result_json"}:
            continue
        child_path = f"$.{key}"
        if key in FORBIDDEN_KEYS:
            found.append(child_path)
        if key == "executable" and nested is not False:
            found.append(f"{child_path}:not_false")
        if key == "repair_executed" and nested is not False:
            found.append(f"{child_path}:not_false")
        if isinstance(nested, str):
            lowered = nested.strip().lower()
            if _looks_like_absolute_path(nested):
                found.append(f"{child_path}:absolute_path")
            if lowered == "executed" or lowered == "repair_executed":
                found.append(f"{child_path}:executed_value")
        elif isinstance(nested, (dict, list)):
            found.extend(unsafe_payload_paths(nested, child_path))
    return sorted(set(found))


def _dict_or_empty(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _looks_like_absolute_path(value: str) -> bool:
    return value.startswith("/") or (len(value) > 2 and value[1:3] == ":\\")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run Phase 2.27f archive/review/audit read-only linkage summary.")
    parser.add_argument("--archive-manifest", type=Path, help="Fake or ignored archive manifest JSON.")
    parser.add_argument("--review-record", type=Path, required=True, help="Fake or ignored local review record JSON.")
    parser.add_argument("--audit-event-file", type=Path, help="Fake or exported sanitized audit event JSON.")
    parser.add_argument("--json", action="store_true", help="Print JSON summary.")
    args = parser.parse_args(argv)

    archive_manifest = load_json(args.archive_manifest) if args.archive_manifest else None
    review_record = load_json(args.review_record)
    audit_event = load_json(args.audit_event_file) if args.audit_event_file else None
    summary = build_linkage_summary(
        archive_manifest=archive_manifest,
        review_record=review_record,
        audit_event=audit_event,
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 1 if summary["status"] == "fail" else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
