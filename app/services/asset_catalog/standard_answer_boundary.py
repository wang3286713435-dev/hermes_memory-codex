from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal

StandardAnswerMode = Literal["missing_evidence", "current_lineage"]
RiskOfOverclaim = Literal["low", "medium", "high"]

FORBIDDEN_STANDARD_BOUNDARY_FIELDS: tuple[str, ...] = (
    "storage_path",
    "raw_row",
    "secret",
    "token",
    "bearer",
    "credential",
    "SELECT ",
    "INSERT ",
    "UPDATE ",
    "DELETE ",
    "nas://",
    "smb://",
    "/Volumes/",
)


@dataclass(frozen=True)
class StandardAnswerBoundary:
    answer_mode: StandardAnswerMode
    can_answer: bool
    missing_evidence: bool
    required_evidence: tuple[str, ...]
    template: str
    rule_scope: str
    risk_of_overclaim: RiskOfOverclaim
    facts_from_catalog_metadata: bool = False
    writes_documents: bool = False
    writes_chunks: bool = False
    writes_opensearch: bool = False
    writes_qdrant: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "answer_mode": self.answer_mode,
            "can_answer": self.can_answer,
            "missing_evidence": self.missing_evidence,
            "required_evidence": list(self.required_evidence),
            "template": self.template,
            "rule_scope": self.rule_scope,
            "risk_of_overclaim": self.risk_of_overclaim,
            "facts_from_catalog_metadata": self.facts_from_catalog_metadata,
            "writes_documents": self.writes_documents,
            "writes_chunks": self.writes_chunks,
            "writes_opensearch": self.writes_opensearch,
            "writes_qdrant": self.writes_qdrant,
        }


class StandardAnswerBoundaryClassifier:
    def classify(self, query: str) -> StandardAnswerBoundary:
        normalized = query.casefold()
        if self._looks_like_dwg_content_question(normalized):
            return self._missing_evidence(
                required_evidence="dwg_parse_evidence",
                rule_scope="DWG content boundary",
                template=(
                    "Missing Evidence: 当前只有目录级 metadata；缺少 "
                    "dwg_parse_evidence，不能回答 DWG 图层、标题栏、外部参照、"
                    "块属性、注释、坐标或图纸内容。"
                ),
            )
        if self._looks_like_rvt_content_question(normalized):
            return self._missing_evidence(
                required_evidence="rvt_parse_evidence",
                rule_scope="RVT content boundary",
                template=(
                    "Missing Evidence: 当前只有目录级 metadata；缺少 "
                    "rvt_parse_evidence，不能回答 RVT Level、Grid、Sheet、View、"
                    "Family、Type 或模型内部内容。"
                ),
            )
        if self._looks_like_bim_component_question(normalized):
            return self._missing_evidence(
                required_evidence="component_evidence",
                rule_scope="BIM component boundary",
                template=(
                    "Missing Evidence: 当前缺少 component_evidence 或 manual_evidence，"
                    "不能回答 BIM 构件存在性、构件清单、参数、LOD 或 LOI。"
                ),
            )
        if self._looks_like_pdf_or_office_content_question(normalized):
            return self._missing_evidence(
                required_evidence="full_text_evidence",
                rule_scope="PDF/Office content boundary",
                template=(
                    "Missing Evidence: 当前只有目录级 metadata；缺少 "
                    "full_text_evidence，不能总结或确认 PDF / Office 文件正文内容。"
                ),
            )
        return self._lineage_boundary(query)

    def _missing_evidence(
        self,
        *,
        required_evidence: str,
        rule_scope: str,
        template: str,
    ) -> StandardAnswerBoundary:
        return StandardAnswerBoundary(
            answer_mode="missing_evidence",
            can_answer=False,
            missing_evidence=True,
            required_evidence=(required_evidence,),
            template=template,
            rule_scope=rule_scope,
            risk_of_overclaim="high",
        )

    def _lineage_boundary(self, query: str) -> StandardAnswerBoundary:
        rule_scope = "A004-A010" if "a004" in query.casefold() or "a010" in query.casefold() else "catalog_lineage"
        return StandardAnswerBoundary(
            answer_mode="current_lineage",
            can_answer=True,
            missing_evidence=False,
            required_evidence=("catalog_metadata",),
            template=(
                "目录/文件名/脱敏路径线索显示……；该回答只表示目录级 lineage "
                "clue，不得作为强事实或合规结论，不能确认内容理解、合规结论或正式交付完整性。"
            ),
            rule_scope=rule_scope,
            risk_of_overclaim="medium",
        )

    def _looks_like_dwg_content_question(self, query: str) -> bool:
        return "dwg" in query and any(
            token in query
            for token in (
                "图层",
                "layer",
                "标题栏",
                "title block",
                "外部参照",
                "xref",
                "块属性",
                "block",
                "坐标",
                "coordinate",
                "图纸内容",
            )
        )

    def _looks_like_rvt_content_question(self, query: str) -> bool:
        return ("rvt" in query or "revit" in query) and any(
            token in query
            for token in (
                "level",
                "grid",
                "sheet",
                "view",
                "family",
                "type",
                "标高",
                "轴网",
                "视图",
                "族",
            )
        )

    def _looks_like_bim_component_question(self, query: str) -> bool:
        return any(token in query for token in ("构件", "component", "lod", "loi")) and any(
            token in query
            for token in (
                "参数",
                "parameter",
                "清单",
                "list",
                "存在",
                "exist",
                "lod",
                "loi",
            )
        )

    def _looks_like_pdf_or_office_content_question(self, query: str) -> bool:
        return any(
            token in query
            for token in (
                "pdf",
                "office",
                "word",
                "doc",
                "docx",
                "excel",
                "xls",
                "xlsx",
                "ppt",
                "pptx",
            )
        ) and any(
            token in query
            for token in (
                "正文",
                "内容",
                "总结",
                "summarize",
                "全文",
                "full text",
            )
        )


def build_memory_reference_boundary() -> dict[str, Any]:
    return {
        "allowed_references": [
            "related_file_ids",
            "query_id",
            "project_id",
            "feedback_labels",
        ],
        "content_proof": False,
        "can_store_nas_content": False,
        "template": (
            "Hermes memory 可以保存低敏引用，例如 related_file_ids、query_id、project_id "
            "和 feedback labels；这些引用不能证明 Hermes 已读取或记住 NAS 文件内容。"
        ),
    }
