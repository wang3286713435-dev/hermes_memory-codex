import importlib.util
import sys
from pathlib import Path

from app.schemas.retrieval import SearchRequest
from app.services.retrieval.service import RetrievalService
from app.services.retrieval.tender_metadata import infer_tender_metadata_fields, snapshot_trace

SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "phase238b_tender_concrete_recall_diagnostics.py"
SPEC = importlib.util.spec_from_file_location("phase238b_tender_concrete_recall_diagnostics", SCRIPT_PATH)
assert SPEC is not None
assert SPEC.loader is not None
diagnostics = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = diagnostics
SPEC.loader.exec_module(diagnostics)


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


def test_personnel_focused_query_uses_personnel_scope_and_aliases():
    service = RetrievalService(db=None)  # type: ignore[arg-type]

    for query in ("人员要求是什么？", "项目人员数量、专业、职称或资质要求是什么？"):
        section_scope = service._infer_section_scope(query)

        assert section_scope["query_profile"] == "personnel_scope"
        assert "项目管理机构" in section_scope["target_sections"]
        assert "主要管理人员" in section_scope["target_sections"]
        assert "技术负责人" in section_scope["query_aliases"]
        assert "专职安全员" in section_scope["query_aliases"]
        assert "人员数量" in section_scope["query_aliases"]
        assert not {
            "项目经理",
            "项目负责人",
            "注册建造师",
            "安全考核证",
            "联合体投标",
            "类似工程业绩",
            "资质要求",
            "资格条件",
            "资格审查文件",
        } & set(section_scope["query_aliases"])
        assert not {
            "联合体投标",
            "类似工程业绩",
            "资信标",
        } & set(section_scope["target_sections"])


def test_broad_qualification_query_is_not_hijacked_by_personnel_scope():
    service = RetrievalService(db=None)  # type: ignore[arg-type]

    section_scope = service._infer_section_scope("投标资质、项目经理、联合体、业绩、人员要求分别是什么？")

    assert section_scope["query_profile"] == "qualification_scope"
    assert "联合体投标" in section_scope["target_sections"]
    assert "类似工程业绩" in section_scope["target_sections"]
    assert "人员要求" in section_scope["target_sections"]


def test_personnel_query_with_excluded_broad_terms_stays_personnel_only():
    service = RetrievalService(db=None)  # type: ignore[arg-type]

    for query in (
        "@主标书 项目人员数量、专业、职称或资质要求是什么？请只回答人员要求，不要回答投标资质、项目经理、联合体、业绩。",
        "项目人员数量、专业、职称或资质要求是什么？请只回答人员要求，不回答投标资质、项目经理、联合体、业绩。",
    ):
        section_scope = service._infer_section_scope(query)

        assert section_scope["query_profile"] == "personnel_scope"
        assert "项目管理机构" in section_scope["target_sections"]
        assert "人员数量" in section_scope["query_aliases"]
        assert not {
            "项目经理",
            "项目负责人",
            "注册建造师",
            "安全考核证",
            "联合体投标",
            "类似工程业绩",
        } & set(section_scope["query_aliases"])
        assert not {"资信标", "联合体投标", "类似工程业绩"} & set(section_scope["target_sections"])


def test_personnel_metadata_ignores_excluded_broad_terms():
    query = "@主标书 项目人员数量、专业、职称或资质要求是什么？请只回答人员要求，不要回答投标资质、项目经理、联合体、业绩。"

    fields = infer_tender_metadata_fields(query)
    trace = snapshot_trace(None, fields)

    assert fields == ["personnel_requirement"]
    assert trace["metadata_deep_field_profile"] == "personnel_scope"


def test_personnel_scope_uses_stronger_personnel_boosts(monkeypatch):
    section_scope, body = _capture_sparse_body(monkeypatch, "项目人员数量、专业、职称或资质要求是什么？")

    shoulds = body["query"]["bool"]["should"]
    assert section_scope["query_profile"] == "personnel_scope"
    assert {"match_phrase": {"text": {"query": "项目管理机构", "boost": 18.0}}} in shoulds
    assert {"match_phrase": {"text": {"query": "人员配备", "boost": 18.0}}} in shoulds
    assert {"match_phrase": {"text": {"query": "技术负责人", "boost": 13.0}}} in shoulds
    assert {"match_phrase": {"text": {"query": "专职安全员", "boost": 13.0}}} in shoulds


def test_personnel_metadata_profile_does_not_turn_generic_qualification_concrete():
    fields = infer_tender_metadata_fields("项目人员数量、专业、职称或资质要求是什么？")
    trace = snapshot_trace(None, fields)

    assert fields == ["personnel_requirement"]
    assert trace["metadata_deep_field_profile"] == "personnel_scope"
    assert trace["deep_field_diagnostics"]["concrete_evidence_required"] is False


def test_diagnostics_expand_only_personnel_query():
    personnel_query = diagnostics.retrieval_query_for_field("personnel_requirement")
    qualification_query = diagnostics.retrieval_query_for_field("qualification_grade_category")

    assert "项目管理机构" in personnel_query
    assert "专职安全员" in personnel_query
    assert "人员数量" in personnel_query
    assert qualification_query == diagnostics.FIELD_QUERIES["qualification_grade_category"]


def test_fixed_policy_fields_remain_outside_personnel_fix():
    price = diagnostics.fixed_policy_diagnostic("price_ceiling")
    project_manager = diagnostics.fixed_policy_diagnostic("project_manager_level")

    assert price["status"] == "field_should_remain_missing_evidence"
    assert project_manager["status"] == "field_requires_human_review"
