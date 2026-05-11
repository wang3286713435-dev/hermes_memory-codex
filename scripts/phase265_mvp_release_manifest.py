#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Sequence

PHASE = "Phase 2.65 Mac mini MVP Landing Acceleration Pack"
RECOMMENDED_INSTALL_ROOT = "/Users/hermes/code"
REQUIRED_SERVICES = [
    "postgres",
    "redis",
    "opensearch",
    "minio",
    "qdrant",
    "hermes_memory_api",
    "hermes_agent_cli",
]
REQUIRED_ENV_KEYS = [
    "DATABASE_URL",
    "OPENSEARCH_URL",
    "QDRANT_URL",
    "QDRANT_COLLECTION",
    "ALIYUN_EMBEDDING_API_KEY",
]
OPTIONAL_ENV_KEYS = [
    "ALIYUN_RERANK_API_KEY",
]


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _sensitive_value_present(value: str) -> bool:
    lowered = value.lower()
    return any(marker in lowered for marker in ("api_key=", "token=", "password=", "secret="))


def _build_preflight_commands() -> list[str]:
    return [
        "sw_vers",
        "whoami",
        "git --version",
        "uv --version",
        "docker --version",
        "df -h /Users/hermes",
        "test -d /Users/hermes/code || mkdir -p /Users/hermes/code",
        "test -d /Users/hermes/env || mkdir -p /Users/hermes/env",
        "test -d /Users/hermes/reports || mkdir -p /Users/hermes/reports",
    ]


def _build_install_commands(hermes_memory_ref: str, hermes_agent_ref: str) -> list[str]:
    return [
        "cd /Users/hermes/code/Hermes_memory && git status --short",
        "cd /Users/hermes/code/Hermes_memory && git fetch origin --tags",
        f"cd /Users/hermes/code/Hermes_memory && git checkout {hermes_memory_ref}",
        "cd /Users/hermes/code/hermes-agent && git status --short",
        "cd /Users/hermes/code/hermes-agent && git fetch --all --tags",
        f"cd /Users/hermes/code/hermes-agent && git checkout {hermes_agent_ref}",
        "cd /Users/hermes/code/Hermes_memory && docker compose up -d --build",
        "cd /Users/hermes/code/hermes-agent && ./setup-hermes.sh || true",
    ]


def _build_health_commands() -> list[str]:
    return [
        "cd /Users/hermes/code/Hermes_memory && docker compose ps",
        "curl http://127.0.0.1:8000/health",
        "cd /Users/hermes/code/hermes-agent && hermes chat --help",
    ]


def _build_hard_stop_conditions() -> list[str]:
    return [
        "hermes-agent reviewed ref is missing or unclear",
        "Hermes_memory reviewed ref is missing or unclear",
        "target worktree is dirty before checkout or update",
        "required secret key is missing",
        "operator would need to print or expose a secret value",
        "Docker, git, uv, or required local permission is unavailable",
        "health check fails after startup",
        "an unclear migration, repair, cleanup, backfill, reindex, delete, DB write, or index write is required",
        "Data Steward feature activation or real DB/NAS smoke is requested in this landing pack",
        "production rollout is requested",
    ]


def _pause_reasons(hermes_memory_ref: str, hermes_agent_ref: str) -> list[str]:
    reasons: list[str] = []
    if not hermes_memory_ref or hermes_memory_ref == "NEEDS_REVIEWED_MEMORY_REF":
        reasons.append("missing_reviewed_hermes_memory_ref")
    if not hermes_agent_ref or hermes_agent_ref == "NEEDS_REVIEWED_AGENT_REF":
        reasons.append("missing_reviewed_hermes_agent_ref")
    if _sensitive_value_present(hermes_memory_ref) or _sensitive_value_present(hermes_agent_ref):
        reasons.append("input_ref_contains_sensitive_marker")
    return reasons


def build_release_manifest(
    *,
    hermes_memory_ref: str,
    hermes_agent_ref: str,
    operator: str | None = None,
) -> dict[str, Any]:
    pause_reasons = _pause_reasons(hermes_memory_ref, hermes_agent_ref)
    return {
        "phase": PHASE,
        "generated_at": _utc_now(),
        "operator": operator or "",
        "status": "pause" if pause_reasons else "ready_for_operator_review",
        "pause_reasons": pause_reasons,
        "dry_run": True,
        "read_only": True,
        "production_rollout": False,
        "repair_attempted": False,
        "db_or_index_written": False,
        "real_db_connected": False,
        "nas_scanned": False,
        "destructive_actions": [],
        "secrets_read": False,
        "secrets_printed": False,
        "services_started": False,
        "git_mutation_attempted": False,
        "hermes_memory_ref": hermes_memory_ref,
        "hermes_agent_ref": hermes_agent_ref,
        "recommended_install_root": RECOMMENDED_INSTALL_ROOT,
        "recommended_paths": {
            "hermes_memory": "/Users/hermes/code/Hermes_memory",
            "hermes_agent": "/Users/hermes/code/hermes-agent",
            "env_dir": "/Users/hermes/env",
            "reports_dir": "/Users/hermes/reports",
        },
        "required_services": list(REQUIRED_SERVICES),
        "required_env_keys": list(REQUIRED_ENV_KEYS),
        "optional_env_keys": list(OPTIONAL_ENV_KEYS),
        "preflight_commands": _build_preflight_commands(),
        "install_commands": _build_install_commands(hermes_memory_ref, hermes_agent_ref),
        "health_commands": _build_health_commands(),
        "rollback_notes": [
            "Record previous known-good refs before update.",
            "Rollback only to a reviewed known-good tag or commit.",
            "After rollback, rerun docker compose ps, /health, and hermes chat --help.",
            "Do not run repair, cleanup, backfill, reindex, delete, or production rollout during rollback.",
        ],
        "hard_stop_conditions": _build_hard_stop_conditions(),
        "operator_notes": [
            "This manifest is a read-only install/update plan, not an execution script.",
            "It does not read .env and must not contain secret values.",
            "If hermes-agent reviewed ref is missing, pause before Mac mini installation.",
            "Real DB/NAS/Data Steward smoke is outside this landing pack.",
        ],
    }


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2)
        handle.write("\n")


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build a read-only Mac mini MVP release manifest.")
    parser.add_argument("--hermes-memory-ref", required=True)
    parser.add_argument("--hermes-agent-ref", required=True)
    parser.add_argument("--output-json")
    parser.add_argument("--operator")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    manifest = build_release_manifest(
        hermes_memory_ref=args.hermes_memory_ref,
        hermes_agent_ref=args.hermes_agent_ref,
        operator=args.operator,
    )
    json.dump(manifest, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    if args.output_json:
        _write_json(Path(args.output_json), manifest)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
