from __future__ import annotations

import pytest

from app.core.config import Settings
from app.services.asset_catalog import (
    DB4B_READONLY_MAX_SAMPLE_LIMIT,
    AssetCatalogReadonlyConnectorShell,
)

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
    "permission_tags": ["SOURCE_SYSTEM:delivery_platform", "PROJECT:101"],
    "confidentiality_level": "UNKNOWN",
    "last_seen_at": "2026-05-08T10:00:00Z",
    "lifecycle_status": "active",
    "index_eligibility": "catalog_only",
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
    "permission_tags": ["SOURCE_SYSTEM:delivery_platform", "PROJECT:101"],
    "confidentiality_level": "UNKNOWN",
    "last_seen_at": "2026-05-08T10:00:00Z",
    "lifecycle_status": "active",
    "index_eligibility": "catalog_only",
}

MODEL_ROW = {
    "model_id": 9988,
    "file_id": 12345,
    "project_id": 101,
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
    "permission_tags": ["SOURCE_SYSTEM:delivery_platform", "PROJECT:101"],
    "confidentiality_level": "UNKNOWN",
    "last_seen_at": "2026-05-08T10:00:00Z",
    "lifecycle_status": "active",
    "index_eligibility": "catalog_only",
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
    def __init__(self, rows_by_sql: dict[str, list[dict[str, object]]]) -> None:
        self.rows_by_sql = rows_by_sql
        self.description: tuple[tuple[str], ...] = ()
        self.rows: list[tuple[object, ...]] = []

    def execute(self, sql: str) -> None:
        selected_rows = self.rows_by_sql[sql]
        columns = tuple(selected_rows[0]) if selected_rows else ()
        self.description = tuple((column,) for column in columns)
        self.rows = [tuple(row[column] for column in columns) for row in selected_rows]

    def fetchall(self) -> list[tuple[object, ...]]:
        return self.rows


class FakeConnection:
    def __init__(self, rows_by_sql: dict[str, list[dict[str, object]]]) -> None:
        self.rows_by_sql = rows_by_sql
        self.execute_calls: list[str] = []

    def cursor(self) -> FakeCursor:
        parent = self

        class RecordingCursor(FakeCursor):
            def execute(self, sql: str) -> None:
                parent.execute_calls.append(sql)
                super().execute(sql)

        return RecordingCursor(self.rows_by_sql)


def test_readonly_connector_config_defaults_are_disabled_and_structure_only() -> None:
    assert Settings.model_fields["platform_asset_readonly_db_enabled"].default is False
    assert Settings.model_fields["platform_asset_readonly_db_password"].default is None
    assert (
        Settings.model_fields["platform_asset_readonly_db_sample_mode"].default
        == "structure_only"
    )
    assert (
        Settings.model_fields["platform_asset_readonly_db_sample_limit"].default
        == DB4B_READONLY_MAX_SAMPLE_LIMIT
    )


def test_readonly_connector_refuses_to_connect_when_disabled() -> None:
    called = False

    def connection_factory() -> FakeConnection:
        nonlocal called
        called = True
        return FakeConnection({})

    connector = AssetCatalogReadonlyConnectorShell(
        enabled=False,
        connection_factory=connection_factory,
    )

    with pytest.raises(ValueError, match="readonly connector disabled"):
        connector.load_rows_by_view()

    assert called is False


def test_readonly_connector_builds_structure_only_queries_by_default() -> None:
    connector = AssetCatalogReadonlyConnectorShell(
        enabled=True,
        connection_factory=lambda: FakeConnection({}),
    )

    queries = connector.build_view_queries()

    assert queries == {
        "ProjectAssetView": "SELECT * FROM ProjectAssetView WHERE 1 = 0",
        "FileAssetView": "SELECT * FROM FileAssetView WHERE 1 = 0",
        "ModelAssetView": "SELECT * FROM ModelAssetView WHERE 1 = 0",
        "AuditEventView": "SELECT * FROM AuditEventView WHERE 1 = 0",
    }
    assert "core_projects" not in " ".join(queries.values())


def test_readonly_connector_builds_limit_queries_only_when_explicit() -> None:
    connector = AssetCatalogReadonlyConnectorShell(
        enabled=True,
        connection_factory=lambda: FakeConnection({}),
        sample_mode="limit",
        sample_limit=30,
    )

    queries = connector.build_view_queries()

    assert queries["ProjectAssetView"] == "SELECT * FROM ProjectAssetView LIMIT 30"
    assert queries["AuditEventView"] == "SELECT * FROM AuditEventView LIMIT 30"


def test_readonly_connector_rejects_unsafe_sample_limits_and_modes() -> None:
    with pytest.raises(ValueError, match="sample limit"):
        AssetCatalogReadonlyConnectorShell(
            enabled=True,
            connection_factory=lambda: FakeConnection({}),
            sample_mode="limit",
            sample_limit=31,
        )

    with pytest.raises(ValueError, match="sample mode"):
        AssetCatalogReadonlyConnectorShell(
            enabled=True,
            connection_factory=lambda: FakeConnection({}),
            sample_mode="full_scan",
        )


def test_readonly_connector_rejects_unknown_view_queries() -> None:
    connector = AssetCatalogReadonlyConnectorShell(
        enabled=True,
        connection_factory=lambda: FakeConnection({}),
    )

    with pytest.raises(ValueError, match="unsupported source view"):
        connector.build_view_query("core_projects")


def test_readonly_connector_loads_fake_rows_into_preflight_fail_closed() -> None:
    rows_by_sql = {
        "SELECT * FROM ProjectAssetView LIMIT 30": [PROJECT_ROW],
        "SELECT * FROM FileAssetView LIMIT 30": [FILE_ROW],
        "SELECT * FROM ModelAssetView LIMIT 30": [MODEL_ROW],
        "SELECT * FROM AuditEventView LIMIT 30": [AUDIT_ROW],
    }
    connection = FakeConnection(rows_by_sql)
    connector = AssetCatalogReadonlyConnectorShell(
        enabled=True,
        connection_factory=lambda: connection,
        sample_mode="limit",
        sample_limit=30,
    )

    result = connector.run_preflight()

    assert connection.execute_calls == list(rows_by_sql)
    assert result.findings == ()
    assert result.preview.summary.item_count == 4
    assert result.preview.summary.last_event_id_candidate == 56789
    assert {item.permission_status for item in result.preview.items} == {"denied"}
    assert {item.action for item in result.preview.items} == {"would_deny"}
    assert {item.reason for item in result.preview.items} == {
        "missing_permission_contract"
    }
    assert result.writes_db is False
    assert result.writes_documents is False
    assert result.writes_chunks is False
    assert result.writes_opensearch is False
    assert result.writes_qdrant is False
