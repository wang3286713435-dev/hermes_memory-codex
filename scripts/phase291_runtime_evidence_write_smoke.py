#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Sequence

from app.services.asset_catalog.evidence_write_runtime_smoke import (
    READY_STATE,
    build_runtime_evidence_writer_smoke_report,
    write_runtime_evidence_writer_smoke_report,
)


def build_runtime_smoke_from_files(
    *,
    approval_json: Path,
    preflight_report: Path,
    payload_json: Path,
    output: Path,
    expected_git_commit: str,
    worktree_status_file: Path | None = None,
    execute_writer: bool = False,
) -> tuple[dict[str, Any], Path]:
    approval = _read_json_object(approval_json, "operator approval")
    preflight = _read_json_object(preflight_report, "preflight report")
    payload = _read_json_object(payload_json, "payload")
    worktree_status_text = (
        worktree_status_file.read_text(encoding="utf-8")
        if worktree_status_file is not None and worktree_status_file.exists()
        else ""
    )

    # The CLI has no DB session injection by design. If --execute-writer is
    # supplied here, the service returns a safe pause instead of writing.
    report = build_runtime_evidence_writer_smoke_report(
        approval=approval,
        preflight_report=preflight,
        payload=payload,
        expected_git_commit=expected_git_commit,
        worktree_status_text=worktree_status_text,
        execute_writer=execute_writer,
        db=None,
    )
    output_path = write_runtime_evidence_writer_smoke_report(output, report)
    return report, output_path


def build_summary(report: dict[str, Any], output_path: Path) -> dict[str, Any]:
    return {
        "decision": report.get("decision"),
        "smoke_report_generated": True,
        "smoke_report_filename": output_path.name,
        "would_invoke_writer": report.get("would_invoke_writer") is True,
        "writer_invoked": report.get("writer_invoked") is True,
        "db_writes": report.get("db_writes") is True,
        "sanitized": report.get("sanitized") is True,
        "pause_reasons": report.get("pause_reasons", []),
        "no_go_reasons": report.get("no_go_reasons", []),
    }


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Build a sanitized Phase 2.91 runtime evidence writer smoke gate "
            "report. Default mode is gate-only and never calls the writer."
        )
    )
    parser.add_argument("--approval-json", type=Path, required=True)
    parser.add_argument("--preflight-report", type=Path, required=True)
    parser.add_argument("--payload-json", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--expected-git-commit", required=True)
    parser.add_argument("--worktree-status-file", type=Path)
    parser.add_argument(
        "--execute-writer",
        action="store_true",
        help=(
            "Explicit writer execution request. The CLI has no DB session and "
            "will pause safely; execution is only supported by injected test sessions."
        ),
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        report, output_path = build_runtime_smoke_from_files(
            approval_json=args.approval_json,
            preflight_report=args.preflight_report,
            payload_json=args.payload_json,
            output=args.output,
            expected_git_commit=args.expected_git_commit,
            worktree_status_file=args.worktree_status_file,
            execute_writer=args.execute_writer,
        )
        json.dump(build_summary(report, output_path), sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")
        return 0 if report.get("decision") == READY_STATE else 1
    except (OSError, ValueError, json.JSONDecodeError) as error:
        json.dump(
            {
                "decision": "writer_smoke_no_go",
                "smoke_report_generated": False,
                "reason": "runtime_writer_smoke_input_error",
                "error_type": type(error).__name__,
                "would_invoke_writer": False,
                "writer_invoked": False,
                "db_writes": False,
                "sanitized": True,
            },
            sys.stdout,
            ensure_ascii=False,
            indent=2,
        )
        sys.stdout.write("\n")
        return 2


def _read_json_object(path: Path, label: str) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{label} JSON must be an object.")
    return value


if __name__ == "__main__":
    raise SystemExit(main())
