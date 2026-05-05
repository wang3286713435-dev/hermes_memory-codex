#!/usr/bin/env python
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


DOCUMENT_ID = "869d4684-0a98-4825-bc72-ada65c15cfc9"
VERSION_ID = "43558ba9-2813-42ff-b11b-3fbb4448a5bb"

FIELDS = [
    "price_ceiling",
    "qualification_grade_category",
    "project_manager_level",
    "performance_requirement",
    "personnel_requirement",
]

FIXED_POLICY_FIELDS = {
    "price_ceiling": {
        "policy": "preserve_missing_evidence",
        "status": "field_should_remain_missing_evidence",
        "retrieval_query": "",
        "recommended_next_action": "Keep Missing Evidence or request source supplementation; do not tune retrieval for anchor-only evidence.",
        "reason": "Phase 2.38a found only anchor-only source availability for price ceiling.",
    },
    "project_manager_level": {
        "policy": "human_review_required",
        "status": "field_requires_human_review",
        "retrieval_query": "",
        "recommended_next_action": "Route to human review; do not infer project manager level from e-certificate or material clauses.",
        "reason": "Phase 2.38a classified project manager level as ambiguous.",
    },
}

CONCRETE_FIELD_CANDIDATES = {
    "qualification_grade_category": [
        "b5a34baa-2b01-44c3-aa44-3dbcefd6cde4",
        "386eeace-c4c3-4bf1-9269-e18a514d0243",
        "da6014b5-2343-499c-b6f2-b438e0968160",
        "06297547-a943-4d84-8002-16fb6854b2a3",
        "ee3b81ca-dd41-4839-8b7e-46973bac51aa",
    ],
    "performance_requirement": [
        "59501aa1-e1b6-4bab-9a1d-266711827146",
        "b8283142-21e5-4d6c-acf8-b239180a00bf",
        "03ce871a-e1b6-4bab-9a1d-266711827146",
        "63c16666-e04c-4870-8f27-0e432c5c6b75",
        "386eeace-c4c3-4bf1-9269-e18a514d0243",
    ],
    "personnel_requirement": [
        "e64e0299-9b47-466f-ada2-25ce3121f2c7",
        "b8283142-21e5-4bab-9a1d-266711827146",
        "03ce871a-e1b6-4bab-9a1d-266711827146",
        "63c16666-e04c-4870-8f27-0e432c5c6b75",
        "a24e6ac9-0333-4e54-9ad3-4c4d70e9ef8d",
    ],
}

FIELD_QUERIES = {
    "qualification_grade_category": "投标人资质具体等级和资质类别要求是什么？",
    "performance_requirement": "类似业绩的数量、金额、年限或规模门槛要求是什么？",
    "personnel_requirement": "项目人员数量、专业、职称或资质要求是什么？",
}

PERSONNEL_QUERY_ALIASES = [
    "项目管理机构",
    "人员配备",
    "人员要求",
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
]

PERSONNEL_SECTION_HINTS = [
    "投标人须知前附表",
    "资格审查",
    "资格后审",
    "项目管理机构",
    "项目班子",
    "主要人员",
    "主要管理人员",
    "人员配备",
    "人员要求",
]


def _json_dump(payload: Any) -> str:
    return json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True)


def _safety_flags() -> dict[str, Any]:
    return {
        "dry_run": True,
        "read_only": True,
        "destructive_actions": [],
        "writes_db": False,
        "mutates_index": False,
        "repairs_issue": False,
        "rollout_approved": False,
    }


def fixed_policy_diagnostic(field: str) -> dict[str, Any]:
    policy = FIXED_POLICY_FIELDS[field]
    return {
        "field": field,
        "policy": policy["policy"],
        "candidate_chunk_ids": [],
        "retrieval_query": policy["retrieval_query"],
        "retrieved_chunk_ids": [],
        "candidate_hits": [],
        "status": policy["status"],
        "recommended_next_action": policy["recommended_next_action"],
        "diagnostic_reason": policy["reason"],
    }


def retrieval_query_for_field(field: str) -> str:
    query = FIELD_QUERIES[field]
    if field != "personnel_requirement":
        return query
    expansion = " ".join([*PERSONNEL_QUERY_ALIASES, *PERSONNEL_SECTION_HINTS])
    return f"{query} {expansion}"


def personnel_expansion_trace(field: str, retrieval_query: str) -> dict[str, Any]:
    if field != "personnel_requirement":
        return {"personnel_expanded_query": False}
    return {
        "personnel_expanded_query": True,
        "baseline_query": FIELD_QUERIES[field],
        "expanded_retrieval_query": retrieval_query,
        "personnel_query_aliases": list(PERSONNEL_QUERY_ALIASES),
        "personnel_section_hints": list(PERSONNEL_SECTION_HINTS),
    }


def skipped_live_diagnostic(field: str, live_error: str | None) -> dict[str, Any]:
    retrieval_query = retrieval_query_for_field(field)
    return {
        "field": field,
        "policy": "diagnose_retrieval_candidate_visibility",
        "candidate_chunk_ids": list(CONCRETE_FIELD_CANDIDATES[field]),
        "retrieval_query": retrieval_query,
        "retrieved_chunk_ids": [],
        "candidate_hits": [],
        "status": "skipped_live_unavailable",
        "recommended_next_action": "Retry read-only recall diagnostics when local DB/OpenSearch are reachable.",
        "diagnostic_reason": "Live retrieval diagnostics could not run.",
        "live_error": live_error,
        **personnel_expansion_trace(field, retrieval_query),
    }


def diagnose_candidate_visibility(
    *,
    field: str,
    candidate_chunk_ids: list[str],
    retrieved_chunk_ids: list[str],
    retrieval_query: str,
    top_k: int,
) -> dict[str, Any]:
    rank_by_chunk_id = {chunk_id: index + 1 for index, chunk_id in enumerate(retrieved_chunk_ids)}
    candidate_hits = [
        {
            "chunk_id": chunk_id,
            "rank": rank_by_chunk_id[chunk_id],
            "in_top_k": rank_by_chunk_id[chunk_id] <= top_k,
        }
        for chunk_id in candidate_chunk_ids
        if chunk_id in rank_by_chunk_id
    ]

    if any(hit["in_top_k"] for hit in candidate_hits):
        status = "candidate_in_top_k"
        next_action = "Candidate source is visible in top-k; use terminal validation before any retrieval tuning."
    elif candidate_hits:
        status = "candidate_present_but_low_rank"
        next_action = "Candidate source is retrievable but low-ranked; plan bounded query/profile diagnostics before ranking changes."
    else:
        status = "candidate_absent_from_retrieval"
        next_action = "Candidate source is absent from retrieval result; inspect filters, index coverage, and query profile before any ranking fix."

    return {
        "field": field,
        "policy": "diagnose_retrieval_candidate_visibility",
        "candidate_chunk_ids": list(candidate_chunk_ids),
        "retrieval_query": retrieval_query,
        "retrieved_chunk_ids": list(retrieved_chunk_ids),
        "candidate_hits": candidate_hits,
        "status": status,
        "recommended_next_action": next_action,
        "diagnostic_reason": f"{len(candidate_hits)} of {len(candidate_chunk_ids)} candidate chunks appeared in retrieved results.",
        **personnel_expansion_trace(field, retrieval_query),
    }


def run_retrieval_diagnostics(
    *,
    document_id: str,
    version_id: str,
    fields: list[str],
    retrieval_mode: str,
    top_k: int,
    diagnostic_limit: int,
) -> tuple[list[dict[str, Any]], str | None]:
    try:
        from app.db.session import SessionLocal
        from app.schemas.retrieval import RetrievalFilter, SearchRequest
        from app.services.retrieval.service import RetrievalService
    except Exception as exc:  # pragma: no cover - environment dependent
        return [skipped_live_diagnostic(field, repr(exc)) for field in fields], repr(exc)

    db = None
    try:
        db = SessionLocal()
        service = RetrievalService(db)
        diagnostics: list[dict[str, Any]] = []
        for field in fields:
            query = retrieval_query_for_field(field)
            request = SearchRequest(
                query=query,
                retrieval_mode=retrieval_mode,  # type: ignore[arg-type]
                top_k=diagnostic_limit,
                filters=RetrievalFilter(document_id=document_id, extra={"version_id": version_id}),
                enable_dense=retrieval_mode in {"dense", "hybrid"},
                enable_sparse=retrieval_mode in {"sparse", "hybrid"},
                enable_hybrid=retrieval_mode == "hybrid",
                debug=True,
            )
            response = service.search(request)
            retrieved_chunk_ids = [item.chunk_id for item in response.results]
            diagnostic = diagnose_candidate_visibility(
                field=field,
                candidate_chunk_ids=CONCRETE_FIELD_CANDIDATES[field],
                retrieved_chunk_ids=retrieved_chunk_ids,
                retrieval_query=query,
                top_k=top_k,
            )
            diagnostic["retrieval_mode"] = response.retrieval_mode
            diagnostic["backend"] = response.backend
            diagnostic["sparse_status"] = response.sparse_status
            diagnostic["dense_status"] = response.dense_status
            diagnostic["applied_filters"] = response.applied_filters
            diagnostics.append(diagnostic)
        return diagnostics, None
    except Exception as exc:  # pragma: no cover - environment dependent
        return [skipped_live_diagnostic(field, repr(exc)) for field in fields], repr(exc)
    finally:
        if db is not None:
            db.close()


def overall_recommendation(field_diagnostics: list[dict[str, Any]]) -> str:
    statuses = {diagnostic["status"] for diagnostic in field_diagnostics}
    if "skipped_live_unavailable" in statuses:
        return "retry_read_only_recall_diagnostics_when_services_available"
    if "candidate_absent_from_retrieval" in statuses:
        return "inspect_filters_index_coverage_and_query_profile_before_any_fix"
    if "candidate_present_but_low_rank" in statuses:
        return "plan_bounded_ranking_or_query_profile_diagnostics"
    if "candidate_in_top_k" in statuses:
        return "candidate_sources_visible_run_terminal_validation_before_retrieval_changes"
    return "preserve_missing_evidence_and_human_review_boundaries"


def build_summary(
    *,
    document_id: str,
    version_id: str,
    fields: list[str],
    concrete_diagnostics: list[dict[str, Any]],
    live_error: str | None = None,
    retrieval_mode: str = "sparse",
    top_k: int = 10,
    diagnostic_limit: int = 50,
) -> dict[str, Any]:
    concrete_by_field = {diagnostic["field"]: diagnostic for diagnostic in concrete_diagnostics}
    field_diagnostics: list[dict[str, Any]] = []
    for field in fields:
        if field in FIXED_POLICY_FIELDS:
            field_diagnostics.append(fixed_policy_diagnostic(field))
        else:
            field_diagnostics.append(concrete_by_field.get(field) or skipped_live_diagnostic(field, live_error))

    return {
        **_safety_flags(),
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "document_id": document_id,
        "version_id": version_id,
        "retrieval_mode": retrieval_mode,
        "top_k": top_k,
        "diagnostic_limit": diagnostic_limit,
        "field_diagnostics": field_diagnostics,
        "overall_recommendation": overall_recommendation(field_diagnostics),
        "live_error": live_error,
    }


def write_report(summary: dict[str, Any], output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = output_dir / f"{stamp}_tender_concrete_recall_diagnostics.json"
    path.write_text(_json_dump(summary) + "\n", encoding="utf-8")
    return path


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Phase 2.38b tender P1 concrete source recall diagnostics.")
    parser.add_argument("--document-id", default=DOCUMENT_ID)
    parser.add_argument("--version-id", default=VERSION_ID)
    parser.add_argument("--field", choices=[*FIELDS, "all"], default="all")
    parser.add_argument("--retrieval-mode", choices=["sparse", "dense", "hybrid"], default="sparse")
    parser.add_argument("--top-k", type=int, default=10)
    parser.add_argument("--diagnostic-limit", type=int, default=50)
    parser.add_argument("--output-dir", type=Path, default=Path("reports/tender_recall_diagnostics"))
    parser.add_argument("--dry-run-preview", action="store_true", help="Print JSON only; do not write report.")
    parser.add_argument("--skip-live", action="store_true", help="Do not connect to DB/OpenSearch; mark concrete fields skipped.")
    parser.add_argument("--json", action="store_true", help="Print JSON output. Kept for explicit CLI readability.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    fields = FIELDS if args.field == "all" else [args.field]
    concrete_fields = [field for field in fields if field in CONCRETE_FIELD_CANDIDATES]

    if args.skip_live or not concrete_fields:
        concrete_diagnostics = [
            skipped_live_diagnostic(field, "skip_live_requested") for field in concrete_fields
        ]
        live_error = "skip_live_requested" if concrete_fields else None
    else:
        concrete_diagnostics, live_error = run_retrieval_diagnostics(
            document_id=args.document_id,
            version_id=args.version_id,
            fields=concrete_fields,
            retrieval_mode=args.retrieval_mode,
            top_k=args.top_k,
            diagnostic_limit=args.diagnostic_limit,
        )

    summary = build_summary(
        document_id=args.document_id,
        version_id=args.version_id,
        fields=fields,
        concrete_diagnostics=concrete_diagnostics,
        live_error=live_error,
        retrieval_mode=args.retrieval_mode,
        top_k=args.top_k,
        diagnostic_limit=args.diagnostic_limit,
    )
    if args.dry_run_preview:
        summary["output_file"] = None
    else:
        summary["output_file"] = str(write_report(summary, args.output_dir))

    print(_json_dump(summary))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
