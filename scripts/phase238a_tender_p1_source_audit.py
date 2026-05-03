#!/usr/bin/env python
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


FIELDS = [
    "price_ceiling",
    "qualification_grade_category",
    "project_manager_level",
    "performance_requirement",
    "personnel_requirement",
]

STATUS_PRIORITY = {
    "concrete_source_found": 4,
    "ambiguous": 3,
    "anchor_only": 2,
    "not_found": 1,
    "skipped_live_unavailable": 0,
}

PRICE_KEYWORDS = ("最高投标限价", "招标控制价", "投标报价上限", "最高限价", "投标限价")
PRICE_AMOUNT_RE = re.compile(r"(人民币)?\s*\d+(?:[.,]\d+)?\s*(万元|万|元|亿元)")
PRICE_PLACEHOLDER_RE = re.compile(r"(详见|见附件|另册|按.*执行|以.*为准)")

QUALIFICATION_ANCHORS = ("资质", "资格条件", "投标人资格", "资格要求")
QUALIFICATION_LEVEL_RE = re.compile(r"(特级|一级|二级|三级|甲级|乙级|丙级|[一二三]级|[1-3]级)")
QUALIFICATION_CATEGORY_RE = re.compile(r"(施工总承包|专业承包|建筑工程|市政公用工程|机电工程|电子与智能化|智能化|资质)")

PROJECT_MANAGER_ANCHORS = ("项目经理", "项目负责人", "注册建造师", "安全生产考核", "B证", "电子证书")
PROJECT_MANAGER_E_CERT_RE = re.compile(r"一级注册建造师电子证书")
PROJECT_MANAGER_REQUIRE_RE = re.compile(r"(项目经理|项目负责人).{0,30}(须具备|应具备|具备|具有|资格要求|资格为|要求为)")
PROJECT_MANAGER_LEVEL_RE = re.compile(r"(一级|二级|注册建造师|B证|安全生产考核)")

PERFORMANCE_ANCHORS = ("类似业绩", "类似工程业绩", "业绩要求", "业绩证明")
PERFORMANCE_CONCRETE_RE = re.compile(r"(近\s*[一二三四五\d]+\s*年|不少于\s*\d+\s*项|\d+\s*项|金额|合同额|规模|建筑面积|平方米|万元|亿元)")

PERSONNEL_ANCHORS = ("人员配备", "项目管理机构", "技术负责人", "专职安全员", "人员要求", "专业人员")
PERSONNEL_CONCRETE_RE = re.compile(r"(\d+\s*人|不少于\s*\d+|须具备|应具备|职称|证书|资格|专业)")


@dataclass(frozen=True)
class ChunkView:
    chunk_id: str
    text: str
    chunk_index: int | None = None
    heading_path: list[str] | None = None
    section_path: list[str] | None = None
    page_start: int | None = None
    page_end: int | None = None

    @classmethod
    def from_mapping(cls, value: dict[str, Any]) -> "ChunkView":
        return cls(
            chunk_id=str(value.get("chunk_id") or value.get("id") or ""),
            text=str(value.get("text") or ""),
            chunk_index=value.get("chunk_index"),
            heading_path=list(value.get("heading_path") or []),
            section_path=list(value.get("section_path") or []),
            page_start=value.get("page_start"),
            page_end=value.get("page_end"),
        )


def _json_dump(payload: Any) -> str:
    return json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True)


def _normalize(text: str) -> str:
    return re.sub(r"\s+", "", text or "")


def _semantic_clauses(text: str) -> list[str]:
    return [part for part in re.split(r"[。；;！？!?，,\n\r]+", text or "") if part.strip()]


def _matches_any(text: str, terms: tuple[str, ...]) -> list[str]:
    return [term for term in terms if term in text]


def _source_location(chunk: ChunkView) -> str:
    bits: list[str] = []
    if chunk.page_start is not None:
        if chunk.page_end and chunk.page_end != chunk.page_start:
            bits.append(f"pages {chunk.page_start}-{chunk.page_end}")
        else:
            bits.append(f"page {chunk.page_start}")
    path = chunk.section_path or chunk.heading_path or []
    if path:
        bits.append(" > ".join(path))
    if chunk.chunk_index is not None:
        bits.append(f"chunk_index {chunk.chunk_index}")
    return " | ".join(bits) or f"chunk {chunk.chunk_id}"


def _excerpt(text: str, terms: list[str]) -> str:
    if not text:
        return ""
    indexes = [text.find(term) for term in terms if term and text.find(term) >= 0]
    index = min(indexes) if indexes else 0
    start = max(0, index - 80)
    end = min(len(text), index + 260)
    return text[start:end].strip()


def _candidate(chunk: ChunkView, terms: list[str], diagnostic: str) -> dict[str, Any]:
    return {
        "chunk_id": chunk.chunk_id,
        "chunk_index": chunk.chunk_index,
        "source_location": _source_location(chunk),
        "matched_terms": terms,
        "diagnostic": diagnostic,
        "excerpt": _excerpt(chunk.text, terms),
    }


def _score_status(candidates: list[tuple[str, dict[str, Any]]]) -> str:
    if not candidates:
        return "not_found"
    return max((status for status, _ in candidates), key=lambda status: STATUS_PRIORITY[status])


def _audit_price(chunks: list[ChunkView]) -> dict[str, Any]:
    candidates: list[tuple[str, dict[str, Any]]] = []
    for chunk in chunks:
        text = chunk.text or ""
        terms = _matches_any(text, PRICE_KEYWORDS)
        if not terms:
            continue
        concrete = any(
            PRICE_AMOUNT_RE.search(clause)
            and not (PRICE_PLACEHOLDER_RE.search(clause) and "不得超过" not in clause)
            for clause in _semantic_clauses(text)
            if any(term in clause for term in PRICE_KEYWORDS)
        )
        status = "concrete_source_found" if concrete else "anchor_only"
        diagnostic = "concrete_amount_with_price_anchor" if concrete else "price_anchor_without_concrete_amount"
        candidates.append((status, _candidate(chunk, terms, diagnostic)))
    return _field_result("price_ceiling", candidates)


def _audit_qualification(chunks: list[ChunkView]) -> dict[str, Any]:
    candidates: list[tuple[str, dict[str, Any]]] = []
    for chunk in chunks:
        text = chunk.text or ""
        terms = _matches_any(text, QUALIFICATION_ANCHORS)
        if not terms:
            continue
        normalized = _normalize(text)
        concrete = (
            "资质" in normalized
            and bool(QUALIFICATION_LEVEL_RE.search(normalized))
            and bool(QUALIFICATION_CATEGORY_RE.search(normalized))
        )
        status = "concrete_source_found" if concrete else "anchor_only"
        diagnostic = "qualification_level_and_category_found" if concrete else "qualification_anchor_without_level_category"
        candidates.append((status, _candidate(chunk, terms, diagnostic)))
    return _field_result("qualification_grade_category", candidates)


def _audit_project_manager(chunks: list[ChunkView]) -> dict[str, Any]:
    candidates: list[tuple[str, dict[str, Any]]] = []
    for chunk in chunks:
        text = chunk.text or ""
        terms = _matches_any(text, PROJECT_MANAGER_ANCHORS)
        if not terms:
            continue
        concrete = False
        e_cert_only = False
        for clause in _semantic_clauses(text):
            normalized = _normalize(clause)
            if PROJECT_MANAGER_E_CERT_RE.search(normalized) and not re.search(r"(项目经理|项目负责人)", normalized):
                e_cert_only = True
                continue
            if PROJECT_MANAGER_REQUIRE_RE.search(normalized) and PROJECT_MANAGER_LEVEL_RE.search(normalized):
                concrete = True
                break
        if concrete:
            status = "concrete_source_found"
            diagnostic = "explicit_project_manager_level_requirement_found"
        elif e_cert_only:
            status = "anchor_only"
            diagnostic = "e_certificate_format_not_project_manager_level"
        else:
            status = "ambiguous"
            diagnostic = "project_manager_related_text_without_explicit_level"
        candidates.append((status, _candidate(chunk, terms, diagnostic)))
    return _field_result("project_manager_level", candidates)


def _audit_performance(chunks: list[ChunkView]) -> dict[str, Any]:
    candidates: list[tuple[str, dict[str, Any]]] = []
    for chunk in chunks:
        text = chunk.text or ""
        terms = _matches_any(text, PERFORMANCE_ANCHORS)
        if not terms:
            continue
        concrete = bool(PERFORMANCE_CONCRETE_RE.search(_normalize(text)))
        status = "concrete_source_found" if concrete else "ambiguous"
        diagnostic = "performance_threshold_found" if concrete else "performance_anchor_without_quantity_amount_year_scale"
        candidates.append((status, _candidate(chunk, terms, diagnostic)))
    return _field_result("performance_requirement", candidates)


def _audit_personnel(chunks: list[ChunkView]) -> dict[str, Any]:
    candidates: list[tuple[str, dict[str, Any]]] = []
    for chunk in chunks:
        text = chunk.text or ""
        terms = _matches_any(text, PERSONNEL_ANCHORS)
        if not terms:
            continue
        concrete = bool(PERSONNEL_CONCRETE_RE.search(_normalize(text)))
        status = "concrete_source_found" if concrete else "ambiguous"
        diagnostic = "personnel_count_or_qualification_found" if concrete else "personnel_anchor_without_count_profession_qualification"
        candidates.append((status, _candidate(chunk, terms, diagnostic)))
    return _field_result("personnel_requirement", candidates)


def _field_result(field: str, candidates: list[tuple[str, dict[str, Any]]]) -> dict[str, Any]:
    status = _score_status(candidates)
    filtered = [candidate for candidate_status, candidate in candidates if candidate_status == status]
    if status == "not_found":
        reason = "No field anchor or concrete source evidence was found in available chunks."
        next_action = "Confirm parser/index coverage first; do not tune retrieval until source availability is known."
    elif status == "anchor_only":
        reason = "Only headings, anchors, placeholders, or non-concrete material requirements were found."
        next_action = "Preserve Missing Evidence unless a concrete source chunk is found manually."
    elif status == "ambiguous":
        reason = "Related text exists, but it is insufficient to safely determine the requested field."
        next_action = "Route to human review before bounded retrieval or extraction planning."
    elif status == "skipped_live_unavailable":
        reason = "Live source audit was skipped because DB/OpenSearch was unavailable."
        next_action = "Retry read-only audit when local services are available."
    else:
        reason = "Concrete source evidence appears to exist in parsed chunks."
        next_action = "Use the candidate chunk ids to plan bounded retrieval recall diagnostics."
    matched_terms = sorted({term for candidate in filtered for term in candidate.get("matched_terms", [])})
    return {
        "field": field,
        "status": status,
        "matched_terms": matched_terms,
        "candidate_chunk_ids": [candidate["chunk_id"] for candidate in filtered],
        "source_locations": [candidate["source_location"] for candidate in filtered],
        "candidate_chunks": filtered[:10],
        "diagnostic_reason": reason,
        "recommended_next_action": next_action,
        "human_review_required": True,
    }


def audit_chunks(chunks: list[ChunkView], fields: list[str]) -> list[dict[str, Any]]:
    auditors = {
        "price_ceiling": _audit_price,
        "qualification_grade_category": _audit_qualification,
        "project_manager_level": _audit_project_manager,
        "performance_requirement": _audit_performance,
        "personnel_requirement": _audit_personnel,
    }
    return [auditors[field](chunks) for field in fields]


def skipped_audits(fields: list[str]) -> list[dict[str, Any]]:
    return [
        {
            "field": field,
            "status": "skipped_live_unavailable",
            "matched_terms": [],
            "candidate_chunk_ids": [],
            "source_locations": [],
            "candidate_chunks": [],
            "diagnostic_reason": "Live source audit was skipped because DB/OpenSearch was unavailable.",
            "recommended_next_action": "Retry read-only audit when local services are available.",
            "human_review_required": True,
        }
        for field in fields
    ]


def load_chunks_from_db(document_id: str, version_id: str) -> tuple[list[ChunkView], str | None]:
    try:
        from app.db.session import SessionLocal
        from app.models.chunk import Chunk
    except Exception as exc:  # pragma: no cover - environment dependent
        return [], repr(exc)

    db = None
    try:
        db = SessionLocal()
        rows = (
            db.query(Chunk)
            .filter(Chunk.document_id == document_id)
            .filter(Chunk.version_id == version_id)
            .order_by(Chunk.chunk_index.asc())
            .limit(5000)
            .all()
        )
        chunks = [
            ChunkView(
                chunk_id=row.id,
                text=row.text,
                chunk_index=row.chunk_index,
                heading_path=row.heading_path,
                section_path=row.section_path,
                page_start=row.page_start,
                page_end=row.page_end,
            )
            for row in rows
        ]
        return chunks, None
    except Exception as exc:  # pragma: no cover - environment dependent
        return [], repr(exc)
    finally:
        if db is not None:
            db.close()


def overall_recommendation(field_audits: list[dict[str, Any]]) -> str:
    statuses = {audit["status"] for audit in field_audits}
    if "skipped_live_unavailable" in statuses:
        return "retry_read_only_audit_when_services_available"
    if "concrete_source_found" in statuses:
        return "plan_bounded_retrieval_diagnostics_for_concrete_source_fields"
    if statuses <= {"not_found", "anchor_only", "ambiguous"}:
        return "preserve_missing_evidence_and_request_human_source_review"
    return "human_review_required_before_any_fix"


def build_summary(
    *,
    document_id: str,
    version_id: str,
    fields: list[str],
    chunks: list[ChunkView] | None,
    live_error: str | None = None,
) -> dict[str, Any]:
    field_audits = skipped_audits(fields) if chunks is None else audit_chunks(chunks, fields)
    if live_error:
        for audit in field_audits:
            audit["live_error"] = live_error
    return {
        "dry_run": True,
        "read_only": True,
        "destructive_actions": [],
        "writes_db": False,
        "mutates_index": False,
        "repairs_issue": False,
        "rollout_approved": False,
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "document_id": document_id,
        "version_id": version_id,
        "field_audits": field_audits,
        "overall_recommendation": overall_recommendation(field_audits),
    }


def write_report(summary: dict[str, Any], output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = output_dir / f"{stamp}_tender_p1_source_audit.json"
    path.write_text(_json_dump(summary) + "\n", encoding="utf-8")
    return path


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Phase 2.38a tender P1 source availability audit.")
    parser.add_argument("--document-id", required=True)
    parser.add_argument("--version-id", required=True)
    parser.add_argument("--field", choices=[*FIELDS, "all"], default="all")
    parser.add_argument("--output-dir", type=Path, default=Path("reports/tender_p1_audit"))
    parser.add_argument("--dry-run-preview", action="store_true", help="Print JSON only; do not write report.")
    parser.add_argument("--skip-live", action="store_true", help="Do not connect to DB/OpenSearch; mark fields skipped.")
    parser.add_argument("--json", action="store_true", help="Print JSON output. Kept for explicit CLI readability.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    fields = FIELDS if args.field == "all" else [args.field]

    chunks: list[ChunkView] | None
    live_error: str | None = None
    if args.skip_live:
        chunks = None
        live_error = "skip_live_requested"
    else:
        chunks, live_error = load_chunks_from_db(args.document_id, args.version_id)
        if live_error or not chunks:
            chunks = None
            live_error = live_error or "no_chunks_found_for_document_version"

    summary = build_summary(
        document_id=args.document_id,
        version_id=args.version_id,
        fields=fields,
        chunks=chunks,
        live_error=live_error,
    )
    if args.dry_run_preview:
        summary["output_file"] = None
    else:
        summary["output_file"] = str(write_report(summary, args.output_dir))

    print(_json_dump(summary))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
