#!/usr/bin/env python
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.base import Base
from app.db.session import SessionLocal
from app.models.audit import AuditLog

FORBIDDEN_PAYLOAD_KEYS = {
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
}

FORBIDDEN_WRITE_KEYS = FORBIDDEN_PAYLOAD_KEYS | {"executed"}

SUMMARY_KEYS = (
    "items_total",
    "approved_count",
    "rejected_count",
    "deferred_count",
    "needs_review_count",
)


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_review_record(record: dict[str, Any]) -> None:
    if record.get("executable") is not False:
        raise ValueError("unsafe review record: executable must be false")
    if record.get("dry_run") is not True:
        raise ValueError("unsafe review record: dry_run must be true")
    if record.get("destructive_actions") != []:
        raise ValueError("unsafe review record: destructive_actions must be empty")


def review_summary(record: dict[str, Any]) -> dict[str, int]:
    summary = record.get("summary") if isinstance(record.get("summary"), dict) else {}
    if all(key in summary for key in SUMMARY_KEYS):
        return {key: _as_int(summary.get(key)) for key in SUMMARY_KEYS}

    decisions = record.get("item_decisions") if isinstance(record.get("item_decisions"), list) else []
    return {
        "items_total": len(decisions),
        "approved_count": sum(1 for item in decisions if _decision(item) == "approved_for_manual_action"),
        "rejected_count": sum(1 for item in decisions if _decision(item) == "rejected"),
        "deferred_count": sum(1 for item in decisions if _decision(item) == "deferred"),
        "needs_review_count": sum(1 for item in decisions if _decision(item) == "needs_review"),
    }


def build_audit_preview(record: dict[str, Any]) -> dict[str, Any]:
    validate_review_record(record)
    payload = {
        "dry_run": True,
        "event_type": "report.review.created",
        "review_id": record.get("review_id"),
        "report_hash": record.get("report_hash"),
        "report_type": record.get("report_type"),
        "review_status": record.get("status"),
        "reviewer": record.get("reviewer"),
        "reviewed_at": record.get("reviewed_at"),
        "summary": review_summary(record),
        "executable": False,
        "would_write_audit_logs": False,
    }
    assert_safe_payload(payload)
    return payload


def assert_safe_payload(value: Any, *, forbidden_keys: set[str] | None = None) -> None:
    unsafe = unsafe_payload_keys(value, forbidden_keys=forbidden_keys)
    unsafe_values = unsafe_payload_values(value)
    if unsafe or unsafe_values:
        problems = sorted(unsafe) + sorted(unsafe_values)
        raise ValueError(f"unsafe audit payload fields: {', '.join(problems)}")


def unsafe_payload_keys(value: Any, *, forbidden_keys: set[str] | None = None) -> set[str]:
    forbidden = forbidden_keys or FORBIDDEN_PAYLOAD_KEYS
    found: set[str] = set()
    if isinstance(value, dict):
        for key, nested in value.items():
            if key in forbidden:
                found.add(key)
            found.update(unsafe_payload_keys(nested, forbidden_keys=forbidden))
    elif isinstance(value, list):
        for item in value:
            found.update(unsafe_payload_keys(item, forbidden_keys=forbidden))
    return found


def unsafe_payload_values(value: Any) -> set[str]:
    found: set[str] = set()
    if isinstance(value, dict):
        for nested in value.values():
            found.update(unsafe_payload_values(nested))
    elif isinstance(value, list):
        for item in value:
            found.update(unsafe_payload_values(item))
    elif isinstance(value, str):
        if _looks_like_absolute_path(value):
            found.add("absolute_path")
    return found


def write_optional_payload(payload: dict[str, Any], output_file: Path | None) -> None:
    if output_file is None:
        return
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def apply_audit_write(payload: dict[str, Any], *, db_url: str | None = None) -> dict[str, Any]:
    payload = dict(payload)
    payload["dry_run"] = False
    payload["would_write_audit_logs"] = True
    assert_safe_payload(payload, forbidden_keys=FORBIDDEN_WRITE_KEYS)
    try:
        payload["audit_event_id"] = write_audit_event(payload, db_url=db_url)
        payload["audit_written"] = True
    except Exception as exc:  # noqa: BLE001 - audit writes must fail open for this CLI.
        payload["audit_written"] = False
        payload["audit_warning"] = _safe_warning(exc)
    return payload


def write_audit_event(payload: dict[str, Any], *, db_url: str | None = None) -> str:
    audit_payload = audit_log_payload(payload)
    assert_safe_payload(audit_payload, forbidden_keys=FORBIDDEN_WRITE_KEYS)
    SessionFactory = _session_factory(db_url)
    db = SessionFactory()
    try:
        event = AuditLog(**audit_payload)
        db.add(event)
        db.commit()
        db.refresh(event)
        return event.id
    finally:
        db.close()


def audit_log_payload(payload: dict[str, Any]) -> dict[str, Any]:
    return {
        "trace_id": f"report_review:{payload.get('review_id')}",
        "user_id": payload.get("reviewer") or "local_dev",
        "action": "report.review.created",
        "resource_type": "report_review",
        "resource_id": payload.get("review_id"),
        "request_json": {
            "source": "review_record",
            "report_hash": payload.get("report_hash"),
            "report_type": payload.get("report_type"),
            "review_status": payload.get("review_status"),
            "reviewed_at": payload.get("reviewed_at"),
        },
        "result_json": {
            "summary": payload.get("summary"),
            "executable": False,
            "approved_for_manual_action_is_execution": False,
            "sanitized": True,
        },
    }


def _session_factory(db_url: str | None):
    if not db_url:
        return SessionLocal
    engine = create_engine(db_url)
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)


def _decision(item: Any) -> str:
    if isinstance(item, dict):
        return str(item.get("decision") or "")
    return ""


def _as_int(value: Any) -> int:
    try:
        return int(value or 0)
    except (TypeError, ValueError):
        return 0


def _looks_like_absolute_path(value: str) -> bool:
    return value.startswith("/") or (len(value) > 2 and value[1:3] == ":\\")


def _safe_warning(exc: Exception) -> str:
    return f"audit write failed: {exc.__class__.__name__}"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Preview or write sanitized Phase 2.27 review audit payloads.")
    parser.add_argument("--review-record", type=Path, required=True, help="Local Phase 2.27a review record JSON.")
    parser.add_argument("--json", action="store_true", help="Print JSON payload.")
    parser.add_argument("--fail-on-unsafe-field", action="store_true", help="Fail if sanitized payload contains unsafe fields.")
    parser.add_argument("--dry-run-preview", action="store_true", default=True, help="Preview only; no audit_logs write.")
    parser.add_argument("--output-file", type=Path, help="Optional local output file for the sanitized preview payload.")
    parser.add_argument("--write-audit", action="store_true", help="Explicitly write sanitized report-level audit_logs event.")
    parser.add_argument("--db-url", help="Optional SQLAlchemy DB URL for audit write smoke tests.")
    args = parser.parse_args(argv)

    try:
        payload = build_audit_preview(load_json(args.review_record))
        if args.write_audit:
            payload = apply_audit_write(payload, db_url=args.db_url)
        unsafe = unsafe_payload_keys(payload, forbidden_keys=FORBIDDEN_WRITE_KEYS)
        if args.fail_on_unsafe_field and unsafe:
            raise ValueError(f"unsafe audit payload fields: {', '.join(sorted(unsafe))}")
        write_optional_payload(payload, args.output_file)
    except Exception as exc:  # noqa: BLE001 - CLI should report unsafe input clearly.
        print(json.dumps({"error": str(exc), "dry_run": True, "would_write_audit_logs": False}, ensure_ascii=False), file=sys.stderr)
        return 1

    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
