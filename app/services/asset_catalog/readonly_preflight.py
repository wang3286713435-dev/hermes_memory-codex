from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import Any

from app.services.asset_catalog.contracts import DEFAULT_SOURCE_SYSTEM, SOURCE_VIEWS, SourceView
from app.services.asset_catalog.mirror_preview import (
    AssetCatalogMirrorPreview,
    AssetCatalogMirrorPreviewItem,
    AssetCatalogMirrorPreviewSummary,
)

DB4A_READONLY_CONTRACT_VERSION = "delivery_platform.asset_views.v1"

DB4A_REQUIRED_VIEW_FIELDS: dict[SourceView, tuple[str, ...]] = {
    "ProjectAssetView": (
        "project_id",
        "project_code",
        "project_name",
        "project_stage",
        "discipline_scope",
        "manager_name",
        "owner_org_name",
        "asset_status",
        "model_file_count",
        "total_size_bytes",
        "last_asset_updated_at",
    ),
    "FileAssetView": (
        "file_id",
        "project_id",
        "project_code",
        "project_name",
        "file_name",
        "file_ext",
        "file_kind",
        "discipline",
        "version_no",
        "size_bytes",
        "checksum",
        "storage_provider",
        "storage_path",
        "logical_path",
        "source_type",
        "process_status",
        "created_at",
        "updated_at",
    ),
    "ModelAssetView": (
        "model_id",
        "file_id",
        "project_code",
        "model_name",
        "model_format",
        "discipline",
        "version_no",
        "preview_available",
        "lightweight_status",
        "component_index_status",
        "storage_path",
        "updated_at",
    ),
    "AuditEventView": (
        "event_id",
        "project_id",
        "module_code",
        "action_code",
        "target_type",
        "target_id",
        "operator_id",
        "summary",
        "created_at",
    ),
}

DB4A_SOURCE_ID_FIELDS: dict[SourceView, str] = {
    "ProjectAssetView": "project_id",
    "FileAssetView": "file_id",
    "ModelAssetView": "model_id",
    "AuditEventView": "event_id",
}


@dataclass(frozen=True)
class AssetCatalogReadonlyPreflightFinding:
    source_view: str
    code: str
    message: str
    field: str | None = None
    severity: str = "error"


@dataclass(frozen=True)
class AssetCatalogReadonlyPreflightResult:
    source_system: str
    source_contract_version: str
    row_counts: dict[str, int]
    findings: tuple[AssetCatalogReadonlyPreflightFinding, ...]
    preview: AssetCatalogMirrorPreview
    connects_real_db: bool = False
    writes_db: bool = False
    writes_documents: bool = False
    writes_chunks: bool = False
    writes_opensearch: bool = False
    writes_qdrant: bool = False


class AssetCatalogReadonlyPreflightValidator:
    """Validates DB-4A read-only View rows without opening a database connection."""

    def __init__(
        self,
        *,
        source_system: str = DEFAULT_SOURCE_SYSTEM,
        source_contract_version: str = DB4A_READONLY_CONTRACT_VERSION,
    ) -> None:
        self.source_system = source_system
        self.source_contract_version = source_contract_version

    def validate(
        self,
        rows_by_view: Mapping[str, Sequence[Mapping[str, Any]]],
    ) -> AssetCatalogReadonlyPreflightResult:
        findings: list[AssetCatalogReadonlyPreflightFinding] = []
        items: list[AssetCatalogMirrorPreviewItem] = []
        row_counts: dict[str, int] = {}

        supported_views = set(SOURCE_VIEWS)
        for source_view in rows_by_view:
            if source_view not in supported_views:
                findings.append(
                    AssetCatalogReadonlyPreflightFinding(
                        source_view=source_view,
                        code="unsupported_source_view",
                        message=f"{source_view} is not part of the DB-4A contract",
                    )
                )

        for source_view in SOURCE_VIEWS:
            rows = tuple(rows_by_view.get(source_view, ()))
            row_counts[source_view] = len(rows)
            for row in rows:
                missing_fields = self._missing_required_fields(source_view, row)
                if missing_fields:
                    findings.extend(
                        self._missing_field_finding(source_view, field)
                        for field in missing_fields
                    )
                    continue
                items.append(self._preview_item(source_view, row))

        preview = AssetCatalogMirrorPreview(
            items=tuple(items),
            summary=AssetCatalogMirrorPreviewSummary(
                dry_run=True,
                item_count=len(items),
                denied_count=sum(item.action == "would_deny" for item in items),
                requires_human_review_count=0,
                last_event_id_candidate=max(
                    (
                        item.last_event_id
                        for item in items
                        if item.source_view == "AuditEventView"
                    ),
                    default=None,
                ),
            ),
        )
        return AssetCatalogReadonlyPreflightResult(
            source_system=self.source_system,
            source_contract_version=self.source_contract_version,
            row_counts=row_counts,
            findings=tuple(findings),
            preview=preview,
        )

    def _missing_required_fields(
        self,
        source_view: SourceView,
        row: Mapping[str, Any],
    ) -> tuple[str, ...]:
        return tuple(
            field
            for field in DB4A_REQUIRED_VIEW_FIELDS[source_view]
            if field not in row
        )

    def _missing_field_finding(
        self,
        source_view: SourceView,
        field: str,
    ) -> AssetCatalogReadonlyPreflightFinding:
        return AssetCatalogReadonlyPreflightFinding(
            source_view=source_view,
            code="missing_required_field",
            field=field,
            message=f"{source_view} is missing required field {field}",
        )

    def _preview_item(
        self,
        source_view: SourceView,
        row: Mapping[str, Any],
    ) -> AssetCatalogMirrorPreviewItem:
        source_id = str(row[DB4A_SOURCE_ID_FIELDS[source_view]])
        project_id = row.get("project_id")
        last_event_id = int(row["event_id"]) if source_view == "AuditEventView" else 0
        return AssetCatalogMirrorPreviewItem(
            asset_uid=f"{self.source_system}:{source_view}:{source_id}",
            source_view=source_view,
            contract_version=self.source_contract_version,
            source_id=source_id,
            project_id=str(project_id) if project_id is not None else None,
            action="would_deny",
            reason="missing_permission_contract",
            permission_status="denied",
            sync_status="active",
            checksum_status=self._checksum_status(source_view, row),
            citation_status="metadata_only",
            evidence_kind="asset_catalog_evidence",
            content_evidence_available=False,
            last_event_id=last_event_id,
        )

    def _checksum_status(
        self,
        source_view: SourceView,
        row: Mapping[str, Any],
    ) -> str:
        if source_view == "FileAssetView":
            return "present" if row.get("checksum") else "missing"
        return "not_applicable"
