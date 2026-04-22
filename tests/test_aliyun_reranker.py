import httpx

from app.core.config import settings
from app.schemas.retrieval import SearchResult
from app.services.evaluation import summarize_retrieval_spike
from app.services.retrieval.rerank import AliyunTextReranker, RerankRequest
from app.services.retrieval.service import RetrievalService


def _result(chunk_id: str, score: float, text: str = "正文") -> SearchResult:
    return SearchResult(
        chunk_id=chunk_id,
        document_id="doc-1",
        version_id="ver-1",
        text=text,
        score=score,
        source_name="招标文件",
        heading_path=["第一章", "投标要求"],
        retrieval_sources=["dense"],
        scores={"dense": score},
    )


def _request() -> RerankRequest:
    return RerankRequest(
        query="投标截止日期是什么？",
        candidates=[
            _result("chunk-low", 0.1, "无关正文"),
            _result("chunk-high", 0.9, "投标截止日期为2026年4月30日"),
        ],
        top_k=2,
        retrieval_mode="hybrid",
        trace_id="trace-1",
    )


def test_aliyun_reranker_maps_scores_and_order(monkeypatch):
    monkeypatch.setattr(settings, "aliyun_rerank_api_key", "test-key")
    monkeypatch.setattr(settings, "aliyun_embedding_api_key", "embedding-key")
    monkeypatch.setattr(settings, "aliyun_rerank_model", "gte-rerank-v2")
    monkeypatch.setattr(settings, "aliyun_rerank_base_url", "https://dashscope.aliyuncs.com")
    captured = {}

    def fake_post(url, json, headers, timeout, trust_env):
        captured["url"] = url
        captured["json"] = json
        captured["headers"] = headers
        captured["timeout"] = timeout
        captured["trust_env"] = trust_env
        return httpx.Response(
            200,
            request=httpx.Request("POST", url),
            json={
                "request_id": "remote-1",
                "output": {
                    "results": [
                        {"index": 0, "relevance_score": 0.98},
                        {"index": 1, "relevance_score": 0.12},
                    ]
                },
            },
        )

    monkeypatch.setattr(httpx, "post", fake_post)

    outcome = AliyunTextReranker().rerank(_request())

    assert outcome.status == "executed"
    assert outcome.provider == "aliyun_text_rerank"
    assert [item.chunk_id for item in outcome.results] == ["chunk-high", "chunk-low"]
    assert outcome.results[0].scores["rerank"] == 0.98
    assert outcome.results[0].metadata["rerank_score"] == 0.98
    assert outcome.trace["model"] == "gte-rerank-v2"
    assert outcome.trace["remote_request_id"] == "remote-1"
    assert outcome.trace["api_key_source"] == "ALIYUN_RERANK_API_KEY"
    assert outcome.trace["fail_open"] is False
    assert outcome.trace["request_url"] == "https://dashscope.aliyuncs.com/api/v1/services/rerank/text-rerank/text-rerank"
    assert captured["headers"]["Authorization"] == "Bearer test-key"
    assert captured["trust_env"] is False
    assert "标题: 招标文件" in captured["json"]["input"]["documents"][0]
    assert "路径: 第一章 / 投标要求" in captured["json"]["input"]["documents"][0]
    assert "正文: 投标截止日期为2026年4月30日" in captured["json"]["input"]["documents"][0]


def test_aliyun_reranker_missing_api_key_fail_opens(monkeypatch):
    monkeypatch.setattr(settings, "aliyun_rerank_api_key", None)
    monkeypatch.setattr(settings, "aliyun_embedding_api_key", None)

    outcome = AliyunTextReranker().rerank(_request())

    assert outcome.status == "failed_open"
    assert outcome.trace["error_type"] == "missing_api_key"
    assert "ALIYUN_EMBEDDING_API_KEY" in outcome.trace["reason"]
    assert outcome.trace["fail_open"] is True
    assert [item.chunk_id for item in outcome.results] == ["chunk-high", "chunk-low"]


def test_aliyun_reranker_falls_back_to_embedding_api_key(monkeypatch):
    monkeypatch.setattr(settings, "aliyun_rerank_api_key", None)
    monkeypatch.setattr(settings, "aliyun_embedding_api_key", "embedding-key")
    captured = {}

    def fake_post(url, json, headers, timeout, trust_env):
        captured["headers"] = headers
        return httpx.Response(
            200,
            request=httpx.Request("POST", url),
            json={
                "output": {
                    "results": [
                        {"index": 0, "relevance_score": 0.77},
                    ]
                }
            },
        )

    monkeypatch.setattr(httpx, "post", fake_post)

    outcome = AliyunTextReranker().rerank(_request())

    assert outcome.status == "executed"
    assert outcome.trace["api_key_source"] == "ALIYUN_EMBEDDING_API_KEY"
    assert captured["headers"]["Authorization"] == "Bearer embedding-key"


def test_aliyun_reranker_invalid_response_fail_opens(monkeypatch):
    monkeypatch.setattr(settings, "aliyun_rerank_api_key", "test-key")
    monkeypatch.setattr(settings, "aliyun_embedding_api_key", None)
    monkeypatch.setattr(
        httpx,
        "post",
        lambda *args, **kwargs: httpx.Response(
            200,
            request=httpx.Request("POST", args[0] if args else "http://test"),
            json={"output": {"results": [{"index": 99, "relevance_score": 0.8}]}},
        ),
    )

    outcome = AliyunTextReranker().rerank(_request())

    assert outcome.status == "failed_open"
    assert outcome.trace["error_type"] == "invalid_result_index"
    assert outcome.trace["fail_open"] is True
    assert [item.chunk_id for item in outcome.results] == ["chunk-high", "chunk-low"]


def test_aliyun_reranker_normalizes_base_url_and_builds_request_url(monkeypatch):
    monkeypatch.setattr(settings, "aliyun_rerank_api_key", "test-key")
    monkeypatch.setattr(settings, "aliyun_embedding_api_key", None)
    monkeypatch.setattr(settings, "aliyun_rerank_base_url", "dashscope.aliyuncs.com/ ")
    captured = {}

    def fake_post(url, json, headers, timeout, trust_env):
        captured["url"] = url
        return httpx.Response(
            200,
            request=httpx.Request("POST", url),
            json={"output": {"results": [{"index": 0, "relevance_score": 0.77}]}},
        )

    monkeypatch.setattr(httpx, "post", fake_post)

    outcome = AliyunTextReranker().rerank(_request())

    assert outcome.status == "executed"
    assert captured["url"] == "https://dashscope.aliyuncs.com/api/v1/services/rerank/text-rerank/text-rerank"
    assert outcome.trace["raw_base_url"] == "dashscope.aliyuncs.com/ "
    assert outcome.trace["normalized_base_url"] == "https://dashscope.aliyuncs.com"
    assert outcome.trace["request_url"] == captured["url"]


def test_retrieval_service_selects_aliyun_reranker_when_enabled(monkeypatch):
    monkeypatch.setattr(settings, "rerank_enabled", True)
    monkeypatch.setattr(settings, "rerank_provider", "aliyun")

    service = RetrievalService(db=None)  # type: ignore[arg-type]

    assert isinstance(service.reranker, AliyunTextReranker)


def test_spike_summary_reports_hit_rates_latency_and_fail_open():
    summary = summarize_retrieval_spike(
        [
            {
                "top_1_hit": True,
                "top_3_hit": True,
                "top_5_hit": True,
                "elapsed_ms": 10,
                "fail_open": False,
            },
            {
                "top_1_hit": False,
                "top_3_hit": True,
                "top_5_hit": True,
                "elapsed_ms": 30,
                "fail_open": True,
            },
        ]
    )

    assert summary["case_count"] == 2
    assert summary["top_1_hit_rate"] == 0.5
    assert summary["top_3_hit_rate"] == 1.0
    assert summary["top_5_hit_rate"] == 1.0
    assert summary["latency_p50_ms"] == 20.0
    assert summary["latency_p95_ms"] == 30
    assert summary["fail_open_count"] == 1
