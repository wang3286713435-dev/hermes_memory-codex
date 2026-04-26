from pathlib import Path
import importlib.util

import pytest
import app.models  # noqa: F401
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings
from app.db.base import Base
from app.models.chunk import Chunk
from app.models.document import Document, DocumentVersion
from app.schemas.documents import DocumentIngestRequest
from app.services.indexing.dense import DenseChunkIndexer, DenseIndexingSummary
from app.services.ingestion.service import DocumentIngestionService
from app.services.storage.service import StoredFile

_BACKFILL_SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "phase216_dense_backfill.py"
_spec = importlib.util.spec_from_file_location("phase216_dense_backfill", _BACKFILL_SCRIPT)
_backfill_module = importlib.util.module_from_spec(_spec)
assert _spec and _spec.loader
_spec.loader.exec_module(_backfill_module)
build_parser = _backfill_module.build_parser


VECTOR = [0.01] * 1024


class FakeEmbedding:
    def embed_query(self, _text):
        return type(
            "EmbeddingOutcome",
            (),
            {"vector": VECTOR, "status": "executed", "trace": {"provider": "fake"}},
        )()


class FakeQdrant:
    def __init__(self):
        self.upserts = []

    def upsert_chunk(self, *, chunk_id, vector, payload):
        self.upserts.append({"chunk_id": chunk_id, "vector": vector, "payload": payload})
        return {"status": "completed"}


class FakeOpenSearchChunkIndexer:
    def index_chunk(self, _chunk, _document, _version) -> bool:
        return True


def test_dense_indexer_upserts_required_payload(monkeypatch):
    monkeypatch.setattr(settings, "vector_store_provider", "qdrant")
    qdrant = FakeQdrant()
    document = Document(id="doc-1", title="主标书", source_type="tender", source_uri="main.docx")
    version = DocumentVersion(id="ver-1", document_id="doc-1", version_name="v1", is_latest=True)
    chunk = Chunk(
        id="11111111-1111-1111-1111-111111111111",
        document_id="doc-1",
        version_id="ver-1",
        chunk_index=3,
        text="总工期要求",
        heading_path=["投标人须知前附表"],
        title_path=["投标人须知前附表"],
        section_path=["工期要求"],
        page_start=1,
        page_end=1,
        char_count=5,
        token_count=5,
        content_hash="hash",
        source_type="tender",
        metadata_json={"section": "schedule"},
    )

    summary = DenseChunkIndexer(embedding=FakeEmbedding(), qdrant=qdrant).index_chunks([chunk], document, version)

    assert summary.status == "executed"
    assert summary.indexed_count == 1
    payload = qdrant.upserts[0]["payload"]
    assert payload["document_id"] == "doc-1"
    assert payload["version_id"] == "ver-1"
    assert payload["chunk_id"] == chunk.id
    assert payload["source_type"] == "tender"
    assert payload["document_type"] is None
    assert payload["source_name"] == "主标书"
    assert payload["chunk_index"] == 3
    assert chunk.embedding_id == chunk.id


def test_ingestion_records_dense_summary_and_embedding_id(tmp_path: Path, monkeypatch):
    db_session = _db_session()
    try:
        source = tmp_path / "sample.txt"
        source.write_text("第一段\n第二段", encoding="utf-8")
        monkeypatch.setattr("app.services.ingestion.service.OpenSearchChunkIndexer", lambda: FakeOpenSearchChunkIndexer())
        monkeypatch.setattr("app.services.ingestion.service.DenseChunkIndexer", lambda: _FakeDenseChunkIndexer())

        job = DocumentIngestionService(db_session).ingest_uploaded_file(
            DocumentIngestRequest(source_uri=source.name, title="sample", source_type="manual", document_type="txt"),
            StoredFile(storage_uri=str(source), local_path=source, file_name=source.name, content_type="text/plain"),
        )

        assert job.status == "completed"
        version = db_session.get(DocumentVersion, job.version_id)
        chunks = db_session.query(Chunk).filter(Chunk.document_id == job.document_id).all()
        assert version.metadata_json["dense_ingestion"]["status"] == "executed"
        assert version.metadata_json["dense_ingestion"]["indexed_count"] == len(chunks)
        assert all(chunk.embedding_id == chunk.id for chunk in chunks)
    finally:
        db_session.close()


def test_ingestion_dense_failure_is_fail_open(tmp_path: Path, monkeypatch):
    db_session = _db_session()
    try:
        source = tmp_path / "sample.txt"
        source.write_text("第一段\n第二段", encoding="utf-8")
        monkeypatch.setattr("app.services.ingestion.service.OpenSearchChunkIndexer", lambda: FakeOpenSearchChunkIndexer())
        monkeypatch.setattr("app.services.ingestion.service.DenseChunkIndexer", lambda: _ExplodingDenseChunkIndexer())

        job = DocumentIngestionService(db_session).ingest_uploaded_file(
            DocumentIngestRequest(source_uri=source.name, title="sample", source_type="manual", document_type="txt"),
            StoredFile(storage_uri=str(source), local_path=source, file_name=source.name, content_type="text/plain"),
        )

        assert job.status == "completed"
        version = db_session.get(DocumentVersion, job.version_id)
        assert version.metadata_json["dense_ingestion"]["status"] == "failed"
        assert version.metadata_json["dense_ingestion"]["failed_count"] == job.chunk_count
    finally:
        db_session.close()


def test_backfill_requires_explicit_document_id():
    with pytest.raises(SystemExit):
        build_parser().parse_args([])


def test_backfill_dry_run_reports_attempted_and_duration(monkeypatch):
    class FakeSession:
        def get(self, _model, _document_id):
            return None

        def close(self):
            return None

    monkeypatch.setattr(_backfill_module, "SessionLocal", lambda: FakeSession())
    summary = _backfill_module.backfill_documents(["missing-doc"], dry_run=True)

    assert summary["documents"][0]["status"] == "not_found"
    assert "duration_ms" in summary["documents"][0]


class _FakeDenseChunkIndexer:
    def index_chunks(self, chunks, _document, _version):
        for chunk in chunks:
            chunk.embedding_id = chunk.id
        return DenseIndexingSummary(status="executed", indexed_count=len(chunks), qdrant_collection="test")


class _ExplodingDenseChunkIndexer:
    def index_chunks(self, _chunks, _document, _version):
        raise RuntimeError("qdrant down")


def _db_session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)()
