from __future__ import annotations

import json
import subprocess
from collections.abc import Mapping, Sequence

import pytest

from app.services.asset_catalog import (
    AssetCatalogReadonlyConnectorShell,
    AssetCatalogReadonlyLiveSmokeRunner,
    readonly_local_live_smoke,
)
from app.services.asset_catalog.readonly_local_live_smoke import (
    DockerMysqlReadonlyQueryRunner,
    run_readonly_local_live_smoke,
    verify_forbidden_table_denials,
)
from app.services.asset_catalog.readonly_preflight import DB4A_REQUIRED_VIEW_FIELDS

SENSITIVE_PROJECT_NAME = "Real Project Name"
SENSITIVE_FILE_NAME = "real-model-file.rvt"
SENSITIVE_NAS_PATH = "/Volumes/internal-nas/real-model-file.rvt"


def _rows_by_view() -> dict[str, list[dict[str, object]]]:
    return {
        "ProjectAssetView": [
            {
                "project_id": 101,
                "project_code": "P-101",
                "project_name": SENSITIVE_PROJECT_NAME,
                "project_stage": "delivery",
                "discipline_scope": "bim",
                "manager_name": "manager-a",
                "owner_org_name": "owner-org",
                "asset_status": "active",
                "model_file_count": 2,
                "total_size_bytes": 4096,
                "last_asset_updated_at": "2026-05-01T00:00:00Z",
            }
        ],
        "FileAssetView": [
            {
                "file_id": 12345,
                "project_id": 101,
                "project_code": "P-101",
                "project_name": SENSITIVE_PROJECT_NAME,
                "file_name": SENSITIVE_FILE_NAME,
                "file_ext": "rvt",
                "file_kind": "model",
                "discipline": "bim",
                "version_no": "v3",
                "size_bytes": 2048,
                "checksum": "sha256:abc",
                "storage_provider": "nas",
                "storage_path": SENSITIVE_NAS_PATH,
                "logical_path": f"P-101/{SENSITIVE_FILE_NAME}",
                "source_type": "platform",
                "process_status": "ready",
                "created_at": "2026-05-01T00:00:00Z",
                "updated_at": "2026-05-02T00:00:00Z",
            }
        ],
        "ModelAssetView": [
            {
                "model_id": 9988,
                "file_id": 12345,
                "project_code": "P-101",
                "model_name": SENSITIVE_FILE_NAME,
                "model_format": "rvt",
                "discipline": "bim",
                "version_no": "v3",
                "preview_available": True,
                "lightweight_status": "ready",
                "component_index_status": "not_requested",
                "storage_path": SENSITIVE_NAS_PATH,
                "updated_at": "2026-05-03T00:00:00Z",
            }
        ],
        "AuditEventView": [
            {
                "event_id": 56789,
                "project_id": 101,
                "module_code": "asset",
                "action_code": "file.updated",
                "target_type": "file",
                "target_id": 12345,
                "operator_id": "operator-a",
                "summary": f"{SENSITIVE_FILE_NAME} updated",
                "created_at": "2026-05-04T00:00:00Z",
            }
        ],
    }


class FakeCursor:
    def __init__(self, rows_by_view: Mapping[str, Sequence[Mapping[str, object]]]) -> None:
        self.rows_by_view = rows_by_view
        self.description: tuple[tuple[str], ...] = ()
        self.rows: list[tuple[object, ...]] = []

    def execute(self, sql: str) -> None:
        source_view = sql.split(" FROM ", maxsplit=1)[1].split(" ", maxsplit=1)[0]
        columns = DB4A_REQUIRED_VIEW_FIELDS[source_view]
        self.description = tuple((column,) for column in columns)
        self.rows = [
            tuple(row[column] for column in columns)
            for row in self.rows_by_view.get(source_view, [])
        ]

    def fetchall(self) -> list[tuple[object, ...]]:
        return self.rows


class FakeConnection:
    def cursor(self) -> FakeCursor:
        return FakeCursor(_rows_by_view())


def test_limit_mode_allows_same_machine_local_dev_authorization() -> None:
    connector = AssetCatalogReadonlyConnectorShell(
        enabled=True,
        connection_factory=FakeConnection,
        sample_mode="limit",
    )
    runner = AssetCatalogReadonlyLiveSmokeRunner(
        enabled=True,
        connector=connector,
        allow_real_sample_data=True,
        same_machine_local_dev_authorized=True,
    )

    result = runner.run()

    assert result.real_sample_data_used is True
    assert result.mainline_agent_updated is False
    assert result.same_machine_local_dev_authorized is True
    assert result.preflight.preview.summary.item_count == 4


def test_docker_mysql_command_uses_env_password_without_command_argument(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("MYSQL_PWD", "secret-password")
    calls: list[tuple[list[str], dict[str, str]]] = []

    def command_runner(
        command: list[str],
        *,
        capture_output: bool,
        text: bool,
        check: bool,
        env: dict[str, str],
    ) -> subprocess.CompletedProcess[str]:
        calls.append((command, env))
        return subprocess.CompletedProcess(command, 0, stdout="one\n1\n", stderr="")

    runner = DockerMysqlReadonlyQueryRunner(command_runner=command_runner)

    result = runner.run_query("SELECT 1")

    assert result.returncode == 0
    command, env = calls[0]
    assert "secret-password" not in command
    assert "--password" not in " ".join(command)
    assert "--env" in command
    assert "MYSQL_PWD" in command
    assert env["MYSQL_PWD"] == "secret-password"


def test_local_live_smoke_outputs_only_sanitized_summary(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("MYSQL_PWD", "secret-password")

    def command_runner(
        command: list[str],
        *,
        capture_output: bool,
        text: bool,
        check: bool,
        env: dict[str, str],
    ) -> subprocess.CompletedProcess[str]:
        sql = command[-1]
        source_view = sql.split(" FROM ", maxsplit=1)[1].split(" ", maxsplit=1)[0]
        columns = DB4A_REQUIRED_VIEW_FIELDS[source_view]
        rows = _rows_by_view()[source_view]
        stdout_lines = ["\t".join(columns)]
        stdout_lines.extend(
            "\t".join(str(row[column]) for column in columns)
            for row in rows
        )
        return subprocess.CompletedProcess(
            command,
            0,
            stdout="\n".join(stdout_lines) + "\n",
            stderr="",
        )

    report = run_readonly_local_live_smoke(
        sample_mode="limit",
        allow_real_sample_data=True,
        same_machine_local_dev_authorized=True,
        command_runner=command_runner,
    )
    payload = json.dumps(report, sort_keys=True)

    assert report["sample_mode"] == "limit"
    assert report["real_sample_data_used"] is True
    assert report["preflight"]["item_count"] == 4
    assert report["preflight"]["denied_count"] == 4
    assert report["preflight"]["last_event_id_candidate_present"] is True
    assert "items" not in report["preflight"]
    assert "asset_uid" not in payload
    assert "source_id" not in payload
    assert SENSITIVE_PROJECT_NAME not in payload
    assert SENSITIVE_FILE_NAME not in payload
    assert SENSITIVE_NAS_PATH not in payload
    assert "secret-password" not in payload


def test_forbidden_table_denials_are_reported_without_raw_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("MYSQL_PWD", "secret-password")

    def command_runner(
        command: list[str],
        *,
        capture_output: bool,
        text: bool,
        check: bool,
        env: dict[str, str],
    ) -> subprocess.CompletedProcess[str]:
        return subprocess.CompletedProcess(
            command,
            1,
            stdout="",
            stderr=f"SELECT command denied near {SENSITIVE_NAS_PATH}",
        )

    runner = DockerMysqlReadonlyQueryRunner(command_runner=command_runner)

    report = verify_forbidden_table_denials(runner)
    payload = json.dumps(report, sort_keys=True)

    assert {item["table"] for item in report} == {
        "core_projects",
        "data_file_resources",
        "core_audit_logs",
    }
    assert {item["denied"] for item in report} == {True}
    assert SENSITIVE_NAS_PATH not in payload
    assert "stderr" not in payload


def test_cli_main_prints_sanitized_json(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    def fake_run_readonly_local_live_smoke(**kwargs: object) -> dict[str, object]:
        assert kwargs["sample_mode"] == "limit"
        assert kwargs["allow_real_sample_data"] is True
        assert kwargs["same_machine_local_dev_authorized"] is True
        return {
            "sample_mode": "limit",
            "real_sample_data_used": True,
            "preflight": {"item_count": 4},
        }

    monkeypatch.setattr(
        readonly_local_live_smoke,
        "run_readonly_local_live_smoke",
        fake_run_readonly_local_live_smoke,
    )

    exit_code = readonly_local_live_smoke.main(
        [
            "--sample-mode",
            "limit",
            "--allow-real-sample-data",
            "--same-machine-local-dev-authorized",
        ]
    )

    assert exit_code == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["sample_mode"] == "limit"
    assert "asset_uid" not in json.dumps(payload, sort_keys=True)
