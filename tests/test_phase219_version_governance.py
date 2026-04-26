from pathlib import Path

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.base import Base
from app.models.audit import AuditLog
from app.models.chunk import Chunk
from app.models.document import DocumentVersion
from app.schemas.documents import DocumentIngestRequest
from app.schemas.retrieval import RetrievalFilter, SearchRequest
from app.services.indexing.dense import DenseIndexingSummary
from app.services.ingestion.service import DocumentIngestionService
from app.services.retrieval.dense import QdrantDenseRetriever
from app.services.retrieval.service import RetrievalService
from app.services.storage.service import StoredFile


class FakeOpenSearchChunkIndexer:
    marked_versions: list[dict] = []

    def index_chunk(self, _chunk, _document, _version) -> bool:
        return True

    def mark_version_latest(
        self,
        version_id: str,
        *,
        is_latest: bool,
        document_id: str | None = None,
        superseded_by_version_id: str | None = None,
    ) -> None:
        self.marked_versions.append(
            {
                "version_id": version_id,
                "is_latest": is_latest,
                "document_id": document_id,
                "superseded_by_version_id": superseded_by_version_id,
            }
        )


class FakeDenseChunkIndexer:
    marked_versions: list[dict] = []

    def index_chunks(self, chunks, _document, _version) -> DenseIndexingSummary:
        for chunk in chunks:
            chunk.embedding_id = chunk.id
        return DenseIndexingSummary(status="executed", indexed_count=len(chunks), qdrant_collection="test")

    def mark_version_latest(
        self,
        version_id: str,
        *,
        is_latest: bool,
        document_id: str | None = None,
        superseded_by_version_id: str | None = None,
    ) -> None:
        self.marked_versions.append(
            {
                "version_id": version_id,
                "is_latest": is_latest,
                "document_id": document_id,
                "superseded_by_version_id": superseded_by_version_id,
            }
        )


@pytest.fixture()
def db_session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    session = sessionmaker(bind=engine)()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture(autouse=True)
def fake_indexers(monkeypatch):
    FakeOpenSearchChunkIndexer.marked_versions = []
    FakeDenseChunkIndexer.marked_versions = []
    monkeypatch.setattr("app.services.ingestion.service.OpenSearchChunkIndexer", lambda: FakeOpenSearchChunkIndexer())
    monkeypatch.setattr("app.services.ingestion.service.DenseChunkIndexer", lambda: FakeDenseChunkIndexer())


def test_new_same_title_upload_supersedes_previous_version(tmp_path: Path, db_session):
    v1 = _ingest_text(db_session, tmp_path, "交付标准", "旧版本关键条款")
    v2 = _ingest_text(db_session, tmp_path, "交付标准", "新版本关键条款")

    assert v1.document_id == v2.document_id
    old_version = db_session.get(DocumentVersion, v1.version_id)
    new_version = db_session.get(DocumentVersion, v2.version_id)
    assert old_version.is_latest is False
    assert old_version.metadata_json["version_status"] == "superseded"
    assert old_version.metadata_json["superseded_by_version_id"] == new_version.id
    assert new_version.is_latest is True
    assert new_version.metadata_json["version_status"] == "active"
    assert FakeOpenSearchChunkIndexer.marked_versions == [
        {
            "version_id": old_version.id,
            "is_latest": False,
            "document_id": v1.document_id,
            "superseded_by_version_id": v2.version_id,
        }
    ]
    assert FakeDenseChunkIndexer.marked_versions == [
        {
            "version_id": old_version.id,
            "is_latest": False,
            "document_id": v1.document_id,
            "superseded_by_version_id": v2.version_id,
        }
    ]


def test_default_retrieval_returns_only_latest_and_explicit_version_returns_history(tmp_path: Path, db_session):
    v1 = _ingest_text(db_session, tmp_path, "版本测试", "共同关键词 旧版本内容")
    v2 = _ingest_text(db_session, tmp_path, "版本测试", "共同关键词 新版本内容")

    service = RetrievalService(db_session)

    latest_response = service.search(
        SearchRequest(
            query="共同关键词",
            retrieval_mode="sparse",
            enable_dense=False,
            filters=RetrievalFilter(document_id=v2.document_id),
        )
    )
    assert latest_response.results
    assert {result.version_id for result in latest_response.results} == {v2.version_id}
    assert latest_response.trace["version_policy"] == "latest_only"

    historical_response = service.search(
        SearchRequest(
            query="共同关键词",
            retrieval_mode="sparse",
            enable_dense=False,
            filters=RetrievalFilter(document_id=v1.document_id, extra={"version_id": v1.version_id}),
        )
    )
    assert historical_response.results
    assert {result.version_id for result in historical_response.results} == {v1.version_id}
    assert historical_response.trace["version_scope"]["stale_version"] is True
    assert historical_response.trace["version_scope"]["latest_version_id"] == v2.version_id


def test_audit_log_records_evidence_version_ids(tmp_path: Path, db_session):
    job = _ingest_text(db_session, tmp_path, "审计版本", "审计关键词 最新内容")

    response = RetrievalService(db_session).search(
        SearchRequest(
            query="审计关键词",
            retrieval_mode="sparse",
            enable_dense=False,
            filters=RetrievalFilter(document_id=job.document_id),
        )
    )

    assert response.results
    event = db_session.query(AuditLog).filter(AuditLog.action == "retrieval.query").one()
    assert event.result_json["version_ids"] == [job.version_id]
    assert event.result_json["evidence_version_ids"] == [job.version_id]


def test_opensearch_default_filter_requires_latest(monkeypatch):
    captured: dict = {}

    class FakeIndices:
        def get_mapping(self, index):
            return {index: {"mappings": {"properties": {}}}}

    class FakeOpenSearch:
        indices = FakeIndices()

        def __init__(self, *_args, **_kwargs):
            pass

        def search(self, *, index, body):
            captured["body"] = body
            return {"hits": {"hits": []}}

    monkeypatch.setattr("app.services.retrieval.service.OpenSearch", FakeOpenSearch)
    service = RetrievalService(db=None)
    monkeypatch.setattr(service, "_write_log", lambda *args, **kwargs: None)
    service.search(SearchRequest(query="版本", retrieval_mode="sparse", enable_dense=False))

    filters = captured["body"]["query"]["bool"]["filter"]
    assert {"term": {"is_latest": True}} in filters


def test_opensearch_explicit_history_version_omits_active_status_filter(monkeypatch):
    captured: dict = {}

    class FakeIndices:
        def get_mapping(self, index):
            return {index: {"mappings": {"properties": {}}}}

    class FakeOpenSearch:
        indices = FakeIndices()

        def __init__(self, *_args, **_kwargs):
            pass

        def search(self, *, index, body):
            captured["body"] = body
            return {"hits": {"hits": []}}

    monkeypatch.setattr("app.services.retrieval.service.OpenSearch", FakeOpenSearch)
    service = RetrievalService(db=None)
    monkeypatch.setattr(service, "_write_log", lambda *args, **kwargs: None)
    service.search(
        SearchRequest(
            query="版本",
            retrieval_mode="sparse",
            enable_dense=False,
            filters=RetrievalFilter(document_id="doc-1", extra={"version_id": "old-version"}),
        )
    )

    filters = captured["body"]["query"]["bool"]["filter"]
    assert {"term": {"status": "active"}} not in filters
    assert {"term": {"version_id": "old-version"}} in filters


def test_opensearch_superseded_update_is_limited_to_document_and_version(monkeypatch):
    captured: dict = {}

    class FakeIndices:
        def exists(self, index):
            return True

        def get_mapping(self, index):
            return {
                index: {
                    "mappings": {
                        "properties": {
                            "title_path": {},
                            "section_path": {},
                            "document_id": {"type": "text", "fields": {"keyword": {"type": "keyword"}}},
                            "version_id": {"type": "text", "fields": {"keyword": {"type": "keyword"}}},
                        }
                    }
                }
            }

    class FakeClient:
        indices = FakeIndices()

        def __init__(self, *_args, **_kwargs):
            pass

        def update_by_query(self, **kwargs):
            captured.update(kwargs)

    monkeypatch.setattr("app.services.indexing.opensearch.OpenSearch", FakeClient)
    from app.services.indexing.opensearch import OpenSearchChunkIndexer

    OpenSearchChunkIndexer().mark_version_latest(
        "old-version",
        is_latest=False,
        document_id="doc-1",
        superseded_by_version_id="new-version",
    )

    body = captured["body"]
    filters = body["query"]["bool"]["filter"]
    assert {"term": {"version_id.keyword": "old-version"}} in filters
    assert {"term": {"document_id.keyword": "doc-1"}} in filters
    assert "ctx._source.status = params.status" in body["script"]["source"]
    assert body["script"]["params"]["status"] == "superseded"
    assert body["script"]["params"]["superseded_by_version_id"] == "new-version"


def test_qdrant_filter_supports_version_id():
    dense = QdrantDenseRetriever()
    qdrant_filter = dense._build_filter({"document_id": "doc-1", "version_id": "ver-1", "is_latest": True})

    assert {"key": "version_id", "match": {"value": "ver-1"}} in qdrant_filter["must"]


def _ingest_text(db_session, tmp_path: Path, title: str, text: str):
    path = tmp_path / f"{title}-{abs(hash(text))}.txt"
    path.write_text(text, encoding="utf-8")
    return DocumentIngestionService(db_session).ingest_uploaded_file(
        DocumentIngestRequest(source_uri=path.name, title=title, source_type="enterprise", document_type="txt"),
        StoredFile(storage_uri=str(path), local_path=path, file_name=path.name, content_type="text/plain"),
    )
