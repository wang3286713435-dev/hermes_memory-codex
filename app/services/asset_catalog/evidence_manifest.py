from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

MANIFEST_VERSION = "nas_evidence_manifest.v0"

FORBIDDEN_PREVIEW_KEYS = frozenset(
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

NO_GO_SAFETY_FLAGS = frozenset(SAFETY_FLAGS)


class UnsafeParserPreviewError(ValueError):
    pass


@dataclass(frozen=True)
class SanitizedEvidenceManifestWriteResult:
    path: Path
    manifest: dict[str, Any]


def build_sanitized_evidence_manifest(
    preview: dict[str, Any],
    *,
    created_at: str | None = None,
) -> dict[str, Any]:
    unsafe_keys = sorted(_find_forbidden_keys(preview))
    if unsafe_keys:
        raise UnsafeParserPreviewError(
            "Sanitized evidence manifest input contains forbidden fields: "
            + ", ".join(unsafe_keys)
        )

    source = _mapping(preview.get("source"))
    sample = _mapping(preview.get("sample"))
    parser_preview = _mapping(preview.get("parser_preview"))
    cleanup = _mapping(preview.get("cleanup"))
    safety = _safety(_mapping(preview.get("safety")))
    decision = _decision(source, parser_preview, cleanup, safety)

    return {
        "manifest_version": MANIFEST_VERSION,
        "run_id": _safe_text(preview.get("run_id"), default="redacted-run-id"),
        "created_at": created_at or _utc_now(),
        "source": {
            "asset_ref": _safe_text(source.get("asset_ref"), default="redacted-asset"),
            "source_view": _safe_text(source.get("source_view"), default="FileAssetView"),
            "project_scope_proven": bool(source.get("project_scope_proven")),
            "permission_proof_status": _safe_text(
                source.get("permission_proof_status"),
                default="missing",
            ),
            "storage_locator_present": bool(source.get("storage_locator_present")),
        },
        "sample": {
            "file_type": _safe_text(sample.get("file_type"), default="unknown"),
            "size_bucket": _safe_text(sample.get("size_bucket"), default="unknown"),
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
        "parser_preview": {
            "parser_status": _safe_text(parser_preview.get("parser_status"), default="skipped"),
            "parser_type": _safe_text(
                parser_preview.get("parser_type"),
                default="sanitized-parser-id",
            ),
            "text_length_bucket": _safe_text(
                parser_preview.get("text_length_bucket"),
                default="unknown",
            ),
            "structure_summary": _structure_summary(
                _mapping(parser_preview.get("structure_summary"))
            ),
            "warnings": _safe_string_list(parser_preview.get("warnings")),
        },
        "safety": safety,
        "cleanup": {
            "scratch_cleanup_status": _safe_text(
                cleanup.get("scratch_cleanup_status"),
                default="not_run",
            ),
            "preview_cleanup_status": _safe_text(
                cleanup.get("preview_cleanup_status"),
                default="not_run",
            ),
        },
        "decision": decision,
    }


def write_sanitized_evidence_manifest(
    output_dir: Path,
    manifest: dict[str, Any],
) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / f"{_safe_filename(manifest.get('run_id'))}.json"
    path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return path


def _decision(
    source: dict[str, Any],
    parser_preview: dict[str, Any],
    cleanup: dict[str, Any],
    safety: dict[str, bool],
) -> dict[str, Any]:
    no_go_reasons = [
        f"{flag}_true"
        for flag, value in safety.items()
        if flag in NO_GO_SAFETY_FLAGS and value is True
    ]
    if no_go_reasons:
        return {
            "manifest_status": "no_go",
            "next_allowed_phase": "none",
            "reasons": no_go_reasons,
        }

    pause_reasons: list[str] = []
    if source.get("project_scope_proven") is not True:
        pause_reasons.append("project_scope_not_proven")
    if source.get("permission_proof_status") != "valid":
        pause_reasons.append("permission_proof_not_valid")
    if parser_preview.get("parser_status") != "parsed":
        pause_reasons.append("parser_not_parsed")
    if cleanup.get("scratch_cleanup_status") != "all_deleted":
        pause_reasons.append("scratch_cleanup_not_all_deleted")
    if cleanup.get("preview_cleanup_status") != "all_deleted":
        pause_reasons.append("preview_cleanup_not_all_deleted")
    if pause_reasons:
        return {
            "manifest_status": "pause",
            "next_allowed_phase": "review_only",
            "reasons": pause_reasons,
        }

    return {
        "manifest_status": "ready_for_review",
        "next_allowed_phase": "review_only",
        "reasons": ["sanitized_preview_ready"],
    }


def _find_forbidden_keys(value: Any) -> set[str]:
    found: set[str] = set()
    if isinstance(value, dict):
        for key, child in value.items():
            lowered = str(key).lower()
            if lowered in FORBIDDEN_PREVIEW_KEYS:
                found.add(str(key))
            found.update(_find_forbidden_keys(child))
    elif isinstance(value, list):
        for child in value:
            found.update(_find_forbidden_keys(child))
    return found


def _mapping(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _safety(value: dict[str, Any]) -> dict[str, bool]:
    return {flag: bool(value.get(flag, False)) for flag in SAFETY_FLAGS}


def _structure_summary(value: dict[str, Any]) -> dict[str, str]:
    return {
        "page_count_bucket": _safe_text(value.get("page_count_bucket"), default="unknown"),
        "sheet_count_bucket": _safe_text(value.get("sheet_count_bucket"), default="unknown"),
        "slide_count_bucket": _safe_text(value.get("slide_count_bucket"), default="unknown"),
        "row_count_bucket": _safe_text(value.get("row_count_bucket"), default="unknown"),
    }


def _safe_string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [_safe_text(item, default="sanitized_warning_code") for item in value]


def _safe_text(value: Any, *, default: str) -> str:
    if value is None:
        return default
    text = str(value).strip()
    return text or default


def _safe_filename(value: Any) -> str:
    raw = _safe_text(value, default="redacted-run-id")
    safe = "".join(character if character.isalnum() or character in {"-", "_"} else "-" for character in raw)
    return safe.strip("-") or "redacted-run-id"


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
