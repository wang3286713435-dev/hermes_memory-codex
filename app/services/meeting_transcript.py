from __future__ import annotations

import re
from typing import Any


MEETING_SCOPE_VALUES = {
    "meeting",
    "meeting_minutes",
    "meeting_transcript",
    "transcript",
}

MEETING_TITLE_HINTS = ("会议", "纪要", "转写", "transcript", "meeting")
DECISION_HINTS = ("决定", "决议", "确认", "同意", "通过", "结论", "明确")
ACTION_HINTS = ("行动项", "待办", "负责", "跟进", "落实", "推进", "完成", "截止", "后续", "计划")
RISK_HINTS = ("风险", "隐患", "问题", "待确认", "不确定", "缺口", "困难")
SPEAKER_EXCLUDE = {
    "会议主题",
    "会议时间",
    "会议目的",
    "项目内容",
    "问题一",
    "问题二",
    "问题三",
    "方案",
    "风险",
    "结论",
}


def is_meeting_document(
    *,
    source_type: str | None = None,
    document_type: str | None = None,
    title: str | None = None,
    source_uri: str | None = None,
) -> bool:
    values = {str(source_type or "").lower(), str(document_type or "").lower()}
    if values & MEETING_SCOPE_VALUES:
        return True
    haystack = f"{title or ''} {source_uri or ''}".lower()
    return any(hint.lower() in haystack for hint in MEETING_TITLE_HINTS)


def enrich_meeting_metadata(
    *,
    text: str,
    metadata: dict[str, Any] | None = None,
    source_type: str | None = None,
    document_type: str | None = None,
    source_name: str | None = None,
    source_uri: str | None = None,
    source_location: str | None = None,
    source_chunk_id: str | None = None,
) -> dict[str, Any]:
    base = dict(metadata or {})
    if not is_meeting_document(
        source_type=source_type,
        document_type=document_type,
        title=source_name,
        source_uri=source_uri,
    ):
        return base

    extracted = extract_meeting_fields(text)
    fields = []
    for field in ("speaker", "timestamp", "topic", "decision", "action_item", "owner", "deadline", "risk"):
        value = extracted.get(field)
        if value:
            fields.append(field)

    confidence = 0.42 + min(0.45, len(fields) * 0.06)
    enriched = {
        **base,
        "content_profile": "meeting_transcript",
        "meeting_transcript": True,
        "meeting_fields": fields,
        "meeting_fields_matched": fields,
        "speaker": extracted.get("speaker"),
        "speakers": extracted.get("speakers", []),
        "timestamp": extracted.get("timestamp"),
        "timestamps": extracted.get("timestamps", []),
        "timestamp_missing": not bool(extracted.get("timestamps")),
        "topic": extracted.get("topic", []),
        "decision": extracted.get("decision", []),
        "action_item": extracted.get("action_item", []),
        "owner": extracted.get("owner", []),
        "deadline": extracted.get("deadline", []),
        "risk": extracted.get("risk", []),
        "source_location": source_location or base.get("source_location") or "chunk_text",
        "source_text_excerpt": _excerpt(text),
        "confidence": round(min(0.95, confidence), 3),
        "transcript_as_fact": False,
        "evidence_required": True,
    }
    if source_chunk_id:
        enriched["source_chunk_id"] = source_chunk_id
    return enriched


def extract_meeting_fields(text: str) -> dict[str, Any]:
    lines = [line.strip() for line in (text or "").splitlines() if line.strip()]
    speakers = _unique(_speaker_from_line(line) for line in lines)
    timestamps = _unique(_timestamp_matches(text or ""))
    topics = _keyword_lines(lines, ("会议主题", "议题", "项目内容", "会议目的"))
    decisions = _keyword_lines(lines, DECISION_HINTS)
    actions = _keyword_lines(lines, ACTION_HINTS)
    risks = _keyword_lines(lines, RISK_HINTS)
    owners = _owners_from_lines(lines)
    deadlines = _unique(_deadline_matches(text or ""))
    return {
        "speaker": speakers[0] if speakers else None,
        "speakers": speakers[:8],
        "timestamp": timestamps[0] if timestamps else None,
        "timestamps": timestamps[:8],
        "topic": topics[:5],
        "decision": decisions[:5],
        "action_item": actions[:5],
        "owner": owners[:8],
        "deadline": deadlines[:8],
        "risk": risks[:5],
    }


def meeting_trace(results: list[Any]) -> dict[str, Any]:
    meeting_results = [result for result in results if (getattr(result, "metadata", {}) or {}).get("meeting_transcript")]
    if not meeting_results:
        return {
            "meeting_transcript_used": False,
            "meeting_fields_matched": [],
            "speaker_detected": False,
            "timestamp_detected": False,
            "action_items_detected": 0,
            "decisions_detected": 0,
            "risks_detected": 0,
            "meeting_source_chunk_ids": [],
            "transcript_as_fact": False,
            "evidence_required": True,
        }

    fields: list[str] = []
    action_count = 0
    decision_count = 0
    risk_count = 0
    chunk_ids: list[str] = []
    speaker_detected = False
    timestamp_detected = False
    for result in meeting_results:
        metadata = getattr(result, "metadata", {}) or {}
        for field in metadata.get("meeting_fields_matched") or metadata.get("meeting_fields") or []:
            if field not in fields:
                fields.append(field)
        action_count += len(metadata.get("action_item") or [])
        decision_count += len(metadata.get("decision") or [])
        risk_count += len(metadata.get("risk") or [])
        speaker_detected = speaker_detected or bool(metadata.get("speaker") or metadata.get("speakers"))
        timestamp_detected = timestamp_detected or bool(metadata.get("timestamp") or metadata.get("timestamps"))
        chunk_id = metadata.get("source_chunk_id") or getattr(result, "chunk_id", None)
        if chunk_id and chunk_id not in chunk_ids:
            chunk_ids.append(str(chunk_id))
    return {
        "meeting_transcript_used": True,
        "meeting_fields_matched": fields,
        "speaker_detected": speaker_detected,
        "timestamp_detected": timestamp_detected,
        "action_items_detected": action_count,
        "decisions_detected": decision_count,
        "risks_detected": risk_count,
        "meeting_source_chunk_ids": chunk_ids,
        "transcript_as_fact": False,
        "evidence_required": True,
    }


def _speaker_from_line(line: str) -> str | None:
    match = re.match(r"^\s*([\u4e00-\u9fffA-Za-z0-9·._ -]{1,24})\s*[:：]", line)
    if not match:
        return None
    speaker = match.group(1).strip()
    if speaker in SPEAKER_EXCLUDE:
        return None
    if any(speaker.startswith(prefix) for prefix in ("问题", "方案", "风险", "结论")):
        return None
    return speaker


def _timestamp_matches(text: str) -> list[str]:
    patterns = [
        r"\d{4}年\d{1,2}月\d{1,2}日",
        r"\d{4}[-/.]\d{1,2}[-/.]\d{1,2}",
        r"\b\d{1,2}:\d{2}(?::\d{2})?\b",
    ]
    matches: list[str] = []
    for pattern in patterns:
        matches.extend(re.findall(pattern, text))
    return matches


def _deadline_matches(text: str) -> list[str]:
    deadline_lines = _keyword_lines([line.strip() for line in text.splitlines() if line.strip()], ("截止", "完成", "deadline", "due"))
    joined = "\n".join(deadline_lines)
    return _timestamp_matches(joined)


def _owners_from_lines(lines: list[str]) -> list[str]:
    owners: list[str] = []
    for line in lines:
        if "负责" not in line and "跟进" not in line:
            continue
        speaker = _speaker_from_line(line)
        if speaker and speaker not in owners:
            owners.append(speaker)
        match = re.search(r"(?:负责人|责任人|由)\s*[:：]?\s*([\u4e00-\u9fffA-Za-z0-9·._ -]{2,12})", line)
        if match:
            owner = match.group(1).strip()
            if owner and owner not in owners:
                owners.append(owner)
    return owners


def _keyword_lines(lines: list[str], keywords: tuple[str, ...]) -> list[str]:
    matched = []
    for line in lines:
        if any(keyword.lower() in line.lower() for keyword in keywords):
            matched.append(line[:260])
    return matched


def _unique(values: Any) -> list[str]:
    output: list[str] = []
    for value in values:
        if not value:
            continue
        if value not in output:
            output.append(str(value))
    return output


def _excerpt(text: str) -> str:
    return re.sub(r"\s+", " ", text or "").strip()[:300]
