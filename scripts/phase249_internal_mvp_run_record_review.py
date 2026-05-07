#!/usr/bin/env python
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.phase242a_mvp_pilot_review_dry_run import build_review_report, render_markdown


UNSAFE_POLICY_FIELDS = (
    "facts_as_answer",
    "transcript_as_fact",
    "snapshot_as_answer",
)
FORBIDDEN_INPUT_FIELDS = (
    "raw_model_output",
    "raw_llm_output",
    "raw_transcript",
    "env_values",
    "secrets",
    "tokens",
    "passwords",
)
BOUNDARY_FIELDS = (
    "not_production_rollout",
    "not_customer_delivery",
    "not_automatic_tender_review",
    "not_automatic_bid",
    "not_automatic_business_decision",
)


def load_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"expected JSON object: {path}")
    return data


def build_review_payload(run_record: dict[str, Any], *, generated_at: str | None = None) -> dict[str, Any]:
    generated_at = generated_at or datetime.now(timezone.utc).isoformat()
    p0_items: list[dict[str, Any]] = []
    p1_items: list[dict[str, Any]] = []
    p2_items: list[dict[str, Any]] = []
    p3_items: list[dict[str, Any]] = []
    missing_evidence: list[dict[str, Any]] = []
    known_risks: list[str] = []
    source_sessions = collect_source_sessions(run_record)
    evidence_policy = {
        "facts_as_answer": False,
        "transcript_as_fact": False,
        "snapshot_as_answer": False,
        "missing_evidence_hidden": False,
        "third_document_contamination": False,
        "alias_persistent_missing": False,
        "retrieval_suppressed": False,
        "production_rollout_claimed": False,
        "repair_authorized": False,
        "data_mutation": False,
    }

    for field in FORBIDDEN_INPUT_FIELDS:
        if field in run_record:
            p1_items.append(
                issue_item(
                    item_id=f"unsafe-input-{field}",
                    issue_type="unsafe_input_field",
                    severity="P1",
                    reason=f"Run record contains field `{field}`; sanitized bridge must not propagate it.",
                    blocking=True,
                )
            )

    parse_alias_summary(run_record, p1_items, known_risks, evidence_policy)
    parse_daily_queries(run_record, p0_items, p1_items, p2_items, missing_evidence, known_risks, evidence_policy)
    parse_issue_summary(run_record, p0_items, p1_items, p2_items, p3_items, known_risks)
    parse_boundaries(run_record, p0_items, evidence_policy)

    citation_summary = summarize_citations(run_record)
    decision_hint = decide_hint(p0_items, p1_items, missing_evidence, evidence_policy)

    return {
        "generated_at": generated_at,
        "dry_run": True,
        "production_rollout": False,
        "repair_authorized": False,
        "destructive_actions": [],
        "data_mutation": False,
        "pilot_round": pilot_round(run_record),
        "reviewer": reviewer(run_record),
        "source_sessions": source_sessions,
        "p0_items": p0_items,
        "p1_items": p1_items,
        "p2_items": p2_items,
        "p3_items": p3_items,
        "evidence_policy": evidence_policy,
        "citation_summary": citation_summary,
        "missing_evidence": missing_evidence,
        "known_risks": unique_strings(known_risks),
        "next_phase_candidates": next_phase_candidates(decision_hint),
        "not_claimable_confirmed": not_claimable_confirmed(run_record),
        "decision_hint": decision_hint,
        "source_record": {
            "record_type": str(run_record.get("record_type") or ""),
            "date": str(run_record.get("date") or ""),
        },
    }


def parse_alias_summary(
    run_record: dict[str, Any],
    p1_items: list[dict[str, Any]],
    known_risks: list[str],
    evidence_policy: dict[str, Any],
) -> None:
    for index, alias in enumerate(_as_list(run_record.get("alias_summary"))):
        if not isinstance(alias, dict):
            continue
        alias_name = str(alias.get("alias") or f"alias-{index + 1}")
        missing = _truthy(alias.get("alias_missing")) or str(alias.get("alias_resolution_status") or "").lower() in {
            "alias_missing",
            "missing",
        }
        suppressed = _truthy(alias.get("retrieval_suppressed")) or _truthy(alias.get("suppress_retrieval"))
        failed = str(alias.get("status") or "").lower() == "fail"
        if not (missing or suppressed or failed):
            continue

        reviewed = _reviewed(alias)
        evidence_policy["alias_persistent_missing"] = evidence_policy["alias_persistent_missing"] or missing
        evidence_policy["retrieval_suppressed"] = evidence_policy["retrieval_suppressed"] or suppressed
        known_risks.append(f"alias/session issue recorded for {alias_name}")
        p1_items.append(
            issue_item(
                item_id=f"alias-{index + 1}",
                issue_type="alias_session",
                severity="P1",
                reason=f"{alias_name} has alias missing, retrieval suppressed, or failed binding in the run record.",
                blocking=not reviewed,
                human_reviewed=reviewed,
                alias=alias_name,
            )
        )


def parse_daily_queries(
    run_record: dict[str, Any],
    p0_items: list[dict[str, Any]],
    p1_items: list[dict[str, Any]],
    p2_items: list[dict[str, Any]],
    missing_evidence: list[dict[str, Any]],
    known_risks: list[str],
    evidence_policy: dict[str, Any],
) -> None:
    for index, query in enumerate(_as_list(run_record.get("daily_query_summary"))):
        if not isinstance(query, dict):
            continue
        query_area = str(query.get("query_area") or f"query-{index + 1}")

        for field in UNSAFE_POLICY_FIELDS:
            if _truthy(query.get(field)):
                evidence_policy[field] = True
                p0_items.append(
                    issue_item(
                        item_id=f"{query_area}-{field}",
                        issue_type="evidence_policy_violation",
                        severity="P0",
                        reason=f"{query_area} recorded {field}=true.",
                        query_area=query_area,
                    )
                )

        if _truthy(query.get("third_document_contamination")):
            evidence_policy["third_document_contamination"] = True
            p0_items.append(
                issue_item(
                    item_id=f"{query_area}-third-document-contamination",
                    issue_type="contamination",
                    severity="P0",
                    reason=f"{query_area} recorded third document contamination.",
                    query_area=query_area,
                )
            )

        result = str(query.get("result") or "").lower()
        if result in {"partial", "fail"}:
            visible = query.get("missing_evidence_visible")
            reviewed = _reviewed_missing(query)
            if visible is False:
                evidence_policy["missing_evidence_hidden"] = True
                p1_items.append(
                    issue_item(
                        item_id=f"{query_area}-hidden-missing-evidence",
                        issue_type="missing_evidence_hidden",
                        severity="P1",
                        reason=f"{query_area} has partial/fail result with hidden Missing Evidence.",
                        blocking=True,
                        query_area=query_area,
                    )
                )
            missing_evidence.append(
                {
                    "query_area": query_area,
                    "result": result,
                    "visible": bool(visible is not False),
                    "human_reviewed": reviewed,
                    "review_status": "reviewed" if reviewed else "needs_review",
                }
            )
            if result == "fail":
                p1_items.append(
                    issue_item(
                        item_id=f"{query_area}-failed-query",
                        issue_type="query_failed",
                        severity="P1",
                        reason=f"{query_area} result is fail; internal MVP expansion should pause unless reviewed.",
                        blocking=not reviewed,
                        human_reviewed=reviewed,
                        query_area=query_area,
                    )
                )
            elif result == "partial":
                p2_items.append(
                    issue_item(
                        item_id=f"{query_area}-partial-query",
                        issue_type="query_partial",
                        severity="P2",
                        reason=f"{query_area} result is partial and remains human-reviewable.",
                        query_area=query_area,
                    )
                )
        if result in {"partial", "fail"}:
            known_risks.append(f"{query_area}:{result}")


def parse_issue_summary(
    run_record: dict[str, Any],
    p0_items: list[dict[str, Any]],
    p1_items: list[dict[str, Any]],
    p2_items: list[dict[str, Any]],
    p3_items: list[dict[str, Any]],
    known_risks: list[str],
) -> None:
    issue_summary = _as_dict(run_record.get("issue_summary"))
    parsed_counts = {"P0": 0, "P1": 0, "P2": 0, "P3": 0}
    for index, issue in enumerate(_as_list(issue_summary.get("issues"))):
        if not isinstance(issue, dict):
            continue
        severity = str(issue.get("severity") or "").upper()
        normalized_severity = severity if severity in parsed_counts else "P3"
        parsed_counts[normalized_severity] += 1
        issue_id = str(issue.get("issue_id") or f"issue-{index + 1}")
        item = issue_item(
            item_id=issue_id,
            issue_type=str(issue.get("issue_type") or "other"),
            severity=normalized_severity,
            reason=str(issue.get("next_action") or issue.get("manual_workaround") or "Recorded from run issue summary."),
            blocking=normalized_severity == "P1" and not _reviewed(issue),
            human_reviewed=_reviewed(issue),
        )
        if normalized_severity == "P0":
            p0_items.append(item)
        elif normalized_severity == "P1":
            p1_items.append(item)
        elif normalized_severity == "P2":
            p2_items.append(item)
        else:
            p3_items.append(item)
        known_risks.append(f"{issue_id}:{normalized_severity}")

    add_count_placeholders(
        issue_summary=issue_summary,
        parsed_counts=parsed_counts,
        p0_items=p0_items,
        p1_items=p1_items,
        p2_items=p2_items,
        p3_items=p3_items,
        known_risks=known_risks,
    )


def add_count_placeholders(
    *,
    issue_summary: dict[str, Any],
    parsed_counts: dict[str, int],
    p0_items: list[dict[str, Any]],
    p1_items: list[dict[str, Any]],
    p2_items: list[dict[str, Any]],
    p3_items: list[dict[str, Any]],
    known_risks: list[str],
) -> None:
    targets = {
        "P0": (_int_count(issue_summary.get("p0_count")), p0_items, True),
        "P1": (_int_count(issue_summary.get("p1_count")), p1_items, True),
        "P2": (_int_count(issue_summary.get("p2_count")), p2_items, False),
        "P3": (_int_count(issue_summary.get("p3_count")), p3_items, False),
    }
    for severity, (declared_count, target_items, blocking) in targets.items():
        missing_count = max(0, declared_count - parsed_counts.get(severity, 0))
        for offset in range(missing_count):
            placeholder_id = f"issue-summary-{severity.lower()}-placeholder-{offset + 1}"
            target_items.append(
                issue_item(
                    item_id=placeholder_id,
                    issue_type="issue_summary_count_only",
                    severity=severity,
                    reason=(
                        f"issue_summary declares {declared_count} {severity} item(s), "
                        "but no matching detailed issue entry was provided."
                    ),
                    blocking=blocking,
                    human_reviewed=False,
                )
            )
            known_risks.append(f"{placeholder_id}:{severity}")


def parse_boundaries(run_record: dict[str, Any], p0_items: list[dict[str, Any]], evidence_policy: dict[str, Any]) -> None:
    decision = _as_dict(run_record.get("decision"))
    boundaries = _as_dict(run_record.get("boundaries"))
    for field in BOUNDARY_FIELDS:
        if decision.get(field) is False or boundaries.get(field) is False:
            evidence_policy["production_rollout_claimed"] = True
            p0_items.append(
                issue_item(
                    item_id=f"boundary-{field}",
                    issue_type="boundary_violation",
                    severity="P0",
                    reason=f"Boundary `{field}` is false in the run record.",
                )
            )
    if boundaries.get("not_repair_cleanup_backfill_reindex_delete") is False:
        evidence_policy["repair_authorized"] = True
        p0_items.append(
            issue_item(
                item_id="boundary-not_repair_cleanup_backfill_reindex_delete",
                issue_type="boundary_violation",
                severity="P0",
                reason="Boundary `not_repair_cleanup_backfill_reindex_delete` is false in the run record.",
            )
        )
    if boundaries.get("no_db_facts_document_versions_auditlogs_opensearch_qdrant_mutation") is False:
        evidence_policy["data_mutation"] = True
        p0_items.append(
            issue_item(
                item_id="boundary-no_db_facts_document_versions_auditlogs_opensearch_qdrant_mutation",
                issue_type="boundary_violation",
                severity="P0",
                reason=(
                    "Boundary `no_db_facts_document_versions_auditlogs_opensearch_qdrant_mutation` "
                    "is false in the run record."
                ),
            )
        )


def summarize_citations(run_record: dict[str, Any]) -> dict[str, Any]:
    queries = [item for item in _as_list(run_record.get("daily_query_summary")) if isinstance(item, dict)]
    with_citations = 0
    document_ids: list[str] = []
    items: list[dict[str, Any]] = []
    for query in queries:
        citation = str(query.get("citation_summary") or "")
        evidence_ids = [str(value) for value in _as_list(query.get("evidence_document_ids")) if value]
        if citation or evidence_ids:
            with_citations += 1
        document_ids.extend(evidence_ids)
        items.append(
            {
                "query_area": str(query.get("query_area") or ""),
                "result": str(query.get("result") or ""),
                "citation_present": bool(citation or evidence_ids),
                "evidence_document_ids": evidence_ids,
            }
        )
    return {
        "total_queries": len(queries),
        "queries_with_citations": with_citations,
        "document_ids": sorted(set(document_ids)),
        "items": items,
    }


def collect_source_sessions(run_record: dict[str, Any]) -> list[str]:
    sessions: list[str] = []
    sessions.extend(str(value) for value in _as_list(run_record.get("source_sessions")) if value)
    sessions.extend(str(value) for value in _as_list(run_record.get("session_ids")) if value)
    if run_record.get("session_id"):
        sessions.append(str(run_record["session_id"]))
    for query in _as_list(run_record.get("daily_query_summary")):
        if not isinstance(query, dict):
            continue
        sessions.extend(str(value) for value in _as_list(query.get("session_ids")) if value)
        if query.get("session_id"):
            sessions.append(str(query["session_id"]))
    return sorted(set(sessions))


def pilot_round(run_record: dict[str, Any]) -> str:
    return str(run_record.get("pilot_round") or run_record.get("run_window") or run_record.get("date") or "")


def reviewer(run_record: dict[str, Any]) -> str:
    decision = _as_dict(run_record.get("decision"))
    return str(run_record.get("reviewer") or decision.get("reviewer") or run_record.get("recorder") or "")


def not_claimable_confirmed(run_record: dict[str, Any]) -> list[str]:
    decision = _as_dict(run_record.get("decision"))
    boundaries = _as_dict(run_record.get("boundaries"))
    labels = {
        "not_production_rollout": "production rollout",
        "not_customer_delivery": "customer delivery",
        "not_automatic_tender_review": "automatic tender review",
        "not_automatic_bid": "automatic bid",
        "not_automatic_business_decision": "automatic business decision",
        "not_repair_cleanup_backfill_reindex_delete": "repair/backfill/reindex/delete authorization",
    }
    confirmed: list[str] = []
    for field, label in labels.items():
        if decision.get(field) is True or boundaries.get(field) is True:
            confirmed.append(label)
    if not confirmed:
        confirmed = list(labels.values())
    return confirmed


def decide_hint(
    p0_items: list[dict[str, Any]],
    p1_items: list[dict[str, Any]],
    missing_evidence: list[dict[str, Any]],
    evidence_policy: dict[str, Any],
) -> str:
    unsafe_fields = (
        *UNSAFE_POLICY_FIELDS,
        "production_rollout_claimed",
        "repair_authorized",
        "data_mutation",
        "third_document_contamination",
    )
    unsafe = any(evidence_policy.get(field) is True for field in unsafe_fields)
    if p0_items or unsafe or evidence_policy.get("third_document_contamination"):
        return "no_go"
    if any(item.get("blocking") is True for item in p1_items):
        return "pause"
    if any(item.get("human_reviewed") is not True for item in missing_evidence):
        return "pause"
    return "go"


def next_phase_candidates(decision_hint: str) -> list[str]:
    if decision_hint == "no_go":
        return ["bounded_p0_review_before_any_mvp_expansion"]
    if decision_hint == "pause":
        return ["bounded_p1_or_missing_evidence_review"]
    return ["continue_internal_controlled_mvp_review"]


def build_output(run_record: dict[str, Any], *, include_review_report: bool = False) -> dict[str, Any]:
    payload = build_review_payload(run_record)
    if not include_review_report:
        return {"review_payload": payload}
    return {"review_payload": payload, "review_report": build_review_report(payload)}


def write_outputs(output: dict[str, Any], output_dir: Path) -> dict[str, str]:
    output_dir.mkdir(parents=True, exist_ok=True)
    payload = _as_dict(output.get("review_payload"))
    report = output.get("review_report")
    paths: dict[str, str] = {}
    payload_json = output_dir / "phase249_review_payload.json"
    payload_md = output_dir / "phase249_review_payload.md"
    payload_json.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    payload_md.write_text(render_payload_markdown(payload), encoding="utf-8")
    paths["payload_json"] = str(payload_json)
    paths["payload_markdown"] = str(payload_md)
    if isinstance(report, dict):
        report_json = output_dir / "phase249_review_report.json"
        report_md = output_dir / "phase249_review_report.md"
        report_json.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        report_md.write_text(render_markdown(report), encoding="utf-8")
        paths["review_report_json"] = str(report_json)
        paths["review_report_markdown"] = str(report_md)
    return paths


def render_payload_markdown(payload: dict[str, Any]) -> str:
    return "\n".join(
        [
            "# Phase 2.49 Internal MVP Run Record Review Payload",
            "",
            f"- decision_hint: `{payload.get('decision_hint')}`",
            f"- P0/P1/P2/P3: `{len(_as_list(payload.get('p0_items')))}` / `{len(_as_list(payload.get('p1_items')))}` / `{len(_as_list(payload.get('p2_items')))}` / `{len(_as_list(payload.get('p3_items')))}`",
            "- dry_run: `true`",
            "- production_rollout: `false`",
            "- repair_authorized: `false`",
            "- data_mutation: `false`",
            "",
        ]
    )


def issue_item(
    *,
    item_id: str,
    issue_type: str,
    severity: str,
    reason: str,
    blocking: bool = False,
    human_reviewed: bool | None = None,
    **extra: Any,
) -> dict[str, Any]:
    item = {
        "id": item_id,
        "issue_type": issue_type,
        "severity": severity,
        "reason": reason,
        "blocking": blocking,
    }
    if human_reviewed is not None:
        item["human_reviewed"] = human_reviewed
    item.update({key: value for key, value in extra.items() if value not in (None, "")})
    return item


def _reviewed(item: dict[str, Any]) -> bool:
    if item.get("human_reviewed") is True or item.get("workaround_reviewed") is True:
        return True
    if item.get("manual_workaround") and str(item.get("review_status") or "").lower() in {
        "reviewed",
        "manual_reviewed",
        "accepted",
        "accepted_missing_evidence",
    }:
        return True
    return False


def _reviewed_missing(query: dict[str, Any]) -> bool:
    if query.get("missing_evidence_human_reviewed") is True:
        return True
    if query.get("human_reviewed") is True:
        return True
    if str(query.get("review_status") or "").lower() in {"reviewed", "manual_reviewed", "accepted_missing_evidence"}:
        return True
    return False


def _truthy(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() in {"1", "true", "yes", "y", "on"}
    return bool(value)


def _as_list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def _as_dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def unique_strings(values: list[str]) -> list[str]:
    return sorted({value for value in values if value})


def _int_count(value: Any) -> int:
    if value is None:
        return 0
    try:
        return max(0, int(value))
    except (TypeError, ValueError):
        return 0


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Convert an explicit internal MVP run record into a sanitized review dry-run payload."
    )
    parser.add_argument("--input-run-record", type=Path, required=True, help="Explicit local run record JSON input.")
    parser.add_argument("--output-dir", type=Path, help="Optional output directory for sanitized JSON/Markdown files.")
    parser.add_argument("--review-report", action="store_true", help="Also build the Phase 2.42a review report in memory.")
    parser.add_argument("--json", action="store_true", help="Print JSON output. Kept for explicit CLI readability.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    output = build_output(load_json(args.input_run_record), include_review_report=args.review_report)
    if args.output_dir:
        output["written_outputs"] = write_outputs(output, args.output_dir)
    print(json.dumps(output, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
