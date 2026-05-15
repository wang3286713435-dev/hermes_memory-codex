from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

PREFLIGHT_VERSION = "nas_evidence_write_preflight.v0"
SUPPORTED_PAYLOAD_VERSIONS = frozenset({"nas_evidence_write_payload.v0"})
MAX_DOCUMENT_COUNT = 1
MAX_CHUNK_COUNT = 20
SAFETY_FLAGS = (
    "writes_authorized",
    "parser_invoked",
    "scratch_copy_performed",
    "documents_written",
    "chunks_written",
    "db_writes",
    "opensearch_writes",
    "qdrant_writes",
    "minio_writes",
    "agent_answer_integration",
    "production_rollout",
)
FORBIDDEN_PAYLOAD_KEYS = frozenset(
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


def build_evidence_write_preflight_report(
    payload: dict[str, Any],
    *,
    operator_approval: dict[str, Any],
    created_at: str | None = None,
) -> dict[str, Any]:
    created = created_at or _utc_now()
    source = _mapping(payload.get("source"))
    candidate_document = _mapping(payload.get("candidate_document"))
    candidate_chunks = _list_of_mappings(payload.get("candidate_chunks"))
    decision = _mapping(payload.get("decision"))

    forbidden_keys = sorted(_find_forbidden_keys(payload))
    safety_reasons = _true_safety_reasons(payload)
    citation_missing = _citation_coverage_missing(source, candidate_document, candidate_chunks)
    operator_approval_result = _operator_approval_result(
        payload,
        operator_approval,
        document_count=1 if candidate_document else 0,
        chunk_count=len(candidate_chunks),
        created_at=created,
    )
    idempotency_key = _idempotency_key(payload, source)
    rollback_available = bool(candidate_document) and bool(candidate_chunks)

    gates = {
        "payload_version_supported": payload.get("payload_version")
        in SUPPORTED_PAYLOAD_VERSIONS,
        "payload_ready_for_write_preflight": decision.get("payload_state")
        == "payload_ready_for_write_dry_run",
        "payload_dry_run_true": payload.get("dry_run") is True,
        "payload_writes_authorized_false": payload.get("writes_authorized") is False,
        "payload_safety_flags_clear": not safety_reasons,
        "no_forbidden_payload_keys": not forbidden_keys,
        "candidate_document_present": bool(candidate_document),
        "candidate_chunk_count_positive": len(candidate_chunks) > 0,
        "candidate_chunk_count_within_default_cap": len(candidate_chunks) <= MAX_CHUNK_COUNT,
        "citation_coverage_complete": not citation_missing,
        "idempotency_key_derivable": bool(idempotency_key),
        "rollback_plan_describable": rollback_available,
        "lock_strategy_explicit": True,
    }
    reasons = _reason_codes(gates)
    reasons.extend(safety_reasons)
    reasons.extend(f"forbidden_payload_key_{key}" for key in forbidden_keys)
    reasons.extend(operator_approval_result["reasons"])
    reasons.extend(f"citation_coverage_{reason}" for reason in citation_missing)

    has_no_go_side_effects = bool(safety_reasons) or bool(forbidden_keys)
    non_operator_gates_pass = all(gates.values())
    operator_approval_passed = operator_approval_result["approved_for_payload"] is True

    if has_no_go_side_effects:
        preflight_state = "write_preflight_no_go"
    elif non_operator_gates_pass and operator_approval_passed:
        preflight_state = "write_preflight_ready_for_dry_run"
        reasons = ["all_preflight_gates_passed"]
    elif non_operator_gates_pass:
        preflight_state = "write_preflight_not_allowed"
    else:
        preflight_state = "write_preflight_not_allowed"

    return {
        "preflight_version": PREFLIGHT_VERSION,
        "run_id": _safe_text(payload.get("run_id"), default="redacted-run-id"),
        "created_at": created,
        "payload_ref": {
            "payload_version": _safe_text(payload.get("payload_version"), default="unknown"),
            "payload_run_id": _safe_text(payload.get("run_id"), default="redacted-run-id"),
            "source_view": _safe_text(source.get("source_view"), default="FileAssetView"),
            "asset_ref": _safe_text(source.get("asset_ref"), default="redacted-asset"),
            "platform_contract_version": _safe_text(
                source.get("platform_contract_version"),
                default="delivery_platform.asset_views.v1.1",
            ),
        },
        "operator_approval": operator_approval_result["summary"],
        "write_scope": {
            "document_count": 1 if candidate_document else 0,
            "chunk_count": len(candidate_chunks),
            "approved_max_document_count": operator_approval_result["max_document_count"],
            "approved_max_chunk_count": operator_approval_result["max_chunk_count"],
            "approved_max_total_text_bucket": operator_approval_result[
                "max_total_text_bucket"
            ],
            "default_max_document_count": MAX_DOCUMENT_COUNT,
            "default_max_chunk_count": MAX_CHUNK_COUNT,
            "small_batch_only": True,
            "broad_scope": False,
            "cross_project_batch": False,
            "automatic_expansion": False,
        },
        "idempotency": {
            "idempotency_key": idempotency_key,
            "derivable": bool(idempotency_key),
            "duplicate_check_required": True,
            "duplicate_write_allowed": False,
            "external_asset_ref": _safe_text(source.get("asset_ref"), default="redacted-asset"),
            "dry_run_document_ref": _dry_run_document_ref(payload),
            "dry_run_chunk_refs": [
                _safe_text(chunk.get("dry_run_chunk_ref"), default=f"chunk-{index + 1:04d}")
                for index, chunk in enumerate(candidate_chunks)
            ],
        },
        "rollback": {
            "rollback_plan_available": rollback_available,
            "rollback_scope": "same_run_only",
            "source_data_mutation": False,
            "delete_original_nas_file": False,
            "delete_platform_db_record": False,
            "repair_backfill_reindex_cleanup": False,
            "auditable": True,
        },
        "citation_coverage": {
            "complete": not citation_missing,
            "chunk_count": len(candidate_chunks),
            "missing": citation_missing,
            "source_asset_ref_required": True,
            "source_view_required": True,
            "platform_contract_version_required": True,
            "parser_type_required": True,
            "redacted_citation_anchor_required": True,
            "scratch_path_allowed": False,
            "true_filename_allowed": False,
        },
        "locks": {
            "lock_required": True,
            "lock_created": False,
            "lock_strategy": "future_write_lock_required",
            "payload_run_id_lock_required": True,
            "project_scope_lock_required": True,
            "ambiguous_lock_state_denied": True,
            "expired_lock_denied": True,
        },
        "safety": _safety(),
        "dry_run": True,
        "writes_authorized": False,
        "decision": {
            "preflight_state": preflight_state,
            "reasons": reasons,
        },
    }


def write_evidence_write_preflight_report(
    output_dir: Path,
    preflight: dict[str, Any],
) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / f"{_safe_filename(preflight.get('run_id'))}-preflight.json"
    path.write_text(
        json.dumps(preflight, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return path


def _operator_approval_result(
    payload: dict[str, Any],
    operator_approval: dict[str, Any],
    *,
    document_count: int,
    chunk_count: int,
    created_at: str,
) -> dict[str, Any]:
    approval = _mapping(operator_approval)
    approval_run_id = _safe_text(approval.get("payload_run_id"), default="")
    payload_run_id = _safe_text(payload.get("run_id"), default="")
    max_document_count = _safe_int(approval.get("max_document_count"), default=0)
    max_chunk_count = _safe_int(approval.get("max_chunk_count"), default=0)
    max_total_text_bucket = _safe_text(approval.get("max_total_text_bucket"), default="")
    approved_project_scope = _safe_text(approval.get("approved_project_scope"), default="")
    approved_at = _safe_text(approval.get("approved_at"), default="")
    expires_at = _safe_text(approval.get("expires_at"), default="")
    reason = _safe_text(approval.get("reason"), default="")

    expiry_valid = _expires_after(expires_at, created_at)
    checks = {
        "operator_approval_explicit": approval.get("approved") is True,
        "operator_approval_payload_run_id_matches": approval_run_id == payload_run_id,
        "operator_approval_approved_at_present": bool(approved_at),
        "operator_approval_expires_at_valid": expiry_valid,
        "operator_approval_project_scope_present": bool(approved_project_scope),
        "operator_approval_reason_present": bool(reason),
        "document_count_within_approval": document_count <= max_document_count,
        "chunk_count_within_approval": chunk_count <= max_chunk_count,
        "approved_document_cap_tiny": 1 <= max_document_count <= MAX_DOCUMENT_COUNT,
        "approved_chunk_cap_tiny": 1 <= max_chunk_count <= MAX_CHUNK_COUNT,
        "approved_total_text_bucket_present": bool(max_total_text_bucket),
    }
    reason_names = {
        "operator_approval_explicit": "operator_approval_not_explicit",
        "operator_approval_payload_run_id_matches": "operator_approval_payload_run_id_mismatch",
        "operator_approval_approved_at_present": "operator_approval_approved_at_missing",
        "operator_approval_expires_at_valid": "operator_approval_expired_or_invalid",
        "operator_approval_project_scope_present": "operator_approval_project_scope_missing",
        "operator_approval_reason_present": "operator_approval_reason_missing",
        "document_count_within_approval": "document_count_exceeds_approval",
        "chunk_count_within_approval": "chunk_count_exceeds_approval",
        "approved_document_cap_tiny": "approved_document_cap_too_broad",
        "approved_chunk_cap_tiny": "approved_chunk_cap_too_broad",
        "approved_total_text_bucket_present": "approved_total_text_bucket_missing",
    }
    return {
        "approved_for_payload": all(checks.values()),
        "reasons": [reason_names[key] for key, value in checks.items() if not value],
        "max_document_count": max_document_count,
        "max_chunk_count": max_chunk_count,
        "max_total_text_bucket": max_total_text_bucket or "missing",
        "summary": {
            "approved": approval.get("approved") is True,
            "payload_run_id_matches": approval_run_id == payload_run_id,
            "approved_at_present": bool(approved_at),
            "expires_at_valid": expiry_valid,
            "approved_project_scope_present": bool(approved_project_scope),
            "max_document_count": max_document_count,
            "max_chunk_count": max_chunk_count,
            "max_total_text_bucket": max_total_text_bucket or "missing",
            "reason_present": bool(reason),
            "permission_default": "DENIED",
        },
    }


def _citation_coverage_missing(
    source: dict[str, Any],
    candidate_document: dict[str, Any],
    candidate_chunks: list[dict[str, Any]],
) -> list[str]:
    missing: list[str] = []
    if not _safe_text(source.get("asset_ref"), default=""):
        missing.append("source_asset_ref_missing")
    if not _safe_text(source.get("source_view"), default=""):
        missing.append("source_view_missing")
    if not _safe_text(source.get("platform_contract_version"), default=""):
        missing.append("platform_contract_version_missing")
    if not _safe_text(candidate_document.get("parser_type"), default=""):
        missing.append("parser_type_missing")
    if not _safe_text(candidate_document.get("permission_proof_status"), default=""):
        missing.append("permission_proof_status_missing")
    for index, chunk in enumerate(candidate_chunks):
        prefix = f"chunk_{index + 1}"
        if not _safe_text(chunk.get("redacted_citation_anchor"), default=""):
            missing.append(f"{prefix}_redacted_citation_anchor_missing")
        if chunk.get("chunk_order") is None:
            missing.append(f"{prefix}_chunk_order_missing")
        if chunk.get("raw_text_present") is not False:
            missing.append(f"{prefix}_raw_text_present_not_false")
        if chunk.get("scratch_path_present") is not False:
            missing.append(f"{prefix}_scratch_path_present_not_false")
        if chunk.get("true_filename_present") is not False:
            missing.append(f"{prefix}_true_filename_present_not_false")
    return missing


def _reason_codes(gates: dict[str, bool]) -> list[str]:
    names = {
        "payload_version_supported": "payload_version_not_supported",
        "payload_ready_for_write_preflight": "payload_not_ready_for_write_preflight",
        "payload_dry_run_true": "payload_dry_run_not_true",
        "payload_writes_authorized_false": "payload_writes_authorized_not_false",
        "payload_safety_flags_clear": "payload_safety_flags_not_clear",
        "no_forbidden_payload_keys": "forbidden_payload_keys_present",
        "candidate_document_present": "candidate_document_missing",
        "candidate_chunk_count_positive": "candidate_chunks_missing",
        "candidate_chunk_count_within_default_cap": "candidate_chunk_count_exceeds_default_cap",
        "citation_coverage_complete": "citation_coverage_incomplete",
        "idempotency_key_derivable": "idempotency_key_not_derivable",
        "rollback_plan_describable": "rollback_plan_not_describable",
        "lock_strategy_explicit": "lock_strategy_not_explicit",
    }
    return [names[key] for key, value in gates.items() if not value]


def _true_safety_reasons(payload: dict[str, Any]) -> list[str]:
    safety = _mapping(payload.get("safety"))
    reasons: list[str] = []
    for flag in SAFETY_FLAGS:
        if payload.get(flag) is True or safety.get(flag) is True:
            reasons.append(f"{flag}_true")
    return reasons


def _find_forbidden_keys(value: Any) -> set[str]:
    found: set[str] = set()
    if isinstance(value, dict):
        for key, child in value.items():
            lowered = str(key).lower()
            if lowered in FORBIDDEN_PAYLOAD_KEYS:
                found.add(str(key))
            found.update(_find_forbidden_keys(child))
    elif isinstance(value, list):
        for child in value:
            found.update(_find_forbidden_keys(child))
    return found


def _safety() -> dict[str, bool]:
    return {
        "raw_text_output": False,
        "true_filename_output": False,
        "true_nas_path_output": False,
        "raw_row_output": False,
        "secret_printed": False,
        "true_business_data_output": False,
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


def _idempotency_key(payload: dict[str, Any], source: dict[str, Any]) -> str:
    run_id = _safe_text(payload.get("run_id"), default="")
    asset_ref = _safe_text(source.get("asset_ref"), default="")
    if not run_id or not asset_ref:
        return ""
    digest = hashlib.sha256(asset_ref.encode("utf-8")).hexdigest()[:12]
    return f"preflight-{_safe_filename(run_id)}-{digest}"


def _dry_run_document_ref(payload: dict[str, Any]) -> str:
    run_id = _safe_text(payload.get("run_id"), default="redacted-run-id")
    return f"{_safe_filename(run_id)}-document-0001"


def _expires_after(expires_at: str, created_at: str) -> bool:
    expires = _parse_datetime(expires_at)
    created = _parse_datetime(created_at)
    if expires is None or created is None:
        return False
    return expires > created


def _parse_datetime(value: str) -> datetime | None:
    text = _safe_text(value, default="")
    if not text:
        return None
    if text.endswith("Z"):
        text = f"{text[:-1]}+00:00"
    try:
        parsed = datetime.fromisoformat(text)
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def _mapping(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _list_of_mappings(value: Any) -> list[dict[str, Any]]:
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, dict)]


def _safe_int(value: Any, *, default: int) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


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
