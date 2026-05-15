from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

RUNTIME_PREFLIGHT_VERSION = "runtime_evidence_write_preflight.v0"
APPROVAL_VERSION = "hermes_evidence_write_operator_approval.v1"
ALLOWED_ACTION = "first_real_hermes_evidence_write_smoke"
TEST_MACHINE_ENVIRONMENT = "test_machine_only"
MAX_DOCUMENTS = 1
MAX_DOCUMENT_VERSIONS = 1
MAX_CHUNKS = 20

REQUIRED_APPROVAL_FIELDS = (
    "approval_version",
    "approval_id",
    "approved_by",
    "approved_at",
    "expires_at",
    "target_environment",
    "target_git_commit",
    "source_system",
    "source_asset_ref",
    "project_scope",
    "permission_proof_ref",
    "sanitized_manifest_ref",
    "eligibility_report_ref",
    "payload_plan_ref",
    "preflight_report_ref",
    "dry_run_ref",
    "rehearsal_ref",
    "rollback_dry_run_ref",
    "write_run_id",
    "evidence_write_idempotency_key",
    "expected_payload_fingerprint",
    "max_documents",
    "max_document_versions",
    "max_chunks",
    "allowed_write_action",
    "feature_flags_expected",
    "writes_authorized",
)

REPORT_REF_FIELDS = (
    "permission_proof_ref",
    "sanitized_manifest_ref",
    "eligibility_report_ref",
    "payload_plan_ref",
    "preflight_report_ref",
    "dry_run_ref",
    "rehearsal_ref",
    "rollback_dry_run_ref",
)

ALLOWED_TRUE_FEATURE_FLAGS = frozenset(
    {
        "PLATFORM_ASSET_REAL_EVIDENCE_WRITE_ENABLED",
        "PLATFORM_ASSET_REAL_EVIDENCE_WRITE_SMOKE_ENABLED",
    }
)

REQUIRED_FALSE_FEATURE_FLAGS = frozenset(
    {
        "PLATFORM_ASSET_AGENT_ANSWER_INTEGRATION_ENABLED",
        "PLATFORM_ASSET_INDEX_WRITE_ENABLED",
        "PLATFORM_ASSET_API_CLI_RUNTIME_ENABLED",
    }
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

FORBIDDEN_STRING_MARKERS = (
    "/Users/",
    "\\Users\\",
    "真实正文",
    "BEGIN PRIVATE KEY",
    "api_key=",
    "password=",
    "token=",
)


def build_runtime_evidence_write_preflight_report(
    approval: dict[str, Any],
    *,
    expected_git_commit: str,
    worktree_status_text: str = "",
    created_at: str | None = None,
) -> dict[str, Any]:
    created = created_at or _utc_now()
    approval_map = _mapping(approval)

    pause_reasons: list[str] = []
    no_go_reasons: list[str] = []

    for field in REQUIRED_APPROVAL_FIELDS:
        if field not in approval_map or approval_map.get(field) in (None, ""):
            if field in {"write_run_id", "evidence_write_idempotency_key"}:
                no_go_reasons.append(
                    "write_run_id_missing"
                    if field == "write_run_id"
                    else "idempotency_key_missing"
                )
            else:
                pause_reasons.append(f"missing_approval_field_{field}")

    if _safe_text(approval_map.get("approval_version")) != APPROVAL_VERSION:
        pause_reasons.append("approval_version_mismatch")
    if _safe_text(approval_map.get("target_git_commit")) != expected_git_commit:
        pause_reasons.append("target_git_commit_mismatch")
    if _safe_text(approval_map.get("target_environment")) != TEST_MACHINE_ENVIRONMENT:
        no_go_reasons.append("target_environment_not_test_machine_only")
    if _safe_text(approval_map.get("allowed_write_action")) != ALLOWED_ACTION:
        no_go_reasons.append("allowed_write_action_invalid")
    if approval_map.get("writes_authorized") is not True:
        pause_reasons.append("writes_authorized_not_true")
    if not _expires_after(_safe_text(approval_map.get("expires_at")), created):
        pause_reasons.append("operator_approval_expired")
    if _safe_int(approval_map.get("max_documents"), default=0) > MAX_DOCUMENTS:
        no_go_reasons.append("max_documents_exceeds_1")
    if _safe_int(approval_map.get("max_document_versions"), default=0) > MAX_DOCUMENT_VERSIONS:
        no_go_reasons.append("max_document_versions_exceeds_1")
    if _safe_int(approval_map.get("max_chunks"), default=0) > MAX_CHUNKS:
        no_go_reasons.append("max_chunks_exceeds_20")
    if _safe_int(approval_map.get("max_documents"), default=0) < 1:
        pause_reasons.append("max_documents_missing_or_zero")
    if _safe_int(approval_map.get("max_document_versions"), default=0) < 1:
        pause_reasons.append("max_document_versions_missing_or_zero")
    if _safe_int(approval_map.get("max_chunks"), default=0) < 1:
        pause_reasons.append("max_chunks_missing_or_zero")
    if not _safe_text(approval_map.get("expected_payload_fingerprint")):
        no_go_reasons.append("payload_fingerprint_missing")
    if worktree_status_text.strip():
        pause_reasons.append("worktree_status_not_clean")

    feature_summary, feature_pause, feature_no_go = _feature_flag_summary(
        _mapping(approval_map.get("feature_flags_expected"))
    )
    pause_reasons.extend(feature_pause)
    no_go_reasons.extend(feature_no_go)

    report_refs, report_pause, report_no_go = _report_refs(approval_map)
    pause_reasons.extend(report_pause)
    no_go_reasons.extend(report_no_go)

    if no_go_reasons:
        state = "preflight_no_go"
        reasons = sorted(set(no_go_reasons + pause_reasons))
    elif pause_reasons:
        state = "preflight_pause"
        reasons = sorted(set(pause_reasons))
    else:
        state = "preflight_ready_for_operator_stop"
        reasons = ["all_runtime_preflight_gates_passed"]

    return {
        "runtime_preflight_version": RUNTIME_PREFLIGHT_VERSION,
        "created_at": created,
        "approval_summary": {
            "approval_id": _safe_text(approval_map.get("approval_id"), default="missing"),
            "approval_version": _safe_text(
                approval_map.get("approval_version"),
                default="missing",
            ),
            "approved_by": _safe_text(approval_map.get("approved_by"), default="missing"),
            "target_environment": _safe_text(
                approval_map.get("target_environment"),
                default="missing",
            ),
            "target_git_commit": _safe_text(
                approval_map.get("target_git_commit"),
                default="missing",
            ),
            "write_run_id": _safe_text(approval_map.get("write_run_id"), default="missing"),
            "source_asset_ref_hash": _hash_text(
                _safe_text(approval_map.get("source_asset_ref"), default="missing")
            ),
        },
        "git": {
            "expected_git_commit": _safe_text(expected_git_commit, default="missing"),
            "target_git_commit_matches": _safe_text(approval_map.get("target_git_commit"))
            == expected_git_commit,
            "worktree_clean": not bool(worktree_status_text.strip()),
        },
        "write_scope": {
            "max_documents": _safe_int(approval_map.get("max_documents"), default=0),
            "max_document_versions": _safe_int(
                approval_map.get("max_document_versions"),
                default=0,
            ),
            "max_chunks": _safe_int(approval_map.get("max_chunks"), default=0),
            "one_run_boundary": (
                _safe_int(approval_map.get("max_documents"), default=0) == 1
                and _safe_int(approval_map.get("max_document_versions"), default=0) == 1
                and 1 <= _safe_int(approval_map.get("max_chunks"), default=0) <= MAX_CHUNKS
            ),
        },
        "idempotency": {
            "write_run_id_present": bool(_safe_text(approval_map.get("write_run_id"))),
            "idempotency_key_present": bool(
                _safe_text(approval_map.get("evidence_write_idempotency_key"))
            ),
            "payload_fingerprint_present": bool(
                _safe_text(approval_map.get("expected_payload_fingerprint"))
            ),
            "idempotency_key_hash": _hash_text(
                _safe_text(
                    approval_map.get("evidence_write_idempotency_key"),
                    default="missing",
                )
            ),
        },
        "feature_flags": feature_summary,
        "report_refs": report_refs,
        "safety": _safety(),
        "dry_run": True,
        "writes_authorized": False,
        "would_invoke_writer": False,
        "decision": {
            "runtime_preflight_state": state,
            "reasons": reasons,
        },
    }


def write_runtime_evidence_write_preflight_report(
    output_path: Path,
    report: dict[str, Any],
) -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return output_path


def _feature_flag_summary(flags: dict[str, Any]) -> tuple[dict[str, Any], list[str], list[str]]:
    pause: list[str] = []
    no_go: list[str] = []
    required = ALLOWED_TRUE_FEATURE_FLAGS | REQUIRED_FALSE_FEATURE_FLAGS
    for flag in sorted(required):
        if flag not in flags:
            pause.append(f"missing_feature_flag_{flag}")
    for flag, value in flags.items():
        if value is True and flag not in ALLOWED_TRUE_FEATURE_FLAGS:
            no_go.append(f"forbidden_feature_flag_true_{flag}")
    for flag in REQUIRED_FALSE_FEATURE_FLAGS:
        if flags.get(flag) is True:
            no_go.append(f"forbidden_feature_flag_true_{flag}")
    return (
        {
            "allowed_true_flags": sorted(ALLOWED_TRUE_FEATURE_FLAGS),
            "required_false_flags": sorted(REQUIRED_FALSE_FEATURE_FLAGS),
            "provided_true_flags": sorted(
                flag for flag, value in flags.items() if value is True
            ),
            "agent_answer_integration": flags.get(
                "PLATFORM_ASSET_AGENT_ANSWER_INTEGRATION_ENABLED"
            )
            is True,
            "index_write": flags.get("PLATFORM_ASSET_INDEX_WRITE_ENABLED") is True,
            "api_cli_runtime": flags.get("PLATFORM_ASSET_API_CLI_RUNTIME_ENABLED") is True,
        },
        pause,
        sorted(set(no_go)),
    )


def _report_refs(
    approval: dict[str, Any],
) -> tuple[list[dict[str, Any]], list[str], list[str]]:
    items: list[dict[str, Any]] = []
    pause: list[str] = []
    no_go: list[str] = []
    for field in REPORT_REF_FIELDS:
        raw_path = _safe_text(approval.get(field), default="")
        path = Path(raw_path) if raw_path else None
        exists = path.exists() if path else False
        appears_sanitized = False
        content_hash = "missing"
        report_status = "missing"
        if not exists:
            pause.append(f"missing_report_ref_{field}")
        else:
            text = path.read_text(encoding="utf-8")
            content_hash = _hash_text(text)
            appears_sanitized = _appears_sanitized(text)
            report_status = _safe_report_status(text)
            if not appears_sanitized:
                no_go.append(f"unsafe_report_ref_{field}")
        items.append(
            {
                "ref_name": field,
                "path_name": path.name if path else "missing",
                "path_hash": _hash_text(raw_path or "missing"),
                "content_hash": content_hash,
                "report_status": report_status,
                "exists": exists,
                "appears_sanitized": appears_sanitized,
            }
        )
    return items, pause, no_go


def _appears_sanitized(text: str) -> bool:
    for marker in FORBIDDEN_STRING_MARKERS:
        if marker in text:
            return False
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        return False
    return _json_appears_sanitized(data)


def _safe_report_status(text: str) -> str:
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        return "invalid_json"
    if not isinstance(data, dict):
        return "non_object"
    return _safe_text(data.get("status"), default="status_not_present")


def _json_appears_sanitized(value: Any) -> bool:
    if isinstance(value, dict):
        for key, item in value.items():
            if key in FORBIDDEN_REPORT_KEYS:
                return False
            if not _json_appears_sanitized(item):
                return False
        return True
    if isinstance(value, list):
        return all(_json_appears_sanitized(item) for item in value)
    if isinstance(value, str):
        return not any(marker in value for marker in FORBIDDEN_STRING_MARKERS)
    return True


def _safety() -> dict[str, bool]:
    return {
        "writer_invoked": False,
        "documents_written": False,
        "document_versions_written": False,
        "chunks_written": False,
        "citations_written": False,
        "db_writes": False,
        "parser_invoked": False,
        "scratch_copy_performed": False,
        "raw_file_content_read": False,
        "nas_scanned": False,
        "opensearch_writes": False,
        "qdrant_writes": False,
        "minio_writes": False,
        "platform_db_writes": False,
        "audit_table_writes": False,
        "agent_answer_integration": False,
        "repair_backfill_reindex_cleanup": False,
        "production_rollout": False,
    }


def _mapping(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _safe_text(value: Any, *, default: str = "") -> str:
    if value is None:
        return default
    text = str(value).strip()
    return text if text else default


def _safe_int(value: Any, *, default: int) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _hash_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()[:16]


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace(
        "+00:00",
        "Z",
    )


def _expires_after(expires_at: str, created_at: str) -> bool:
    try:
        expires = _parse_time(expires_at)
        created = _parse_time(created_at)
    except ValueError:
        return False
    return expires > created


def _parse_time(value: str) -> datetime:
    if value.endswith("Z"):
        value = value[:-1] + "+00:00"
    parsed = datetime.fromisoformat(value)
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)
