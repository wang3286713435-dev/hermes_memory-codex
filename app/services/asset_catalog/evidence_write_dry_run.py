from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

WRITE_DRY_RUN_VERSION = "nas_evidence_write_dry_run.v0"
PREFLIGHT_VERSION = "nas_evidence_write_preflight.v0"
SAFETY_FLAGS = (
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
FORBIDDEN_INPUT_KEYS = frozenset(
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


class InMemoryEvidenceWriteDryRunStore:
    def __init__(self) -> None:
        self._records: dict[str, dict[str, Any]] = {}

    def register(
        self,
        *,
        idempotency_key: str,
        fingerprint: str,
        simulated_document_ref: str,
        simulated_chunk_refs: list[str],
    ) -> dict[str, Any]:
        existing = self._records.get(idempotency_key)
        if existing is None:
            self._records[idempotency_key] = {
                "fingerprint": fingerprint,
                "simulated_document_ref": simulated_document_ref,
                "simulated_chunk_refs": simulated_chunk_refs,
            }
            return {
                "status": "created",
                "duplicates_detected": 0,
                "idempotency_conflict": False,
            }
        if existing["fingerprint"] == fingerprint:
            return {
                "status": "duplicate_detected",
                "duplicates_detected": 1,
                "idempotency_conflict": False,
            }
        return {
            "status": "idempotency_conflict",
            "duplicates_detected": 0,
            "idempotency_conflict": True,
        }


def build_evidence_write_dry_run_report(
    preflight: dict[str, Any],
    *,
    created_at: str | None = None,
    store: InMemoryEvidenceWriteDryRunStore | None = None,
) -> dict[str, Any]:
    created = created_at or _utc_now()
    payload_ref = _mapping(preflight.get("payload_ref"))
    idempotency = _mapping(preflight.get("idempotency"))
    citation_coverage = _mapping(preflight.get("citation_coverage"))
    rollback = _mapping(preflight.get("rollback"))
    locks = _mapping(preflight.get("locks"))
    decision = _mapping(preflight.get("decision"))
    safety = _mapping(preflight.get("safety"))

    forbidden_keys = sorted(_find_forbidden_keys(preflight))
    safety_reasons = _true_safety_reasons(preflight)
    idempotency_key = _safe_text(idempotency.get("idempotency_key"), default="")
    chunk_count = _safe_int(citation_coverage.get("chunk_count"), default=0)
    anchors = _redacted_anchors(citation_coverage, idempotency, chunk_count)
    document_ref = _simulated_document_ref(payload_ref, idempotency, preflight)
    chunk_refs = [
        _simulated_chunk_ref(document_ref, index, anchor)
        for index, anchor in enumerate(anchors, start=1)
    ]
    fingerprint = _fingerprint(preflight)

    gates = {
        "preflight_version_supported": preflight.get("preflight_version")
        == PREFLIGHT_VERSION,
        "preflight_ready_for_write_dry_run": decision.get("preflight_state")
        == "write_preflight_ready_for_dry_run",
        "preflight_dry_run_true": preflight.get("dry_run") is True,
        "preflight_writes_authorized_false": preflight.get("writes_authorized") is False,
        "preflight_safety_flags_clear": not safety_reasons,
        "no_forbidden_input_keys": not forbidden_keys,
        "payload_ref_asset_ref_present": bool(payload_ref.get("asset_ref")),
        "payload_ref_source_view_present": bool(payload_ref.get("source_view")),
        "payload_ref_platform_contract_version_present": bool(
            payload_ref.get("platform_contract_version")
        ),
        "idempotency_key_present": bool(idempotency_key),
        "citation_coverage_complete": citation_coverage.get("complete") is True,
        "rollback_plan_available": rollback.get("rollback_plan_available") is True,
        "lock_required": locks.get("lock_required") is True,
    }
    reasons = _reason_codes(gates)
    reasons.extend(safety_reasons)
    reasons.extend(f"forbidden_input_key_{key}" for key in forbidden_keys)

    store_result = {
        "status": "not_registered",
        "duplicates_detected": 0,
        "idempotency_conflict": False,
    }
    state = "write_dry_run_not_allowed"
    if safety_reasons or forbidden_keys:
        state = "write_dry_run_no_go"
    elif all(gates.values()):
        store_result = (store or InMemoryEvidenceWriteDryRunStore()).register(
            idempotency_key=idempotency_key,
            fingerprint=fingerprint,
            simulated_document_ref=document_ref,
            simulated_chunk_refs=chunk_refs,
        )
        if store_result["idempotency_conflict"]:
            state = "write_dry_run_no_go"
            reasons.append("idempotency_conflict")
        else:
            state = "write_dry_run_go"
            reasons = ["all_write_dry_run_gates_passed"]
            if store_result["duplicates_detected"]:
                reasons.append("duplicate_simulation_detected")

    simulated_documents = []
    simulated_chunks = []
    simulated_citations = []
    if state == "write_dry_run_go":
        source_view = _safe_text(payload_ref.get("source_view"), default="FileAssetView")
        asset_ref = _safe_text(payload_ref.get("asset_ref"), default="redacted-asset")
        simulated_documents.append(
            {
                "simulated_document_ref": document_ref,
                "external_asset_ref": _external_asset_ref(payload_ref),
                "source_catalog_ref": f"{source_view}:{asset_ref}",
                "source_preflight_report_id": _safe_text(
                    preflight.get("run_id"),
                    default="redacted-preflight-run",
                ),
                "candidate_version_ref": _candidate_version_ref(payload_ref, idempotency),
                "idempotency_key": idempotency_key,
                "created_in_dry_run": True,
            }
        )
        for index, anchor in enumerate(anchors, start=1):
            chunk_ref = chunk_refs[index - 1]
            simulated_chunks.append(
                {
                    "simulated_chunk_ref": chunk_ref,
                    "simulated_document_ref": document_ref,
                    "candidate_chunk_index": index,
                    "redacted_citation_anchor": anchor,
                    "source_catalog_ref": f"{source_view}:{asset_ref}",
                    "source_preflight_item_ref": _safe_text(
                        preflight.get("run_id"),
                        default="redacted-preflight-run",
                    ),
                    "idempotency_key": idempotency_key,
                    "created_in_dry_run": True,
                }
            )
            simulated_citations.append(
                {
                    "simulated_chunk_ref": chunk_ref,
                    "source_asset_ref": asset_ref,
                    "source_view": source_view,
                    "redacted_citation_anchor": anchor,
                    "production_evidence": False,
                }
            )

    return {
        "write_dry_run_version": WRITE_DRY_RUN_VERSION,
        "run_id": _safe_text(preflight.get("run_id"), default="redacted-preflight-run"),
        "created_at": created,
        "preflight_ref": {
            "preflight_version": _safe_text(
                preflight.get("preflight_version"),
                default="unknown",
            ),
            "preflight_run_id": _safe_text(
                preflight.get("run_id"),
                default="redacted-preflight-run",
            ),
            "preflight_state": _safe_text(
                decision.get("preflight_state"),
                default="unknown",
            ),
        },
        "simulated_store": {
            "backend": "in_memory",
            "real_hermes_db_used": False,
            "platform_db_used": False,
            "opensearch_used": False,
            "qdrant_used": False,
            "minio_used": False,
        },
        "simulated_documents": simulated_documents,
        "simulated_chunks": simulated_chunks,
        "simulated_citations": simulated_citations,
        "idempotency": {
            "idempotency_key": idempotency_key or "missing",
            "status": store_result["status"],
            "duplicates_detected": store_result["duplicates_detected"],
            "idempotency_conflict": store_result["idempotency_conflict"],
            "duplicate_write_allowed": False,
        },
        "rollback": {
            "rollback_plan_available": rollback.get("rollback_plan_available") is True,
            "rollback_scope": "same_run_only",
            "simulated_refs_to_remove": (
                [document_ref] + chunk_refs if state == "write_dry_run_go" else []
            ),
            "source_data_mutation": False,
            "delete_original_nas_file": False,
            "delete_platform_db_record": False,
            "repair_backfill_reindex_cleanup": False,
        },
        "safety": _safety(),
        "dry_run": True,
        "writes_authorized": False,
        "decision": {
            "write_dry_run_state": state,
            "reasons": reasons or ["write_dry_run_not_allowed"],
        },
    }


def write_evidence_write_dry_run_report(
    output_dir: Path,
    report: dict[str, Any],
) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / f"{_safe_filename(report.get('run_id'))}-write-dry-run.json"
    path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return path


def _safety() -> dict[str, bool]:
    return {
        "documents_written": False,
        "chunks_written": False,
        "db_writes": False,
        "opensearch_writes": False,
        "qdrant_writes": False,
        "minio_writes": False,
        "parser_invoked": False,
        "file_copied": False,
        "raw_content_read": False,
        "nas_scanned": False,
        "agent_answer_integration": False,
        "production_rollout": False,
        "report_is_production_evidence": False,
    }


def _mapping(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _safe_text(value: Any, *, default: str) -> str:
    if value is None:
        return default
    text = str(value).strip()
    return text or default


def _safe_int(value: Any, *, default: int) -> int:
    if isinstance(value, bool):
        return default
    if isinstance(value, int):
        return value
    try:
        return int(str(value))
    except (TypeError, ValueError):
        return default


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _safe_filename(value: Any) -> str:
    text = _safe_text(value, default="redacted-run")
    return "".join(char if char.isalnum() or char in {"-", "_"} else "-" for char in text)


def _sha256(prefix: str, payload: str) -> str:
    return f"{prefix}_{hashlib.sha256(payload.encode('utf-8')).hexdigest()[:24]}"


def _canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _fingerprint(preflight: dict[str, Any]) -> str:
    return hashlib.sha256(_canonical_json(preflight).encode("utf-8")).hexdigest()


def _external_asset_ref(payload_ref: dict[str, Any]) -> str:
    source_view = _safe_text(payload_ref.get("source_view"), default="FileAssetView")
    asset_ref = _safe_text(payload_ref.get("asset_ref"), default="redacted-asset")
    contract_version = _safe_text(
        payload_ref.get("platform_contract_version"),
        default="delivery_platform.asset_views.v1.1",
    )
    return _sha256("extasset", f"{source_view}|{asset_ref}|{contract_version}")


def _candidate_version_ref(
    payload_ref: dict[str, Any],
    idempotency: dict[str, Any],
) -> str:
    seed = "|".join(
        [
            _safe_text(payload_ref.get("asset_ref"), default="redacted-asset"),
            _safe_text(payload_ref.get("payload_run_id"), default="redacted-payload-run"),
            _safe_text(idempotency.get("idempotency_key"), default="missing-key"),
        ]
    )
    return _sha256("simver", seed)


def _simulated_document_ref(
    payload_ref: dict[str, Any],
    idempotency: dict[str, Any],
    preflight: dict[str, Any],
) -> str:
    seed = "|".join(
        [
            _safe_text(payload_ref.get("asset_ref"), default="redacted-asset"),
            _safe_text(payload_ref.get("payload_run_id"), default="redacted-payload-run"),
            _safe_text(idempotency.get("idempotency_key"), default="missing-key"),
            _safe_text(preflight.get("preflight_version"), default="unknown"),
        ]
    )
    return _sha256("simdoc", seed)


def _simulated_chunk_ref(document_ref: str, index: int, anchor: str) -> str:
    return _sha256("simchunk", f"{document_ref}|{index}|{anchor}")


def _redacted_anchors(
    citation_coverage: dict[str, Any],
    idempotency: dict[str, Any],
    chunk_count: int,
) -> list[str]:
    anchors = citation_coverage.get("redacted_citation_anchors")
    if isinstance(anchors, list) and all(isinstance(anchor, str) for anchor in anchors):
        return anchors
    dry_run_refs = idempotency.get("dry_run_chunk_refs")
    if isinstance(dry_run_refs, list) and dry_run_refs:
        return [
            f"redacted-anchor:{_safe_text(ref, default=f'chunk-{index:04d}')}"
            for index, ref in enumerate(dry_run_refs, start=1)
        ]
    count = max(chunk_count, 0)
    return [f"redacted-anchor:chunk-{index:04d}" for index in range(1, count + 1)]


def _find_forbidden_keys(value: Any) -> set[str]:
    found: set[str] = set()
    if isinstance(value, dict):
        for key, child in value.items():
            key_text = str(key)
            if key_text in FORBIDDEN_INPUT_KEYS:
                found.add(key_text)
            found.update(_find_forbidden_keys(child))
    elif isinstance(value, list):
        for child in value:
            found.update(_find_forbidden_keys(child))
    return found


def _true_safety_reasons(preflight: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    if preflight.get("writes_authorized") is True:
        reasons.append("writes_authorized_true")
    safety = _mapping(preflight.get("safety"))
    for flag in SAFETY_FLAGS:
        if safety.get(flag) is True:
            reasons.append(f"{flag}_true")
    return reasons


def _reason_codes(gates: dict[str, bool]) -> list[str]:
    reason_names = {
        "preflight_version_supported": "preflight_version_unsupported",
        "preflight_ready_for_write_dry_run": "preflight_not_ready_for_write_dry_run",
        "preflight_dry_run_true": "preflight_dry_run_not_true",
        "preflight_writes_authorized_false": "preflight_writes_authorized_not_false",
        "preflight_safety_flags_clear": "preflight_safety_flags_not_clear",
        "no_forbidden_input_keys": "forbidden_input_keys_present",
        "payload_ref_asset_ref_present": "payload_ref_asset_ref_missing",
        "payload_ref_source_view_present": "payload_ref_source_view_missing",
        "payload_ref_platform_contract_version_present": "payload_ref_platform_contract_version_missing",
        "idempotency_key_present": "idempotency_key_missing",
        "citation_coverage_complete": "citation_coverage_not_complete",
        "rollback_plan_available": "rollback_plan_missing",
        "lock_required": "lock_required_missing",
    }
    return [reason_names[key] for key, value in gates.items() if not value]
