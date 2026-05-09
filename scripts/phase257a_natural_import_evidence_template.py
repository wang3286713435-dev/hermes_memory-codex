from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Sequence

DANGEROUS_AUTHORIZATION_FIELDS = (
    "cleanup_authorized",
    "repair_authorized",
    "backfill_authorized",
    "reindex_authorized",
    "rollout_authorized",
)


def build_evidence_template(
    *,
    source_path: Path,
    alias: str,
    session_id: str,
    operator: str,
) -> dict[str, Any]:
    """Build a metadata-only natural import evidence template."""

    source_path = source_path.expanduser()
    is_file = source_path.is_file()
    missing = []
    if not is_file:
        missing.append("source_path_exists")
    if not alias.strip():
        missing.append("alias")
    if not session_id.strip():
        missing.append("session_id")
    if not operator.strip():
        missing.append("operator")

    status = "Pause" if missing else "ReadyForAuthorizedSmoke"
    return {
        "phase": "Phase 2.57a",
        "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "dry_run": True,
        "real_upload_called": False,
        "real_file_uploaded": False,
        "plain_upload_bypass_used": False,
        "cleanup_authorized": False,
        "repair_authorized": False,
        "backfill_authorized": False,
        "reindex_authorized": False,
        "rollout_authorized": False,
        "source_path": str(source_path),
        "source_path_exists": is_file,
        "source_file_name": source_path.name,
        "source_file_size_bytes": source_path.stat().st_size if is_file else None,
        "source_file_type": source_path.suffix.lower() or None,
        "alias": alias.strip(),
        "session_id": session_id.strip(),
        "operator": operator.strip(),
        "go_pause_no_go": status,
        "missing_required_fields": missing,
        "required_next_steps": [
            "Obtain explicit user authorization before any real upload.",
            "Run the real smoke through the Hermes CLI natural-language import path.",
            "Do not use direct API upload as a substitute for natural import evidence.",
            "After upload, record document_id, version_id, chunk_count, indexed_count, alias persistence, citation, and contamination flags.",
        ],
    }


def build_review_summary(payload: dict[str, Any]) -> dict[str, Any]:
    """Review a dry-run evidence template without authorizing or executing upload."""

    blocking_reasons: list[str] = []
    warning_reasons: list[str] = []

    if payload.get("dry_run") is not True:
        blocking_reasons.append("dry_run_not_true")
    if payload.get("real_upload_called") is True:
        blocking_reasons.append("real_upload_called")
    if payload.get("plain_upload_bypass_used") is True:
        blocking_reasons.append("plain_upload_bypass_used")
    if payload.get("real_file_uploaded") is True:
        blocking_reasons.append("real_file_uploaded")
    if payload.get("source_path_exists") is not True:
        blocking_reasons.append("source_path_missing")
    if not str(payload.get("alias") or "").strip():
        blocking_reasons.append("alias_missing")
    if not str(payload.get("session_id") or "").strip():
        blocking_reasons.append("session_id_missing")
    if not str(payload.get("operator") or "").strip():
        blocking_reasons.append("operator_missing")
    if payload.get("go_pause_no_go") != "ReadyForAuthorizedSmoke":
        warning_reasons.append("not_ready_for_authorized_smoke")

    dangerous_reasons = [field for field in DANGEROUS_AUTHORIZATION_FIELDS if payload.get(field) is True]
    blocking_reasons.extend(dangerous_reasons)

    if dangerous_reasons:
        review_status = "no_go"
    elif blocking_reasons:
        review_status = "pause"
    elif warning_reasons:
        review_status = "pause"
    else:
        review_status = "ready_for_operator_authorization"

    return {
        "phase": "Phase 2.58",
        "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "dry_run": True,
        "review_only": True,
        "real_upload_called": bool(payload.get("real_upload_called") is True),
        "real_file_uploaded": bool(payload.get("real_file_uploaded") is True),
        "plain_upload_bypass_used": bool(payload.get("plain_upload_bypass_used") is True),
        "review_status": review_status,
        "go_pause_no_go": payload.get("go_pause_no_go"),
        "blocking_reasons": blocking_reasons,
        "warning_reasons": warning_reasons,
        "safe_to_request_real_smoke_authorization": review_status == "ready_for_operator_authorization",
        "required_next_steps": [
            "Use this review only to decide whether to request explicit user authorization for a future real smoke.",
            "Do not treat this review as upload success or production readiness.",
            "If authorized later, run the real smoke through the Hermes CLI natural-language import path.",
        ],
    }


def write_evidence_template(payload: dict[str, Any], *, output: Path, reports_root: Path) -> None:
    output = output.expanduser()
    reports_root = reports_root.expanduser().resolve()
    allowed_dir = (reports_root / "internal_mvp_runs").resolve()
    resolved_output = output.resolve()
    if allowed_dir not in [resolved_output.parent, *resolved_output.parents]:
        raise ValueError("Output must be under reports/internal_mvp_runs/")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build a dry-run natural import evidence template.")
    parser.add_argument("--source-path")
    parser.add_argument("--alias")
    parser.add_argument("--session-id")
    parser.add_argument("--operator")
    parser.add_argument("--review-json")
    parser.add_argument("--output")
    parser.add_argument("--reports-root", default="reports")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    if args.review_json:
        review_payload = json.loads(Path(args.review_json).read_text(encoding="utf-8"))
        payload = build_review_summary(review_payload)
    else:
        missing_args = [
            name
            for name in ("source_path", "alias", "session_id", "operator")
            if getattr(args, name) is None
        ]
        if missing_args:
            raise SystemExit(f"Missing required arguments for template mode: {', '.join(missing_args)}")
        payload = build_evidence_template(
            source_path=Path(args.source_path),
            alias=args.alias,
            session_id=args.session_id,
            operator=args.operator,
        )
    if args.output:
        write_evidence_template(payload, output=Path(args.output), reports_root=Path(args.reports_root))
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
