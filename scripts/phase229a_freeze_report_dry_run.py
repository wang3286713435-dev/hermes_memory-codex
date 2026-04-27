#!/usr/bin/env python
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_EVIDENCE = {
    "eval_summary": "Phase 2.14 / governance / facts / CLI smoke eval evidence",
    "readiness_report": "Phase 2.25a readiness audit dry-run evidence",
    "repair_plan": "Phase 2.26a repair plan dry-run evidence",
}

OPTIONAL_EVIDENCE = {
    "linkage_summary": "Phase 2.27f archive / review / audit linkage evidence",
}


def load_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"expected JSON object: {_display_path(path)}")
    return data


def build_freeze_report(
    *,
    eval_summary_paths: list[Path],
    readiness_report_path: Path | None,
    repair_plan_path: Path | None,
    linkage_summary_path: Path | None,
    generated_at: str | None = None,
) -> dict[str, Any]:
    generated_at = generated_at or datetime.now(timezone.utc).isoformat()
    evidence_inputs: list[dict[str, Any]] = []

    for path in eval_summary_paths:
        evidence_inputs.append(build_evidence_input("eval_summary", path, load_json(path)))
    if readiness_report_path:
        evidence_inputs.append(build_evidence_input("readiness_report", readiness_report_path, load_json(readiness_report_path)))
    if repair_plan_path:
        evidence_inputs.append(build_evidence_input("repair_plan", repair_plan_path, load_json(repair_plan_path)))
    if linkage_summary_path:
        evidence_inputs.append(build_evidence_input("linkage_summary", linkage_summary_path, load_json(linkage_summary_path)))

    checklist = build_checklist(evidence_inputs)
    status = aggregate_status(checklist)
    risks = build_risks(checklist, evidence_inputs)

    return {
        "phase": "Phase 2.29a",
        "generated_at": generated_at,
        "dry_run": True,
        "status": status,
        "rollout_ready": False,
        "production_rollout": False,
        "repair_executed": False,
        "destructive_actions": [],
        "checklist": checklist,
        "evidence_inputs": evidence_inputs,
        "go_no_go": {
            "mvp_freeze_candidate": status == "pass",
            "production_rollout": False,
            "reasons": go_no_go_reasons(status, checklist),
        },
        "risks": risks,
        "next_steps": next_steps(status),
    }


def build_evidence_input(evidence_type: str, path: Path, payload: dict[str, Any]) -> dict[str, Any]:
    unsafe = unsafe_issues(payload)
    status = evidence_status(payload)
    if unsafe:
        status = "fail"
    return {
        "type": evidence_type,
        "path": _display_path(path),
        "status": status,
        "summary": summary_counters(payload),
        "unsafe_issues": unsafe,
    }


def build_checklist(evidence_inputs: list[dict[str, Any]]) -> list[dict[str, Any]]:
    checklist: list[dict[str, Any]] = []

    for evidence_type, title in REQUIRED_EVIDENCE.items():
        matching = [item for item in evidence_inputs if item["type"] == evidence_type]
        checklist.append(checklist_item(evidence_type, title, matching, required=True))

    for evidence_type, title in OPTIONAL_EVIDENCE.items():
        matching = [item for item in evidence_inputs if item["type"] == evidence_type]
        checklist.append(checklist_item(evidence_type, title, matching, required=False))

    checklist.extend(
        [
            {
                "id": "dry_run_guards",
                "title": "Dry-run safety guards",
                "status": "pass",
                "required": True,
                "reason": "dry_run=true, destructive_actions=[], repair_executed=false are hard-coded in the freeze report.",
            },
            {
                "id": "production_rollout_blocked",
                "title": "Production rollout blocked",
                "status": "pass",
                "required": True,
                "reason": "rollout_ready=false and production_rollout=false are hard-coded in this phase.",
            },
            {
                "id": "facts_answer_boundary",
                "title": "Facts answer boundary preserved",
                "status": "pass",
                "required": True,
                "reason": "Phase 2.29a does not change retrieval, Agent answer generation, or facts_as_answer semantics.",
            },
        ]
    )
    return checklist


def checklist_item(evidence_type: str, title: str, matching: list[dict[str, Any]], *, required: bool) -> dict[str, Any]:
    if not matching:
        return {
            "id": evidence_type,
            "title": title,
            "status": "warn" if required else "not_provided",
            "required": required,
            "evidence_count": 0,
            "reason": "required evidence not provided" if required else "optional evidence not provided",
        }

    statuses = [item["status"] for item in matching]
    if "fail" in statuses:
        status = "fail"
    elif "warn" in statuses:
        status = "warn"
    else:
        status = "pass"
    return {
        "id": evidence_type,
        "title": title,
        "status": status,
        "required": required,
        "evidence_count": len(matching),
        "reason": f"{len(matching)} explicit evidence input(s) provided",
    }


def aggregate_status(checklist: list[dict[str, Any]]) -> str:
    statuses = [item["status"] for item in checklist if item["status"] != "not_provided"]
    if "fail" in statuses:
        return "fail"
    if "warn" in statuses:
        return "warn"
    return "pass"


def build_risks(checklist: list[dict[str, Any]], evidence_inputs: list[dict[str, Any]]) -> list[str]:
    risks: list[str] = []
    missing = [item["id"] for item in checklist if item["required"] and item["status"] == "warn" and item.get("evidence_count") == 0]
    if missing:
        risks.append(f"missing required freeze evidence: {', '.join(missing)}")
    failed = [item["id"] for item in checklist if item["status"] == "fail"]
    if failed:
        risks.append(f"failing or unsafe freeze evidence: {', '.join(failed)}")
    if any(item["status"] == "warn" for item in evidence_inputs):
        risks.append("one or more evidence inputs reported warnings")
    risks.append("production rollout remains out of scope")
    risks.append("repair executor remains out of scope")
    return risks


def go_no_go_reasons(status: str, checklist: list[dict[str, Any]]) -> list[str]:
    reasons = ["production rollout is explicitly out of scope"]
    if status == "pass":
        reasons.append("all required freeze evidence is present and passing")
    elif status == "warn":
        reasons.append("required freeze evidence is incomplete or warning")
    else:
        reasons.append("required freeze evidence contains failing or unsafe input")
    missing_manual = [item["id"] for item in checklist if item["status"] == "not_provided"]
    if missing_manual:
        reasons.append(f"optional manual evidence not provided: {', '.join(missing_manual)}")
    return reasons


def next_steps(status: str) -> list[str]:
    if status == "pass":
        return ["Codex B review", "consider Phase 2.29b readiness freeze baseline decision"]
    if status == "warn":
        return ["collect missing or warning freeze evidence", "rerun Phase 2.29a dry-run with explicit evidence paths"]
    return ["inspect failing or unsafe evidence input", "do not proceed to MVP freeze candidate"]


def evidence_status(payload: dict[str, Any]) -> str:
    status = str(payload.get("status") or "").lower()
    summary = payload.get("summary") if isinstance(payload.get("summary"), dict) else {}
    failed = _as_int(payload.get("failed", summary.get("failed", summary.get("failures", 0))))
    critical = _as_int(summary.get("critical", payload.get("critical", 0)))
    warnings = _as_int(payload.get("warnings", summary.get("warnings", 0)))

    if status in {"fail", "failed", "error"} or failed > 0 or critical > 0:
        return "fail"
    if status in {"warn", "warning"} or warnings > 0:
        return "warn"
    return "pass"


def summary_counters(payload: dict[str, Any]) -> dict[str, int]:
    summary = payload.get("summary") if isinstance(payload.get("summary"), dict) else {}
    return {
        "total": _as_int(payload.get("total", summary.get("total", summary.get("checks_total", 0)))),
        "passed": _as_int(payload.get("passed", summary.get("passed", 0))),
        "failed": _as_int(payload.get("failed", summary.get("failed", summary.get("failures", 0)))),
        "warnings": _as_int(payload.get("warnings", summary.get("warnings", 0))),
        "critical": _as_int(payload.get("critical", summary.get("critical", 0))),
    }


def unsafe_issues(payload: dict[str, Any]) -> list[str]:
    issues: list[str] = []
    if payload.get("dry_run") is False:
        issues.append("dry_run_false")
    if payload.get("destructive_actions"):
        issues.append("destructive_actions_present")
    if payload.get("rollout_ready") is True:
        issues.append("rollout_ready_true")
    if payload.get("production_rollout") is True:
        issues.append("production_rollout_true")
    if payload.get("repair_executed") is True:
        issues.append("repair_executed_true")
    return issues


def _as_int(value: Any) -> int:
    try:
        return int(value or 0)
    except (TypeError, ValueError):
        return 0


def _display_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.name


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build a Phase 2.29a MVP freeze report dry-run.")
    parser.add_argument("--eval-summary", action="append", type=Path, default=[], help="Explicit eval summary JSON path.")
    parser.add_argument("--readiness-report", type=Path, help="Explicit readiness audit JSON path.")
    parser.add_argument("--repair-plan", type=Path, help="Explicit repair plan JSON path.")
    parser.add_argument("--linkage-summary", type=Path, help="Explicit linkage summary JSON path.")
    parser.add_argument("--output-file", type=Path, help="Optional output path. Defaults to stdout only.")
    parser.add_argument("--dry-run-preview", action="store_true", help="Preview output without writing --output-file.")
    parser.add_argument("--fail-on-warn", action="store_true", help="Return non-zero when report status is warn.")
    parser.add_argument("--json", action="store_true", help="Print JSON output.")
    args = parser.parse_args(argv)

    report = build_freeze_report(
        eval_summary_paths=args.eval_summary,
        readiness_report_path=args.readiness_report,
        repair_plan_path=args.repair_plan,
        linkage_summary_path=args.linkage_summary,
    )

    if args.output_file and not args.dry_run_preview:
        args.output_file.parent.mkdir(parents=True, exist_ok=True)
        args.output_file.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(json.dumps(report, ensure_ascii=False, indent=2))

    if report["status"] == "fail":
        return 2
    if args.fail_on_warn and report["status"] == "warn":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
