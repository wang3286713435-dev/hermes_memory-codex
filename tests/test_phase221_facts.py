from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.base import Base
from app.models.audit import AuditLog
from app.models.chunk import Chunk
from app.models.document import Document, DocumentVersion
from app.services.facts import FactService, FactValidationError


def test_fact_creation_requires_source_chunk(tmp_path):
    db = _db_session(tmp_path)
    service = FactService(db)

    try:
        service.create_fact_from_evidence(
            fact_type="meeting_action_item",
            subject="王工",
            predicate="负责",
            value="整理风险清单",
            source_chunk_id="",
        )
    except FactValidationError as exc:
        assert str(exc) == "source_chunk_id_required"
    else:  # pragma: no cover
        raise AssertionError("fact without source_chunk_id should fail")


def test_fact_creation_defaults_unverified_and_binds_evidence(tmp_path):
    db = _db_session(tmp_path)
    chunk = _seed_document_chunk(db)
    audit = _seed_audit(db)

    fact = FactService(db).create_fact_from_evidence(
        fact_type="tender_basic_info",
        subject="主标书",
        predicate="建设单位",
        value="深圳市福升建设开发有限公司",
        source_chunk_id=chunk.id,
        confidence=0.92,
        created_by="tester",
        audit_event_id=audit.id,
    )

    assert fact.verification_status == "unverified"
    assert fact.source_document_id == chunk.document_id
    assert fact.source_version_id == chunk.version_id
    assert fact.source_chunk_id == chunk.id
    assert fact.audit_event_id == audit.id

    fact_audit = db.query(AuditLog).filter(AuditLog.action == "fact.create").one()
    assert fact_audit.result_json["verification_status"] == "unverified"
    assert fact_audit.request_json["source_chunk_id"] == chunk.id


def test_stale_source_version_is_reported_when_listing_by_document(tmp_path):
    db = _db_session(tmp_path)
    old_chunk = _seed_document_chunk(db, version_id="version-old", is_latest=False)
    _seed_version(db, document_id=old_chunk.document_id, version_id="version-new", is_latest=True)

    fact = FactService(db).create_fact_from_evidence(
        fact_type="tender_basic_info",
        subject="版本测试",
        predicate="金额",
        value="100 万元",
        source_chunk_id=old_chunk.id,
    )

    views = FactService(db).list_facts_by_document(old_chunk.document_id)
    assert [view.fact.id for view in views] == [fact.id]
    assert views[0].source_version_is_latest is False
    assert views[0].stale_source_version is True


def test_list_facts_by_subject_and_confirm_reject(tmp_path):
    db = _db_session(tmp_path)
    chunk = _seed_document_chunk(db)
    service = FactService(db)
    fact = service.create_fact_from_evidence(
        fact_type="meeting_action_item",
        subject="建军",
        predicate="负责",
        value="复核模型清单",
        source_chunk_id=chunk.id,
    )

    views = service.list_facts_by_subject("建军")
    assert [view.fact.id for view in views] == [fact.id]

    confirmed = service.confirm_fact(fact.id, actor_id="reviewer")
    assert confirmed.verification_status == "confirmed"
    assert confirmed.confirmed_by == "reviewer"

    rejected = service.mark_fact_rejected(fact.id, actor_id="reviewer")
    assert rejected.verification_status == "rejected"
    assert rejected.confirmed_by is None


def _db_session(tmp_path):
    engine = create_engine(f"sqlite:///{tmp_path / 'facts.db'}")
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)()


def _seed_document_chunk(
    db,
    *,
    document_id: str = "doc-1",
    version_id: str = "version-1",
    chunk_id: str = "chunk-1",
    is_latest: bool = True,
) -> Chunk:
    if db.get(Document, document_id) is None:
        db.add(
            Document(
                id=document_id,
                title="测试文件",
                source_type="tender",
                source_uri="test.docx",
                document_type="tender",
                metadata_json={},
            )
        )
    _seed_version(db, document_id=document_id, version_id=version_id, is_latest=is_latest)
    chunk = Chunk(
        id=chunk_id,
        document_id=document_id,
        version_id=version_id,
        chunk_index=0,
        text="事实来源 chunk",
        heading_path=[],
        title_path=[],
        section_path=[],
        page_start=None,
        page_end=None,
        char_count=8,
        content_hash=f"hash-{chunk_id}",
        token_count=None,
        source_type="tender",
        metadata_json={},
        permission_tags=[],
    )
    db.merge(chunk)
    db.commit()
    return chunk


def _seed_version(db, *, document_id: str, version_id: str, is_latest: bool) -> None:
    db.merge(
        DocumentVersion(
            id=version_id,
            document_id=document_id,
            version_name="v1",
            is_latest=is_latest,
            parse_status="completed",
            metadata_json={"version_status": "active" if is_latest else "superseded"},
        )
    )
    db.commit()


def _seed_audit(db) -> AuditLog:
    audit = AuditLog(
        trace_id="trace-1",
        user_id="tester",
        action="retrieval.query",
        resource_type="retrieval",
        resource_id="trace-1",
        request_json={"query": "建设单位"},
        result_json={"evidence_chunk_ids": ["chunk-1"]},
    )
    db.add(audit)
    db.commit()
    db.refresh(audit)
    return audit
