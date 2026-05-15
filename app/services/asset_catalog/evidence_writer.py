from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import Any

from sqlalchemy.orm import Session

from app.models.chunk import Chunk
from app.models.citation import CitationRecord
from app.models.document import Document, DocumentVersion

EVIDENCE_WRITE_VERSION = "hermes_evidence_only_write.v0"
PAYLOAD_VERSION = "hermes_evidence_only_payload.v0"
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


@dataclass(frozen=True)
class EvidenceWriteDecision:
    state: str
    reasons: list[str]


@dataclass(frozen=True)
class EvidenceWriteRollbackPlan:
    write_run_id: str
    rows_by_model: dict[str, list[str]]
    dry_run: bool = True
    delete_rows: bool = False
    executable: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "write_run_id": self.write_run_id,
            "rows_by_model": self.rows_by_model,
            "dry_run": self.dry_run,
            "delete_rows": self.delete_rows,
            "executable": self.executable,
            "external_side_effects": {
                "platform_db": False,
                "opensearch": False,
                "qdrant": False,
                "minio": False,
                "nas": False,
                "audit_logs": False,
            },
        }


class EvidenceOnlyWriter:
    """Test-local evidence writer for Phase 2.87b.

    The service only writes through an injected SQLAlchemy session. It has no
    parser, file, index, object-store, audit, API, or CLI side effects.
    """

    def __init__(self, db: Session) -> None:
        self.db = db

    def write(self, payload: dict[str, Any]) -> dict[str, Any]:
        result = build_evidence_write_result(payload)
        state = result["decision"]["state"]
        if state != "evidence_write_ready":
            return result

        idempotency_key = result["idempotency"]["idempotency_key"]
        fingerprint = result["idempotency"]["payload_fingerprint"]
        duplicate = self._find_existing_by_idempotency(idempotency_key)
        if duplicate is not None:
            existing_fingerprint = (duplicate.metadata_json or {}).get(
                "evidence_write_payload_fingerprint"
            )
            if existing_fingerprint == fingerprint:
                result["decision"] = {
                    "state": "evidence_write_duplicate",
                    "reasons": ["duplicate_evidence_write_detected"],
                }
                result["idempotency"]["status"] = "duplicate_detected"
                result["idempotency"]["duplicates_detected"] = 1
                result["writes"] = _empty_writes()
                result["safety"] = _safety(db_writes=False)
                return result
            result["decision"] = {
                "state": "evidence_write_no_go",
                "reasons": ["idempotency_conflict"],
            }
            result["idempotency"]["status"] = "idempotency_conflict"
            result["idempotency"]["idempotency_conflict"] = True
            result["writes"] = _empty_writes()
            result["safety"] = _safety(db_writes=False)
            return result

        document, version, chunks, citations = self._create_rows(payload, fingerprint)
        self.db.flush()
        result["decision"] = {
            "state": "evidence_write_go",
            "reasons": ["all_evidence_write_gates_passed"],
        }
        result["idempotency"]["status"] = "created"
        result["created_ids"] = {
            "document_id": document.id,
            "version_id": version.id,
            "chunk_ids": [chunk.id for chunk in chunks],
            "citation_ids": [citation.id for citation in citations],
        }
        result["writes"] = {
            "documents": 1,
            "document_versions": 1,
            "chunks": len(chunks),
            "citations": len(citations),
        }
        result["safety"] = _safety(db_writes=True)
        return result

    def build_rollback_dry_run(self, write_run_id: str) -> dict[str, Any]:
        documents = _rows_with_run_id(self.db.query(Document).all(), write_run_id)
        versions = _rows_with_run_id(self.db.query(DocumentVersion).all(), write_run_id)
        chunks = _rows_with_run_id(self.db.query(Chunk).all(), write_run_id)
        chunk_ids = [chunk.id for chunk in chunks]
        citations = (
            self.db.query(CitationRecord)
            .filter(CitationRecord.chunk_id.in_(chunk_ids))
            .all()
            if chunk_ids
            else []
        )
        return EvidenceWriteRollbackPlan(
            write_run_id=write_run_id,
            rows_by_model={
                "Document": [row.id for row in documents],
                "DocumentVersion": [row.id for row in versions],
                "Chunk": [row.id for row in chunks],
                "CitationRecord": [row.id for row in citations],
            },
        ).to_dict()

    def _find_existing_by_idempotency(self, idempotency_key: str) -> DocumentVersion | None:
        for version in self.db.query(DocumentVersion).all():
            metadata = version.metadata_json or {}
            if metadata.get("evidence_write_idempotency_key") == idempotency_key:
                return version
        return None

    def _create_rows(
        self,
        payload: dict[str, Any],
        fingerprint: str,
    ) -> tuple[Document, DocumentVersion, list[Chunk], list[CitationRecord]]:
        document_payload = _mapping(payload.get("document"))
        version_payload = _mapping(payload.get("document_version"))
        chunks_payload = _list_of_mappings(payload.get("chunks"))
        metadata = _run_metadata(payload, fingerprint)

        document = Document(
            title=_safe_text(document_payload.get("title"), default="redacted evidence document"),
            source_type=_safe_text(document_payload.get("source_type"), default="platform_asset"),
            source_uri=_safe_text(document_payload.get("source_uri"), default="asset-ref:redacted"),
            storage_uri=None,
            document_type=_safe_text(
                document_payload.get("document_type"),
                default="sanitized_test_evidence",
            ),
            owner_id=None,
            department_id=None,
            project_id=_safe_text(payload.get("project_scope"), default=""),
            confidentiality_level=_safe_text(
                document_payload.get("confidentiality_level"),
                default="internal",
            ),
            status=_safe_text(document_payload.get("status"), default="active"),
            metadata_json={**metadata, "version_status": "active"},
        )
        self.db.add(document)
        self.db.flush()

        version = DocumentVersion(
            document_id=document.id,
            version_name=_safe_text(version_payload.get("version_name"), default="test-smoke-v1"),
            version_number=_safe_text(version_payload.get("version_number"), default="v1"),
            file_hash=_safe_text(version_payload.get("file_hash"), default="redacted-file-hash"),
            content_hash=_safe_text(
                version_payload.get("content_hash"),
                default=fingerprint,
            ),
            is_latest=True,
            parse_status=_safe_text(version_payload.get("parse_status"), default="parsed"),
            metadata_json={**metadata, "version_status": "active"},
        )
        self.db.add(version)
        self.db.flush()

        chunks: list[Chunk] = []
        citations: list[CitationRecord] = []
        for index, item in enumerate(chunks_payload):
            sanitized_text = _safe_text(item.get("sanitized_text"), default="")
            quote = _safe_text(item.get("sanitized_quote"), default=sanitized_text[:512])
            chunk = Chunk(
                document_id=document.id,
                version_id=version.id,
                chunk_index=_safe_int(item.get("chunk_index"), default=index),
                text=sanitized_text,
                heading_path=_optional_list(item.get("heading_path")),
                title_path=_optional_list(item.get("title_path")),
                section_path=_optional_list(item.get("section_path")),
                page_start=_optional_int(item.get("page_start")),
                page_end=_optional_int(item.get("page_end")),
                char_count=len(sanitized_text),
                content_hash=_safe_text(
                    item.get("content_hash"),
                    default=_hash_text(sanitized_text),
                ),
                token_count=_optional_int(item.get("token_count")),
                source_type=_safe_text(item.get("source_type"), default="platform_asset"),
                metadata_json={
                    **metadata,
                    "source_chunk_ref": _safe_text(item.get("chunk_ref"), default=f"chunk-{index}"),
                    "agent_answer_eligible": False,
                    "index_write_eligible": False,
                },
                embedding_id=None,
                sparse_id=None,
                permission_tags=_optional_list(item.get("permission_tags")),
            )
            self.db.add(chunk)
            self.db.flush()
            citation = CitationRecord(
                document_id=document.id,
                version_id=version.id,
                chunk_id=chunk.id,
                source_name=document.title,
                source_uri=document.source_uri,
                page_start=chunk.page_start,
                page_end=chunk.page_end,
                heading_path=chunk.heading_path,
                quote_text=quote,
            )
            self.db.add(citation)
            chunks.append(chunk)
            citations.append(citation)
        return document, version, chunks, citations


def build_evidence_write_result(payload: dict[str, Any]) -> dict[str, Any]:
    forbidden_keys = sorted(_find_forbidden_keys(payload))
    fingerprint = _fingerprint(payload)
    idempotency = _mapping(payload.get("idempotency"))
    idempotency_key = _safe_text(idempotency.get("idempotency_key"), default="")
    chunks = _list_of_mappings(payload.get("chunks"))
    gates = _gates(payload, chunks, idempotency_key)
    reasons = _reason_codes(gates)
    reasons.extend(f"forbidden_input_key_{key}" for key in forbidden_keys)

    state = "evidence_write_ready" if all(gates.values()) and not forbidden_keys else "evidence_write_not_allowed"
    if forbidden_keys:
        state = "evidence_write_no_go"

    return {
        "evidence_write_version": EVIDENCE_WRITE_VERSION,
        "dry_run": False,
        "test_db_session_only": True,
        "runtime_wiring_enabled": False,
        "decision": {
            "state": state,
            "reasons": reasons or ["all_evidence_write_gates_passed"],
        },
        "idempotency": {
            "idempotency_key": idempotency_key or "missing",
            "payload_fingerprint": fingerprint,
            "status": "not_registered",
            "duplicates_detected": 0,
            "idempotency_conflict": False,
        },
        "writes": _empty_writes(),
        "created_ids": {
            "document_id": "",
            "version_id": "",
            "chunk_ids": [],
            "citation_ids": [],
        },
        "rollback": {
            "rollback_dry_run_ref": _safe_text(payload.get("rollback_dry_run_ref"), default=""),
            "rollback_plan_available": bool(payload.get("rollback_dry_run_ref")),
            "rollback_scope": "same_write_run_only",
            "delete_rows": False,
            "executable": False,
        },
        "safety": _safety(db_writes=False),
    }


def _gates(
    payload: dict[str, Any],
    chunks: list[dict[str, Any]],
    idempotency_key: str,
) -> dict[str, bool]:
    flags = _mapping(payload.get("feature_flags"))
    approval = _mapping(payload.get("operator_approval"))
    return {
        "payload_version_supported": payload.get("payload_version") == PAYLOAD_VERSION,
        "real_evidence_write_enabled": flags.get("PLATFORM_ASSET_REAL_EVIDENCE_WRITE_ENABLED") is True,
        "real_evidence_write_smoke_enabled": (
            flags.get("PLATFORM_ASSET_REAL_EVIDENCE_WRITE_SMOKE_ENABLED") is True
        ),
        "agent_answer_integration_disabled": (
            flags.get("PLATFORM_ASSET_AGENT_ANSWER_INTEGRATION_ENABLED") is False
        ),
        "index_write_disabled": flags.get("PLATFORM_ASSET_INDEX_WRITE_ENABLED") is False,
        "operator_approval_present": bool(approval),
        "operator_writes_authorized": approval.get("writes_authorized") is True,
        "target_environment_test_machine_only": (
            payload.get("target_environment") == "test_machine_only"
            and approval.get("target_environment") == "test_machine_only"
        ),
        "write_run_id_present": bool(_safe_text(payload.get("write_run_id"), default="")),
        "write_run_id_matches_approval": (
            payload.get("write_run_id") == approval.get("write_run_id")
        ),
        "source_asset_ref_matches_approval": (
            payload.get("source_asset_ref") == approval.get("source_asset_ref")
        ),
        "project_scope_matches_approval": (
            payload.get("project_scope") == approval.get("project_scope")
        ),
        "permission_proof_ref_present": bool(
            _safe_text(payload.get("permission_proof_ref"), default="")
        ),
        "permission_proof_ref_matches_approval": (
            payload.get("permission_proof_ref") == approval.get("permission_proof_ref")
        ),
        "rollback_dry_run_ref_present": bool(
            _safe_text(payload.get("rollback_dry_run_ref"), default="")
        ),
        "rollback_dry_run_ref_matches_approval": (
            payload.get("rollback_dry_run_ref") == approval.get("rollback_dry_run_ref")
        ),
        "max_documents_one": approval.get("max_documents") == 1,
        "max_document_versions_one": approval.get("max_document_versions") == 1,
        "max_chunks_within_limit": approval.get("max_chunks") == 20,
        "chunk_limit_not_exceeded": len(chunks) <= 20,
        "chunks_present": bool(chunks),
        "chunks_sanitized_text_present": all(
            bool(_safe_text(chunk.get("sanitized_text"), default="")) for chunk in chunks
        ),
        "idempotency_key_present": bool(idempotency_key),
    }


def _run_metadata(payload: dict[str, Any], fingerprint: str) -> dict[str, Any]:
    approval = _mapping(payload.get("operator_approval"))
    idempotency = _mapping(payload.get("idempotency"))
    return {
        "source_system": _safe_text(payload.get("source_system"), default="platform_asset_catalog"),
        "source_asset_ref": _safe_text(payload.get("source_asset_ref"), default=""),
        "project_scope": _safe_text(payload.get("project_scope"), default=""),
        "permission_proof_ref": _safe_text(payload.get("permission_proof_ref"), default=""),
        "operator_approval_id": _safe_text(approval.get("approval_id"), default=""),
        "write_run_id": _safe_text(payload.get("write_run_id"), default=""),
        "evidence_write_idempotency_key": _safe_text(
            idempotency.get("idempotency_key"),
            default="",
        ),
        "evidence_write_payload_fingerprint": fingerprint,
        "evidence_write_smoke": True,
        "agent_answer_eligible": False,
        "index_write_eligible": False,
    }


def _rows_with_run_id(rows: list[Any], write_run_id: str) -> list[Any]:
    return [
        row
        for row in rows
        if (getattr(row, "metadata_json", None) or {}).get("write_run_id") == write_run_id
    ]


def _safety(*, db_writes: bool) -> dict[str, bool]:
    return {
        "documents_written": db_writes,
        "document_versions_written": db_writes,
        "chunks_written": db_writes,
        "citations_written": db_writes,
        "db_writes": db_writes,
        "test_db_session_only": True,
        "real_db_writes": False,
        "audit_table_writes": False,
        "opensearch_writes": False,
        "qdrant_writes": False,
        "minio_writes": False,
        "parser_invoked": False,
        "file_copied": False,
        "raw_content_read": False,
        "nas_scanned": False,
        "agent_answer_integration": False,
        "production_rollout": False,
    }


def _empty_writes() -> dict[str, int]:
    return {
        "documents": 0,
        "document_versions": 0,
        "chunks": 0,
        "citations": 0,
    }


def _reason_codes(gates: dict[str, bool]) -> list[str]:
    reasons: list[str] = []
    for name, passed in gates.items():
        if passed:
            continue
        if name == "chunk_limit_not_exceeded":
            reasons.append("chunk_limit_exceeded")
        else:
            reasons.append(f"{name}_missing")
    return reasons


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


def _fingerprint(value: Any) -> str:
    return hashlib.sha256(_canonical_json(value).encode("utf-8")).hexdigest()


def _hash_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _mapping(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _list_of_mappings(value: Any) -> list[dict[str, Any]]:
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, dict)]


def _safe_text(value: Any, *, default: str) -> str:
    if value is None:
        return default
    text = str(value).strip()
    return text or default


def _safe_int(value: Any, *, default: int) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _optional_int(value: Any) -> int | None:
    if value is None:
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _optional_list(value: Any) -> list[Any] | None:
    return value if isinstance(value, list) else None
