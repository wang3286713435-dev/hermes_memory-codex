#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Sequence

from app.services.asset_catalog.evidence_write_rehearsal import (
    SQLiteEvidenceWriteRehearsalStore,
    build_evidence_write_rehearsal_report,
    write_evidence_write_rehearsal_report,
)

DEFAULT_OUTPUT_DIR = Path("reports/nas_evidence_write_rehearsal")


def build_rehearsal_from_file(
    write_dry_run_json: Path,
    *,
    created_at: str | None = None,
    sqlite_path: Path | None = None,
) -> dict[str, Any]:
    write_dry_run = json.loads(write_dry_run_json.read_text(encoding="utf-8"))
    if not isinstance(write_dry_run, dict):
        raise ValueError("Evidence write dry-run report must be a JSON object.")
    store_path = sqlite_path or Path(":memory:")
    store = SQLiteEvidenceWriteRehearsalStore(store_path)
    return build_evidence_write_rehearsal_report(
        write_dry_run,
        created_at=created_at,
        store=store,
    )


def build_summary(report: dict[str, Any], output_path: Path) -> dict[str, Any]:
    state = report.get("decision", {}).get("rehearsal_state")
    safety = report.get("safety", {})
    temp_store = report.get("temp_store", {})
    return {
        "decision": "go" if state == "rehearsal_go" else state,
        "rehearsal_state": state,
        "rehearsal_artifact_generated": True,
        "rehearsal_filename": output_path.name,
        "temp_store_backend": temp_store.get("backend"),
        "documents_written": safety.get("documents_written") is True,
        "document_versions_written": safety.get("document_versions_written") is True,
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
            "Run a temp repository evidence-write rehearsal from a sanitized "
            "evidence write dry-run report."
        )
    )
    parser.add_argument("--write-dry-run-json", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--created-at")
    parser.add_argument("--sqlite-path", type=Path)
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        report = build_rehearsal_from_file(
            args.write_dry_run_json,
            created_at=args.created_at,
            sqlite_path=args.sqlite_path,
        )
        output_path = write_evidence_write_rehearsal_report(args.output_dir, report)
        summary = build_summary(report, output_path)
        json.dump(summary, sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")
        return 0
    except (OSError, ValueError, json.JSONDecodeError) as error:
        json.dump(
            {
                "decision": "no_go",
                "rehearsal_artifact_generated": False,
                "reason": "rehearsal_input_error",
                "error_type": type(error).__name__,
                "documents_written": False,
                "document_versions_written": False,
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
