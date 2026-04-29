from app.schemas.retrieval import SearchRequest
from app.services.retrieval.service import RetrievalService


class _FakeIndices:
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


def _capture_sparse_body(monkeypatch, query: str):
    captured = {}

    class FakeClient:
        def __init__(self, *_args, **_kwargs):
            self.indices = _FakeIndices()

        def search(self, *, index, body):
            captured["body"] = body
            return {"hits": {"hits": []}}

    monkeypatch.setattr("app.services.retrieval.service.OpenSearch", FakeClient)
    service = RetrievalService(db=None)  # type: ignore[arg-type]
    section_scope = service._infer_section_scope(query)
    service._sparse_search(
        SearchRequest(query=query, top_k=5),
        {"source_type": "tender", "document_id": "doc-1", "document_type": "tender", "is_latest": True},
        section_scope,
    )
    return section_scope, captured["body"]


def test_price_ceiling_query_uses_pricing_profile_and_strong_limit_phrases(monkeypatch):
    section_scope, body = _capture_sparse_body(monkeypatch, "最高投标限价和招标控制价是多少？")

    shoulds = body["query"]["bool"]["should"]
    assert section_scope["query_profile"] == "pricing_scope"
    assert "投标人须知前附表" in section_scope["target_sections"]
    assert "工程量清单" in section_scope["target_sections"]
    assert {"match_phrase": {"text": {"query": "最高投标限价", "boost": 16.0}}} in shoulds
    assert {"match_phrase": {"text": {"query": "招标控制价", "boost": 16.0}}} in shoulds
    assert {"match_phrase": {"text": {"query": "投标报价上限", "boost": 12.0}}} in shoulds


def test_qualification_query_covers_consortium_performance_and_personnel(monkeypatch):
    section_scope, body = _capture_sparse_body(monkeypatch, "投标资质、项目经理、联合体、业绩、人员要求分别是什么？")

    shoulds = body["query"]["bool"]["should"]
    assert section_scope["query_profile"] == "qualification_scope"
    assert "联合体投标" in section_scope["target_sections"]
    assert "类似工程业绩" in section_scope["target_sections"]
    assert "人员要求" in section_scope["target_sections"]
    assert {"match_phrase": {"text": {"query": "投标人资格要求", "boost": 16.0}}} in shoulds
    assert {"match_phrase": {"text": {"query": "联合体投标", "boost": 10.0}}} in shoulds
    assert {"match_phrase": {"text": {"query": "类似工程业绩", "boost": 10.0}}} in shoulds
    assert {"match_phrase": {"text": {"query": "人员配备", "boost": 8.0}}} in shoulds
