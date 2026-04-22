from app.memory_kernel.citation_generator import CitationGenerator
from app.memory_kernel.context_builder import ContextBuilder
from app.memory_kernel.contracts import QueryRoute
from app.schemas.retrieval import SearchResponse, SearchResult


def _result(chunk_id: str, source: str) -> SearchResult:
    return SearchResult(
        chunk_id=chunk_id,
        document_id="doc-1",
        version_id="ver-1",
        text=f"{source} retrieval text",
        score=1.0,
        source_name="企业资料",
        source_uri="local://doc-1",
        source_type="upload",
        heading_path=["一级标题", source],
        page_start=1,
        page_end=2,
        retrieval_sources=[source],
        scores={source: 1.0},
    )


def _response(mode: str, results: list[SearchResult]) -> SearchResponse:
    return SearchResponse(
        query="投标截止日期",
        results=results,
        backend=mode,
        retrieval_mode=mode,  # type: ignore[arg-type]
        dense_status="executed" if mode in {"dense", "hybrid"} else "skipped",
        sparse_status="executed" if mode in {"sparse", "hybrid"} else "skipped",
        dense_retrieval_status="executed" if mode in {"dense", "hybrid"} else "skipped",
        applied_filters={"source_type": "upload"},
        ignored_filters={},
        trace={
            "dense": {"status": "executed"} if mode in {"dense", "hybrid"} else {"status": "skipped"},
            "sparse": {"status": "executed"} if mode in {"sparse", "hybrid"} else {"status": "skipped"},
            "hybrid": {"status": "executed"} if mode == "hybrid" else {"status": "skipped"},
        },
    )


def test_context_builder_accepts_dense_sparse_and_hybrid_results():
    builder = ContextBuilder()
    citations = CitationGenerator()

    cases = {
        "dense": [_result("chunk-dense", "dense")],
        "sparse": [_result("chunk-sparse", "sparse")],
        "hybrid": [
            SearchResult(
                chunk_id="chunk-shared",
                document_id="doc-1",
                version_id="ver-1",
                text="hybrid retrieval text",
                score=2.0,
                source_name="企业资料",
                source_uri="local://doc-1",
                source_type="upload",
                heading_path=["一级标题", "hybrid"],
                page_start=1,
                page_end=2,
                retrieval_sources=["dense", "sparse"],
                scores={"dense": 0.8, "sparse": 1.2},
            )
        ],
    }

    for mode, results in cases.items():
        response = _response(mode, results)
        generated_citations = citations.generate(response.results)
        context = builder.build(
            query=response.query,
            route=QueryRoute(route_type="document_knowledge", retrieval_mode=mode, reason="test"),
            search_response=response,
            citations=generated_citations,
        )

        assert len(context.items) == 1
        assert len(context.citations) == 1
        assert context.items[0].chunk_id == results[0].chunk_id
        assert context.items[0].document_id == "doc-1"
        assert context.items[0].heading_path[-1] == mode
        assert context.citations[0].chunk_id == results[0].chunk_id
        assert context.retrieval_mode == mode
        assert context.applied_filters == {"source_type": "upload"}


def test_citation_generation_uses_unified_result_contract_only():
    result = SearchResult(
        chunk_id="chunk-hybrid",
        document_id="doc-1",
        version_id="ver-1",
        text="hybrid citation text",
        score=2.0,
        source_name="企业资料",
        source_uri="local://doc-1",
        heading_path=["章", "节"],
        page_start=3,
        page_end=4,
        retrieval_sources=["dense", "sparse"],
        scores={"dense": 0.9, "sparse": 1.1},
    )

    citation = CitationGenerator().generate([result])[0]

    assert citation.document_id == "doc-1"
    assert citation.version_id == "ver-1"
    assert citation.chunk_id == "chunk-hybrid"
    assert citation.heading_path == ["章", "节"]
    assert citation.page_start == 3
    assert citation.page_end == 4
    assert citation.quote_text == "hybrid citation text"
