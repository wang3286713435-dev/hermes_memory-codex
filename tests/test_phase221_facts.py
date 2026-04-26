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
    assert confirmed.confirmed_at is not None

    rejected = service.mark_fact_rejected(fact.id, actor_id="reviewer", rejection_reason="证据不足")
    assert rejected.verification_status == "rejected"
    assert rejected.confirmed_by is None
    assert rejected.confirmed_at is None
    assert rejected.rejected_by == "reviewer"
    assert rejected.rejected_at is not None
    assert rejected.rejection_reason == "证据不足"


def test_fact_confirm_requires_confirmed_by_and_writes_audit(tmp_path):
    db = _db_session(tmp_path)
    chunk = _seed_document_chunk(db)
    service = FactService(db)
    fact = service.create_fact_from_evidence(
        fact_type="meeting_action_item",
        subject="确认测试",
        predicate="负责",
        value="复核",
        source_chunk_id=chunk.id,
    )

    try:
        service.confirm_fact(fact.id)
    except FactValidationError as exc:
        assert str(exc) == "confirmed_by_required"
    else:  # pragma: no cover
        raise AssertionError("confirm without confirmed_by should fail")

    confirmed = service.confirm_fact(fact.id, confirmed_by="reviewer-a")

    assert confirmed.verification_status == "confirmed"
    assert confirmed.confirmed_by == "reviewer-a"
    assert confirmed.confirmed_at is not None
    event = _last_fact_status_audit(db, "fact.confirm")
    assert event.user_id == "reviewer-a"
    assert event.result_json["confirmed_by"] == "reviewer-a"
    assert event.result_json["confirmed_at"] is not None


def test_fact_reject_writes_reviewer_reason_and_audit(tmp_path):
    db = _db_session(tmp_path)
    chunk = _seed_document_chunk(db)
    service = FactService(db)
    fact = service.create_fact_from_evidence(
        fact_type="meeting_action_item",
        subject="拒绝测试",
        predicate="负责",
        value="复核",
        source_chunk_id=chunk.id,
    )

    rejected = service.reject_fact(fact.id, rejected_by="reviewer-b", rejection_reason="来源不足")

    assert rejected.verification_status == "rejected"
    assert rejected.rejected_by == "reviewer-b"
    assert rejected.rejected_at is not None
    assert rejected.rejection_reason == "来源不足"
    event = _last_fact_status_audit(db, "fact.reject")
    assert event.user_id == "reviewer-b"
    assert event.result_json["rejected_by"] == "reviewer-b"
    assert event.result_json["rejected_at"] is not None
    assert event.result_json["rejection_reason"] == "来源不足"


def test_fact_reject_requires_rejected_by_and_defaults_reason(tmp_path):
    db = _db_session(tmp_path)
    chunk = _seed_document_chunk(db)
    service = FactService(db)
    fact = service.create_fact_from_evidence(
        fact_type="meeting_action_item",
        subject="拒绝默认原因",
        predicate="负责",
        value="复核",
        source_chunk_id=chunk.id,
    )

    try:
        service.reject_fact(fact.id)
    except FactValidationError as exc:
        assert str(exc) == "rejected_by_required"
    else:  # pragma: no cover
        raise AssertionError("reject without rejected_by should fail")

    rejected = service.reject_fact(fact.id, rejected_by="reviewer-c")

    assert rejected.rejection_reason == "not_specified"


def test_rejected_fact_query_still_returns_when_policy_allows(tmp_path):
    db = _db_session(tmp_path)
    chunk = _seed_document_chunk(db)
    service = FactService(db)
    fact = service.create_fact_from_evidence(
        fact_type="meeting_action_item",
        subject="已拒绝仍可查",
        predicate="负责",
        value="复核",
        source_chunk_id=chunk.id,
    )
    service.reject_fact(fact.id, rejected_by="reviewer", rejection_reason="人工否决")

    views = service.list_facts_by_subject("已拒绝仍可查")

    assert [view.fact.id for view in views] == [fact.id]
    assert views[0].fact.verification_status == "rejected"


def test_fact_query_no_acl_defaults_not_configured_allow_and_audits(tmp_path):
    db = _db_session(tmp_path)
    chunk = _seed_document_chunk(db, metadata_json={})
    fact = FactService(db).create_fact_from_evidence(
        fact_type="tender_basic_info",
        subject="无权限配置",
        predicate="建设单位",
        value="测试单位",
        source_chunk_id=chunk.id,
    )

    views = FactService(db).list_facts_by_document(chunk.document_id)

    assert [view.fact.id for view in views] == [fact.id]
    event = _last_fact_query_audit(db)
    assert event.request_json["requester_id"] == "local_dev"
    assert event.request_json["tenant_id"] == "local_dev"
    assert event.result_json["returned_fact_ids"] == [fact.id]
    assert event.result_json["denied_fact_ids"] == []
    assert event.result_json["policy_decision"] == "not_configured_allow"


def test_fact_query_allows_requester_and_role(tmp_path):
    db = _db_session(tmp_path)
    requester_chunk = _seed_document_chunk(
        db,
        document_id="doc-requester",
        version_id="version-requester",
        chunk_id="chunk-requester",
        metadata_json={"allowed_requester_ids": ["u-1"], "tenant_id": "t-1"},
    )
    role_chunk = _seed_document_chunk(
        db,
        document_id="doc-role",
        version_id="version-role",
        chunk_id="chunk-role",
        metadata_json={"allowed_roles": ["bid"], "tenant_id": "t-1"},
    )
    service = FactService(db)
    requester_fact = service.create_fact_from_evidence(
        fact_type="tender_basic_info",
        subject="requester allow",
        predicate="值",
        value="A",
        source_chunk_id=requester_chunk.id,
    )
    role_fact = service.create_fact_from_evidence(
        fact_type="tender_basic_info",
        subject="role allow",
        predicate="值",
        value="B",
        source_chunk_id=role_chunk.id,
    )

    requester_views = service.list_facts_by_document(
        requester_chunk.document_id,
        requester_id="u-1",
        tenant_id="t-1",
        role="staff",
    )
    role_views = service.list_facts_by_document(
        role_chunk.document_id,
        requester_id="u-2",
        tenant_id="t-1",
        role="bid",
    )

    assert [view.fact.id for view in requester_views] == [requester_fact.id]
    assert [view.fact.id for view in role_views] == [role_fact.id]
    events = (
        db.query(AuditLog)
        .filter(AuditLog.action == "fact.query")
        .order_by(AuditLog.created_at.asc())
        .all()
    )
    assert events[-2].result_json["policy_decision"] == "allow"
    assert events[-1].result_json["policy_decision"] == "allow"


def test_fact_query_tenant_mismatch_denies_and_does_not_return_fact(tmp_path):
    db = _db_session(tmp_path)
    chunk = _seed_document_chunk(db, metadata_json={"tenant_id": "tenant-a"})
    fact = FactService(db).create_fact_from_evidence(
        fact_type="tender_basic_info",
        subject="租户隔离",
        predicate="值",
        value="A",
        source_chunk_id=chunk.id,
    )

    views = FactService(db).list_facts_by_document(
        chunk.document_id,
        requester_id="u-1",
        tenant_id="tenant-b",
        role="staff",
    )

    assert views == []
    event = _last_fact_query_audit(db)
    assert event.result_json["policy_decision"] == "deny"
    assert event.result_json["returned_fact_ids"] == []
    assert event.result_json["denied_fact_ids"] == [fact.id]
    assert event.result_json["source_document_ids"] == [chunk.document_id]


def test_fact_query_audit_failure_does_not_block_query(tmp_path, monkeypatch):
    db = _db_session(tmp_path)
    chunk = _seed_document_chunk(db)
    fact = FactService(db).create_fact_from_evidence(
        fact_type="meeting_action_item",
        subject="audit fail-open",
        predicate="负责",
        value="继续返回",
        source_chunk_id=chunk.id,
    )

    def fail_add(_item):
        raise RuntimeError("audit down")

    monkeypatch.setattr(db, "add", fail_add)

    views = FactService(db).list_facts_by_document(chunk.document_id)

    assert [view.fact.id for view in views] == [fact.id]


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
    metadata_json: dict | None = None,
) -> Chunk:
    if db.get(Document, document_id) is None:
        db.add(
            Document(
                id=document_id,
                title="测试文件",
                source_type="tender",
                source_uri="test.docx",
                document_type="tender",
                metadata_json=metadata_json or {},
            )
        )
    else:
        document = db.get(Document, document_id)
        document.metadata_json = metadata_json or {}
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


def _last_fact_query_audit(db) -> AuditLog:
    return (
        db.query(AuditLog)
        .filter(AuditLog.action == "fact.query")
        .order_by(AuditLog.created_at.desc())
        .first()
    )


def _last_fact_status_audit(db, action: str) -> AuditLog:
    return (
        db.query(AuditLog)
        .filter(AuditLog.action == action)
        .order_by(AuditLog.created_at.desc())
        .first()
    )
