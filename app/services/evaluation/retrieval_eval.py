from dataclasses import dataclass, field
from statistics import mean, median

from app.schemas.retrieval import SearchResponse


@dataclass(frozen=True)
class RetrievalEvalCase:
    query: str
    case_id: str | None = None
    expected_chunk_ids: set[str] = field(default_factory=set)
    expected_document_ids: set[str] = field(default_factory=set)
    notes: str | None = None


def evaluate_retrieval_response(case: RetrievalEvalCase, response: SearchResponse) -> dict:
    """Minimal retrieval evaluation entry for future rerank evaluation work."""
    returned_ids = [item.chunk_id for item in response.results]
    returned_document_ids = [item.document_id for item in response.results]
    expected_hits = [chunk_id for chunk_id in returned_ids if chunk_id in case.expected_chunk_ids]
    expected_document_hits = [
        document_id for document_id in returned_document_ids if document_id in case.expected_document_ids
    ]
    top_1_ids = returned_ids[:1]
    top_3_ids = returned_ids[:3]
    top_5_ids = returned_ids[:5]
    top_1_docs = returned_document_ids[:1]
    top_3_docs = returned_document_ids[:3]
    top_5_docs = returned_document_ids[:5]

    top_1_hit = bool(set(top_1_ids) & case.expected_chunk_ids or set(top_1_docs) & case.expected_document_ids)
    top_3_hit = bool(set(top_3_ids) & case.expected_chunk_ids or set(top_3_docs) & case.expected_document_ids)
    top_5_hit = bool(set(top_5_ids) & case.expected_chunk_ids or set(top_5_docs) & case.expected_document_ids)
    return {
        "case_id": case.case_id,
        "query": case.query,
        "returned_count": len(returned_ids),
        "expected_count": len(case.expected_chunk_ids),
        "hit_count": len(expected_hits),
        "hit_chunk_ids": expected_hits,
        "hit_document_ids": expected_document_hits,
        "has_expected_hit": bool(expected_hits or expected_document_hits),
        "top_1_hit": top_1_hit,
        "top_3_hit": top_3_hit,
        "top_5_hit": top_5_hit,
        "rerank_status": response.trace.get("rerank_status"),
        "fail_open": bool(response.trace.get("rerank", {}).get("fail_open")),
        "elapsed_ms": float(response.trace.get("rerank", {}).get("elapsed_ms") or 0.0),
        "candidate_pool": response.trace.get("candidate_pool", {}),
    }


def summarize_retrieval_spike(reports: list[dict]) -> dict:
    """Summarize a small baseline-vs-experiment retrieval spike."""
    if not reports:
        return {
            "case_count": 0,
            "top_1_hit_rate": 0.0,
            "top_3_hit_rate": 0.0,
            "top_5_hit_rate": 0.0,
            "latency_avg_ms": 0.0,
            "latency_p50_ms": 0.0,
            "latency_p95_ms": 0.0,
            "fail_open_count": 0,
        }

    latencies = sorted(float(report.get("elapsed_ms") or 0.0) for report in reports)
    return {
        "case_count": len(reports),
        "top_1_hit_rate": _hit_rate(reports, "top_1_hit"),
        "top_3_hit_rate": _hit_rate(reports, "top_3_hit"),
        "top_5_hit_rate": _hit_rate(reports, "top_5_hit"),
        "latency_avg_ms": round(mean(latencies), 3),
        "latency_p50_ms": round(median(latencies), 3),
        "latency_p95_ms": round(_percentile(latencies, 95), 3),
        "fail_open_count": sum(1 for report in reports if report.get("fail_open")),
    }


def _hit_rate(reports: list[dict], field: str) -> float:
    return round(sum(1 for report in reports if report.get(field)) / len(reports), 4)


def _percentile(values: list[float], percentile: int) -> float:
    if not values:
        return 0.0
    if len(values) == 1:
        return values[0]
    index = min(len(values) - 1, round((percentile / 100) * (len(values) - 1)))
    return values[index]
