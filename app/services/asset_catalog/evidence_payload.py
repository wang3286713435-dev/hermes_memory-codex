from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

PAYLOAD_VERSION = "nas_evidence_write_payload.v0"
SUPPORTED_ELIGIBILITY_REPORT_VERSIONS = frozenset({"nas_evidence_write_eligibility.v0"})
HUMAN_REVIEW_DECISIONS = frozenset(
    {
        "approve_for_payload_dry_run_planning",
        "needs_more_metadata",
        "reject_sensitive_or_unsafe",
        "reject_unsupported_type",
        "reject_permission_unclear",
    }
)
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
FORBIDDEN_REPORT_KEYS = frozenset(
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


def build_evidence_write_payload_plan(
    eligibility_report: dict[str, Any],
    *,
    human_review_decision: str,
    created_at: str | None = None,
) -> dict[str, Any]:
    source = _mapping(eligibility_report.get("source"))
    sample = _mapping(eligibility_report.get("sample"))
    forbidden_keys = sorted(_find_forbidden_keys(eligibility_report))
    safety_reasons = _true_safety_reasons(eligibility_report)
    review_decision = _normalize_review_decision(human_review_decision)

    gates = {
        "eligibility_report_version_supported": eligibility_report.get("report_version")
        in SUPPORTED_ELIGIBILITY_REPORT_VERSIONS,
        "eligibility_ready_for_payload_planning": eligibility_report.get("eligibility_state")
        == "eligible_for_evidence_write_planning",
        "eligibility_writes_authorized_false": eligibility_report.get("writes_authorized")
        is False,
        "eligibility_safety_flags_clear": not safety_reasons,
        "no_forbidden_report_keys": not forbidden_keys,
        "project_scope_proven": source.get("project_scope_proven") is True,
        "permission_proof_valid": source.get("permission_proof_status") == "valid",
        "storage_locator_present": source.get("storage_locator_present") is True,
        "citation_contract_satisfied": _citation_contract_satisfied(source, sample),
        "human_review_approved_for_payload": review_decision
        == "approve_for_payload_dry_run_planning",
    }

    reasons = _reason_codes(gates)
    reasons.extend(safety_reasons)
    reasons.extend(f"forbidden_report_key_{key}" for key in forbidden_keys)

    has_no_go_side_effects = bool(safety_reasons) or bool(forbidden_keys)
    non_human_gates_pass = all(
        value
        for key, value in gates.items()
        if key != "human_review_approved_for_payload"
    )
    if has_no_go_side_effects:
        payload_state = "payload_no_go"
    elif non_human_gates_pass and gates["human_review_approved_for_payload"]:
        payload_state = "payload_ready_for_write_dry_run"
        reasons = ["all_payload_planning_gates_passed"]
    elif non_human_gates_pass:
        payload_state = "payload_ready_for_human_review"
        reasons = ["human_review_not_approved_for_payload_dry_run"]
    else:
        payload_state = "payload_not_allowed"

    candidate_chunks = (
        [_candidate_chunk(eligibility_report, source, sample)]
        if payload_state in {"payload_ready_for_write_dry_run", "payload_ready_for_human_review"}
        else []
    )

    return {
        "payload_version": PAYLOAD_VERSION,
        "run_id": _safe_text(eligibility_report.get("run_id"), default="redacted-run-id"),
        "created_at": created_at or _utc_now(),
        "source": {
            "asset_ref": _safe_text(source.get("asset_ref"), default="redacted-asset"),
            "source_view": _safe_text(source.get("source_view"), default="FileAssetView"),
            "platform_contract_version": _safe_text(
                eligibility_report.get("platform_contract_version"),
                default="delivery_platform.asset_views.v1.1",
            ),
            "eligibility_report_version": _safe_text(
                eligibility_report.get("report_version"),
                default="unknown",
            ),
            "eligibility_report_run_id": _safe_text(
                eligibility_report.get("run_id"),
                default="redacted-run-id",
            ),
            "hash_or_checksum_present": True,
            "cleanup_status": "all_deleted",
        },
        "eligibility": {
            "state": _safe_text(
                eligibility_report.get("eligibility_state"),
                default="not_eligible",
            ),
            "human_review_decision": review_decision,
            "permission_default": "DENIED",
        },
        "candidate_document": _candidate_document(source, sample),
        "candidate_chunks": candidate_chunks,
        "citation_contract": {
            "cite_db_asset_ref": True,
            "cite_scratch_path": False,
            "cite_temp_filename": False,
            "source_view_required": True,
            "platform_contract_version_required": True,
            "parser_type_required": True,
            "checksum_or_hash_presence_required": True,
            "permission_proof_status_required": True,
        },
        "safety": _safety(),
        "dry_run": True,
        "writes_authorized": False,
        "decision": {
            "payload_state": payload_state,
            "reasons": reasons,
        },
    }


def write_evidence_write_payload_plan(output_dir: Path, payload: dict[str, Any]) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / f"{_safe_filename(payload.get('run_id'))}-payload.json"
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return path


def _candidate_document(source: dict[str, Any], sample: dict[str, Any]) -> dict[str, Any]:
    return {
        "external_source_type": "platform_asset_catalog",
        "external_asset_ref": _safe_text(source.get("asset_ref"), default="redacted-asset"),
        "sanitized_title": "redacted_asset_document",
        "source_view": _safe_text(source.get("source_view"), default="FileAssetView"),
        "file_type": _safe_text(sample.get("file_type"), default="unknown").lower(),
        "parser_type": "sanitized_parser_preview",
        "permission_proof_status": _safe_text(
            source.get("permission_proof_status"),
            default="missing",
        ),
        "confidentiality_status": _safe_text(
            sample.get("confidentiality_status"),
            default="unknown",
        ),
        "lifecycle_status": _safe_text(sample.get("lifecycle_status"), default="unknown"),
        "index_eligibility_status": _safe_text(
            sample.get("index_eligibility_status"),
            default="unknown",
        ),
        "document_write_mode": "dry_run_only",
        "raw_text_present": False,
        "true_source_path_present": False,
    }


def _candidate_chunk(
    eligibility_report: dict[str, Any],
    source: dict[str, Any],
    sample: dict[str, Any],
) -> dict[str, Any]:
    run_id = _safe_text(eligibility_report.get("run_id"), default="redacted-run-id")
    return {
        "dry_run_chunk_ref": f"{_safe_filename(run_id)}-chunk-0001",
        "chunk_write_mode": "dry_run_only",
        "chunk_order": 1,
        "text_length_bucket": "derived_from_manifest",
        "structure_bucket": "sanitized_structure_summary",
        "parser_section_label": "sanitized_section",
        "redacted_citation_anchor": (
            f"{_safe_text(source.get('source_view'), default='FileAssetView')}:"
            f"{_safe_text(source.get('asset_ref'), default='redacted-asset')}:chunk-0001"
        ),
        "file_type": _safe_text(sample.get("file_type"), default="unknown").lower(),
        "raw_text_present": False,
        "scratch_path_present": False,
        "true_filename_present": False,
    }


def _citation_contract_satisfied(source: dict[str, Any], sample: dict[str, Any]) -> bool:
    return (
        bool(_safe_text(source.get("asset_ref"), default=""))
        and bool(_safe_text(source.get("source_view"), default=""))
        and bool(_safe_text(sample.get("file_type"), default=""))
    )


def _safety() -> dict[str, bool]:
    return {
        "raw_text_output": False,
        "true_filename_output": False,
        "true_nas_path_output": False,
        "raw_row_output": False,
        "secret_printed": False,
        "true_business_data_output": False,
        "documents_written": False,
        "chunks_written": False,
        "db_writes": False,
        "opensearch_writes": False,
        "qdrant_writes": False,
        "minio_writes": False,
        "agent_answer_integration": False,
        "production_rollout": False,
    }


def _reason_codes(gates: dict[str, bool]) -> list[str]:
    names = {
        "eligibility_report_version_supported": "eligibility_report_version_not_supported",
        "eligibility_ready_for_payload_planning": "eligibility_not_ready_for_payload_planning",
        "eligibility_writes_authorized_false": "eligibility_writes_authorized_not_false",
        "eligibility_safety_flags_clear": "eligibility_safety_flags_not_clear",
        "no_forbidden_report_keys": "forbidden_report_keys_present",
        "project_scope_proven": "project_scope_not_proven",
        "permission_proof_valid": "permission_proof_not_valid",
        "storage_locator_present": "storage_locator_not_present",
        "citation_contract_satisfied": "citation_contract_not_satisfied",
        "human_review_approved_for_payload": "human_review_not_approved_for_payload_dry_run",
    }
    return [names[key] for key, value in gates.items() if not value]


def _true_safety_reasons(value: dict[str, Any]) -> list[str]:
    return [f"{flag}_true" for flag in SAFETY_FLAGS if value.get(flag) is True]


def _find_forbidden_keys(value: Any) -> set[str]:
    found: set[str] = set()
    if isinstance(value, dict):
        for key, child in value.items():
            lowered = str(key).lower()
            if lowered in FORBIDDEN_REPORT_KEYS:
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
