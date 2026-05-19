from __future__ import annotations

import pytest

from app.services.asset_catalog.standard_answer_boundary import (
    FORBIDDEN_STANDARD_BOUNDARY_FIELDS,
    StandardAnswerBoundaryClassifier,
    build_memory_reference_boundary,
)


@pytest.mark.parametrize(
    ("query", "expected_evidence"),
    [
        ("这个 DWG 图纸的图层和标题栏是否合规？", "dwg_parse_evidence"),
        ("检查 dwg 外部参照、块属性和坐标内容", "dwg_parse_evidence"),
        ("RVT 模型里 Level/Grid/Sheet/View/Family/Type 是否完整？", "rvt_parse_evidence"),
        ("这个 BIM 构件参数、LOD、LOI 和构件清单是什么？", "component_evidence"),
        ("请总结这个 PDF/Office 文件正文内容", "full_text_evidence"),
        ("请总结这个 docx 文件正文内容", "full_text_evidence"),
        ("请总结这个 xlsx 表格正文内容", "full_text_evidence"),
    ],
)
def test_content_level_questions_return_missing_evidence_templates(
    query: str,
    expected_evidence: str,
) -> None:
    boundary = StandardAnswerBoundaryClassifier().classify(query)

    assert boundary.answer_mode == "missing_evidence"
    assert boundary.can_answer is False
    assert boundary.required_evidence == (expected_evidence,)
    assert boundary.missing_evidence is True
    assert boundary.facts_from_catalog_metadata is False
    assert boundary.writes_documents is False
    assert boundary.writes_chunks is False
    assert boundary.writes_opensearch is False
    assert boundary.writes_qdrant is False
    assert expected_evidence in boundary.template


def test_catalog_lineage_answers_are_clues_not_factual_conclusions() -> None:
    boundary = StandardAnswerBoundaryClassifier().classify(
        "根据目录、文件名、脱敏路径线索判断专业、阶段和图号",
    )

    assert boundary.answer_mode == "current_lineage"
    assert boundary.can_answer is True
    assert boundary.required_evidence == ("catalog_metadata",)
    assert boundary.missing_evidence is False
    assert "目录/文件名/脱敏路径线索显示" in boundary.template
    assert "不能确认内容理解、合规结论或正式交付完整性" in boundary.template
    assert "确认该文件内容合规" not in boundary.template
    assert "已读取 NAS 文件内容" not in boundary.template


def test_a004_to_a010_are_sometimes_lineage_only_not_strong_facts() -> None:
    boundary = StandardAnswerBoundaryClassifier().classify("A004-A010 命名、专业、阶段、版本是否满足标准？")

    assert boundary.rule_scope == "A004-A010"
    assert boundary.answer_mode == "current_lineage"
    assert boundary.risk_of_overclaim == "medium"
    assert boundary.can_answer is True
    assert "线索" in boundary.template
    assert "不得作为强事实或合规结论" in boundary.template


def test_templates_do_not_expose_forbidden_fields_or_claim_runtime_writes() -> None:
    classifier = StandardAnswerBoundaryClassifier()
    boundaries = [
        classifier.classify("DWG 图层内容"),
        classifier.classify("RVT Family Type"),
        classifier.classify("BIM 构件参数"),
        classifier.classify("PDF 正文内容"),
        classifier.classify("目录文件名线索"),
    ]

    for boundary in boundaries:
        payload = boundary.to_dict()
        serialized = str(payload)
        for forbidden in FORBIDDEN_STANDARD_BOUNDARY_FIELDS:
            assert forbidden not in serialized
        assert payload["writes_documents"] is False
        assert payload["writes_chunks"] is False
        assert payload["writes_opensearch"] is False
        assert payload["writes_qdrant"] is False


def test_memory_reference_boundary_is_low_sensitive_not_content_proof() -> None:
    boundary = build_memory_reference_boundary()

    assert boundary["allowed_references"] == [
        "related_file_ids",
        "query_id",
        "project_id",
        "feedback_labels",
    ]
    assert boundary["content_proof"] is False
    assert boundary["can_store_nas_content"] is False
    assert boundary["template"].startswith("Hermes memory 可以保存低敏引用")
    assert "不能证明 Hermes 已读取或记住 NAS 文件内容" in boundary["template"]
