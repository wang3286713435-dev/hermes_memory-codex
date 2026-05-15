#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Sequence

from app.services.asset_catalog.evidence_write_runtime_preflight import (
    build_runtime_evidence_write_preflight_report,
    write_runtime_evidence_write_preflight_report,
)


def build_runtime_preflight_from_file(
    approval_json: Path,
    *,
    expected_git_commit: str,
    worktree_status_file: Path | None = None,
    created_at: str | None = None,
) -> dict[str, Any]:
    approval = json.loads(approval_json.read_text(encoding="utf-8"))
    if not isinstance(approval, dict):
        raise ValueError("Operator approval JSON must be an object.")
    worktree_status_text = (
        worktree_status_file.read_text(encoding="utf-8")
        if worktree_status_file is not None and worktree_status_file.exists()
        else ""
    )
    return build_runtime_evidence_write_preflight_report(
        approval,
        expected_git_commit=expected_git_commit,
        worktree_status_text=worktree_status_text,
        created_at=created_at,
    )


def build_summary(report: dict[str, Any], output_path: Path) -> dict[str, Any]:
    state = report.get("decision", {}).get("runtime_preflight_state")
    safety = report.get("safety", {})
    return {
        "decision": "go" if state == "preflight_ready_for_operator_stop" else state,
        "runtime_preflight_state": state,
        "preflight_artifact_generated": True,
        "preflight_filename": output_path.name,
        "would_invoke_writer": report.get("would_invoke_writer") is True,
        "db_writes": safety.get("db_writes") is True,
        "writer_invoked": safety.get("writer_invoked") is True,
        "parser_invoked": safety.get("parser_invoked") is True,
        "opensearch_writes": safety.get("opensearch_writes") is True,
        "qdrant_writes": safety.get("qdrant_writes") is True,
        "minio_writes": safety.get("minio_writes") is True,
        "agent_answer_integration": safety.get("agent_answer_integration") is True,
        "production_rollout": safety.get("production_rollout") is True,
    }


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Generate an ignored local runtime evidence write preflight report "
            "from an operator approval JSON. This stops before writer invocation."
        )
    )
    parser.add_argument("--approval-json", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--expected-git-commit", required=True)
    parser.add_argument("--worktree-status-file", type=Path)
    parser.add_argument("--created-at")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        report = build_runtime_preflight_from_file(
            args.approval_json,
            expected_git_commit=args.expected_git_commit,
            worktree_status_file=args.worktree_status_file,
            created_at=args.created_at,
        )
        output_path = write_runtime_evidence_write_preflight_report(
            args.output,
            report,
        )
        summary = build_summary(report, output_path)
        json.dump(summary, sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")
        state = report.get("decision", {}).get("runtime_preflight_state")
        return 0 if state == "preflight_ready_for_operator_stop" else 1
    except (OSError, ValueError, json.JSONDecodeError) as error:
        json.dump(
            {
                "decision": "preflight_no_go",
                "runtime_preflight_state": "preflight_no_go",
                "preflight_artifact_generated": False,
                "reason": "runtime_preflight_input_error",
                "error_type": type(error).__name__,
                "would_invoke_writer": False,
                "db_writes": False,
                "writer_invoked": False,
                "parser_invoked": False,
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
