from __future__ import annotations

import importlib.util
import json
from pathlib import Path

MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "phase260_mvp_local_readiness_pack.py"
SPEC = importlib.util.spec_from_file_location("phase260_mvp_local_readiness_pack", MODULE_PATH)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)

build_readiness_report = MODULE.build_readiness_report
main = MODULE.main


def _write_required_workspace_files(root: Path) -> None:
    (root / "docs").mkdir()
    (root / "scripts").mkdir()
    (root / "reports" / "agent_runs").mkdir(parents=True)
    (root / "docs" / "MAC_MINI_NATURAL_IMPORT_OPERATOR_CHECKLIST.md").write_text("checklist", encoding="utf-8")
    (root / "docs" / "NEXT_CODEX_C_PROMPT.md").write_text("prompt", encoding="utf-8")
    (root / "docs" / "PHASE259_NATURAL_IMPORT_SECOND_SMOKE_PLAN.md").write_text("plan", encoding="utf-8")
    (root / "scripts" / "run_local_api.sh").write_text("#!/usr/bin/env bash\n", encoding="utf-8")
    (root / "reports" / "agent_runs" / "latest.json").write_text(
        json.dumps({"phase": "test", "status": "baseline"}),
        encoding="utf-8",
    )


def _fake_git_runner(*_args, **_kwargs):
    return "abc123" if "rev-parse" in _args[0] else "phase-test-tag"


def test_skip_api_health_with_required_files_is_go(tmp_path):
    _write_required_workspace_files(tmp_path)

    report = build_readiness_report(
        workspace_root=tmp_path,
        api_url="http://127.0.0.1:8000",
        skip_api_health=True,
        env={},
        git_runner=_fake_git_runner,
    )

    assert report["status"] == "go"
    assert report["dry_run"] is True
    assert report["read_only"] is True
    assert report["destructive_actions"] == []
    assert report["real_upload_called"] is False
    assert report["api_smoke_called"] is False
    assert report["cli_smoke_called"] is False
    assert report["db_or_index_written"] is False
    assert report["production_rollout"] is False


def test_missing_latest_json_is_pause(tmp_path):
    _write_required_workspace_files(tmp_path)
    (tmp_path / "reports" / "agent_runs" / "latest.json").unlink()

    report = build_readiness_report(
        workspace_root=tmp_path,
        api_url="http://127.0.0.1:8000",
        skip_api_health=True,
        env={},
        git_runner=_fake_git_runner,
    )

    assert report["status"] == "pause"
    check = next(check for check in report["checks"] if check["id"] == "latest_json_present")
    assert check["status"] == "pause"


def test_dangerous_env_flag_true_is_no_go(tmp_path):
    _write_required_workspace_files(tmp_path)

    report = build_readiness_report(
        workspace_root=tmp_path,
        api_url="http://127.0.0.1:8000",
        skip_api_health=True,
        env={"HERMES_REPAIR_AUTHORIZED": "true"},
        git_runner=_fake_git_runner,
    )

    assert report["status"] == "no_go"
    check = next(check for check in report["checks"] if check["id"] == "dangerous_env_flags_absent")
    assert check["status"] == "no_go"
    assert check["details"]["dangerous_flags"] == ["HERMES_REPAIR_AUTHORIZED"]


def test_api_health_failure_without_skip_is_pause(tmp_path):
    _write_required_workspace_files(tmp_path)

    def failing_health(_url: str) -> tuple[bool, str]:
        return False, "connection refused"

    report = build_readiness_report(
        workspace_root=tmp_path,
        api_url="http://127.0.0.1:8000",
        skip_api_health=False,
        env={},
        git_runner=_fake_git_runner,
        health_checker=failing_health,
    )

    assert report["status"] == "pause"
    check = next(check for check in report["checks"] if check["id"] == "api_health_optional")
    assert check["status"] == "pause"
    assert "connection refused" in check["message"]


def test_output_json_writes_to_explicit_path_and_remains_dry_run(tmp_path):
    _write_required_workspace_files(tmp_path)
    output = tmp_path / "out" / "readiness.json"

    exit_code = main(
        [
            "--workspace-root",
            str(tmp_path),
            "--skip-api-health",
            "--output-json",
            str(output),
        ],
        env={},
        git_runner=_fake_git_runner,
    )

    assert exit_code == 0
    payload = json.loads(output.read_text(encoding="utf-8"))
    assert payload["status"] == "go"
    assert payload["dry_run"] is True
    assert payload["read_only"] is True
    assert payload["destructive_actions"] == []


def test_fixed_safety_fields_are_never_mutating(tmp_path):
    _write_required_workspace_files(tmp_path)

    report = build_readiness_report(
        workspace_root=tmp_path,
        api_url="http://127.0.0.1:8000",
        skip_api_health=True,
        env={},
        git_runner=_fake_git_runner,
    )

    assert report["dry_run"] is True
    assert report["read_only"] is True
    assert report["destructive_actions"] == []
    assert report["real_upload_called"] is False
    assert report["api_smoke_called"] is False
    assert report["cli_smoke_called"] is False
    assert report["db_or_index_written"] is False
    assert report["production_rollout"] is False
