from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.base import Base
from app.models.chunk import Chunk
from app.models.document import Document, DocumentVersion
from app.schemas.retrieval import RetrievalFilter, SearchRequest, SearchResult
from app.services.retrieval.service import RetrievalService


def _make_db(tmp_path, *, price_text: str, qualification_text: str):
    engine = create_engine(f"sqlite:///{tmp_path / 'phase236.db'}")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    db = Session()
    db.add_all(
        [
            Document(
                id="doc-tender",
                title="Phase 2.36 测试标书",
                source_type="tender",
                source_uri="local://phase236-tender",
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
                id="chunk-price",
                document_id="doc-tender",
                version_id="ver-tender",
                chunk_index=8,
                text=price_text,
                heading_path=["投标人须知前附表"],
                title_path=["投标人须知前附表"],
                section_path=["投标人须知前附表", "最高投标限价"],
                page_start=8,
                page_end=8,
                char_count=len(price_text),
                content_hash="hash-price",
                token_count=None,
                source_type="tender",
                metadata_json={},
                permission_tags=[],
            ),
            Chunk(
                id="chunk-qualification",
                document_id="doc-tender",
                version_id="ver-tender",
                chunk_index=18,
                text=qualification_text,
                heading_path=["资格审查"],
                title_path=["资格审查"],
                section_path=["资格审查", "投标人资格要求"],
                page_start=18,
                page_end=18,
                char_count=len(qualification_text),
                content_hash="hash-qualification",
                token_count=None,
                source_type="tender",
                metadata_json={},
                permission_tags=[],
            ),
        ]
    )
    db.commit()
    return db


def _search_with_fake_sparse(monkeypatch, service: RetrievalService, query: str, result: SearchResult | None = None):
    def fake_sparse_search(request, applied_filters, section_scope):
        if result is None:
            return []
        return [result]

    monkeypatch.setattr(service, "_sparse_search", fake_sparse_search)
    return service.search(
        SearchRequest(
            query=query,
            retrieval_mode="sparse",
            enable_dense=False,
            filters=RetrievalFilter(document_id="doc-tender", document_type="tender"),
        )
    )


def test_price_ceiling_concrete_trace_exposes_section_diagnostics(tmp_path, monkeypatch):
    db = _make_db(
        tmp_path,
        price_text="投标人须知前附表\n最高投标限价：人民币200万元。投标报价不得超过招标控制价。",
        qualification_text="资格审查\n投标人资格要求：须提供营业执照、资质证书、安全生产许可证等证明材料。",
    )
    service = RetrievalService(db=db)
    result = SearchResult(
        chunk_id="chunk-price",
        document_id="doc-tender",
        version_id="ver-tender",
        text="最高投标限价：人民币200万元。",
        score=100.0,
        source_name="Phase 2.36 测试标书",
        retrieval_sources=["sparse"],
    )

    response = _search_with_fake_sparse(monkeypatch, service, "最高投标限价和招标控制价是多少？", result)

    assert response.trace["metadata_deep_field_profile"] == "pricing_scope"
    assert response.trace["deep_field_profile"] == "pricing_scope"
    assert "投标人须知前附表" in response.trace["deep_field_section_hints"]
    assert "最高投标限价" in response.trace["deep_field_query_aliases"]
    assert response.trace["deep_field_missing_reason"] is None
    diagnostics = response.trace["deep_field_diagnostics"]
    assert diagnostics["status"] == "concrete_evidence_found"
    assert diagnostics["concrete_evidence_present"] is True
    assert diagnostics["concrete_evidence_required_fields"] == ["price_ceiling"]
    assert diagnostics["metadata_source_chunk_ids"] == ["chunk-price"]
    db.close()


def test_price_ceiling_placeholder_keeps_missing_evidence_diagnostics(tmp_path, monkeypatch):
    db = _make_db(
        tmp_path,
        price_text="投标人须知前附表\n最高投标限价详见附件，投标报价按招标控制价执行。",
        qualification_text="资格审查\n投标人资格要求：具备建筑工程施工总承包一级及以上资质。",
    )
    service = RetrievalService(db=db)

    response = _search_with_fake_sparse(monkeypatch, service, "最高投标限价和招标控制价是多少？")

    assert response.trace["metadata_snapshot_used"] is False
    assert response.trace["metadata_deep_field_profile"] == "pricing_scope"
    assert response.trace["deep_field_profile"] == "pricing_scope"
    assert response.trace["deep_field_missing_reason"] == "missing_concrete_price_amount"
    diagnostics = response.trace["deep_field_diagnostics"]
    assert diagnostics["status"] == "missing_concrete_evidence"
    assert diagnostics["concrete_evidence_present"] is False
    assert diagnostics["concrete_evidence_missing_fields"] == ["price_ceiling"]
    assert "最高投标限价" in diagnostics["query_aliases_used"]
    db.close()


def test_price_ceiling_metadata_anchor_without_final_amount_stays_missing(tmp_path, monkeypatch):
    db = _make_db(
        tmp_path,
        price_text="投标人须知前附表\n最高投标限价：人民币200万元。投标报价不得超过招标控制价。",
        qualification_text="资格审查\n投标人资格要求：具备建筑工程施工总承包一级及以上资质。",
    )
    service = RetrievalService(db=db)
    result = SearchResult(
        chunk_id="chunk-price-neighbor",
        document_id="doc-tender",
        version_id="ver-tender",
        text="投标报价不得超过招标控制价，具体金额详见附件。",
        score=100.0,
        source_name="Phase 2.36 测试标书",
        retrieval_sources=["sparse"],
    )

    response = _search_with_fake_sparse(monkeypatch, service, "最高投标限价和招标控制价是多少？", result)

    assert response.trace["deep_field_missing_reason"] == "missing_concrete_price_amount"
    diagnostics = response.trace["deep_field_diagnostics"]
    assert diagnostics["status"] == "missing_concrete_evidence"
    assert diagnostics["concrete_evidence_present"] is False
    assert diagnostics["concrete_evidence_missing_fields"] == ["price_ceiling"]
    assert diagnostics["diagnostic_consistency"] == "metadata_anchor_without_final_concrete_evidence"
    db.close()


def test_qualification_concrete_trace_exposes_section_diagnostics(tmp_path, monkeypatch):
    db = _make_db(
        tmp_path,
        price_text="投标人须知前附表\n最高投标限价详见附件。",
        qualification_text="资格审查\n投标人资格要求：具备建筑工程施工总承包一级及以上资质。",
    )
    service = RetrievalService(db=db)
    result = SearchResult(
        chunk_id="chunk-qualification",
        document_id="doc-tender",
        version_id="ver-tender",
        text="具备建筑工程施工总承包一级及以上资质。",
        score=100.0,
        source_name="Phase 2.36 测试标书",
        retrieval_sources=["sparse"],
    )

    response = _search_with_fake_sparse(monkeypatch, service, "投标资质等级和类别是什么？", result)

    assert response.trace["metadata_deep_field_profile"] == "qualification_scope"
    assert response.trace["deep_field_profile"] == "qualification_scope"
    assert "资格审查" in response.trace["deep_field_section_hints"]
    assert "资质要求" in response.trace["deep_field_query_aliases"]
    diagnostics = response.trace["deep_field_diagnostics"]
    assert diagnostics["status"] == "concrete_evidence_found"
    assert diagnostics["concrete_evidence_present"] is True
    assert diagnostics["concrete_evidence_required_fields"] == ["qualification_requirement"]
    assert diagnostics["metadata_source_chunk_ids"] == ["chunk-qualification"]
    db.close()


def test_qualification_certificate_list_keeps_missing_evidence_diagnostics(tmp_path, monkeypatch):
    db = _make_db(
        tmp_path,
        price_text="投标人须知前附表\n最高投标限价：人民币200万元。",
        qualification_text="资格审查\n投标人资格要求：须提供营业执照、资质证书、安全生产许可证等证明材料。",
    )
    service = RetrievalService(db=db)

    response = _search_with_fake_sparse(monkeypatch, service, "投标资质等级和类别是什么？")

    assert response.trace["metadata_snapshot_used"] is False
    assert response.trace["metadata_deep_field_profile"] == "qualification_scope"
    assert response.trace["deep_field_profile"] == "qualification_scope"
    assert response.trace["deep_field_missing_reason"] == "missing_concrete_qualification_level_or_category"
    diagnostics = response.trace["deep_field_diagnostics"]
    assert diagnostics["status"] == "missing_concrete_evidence"
    assert diagnostics["concrete_evidence_present"] is False
    assert diagnostics["concrete_evidence_missing_fields"] == ["qualification_requirement"]
    assert "资质要求" in diagnostics["query_aliases_used"]
    assert "投标人资格要求" in diagnostics["boosted_phrases_used"]
    db.close()


def test_project_manager_explicit_level_trace_is_concrete(tmp_path, monkeypatch):
    db = _make_db(
        tmp_path,
        price_text="投标人须知前附表\n最高投标限价：人民币200万元。",
        qualification_text="资格审查\n项目经理须具备一级注册建造师和安全生产考核B证。",
    )
    service = RetrievalService(db=db)
    result = SearchResult(
        chunk_id="chunk-qualification",
        document_id="doc-tender",
        version_id="ver-tender",
        text="项目经理须具备一级注册建造师和安全生产考核B证。",
        score=100.0,
        source_name="Phase 2.36 测试标书",
        retrieval_sources=["sparse"],
    )

    response = _search_with_fake_sparse(monkeypatch, service, "项目经理注册建造师和B证要求是什么？", result)

    diagnostics = response.trace["deep_field_diagnostics"]
    assert diagnostics["status"] == "concrete_evidence_found"
    assert diagnostics["concrete_evidence_present"] is True
    assert diagnostics["concrete_evidence_required_fields"] == ["project_manager_requirement"]
    assert diagnostics["project_manager_level_explicit"] is True
    assert "project_manager_level_missing_reason" not in diagnostics
    db.close()


def test_project_manager_electronic_certificate_format_is_not_role_level(tmp_path, monkeypatch):
    db = _make_db(
        tmp_path,
        price_text="投标人须知前附表\n最高投标限价：人民币200万元。",
        qualification_text="资格审查\n投标文件应提供一级注册建造师电子证书格式、签名件和证书材料。",
    )
    service = RetrievalService(db=db)
    result = SearchResult(
        chunk_id="chunk-qualification",
        document_id="doc-tender",
        version_id="ver-tender",
        text="投标文件应提供一级注册建造师电子证书格式、签名件和证书材料。",
        score=100.0,
        source_name="Phase 2.36 测试标书",
        retrieval_sources=["sparse"],
    )

    response = _search_with_fake_sparse(monkeypatch, service, "项目经理注册建造师和B证要求是什么？", result)

    assert response.trace["deep_field_missing_reason"] == "missing_explicit_project_manager_level"
    diagnostics = response.trace["deep_field_diagnostics"]
    assert diagnostics["status"] == "missing_concrete_evidence"
    assert diagnostics["concrete_evidence_present"] is False
    assert diagnostics["project_manager_level_explicit"] is False
    assert (
        diagnostics["project_manager_level_missing_reason"]
        == "electronic_certificate_format_is_not_role_level_requirement"
    )
    db.close()
