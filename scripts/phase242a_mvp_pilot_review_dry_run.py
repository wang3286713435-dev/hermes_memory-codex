#!/usr/bin/env python
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SAFE_POLICY_FIELDS = ("facts_as_answer", "transcript_as_fact", "snapshot_as_answer")


def load_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"expected JSON object: {path}")
    return data


def build_review_report(payload: dict[str, Any], *, generated_at: str | None = None) -> dict[str, Any]:
    generated_at = generated_at or datetime.now(timezone.utc).isoformat()
    p0_items = _as_list(payload.get("p0_items"))
    p1_items = _as_list(payload.get("p1_items"))
    p2_items = _as_list(payload.get("p2_items"))
    p3_items = _as_list(payload.get("p3_items"))
    evidence_policy = _as_dict(payload.get("evidence_policy"))
    missing_evidence = _as_list(payload.get("missing_evidence"))

    unsafe_reasons = unsafe_reasons_for(payload, evidence_policy)
    unreviewed_missing = unreviewed_missing_evidence(missing_evidence)
    blocking_p1 = blocking_p1_items(p1_items)
    decision, decision_reason = decide(
        p0_items=p0_items,
        unsafe_reasons=unsafe_reasons,
        unreviewed_missing=unreviewed_missing,
        blocking_p1=blocking_p1,
        p1_items=p1_items,
    )

    return {
        "report_id": report_id(generated_at),
        "generated_at": generated_at,
        "dry_run": True,
        "production_rollout": False,
        "repair_authorized": False,
        "destructive_actions": [],
        "data_mutation": False,
        "facts_as_answer": False,
        "transcript_as_fact": False,
        "snapshot_as_answer": False,
        "pilot_round": str(payload.get("pilot_round") or ""),
        "reviewer": str(payload.get("reviewer") or ""),
        "source_sessions": _as_list(payload.get("source_sessions")),
        "p0_count": len(p0_items),
        "p1_count": len(p1_items),
        "p2_count": len(p2_items),
        "p3_count": len(p3_items),
        "decision": decision,
        "decision_reason": decision_reason,
        "evidence_policy_summary": evidence_policy_summary(evidence_policy, unsafe_reasons),
        "citation_summary": _as_dict(payload.get("citation_summary")),
        "missing_evidence_summary": {
            "items": missing_evidence,
            "count": len(missing_evidence),
            "unreviewed_count": len(unreviewed_missing),
            "unreviewed_items": unreviewed_missing,
            "human_review_required": bool(missing_evidence),
        },
        "known_risks": _as_list(payload.get("known_risks")),
        "not_claimable_confirmed": payload.get("not_claimable_confirmed", []),
        "next_phase_candidates": _as_list(payload.get("next_phase_candidates")),
        "unsafe_reasons": unsafe_reasons,
        "p1_manual_review_required": bool(p1_items),
        "blocking_p1_items": blocking_p1,
        "human_review_required": bool(p0_items or p1_items or missing_evidence or unsafe_reasons),
        "not_production_rollout_approval": True,
        "not_repair_authorization": True,
    }


def unsafe_reasons_for(payload: dict[str, Any], evidence_policy: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    for field in SAFE_POLICY_FIELDS:
        if evidence_policy.get(field) is not False:
            reasons.append(f"unsafe_evidence_policy:{field}")

    if payload.get("production_rollout_claimed") is True or evidence_policy.get("production_rollout_claimed") is True:
        reasons.append("production_rollout_claimed")
    if payload.get("repair_authorized") is True or evidence_policy.get("repair_authorized") is True:
        reasons.append("repair_authorized_input")
    if payload.get("data_mutation") is True or evidence_policy.get("data_mutation") is True:
        reasons.append("data_mutation_input")
    if _as_list(payload.get("destructive_actions")):
        reasons.append("destructive_actions_input")
    return reasons


def evidence_policy_summary(evidence_policy: dict[str, Any], unsafe_reasons: list[str]) -> dict[str, Any]:
    return {
        "facts_as_answer": evidence_policy.get("facts_as_answer"),
        "transcript_as_fact": evidence_policy.get("transcript_as_fact"),
        "snapshot_as_answer": evidence_policy.get("snapshot_as_answer"),
        "missing_evidence_hidden": evidence_policy.get("missing_evidence_hidden", False),
        "production_rollout_claimed": evidence_policy.get("production_rollout_claimed", False),
        "safe": not unsafe_reasons,
        "unsafe_reasons": unsafe_reasons,
    }


def decide(
    *,
    p0_items: list[Any],
    unsafe_reasons: list[str],
    unreviewed_missing: list[Any],
    blocking_p1: list[Any],
    p1_items: list[Any],
) -> tuple[str, str]:
    if p0_items:
        return "no_go", "P0 item present; MVP Pilot expansion must stop for bounded review."
    if unsafe_reasons:
        return "no_go", "Unsafe evidence policy, rollout, repair, destructive action, or data mutation input detected."
    if unreviewed_missing:
        return "pause", "Missing Evidence requires human review before continuing the MVP Pilot."
    if blocking_p1:
        return "pause", "Blocking P1 item requires bounded fix or explicit human review."
    if p1_items:
        return "go", "P1 items are recorded for human review; Go only means continue internal controlled MVP Pilot."
    return "go", "No P0 or unsafe policy detected; Go only means continue internal controlled MVP Pilot."


def unreviewed_missing_evidence(items: list[Any]) -> list[Any]:
    unreviewed: list[Any] = []
    for item in items:
        if not isinstance(item, dict):
            unreviewed.append(item)
            continue
        if item.get("human_reviewed") is True:
            continue
        if str(item.get("review_status") or "").lower() in {"reviewed", "manual_reviewed", "accepted_missing_evidence"}:
            continue
        unreviewed.append(item)
    return unreviewed


def blocking_p1_items(items: list[Any]) -> list[Any]:
    blocking: list[Any] = []
    for item in items:
        if isinstance(item, dict) and (item.get("blocking") is True or item.get("blocks_pilot") is True):
            blocking.append(item)
    return blocking


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        f"# MVP Pilot Review Dry-run Report: {report['report_id']}",
        "",
        f"- Decision: `{report['decision']}`",
        f"- Decision reason: {report['decision_reason']}",
        f"- P0/P1/P2/P3: {report['p0_count']} / {report['p1_count']} / {report['p2_count']} / {report['p3_count']}",
        "- This is not production rollout approval.",
        "- This is not repair authorization.",
        "- Human review required.",
        "- Missing Evidence must be manually reviewed.",
        "",
        "## Safety Flags",
        "",
        f"- dry_run: `{str(report['dry_run']).lower()}`",
        f"- production_rollout: `{str(report['production_rollout']).lower()}`",
        f"- repair_authorized: `{str(report['repair_authorized']).lower()}`",
        f"- data_mutation: `{str(report['data_mutation']).lower()}`",
        f"- facts_as_answer: `{str(report['facts_as_answer']).lower()}`",
        f"- transcript_as_fact: `{str(report['transcript_as_fact']).lower()}`",
        f"- snapshot_as_answer: `{str(report['snapshot_as_answer']).lower()}`",
        "",
        "## Missing Evidence",
        "",
        f"- count: `{report['missing_evidence_summary']['count']}`",
        f"- unreviewed_count: `{report['missing_evidence_summary']['unreviewed_count']}`",
    ]
    return "\n".join(lines) + "\n"


def write_outputs(report: dict[str, Any], output_dir: Path) -> dict[str, str]:
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / f"{report['report_id']}.json"
    markdown_path = output_dir / f"{report['report_id']}.md"
    json_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    markdown_path.write_text(render_markdown(report), encoding="utf-8")
    return {"json": str(json_path), "markdown": str(markdown_path)}


def report_id(generated_at: str) -> str:
    safe = "".join(char if char.isdigit() else "" for char in generated_at)
    return f"mvp-pilot-review-{safe[:14] or 'manual'}"


def _as_list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def _as_dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build a Phase 2.42a MVP Pilot review dry-run report.")
    parser.add_argument("--input", type=Path, required=True, help="Explicit review evidence JSON input.")
    parser.add_argument("--output-dir", type=Path, help="Optional output directory for JSON and Markdown report.")
    parser.add_argument("--json", action="store_true", help="Print JSON output. Kept for explicit CLI readability.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    report = build_review_report(load_json(args.input))
    if args.output_dir:
        report["written_outputs"] = write_outputs(report, args.output_dir)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
