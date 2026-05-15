from __future__ import annotations

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.base import Base
from app.models.chunk import Chunk
from app.models.citation import CitationRecord
from app.models.document import Document, DocumentVersion


def _writer_module():
    from app.services.asset_catalog.evidence_writer import (
        EVIDENCE_WRITE_VERSION,
        EvidenceOnlyWriter,
        build_evidence_write_result,
    )

    return EVIDENCE_WRITE_VERSION, EvidenceOnlyWriter, build_evidence_write_result


def test_missing_approval_and_flags_fail_closed() -> None:
    _version, _writer_cls, build_result = _writer_module()
    payload = _ready_payload()
    payload["operator_approval"] = {}
    payload["feature_flags"]["PLATFORM_ASSET_REAL_EVIDENCE_WRITE_ENABLED"] = False

    result = build_result(payload)

    assert result["decision"]["state"] == "evidence_write_not_allowed"
    assert "operator_approval_present_missing" in result["decision"]["reasons"]
    assert "real_evidence_write_enabled_missing" in result["decision"]["reasons"]
    assert result["writes"]["documents"] == 0
    assert result["safety"]["db_writes"] is False


def test_payload_limits_fail_closed_without_writing() -> None:
    _version, writer_cls, _build_result = _writer_module()
    db = _db_session()
    payload = _ready_payload()
    payload["operator_approval"]["max_chunks"] = 20
    payload["chunks"] = [
        {
            **payload["chunks"][0],
            "chunk_index": index,
            "chunk_ref": f"chunk-{index}",
            "sanitized_text": f"sanitized chunk {index}",
            "sanitized_quote": f"sanitized quote {index}",
        }
        for index in range(21)
    ]

    result = writer_cls(db).write(payload)

    assert result["decision"]["state"] == "evidence_write_not_allowed"
    assert "chunk_limit_exceeded" in result["decision"]["reasons"]
    assert db.query(Document).count() == 0
    assert db.query(Chunk).count() == 0


def test_forbidden_raw_fields_fail_closed() -> None:
    _version, writer_cls, _build_result = _writer_module()
    db = _db_session()
    payload = _ready_payload()
    payload["chunks"][0]["raw_text"] = "do not write raw content"

    result = writer_cls(db).write(payload)

    assert result["decision"]["state"] == "evidence_write_no_go"
    assert "forbidden_input_key_raw_text" in result["decision"]["reasons"]
    assert db.query(Document).count() == 0


def test_successful_write_creates_test_db_document_version_chunks_and_citations() -> None:
    version, writer_cls, _build_result = _writer_module()
    db = _db_session()

    result = writer_cls(db).write(_ready_payload())

    assert version == "hermes_evidence_only_write.v0"
    assert result["decision"]["state"] == "evidence_write_go"
    assert result["writes"] == {
        "documents": 1,
        "document_versions": 1,
        "chunks": 2,
        "citations": 2,
    }
    assert result["safety"]["db_writes"] is True
    assert result["safety"]["opensearch_writes"] is False
    assert result["safety"]["qdrant_writes"] is False
    assert result["safety"]["minio_writes"] is False
    assert result["safety"]["parser_invoked"] is False
    assert result["safety"]["nas_scanned"] is False
    assert result["safety"]["agent_answer_integration"] is False

    document = db.query(Document).one()
    version_row = db.query(DocumentVersion).one()
    chunks = db.query(Chunk).order_by(Chunk.chunk_index).all()
    citations = db.query(CitationRecord).order_by(CitationRecord.page_start).all()

    assert document.title == "redacted evidence document"
    assert document.metadata_json["evidence_write_idempotency_key"] == "idem-001"
    assert version_row.document_id == document.id
    assert version_row.metadata_json["write_run_id"] == "write-run-001"
    assert version_row.metadata_json["evidence_write_smoke"] is True
    assert version_row.metadata_json["agent_answer_eligible"] is False
    assert version_row.metadata_json["index_write_eligible"] is False
    assert [chunk.text for chunk in chunks] == [
        "sanitized evidence chunk one",
        "sanitized evidence chunk two",
    ]
    assert chunks[0].metadata_json["source_asset_ref"] == "asset-ref-001"
    assert citations[0].chunk_id == chunks[0].id
    assert citations[0].quote_text == "sanitized quote one"


def test_same_idempotency_key_and_same_payload_is_duplicate_no_new_rows() -> None:
    _version, writer_cls, _build_result = _writer_module()
    db = _db_session()
    writer = writer_cls(db)

    first = writer.write(_ready_payload())
    second = writer.write(_ready_payload())

    assert first["decision"]["state"] == "evidence_write_go"
    assert second["decision"]["state"] == "evidence_write_duplicate"
    assert second["idempotency"]["duplicates_detected"] == 1
    assert db.query(Document).count() == 1
    assert db.query(Chunk).count() == 2


def test_same_idempotency_key_with_different_payload_is_conflict() -> None:
    _version, writer_cls, _build_result = _writer_module()
    db = _db_session()
    writer = writer_cls(db)
    writer.write(_ready_payload())
    conflicting = _ready_payload()
    conflicting["chunks"][0]["sanitized_text"] = "changed sanitized chunk"

    result = writer.write(conflicting)

    assert result["decision"]["state"] == "evidence_write_no_go"
    assert "idempotency_conflict" in result["decision"]["reasons"]
    assert result["idempotency"]["idempotency_conflict"] is True
    assert db.query(Document).count() == 1
    assert db.query(Chunk).count() == 2


def test_rollback_dry_run_lists_only_rows_created_by_write_run() -> None:
    _version, writer_cls, _build_result = _writer_module()
    db = _db_session()
    writer = writer_cls(db)
    writer.write(_ready_payload())
    other_payload = _ready_payload("write-run-002", "idem-002")
    writer.write(other_payload)

    plan = writer.build_rollback_dry_run("write-run-001")

    assert plan["dry_run"] is True
    assert plan["delete_rows"] is False
    assert plan["write_run_id"] == "write-run-001"
    assert plan["rows_by_model"].keys() == {
        "Document",
        "DocumentVersion",
        "Chunk",
        "CitationRecord",
    }
    assert len(plan["rows_by_model"]["Document"]) == 1
    assert len(plan["rows_by_model"]["DocumentVersion"]) == 1
    assert len(plan["rows_by_model"]["Chunk"]) == 2
    assert len(plan["rows_by_model"]["CitationRecord"]) == 2
    assert db.query(Document).count() == 2


def _db_session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)()


def _ready_payload(
    write_run_id: str = "write-run-001",
    idempotency_key: str = "idem-001",
) -> dict:
    return {
        "payload_version": "hermes_evidence_only_payload.v0",
        "target_environment": "test_machine_only",
        "feature_flags": {
            "PLATFORM_ASSET_REAL_EVIDENCE_WRITE_ENABLED": True,
            "PLATFORM_ASSET_REAL_EVIDENCE_WRITE_SMOKE_ENABLED": True,
            "PLATFORM_ASSET_AGENT_ANSWER_INTEGRATION_ENABLED": False,
            "PLATFORM_ASSET_INDEX_WRITE_ENABLED": False,
        },
        "operator_approval": {
            "approval_id": "approval-001",
            "writes_authorized": True,
            "target_environment": "test_machine_only",
            "write_run_id": write_run_id,
            "source_asset_ref": "asset-ref-001",
            "project_scope": "project-scope-001",
            "permission_proof_ref": "permission-proof-001",
            "rollback_dry_run_ref": "rollback-ref-001",
            "max_documents": 1,
            "max_document_versions": 1,
            "max_chunks": 20,
        },
        "write_run_id": write_run_id,
        "source_system": "platform_asset_catalog",
        "source_asset_ref": "asset-ref-001",
        "project_scope": "project-scope-001",
        "permission_proof_ref": "permission-proof-001",
        "rollback_dry_run_ref": "rollback-ref-001",
        "idempotency": {
            "idempotency_key": idempotency_key,
        },
        "document": {
            "title": "redacted evidence document",
            "source_type": "platform_asset",
            "source_uri": "asset-ref:asset-ref-001",
            "document_type": "sanitized_test_evidence",
            "confidentiality_level": "internal",
            "status": "active",
        },
        "document_version": {
            "version_name": "test-smoke-v1",
            "version_number": "v1",
            "file_hash": "redacted-file-hash",
            "content_hash": "redacted-content-hash",
            "parse_status": "parsed",
        },
        "chunks": [
            {
                "chunk_ref": "chunk-1",
                "chunk_index": 0,
                "sanitized_text": "sanitized evidence chunk one",
                "sanitized_quote": "sanitized quote one",
                "heading_path": ["redacted heading"],
                "page_start": 1,
                "page_end": 1,
                "content_hash": "chunk-hash-1",
                "source_type": "platform_asset",
                "permission_tags": ["project:project-scope-001"],
            },
            {
                "chunk_ref": "chunk-2",
                "chunk_index": 1,
                "sanitized_text": "sanitized evidence chunk two",
                "sanitized_quote": "sanitized quote two",
                "heading_path": ["redacted heading"],
                "page_start": 2,
                "page_end": 2,
                "content_hash": "chunk-hash-2",
                "source_type": "platform_asset",
                "permission_tags": ["project:project-scope-001"],
            },
        ],
    }
