from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from sqlalchemy.orm import Session

from app.services.asset_catalog.evidence_writer import (
    FORBIDDEN_INPUT_KEYS,
    EvidenceOnlyWriter,
)

RUNTIME_SMOKE_REPORT_VERSION = "hermes_runtime_evidence_writer_smoke.v0"
READY_STATE = "writer_smoke_ready_for_operator_stop"
EXECUTED_STATE = "writer_smoke_executed"
PAUSE_STATE = "writer_smoke_pause"
NO_GO_STATE = "writer_smoke_no_go"
PREFLIGHT_READY_STATE = "preflight_ready_for_operator_stop"
TEST_MACHINE_ENVIRONMENT = "test_machine_only"
MAX_DOCUMENTS = 1
MAX_DOCUMENT_VERSIONS = 1
MAX_CHUNKS = 20

REQUIRED_TRUE_FLAGS = frozenset(
    {
        "PLATFORM_ASSET_REAL_EVIDENCE_WRITE_ENABLED",
        "PLATFORM_ASSET_REAL_EVIDENCE_WRITE_SMOKE_ENABLED",
    }
)
REQUIRED_FALSE_FLAGS = frozenset(
    {
        "PLATFORM_ASSET_AGENT_ANSWER_INTEGRATION_ENABLED",
        "PLATFORM_ASSET_INDEX_WRITE_ENABLED",
        "PLATFORM_ASSET_API_CLI_RUNTIME_ENABLED",
        "PLATFORM_ASSET_PARSER_ENABLED",
        "PLATFORM_ASSET_ROLLOUT_ENABLED",
    }
)


def build_runtime_evidence_writer_smoke_report(
    *,
    approval: dict[str, Any],
    preflight_report: dict[str, Any],
    payload: dict[str, Any],
    expected_git_commit: str,
    worktree_status_text: str = "",
    execute_writer: bool = False,
    db: Session | None = None,
) -> dict[str, Any]:
    """Validate a future runtime writer smoke without touching real DBs.

    The default path is gate-only. The only write-capable path requires an
    injected SQLAlchemy session, which keeps Phase 2.91 execution test-local.
    """

    pause_reasons: list[str] = []
    no_go_reasons: list[str] = []
    approval_map = _mapping(approval)
    payload_map = _mapping(payload)
    preflight_map = _mapping(preflight_report)

    pause_reasons.extend(_missing_input_reasons(approval_map, payload_map, preflight_map))
    preflight_state = _preflight_state(preflight_map)
    if preflight_state != PREFLIGHT_READY_STATE:
        no_go_reasons.append("preflight_not_ready")
    if worktree_status_text.strip():
        pause_reasons.append("worktree_status_not_clean")

    no_go_reasons.extend(
        _approval_and_payload_mismatch_reasons(
            approval_map,
            payload_map,
            expected_git_commit=expected_git_commit,
        )
    )
    pause_reasons.extend(_missing_feature_flag_reasons(approval_map, payload_map))
    no_go_reasons.extend(_forbidden_feature_flag_reasons(approval_map, payload_map))
    no_go_reasons.extend(_scope_reasons(approval_map, payload_map))
    no_go_reasons.extend(
        f"forbidden_payload_key_{key}" for key in sorted(_find_forbidden_keys(payload_map))
    )
    no_go_reasons.extend(_preflight_side_effect_reasons(preflight_map))

    if execute_writer and db is None:
        pause_reasons.append("execute_writer_requires_injected_test_session")

    report = _base_report(
        approval_map,
        payload_map,
        preflight_state=preflight_state,
        git_commit_match=_safe_text(approval_map.get("target_git_commit"))
        == expected_git_commit,
    )

    if no_go_reasons:
        report["decision"] = NO_GO_STATE
        report["no_go_reasons"] = sorted(set(no_go_reasons))
        if pause_reasons:
            report["pause_reasons"] = sorted(set(pause_reasons))
        return report
    if pause_reasons:
        report["decision"] = PAUSE_STATE
        report["pause_reasons"] = sorted(set(pause_reasons))
        return report
    if not execute_writer:
        report["decision"] = READY_STATE
        return report

    writer = EvidenceOnlyWriter(db)
    write_run_id = _safe_text(payload_map.get("write_run_id"))
    rollback_before = writer.build_rollback_dry_run(write_run_id)
    write_result = writer.write(payload_map)
    rollback_after = writer.build_rollback_dry_run(write_run_id)

    report["decision"] = EXECUTED_STATE
    report["would_invoke_writer"] = True
    report["writer_invoked"] = True
    report["db_writes"] = write_result.get("safety", {}).get("db_writes") is True
    report["created_counts"] = _created_counts(write_result)
    report["idempotency_status"] = _safe_text(
        write_result.get("idempotency", {}).get("status"),
        default="unknown",
    )
    report["rollback_dry_run_before"] = rollback_before
    report["rollback_dry_run_after"] = rollback_after
    if write_result.get("decision", {}).get("state") == "evidence_write_no_go":
        report["decision"] = NO_GO_STATE
        report["no_go_reasons"] = list(write_result.get("decision", {}).get("reasons", []))
        report["writer_invoked"] = True
        report["db_writes"] = False
    return report


def write_runtime_evidence_writer_smoke_report(
    output_path: Path,
    report: dict[str, Any],
) -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return output_path


def _base_report(
    approval: dict[str, Any],
    payload: dict[str, Any],
    *,
    preflight_state: str,
    git_commit_match: bool,
) -> dict[str, Any]:
    return {
        "report_version": RUNTIME_SMOKE_REPORT_VERSION,
        "decision": PAUSE_STATE,
        "write_run_id": _safe_text(payload.get("write_run_id")),
        "operator_approval_id": _safe_text(approval.get("approval_id")),
        "target_environment": _safe_text(
            approval.get("target_environment"),
            default="missing",
        ),
        "git_commit_match": git_commit_match,
        "preflight_state": preflight_state,
        "would_invoke_writer": False,
        "writer_invoked": False,
        "db_writes": False,
        "created_counts": _empty_counts(),
        "idempotency_status": "not_attempted",
        "rollback_dry_run_before": {},
        "rollback_dry_run_after": {},
        "forbidden_actions": _forbidden_actions(),
        "sanitized": True,
        "pause_reasons": [],
        "no_go_reasons": [],
    }


def _missing_input_reasons(
    approval: dict[str, Any],
    payload: dict[str, Any],
    preflight_report: dict[str, Any],
) -> list[str]:
    reasons: list[str] = []
    if not approval:
        reasons.append("missing_approval")
    if not payload:
        reasons.append("missing_payload")
    if not preflight_report:
        reasons.append("missing_preflight_report")
    for field in ("approval_id", "target_git_commit", "write_run_id"):
        if approval and not _safe_text(approval.get(field)):
            reasons.append(f"missing_approval_field_{field}")
    if payload and not _safe_text(payload.get("payload_fingerprint")):
        reasons.append("missing_payload_fingerprint")
    return reasons


def _approval_and_payload_mismatch_reasons(
    approval: dict[str, Any],
    payload: dict[str, Any],
    *,
    expected_git_commit: str,
) -> list[str]:
    reasons: list[str] = []
    if _safe_text(approval.get("target_environment")) != TEST_MACHINE_ENVIRONMENT:
        reasons.append("target_environment_not_test_machine_only")
    if _safe_text(payload.get("target_environment")) != TEST_MACHINE_ENVIRONMENT:
        reasons.append("payload_target_environment_not_test_machine_only")
    if _safe_text(approval.get("target_git_commit")) != expected_git_commit:
        reasons.append("target_git_commit_mismatch")
    if _safe_text(approval.get("write_run_id")) != _safe_text(payload.get("write_run_id")):
        reasons.append("write_run_id_mismatch")
    if _safe_text(approval.get("source_asset_ref")) != _safe_text(payload.get("source_asset_ref")):
        reasons.append("source_asset_ref_mismatch")
    if _safe_text(approval.get("project_scope")) != _safe_text(payload.get("project_scope")):
        reasons.append("project_scope_mismatch")
    if _safe_text(approval.get("permission_proof_ref")) != _safe_text(
        payload.get("permission_proof_ref")
    ):
        reasons.append("permission_proof_ref_mismatch")
    if _safe_text(approval.get("rollback_dry_run_ref")) != _safe_text(
        payload.get("rollback_dry_run_ref")
    ):
        reasons.append("rollback_dry_run_ref_mismatch")
    if _safe_text(approval.get("expected_payload_fingerprint")) != _safe_text(
        payload.get("payload_fingerprint")
    ):
        reasons.append("payload_fingerprint_mismatch")
    if _safe_text(approval.get("evidence_write_idempotency_key")) != _safe_text(
        _mapping(payload.get("idempotency")).get("idempotency_key")
    ):
        reasons.append("idempotency_key_mismatch")
    if approval.get("writes_authorized") is not True:
        reasons.append("writes_authorized_not_true")
    return reasons


def _missing_feature_flag_reasons(
    approval: dict[str, Any],
    payload: dict[str, Any],
) -> list[str]:
    approval_flags = _mapping(approval.get("feature_flags_expected"))
    payload_flags = _mapping(payload.get("feature_flags"))
    reasons: list[str] = []
    for flag in sorted(REQUIRED_TRUE_FLAGS | REQUIRED_FALSE_FLAGS):
        if flag not in approval_flags:
            reasons.append(f"missing_approval_feature_flag_{flag}")
        if flag not in payload_flags:
            reasons.append(f"missing_payload_feature_flag_{flag}")
    return reasons


def _forbidden_feature_flag_reasons(
    approval: dict[str, Any],
    payload: dict[str, Any],
) -> list[str]:
    approval_flags = _mapping(approval.get("feature_flags_expected"))
    payload_flags = _mapping(payload.get("feature_flags"))
    reasons: list[str] = []
    for flag in sorted(REQUIRED_TRUE_FLAGS):
        if approval_flags.get(flag) is not True:
            reasons.append(f"required_feature_flag_not_true_{flag}")
        if payload_flags.get(flag) is not True:
            reasons.append(f"payload_required_feature_flag_not_true_{flag}")
    for flag in sorted(REQUIRED_FALSE_FLAGS):
        if approval_flags.get(flag) is True or payload_flags.get(flag) is True:
            reasons.append(f"forbidden_feature_flag_true_{flag}")
    return reasons


def _scope_reasons(approval: dict[str, Any], payload: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    chunks = _list_of_mappings(payload.get("chunks"))
    if _safe_int(approval.get("max_documents"), default=0) != MAX_DOCUMENTS:
        reasons.append("document_scope_not_one")
    if _safe_int(approval.get("max_document_versions"), default=0) != MAX_DOCUMENT_VERSIONS:
        reasons.append("version_scope_not_one")
    if _safe_int(approval.get("max_chunks"), default=0) != MAX_CHUNKS:
        reasons.append("chunk_approval_limit_not_20")
    if len(chunks) > MAX_CHUNKS:
        reasons.append("chunk_scope_exceeds_20")
    if isinstance(payload.get("documents"), list) and len(payload["documents"]) > MAX_DOCUMENTS:
        reasons.append("document_scope_exceeds_1")
    if isinstance(payload.get("document_versions"), list) and len(
        payload["document_versions"]
    ) > MAX_DOCUMENT_VERSIONS:
        reasons.append("version_scope_exceeds_1")
    return reasons


def _preflight_side_effect_reasons(preflight_report: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    safety = _mapping(preflight_report.get("safety"))
    forbidden_safety = {
        "writer_invoked": "preflight_writer_invoked",
        "db_writes": "preflight_db_writes",
        "parser_invoked": "preflight_parser_invoked",
        "file_copied": "preflight_file_copied",
        "nas_scanned": "preflight_nas_scanned",
        "opensearch_writes": "preflight_opensearch_writes",
        "qdrant_writes": "preflight_qdrant_writes",
        "minio_writes": "preflight_minio_writes",
        "agent_answer_integration": "preflight_agent_answer_integration",
        "production_rollout": "preflight_production_rollout",
    }
    for field, reason in forbidden_safety.items():
        if safety.get(field) is True:
            reasons.append(reason)
    if preflight_report.get("would_invoke_writer") is True:
        reasons.append("preflight_would_invoke_writer")
    if preflight_report.get("writes_authorized") is True:
        reasons.append("preflight_writes_authorized")
    return reasons


def _created_counts(write_result: dict[str, Any]) -> dict[str, int]:
    writes = _mapping(write_result.get("writes"))
    return {
        "documents": _safe_int(writes.get("documents"), default=0),
        "document_versions": _safe_int(writes.get("document_versions"), default=0),
        "chunks": _safe_int(writes.get("chunks"), default=0),
        "citations": _safe_int(writes.get("citations"), default=0),
    }


def _preflight_state(preflight_report: dict[str, Any]) -> str:
    return _safe_text(
        _mapping(preflight_report.get("decision")).get("runtime_preflight_state"),
        default="missing",
    )


def _forbidden_actions() -> dict[str, bool]:
    return {
        "parser_executed": False,
        "scratch_copy_performed": False,
        "nas_scanned": False,
        "opensearch_written": False,
        "qdrant_written": False,
        "minio_written": False,
        "platform_db_written": False,
        "agent_answer_integration_enabled": False,
        "repair_executed": False,
        "rollout_executed": False,
    }


def _empty_counts() -> dict[str, int]:
    return {
        "documents": 0,
        "document_versions": 0,
        "chunks": 0,
        "citations": 0,
    }


def _find_forbidden_keys(value: Any) -> set[str]:
    found: set[str] = set()
    if isinstance(value, dict):
        for key, nested in value.items():
            if key in FORBIDDEN_INPUT_KEYS:
                found.add(key)
            found.update(_find_forbidden_keys(nested))
    elif isinstance(value, list):
        for item in value:
            found.update(_find_forbidden_keys(item))
    return found


def _mapping(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _list_of_mappings(value: Any) -> list[dict[str, Any]]:
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, dict)]


def _safe_text(value: Any, *, default: str = "") -> str:
    if value is None:
        return default
    text = str(value).strip()
    return text or default


def _safe_int(value: Any, *, default: int) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default
