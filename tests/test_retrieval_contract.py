from app.schemas.retrieval import RetrievalFilter, SearchRequest, SearchResult
from app.services.retrieval.dense import DenseSearchOutcome
from app.services.retrieval.service import RetrievalService
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

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
