#!/usr/bin/env python
from __future__ import annotations

import argparse
import json
import os
import subprocess
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Mapping, Sequence

PHASE = "Phase 2.60 Internal MVP Launch Readiness Pack"
DANGEROUS_ENV_FLAGS = (
    "HERMES_CLEANUP_AUTHORIZED",
    "HERMES_REPAIR_AUTHORIZED",
    "HERMES_BACKFILL_AUTHORIZED",
    "HERMES_REINDEX_AUTHORIZED",
    "HERMES_ROLLOUT_AUTHORIZED",
)
TRUE_VALUES = {"1", "true", "yes", "on"}


def make_check(check_id: str, status: str, message: str, **details: Any) -> dict[str, Any]:
    return {
        "id": check_id,
        "status": status,
        "message": message,
        "details": details,
    }


def aggregate_status(checks: list[dict[str, Any]]) -> str:
    statuses = {check["status"] for check in checks}
    if "no_go" in statuses:
        return "no_go"
    if "pause" in statuses:
        return "pause"
    return "go"


def run_git(args: Sequence[str], *, cwd: Path) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=cwd,
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError((result.stderr or result.stdout or "git command failed").strip())
    return result.stdout.strip()


def check_api_health(api_url: str) -> tuple[bool, str]:
    health_url = api_url.rstrip("/") + "/health"
    try:
        with urllib.request.urlopen(health_url, timeout=3) as response:
            status_code = getattr(response, "status", response.getcode())
            if 200 <= int(status_code) < 300:
                return True, f"/health returned HTTP {status_code}"
            return False, f"/health returned HTTP {status_code}"
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        return False, str(exc)


def _path_exists_check(workspace_root: Path, relative_path: str, check_id: str, label: str) -> dict[str, Any]:
    path = workspace_root / relative_path
    if path.exists():
        return make_check(check_id, "pass", f"{label} exists.", path=relative_path)
    return make_check(check_id, "pause", f"{label} is missing.", path=relative_path)


def _latest_json_check(workspace_root: Path) -> dict[str, Any]:
    path = workspace_root / "reports" / "agent_runs" / "latest.json"
    if not path.exists():
        return make_check("latest_json_present", "pause", "reports/agent_runs/latest.json is missing.")
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return make_check("latest_json_present", "pause", f"latest.json is not valid JSON: {exc}")
    return make_check(
        "latest_json_present",
        "pass",
        "reports/agent_runs/latest.json is present and parseable.",
        phase=payload.get("phase"),
        latest_status=payload.get("status"),
    )


def _dangerous_env_check(env: Mapping[str, str]) -> dict[str, Any]:
    dangerous = [
        key
        for key in DANGEROUS_ENV_FLAGS
        if str(env.get(key, "")).strip().lower() in TRUE_VALUES
    ]
    if dangerous:
        return make_check(
            "dangerous_env_flags_absent",
            "no_go",
            "Dangerous authorization environment flags are enabled.",
            dangerous_flags=dangerous,
        )
    return make_check(
        "dangerous_env_flags_absent",
        "pass",
        "No dangerous authorization environment flags are enabled.",
        checked_flags=list(DANGEROUS_ENV_FLAGS),
    )


def build_readiness_report(
    *,
    workspace_root: Path,
    api_url: str,
    skip_api_health: bool,
    env: Mapping[str, str] | None = None,
    git_runner: Callable[[Sequence[str]], str] | None = None,
    health_checker: Callable[[str], tuple[bool, str]] = check_api_health,
) -> dict[str, Any]:
    workspace_root = workspace_root.expanduser().resolve()
    env = env if env is not None else os.environ

    def git(args: Sequence[str]) -> str:
        if git_runner is not None:
            return git_runner(args, cwd=workspace_root)
        return run_git(args, cwd=workspace_root)

    checks: list[dict[str, Any]] = []
    try:
        head = git(["rev-parse", "--short", "HEAD"])
        checks.append(make_check("repo_head_present", "pass", "Current Git HEAD is readable.", head=head))
    except Exception as exc:  # noqa: BLE001 - diagnostics runner should report, not crash.
        checks.append(make_check("repo_head_present", "pause", f"Could not read Git HEAD: {exc}"))

    try:
        tag = git(["describe", "--tags", "--abbrev=0"])
        checks.append(make_check("baseline_tag_present", "pass", "Latest Git tag is readable.", tag=tag))
    except Exception as exc:  # noqa: BLE001
        checks.append(make_check("baseline_tag_present", "pause", f"Could not read latest Git tag: {exc}"))

    checks.append(_latest_json_check(workspace_root))
    checks.append(
        _path_exists_check(
            workspace_root,
            "docs/MAC_MINI_NATURAL_IMPORT_OPERATOR_CHECKLIST.md",
            "operator_checklist_present",
            "Mac mini natural import operator checklist",
        )
    )
    checks.append(
        _path_exists_check(
            workspace_root,
            "docs/NEXT_CODEX_C_PROMPT.md",
            "codex_c_prompt_present",
            "Codex C pending authorization prompt",
        )
    )
    checks.append(
        _path_exists_check(
            workspace_root,
            "docs/PHASE259_NATURAL_IMPORT_SECOND_SMOKE_PLAN.md",
            "second_smoke_gate_documented",
            "Phase 2.59 second smoke gate document",
        )
    )
    checks.append(
        _path_exists_check(
            workspace_root,
            "scripts/run_local_api.sh",
            "run_local_api_script_present",
            "Local API helper script",
        )
    )

    if skip_api_health:
        checks.append(
            make_check(
                "api_health_optional",
                "pass",
                "API health check skipped by operator flag.",
                skipped=True,
                api_url=api_url,
            )
        )
    else:
        ok, message = health_checker(api_url)
        checks.append(
            make_check(
                "api_health_optional",
                "pass" if ok else "pause",
                message if ok else f"API health check failed: {message}",
                skipped=False,
                api_url=api_url,
            )
        )

    checks.append(_dangerous_env_check(env))
    checks.append(
        make_check(
            "data_steward_not_active",
            "pass",
            "Phase 2.60 does not require DB/NAS/Data Steward activation.",
        )
    )

    status = aggregate_status(checks)
    return {
        "phase": PHASE,
        "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "dry_run": True,
        "read_only": True,
        "destructive_actions": [],
        "real_upload_called": False,
        "api_smoke_called": False,
        "cli_smoke_called": False,
        "db_or_index_written": False,
        "production_rollout": False,
        "status": status,
        "checks": checks,
        "known_risks": [
            "Readiness Go only means internal controlled MVP use may proceed with a human operator.",
            "This runner does not perform a second real natural import smoke.",
            "This runner does not start services, upload files, repair data, or write DB/index state.",
        ],
        "operator_next_steps": _operator_next_steps(status),
    }


def _operator_next_steps(status: str) -> list[str]:
    if status == "go":
        return [
            "Proceed only with internal controlled MVP usage under human operator supervision.",
            "Use the Mac mini operator checklist before any real natural import.",
            "Do not treat this as production rollout approval.",
        ]
    if status == "pause":
        return [
            "Resolve pause checks before internal MVP usage.",
            "Do not upload files or run CLI smoke as part of this readiness check.",
            "Re-run this dry-run after prerequisites are restored.",
        ]
    return [
        "Stop and review no-go checks with Codex B / human owner.",
        "Do not perform repair, cleanup, reindex, backfill, or rollout.",
        "Clear dangerous authorization signals before continuing.",
    ]


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build a read-only internal MVP local readiness report.")
    parser.add_argument("--workspace-root", default=".")
    parser.add_argument("--api-url")
    parser.add_argument("--skip-api-health", action="store_true")
    parser.add_argument("--output-json")
    return parser.parse_args(argv)


def main(
    argv: Sequence[str] | None = None,
    *,
    env: Mapping[str, str] | None = None,
    git_runner: Callable[[Sequence[str]], str] | None = None,
    health_checker: Callable[[str], tuple[bool, str]] = check_api_health,
) -> int:
    args = parse_args(argv)
    env = env if env is not None else os.environ
    api_url = args.api_url or env.get("HERMES_MEMORY_API_BASE_URL") or "http://127.0.0.1:8000"
    report = build_readiness_report(
        workspace_root=Path(args.workspace_root),
        api_url=api_url,
        skip_api_health=args.skip_api_health,
        env=env,
        git_runner=git_runner,
        health_checker=health_checker,
    )
    output = json.dumps(report, ensure_ascii=False, indent=2)
    if args.output_json:
        output_path = Path(args.output_json).expanduser()
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(output + "\n", encoding="utf-8")
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
