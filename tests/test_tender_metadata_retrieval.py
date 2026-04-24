from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.base import Base
from app.models.chunk import Chunk
from app.models.document import Document, DocumentVersion
from app.schemas.retrieval import RetrievalFilter, SearchRequest, SearchResult
from app.services.retrieval.service import RetrievalService


def _make_db(tmp_path):
    engine = create_engine(f"sqlite:///{tmp_path / 'metadata.db'}")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    db = Session()
    db.add_all(
        [
            Document(
                id="doc-tender",
                title="测试大型标书",
                source_type="tender",
                source_uri="local://doc-tender",
                storage_uri=None,
                document_type="tender",
                status="active",
                metadata_json={},
            ),
            DocumentVersion(
                id="ver-tender",
                document_id="doc-tender",
                version_name="v1",
                is_latest=True,
                parse_status="completed",
                metadata_json={},
            ),
            Chunk(
                id="chunk-basic",
                document_id="doc-tender",
                version_id="ver-tender",
                chunk_index=1,
                text="招标公告\n工程名称：测试大型项目施工总承包工程\n工程地点：深圳市福田区园岭街道\n建设单位：深圳市测试建设有限公司\n代建单位：深圳市测试代建有限公司",
                heading_path=["招标公告"],
                title_path=["招标公告"],
                section_path=["招标公告"],
                page_start=1,
                page_end=1,
                char_count=100,
                content_hash="hash-basic",
                token_count=None,
                source_type="tender",
                metadata_json={},
                permission_tags=[],
            ),
            Chunk(
                id="chunk-boq",
                document_id="doc-tender",
                version_id="ver-tender",
                chunk_index=120,
                text="工程量清单章节包含大量工程地点周边措施项目描述，但不是基础信息来源。",
                heading_path=["工程量清单"],
                title_path=["工程量清单"],
                section_path=["工程量清单"],
                page_start=120,
                page_end=120,
                char_count=60,
                content_hash="hash-boq",
                token_count=None,
                source_type="tender",
                metadata_json={},
                permission_tags=[],
            ),
        ]
    )
    db.commit()
    return db


def test_tender_metadata_snapshot_matches_basic_info_fields(tmp_path):
    db = _make_db(tmp_path)
    service = RetrievalService(db=db)

    trace = service._infer_tender_metadata_scope(
        "工程地点、建设单位、代建单位分别是什么？",
        {"document_id": "doc-tender", "document_type": "tender", "is_latest": True},
    )

    assert trace["metadata_snapshot_used"] is True
    assert set(trace["metadata_fields_matched"]) == {
        "project_location",
        "construction_unit",
        "agent_or_delegate_unit",
    }
    assert trace["metadata_source_chunk_ids"] == ["chunk-basic", "chunk-basic", "chunk-basic"]
    assert trace["evidence_required"] is True
    assert trace["snapshot_as_answer"] is False
    db.close()


def test_tender_metadata_snapshot_guides_database_evidence(tmp_path):
    db = _make_db(tmp_path)
    service = RetrievalService(db=db)
    request = SearchRequest(
        query="工程地点、建设单位、代建单位分别是什么？",
        retrieval_mode="sparse",
        enable_dense=False,
        filters=RetrievalFilter(document_id="doc-tender", document_type="tender"),
    )
    applied = {"document_id": "doc-tender", "document_type": "tender", "is_latest": True}
    metadata_trace = service._infer_tender_metadata_scope(request.query, applied)
    section_scope = service._with_metadata_guidance(service._infer_section_scope(request.query), metadata_trace)

    results = service._database_fallback_search(request, applied, section_scope)

    assert results[0].chunk_id == "chunk-basic"
    assert results[0].retrieval_sources == ["metadata_anchor"]
    assert results[0].metadata["metadata_snapshot_anchor"] is True
    assert results[0].metadata["snapshot_as_answer"] is False
    db.close()


def test_tender_metadata_snapshot_open_search_trace_is_not_answer_evidence(tmp_path, monkeypatch):
    db = _make_db(tmp_path)
    service = RetrievalService(db=db)
    request = SearchRequest(
        query="工程地点、建设单位、代建单位分别是什么？",
        retrieval_mode="sparse",
        enable_dense=False,
        filters=RetrievalFilter(document_id="doc-tender", document_type="tender"),
    )

    def fake_sparse_search(request, applied_filters, section_scope):
        assert section_scope["metadata_snapshot_used"] is True
        assert section_scope["metadata_source_chunk_ids"] == ["chunk-basic", "chunk-basic", "chunk-basic"]
        return [
            SearchResult(
                chunk_id="chunk-basic",
                document_id="doc-tender",
                version_id="ver-tender",
                chunk_index=1,
                text="工程地点：深圳市福田区园岭街道",
                score=100.0,
                source_name="测试大型标书",
                retrieval_sources=["sparse"],
            )
        ]

    monkeypatch.setattr(service, "_sparse_search", fake_sparse_search)
    response = service.search(request)

    assert response.trace["metadata_snapshot_used"] is True
    assert response.trace["snapshot_as_answer"] is False
    assert response.trace["evidence_required"] is True
    assert response.results[0].chunk_id == "chunk-basic"
    db.close()


def test_tender_metadata_missing_snapshot_falls_back_to_plain_retrieval(tmp_path):
    db = _make_db(tmp_path)
    service = RetrievalService(db=db)
    request = SearchRequest(
        query="投标截止日期是什么？",
        retrieval_mode="sparse",
        enable_dense=False,
        filters=RetrievalFilter(document_id="doc-tender", document_type="tender"),
    )
    applied = {"document_id": "doc-tender", "document_type": "tender", "is_latest": True}
    metadata_trace = service._infer_tender_metadata_scope(request.query, applied)
    section_scope = service._with_metadata_guidance(service._infer_section_scope(request.query), metadata_trace)

    results = service._database_fallback_search(request, applied, section_scope)

    assert metadata_trace["metadata_snapshot_used"] is False
    assert all("metadata_anchor" not in result.retrieval_sources for result in results)
    db.close()
