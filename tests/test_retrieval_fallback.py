from app.services.retrieval.service import RetrievalService


def test_simplify_query_terms_prefers_meaningful_keywords():
    service = RetrievalService(db=None)  # type: ignore[arg-type]
    terms = service._simplify_query_terms("请查一下星河项目招标资料里的投标截止日期是什么")
    assert "星河项目" in terms
    assert "招标资料" in terms
    assert "投标截止日期" in terms
    assert len(terms) <= 4


def test_simplify_query_terms_handles_short_plain_query():
    service = RetrievalService(db=None)  # type: ignore[arg-type]
    terms = service._simplify_query_terms("投标截止日期")
    assert terms[0] == "投标截止日期"

