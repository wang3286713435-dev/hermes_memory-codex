#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Sequence

from app.services.asset_catalog.evidence_preflight import (
    build_evidence_write_preflight_report,
    write_evidence_write_preflight_report,
)

DEFAULT_OUTPUT_DIR = Path("reports/nas_evidence_preflight")


def build_preflight_from_files(
    payload_json: Path,
    operator_approval_json: Path,
    *,
    created_at: str | None = None,
) -> dict[str, Any]:
    payload = json.loads(payload_json.read_text(encoding="utf-8"))
    operator_approval = json.loads(operator_approval_json.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("Evidence write payload plan must be a JSON object.")
    if not isinstance(operator_approval, dict):
        raise ValueError("Operator approval must be a JSON object.")
    return build_evidence_write_preflight_report(
        payload,
        operator_approval=operator_approval,
        created_at=created_at,
    )


def build_summary(preflight: dict[str, Any], output_path: Path) -> dict[str, Any]:
    preflight_state = preflight.get("decision", {}).get("preflight_state")
    safety = preflight.get("safety", {})
    return {
        "decision": "go" if preflight_state == "write_preflight_ready_for_dry_run" else preflight_state,
        "preflight_state": preflight_state,
        "preflight_artifact_generated": True,
        "preflight_filename": output_path.name,
        "writes_authorized": preflight.get("writes_authorized") is True,
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
            "Generate an ignored local evidence-write preflight dry-run report "
            "from a sanitized payload plan and operator approval."
        )
    )
    parser.add_argument("--payload-json", type=Path, required=True)
    parser.add_argument("--operator-approval-json", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--created-at")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        preflight = build_preflight_from_files(
            args.payload_json,
            args.operator_approval_json,
            created_at=args.created_at,
        )
        output_path = write_evidence_write_preflight_report(args.output_dir, preflight)
        summary = build_summary(preflight, output_path)
        json.dump(summary, sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")
        return 0
    except (OSError, ValueError, json.JSONDecodeError) as error:
        json.dump(
            {
                "decision": "no_go",
                "preflight_artifact_generated": False,
                "reason": "preflight_input_error",
                "error_type": type(error).__name__,
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
