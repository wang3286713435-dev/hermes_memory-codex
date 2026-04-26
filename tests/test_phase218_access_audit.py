from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.base import Base
from app.models.audit import AuditLog
from app.models.document import Document
from app.schemas.retrieval import RetrievalFilter, SearchRequest, SearchResult
from app.services.retrieval.service import RetrievalService


def _db_session(tmp_path):
    engine = create_engine(f"sqlite:///{tmp_path / 'access_audit.db'}")
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine)
    return SessionLocal()


def _document(db, document_id: str, metadata: dict | None = None):
    db.add(
        Document(
            id=document_id,
            title=f"{document_id}.docx",
            source_type="tender",
            source_uri=f"{document_id}.docx",
            document_type="tender",
            metadata_json=metadata or {},
        )
    )
    db.commit()


def _result(document_id: str, chunk_id: str = "chunk-1") -> SearchResult:
    return SearchResult(
        chunk_id=chunk_id,
        document_id=document_id,
        version_id="version-1",
        chunk_index=0,
        text="测试 evidence",
        score=1.0,
        source_name=f"{document_id}.docx",
        source_type="tender",
        retrieval_sources=["sparse"],
        scores={"sparse": 1.0},
    )


def _service_with_sparse(db, monkeypatch, results: list[SearchResult]) -> RetrievalService:
    service = RetrievalService(db=db)
    monkeypatch.setattr(service, "_execute_sparse_search", lambda *_args, **_kwargs: results)
    return service


def test_no_acl_defaults_allow_and_traces_not_configured(tmp_path, monkeypatch):
    db = _db_session(tmp_path)
    _document(db, "doc-open", metadata={})
    service = _service_with_sparse(db, monkeypatch, [_result("doc-open")])

    response = service.search(SearchRequest(query="查资质", retrieval_mode="sparse", enable_dense=False))

    assert [result.document_id for result in response.results] == ["doc-open"]
    assert response.trace["access_policy"]["policy_decision"] == "not_configured_allow"
    assert response.trace["access_policy"]["permission_trace_missing"] is True


def test_allowed_requester_id_allows_and_writes_audit(tmp_path, monkeypatch):
    db = _db_session(tmp_path)
    _document(db, "doc-user", metadata={"allowed_requester_ids": ["u-1"], "tenant_id": "t-1"})
    service = _service_with_sparse(db, monkeypatch, [_result("doc-user", "chunk-user")])

    response = service.search(
        SearchRequest(
            query="查资质",
            user_id="u-1",
            retrieval_mode="sparse",
            enable_dense=False,
            filters=RetrievalFilter(extra={"tenant_id": "t-1", "role": "staff"}),
        )
    )

    assert [result.document_id for result in response.results] == ["doc-user"]
    assert response.trace["access_policy"]["policy_decision"] == "allow"
    event = db.query(AuditLog).one()
    assert event.user_id == "u-1"
    assert event.request_json["query"] == "查资质"
    assert event.result_json["returned_document_ids"] == ["doc-user"]
    assert event.result_json["evidence_chunk_ids"] == ["chunk-user"]
    assert event.result_json["policy_decision"] == "allow"


def test_allowed_role_allows(tmp_path, monkeypatch):
    db = _db_session(tmp_path)
    _document(db, "doc-role", metadata={"allowed_roles": ["bid"], "tenant_id": "t-1"})
    service = _service_with_sparse(db, monkeypatch, [_result("doc-role")])

    response = service.search(
        SearchRequest(
            query="查资质",
            retrieval_mode="sparse",
            enable_dense=False,
            filters=RetrievalFilter(extra={"tenant_id": "t-1", "role": "bid"}),
        )
    )

    assert [result.document_id for result in response.results] == ["doc-role"]
    assert response.trace["access_policy"]["policy_reason"] == "role_allowed"


def test_tenant_mismatch_denies_document_evidence(tmp_path, monkeypatch):
    db = _db_session(tmp_path)
    _document(db, "doc-denied", metadata={"tenant_id": "tenant-a"})
    service = _service_with_sparse(db, monkeypatch, [_result("doc-denied")])

    response = service.search(
        SearchRequest(
            query="查资质",
            retrieval_mode="sparse",
            enable_dense=False,
            filters=RetrievalFilter(extra={"tenant_id": "tenant-b", "role": "staff"}),
        )
    )

    assert response.results == []
    assert response.trace["access_policy"]["policy_decision"] == "deny"
    assert response.trace["access_policy"]["denied_document_ids"] == ["doc-denied"]


def test_audit_write_failure_does_not_block_retrieval(tmp_path, monkeypatch):
    db = _db_session(tmp_path)
    _document(db, "doc-open", metadata={})
    service = _service_with_sparse(db, monkeypatch, [_result("doc-open")])

    def fail_audit(**_kwargs):
        raise RuntimeError("audit unavailable")

    monkeypatch.setattr(service, "_add_audit_event", fail_audit)
    response = service.search(SearchRequest(query="查资质", retrieval_mode="sparse", enable_dense=False))

    assert [result.document_id for result in response.results] == ["doc-open"]
