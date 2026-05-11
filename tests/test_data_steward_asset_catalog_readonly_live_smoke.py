from __future__ import annotations

import pytest

from app.core.config import Settings
from app.services.asset_catalog import (
    AssetCatalogReadonlyConnectorShell,
    AssetCatalogReadonlyLiveSmokeRunner,
)
from app.services.asset_catalog.readonly_preflight import DB4A_REQUIRED_VIEW_FIELDS

PROJECT_ROW = {
    "project_id": 101,
    "project_code": "P-101",
    "project_name": "C Tower",
    "project_stage": "delivery",
    "discipline_scope": "bim",
    "manager_name": "manager-a",
    "owner_org_name": "owner-org",
    "asset_status": "active",
    "model_file_count": 2,
    "total_size_bytes": 4096,
    "last_asset_updated_at": "2026-05-01T00:00:00Z",
}

FILE_ROW = {
    "file_id": 12345,
    "project_id": 101,
    "project_code": "P-101",
    "project_name": "C Tower",
    "file_name": "model-index.xlsx",
    "file_ext": "xlsx",
    "file_kind": "model_index",
    "discipline": "bim",
    "version_no": "v3",
    "size_bytes": 2048,
    "checksum": "sha256:abc",
    "storage_provider": "nas",
    "storage_path": "/safe/dev/path/model-index.xlsx",
    "logical_path": "P-101/model-index.xlsx",
    "source_type": "platform",
    "process_status": "ready",
    "created_at": "2026-05-01T00:00:00Z",
    "updated_at": "2026-05-02T00:00:00Z",
}

MODEL_ROW = {
    "model_id": 9988,
    "file_id": 12345,
    "project_code": "P-101",
    "model_name": "C Tower BIM",
    "model_format": "rvt",
    "discipline": "bim",
    "version_no": "v3",
    "preview_available": True,
    "lightweight_status": "ready",
    "component_index_status": "not_requested",
    "storage_path": "/safe/dev/path/model.rvt",
    "updated_at": "2026-05-03T00:00:00Z",
}

AUDIT_ROW = {
    "event_id": 56789,
    "project_id": 101,
    "module_code": "asset",
    "action_code": "file.updated",
    "target_type": "file",
    "target_id": 12345,
    "operator_id": "operator-a",
    "summary": "file updated",
    "created_at": "2026-05-04T00:00:00Z",
}


class FakeCursor:
    def __init__(
        self,
        *,
        columns_by_sql: dict[str, tuple[str, ...]],
        rows_by_sql: dict[str, list[dict[str, object]]],
    ) -> None:
        self.columns_by_sql = columns_by_sql
        self.rows_by_sql = rows_by_sql
        self.description: tuple[tuple[str], ...] = ()
        self.rows: list[tuple[object, ...]] = []

    def execute(self, sql: str) -> None:
        columns = self.columns_by_sql[sql]
        self.description = tuple((column,) for column in columns)
        self.rows = [
            tuple(row[column] for column in columns)
            for row in self.rows_by_sql.get(sql, [])
        ]

    def fetchall(self) -> list[tuple[object, ...]]:
        return self.rows


class FakeConnection:
    def __init__(
        self,
        *,
        columns_by_sql: dict[str, tuple[str, ...]],
        rows_by_sql: dict[str, list[dict[str, object]]] | None = None,
    ) -> None:
        self.columns_by_sql = columns_by_sql
        self.rows_by_sql = rows_by_sql or {}
        self.execute_calls: list[str] = []

    def cursor(self) -> FakeCursor:
        parent = self

        class RecordingCursor(FakeCursor):
            def execute(self, sql: str) -> None:
                parent.execute_calls.append(sql)
                super().execute(sql)

        return RecordingCursor(
            columns_by_sql=self.columns_by_sql,
            rows_by_sql=self.rows_by_sql,
        )


def _structure_queries() -> dict[str, str]:
    return {
        source_view: f"SELECT * FROM {source_view} WHERE 1 = 0"
        for source_view in DB4A_REQUIRED_VIEW_FIELDS
    }


def _limit_queries() -> dict[str, str]:
    return {
        source_view: f"SELECT * FROM {source_view} LIMIT 30"
        for source_view in DB4A_REQUIRED_VIEW_FIELDS
    }


def _columns_by_sql(*, sample_mode: str) -> dict[str, tuple[str, ...]]:
    queries = _structure_queries() if sample_mode == "structure_only" else _limit_queries()
    return {
        sql: DB4A_REQUIRED_VIEW_FIELDS[source_view]
        for source_view, sql in queries.items()
    }


def _rows_by_sql() -> dict[str, list[dict[str, object]]]:
    queries = _limit_queries()
    return {
        queries["ProjectAssetView"]: [PROJECT_ROW],
        queries["FileAssetView"]: [FILE_ROW],
        queries["ModelAssetView"]: [MODEL_ROW],
        queries["AuditEventView"]: [AUDIT_ROW],
    }


def test_live_smoke_config_defaults_are_safe() -> None:
    assert Settings.model_fields["platform_asset_readonly_live_smoke_enabled"].default is False
    assert (
        Settings.model_fields["platform_asset_readonly_mainline_agent_updated"].default
        is False
    )
    assert (
        Settings.model_fields["platform_asset_readonly_allow_real_sample_data"].default
        is False
    )


def test_disabled_live_smoke_does_not_call_connection_factory() -> None:
    called = False

    def connection_factory() -> FakeConnection:
        nonlocal called
        called = True
        return FakeConnection(columns_by_sql={})

    connector = AssetCatalogReadonlyConnectorShell(
        enabled=True,
        connection_factory=connection_factory,
    )
    runner = AssetCatalogReadonlyLiveSmokeRunner(enabled=False, connector=connector)

    with pytest.raises(ValueError, match="live smoke disabled"):
        runner.run()

    assert called is False


def test_structure_only_live_smoke_validates_columns_without_real_rows() -> None:
    connection = FakeConnection(columns_by_sql=_columns_by_sql(sample_mode="structure_only"))
    connector = AssetCatalogReadonlyConnectorShell(
        enabled=True,
        connection_factory=lambda: connection,
    )
    runner = AssetCatalogReadonlyLiveSmokeRunner(enabled=True, connector=connector)

    result = runner.run()

    assert result.sample_mode == "structure_only"
    assert result.real_sample_data_used is False
    assert result.findings == ()
    assert result.preflight.preview.summary.item_count == 0
    assert all("WHERE 1 = 0" in sql for sql in connection.execute_calls)
    assert "LIMIT 30" not in " ".join(connection.execute_calls)
    assert result.writes_documents is False
    assert result.writes_chunks is False
    assert result.writes_opensearch is False
    assert result.writes_qdrant is False


def test_live_smoke_reports_missing_required_column() -> None:
    columns_by_sql = _columns_by_sql(sample_mode="structure_only")
    file_sql = _structure_queries()["FileAssetView"]
    columns_by_sql[file_sql] = tuple(
        column for column in columns_by_sql[file_sql] if column != "file_id"
    )
    connector = AssetCatalogReadonlyConnectorShell(
        enabled=True,
        connection_factory=lambda: FakeConnection(columns_by_sql=columns_by_sql),
    )
    runner = AssetCatalogReadonlyLiveSmokeRunner(enabled=True, connector=connector)

    result = runner.run()

    assert len(result.findings) == 1
    assert result.findings[0].source_view == "FileAssetView"
    assert result.findings[0].code == "missing_required_column"
    assert result.findings[0].field == "file_id"


def test_limit_mode_requires_mainline_agent_update_and_real_data_authorization() -> None:
    connector = AssetCatalogReadonlyConnectorShell(
        enabled=True,
        connection_factory=lambda: FakeConnection(
            columns_by_sql=_columns_by_sql(sample_mode="limit"),
            rows_by_sql=_rows_by_sql(),
        ),
        sample_mode="limit",
    )
    runner = AssetCatalogReadonlyLiveSmokeRunner(enabled=True, connector=connector)

    with pytest.raises(ValueError, match="mainline enterprise agent update"):
        runner.run()


def test_limit_mode_runs_only_after_mainline_update_and_real_data_authorization() -> None:
    connector = AssetCatalogReadonlyConnectorShell(
        enabled=True,
        connection_factory=lambda: FakeConnection(
            columns_by_sql=_columns_by_sql(sample_mode="limit"),
            rows_by_sql=_rows_by_sql(),
        ),
        sample_mode="limit",
    )
    runner = AssetCatalogReadonlyLiveSmokeRunner(
        enabled=True,
        connector=connector,
        mainline_agent_updated=True,
        allow_real_sample_data=True,
    )

    result = runner.run()

    assert result.sample_mode == "limit"
    assert result.real_sample_data_used is True
    assert result.preflight.preview.summary.item_count == 4
    assert {item.permission_status for item in result.preflight.preview.items} == {"denied"}
    assert result.preflight.preview.summary.last_event_id_candidate == 56789
