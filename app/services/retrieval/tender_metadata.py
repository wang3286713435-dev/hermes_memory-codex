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
        "triggers": ("最高投标限价", "招标控制价", "最高限价", "投标限价"),
        "section_hints": ("招标公告", "投标人须知前附表", "工程量清单", "限价明细"),
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
}


def infer_tender_metadata_fields(query: str) -> list[str]:
    text = normalize_text(query)
    if not text:
        return []
    matched: list[str] = []
    for field_name, rule in FIELD_RULES.items():
        if any(normalize_text(trigger) in text for trigger in rule["triggers"]):
            matched.append(field_name)
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
    if snapshot is None:
        return {
            "metadata_snapshot_used": False,
            "metadata_snapshot_status": "unavailable",
            "metadata_fields_matched": matched_fields,
            "metadata_source_chunk_ids": [],
            "source_chunk_ids": [],
            "evidence_required": True,
            "snapshot_as_answer": False,
        }
    matched = snapshot.matched(matched_fields)
    return {
        "metadata_snapshot_used": bool(matched),
        "metadata_snapshot_status": "matched" if matched else "no_field_match",
        "metadata_snapshot_document_id": snapshot.document_id,
        "metadata_snapshot_version_id": snapshot.version_id,
        "metadata_fields_matched": [field.field_name for field in matched],
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
        "metadata_guided_query_profile": "tender_basic_info" if matched else "default",
    }


def normalize_text(value: str) -> str:
    return re.sub(r"\s+", "", value or "").lower()


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
