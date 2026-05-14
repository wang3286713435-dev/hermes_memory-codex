#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Sequence

from app.services.asset_catalog.evidence_eligibility import (
    build_evidence_write_eligibility_report,
    write_evidence_write_eligibility_report,
)

DEFAULT_OUTPUT_DIR = Path("reports/nas_evidence_eligibility")


def build_report_from_file(
    manifest_json: Path,
    *,
    human_review_decision: str,
    created_at: str | None = None,
) -> dict[str, Any]:
    payload = json.loads(manifest_json.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("Sanitized evidence manifest must be a JSON object.")
    return build_evidence_write_eligibility_report(
        payload,
        human_review_decision=human_review_decision,
        created_at=created_at,
    )


def build_summary(report: dict[str, Any], output_path: Path) -> dict[str, Any]:
    eligibility_state = report.get("eligibility_state")
    return {
        "decision": "go"
        if eligibility_state == "eligible_for_evidence_write_planning"
        else eligibility_state,
        "eligibility_state": eligibility_state,
        "eligibility_report_generated": True,
        "eligibility_report_filename": output_path.name,
        "writes_authorized": report.get("writes_authorized") is True,
        "parser_invoked": report.get("parser_invoked") is True,
        "scratch_copy_performed": report.get("scratch_copy_performed") is True,
        "documents_written": report.get("documents_written") is True,
        "chunks_written": report.get("chunks_written") is True,
        "db_writes": report.get("db_writes") is True,
        "opensearch_writes": report.get("opensearch_writes") is True,
        "qdrant_writes": report.get("qdrant_writes") is True,
        "minio_writes": report.get("minio_writes") is True,
        "agent_answer_integration": report.get("agent_answer_integration") is True,
        "production_rollout": report.get("production_rollout") is True,
        "permission_default": report.get("permission_default"),
    }


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Generate an ignored dry-run eligibility report from a sanitized NAS "
            "evidence manifest."
        )
    )
    parser.add_argument("--manifest-json", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument(
        "--human-review-decision",
        default="needs_more_metadata",
        choices=(
            "approve_for_evidence_write_planning",
            "needs_more_metadata",
            "reject_sensitive_or_unsafe",
            "reject_unsupported_type",
            "reject_permission_unclear",
        ),
    )
    parser.add_argument("--created-at")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        report = build_report_from_file(
            args.manifest_json,
            human_review_decision=args.human_review_decision,
            created_at=args.created_at,
        )
        output_path = write_evidence_write_eligibility_report(args.output_dir, report)
        summary = build_summary(report, output_path)
        json.dump(summary, sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")
        return 0
    except (OSError, ValueError, json.JSONDecodeError) as error:
        json.dump(
            {
                "decision": "no_go",
                "eligibility_report_generated": False,
                "reason": str(error),
                "writes_authorized": False,
                "parser_invoked": False,
                "scratch_copy_performed": False,
                "documents_written": False,
                "chunks_written": False,
                "db_writes": False,
                "opensearch_writes": False,
                "qdrant_writes": False,
                "minio_writes": False,
                "agent_answer_integration": False,
                "production_rollout": False,
            },
            sys.stdout,
            ensure_ascii=False,
            indent=2,
        )
        sys.stdout.write("\n")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
