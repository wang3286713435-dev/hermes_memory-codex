#!/usr/bin/env python
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any, Callable

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_ENV_KEYS = (
    "DATABASE_URL",
    "OPENSEARCH_URL",
    "QDRANT_URL",
    "QDRANT_COLLECTION",
)


def make_check(
    *,
    check_id: str,
    category: str,
    status: str,
    message: str,
    stop_required: bool = False,
    human_action_required: bool = False,
) -> dict[str, Any]:
    return {
        "id": check_id,
        "category": category,
        "status": status,
        "message": message,
        "stop_required": stop_required,
        "human_action_required": human_action_required,
    }


def build_summary(checks: list[dict[str, Any]]) -> dict[str, Any]:
    failures = sum(1 for check in checks if check["status"] == "fail")
    warnings = sum(1 for check in checks if check["status"] == "warn")
    passed = sum(1 for check in checks if check["status"] == "pass")
    status = "fail" if failures else "warn" if warnings else "pass"
    return {
        "dry_run": True,
        "writes_db": False,
        "repairs": False,
        "rollout_approved": False,
        "status": status,
        "checks_total": len(checks),
        "passed": passed,
        "warnings": warnings,
        "failures": failures,
        "stop_required": any(bool(check.get("stop_required")) for check in checks),
        "human_action_required": [
            check["id"] for check in checks if bool(check.get("human_action_required"))
        ],
        "checks": checks,
    }


def parse_env_file(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[len("export ") :].strip()
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        if not key:
            continue
        values[key] = value.strip().strip("'\"")
    return values


def env_checks(
    *,
    env_file: Path | None,
    expected_qdrant_collection: str | None,
) -> list[dict[str, Any]]:
    if env_file is None:
        checks = [
            make_check(
                check_id="env_file",
                category="env",
                status="skipped",
                message="No env file provided; key-name checks skipped.",
            )
        ]
        if expected_qdrant_collection:
            checks.append(
                make_check(
                    check_id="qdrant_collection",
                    category="env",
                    status="skipped",
                    message="No env file provided; QDRANT_COLLECTION expectation skipped.",
                )
            )
        return checks
    if not env_file.exists():
        checks = [
            make_check(
                check_id="env_file",
                category="env",
                status="warn",
                message="Env file path does not exist; no values were read.",
                human_action_required=True,
            )
        ]
        if expected_qdrant_collection:
            checks.append(
                make_check(
                    check_id="qdrant_collection",
                    category="env",
                    status="skipped",
                    message="Env file missing; QDRANT_COLLECTION expectation skipped.",
                )
            )
        return checks

    env_values = parse_env_file(env_file)
    present = set(env_values)
    missing = [key for key in REQUIRED_ENV_KEYS if key not in present]
    checks = [
        make_check(
            check_id="env_file",
            category="env",
            status="pass",
            message="Env file exists; values were not printed.",
        ),
        make_check(
            check_id="env_required_keys",
            category="env",
            status="warn" if missing else "pass",
            message=(
                f"Missing required key names: {', '.join(missing)}."
                if missing
                else "Required env key names are present; values were not printed."
            ),
            human_action_required=bool(missing),
        ),
    ]
    if expected_qdrant_collection:
        actual = env_values.get("QDRANT_COLLECTION")
        if actual is None:
            checks.append(
                make_check(
                    check_id="qdrant_collection",
                    category="env",
                    status="fail",
                    message="QDRANT_COLLECTION key is missing.",
                    stop_required=True,
                    human_action_required=True,
                )
            )
        elif actual != expected_qdrant_collection:
            checks.append(
                make_check(
                    check_id="qdrant_collection",
                    category="env",
                    status="fail",
                    message="QDRANT_COLLECTION does not match expected value.",
                    stop_required=True,
                    human_action_required=True,
                )
            )
        else:
            checks.append(
                make_check(
                    check_id="qdrant_collection",
                    category="env",
                    status="pass",
                    message="QDRANT_COLLECTION matches expected value.",
                )
            )
    return checks


def run_git(args: list[str], *, cwd: Path = ROOT) -> subprocess.CompletedProcess[str]:
    return subprocess.run(["git", *args], cwd=cwd, check=False, capture_output=True, text=True)


def git_checks(*, cwd: Path = ROOT) -> list[dict[str, Any]]:
    commit = run_git(["rev-parse", "--short", "HEAD"], cwd=cwd)
    status = run_git(["status", "--short"], cwd=cwd)
    checks = []
    if commit.returncode == 0 and commit.stdout.strip():
        checks.append(
            make_check(
                check_id="git_commit",
                category="git",
                status="pass",
                message=f"Current commit: {commit.stdout.strip()}.",
            )
        )
    else:
        checks.append(
            make_check(
                check_id="git_commit",
                category="git",
                status="warn",
                message="Could not read current Git commit.",
                human_action_required=True,
            )
        )
    if status.returncode != 0:
        checks.append(
            make_check(
                check_id="git_dirty",
                category="git",
                status="warn",
                message="Could not inspect Git worktree status.",
                human_action_required=True,
            )
        )
    elif status.stdout.strip():
        checks.append(
            make_check(
                check_id="git_dirty",
                category="git",
                status="warn",
                message="Git worktree has dirty files; review before deployment.",
                human_action_required=True,
            )
        )
    else:
        checks.append(
            make_check(
                check_id="git_dirty",
                category="git",
                status="pass",
                message="Git worktree is clean.",
            )
        )
    return checks


def mount_path_check(path: Path) -> dict[str, Any]:
    if path.exists() and os.access(path, os.R_OK):
        return make_check(
            check_id=f"mount:{path}",
            category="mount",
            status="pass",
            message="Mount path exists and is readable.",
        )
    return make_check(
        check_id=f"mount:{path}",
        category="mount",
        status="warn",
        message="Mount path is missing or not readable.",
        human_action_required=True,
    )


def parse_check_url(value: str) -> tuple[str, str]:
    if "=" not in value:
        raise ValueError("--check-url must use NAME=URL format")
    name, url = value.split("=", 1)
    name = name.strip()
    url = url.strip()
    if not name or not url:
        raise ValueError("--check-url must include non-empty NAME and URL")
    if not (url.startswith("http://") or url.startswith("https://")):
        raise ValueError("--check-url only supports http:// or https:// URLs")
    return name, url


def url_check(
    value: str,
    *,
    timeout: float = 2.0,
    urlopen: Callable[..., Any] = urllib.request.urlopen,
) -> dict[str, Any]:
    name, url = parse_check_url(value)
    try:
        request = urllib.request.Request(url, method="HEAD")
        response = urlopen(request, timeout=timeout)
        code = int(getattr(response, "status", 200))
        if 200 <= code < 400:
            return make_check(
                check_id=f"url:{name}",
                category="url",
                status="pass",
                message=f"{name} is reachable with HEAD.",
            )
    except urllib.error.HTTPError as exc:
        if exc.code != 405:
            return make_check(
                check_id=f"url:{name}",
                category="url",
                status="warn",
                message=f"{name} returned HTTP {exc.code}.",
                human_action_required=True,
            )
    except Exception as exc:  # noqa: BLE001 - diagnostic runner must not crash on reachability failure.
        return make_check(
            check_id=f"url:{name}",
            category="url",
            status="warn",
            message=f"{name} is not reachable: {exc.__class__.__name__}.",
            human_action_required=True,
        )

    try:
        request = urllib.request.Request(url, method="GET")
        response = urlopen(request, timeout=timeout)
        code = int(getattr(response, "status", 200))
        if 200 <= code < 400:
            return make_check(
                check_id=f"url:{name}",
                category="url",
                status="pass",
                message=f"{name} is reachable with GET.",
            )
        return make_check(
            check_id=f"url:{name}",
            category="url",
            status="warn",
            message=f"{name} returned HTTP {code}.",
            human_action_required=True,
        )
    except Exception as exc:  # noqa: BLE001 - diagnostic runner must not crash on reachability failure.
        return make_check(
            check_id=f"url:{name}",
            category="url",
            status="warn",
            message=f"{name} is not reachable: {exc.__class__.__name__}.",
            human_action_required=True,
        )


def latest_json_ignore_check(
    *,
    cwd: Path = ROOT,
    runner: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run,
) -> dict[str, Any]:
    target = "reports/agent_runs/latest.json"
    result = runner(
        ["git", "check-ignore", "-q", target],
        cwd=cwd,
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode == 0:
        return make_check(
            check_id="latest_json_ignored",
            category="runtime_path",
            status="pass",
            message="reports/agent_runs/latest.json is ignored by Git.",
        )
    return make_check(
        check_id="latest_json_ignored",
        category="runtime_path",
        status="warn",
        message="reports/agent_runs/latest.json is not ignored by Git.",
        human_action_required=True,
    )


def collect_checks(args: argparse.Namespace) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []
    checks.extend(git_checks())
    env_file = Path(args.env_file).expanduser() if args.env_file else None
    checks.extend(
        env_checks(
            env_file=env_file,
            expected_qdrant_collection=args.expect_qdrant_collection,
        )
    )
    for path_value in args.mount_path or []:
        checks.append(mount_path_check(Path(path_value).expanduser()))
    for url_value in args.check_url or []:
        checks.append(url_check(url_value))
    checks.append(latest_json_ignore_check())
    return checks


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Phase 2.45c read-only health-check dry-run runner.")
    parser.add_argument("--json", action="store_true", help="Emit JSON summary.")
    parser.add_argument("--env-file", help="Optional env file path; only key names are inspected.")
    parser.add_argument("--mount-path", action="append", help="Optional mount path to check; can be repeated.")
    parser.add_argument("--check-url", action="append", help="Optional NAME=URL reachability check; can be repeated.")
    parser.add_argument("--expect-qdrant-collection", help="Expected QDRANT_COLLECTION value.")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    checks = collect_checks(args)
    summary = build_summary(checks)
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
