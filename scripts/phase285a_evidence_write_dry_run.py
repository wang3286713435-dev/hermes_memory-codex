#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Sequence

from app.services.asset_catalog.evidence_write_dry_run import (
    build_evidence_write_dry_run_report,
    write_evidence_write_dry_run_report,
)

DEFAULT_OUTPUT_DIR = Path("reports/nas_evidence_write_dry_run")


def build_write_dry_run_from_file(
    preflight_json: Path,
    *,
    created_at: str | None = None,
) -> dict[str, Any]:
    preflight = json.loads(preflight_json.read_text(encoding="utf-8"))
    if not isinstance(preflight, dict):
        raise ValueError("Evidence write preflight report must be a JSON object.")
    return build_evidence_write_dry_run_report(preflight, created_at=created_at)


def build_summary(report: dict[str, Any], output_path: Path) -> dict[str, Any]:
    state = report.get("decision", {}).get("write_dry_run_state")
    safety = report.get("safety", {})
    return {
        "decision": "go" if state == "write_dry_run_go" else state,
        "write_dry_run_state": state,
        "write_dry_run_artifact_generated": True,
        "write_dry_run_filename": output_path.name,
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
            "Generate an ignored local evidence-write dry-run report from a "
            "sanitized preflight report."
        )
    )
    parser.add_argument("--preflight-json", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--created-at")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        report = build_write_dry_run_from_file(
            args.preflight_json,
            created_at=args.created_at,
        )
        output_path = write_evidence_write_dry_run_report(args.output_dir, report)
        summary = build_summary(report, output_path)
        json.dump(summary, sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")
        return 0
    except (OSError, ValueError, json.JSONDecodeError) as error:
        json.dump(
            {
                "decision": "no_go",
                "write_dry_run_artifact_generated": False,
                "reason": "write_dry_run_input_error",
                "error_type": type(error).__name__,
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
