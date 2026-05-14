#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Sequence

from app.services.asset_catalog.evidence_payload import (
    build_evidence_write_payload_plan,
    write_evidence_write_payload_plan,
)

DEFAULT_OUTPUT_DIR = Path("reports/nas_evidence_payloads")


def build_payload_from_file(
    eligibility_json: Path,
    *,
    human_review_decision: str,
    created_at: str | None = None,
) -> dict[str, Any]:
    payload = json.loads(eligibility_json.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("Evidence write eligibility report must be a JSON object.")
    return build_evidence_write_payload_plan(
        payload,
        human_review_decision=human_review_decision,
        created_at=created_at,
    )


def build_summary(payload: dict[str, Any], output_path: Path) -> dict[str, Any]:
    payload_state = payload.get("decision", {}).get("payload_state")
    safety = payload.get("safety", {})
    return {
        "decision": "go" if payload_state == "payload_ready_for_write_dry_run" else payload_state,
        "payload_state": payload_state,
        "payload_artifact_generated": True,
        "payload_filename": output_path.name,
        "writes_authorized": payload.get("writes_authorized") is True,
        "documents_written": safety.get("documents_written") is True,
        "chunks_written": safety.get("chunks_written") is True,
        "db_writes": safety.get("db_writes") is True,
        "opensearch_writes": safety.get("opensearch_writes") is True,
        "qdrant_writes": safety.get("qdrant_writes") is True,
        "minio_writes": safety.get("minio_writes") is True,
        "agent_answer_integration": safety.get("agent_answer_integration") is True,
        "production_rollout": safety.get("production_rollout") is True,
    }


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Generate an ignored dry-run evidence-write payload plan from a sanitized "
            "eligibility report."
        )
    )
    parser.add_argument("--eligibility-json", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument(
        "--human-review-decision",
        default="needs_more_metadata",
        choices=(
            "approve_for_payload_dry_run_planning",
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
        payload = build_payload_from_file(
            args.eligibility_json,
            human_review_decision=args.human_review_decision,
            created_at=args.created_at,
        )
        output_path = write_evidence_write_payload_plan(args.output_dir, payload)
        summary = build_summary(payload, output_path)
        json.dump(summary, sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")
        return 0
    except (OSError, ValueError, json.JSONDecodeError) as error:
        json.dump(
            {
                "decision": "no_go",
                "payload_artifact_generated": False,
                "reason": str(error),
                "writes_authorized": False,
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
