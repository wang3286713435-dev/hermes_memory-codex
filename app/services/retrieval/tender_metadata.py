from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class TenderMetadataField:
    field_name: str
    display_name: str
    source_chunk_id: str
    source_text_excerpt: str
    source_location: str
    confidence: float


@dataclass(frozen=True)
class TenderMetadataSnapshot:
    document_id: str
    version_id: str | None
    fields: dict[str, TenderMetadataField]

    def matched(self, field_names: list[str]) -> list[TenderMetadataField]:
        return [self.fields[name] for name in field_names if name in self.fields]


FIELD_RULES: dict[str, dict[str, Any]] = {
    "project_name": {
        "display": "工程名称",
        "triggers": ("工程名称", "项目名称"),
        "positive_patterns": ("工程名称：", "项目名称："),
        "section_hints": ("招标公告", "投标人须知前附表", "工程概况", "项目概况"),
    },
    "project_location": {
        "display": "工程地点",
        "triggers": ("工程地点", "建设地点", "项目地点", "工程地址", "建设地址"),
        "positive_patterns": ("工程地点：", "建设地点：", "工程地址：", "建设地址："),
        "section_hints": ("招标公告", "投标人须知前附表", "工程概况", "项目概况"),
    },
    "tenderer": {
        "display": "招标人",
        "triggers": ("招标人", "发包人"),
        "positive_patterns": ("招标人：", "招标人为", "发包人：", "发包人单位为"),
        "section_hints": ("招标公告", "投标人须知前附表", "工程概况", "项目概况"),
    },
    "construction_unit": {
        "display": "建设单位",
        "triggers": ("建设单位",),
        "positive_patterns": ("建设单位：", "建设单位为", "发包人单位为", "代表建设单位"),
        "section_hints": ("招标公告", "投标人须知前附表", "工程概况", "项目概况"),
    },
    "agent_or_delegate_unit": {
        "display": "代建单位",
        "triggers": ("代建单位", "代建人", "项目代建", "代理建设", "建设管理单位"),
        "positive_patterns": ("代建单位：", "代建单位为", "发包人单位为", "项目代建单位", "代表建设单位"),
        "section_hints": ("招标公告", "投标人须知前附表", "工程概况", "项目概况"),
    },
    "price_ceiling": {
        "display": "最高投标限价",
        "triggers": (
            "最高投标限价",
            "招标控制价",
            "最高限价",
            "投标限价",
            "投标报价上限",
            "报价上限",
            "最高报价",
            "限价金额",
            "控制价",
        ),
        "positive_patterns": (
            "最高投标限价：",
            "最高投标限价为",
            "招标控制价：",
            "招标控制价为",
            "最高限价：",
            "最高限价为",
            "投标报价上限",
            "报价上限",
            "不得超过",
        ),
        "section_hints": ("招标公告", "投标人须知前附表", "工程量清单", "限价明细", "最高投标限价", "招标控制价", "投标报价要求"),
        "precision": "price_amount",
    },
    "duration": {
        "display": "工期",
        "triggers": ("工期", "总工期", "计划工期", "合同工期", "计划开工日期", "计划竣工日期"),
        "section_hints": ("招标公告", "投标人须知前附表", "工期要求", "工程概况"),
    },
    "project_number": {
        "display": "项目编号",
        "triggers": ("项目编号", "招标编号", "工程编号", "标书编号"),
        "section_hints": ("招标公告", "投标人须知前附表"),
    },
    "bid_section": {
        "display": "标段信息",
        "triggers": ("标段", "标段名称", "标段编号"),
        "section_hints": ("招标公告", "投标人须知前附表", "标段划分"),
    },
    "qualification_requirement": {
        "display": "投标资质",
        "triggers": ("投标资质", "资质等级", "资质要求", "施工总承包资质", "专业承包资质", "资格要求", "资格条件", "投标人资格"),
        "positive_patterns": ("投标人资格要求", "资质要求", "资质等级", "具备", "及以上资质"),
        "section_hints": ("投标人须知前附表", "资格审查", "资格后审", "资信标", "资格条件"),
        "precision": "qualification_level",
    },
    "project_manager_requirement": {
        "display": "项目经理资格",
        "triggers": ("项目经理", "项目负责人", "注册建造师", "建造师", "b证", "B证", "安全生产考核", "安全考核"),
        "positive_patterns": ("项目经理须", "项目负责人须", "注册建造师", "安全生产考核", "B证"),
        "section_hints": ("投标人须知前附表", "资格审查", "资格后审", "项目管理机构", "项目经理"),
        "precision": "project_manager_explicit_level",
    },
    "consortium_requirement": {
        "display": "联合体",
        "triggers": ("联合体", "联合体投标", "接受联合体", "不接受联合体"),
        "positive_patterns": ("接受联合体", "不接受联合体", "联合体投标"),
        "section_hints": ("投标人须知前附表", "资格审查", "资格后审", "联合体投标"),
    },
    "performance_requirement": {
        "display": "业绩要求",
        "triggers": ("业绩", "类似工程业绩", "同类工程业绩", "投标人业绩", "项目经理业绩"),
        "positive_patterns": ("类似工程业绩", "同类工程业绩", "投标人业绩", "项目经理业绩"),
        "section_hints": ("投标人须知前附表", "资格审查", "资格后审", "资信标", "业绩"),
    },
    "personnel_requirement": {
        "display": "人员要求",
        "triggers": (
            "人员要求",
            "人员配备",
            "项目管理机构",
            "主要人员",
            "主要管理人员",
            "项目班子",
            "技术负责人",
            "专职安全员",
            "安全员",
            "质量员",
            "施工员",
            "人员数量",
            "人员专业",
            "人员资质",
        ),
        "positive_patterns": (
            "人员要求",
            "人员配备",
            "项目管理机构",
            "主要人员",
            "主要管理人员",
            "项目班子",
            "技术负责人",
            "专职安全员",
        ),
        "section_hints": ("投标人须知前附表", "资格审查", "项目管理机构", "主要人员", "主要管理人员", "人员配备"),
    },
}

FIELD_PROFILES: dict[str, str] = {
    "price_ceiling": "pricing_scope",
    "duration": "schedule_scope",
    "qualification_requirement": "qualification_scope",
    "project_manager_requirement": "qualification_scope",
    "consortium_requirement": "qualification_scope",
    "performance_requirement": "qualification_scope",
    "personnel_requirement": "personnel_scope",
}

CONCRETE_FIELD_REQUIREMENTS: dict[str, dict[str, str]] = {
    "price_ceiling": {
        "evidence": "numeric_amount_with_currency_or_unit",
        "missing_reason": "missing_concrete_price_amount",
    },
    "qualification_requirement": {
        "evidence": "qualification_level_and_category",
        "missing_reason": "missing_concrete_qualification_level_or_category",
    },
    "project_manager_requirement": {
        "evidence": "explicit_project_manager_role_level_requirement",
        "missing_reason": "missing_explicit_project_manager_level",
    },
}


def infer_tender_metadata_fields(query: str) -> list[str]:
    text = normalize_text(query)
    if not text:
        return []
    matched: list[str] = []
    for field_name, rule in FIELD_RULES.items():
        if any(normalize_text(trigger) in text for trigger in rule["triggers"]):
            matched.append(field_name)
    if "personnel_requirement" in matched and _is_personnel_focused_query(text):
        matched = [
            field_name
            for field_name in matched
            if field_name
            not in {
                "qualification_requirement",
                "project_manager_requirement",
                "consortium_requirement",
                "performance_requirement",
            }
        ]
    return matched


def build_tender_metadata_snapshot(document_id: str, chunks: list[Any]) -> TenderMetadataSnapshot:
    fields: dict[str, TenderMetadataField] = {}
    version_id = None
    for field_name, rule in FIELD_RULES.items():
        best = _best_chunk_for_rule(chunks, rule)
        if best is None:
            continue
        chunk, confidence = best
        if version_id is None:
            version_id = getattr(chunk, "version_id", None)
        fields[field_name] = TenderMetadataField(
            field_name=field_name,
            display_name=str(rule["display"]),
            source_chunk_id=str(getattr(chunk, "id", "")),
            source_text_excerpt=_excerpt_for_rule(str(getattr(chunk, "text", "") or ""), rule["triggers"]),
            source_location=_source_location(chunk),
            confidence=confidence,
        )
    return TenderMetadataSnapshot(document_id=document_id, version_id=version_id, fields=fields)


def snapshot_trace(snapshot: TenderMetadataSnapshot | None, matched_fields: list[str]) -> dict[str, Any]:
    guided_profile = _guided_profile(matched_fields)
    if snapshot is None:
        deep_diagnostics = _deep_field_diagnostics(matched_fields, [])
        return {
            "metadata_snapshot_used": False,
            "metadata_snapshot_status": "unavailable",
            "metadata_intent_fields": matched_fields,
            "metadata_fields_matched": matched_fields,
            "metadata_source_chunk_ids": [],
            "source_chunk_ids": [],
            "evidence_required": True,
            "snapshot_as_answer": False,
            "metadata_guided_query_profile": guided_profile,
            "metadata_deep_field_profile": guided_profile,
            "deep_field_missing_reason": deep_diagnostics["missing_reason"],
            "deep_field_diagnostics": deep_diagnostics,
        }
    matched = snapshot.matched(matched_fields)
    matched_field_names = [field.field_name for field in matched]
    guided_profile = _guided_profile(matched_field_names or matched_fields)
    deep_diagnostics = _deep_field_diagnostics(matched_fields, matched_field_names)
    return {
        "metadata_snapshot_used": bool(matched),
        "metadata_snapshot_status": "matched" if matched else "no_field_match",
        "metadata_snapshot_document_id": snapshot.document_id,
        "metadata_snapshot_version_id": snapshot.version_id,
        "metadata_intent_fields": matched_fields,
        "metadata_fields_matched": matched_field_names,
        "metadata_source_chunk_ids": [field.source_chunk_id for field in matched],
        "source_chunk_ids": [field.source_chunk_id for field in matched],
        "metadata_source_locations": {
            field.field_name: field.source_location for field in matched
        },
        "metadata_source_excerpts": {
            field.field_name: field.source_text_excerpt for field in matched
        },
        "metadata_confidence": {
            field.field_name: field.confidence for field in matched
        },
        "evidence_required": True,
        "snapshot_as_answer": False,
        "metadata_guided_query_profile": guided_profile if matched else "default",
        "metadata_deep_field_profile": guided_profile,
        "deep_field_missing_reason": deep_diagnostics["missing_reason"],
        "deep_field_diagnostics": deep_diagnostics,
    }


def normalize_text(value: str) -> str:
    return re.sub(r"\s+", "", value or "").lower()


_PRICE_AMOUNT_PATTERN = re.compile(
    r"(?:人民币|¥|￥)?\s*\d+(?:[,，]\d{3})*(?:\.\d+)?\s*(?:亿元|万元|元|亿|万)"
)
_QUALIFICATION_LEVEL_PATTERN = re.compile(
    r"(?:特级|一级|二级|三级|甲级|乙级|丙级|[一二三]级|壹级|贰级|叁级)"
)
_QUALIFICATION_CATEGORY_PATTERN = re.compile(
    r"(?:施工总承包|专业承包|工程设计|建筑工程|市政公用工程|机电工程|电子与智能化|建筑机电安装|消防设施|智能化工程)"
)
_PRICE_FIELD_KEYWORDS = (
    "最高投标限价",
    "招标控制价",
    "最高限价",
    "投标报价上限",
    "报价上限",
    "投标限价",
    "控制价",
)
_PRICE_PLACEHOLDER_PATTERN = re.compile(r"(详见|另行|后续|附件|清单|公示|通知|按.*执行)")
_PROJECT_MANAGER_REQUIREMENT_PATTERN = re.compile(
    r"(?:项目经理|项目负责人)[^。；;，,]{0,45}"
    r"(?:须具备|应具备|具备|具有|取得|资格要求|资格为|要求为|：|:)"
    r"[^。；;，,]{0,45}"
    r"(?:特级|一级|二级|三级|[一二三]级|壹级|贰级|叁级)"
    r"[^。；;，,]{0,20}(?:注册建造师|建造师)"
)
_PROJECT_MANAGER_E_CERT_ONLY_PATTERN = re.compile(
    r"(?:电子证书|电子证照|证书格式|证书材料|扫描件|签名件|复印件|上传|提供)"
)


def _best_chunk_for_rule(chunks: list[Any], rule: dict[str, Any]) -> tuple[Any, float] | None:
    best: tuple[Any, float, float] | None = None
    for chunk in chunks:
        text = str(getattr(chunk, "text", "") or "")
        heading = " ".join(
            [
                *list(getattr(chunk, "heading_path", None) or []),
                *list(getattr(chunk, "title_path", None) or []),
                *list(getattr(chunk, "section_path", None) or []),
            ]
        )
        haystack = normalize_text(f"{heading} {text}")
        if not haystack:
            continue
        trigger_hits = sum(1 for trigger in rule["triggers"] if normalize_text(trigger) in haystack)
        if trigger_hits <= 0:
            continue
        if not _passes_precision_gate(haystack, rule):
            continue
        section_hits = sum(1 for section in rule["section_hints"] if normalize_text(section) in haystack)
        positive_hits = sum(
            1 for pattern in rule.get("positive_patterns", ()) if normalize_text(pattern) in haystack
        )
        negative_hits = sum(
            1 for pattern in ("投标文件否决性条款", "定标委员会", "定标环节", "定标方案") if normalize_text(pattern) in haystack
        )
        chunk_index = int(getattr(chunk, "chunk_index", 999999) or 0)
        front_matter_bonus = max(0.0, 1.0 - min(chunk_index, 120) / 120)
        score = (
            0.50
            + (trigger_hits * 0.12)
            + (section_hits * 0.08)
            + (positive_hits * 0.22)
            + (front_matter_bonus * 0.06)
            - (negative_hits * 0.24)
        )
        if score < 0.62:
            continue
        confidence = round(min(0.95, score), 3)
        rank_score = confidence - (chunk_index * 0.0001)
        if best is None or rank_score > best[1]:
            best = (chunk, rank_score, confidence)
    if best is None:
        return None
    return best[0], best[2]


def _passes_precision_gate(haystack: str, rule: dict[str, Any]) -> bool:
    precision = rule.get("precision")
    if not precision:
        return True
    if precision == "price_amount":
        return has_concrete_deep_field_evidence("price_ceiling", haystack)
    if precision == "qualification_level":
        return has_concrete_deep_field_evidence("qualification_requirement", haystack)
    if precision == "project_manager_explicit_level":
        return has_concrete_deep_field_evidence("project_manager_requirement", haystack)
    return True


def has_concrete_deep_field_evidence(field_name: str, text: str) -> bool:
    haystack = normalize_text(text)
    if not haystack:
        return False
    if field_name == "price_ceiling":
        return _has_concrete_price_ceiling(haystack)
    if field_name == "qualification_requirement":
        return bool(
            "资质" in haystack
            and _QUALIFICATION_LEVEL_PATTERN.search(haystack)
            and _QUALIFICATION_CATEGORY_PATTERN.search(haystack)
        )
    if field_name == "project_manager_requirement":
        return _has_explicit_project_manager_level(haystack)
    return False


def concrete_deep_field_missing_reason(field_name: str) -> str | None:
    requirement = CONCRETE_FIELD_REQUIREMENTS.get(field_name)
    if not requirement:
        return None
    return requirement["missing_reason"]


def _has_concrete_price_ceiling(haystack: str) -> bool:
    for clause in _semantic_clauses(haystack):
        if not any(keyword in clause for keyword in _PRICE_FIELD_KEYWORDS):
            continue
        if not _PRICE_AMOUNT_PATTERN.search(clause):
            continue
        if _PRICE_PLACEHOLDER_PATTERN.search(clause) and "不得超过" not in clause:
            continue
        return True
    return False


def _has_explicit_project_manager_level(haystack: str) -> bool:
    for clause in _semantic_clauses(haystack):
        if not _PROJECT_MANAGER_REQUIREMENT_PATTERN.search(clause):
            continue
        if _PROJECT_MANAGER_E_CERT_ONLY_PATTERN.search(clause) and not any(
            token in clause for token in ("须具备", "应具备", "具备", "具有", "资格要求", "资格为", "要求为")
        ):
            continue
        return True
    return False


def _semantic_clauses(haystack: str) -> list[str]:
    return [clause for clause in re.split(r"[。；;！？!?，,\n\r]+", haystack) if clause]


def _excerpt_for_rule(text: str, triggers: tuple[str, ...]) -> str:
    normalized_text = text or ""
    for trigger in triggers:
        index = normalized_text.find(trigger)
        if index >= 0:
            start = max(0, index - 80)
            end = min(len(normalized_text), index + 220)
            return normalized_text[start:end].strip()
    return normalized_text[:300].strip()


def _source_location(chunk: Any) -> str:
    heading = [
        *list(getattr(chunk, "heading_path", None) or []),
        *list(getattr(chunk, "title_path", None) or []),
        *list(getattr(chunk, "section_path", None) or []),
    ]
    location = " > ".join(str(part) for part in heading if part)
    if location:
        return location
    return f"chunk_index={getattr(chunk, 'chunk_index', None)}"


def _guided_profile(field_names: list[str]) -> str:
    if set(field_names) == {"personnel_requirement"}:
        return "personnel_scope"
    priority = {
        "default": 0,
        "tender_basic_info": 1,
        "schedule_scope": 2,
        "pricing_scope": 3,
        "qualification_scope": 3,
        "personnel_scope": 3,
    }
    profile = "tender_basic_info" if field_names else "default"
    for field_name in field_names:
        candidate = FIELD_PROFILES.get(field_name, "tender_basic_info")
        if priority.get(candidate, 0) > priority.get(profile, 0):
            profile = candidate
    return profile


def _is_personnel_focused_query(normalized_query: str) -> bool:
    if not normalized_query:
        return False
    positive_intent_text = _without_excluded_intent_terms(normalized_query)
    personnel_signals = (
        "人员要求",
        "人员配备",
        "人员数量",
        "人员专业",
        "人员资质",
        "项目人员",
        "项目管理机构",
        "项目班子",
        "主要人员",
        "主要管理人员",
        "技术负责人",
        "专职安全员",
        "安全员",
        "质量员",
        "施工员",
    )
    if not any(signal in positive_intent_text for signal in personnel_signals):
        return False
    broad_qualification_signals = ("投标资质", "项目经理", "联合体", "类似业绩", "同类工程业绩", "投标人业绩")
    return not any(signal in positive_intent_text for signal in broad_qualification_signals)


def _without_excluded_intent_terms(normalized_query: str) -> str:
    text = normalized_query or ""
    for marker in ("不要回答", "不要包含", "不回答", "不包含", "排除", "无需回答", "不要", "无需"):
        index = text.find(marker)
        if index >= 0:
            text = text[:index]
    return text


def _deep_field_diagnostics(intent_fields: list[str], matched_fields: list[str]) -> dict[str, Any]:
    intent = list(dict.fromkeys(intent_fields))
    matched = list(dict.fromkeys(matched_fields))
    matched_set = set(matched)
    required_fields = [field for field in intent if field in CONCRETE_FIELD_REQUIREMENTS]
    missing_fields = [field for field in required_fields if field not in matched_set]
    matched_required_fields = [field for field in required_fields if field in matched_set]
    missing_reasons = [
        CONCRETE_FIELD_REQUIREMENTS[field]["missing_reason"] for field in missing_fields
    ]
    required_evidence = {
        field: CONCRETE_FIELD_REQUIREMENTS[field]["evidence"] for field in required_fields
    }
    diagnostics = {
        "status": _deep_field_status(required_fields, missing_fields),
        "intent_fields": intent,
        "matched_fields": matched,
        "concrete_evidence_required": bool(required_fields),
        "concrete_evidence_required_fields": required_fields,
        "concrete_evidence_matched_fields": matched_required_fields,
        "concrete_evidence_missing_fields": missing_fields,
        "required_evidence": required_evidence,
        "missing_reasons": missing_reasons,
        "missing_reason": missing_reasons[0] if len(missing_reasons) == 1 else (missing_reasons or None),
    }
    if "project_manager_requirement" in intent:
        project_manager_level_explicit = "project_manager_requirement" in matched_set
        diagnostics["project_manager_level_explicit"] = project_manager_level_explicit
        if not project_manager_level_explicit:
            diagnostics["project_manager_level_missing_reason"] = (
                "electronic_certificate_format_is_not_role_level_requirement"
            )
    return diagnostics


def _deep_field_status(required_fields: list[str], missing_fields: list[str]) -> str:
    if not required_fields:
        return "not_concrete_deep_field"
    if missing_fields:
        return "missing_concrete_evidence"
    return "concrete_evidence_found"
