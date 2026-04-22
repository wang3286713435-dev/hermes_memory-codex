from app.core.config import settings
from app.schemas.retrieval import RetrievalFilter, SearchRequest, SearchResult
from app.services.evaluation import RetrievalEvalCase, evaluate_retrieval_response
from app.services.retrieval.dense import DenseSearchOutcome
from app.services.retrieval.rerank import NoopReranker, RerankRequest
from app.services.retrieval.service import RetrievalService


def _result(chunk_id: str, score: float, source: str) -> SearchResult:
    return SearchResult(
        chunk_id=chunk_id,
        document_id="doc-1",
        version_id="ver-1",
        text=f"{source} text",
        score=score,
        source_type="tender" if source == "tender" else "company_doc",
        retrieval_sources=[source],
        scores={source: score},
    )


def test_noop_reranker_returns_diagnostic_outcome():
    outcome = NoopReranker().rerank(
        RerankRequest(
            query="投标截止日期",
            candidates=[_result("low", 0.1, "dense"), _result("high", 0.9, "sparse")],
            top_k=1,
            retrieval_mode="hybrid",
            trace_id="trace-1",
        )
    )

    assert outcome.status == "skipped"
    assert outcome.provider == "noop"
    assert [item.chunk_id for item in outcome.results] == ["high"]
    assert outcome.trace["reason"] == "noop_reranker_preserves_score_order"
    assert outcome.trace["reason_if_skipped"] == "noop_reranker_preserves_score_order"
    assert outcome.trace["fail_open"] is False
    assert outcome.trace["elapsed_ms"] >= 0
    assert outcome.trace["input_count"] == 2
    assert outcome.trace["output_count"] == 1
    assert outcome.trace["candidate_count_in"] == 2
    assert outcome.trace["candidate_count_out"] == 1


def test_candidate_pool_and_rerank_trace_are_recorded(monkeypatch):
    service = RetrievalService(db=None)  # type: ignore[arg-type]

    class FakeDense:
        def search(self, _request, _applied_filters):
            return DenseSearchOutcome(
                results=[_result("shared", 0.6, "dense"), _result("dense-only", 0.4, "dense")],
                status="executed",
                trace={"backend": "fake_vector"},
            )

    service.dense = FakeDense()
    monkeypatch.setattr(
        service,
        "_sparse_search",
        lambda _request, _filters: [
            _result("shared", 2.0, "sparse"),
            _result("sparse-only", 1.0, "sparse"),
        ],
    )
    monkeypatch.setattr(service, "_write_log", lambda *args, **kwargs: None)

    response = service.search(SearchRequest(query="投标截止日期", retrieval_mode="hybrid", top_k=2))

    assert [item.chunk_id for item in response.results] == ["shared", "sparse-only"]
    assert response.trace["candidate_pool"]["raw_count"] == 4
    assert response.trace["candidate_pool"]["deduped_count"] == 3
    assert response.trace["candidate_pool"]["dense_returned"] == 2
    assert response.trace["candidate_pool"]["sparse_returned"] == 2
    assert response.trace["candidate_pool"]["before_dedupe"] == 4
    assert response.trace["candidate_pool"]["after_dedupe"] == 3
    assert response.trace["candidate_pool"]["source_counts"] == {"dense": 2, "sparse": 2}
    assert response.trace["rerank_status"] == "skipped"
    assert response.trace["rerank"]["provider"] == "noop"
    assert response.trace["rerank"]["input_count"] == 3
    assert response.trace["rerank"]["output_count"] == 2
    assert response.trace["rerank"]["candidate_count_in"] == 3
    assert response.trace["rerank"]["candidate_count_out"] == 2


def test_rerank_failure_fail_opens_to_candidate_pool(monkeypatch):
    monkeypatch.setattr(settings, "rerank_enabled", True)
    monkeypatch.setattr(settings, "rerank_provider", "aliyun")
    monkeypatch.setattr(settings, "rerank_default_enablement_enabled", True)
    monkeypatch.setattr(settings, "rerank_default_enablement_keywords", "资质,要求,条款,截止")
    monkeypatch.setattr(settings, "rerank_default_enablement_source_types", "tender")
    service = RetrievalService(db=None)  # type: ignore[arg-type]

    class BrokenReranker:
        provider = "broken"

        def rerank(self, _request):
            raise RuntimeError("reranker offline")

    service.reranker = BrokenReranker()
    monkeypatch.setattr(
        service,
        "_sparse_search",
        lambda _request, _filters: [
            SearchResult(
                chunk_id="a",
                document_id="doc-tender",
                version_id="ver-1",
                text="招标资质要求正文 A",
                score=0.1,
                source_type="tender",
                retrieval_sources=["sparse"],
                scores={"sparse": 0.1},
            ),
            SearchResult(
                chunk_id="b",
                document_id="doc-tender",
                version_id="ver-1",
                text="招标资质要求正文 B",
                score=0.9,
                source_type="tender",
                retrieval_sources=["sparse"],
                scores={"sparse": 0.9},
            ),
        ],
    )
    monkeypatch.setattr(service, "_write_log", lambda *args, **kwargs: None)

    response = service.search(
        SearchRequest(
            query="投标截止日期",
            route_type="tender_query",
            retrieval_mode="sparse",
            enable_dense=False,
            top_k=1,
            filters=RetrievalFilter(source_type="tender"),
        )
    )

    assert [item.chunk_id for item in response.results] == ["b"]
    assert response.trace["rerank_status"] == "failed_open"
    assert response.trace["rerank"]["provider"] == "broken"
    assert response.trace["rerank"]["reason"] == "rerank_exception"
    assert response.trace["rerank"]["fail_open"] is True
    assert response.trace["rerank"]["elapsed_ms"] >= 0
    assert response.trace["rerank"]["output_count"] == 1


def test_retrieval_eval_entry_reads_final_results_and_trace(monkeypatch):
    service = RetrievalService(db=None)  # type: ignore[arg-type]
    monkeypatch.setattr(
        service,
        "_sparse_search",
        lambda _request, _filters: [_result("expected", 1.0, "sparse")],
    )
    monkeypatch.setattr(service, "_write_log", lambda *args, **kwargs: None)

    response = service.search(
        SearchRequest(query="投标截止日期", retrieval_mode="sparse", enable_dense=False, top_k=5)
    )
    report = evaluate_retrieval_response(
        RetrievalEvalCase(query="投标截止日期", expected_chunk_ids={"expected"}),
        response,
    )

    assert report["has_expected_hit"] is True
    assert report["hit_chunk_ids"] == ["expected"]
    assert report["rerank_status"] == "skipped"
    assert report["candidate_pool"]["deduped_count"] == 1


def test_local_default_enablement_executes_for_tender_qualification_query(monkeypatch):
    monkeypatch.setattr(settings, "rerank_enabled", True)
    monkeypatch.setattr(settings, "rerank_provider", "aliyun")
    monkeypatch.setattr(settings, "rerank_default_enablement_enabled", True)
    monkeypatch.setattr(settings, "rerank_default_enablement_keywords", "资质,要求,条款,截止")
    monkeypatch.setattr(settings, "rerank_default_enablement_source_types", "tender")
    monkeypatch.setattr(settings, "rerank_default_enablement_min_candidates", 2)

    service = RetrievalService(db=None)  # type: ignore[arg-type]

    class FakeAliyunReranker:
        provider = "aliyun_text_rerank"

        def rerank(self, request):
            return NoopReranker().rerank(request)

    service.reranker = FakeAliyunReranker()
    monkeypatch.setattr(
        service,
        "_sparse_search",
        lambda _request, _filters: [
            SearchResult(
                chunk_id="tender-1",
                document_id="doc-tender",
                version_id="ver-1",
                text="招标资质要求正文",
                score=1.0,
                source_type="tender",
                retrieval_sources=["sparse"],
                scores={"sparse": 1.0},
            ),
            SearchResult(
                chunk_id="tender-2",
                document_id="doc-tender",
                version_id="ver-1",
                text="投标截止条款正文",
                score=0.8,
                source_type="tender",
                retrieval_sources=["sparse"],
                scores={"sparse": 0.8},
            ),
        ],
    )
    monkeypatch.setattr(service, "_write_log", lambda *args, **kwargs: None)

    response = service.search(
        SearchRequest(
            query="智慧园区项目有哪些资质要求？",
            route_type="tender_query",
            retrieval_mode="sparse",
            enable_dense=False,
            top_k=2,
            filters=RetrievalFilter(source_type="tender"),
        )
    )

    assert response.trace["rerank_policy"]["enabled"] is True
    assert response.trace["rerank_policy"]["reason"] == "local_default_enablement_matched"
    assert "资质" in response.trace["rerank_policy"]["matched_keywords"]
    assert response.trace["rerank_status"] == "skipped"
    assert response.trace["rerank"]["provider"] == "noop"
    assert response.trace["rerank"]["policy_enabled"] is True


def test_local_default_enablement_skips_non_target_query(monkeypatch):
    monkeypatch.setattr(settings, "rerank_enabled", True)
    monkeypatch.setattr(settings, "rerank_provider", "aliyun")
    monkeypatch.setattr(settings, "rerank_default_enablement_enabled", True)
    monkeypatch.setattr(settings, "rerank_default_enablement_keywords", "资质,要求,条款,截止")
    monkeypatch.setattr(settings, "rerank_default_enablement_source_types", "tender")
    monkeypatch.setattr(settings, "rerank_default_enablement_min_candidates", 2)

    service = RetrievalService(db=None)  # type: ignore[arg-type]
    monkeypatch.setattr(
        service,
        "_sparse_search",
        lambda _request, _filters: [
            SearchResult(
                chunk_id="company-1",
                document_id="doc-company",
                version_id="ver-1",
                text="公司资质概览",
                score=1.0,
                source_type="company_doc",
                retrieval_sources=["sparse"],
                scores={"sparse": 1.0},
            ),
            SearchResult(
                chunk_id="company-2",
                document_id="doc-company",
                version_id="ver-1",
                text="CMMI3 认证",
                score=0.8,
                source_type="company_doc",
                retrieval_sources=["sparse"],
                scores={"sparse": 0.8},
            ),
        ],
    )
    monkeypatch.setattr(service, "_write_log", lambda *args, **kwargs: None)

    response = service.search(
        SearchRequest(query="公司通过了哪些认证？", retrieval_mode="sparse", enable_dense=False, top_k=2)
    )

    assert response.trace["rerank_policy"]["enabled"] is False
    assert response.trace["rerank_policy"]["reason"] == "local_default_enablement_not_matched"
    assert response.trace["rerank_status"] == "skipped"
    assert response.trace["rerank"]["provider"] == "noop"
    assert response.trace["rerank"]["policy_reason"] == "local_default_enablement_not_matched"


def test_local_default_enablement_does_not_unlock_from_candidate_source_types(monkeypatch):
    monkeypatch.setattr(settings, "rerank_enabled", True)
    monkeypatch.setattr(settings, "rerank_provider", "aliyun")
    monkeypatch.setattr(settings, "rerank_default_enablement_enabled", True)
    monkeypatch.setattr(settings, "rerank_default_enablement_keywords", "资质,要求,条款,截止")
    monkeypatch.setattr(settings, "rerank_default_enablement_source_types", "tender")
    monkeypatch.setattr(settings, "rerank_default_enablement_route_types", "tender_query")
    monkeypatch.setattr(settings, "rerank_default_enablement_min_candidates", 2)

    service = RetrievalService(db=None)  # type: ignore[arg-type]
    monkeypatch.setattr(
        service,
        "_sparse_search",
        lambda _request, _filters: [
            SearchResult(
                chunk_id="company-1",
                document_id="doc-company",
                version_id="ver-1",
                text="公司具备安防资质与项目经验",
                score=1.0,
                source_type="company_doc",
                retrieval_sources=["sparse"],
                scores={"sparse": 1.0},
            ),
            SearchResult(
                chunk_id="tender-1",
                document_id="doc-tender",
                version_id="ver-1",
                text="招标文件中的资质要求",
                score=0.9,
                source_type="tender",
                retrieval_sources=["sparse"],
                scores={"sparse": 0.9},
            ),
        ],
    )
    monkeypatch.setattr(service, "_write_log", lambda *args, **kwargs: None)

    response = service.search(
        SearchRequest(query="公司具备什么级别的安防资质？", retrieval_mode="sparse", enable_dense=False, top_k=2)
    )

    assert response.trace["rerank_policy"]["enabled"] is False
    assert response.trace["rerank_policy"]["reason"] == "local_default_enablement_not_matched"
    assert response.trace["rerank_policy"]["source_type_match"] is False
    assert response.trace["rerank_policy"]["route_type_match"] is False
    assert response.trace["rerank_policy"]["candidate_source_types"] == ["company_doc", "tender"]
    assert "资质" in response.trace["rerank_policy"]["matched_keywords"]
    assert response.trace["rerank_status"] == "skipped"
    assert response.trace["rerank"]["policy_reason"] == "local_default_enablement_not_matched"


def test_global_rerank_disable_forces_baseline(monkeypatch):
    monkeypatch.setattr(settings, "rerank_enabled", False)
    monkeypatch.setattr(settings, "rerank_provider", "aliyun")
    monkeypatch.setattr(settings, "rerank_default_enablement_enabled", True)

    service = RetrievalService(db=None)  # type: ignore[arg-type]
    monkeypatch.setattr(
        service,
        "_sparse_search",
        lambda _request, _filters: [
            SearchResult(
                chunk_id="tender-1",
                document_id="doc-tender",
                version_id="ver-1",
                text="招标资质要求正文",
                score=1.0,
                source_type="tender",
                retrieval_sources=["sparse"],
                scores={"sparse": 1.0},
            ),
            SearchResult(
                chunk_id="tender-2",
                document_id="doc-tender",
                version_id="ver-1",
                text="投标截止条款正文",
                score=0.8,
                source_type="tender",
                retrieval_sources=["sparse"],
                scores={"sparse": 0.8},
            ),
        ],
    )
    monkeypatch.setattr(service, "_write_log", lambda *args, **kwargs: None)

    response = service.search(
        SearchRequest(query="智慧园区项目有哪些资质要求？", retrieval_mode="sparse", enable_dense=False, top_k=2)
    )

    assert response.trace["rerank_policy"]["enabled"] is False
    assert response.trace["rerank_policy"]["reason"] == "rerank_globally_disabled"
    assert response.trace["rerank_status"] == "skipped"


def test_local_default_enablement_disable_forces_baseline(monkeypatch):
    monkeypatch.setattr(settings, "rerank_enabled", True)
    monkeypatch.setattr(settings, "rerank_provider", "aliyun")
    monkeypatch.setattr(settings, "rerank_default_enablement_enabled", False)

    service = RetrievalService(db=None)  # type: ignore[arg-type]
    monkeypatch.setattr(
        service,
        "_sparse_search",
        lambda _request, _filters: [
            SearchResult(
                chunk_id="tender-1",
                document_id="doc-tender",
                version_id="ver-1",
                text="招标资质要求正文",
                score=1.0,
                source_type="tender",
                retrieval_sources=["sparse"],
                scores={"sparse": 1.0},
            ),
            SearchResult(
                chunk_id="tender-2",
                document_id="doc-tender",
                version_id="ver-1",
                text="投标截止条款正文",
                score=0.8,
                source_type="tender",
                retrieval_sources=["sparse"],
                scores={"sparse": 0.8},
            ),
        ],
    )
    monkeypatch.setattr(service, "_write_log", lambda *args, **kwargs: None)

    response = service.search(
        SearchRequest(query="智慧园区项目有哪些资质要求？", retrieval_mode="sparse", enable_dense=False, top_k=2)
    )

    assert response.trace["rerank_policy"]["enabled"] is False
    assert response.trace["rerank_policy"]["reason"] == "local_default_enablement_disabled"
    assert response.trace["rerank_status"] == "skipped"


def test_local_default_enablement_fail_open_keeps_trace(monkeypatch):
    monkeypatch.setattr(settings, "rerank_enabled", True)
    monkeypatch.setattr(settings, "rerank_provider", "aliyun")
    monkeypatch.setattr(settings, "rerank_default_enablement_enabled", True)
    monkeypatch.setattr(settings, "rerank_default_enablement_keywords", "资质,要求,条款,截止")
    monkeypatch.setattr(settings, "rerank_default_enablement_source_types", "tender")

    service = RetrievalService(db=None)  # type: ignore[arg-type]

    class BrokenReranker:
        provider = "aliyun_text_rerank"

        def rerank(self, _request):
            raise TimeoutError("provider timeout")

    service.reranker = BrokenReranker()
    monkeypatch.setattr(
        service,
        "_sparse_search",
        lambda _request, _filters: [
            SearchResult(
                chunk_id="tender-1",
                document_id="doc-tender",
                version_id="ver-1",
                text="招标资质要求正文",
                score=1.0,
                source_type="tender",
                retrieval_sources=["sparse"],
                scores={"sparse": 1.0},
            ),
            SearchResult(
                chunk_id="tender-2",
                document_id="doc-tender",
                version_id="ver-1",
                text="投标截止条款正文",
                score=0.8,
                source_type="tender",
                retrieval_sources=["sparse"],
                scores={"sparse": 0.8},
            ),
        ],
    )
    monkeypatch.setattr(service, "_write_log", lambda *args, **kwargs: None)

    response = service.search(
        SearchRequest(
            query="智慧园区项目有哪些资质要求？",
            route_type="tender_query",
            retrieval_mode="sparse",
            enable_dense=False,
            top_k=1,
            filters=RetrievalFilter(source_type="tender"),
        )
    )

    assert response.trace["rerank_policy"]["enabled"] is True
    assert response.trace["rerank_status"] == "failed_open"
    assert response.trace["rerank"]["fail_open"] is True
    assert response.trace["rerank"]["reason"] == "rerank_exception"
    assert response.trace["rerank"]["policy_reason"] == "local_default_enablement_matched"
