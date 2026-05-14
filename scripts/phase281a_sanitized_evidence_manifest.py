#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Sequence

from app.services.asset_catalog.evidence_manifest import (
    UnsafeParserPreviewError,
    build_sanitized_evidence_manifest,
    write_sanitized_evidence_manifest,
)

DEFAULT_OUTPUT_DIR = Path("reports/nas_evidence_manifests")


def build_manifest_from_file(
    input_json: Path,
    *,
    created_at: str | None = None,
) -> dict[str, Any]:
    payload = json.loads(input_json.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise UnsafeParserPreviewError("Sanitized parser preview must be a JSON object.")
    return build_sanitized_evidence_manifest(payload, created_at=created_at)


def build_summary(manifest: dict[str, Any], output_path: Path) -> dict[str, Any]:
    decision = manifest.get("decision", {})
    safety = manifest.get("safety", {})
    manifest_status = decision.get("manifest_status")
    return {
        "decision": "go" if manifest_status == "ready_for_review" else manifest_status,
        "manifest_status": manifest_status,
        "manifest_artifact_generated": True,
        "manifest_filename": output_path.name,
        "raw_text_output": safety.get("raw_text_output") is True,
        "true_filename_output": safety.get("true_filename_output") is True,
        "true_nas_path_output": safety.get("true_nas_path_output") is True,
        "raw_row_output": safety.get("raw_row_output") is True,
        "secret_printed": safety.get("secret_printed") is True,
        "true_business_data_output": safety.get("true_business_data_output") is True,
        "documents_written": safety.get("documents_written") is True,
        "chunks_written": safety.get("chunks_written") is True,
        "db_writes": safety.get("db_writes") is True,
        "opensearch_writes": safety.get("opensearch_writes") is True,
        "qdrant_writes": safety.get("qdrant_writes") is True,
        "minio_writes": safety.get("minio_writes") is True,
        "agent_answer_integration": safety.get("agent_answer_integration") is True,
        "production_rollout": False,
    }


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate an ignored sanitized NAS evidence manifest from parser-preview metadata."
    )
    parser.add_argument("--input-json", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--created-at")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        manifest = build_manifest_from_file(args.input_json, created_at=args.created_at)
        output_path = write_sanitized_evidence_manifest(args.output_dir, manifest)
        summary = build_summary(manifest, output_path)
        json.dump(summary, sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")
        return 0
    except UnsafeParserPreviewError as error:
        json.dump(
            {
                "decision": "no_go",
                "manifest_artifact_generated": False,
                "reason": str(error),
                "secret_printed": False,
                "raw_text_output": False,
                "true_filename_output": False,
                "true_nas_path_output": False,
                "raw_row_output": False,
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
