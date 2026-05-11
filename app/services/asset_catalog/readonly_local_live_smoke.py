from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from collections.abc import Callable, Sequence
from typing import Any

from app.services.asset_catalog.readonly_connector import (
    DB4B_READONLY_MAX_SAMPLE_LIMIT,
    DB4B_READONLY_SAMPLE_MODES,
    AssetCatalogReadonlyConnectorShell,
)
from app.services.asset_catalog.readonly_live_smoke import (
    AssetCatalogReadonlyLiveSmokeResult,
    AssetCatalogReadonlyLiveSmokeRunner,
)

DB4D_FORBIDDEN_TABLES = (
    "core_projects",
    "data_file_resources",
    "core_audit_logs",
)


class DockerMysqlReadonlyQueryError(RuntimeError):
    """Sanitized query failure for local readonly smoke."""


class DockerMysqlReadonlyQueryRunner:
    """Runs local Docker MySQL readonly queries without placing secrets in argv."""

    def __init__(
        self,
        *,
        container: str = "delivery-mysql",
        database: str = "delivery_platform",
        user: str = "hermes_agent_ro",
        host: str = "127.0.0.1",
        port: int = 3306,
        password_env_var: str = "MYSQL_PWD",
        docker_binary: str = "docker",
        command_runner: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run,
    ) -> None:
        self.container = container
        self.database = database
        self.user = user
        self.host = host
        self.port = port
        self.password_env_var = password_env_var
        self.docker_binary = docker_binary
        self.command_runner = command_runner

    def build_command(self, sql: str) -> list[str]:
        return [
            self.docker_binary,
            "exec",
            "--env",
            self.password_env_var,
            self.container,
            "mysql",
            "--batch",
            "--raw",
            "--protocol=tcp",
            "--host",
            self.host,
            "--port",
            str(self.port),
            "--user",
            self.user,
            self.database,
            "--execute",
            sql,
        ]

    def run_query(self, sql: str) -> subprocess.CompletedProcess[str]:
        env = os.environ.copy()
        if not env.get(self.password_env_var):
            raise ValueError("readonly mysql password environment variable is missing")
        return self.command_runner(
            self.build_command(sql),
            capture_output=True,
            text=True,
            check=False,
            env=env,
        )


class DockerMysqlDbApiConnection:
    def __init__(self, query_runner: DockerMysqlReadonlyQueryRunner) -> None:
        self.query_runner = query_runner

    def cursor(self) -> DockerMysqlDbApiCursor:
        return DockerMysqlDbApiCursor(self.query_runner)


class DockerMysqlDbApiCursor:
    def __init__(self, query_runner: DockerMysqlReadonlyQueryRunner) -> None:
        self.query_runner = query_runner
        self.description: tuple[tuple[str], ...] = ()
        self._rows: list[tuple[str, ...]] = []

    def execute(self, sql: str) -> None:
        result = self.query_runner.run_query(sql)
        if result.returncode != 0:
            raise DockerMysqlReadonlyQueryError("readonly mysql query failed")
        columns, rows = _parse_mysql_batch_stdout(result.stdout)
        self.description = tuple((column,) for column in columns)
        self._rows = rows

    def fetchall(self) -> list[tuple[str, ...]]:
        return self._rows

    def close(self) -> None:
        return None


def run_readonly_local_live_smoke(
    *,
    sample_mode: str = "structure_only",
    sample_limit: int = DB4B_READONLY_MAX_SAMPLE_LIMIT,
    allow_real_sample_data: bool = False,
    same_machine_local_dev_authorized: bool = False,
    query_runner: DockerMysqlReadonlyQueryRunner | None = None,
    command_runner: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run,
) -> dict[str, Any]:
    if sample_mode not in DB4B_READONLY_SAMPLE_MODES:
        raise ValueError("unsupported readonly sample mode")

    mysql_runner = query_runner or DockerMysqlReadonlyQueryRunner(
        command_runner=command_runner
    )
    connection = DockerMysqlDbApiConnection(mysql_runner)
    connector = AssetCatalogReadonlyConnectorShell(
        enabled=True,
        connection_factory=lambda: connection,
        sample_mode=sample_mode,
        sample_limit=sample_limit,
    )
    smoke_runner = AssetCatalogReadonlyLiveSmokeRunner(
        enabled=True,
        connector=connector,
        allow_real_sample_data=allow_real_sample_data,
        same_machine_local_dev_authorized=same_machine_local_dev_authorized,
    )
    return sanitize_live_smoke_result(smoke_runner.run())


def verify_forbidden_table_denials(
    query_runner: DockerMysqlReadonlyQueryRunner,
    *,
    forbidden_tables: Sequence[str] = DB4D_FORBIDDEN_TABLES,
) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    for table in forbidden_tables:
        completed = query_runner.run_query(f"SELECT COUNT(*) FROM {table}")
        results.append(
            {
                "table": table,
                "denied": completed.returncode != 0,
                "status": "denied" if completed.returncode != 0 else "readable",
            }
        )
    return results


def sanitize_live_smoke_result(
    result: AssetCatalogReadonlyLiveSmokeResult,
) -> dict[str, Any]:
    preview_summary = result.preflight.preview.summary
    return {
        "sample_mode": result.sample_mode,
        "real_sample_data_used": result.real_sample_data_used,
        "mainline_agent_updated": result.mainline_agent_updated,
        "same_machine_local_dev_authorized": result.same_machine_local_dev_authorized,
        "source_views_checked": sorted(result.column_names_by_view),
        "column_counts_by_view": {
            source_view: len(columns)
            for source_view, columns in sorted(result.column_names_by_view.items())
        },
        "live_smoke_findings": [
            {
                "source_view": finding.source_view,
                "code": finding.code,
                "field": finding.field,
                "severity": finding.severity,
            }
            for finding in result.findings
        ],
        "preflight": {
            "row_counts": dict(sorted(result.preflight.row_counts.items())),
            "finding_count": len(result.preflight.findings),
            "finding_codes": sorted(
                {
                    finding.code
                    for finding in result.preflight.findings
                }
            ),
            "item_count": preview_summary.item_count,
            "denied_count": preview_summary.denied_count,
            "requires_human_review_count": preview_summary.requires_human_review_count,
            "last_event_id_candidate_present": (
                preview_summary.last_event_id_candidate is not None
            ),
        },
        "writes": {
            "db": result.writes_db,
            "documents": result.writes_documents,
            "chunks": result.writes_chunks,
            "opensearch": result.writes_opensearch,
            "qdrant": result.writes_qdrant,
        },
    }


def _parse_mysql_batch_stdout(stdout: str) -> tuple[tuple[str, ...], list[tuple[str, ...]]]:
    lines = stdout.splitlines()
    if not lines:
        return (), []
    columns = tuple(lines[0].split("\t"))
    rows = [tuple(line.split("\t")) for line in lines[1:]]
    for row in rows:
        if len(row) != len(columns):
            raise ValueError("mysql result shape does not match column header")
    return columns, rows


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Run sanitized DB-4D readonly local live smoke."
    )
    parser.add_argument(
        "--sample-mode",
        choices=DB4B_READONLY_SAMPLE_MODES,
        default="structure_only",
    )
    parser.add_argument(
        "--sample-limit",
        type=int,
        default=DB4B_READONLY_MAX_SAMPLE_LIMIT,
    )
    parser.add_argument("--allow-real-sample-data", action="store_true")
    parser.add_argument("--same-machine-local-dev-authorized", action="store_true")
    parser.add_argument("--forbidden-table-probe", action="store_true")
    args = parser.parse_args(argv)

    try:
        report = run_readonly_local_live_smoke(
            sample_mode=args.sample_mode,
            sample_limit=args.sample_limit,
            allow_real_sample_data=args.allow_real_sample_data,
            same_machine_local_dev_authorized=args.same_machine_local_dev_authorized,
        )
        if args.forbidden_table_probe:
            report["forbidden_table_denials"] = verify_forbidden_table_denials(
                DockerMysqlReadonlyQueryRunner()
            )
    except Exception as exc:
        error_report = {
            "ok": False,
            "error_type": type(exc).__name__,
            "message": "readonly local live smoke failed",
        }
        print(json.dumps(error_report, ensure_ascii=False, sort_keys=True), file=sys.stderr)
        return 1

    print(json.dumps(report, ensure_ascii=False, sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
