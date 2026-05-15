from __future__ import annotations

import hashlib
import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Protocol

REHEARSAL_VERSION = "nas_evidence_write_rehearsal.v0"
WRITE_DRY_RUN_VERSION = "nas_evidence_write_dry_run.v0"
SAFETY_FLAGS = (
    "parser_invoked",
    "file_copied",
    "raw_content_read",
    "nas_scanned",
    "documents_written",
    "document_versions_written",
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


class EvidenceWriteRehearsalStore(Protocol):
    backend: str

    def register(
        self,
        *,
        idempotency_key: str,
        fingerprint: str,
        documents: list[dict[str, Any]],
        document_versions: list[dict[str, Any]],
        chunks: list[dict[str, Any]],
        citations: list[dict[str, Any]],
    ) -> dict[str, Any]: ...


class InMemoryEvidenceWriteRehearsalStore:
    backend = "in_memory"

    def __init__(self) -> None:
        self._idempotency: dict[str, str] = {}
        self.documents: list[dict[str, Any]] = []
        self.document_versions: list[dict[str, Any]] = []
        self.chunks: list[dict[str, Any]] = []
        self.citations: list[dict[str, Any]] = []

    def register(
        self,
        *,
        idempotency_key: str,
        fingerprint: str,
        documents: list[dict[str, Any]],
        document_versions: list[dict[str, Any]],
        chunks: list[dict[str, Any]],
        citations: list[dict[str, Any]],
    ) -> dict[str, Any]:
        existing = self._idempotency.get(idempotency_key)
        if existing is None:
            self._idempotency[idempotency_key] = fingerprint
            self.documents.extend(documents)
            self.document_versions.extend(document_versions)
            self.chunks.extend(chunks)
            self.citations.extend(citations)
            return {
                "status": "created",
                "duplicates_detected": 0,
                "idempotency_conflict": False,
            }
        if existing == fingerprint:
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


class SQLiteEvidenceWriteRehearsalStore:
    backend = "sqlite"

    def __init__(self, path: Path) -> None:
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._connection = sqlite3.connect(str(path))
        self._create_schema()

    def register(
        self,
        *,
        idempotency_key: str,
        fingerprint: str,
        documents: list[dict[str, Any]],
        document_versions: list[dict[str, Any]],
        chunks: list[dict[str, Any]],
        citations: list[dict[str, Any]],
    ) -> dict[str, Any]:
        existing = self._connection.execute(
            "SELECT fingerprint FROM rehearsal_idempotency WHERE idempotency_key = ?",
            (idempotency_key,),
        ).fetchone()
        if existing is None:
            self._connection.execute(
                "INSERT INTO rehearsal_idempotency(idempotency_key, fingerprint) VALUES (?, ?)",
                (idempotency_key, fingerprint),
            )
            self._insert_payloads("rehearsal_documents", "ref", documents)
            self._insert_payloads("rehearsal_document_versions", "ref", document_versions)
            self._insert_payloads("rehearsal_chunks", "ref", chunks)
            self._insert_payloads("rehearsal_citations", "ref", citations)
            self._connection.commit()
            return {
                "status": "created",
                "duplicates_detected": 0,
                "idempotency_conflict": False,
            }
        if existing[0] == fingerprint:
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

    def _create_schema(self) -> None:
        self._connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS rehearsal_idempotency (
              idempotency_key TEXT PRIMARY KEY,
              fingerprint TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS rehearsal_documents (
              ref TEXT PRIMARY KEY,
              payload TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS rehearsal_document_versions (
              ref TEXT PRIMARY KEY,
              payload TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS rehearsal_chunks (
              ref TEXT PRIMARY KEY,
              payload TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS rehearsal_citations (
              ref TEXT PRIMARY KEY,
              payload TEXT NOT NULL
            );
            """
        )
        self._connection.commit()

    def _insert_payloads(
        self,
        table: str,
        ref_column: str,
        rows: list[dict[str, Any]],
    ) -> None:
        for row in rows:
            ref = _first_present_ref(row)
            self._connection.execute(
                f"INSERT OR IGNORE INTO {table}({ref_column}, payload) VALUES (?, ?)",
                (ref, _canonical_json(row)),
            )


def build_evidence_write_rehearsal_report(
    write_dry_run: dict[str, Any],
    *,
    created_at: str | None = None,
    store: EvidenceWriteRehearsalStore | None = None,
) -> dict[str, Any]:
    created = created_at or _utc_now()
    decision = _mapping(write_dry_run.get("decision"))
    safety = _mapping(write_dry_run.get("safety"))
    idempotency = _mapping(write_dry_run.get("idempotency"))
    simulated_documents = _list_of_mappings(write_dry_run.get("simulated_documents"))
    simulated_chunks = _list_of_mappings(write_dry_run.get("simulated_chunks"))
    simulated_citations = _list_of_mappings(write_dry_run.get("simulated_citations"))

    forbidden_keys = sorted(_find_forbidden_keys(write_dry_run))
    safety_reasons = _true_safety_reasons(write_dry_run)
    idempotency_key = _safe_text(idempotency.get("idempotency_key"), default="")
    fingerprint = _fingerprint(write_dry_run)

    gates = {
        "write_dry_run_version_supported": write_dry_run.get("write_dry_run_version")
        == WRITE_DRY_RUN_VERSION,
        "write_dry_run_go": decision.get("write_dry_run_state")
        == "write_dry_run_go",
        "write_dry_run_dry_run_true": write_dry_run.get("dry_run") is True,
        "write_dry_run_writes_authorized_false": (
            write_dry_run.get("writes_authorized") is False
        ),
        "write_dry_run_safety_flags_clear": not safety_reasons,
        "no_forbidden_input_keys": not forbidden_keys,
        "idempotency_key_present": bool(idempotency_key),
        "simulated_documents_present": bool(simulated_documents),
        "simulated_chunks_present": bool(simulated_chunks),
        "simulated_citations_present": bool(simulated_citations),
    }
    reasons = _reason_codes(gates)
    reasons.extend(safety_reasons)
    reasons.extend(f"forbidden_input_key_{key}" for key in forbidden_keys)

    rehearsal_documents: list[dict[str, Any]] = []
    rehearsal_document_versions: list[dict[str, Any]] = []
    rehearsal_chunks: list[dict[str, Any]] = []
    rehearsal_citations: list[dict[str, Any]] = []
    store_result = {
        "status": "not_registered",
        "duplicates_detected": 0,
        "idempotency_conflict": False,
    }
    state = "rehearsal_not_allowed"

    if safety_reasons or forbidden_keys:
        state = "rehearsal_no_go"
    elif all(gates.values()):
        (
            rehearsal_documents,
            rehearsal_document_versions,
            rehearsal_chunks,
            rehearsal_citations,
        ) = _build_rehearsal_records(
            write_dry_run=write_dry_run,
            simulated_documents=simulated_documents,
            simulated_chunks=simulated_chunks,
            simulated_citations=simulated_citations,
            idempotency_key=idempotency_key,
        )
        store_result = (store or InMemoryEvidenceWriteRehearsalStore()).register(
            idempotency_key=idempotency_key,
            fingerprint=fingerprint,
            documents=rehearsal_documents,
            document_versions=rehearsal_document_versions,
            chunks=rehearsal_chunks,
            citations=rehearsal_citations,
        )
        if store_result["idempotency_conflict"]:
            state = "rehearsal_no_go"
            reasons.append("idempotency_conflict")
            rehearsal_documents = []
            rehearsal_document_versions = []
            rehearsal_chunks = []
            rehearsal_citations = []
        else:
            state = "rehearsal_go"
            reasons = ["all_rehearsal_gates_passed"]
            if store_result["duplicates_detected"]:
                reasons.append("duplicate_rehearsal_detected")

    return {
        "rehearsal_version": REHEARSAL_VERSION,
        "run_id": _safe_text(write_dry_run.get("run_id"), default="redacted-write-dry-run"),
        "created_at": created,
        "write_dry_run_ref": {
            "write_dry_run_version": _safe_text(
                write_dry_run.get("write_dry_run_version"),
                default="unknown",
            ),
            "write_dry_run_run_id": _safe_text(
                write_dry_run.get("run_id"),
                default="redacted-write-dry-run",
            ),
            "write_dry_run_state": _safe_text(
                decision.get("write_dry_run_state"),
                default="unknown",
            ),
        },
        "temp_store": {
            "backend": (store.backend if store is not None else "in_memory"),
            "real_hermes_db_used": False,
            "platform_db_used": False,
            "opensearch_used": False,
            "qdrant_used": False,
            "minio_used": False,
        },
        "rehearsal_documents": rehearsal_documents,
        "rehearsal_document_versions": rehearsal_document_versions,
        "rehearsal_chunks": rehearsal_chunks,
        "rehearsal_citations": rehearsal_citations,
        "idempotency": {
            "idempotency_key": idempotency_key or "missing",
            "status": store_result["status"],
            "duplicates_detected": store_result["duplicates_detected"],
            "idempotency_conflict": store_result["idempotency_conflict"],
            "duplicate_write_allowed": False,
        },
        "rollback": _rollback(
            state,
            rehearsal_documents,
            rehearsal_document_versions,
            rehearsal_chunks,
            rehearsal_citations,
        ),
        "safety": _safety(),
        "dry_run": True,
        "writes_authorized": False,
        "decision": {
            "rehearsal_state": state,
            "reasons": reasons or ["rehearsal_not_allowed"],
        },
    }


def write_evidence_write_rehearsal_report(
    output_dir: Path,
    report: dict[str, Any],
) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / f"{_safe_filename(report.get('run_id'))}-rehearsal.json"
    path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return path


def _build_rehearsal_records(
    *,
    write_dry_run: dict[str, Any],
    simulated_documents: list[dict[str, Any]],
    simulated_chunks: list[dict[str, Any]],
    simulated_citations: list[dict[str, Any]],
    idempotency_key: str,
) -> tuple[
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
]:
    run_id = _safe_text(write_dry_run.get("run_id"), default="redacted-write-dry-run")
    documents: list[dict[str, Any]] = []
    versions: list[dict[str, Any]] = []
    chunks: list[dict[str, Any]] = []
    citations: list[dict[str, Any]] = []

    for document in simulated_documents:
        simulated_document_ref = _safe_text(
            document.get("simulated_document_ref"),
            default="missing-simdoc",
        )
        rehearsal_document_ref = _rehearsal_ref(
            "rehearsal_doc",
            run_id,
            simulated_document_ref,
        )
        candidate_version_ref = _safe_text(
            document.get("candidate_version_ref"),
            default="missing-simver",
        )
        rehearsal_version_ref = _rehearsal_ref(
            "rehearsal_ver",
            rehearsal_document_ref,
            candidate_version_ref,
        )
        documents.append(
            {
                "rehearsal_document_ref": rehearsal_document_ref,
                "simulated_document_ref": simulated_document_ref,
                "external_asset_ref": _safe_text(
                    document.get("external_asset_ref"),
                    default="missing-external-asset",
                ),
                "source_catalog_ref": _safe_text(
                    document.get("source_catalog_ref"),
                    default="missing-source-catalog",
                ),
                "idempotency_key": idempotency_key,
                "temp_repository_only": True,
            }
        )
        versions.append(
            {
                "rehearsal_document_version_ref": rehearsal_version_ref,
                "rehearsal_document_ref": rehearsal_document_ref,
                "candidate_version_ref": candidate_version_ref,
                "simulated_document_ref": simulated_document_ref,
                "temp_repository_only": True,
            }
        )

    document_ref = (
        documents[0]["rehearsal_document_ref"] if documents else "missing-rehearsal-doc"
    )
    version_ref = (
        versions[0]["rehearsal_document_version_ref"]
        if versions
        else "missing-rehearsal-version"
    )
    for index, chunk in enumerate(simulated_chunks, start=1):
        simulated_chunk_ref = _safe_text(
            chunk.get("simulated_chunk_ref"),
            default=f"missing-simchunk-{index}",
        )
        rehearsal_chunk_ref = _rehearsal_ref(
            "rehearsal_chunk",
            version_ref,
            simulated_chunk_ref,
        )
        chunks.append(
            {
                "rehearsal_chunk_ref": rehearsal_chunk_ref,
                "rehearsal_document_ref": document_ref,
                "rehearsal_document_version_ref": version_ref,
                "simulated_chunk_ref": simulated_chunk_ref,
                "simulated_document_ref": _safe_text(
                    chunk.get("simulated_document_ref"),
                    default="missing-simdoc",
                ),
                "candidate_chunk_index": _safe_int(
                    chunk.get("candidate_chunk_index"),
                    default=index,
                ),
                "redacted_citation_anchor": _safe_text(
                    chunk.get("redacted_citation_anchor"),
                    default=f"redacted-anchor:{index:04d}",
                ),
                "source_catalog_ref": _safe_text(
                    chunk.get("source_catalog_ref"),
                    default="missing-source-catalog",
                ),
                "idempotency_key": idempotency_key,
                "temp_repository_only": True,
            }
        )

    for index, citation in enumerate(simulated_citations, start=1):
        simulated_chunk_ref = _safe_text(
            citation.get("simulated_chunk_ref"),
            default=f"missing-simchunk-{index}",
        )
        matching_chunk = next(
            (
                chunk
                for chunk in chunks
                if chunk["simulated_chunk_ref"] == simulated_chunk_ref
            ),
            chunks[min(index - 1, len(chunks) - 1)] if chunks else {},
        )
        rehearsal_citation_ref = _rehearsal_ref(
            "rehearsal_cite",
            matching_chunk.get("rehearsal_chunk_ref", "missing-rehearsal-chunk"),
            _safe_text(citation.get("redacted_citation_anchor"), default=str(index)),
        )
        citations.append(
            {
                "rehearsal_citation_ref": rehearsal_citation_ref,
                "rehearsal_chunk_ref": matching_chunk.get(
                    "rehearsal_chunk_ref",
                    "missing-rehearsal-chunk",
                ),
                "simulated_chunk_ref": simulated_chunk_ref,
                "source_asset_ref": _safe_text(
                    citation.get("source_asset_ref"),
                    default="missing-source-asset",
                ),
                "source_view": _safe_text(
                    citation.get("source_view"),
                    default="FileAssetView",
                ),
                "redacted_citation_anchor": _safe_text(
                    citation.get("redacted_citation_anchor"),
                    default=f"redacted-anchor:{index:04d}",
                ),
                "production_evidence": False,
                "temp_repository_only": True,
            }
        )
    return documents, versions, chunks, citations


def _rollback(
    state: str,
    documents: list[dict[str, Any]],
    versions: list[dict[str, Any]],
    chunks: list[dict[str, Any]],
    citations: list[dict[str, Any]],
) -> dict[str, Any]:
    refs: list[str] = []
    if state == "rehearsal_go":
        refs.extend(row["rehearsal_document_ref"] for row in documents)
        refs.extend(row["rehearsal_document_version_ref"] for row in versions)
        refs.extend(row["rehearsal_chunk_ref"] for row in chunks)
        refs.extend(row["rehearsal_citation_ref"] for row in citations)
    return {
        "rollback_plan_available": state == "rehearsal_go",
        "rollback_scope": "temp_rehearsal_only",
        "temp_refs_to_remove": refs,
        "source_data_mutation": False,
        "delete_original_nas_file": False,
        "delete_platform_db_record": False,
        "repair_backfill_reindex_cleanup": False,
    }


def _safety() -> dict[str, bool]:
    return {
        "documents_written": False,
        "document_versions_written": False,
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


def _canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _fingerprint(value: dict[str, Any]) -> str:
    return hashlib.sha256(_canonical_json(value).encode("utf-8")).hexdigest()


def _rehearsal_ref(prefix: str, *parts: str) -> str:
    return f"{prefix}_{hashlib.sha256('|'.join(parts).encode('utf-8')).hexdigest()[:24]}"


def _first_present_ref(row: dict[str, Any]) -> str:
    for key in (
        "rehearsal_document_ref",
        "rehearsal_document_version_ref",
        "rehearsal_chunk_ref",
        "rehearsal_citation_ref",
    ):
        value = row.get(key)
        if value:
            return str(value)
    return _rehearsal_ref("rehearsal_ref", _canonical_json(row))


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


def _true_safety_reasons(write_dry_run: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    if write_dry_run.get("writes_authorized") is True:
        reasons.append("writes_authorized_true")
    safety = _mapping(write_dry_run.get("safety"))
    for flag in SAFETY_FLAGS:
        if safety.get(flag) is True:
            reasons.append(f"{flag}_true")
    return reasons


def _reason_codes(gates: dict[str, bool]) -> list[str]:
    reason_names = {
        "write_dry_run_version_supported": "write_dry_run_version_unsupported",
        "write_dry_run_go": "write_dry_run_not_go",
        "write_dry_run_dry_run_true": "write_dry_run_dry_run_not_true",
        "write_dry_run_writes_authorized_false": "write_dry_run_writes_authorized_not_false",
        "write_dry_run_safety_flags_clear": "write_dry_run_safety_flags_not_clear",
        "no_forbidden_input_keys": "forbidden_input_keys_present",
        "idempotency_key_present": "idempotency_key_missing",
        "simulated_documents_present": "simulated_documents_missing",
        "simulated_chunks_present": "simulated_chunks_missing",
        "simulated_citations_present": "simulated_citations_missing",
    }
    return [reason_names[key] for key, value in gates.items() if not value]
