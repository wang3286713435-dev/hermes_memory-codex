from app.schemas.retrieval import RetrievalFilter, SearchRequest, SearchResult
from app.services.retrieval.dense import DenseSearchOutcome
from app.services.retrieval.service import RetrievalService
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta, timezone

from app.db.base import Base
from app.models.chunk import Chunk
from app.models.document import Document, DocumentVersion


def _result(chunk_id: str, score: float, source: str) -> SearchResult:
    return SearchResult(
        chunk_id=chunk_id,
        document_id="doc-1",
        version_id="ver-1",
        text=f"{source} text",
        score=score,
        retrieval_sources=[source],
        scores={source: score},
    )


def test_search_request_contract_defaults_to_hybrid():
    request = SearchRequest(query="投标截止日期")

    assert request.retrieval_mode == "hybrid"
    assert request.enable_dense is True
    assert request.enable_sparse is True
    assert request.enable_hybrid is True
    assert request.filters.is_latest is True


def test_metadata_filters_are_applied_and_unsupported_filters_are_reported(monkeypatch):
    service = RetrievalService(db=None)  # type: ignore[arg-type]
    captured = {}

    def fake_sparse(request, applied_filters):
        captured["applied_filters"] = applied_filters
        return [_result("chunk-sparse", 3.0, "sparse")]

    monkeypatch.setattr(service, "_sparse_search", fake_sparse)
    monkeypatch.setattr(service, "_write_log", lambda *args, **kwargs: None)

    response = service.search(
        SearchRequest(
            query="招标资料",
            retrieval_mode="sparse",
            enable_dense=False,
            filters=RetrievalFilter(
                source_type="upload",
                document_id="doc-1",
                document_type="tender",
                project_id="project-unsupported",
                custom_flag="custom-unsupported",
            ),
        )
    )

    assert captured["applied_filters"] == {
        "source_type": "upload",
        "document_id": "doc-1",
        "document_type": "tender",
        "is_latest": True,
    }
    assert response.applied_filters == captured["applied_filters"]
    assert response.ignored_filters == {
        "project_id": "project-unsupported",
        "custom_flag": "custom-unsupported",
    }
    assert response.sparse_status == "executed"


def test_dense_adapter_path_returns_unified_contract(monkeypatch):
    service = RetrievalService(db=None)  # type: ignore[arg-type]

    class FakeDense:
        def search(self, request, applied_filters):
            assert applied_filters["source_type"] == "upload"
            return DenseSearchOutcome(
                results=[_result("chunk-dense", 0.8, "dense")],
                status="executed",
                trace={"backend": "fake_vector"},
            )

    service.dense = FakeDense()
    monkeypatch.setattr(service, "_write_log", lambda *args, **kwargs: None)

    response = service.search(
        SearchRequest(
            query="项目方案",
            retrieval_mode="dense",
            enable_sparse=False,
            filters=RetrievalFilter(source_type="upload"),
        )
    )

    assert response.backend == "fake_vector"
    assert response.dense_status == "executed"
    assert response.sparse_status == "skipped"
    assert response.results[0].retrieval_sources == ["dense"]
    assert response.trace["dense"]["backend"] == "fake_vector"


def test_hybrid_merges_dense_and_sparse_results_with_trace(monkeypatch):
    service = RetrievalService(db=None)  # type: ignore[arg-type]

    class FakeDense:
        def search(self, request, applied_filters):
            return DenseSearchOutcome(
                results=[
                    _result("shared", 0.6, "dense"),
                    _result("dense-only", 0.4, "dense"),
                ],
                status="executed",
                trace={"backend": "fake_vector"},
            )

    def fake_sparse(request, applied_filters):
        return [
            _result("shared", 2.0, "sparse"),
            _result("sparse-only", 1.0, "sparse"),
        ]

    service.dense = FakeDense()
    monkeypatch.setattr(service, "_sparse_search", fake_sparse)
    monkeypatch.setattr(service, "_write_log", lambda *args, **kwargs: None)

    response = service.search(SearchRequest(query="投标截止日期", retrieval_mode="hybrid", top_k=5))

    shared = next(item for item in response.results if item.chunk_id == "shared")
    assert response.backend == "hybrid"
    assert response.dense_status == "executed"
    assert response.sparse_status == "executed"
    assert shared.retrieval_sources == ["dense", "sparse"]
    assert shared.scores == {"dense": 0.6, "sparse": 2.0}
    assert shared.score == 2.6
    assert response.trace["hybrid"]["fusion"] == "score_sum_by_source"


def test_search_with_db_none_skips_document_scope_inference(monkeypatch):
    service = RetrievalService(db=None)  # type: ignore[arg-type]

    def fake_sparse(_request, applied_filters, _section_scope):
        assert "document_id" not in applied_filters
        return [_result("chunk-sparse", 1.0, "sparse")]

    monkeypatch.setattr(service, "_sparse_search", fake_sparse)
    monkeypatch.setattr(service, "_write_log", lambda *args, **kwargs: None)

    response = service.search(
        SearchRequest(
            query="请围绕《附件十一：数字化交付标准》回答",
            retrieval_mode="sparse",
            enable_dense=False,
            filters=RetrievalFilter(source_type="tender", document_type="tender"),
        )
    )

    assert response.sparse_status == "executed"
    assert response.trace["document_scope"]["status"] == "db_unavailable"
    assert response.trace["document_scope"]["reason"] == "document_scope_requires_db"


def test_database_fallback_applies_source_type_and_document_id_filters(tmp_path):
    engine = create_engine(f"sqlite:///{tmp_path / 'filters.db'}")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    db = Session()
    db.add_all(
        [
            Document(
                id="doc-1",
                title="星河项目招标资料",
                source_type="upload",
                source_uri="local://doc-1",
                storage_uri=None,
                document_type="tender",
                status="active",
                metadata_json={},
            ),
            DocumentVersion(
                id="ver-1",
                document_id="doc-1",
                version_name="v1",
                is_latest=True,
                parse_status="completed",
                metadata_json={},
            ),
            Chunk(
                id="chunk-1",
                document_id="doc-1",
                version_id="ver-1",
                chunk_index=0,
                text="投标截止日期为2025年5月20日。",
                heading_path=[],
                title_path=[],
                section_path=[],
                page_start=None,
                page_end=None,
                char_count=20,
                content_hash="hash-1",
                token_count=None,
                source_type="upload",
                metadata_json={},
                permission_tags=[],
            ),
            Document(
                id="doc-2",
                title="其他资料",
                source_type="wechat",
                source_uri="local://doc-2",
                storage_uri=None,
                document_type="article",
                status="active",
                metadata_json={},
            ),
            DocumentVersion(
                id="ver-2",
                document_id="doc-2",
                version_name="v1",
                is_latest=True,
                parse_status="completed",
                metadata_json={},
            ),
            Chunk(
                id="chunk-2",
                document_id="doc-2",
                version_id="ver-2",
                chunk_index=0,
                text="投标截止日期为2026年1月1日。",
                heading_path=[],
                title_path=[],
                section_path=[],
                page_start=None,
                page_end=None,
                char_count=20,
                content_hash="hash-2",
                token_count=None,
                source_type="wechat",
                metadata_json={},
                permission_tags=[],
            ),
        ]
    )
    db.commit()

    service = RetrievalService(db=db)
    results = service._database_fallback_search(
        SearchRequest(query="投标截止日期"),
        {"source_type": "upload", "document_id": "doc-1", "is_latest": True},
    )

    assert [item.chunk_id for item in results] == ["chunk-1"]
    db.close()


def test_database_fallback_returns_empty_without_db():
    service = RetrievalService(db=None)  # type: ignore[arg-type]

    results = service._database_fallback_search(SearchRequest(query="投标截止日期"))

    assert results == []


def test_sparse_search_uses_keyword_subfields_for_text_mappings(monkeypatch):
    service = RetrievalService(db=None)  # type: ignore[arg-type]

    captured = {}

    class FakeIndices:
        def get_mapping(self, index):
            return {
                index: {
                    "mappings": {
                        "properties": {
                            "status": {"type": "text", "fields": {"keyword": {"type": "keyword"}}},
                            "source_type": {"type": "text", "fields": {"keyword": {"type": "keyword"}}},
                            "document_id": {"type": "text", "fields": {"keyword": {"type": "keyword"}}},
                            "document_type": {"type": "text", "fields": {"keyword": {"type": "keyword"}}},
                            "is_latest": {"type": "boolean"},
                        }
                    }
                }
            }

    class FakeClient:
        def __init__(self, *_args, **_kwargs):
            self.indices = FakeIndices()

        def search(self, *, index, body):
            captured["index"] = index
            captured["body"] = body
            return {"hits": {"hits": []}}

    monkeypatch.setattr("app.services.retrieval.service.OpenSearch", FakeClient)

    service._sparse_search(
        SearchRequest(query="答疑补遗", top_k=5),
        {
            "source_type": "tender",
            "document_id": "1db84714-d49f-48a2-8fa9-c6f73424dd32",
            "document_type": "tender",
            "is_latest": True,
        },
    )

    filters = captured["body"]["query"]["bool"]["filter"]
    assert {"term": {"status.keyword": "active"}} in filters
    assert {"term": {"source_type.keyword": "tender"}} in filters
    assert {"term": {"document_id.keyword": "1db84714-d49f-48a2-8fa9-c6f73424dd32"}} in filters


def test_sparse_search_adds_section_scope_boosts_for_structured_bid_queries(monkeypatch):
    service = RetrievalService(db=None)  # type: ignore[arg-type]
    captured = {}

    class FakeIndices:
        def get_mapping(self, index):
            return {
                index: {
                    "mappings": {
                        "properties": {
                            "status": {"type": "text", "fields": {"keyword": {"type": "keyword"}}},
                            "source_type": {"type": "text", "fields": {"keyword": {"type": "keyword"}}},
                            "document_id": {"type": "text", "fields": {"keyword": {"type": "keyword"}}},
                            "document_type": {"type": "text", "fields": {"keyword": {"type": "keyword"}}},
                            "is_latest": {"type": "boolean"},
                        }
                    }
                }
            }

    class FakeClient:
        def __init__(self, *_args, **_kwargs):
            self.indices = FakeIndices()

        def search(self, *, index, body):
            captured["body"] = body
            return {"hits": {"hits": []}}

    monkeypatch.setattr("app.services.retrieval.service.OpenSearch", FakeClient)

    section_scope = service._infer_section_scope("施工总承包资质等级要求是什么")
    service._sparse_search(
        SearchRequest(query="施工总承包资质等级要求是什么", top_k=5),
        {"source_type": "tender", "document_id": "doc-1", "document_type": "tender", "is_latest": True},
        section_scope,
    )

    shoulds = captured["body"]["query"]["bool"]["should"]
    filters = captured["body"]["query"]["bool"]["filter"]
    assert {"match": {"heading_path": {"query": "投标人须知前附表", "boost": 6.0}}} in shoulds
    assert {"match": {"heading_path": {"query": "资格审查", "boost": 6.0}}} in shoulds
    assert captured["body"]["size"] == 10
    assert {"term": {"document_type.keyword": "tender"}} in filters
    assert {"term": {"is_latest": True}} in filters


def test_sparse_search_adds_schedule_clause_boosts_for_schedule_queries(monkeypatch):
    service = RetrievalService(db=None)  # type: ignore[arg-type]
    captured = {}

    class FakeIndices:
        def get_mapping(self, index):
            return {
                index: {
                    "mappings": {
                        "properties": {
                            "status": {"type": "text", "fields": {"keyword": {"type": "keyword"}}},
                            "source_type": {"type": "text", "fields": {"keyword": {"type": "keyword"}}},
                            "document_id": {"type": "text", "fields": {"keyword": {"type": "keyword"}}},
                            "document_type": {"type": "text", "fields": {"keyword": {"type": "keyword"}}},
                            "is_latest": {"type": "boolean"},
                        }
                    }
                }
            }

    class FakeClient:
        def __init__(self, *_args, **_kwargs):
            self.indices = FakeIndices()

        def search(self, *, index, body):
            captured["body"] = body
            return {"hits": {"hits": []}}

    monkeypatch.setattr("app.services.retrieval.service.OpenSearch", FakeClient)

    section_scope = service._infer_section_scope("总工期和关键节点怎么要求")
    service._sparse_search(
        SearchRequest(query="总工期和关键节点怎么要求", top_k=5),
        {"source_type": "tender", "document_id": "doc-1", "document_type": "tender", "is_latest": True},
        section_scope,
    )

    shoulds = captured["body"]["query"]["bool"]["should"]
    assert {"match": {"heading_path": {"query": "工期要求", "boost": 7.0}}} in shoulds
    assert {"match": {"heading_path": {"query": "计划开工日期", "boost": 7.0}}} in shoulds
    assert {"match": {"heading_path": {"query": "关键工期节点", "boost": 7.0}}} in shoulds
    assert {"match_phrase": {"text": {"query": "计划竣工日期", "boost": 4.5}}} in shoulds
    assert {"match_phrase": {"text": {"query": "工期要求", "boost": 6.0}}} in shoulds
    assert {"match_phrase": {"text": {"query": "工期要求", "boost": 14.0}}} in shoulds
    assert {"match_phrase": {"text": {"query": "总工期", "boost": 10.0}}} in shoulds
    assert {"match_phrase": {"text": {"query": "计划开工日期", "boost": 9.0}}} in shoulds
    assert {"match_phrase": {"text": {"query": "日历天", "boost": 6.0}}} in shoulds


def test_sparse_search_adds_contract_clause_boosts_for_commercial_queries(monkeypatch):
    service = RetrievalService(db=None)  # type: ignore[arg-type]
    captured = {}

    class FakeIndices:
        def get_mapping(self, index):
            return {
                index: {
                    "mappings": {
                        "properties": {
                            "status": {"type": "text", "fields": {"keyword": {"type": "keyword"}}},
                            "source_type": {"type": "text", "fields": {"keyword": {"type": "keyword"}}},
                            "document_id": {"type": "text", "fields": {"keyword": {"type": "keyword"}}},
                            "document_type": {"type": "text", "fields": {"keyword": {"type": "keyword"}}},
                            "is_latest": {"type": "boolean"},
                        }
                    }
                }
            }

    class FakeClient:
        def __init__(self, *_args, **_kwargs):
            self.indices = FakeIndices()

        def search(self, *, index, body):
            captured["body"] = body
            return {"hits": {"hits": []}}

    monkeypatch.setattr("app.services.retrieval.service.OpenSearch", FakeClient)

    section_scope = service._infer_section_scope("付款节点和结算方式是什么")
    service._sparse_search(
        SearchRequest(query="付款节点和结算方式是什么", top_k=5),
        {"source_type": "tender", "document_id": "doc-1", "document_type": "tender", "is_latest": True},
        section_scope,
    )

    shoulds = captured["body"]["query"]["bool"]["should"]
    assert {"match": {"heading_path": {"query": "合同专用条款", "boost": 10.0}}} in shoulds
    assert {"match": {"heading_path": {"query": "工程款支付", "boost": 10.0}}} in shoulds
    assert {"match": {"heading_path": {"query": "竣工结算", "boost": 10.0}}} in shoulds
    assert {"match": {"heading_path": {"query": "付款", "boost": 6.0}}} in shoulds
    assert {"match_phrase": {"text": {"query": "工程款支付", "boost": 6.5}}} in shoulds


def test_search_infers_document_id_from_explicit_document_title(monkeypatch, tmp_path):
    engine = create_engine(f"sqlite:///{tmp_path / 'document_scope.db'}")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    db = Session()
    db.add_all(
        [
            Document(
                id="doc-old",
                title="宝安新桥东重点城市更新项目答疑补遗文件（一）",
                source_type="tender",
                source_uri="旧文件.docx",
                storage_uri=None,
                document_type="tender",
                status="active",
                metadata_json={},
            ),
            Document(
                id="doc-new",
                title="附件十一：数字化交付标准",
                source_type="tender",
                source_uri="附件十一：数字化交付标准.docx",
                storage_uri=None,
                document_type="tender",
                status="active",
                metadata_json={},
            ),
        ]
    )
    db.commit()

    service = RetrievalService(db=db)
    captured = {}

    def fake_sparse(request, applied_filters):
        captured["applied_filters"] = dict(applied_filters)
        return [
            SearchResult(
                chunk_id="chunk-new",
                document_id="doc-new",
                version_id="ver-new",
                text="数字化交付标准内容",
                score=3.0,
                source_name="附件十一：数字化交付标准",
                source_type="tender",
                retrieval_sources=["sparse"],
                scores={"sparse": 3.0},
            )
        ]

    monkeypatch.setattr(service, "_sparse_search", fake_sparse)
    monkeypatch.setattr(service, "_write_log", lambda *args, **kwargs: None)

    response = service.search(
        SearchRequest(
            query="请围绕《附件十一：数字化交付标准》回答",
            retrieval_mode="sparse",
            enable_dense=False,
            filters=RetrievalFilter(source_type="tender", document_type="tender"),
        )
    )

    assert captured["applied_filters"]["document_id"] == "doc-new"
    assert response.applied_filters["document_id"] == "doc-new"
    assert response.trace["document_scope"]["status"] == "inferred_from_query"
    assert response.results[0].document_id == "doc-new"
    db.close()


def test_search_prefers_latest_document_when_same_title_matches(monkeypatch, tmp_path):
    engine = create_engine(f"sqlite:///{tmp_path / 'duplicate_document_scope.db'}")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    db = Session()
    older = datetime.now(timezone.utc) - timedelta(minutes=5)
    newer = datetime.now(timezone.utc)
    db.add_all(
        [
            Document(
                id="doc-old-title",
                title="附件十一：数字化交付标准",
                source_type="tender",
                source_uri="附件十一：数字化交付标准.doc",
                storage_uri=None,
                document_type="tender",
                status="active",
                metadata_json={},
                created_at=older,
                updated_at=older,
            ),
            Document(
                id="doc-new-title",
                title="附件十一：数字化交付标准",
                source_type="tender",
                source_uri="附件十一：数字化交付标准.docx",
                storage_uri=None,
                document_type="tender",
                status="active",
                metadata_json={},
                created_at=newer,
                updated_at=newer,
            ),
        ]
    )
    db.commit()

    service = RetrievalService(db=db)
    captured = {}

    def fake_sparse(request, applied_filters):
        captured["applied_filters"] = dict(applied_filters)
        return [
            SearchResult(
                chunk_id="chunk-latest",
                document_id=applied_filters["document_id"],
                version_id="ver-new",
                text="数字化交付标准内容",
                score=3.0,
                source_name="附件十一：数字化交付标准",
                source_type="tender",
                retrieval_sources=["sparse"],
                scores={"sparse": 3.0},
            )
        ]

    monkeypatch.setattr(service, "_sparse_search", fake_sparse)
    monkeypatch.setattr(service, "_write_log", lambda *args, **kwargs: None)

    response = service.search(
        SearchRequest(
            query="请围绕《附件十一：数字化交付标准》回答",
            retrieval_mode="sparse",
            enable_dense=False,
            filters=RetrievalFilter(source_type="tender", document_type="tender"),
        )
    )

    assert captured["applied_filters"]["document_id"] == "doc-new-title"
    assert response.trace["document_scope"]["status"] == "inferred_from_query_latest_match"
    assert response.results[0].document_id == "doc-new-title"
    db.close()
