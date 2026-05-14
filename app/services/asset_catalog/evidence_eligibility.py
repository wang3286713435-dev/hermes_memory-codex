from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ELIGIBILITY_REPORT_VERSION = "nas_evidence_write_eligibility.v0"
SUPPORTED_MANIFEST_VERSIONS = frozenset({"nas_evidence_manifest.v0"})
SUPPORTED_FILE_TYPES = frozenset(
    {
        "csv",
        "doc",
        "docx",
        "html",
        "md",
        "pdf",
        "ppt",
        "pptx",
        "text",
        "txt",
        "xls",
        "xlsx",
    }
)
HUMAN_REVIEW_DECISIONS = frozenset(
    {
        "approve_for_evidence_write_planning",
        "needs_more_metadata",
        "reject_sensitive_or_unsafe",
        "reject_unsupported_type",
        "reject_permission_unclear",
    }
)
SAFETY_FLAGS = (
    "raw_text_output",
    "true_filename_output",
    "true_nas_path_output",
    "raw_row_output",
    "secret_printed",
    "true_business_data_output",
    "documents_written",
    "chunks_written",
    "db_writes",
    "opensearch_writes",
    "qdrant_writes",
    "minio_writes",
    "agent_answer_integration",
)
FORBIDDEN_MANIFEST_KEYS = frozenset(
    {
        "raw_text",
        "text",
        "content",
        "file_name",
        "filename",
        "true_filename",
        "nas_path",
        "true_nas_path",
        "source_path",
        "storage_path",
        "scratch_path",
        "raw_row",
        "secret",
        "token",
        "password",
        "api_key",
    }
)


def build_evidence_write_eligibility_report(
    manifest: dict[str, Any],
    *,
    human_review_decision: str,
    created_at: str | None = None,
) -> dict[str, Any]:
    source = _mapping(manifest.get("source"))
    sample = _mapping(manifest.get("sample"))
    parser_preview = _mapping(manifest.get("parser_preview"))
    cleanup = _mapping(manifest.get("cleanup"))
    safety = _mapping(manifest.get("safety"))
    decision = _mapping(manifest.get("decision"))
    forbidden_keys = sorted(_find_forbidden_keys(manifest))
    normalized_review_decision = _normalize_review_decision(human_review_decision)

    gates = {
        "manifest_version_supported": manifest.get("manifest_version")
        in SUPPORTED_MANIFEST_VERSIONS,
        "manifest_ready_for_review": decision.get("manifest_status") == "ready_for_review",
        "project_scope_proven": source.get("project_scope_proven") is True,
        "permission_proof_valid": source.get("permission_proof_status") == "valid",
        "storage_locator_present": source.get("storage_locator_present") is True,
        "parser_parsed": parser_preview.get("parser_status") == "parsed",
        "text_length_present": _safe_text(parser_preview.get("text_length_bucket"), default="unknown")
        not in {"empty", "unknown"},
        "cleanup_all_deleted": cleanup.get("scratch_cleanup_status") == "all_deleted"
        and cleanup.get("preview_cleanup_status") == "all_deleted",
        "safety_flags_clear": not _true_safety_reasons(safety),
        "no_forbidden_manifest_keys": not forbidden_keys,
        "index_eligibility_preview": sample.get("index_eligibility_status")
        == "eligible_for_preview",
        "confidentiality_known": sample.get("confidentiality_status") == "known",
        "lifecycle_active": sample.get("lifecycle_status") == "active",
        "file_type_supported": _safe_text(sample.get("file_type"), default="unknown").lower()
        in SUPPORTED_FILE_TYPES,
        "human_review_approved_for_planning": normalized_review_decision
        == "approve_for_evidence_write_planning",
    }

    reasons = _reason_codes(gates)
    reasons.extend(_true_safety_reasons(safety))
    reasons.extend(f"forbidden_manifest_key_{key}" for key in forbidden_keys)
    if decision.get("manifest_status") == "no_go":
        reasons.insert(0, "manifest_no_go")

    non_human_gates_pass = all(
        value
        for key, value in gates.items()
        if key != "human_review_approved_for_planning"
    )
    has_no_go_side_effects = (
        decision.get("manifest_status") == "no_go"
        or bool(_true_safety_reasons(safety))
        or bool(forbidden_keys)
    )
    if has_no_go_side_effects:
        eligibility_state = "no_go"
    elif non_human_gates_pass and gates["human_review_approved_for_planning"]:
        eligibility_state = "eligible_for_evidence_write_planning"
        reasons = ["all_planning_gates_passed"]
    elif non_human_gates_pass:
        eligibility_state = "eligible_for_human_review"
        reasons = ["human_review_not_approved_for_planning"]
    else:
        eligibility_state = "not_eligible"

    return {
        "report_version": ELIGIBILITY_REPORT_VERSION,
        "run_id": _safe_text(manifest.get("run_id"), default="redacted-run-id"),
        "created_at": created_at or _utc_now(),
        "source": {
            "asset_ref": _safe_text(source.get("asset_ref"), default="redacted-asset"),
            "source_view": _safe_text(source.get("source_view"), default="FileAssetView"),
            "project_scope_proven": gates["project_scope_proven"],
            "permission_proof_status": _safe_text(
                source.get("permission_proof_status"),
                default="missing",
            ),
            "storage_locator_present": gates["storage_locator_present"],
        },
        "sample": {
            "file_type": _safe_text(sample.get("file_type"), default="unknown").lower(),
            "confidentiality_status": _safe_text(
                sample.get("confidentiality_status"),
                default="unknown",
            ),
            "lifecycle_status": _safe_text(sample.get("lifecycle_status"), default="unknown"),
            "index_eligibility_status": _safe_text(
                sample.get("index_eligibility_status"),
                default="unknown",
            ),
        },
        "human_review_decision": normalized_review_decision,
        "eligibility_state": eligibility_state,
        "permission_default": "DENIED",
        "gates": gates,
        "reasons": reasons,
        "writes_authorized": False,
        "parser_invoked": False,
        "scratch_copy_performed": False,
        "documents_written": False,
        "chunks_written": False,
        "db_writes": False,
        "opensearch_writes": False,
        "qdrant_writes": False,
        "minio_writes": False,
        "agent_answer_integration": False,
        "production_rollout": False,
    }


def write_evidence_write_eligibility_report(
    output_dir: Path,
    report: dict[str, Any],
) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / f"{_safe_filename(report.get('run_id'))}-eligibility.json"
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return path


def _reason_codes(gates: dict[str, bool]) -> list[str]:
    names = {
        "manifest_version_supported": "manifest_version_not_supported",
        "manifest_ready_for_review": "manifest_not_ready_for_review",
        "project_scope_proven": "project_scope_not_proven",
        "permission_proof_valid": "permission_proof_not_valid",
        "storage_locator_present": "storage_locator_not_present",
        "parser_parsed": "parser_not_parsed",
        "text_length_present": "text_length_missing_or_empty",
        "cleanup_all_deleted": "cleanup_not_all_deleted",
        "safety_flags_clear": "safety_flags_not_clear",
        "no_forbidden_manifest_keys": "forbidden_manifest_keys_present",
        "index_eligibility_preview": "index_eligibility_not_preview",
        "confidentiality_known": "confidentiality_not_known",
        "lifecycle_active": "lifecycle_not_active",
        "file_type_supported": "file_type_not_supported",
        "human_review_approved_for_planning": "human_review_not_approved_for_planning",
    }
    return [names[key] for key, value in gates.items() if not value]


def _true_safety_reasons(safety: dict[str, Any]) -> list[str]:
    return [f"{flag}_true" for flag in SAFETY_FLAGS if safety.get(flag) is True]


def _find_forbidden_keys(value: Any) -> set[str]:
    found: set[str] = set()
    if isinstance(value, dict):
        for key, child in value.items():
            lowered = str(key).lower()
            if lowered in FORBIDDEN_MANIFEST_KEYS:
                found.add(str(key))
            found.update(_find_forbidden_keys(child))
    elif isinstance(value, list):
        for child in value:
            found.update(_find_forbidden_keys(child))
    return found


def _normalize_review_decision(value: str) -> str:
    normalized = _safe_text(value, default="needs_more_metadata")
    if normalized not in HUMAN_REVIEW_DECISIONS:
        return "needs_more_metadata"
    return normalized


def _mapping(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _safe_text(value: Any, *, default: str) -> str:
    if value is None:
        return default
    text = str(value).strip()
    return text or default


def _safe_filename(value: Any) -> str:
    raw = _safe_text(value, default="redacted-run-id")
    safe = "".join(
        character if character.isalnum() or character in {"-", "_"} else "-"
        for character in raw
    )
    return safe.strip("-") or "redacted-run-id"


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
