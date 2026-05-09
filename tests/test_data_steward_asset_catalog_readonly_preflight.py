from __future__ import annotations

from app.core.config import Settings
from app.services.asset_catalog import (
    DB4A_READONLY_CONTRACT_VERSION,
    AssetCatalogReadonlyPreflightValidator,
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
    "storage_path": "/safe/staging/path/model-index.xlsx",
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
    "storage_path": "/safe/staging/path/model.rvt",
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


def _rows_by_view():
    return {
        "ProjectAssetView": [PROJECT_ROW],
        "FileAssetView": [FILE_ROW],
        "ModelAssetView": [MODEL_ROW],
        "AuditEventView": [AUDIT_ROW],
    }


def test_readonly_db_config_defaults_are_safe() -> None:
    assert Settings.model_fields["platform_asset_readonly_db_enabled"].default is False
    assert Settings.model_fields["platform_asset_readonly_db_dsn"].default is None
    assert Settings.model_fields["platform_asset_readonly_db_user"].default is None
    assert (
        Settings.model_fields["platform_asset_readonly_db_contract_version"].default
        == DB4A_READONLY_CONTRACT_VERSION
    )


def test_readonly_preflight_normalizes_rows_to_catalog_preview_fail_closed() -> None:
    result = AssetCatalogReadonlyPreflightValidator().validate(_rows_by_view())

    assert result.source_system == "delivery_platform"
    assert result.source_contract_version == DB4A_READONLY_CONTRACT_VERSION
    assert result.findings == ()
    assert result.connects_real_db is False
    assert result.writes_db is False
    assert result.writes_documents is False
    assert result.writes_chunks is False
    assert result.writes_opensearch is False
    assert result.writes_qdrant is False

    items = {(item.source_view, item.source_id): item for item in result.preview.items}
    file_item = items[("FileAssetView", "12345")]
    assert file_item.asset_uid == "delivery_platform:FileAssetView:12345"
    assert file_item.contract_version == DB4A_READONLY_CONTRACT_VERSION
    assert file_item.project_id == "101"
    assert file_item.permission_status == "denied"
    assert file_item.action == "would_deny"
    assert file_item.reason == "missing_permission_contract"
    assert file_item.citation_status == "metadata_only"
    assert file_item.evidence_kind == "asset_catalog_evidence"
    assert file_item.content_evidence_available is False


def test_readonly_preflight_uses_audit_event_id_as_checkpoint_candidate() -> None:
    result = AssetCatalogReadonlyPreflightValidator().validate(_rows_by_view())

    assert result.preview.summary.last_event_id_candidate == 56789
    assert result.row_counts == {
        "ProjectAssetView": 1,
        "FileAssetView": 1,
        "ModelAssetView": 1,
        "AuditEventView": 1,
    }


def test_readonly_preflight_reports_missing_required_view_field() -> None:
    rows_by_view = _rows_by_view()
    rows_by_view["FileAssetView"] = [
        {key: value for key, value in FILE_ROW.items() if key != "file_id"}
    ]

    result = AssetCatalogReadonlyPreflightValidator().validate(rows_by_view)

    assert result.findings
    assert result.findings[0].source_view == "FileAssetView"
    assert result.findings[0].code == "missing_required_field"
    assert result.findings[0].field == "file_id"
    assert ("FileAssetView", "") not in {
        (item.source_view, item.source_id) for item in result.preview.items
    }


def test_readonly_preflight_reports_unsupported_view_contract_drift() -> None:
    rows_by_view = _rows_by_view()
    rows_by_view["UnexpectedAssetView"] = [{"id": 1}]

    result = AssetCatalogReadonlyPreflightValidator().validate(rows_by_view)

    unsupported = [
        finding
        for finding in result.findings
        if finding.code == "unsupported_source_view"
    ]
    assert len(unsupported) == 1
    assert unsupported[0].source_view == "UnexpectedAssetView"
    assert unsupported[0].severity == "error"
