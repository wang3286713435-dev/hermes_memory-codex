from __future__ import annotations

import importlib.util
import json
from pathlib import Path

MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "phase265_mvp_release_manifest.py"
SPEC = importlib.util.spec_from_file_location("phase265_mvp_release_manifest", MODULE_PATH)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)

build_release_manifest = MODULE.build_release_manifest
main = MODULE.main


def test_manifest_has_fixed_readonly_safety_fields():
    manifest = build_release_manifest(
        hermes_memory_ref="phase-2.64b-data-steward-selective-integration-baseline",
        hermes_agent_ref="agent-reviewed-tag",
        operator="codex-a",
    )

    assert manifest["status"] == "ready_for_operator_review"
    assert manifest["dry_run"] is True
    assert manifest["read_only"] is True
    assert manifest["production_rollout"] is False
    assert manifest["repair_attempted"] is False
    assert manifest["db_or_index_written"] is False
    assert manifest["real_db_connected"] is False
    assert manifest["nas_scanned"] is False
    assert manifest["destructive_actions"] == []
    assert manifest["secrets_read"] is False
    assert manifest["secrets_printed"] is False
    assert manifest["services_started"] is False
    assert manifest["git_mutation_attempted"] is False


def test_manifest_contains_required_services_env_and_paths():
    manifest = build_release_manifest(
        hermes_memory_ref="phase-2.64b-data-steward-selective-integration-baseline",
        hermes_agent_ref="agent-reviewed-tag",
    )

    assert manifest["recommended_install_root"] == "/Users/hermes/code"
    assert manifest["recommended_paths"]["hermes_memory"] == "/Users/hermes/code/Hermes_memory"
    assert manifest["recommended_paths"]["hermes_agent"] == "/Users/hermes/code/hermes-agent"
    assert set(manifest["required_services"]) >= {
        "postgres",
        "redis",
        "opensearch",
        "minio",
        "qdrant",
        "hermes_memory_api",
        "hermes_agent_cli",
    }
    assert set(manifest["required_env_keys"]) >= {
        "DATABASE_URL",
        "OPENSEARCH_URL",
        "QDRANT_URL",
        "QDRANT_COLLECTION",
        "ALIYUN_EMBEDDING_API_KEY",
    }
    assert manifest["optional_env_keys"] == ["ALIYUN_RERANK_API_KEY"]


def test_missing_agent_ref_marks_pause():
    manifest = build_release_manifest(
        hermes_memory_ref="phase-2.64b-data-steward-selective-integration-baseline",
        hermes_agent_ref="NEEDS_REVIEWED_AGENT_REF",
    )

    assert manifest["status"] == "pause"
    assert manifest["pause_reasons"] == ["missing_reviewed_hermes_agent_ref"]


def test_reviewed_agent_tag_is_ready_for_operator_review():
    manifest = build_release_manifest(
        hermes_memory_ref="phase-2.64b-data-steward-selective-integration-baseline",
        hermes_agent_ref="phase-2.56e-natural-import-real-upload-smoke-baseline",
    )

    assert manifest["status"] == "ready_for_operator_review"
    assert manifest["pause_reasons"] == []
    assert manifest["hermes_agent_ref"] == "phase-2.56e-natural-import-real-upload-smoke-baseline"


def test_manifest_does_not_include_secret_values_from_refs():
    manifest = build_release_manifest(
        hermes_memory_ref="phase-2.64b-data-steward-selective-integration-baseline",
        hermes_agent_ref="token=abc123",
    )

    assert manifest["status"] == "pause"
    assert "input_ref_contains_sensitive_marker" in manifest["pause_reasons"]
    assert manifest["secrets_read"] is False
    assert manifest["secrets_printed"] is False


def test_output_json_only_writes_when_explicit(tmp_path):
    output = tmp_path / "manifest.json"

    exit_code = main(
        [
            "--hermes-memory-ref",
            "phase-2.64b-data-steward-selective-integration-baseline",
            "--hermes-agent-ref",
            "NEEDS_REVIEWED_AGENT_REF",
            "--operator",
            "codex-a",
            "--output-json",
            str(output),
        ]
    )

    assert exit_code == 0
    payload = json.loads(output.read_text(encoding="utf-8"))
    assert payload["operator"] == "codex-a"
    assert payload["status"] == "pause"
    assert payload["dry_run"] is True
    assert payload["read_only"] is True


def test_install_commands_reference_reviewed_refs_only_as_text():
    manifest = build_release_manifest(
        hermes_memory_ref="phase-2.64b-data-steward-selective-integration-baseline",
        hermes_agent_ref="agent-reviewed-tag",
    )

    commands = "\n".join(manifest["install_commands"])
    assert "git checkout phase-2.64b-data-steward-selective-integration-baseline" in commands
    assert "git checkout agent-reviewed-tag" in commands
    assert "git pull" not in commands
    assert "reset --hard" not in commands
