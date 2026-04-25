import sys
from pathlib import Path

from app.schemas.retrieval import SearchResponse, SearchResult

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.phase214_regression_eval import EvalCase, evaluate_case_response


def test_eval_case_passes_when_expected_doc_trace_and_fields_match():
    case = EvalCase(
        id="pass",
        query="query",
        filters={},
        expected_document_ids=["doc-a"],
        required_trace_flags={"metadata_snapshot_used": True, "snapshot_as_answer": False},
        required_citation_fields=["sheet_name", "cell_range"],
    )
    response = _response(
        document_ids=["doc-a"],
        metadata={"sheet_name": "报价汇总", "cell_range": "A1:C3"},
        trace={"metadata_snapshot_used": True, "snapshot_as_answer": False},
    )

    result = evaluate_case_response(case, response, latency_ms=12.5)

    assert result.passed is True
    assert result.missing_expected_document_ids == []
    assert result.failed_trace_flags == {}
    assert result.missing_citation_fields == []


def test_eval_case_detects_forbidden_document_id():
    case = EvalCase(
        id="forbidden",
        query="query",
        filters={},
        expected_document_ids=["doc-a"],
        forbidden_document_ids=["doc-b"],
    )
    response = _response(document_ids=["doc-a", "doc-b"])

    result = evaluate_case_response(case, response, latency_ms=1)

    assert result.passed is False
    assert result.unexpected_document_ids == ["doc-b"]
    assert result.forbidden_document_ids == ["doc-b"]


def test_eval_case_detects_missing_citation_fields():
    case = EvalCase(
        id="missing-field",
        query="query",
        filters={},
        expected_document_ids=["doc-a"],
        required_citation_fields=["slide_number", "slide_title"],
    )
    response = _response(document_ids=["doc-a"], metadata={"slide_number": 3})

    result = evaluate_case_response(case, response, latency_ms=1)

    assert result.passed is False
    assert result.missing_citation_fields == ["slide_title"]


def test_eval_case_detects_failed_trace_flags():
    case = EvalCase(
        id="trace",
        query="query",
        filters={},
        expected_document_ids=["doc-a"],
        required_trace_flags={"transcript_as_fact": False, "meeting_transcript_used": True},
    )
    response = _response(
        document_ids=["doc-a"],
        trace={"transcript_as_fact": True, "meeting_transcript_used": True},
    )

    result = evaluate_case_response(case, response, latency_ms=1)

    assert result.passed is False
    assert result.failed_trace_flags == {
        "transcript_as_fact": {"expected": False, "actual": True}
    }


def _response(
    *,
    document_ids: list[str],
    metadata: dict | None = None,
    trace: dict | None = None,
) -> SearchResponse:
    return SearchResponse(
        query="query",
        results=[
            SearchResult(
                chunk_id=f"chunk-{index}",
                document_id=document_id,
                version_id="version",
                text="evidence",
                score=1.0,
                metadata=metadata or {},
            )
            for index, document_id in enumerate(document_ids)
        ],
        backend="test",
        retrieval_mode="sparse",
        trace=trace or {},
    )
