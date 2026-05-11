from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from app.services.asset_catalog.contracts import AssetViewRecord, SourceView
from app.services.asset_catalog.fake_adapter import FakePlatformAssetCatalogAdapter

PreviewAction = Literal[
    "would_upsert",
    "would_skip",
    "would_deny",
    "would_mark_moved",
    "would_mark_stale",
    "would_mark_missing",
    "would_require_human_review",
]


@dataclass(frozen=True)
class AssetCatalogMirrorPreviewItem:
    asset_uid: str
    source_view: SourceView
    contract_version: str
    source_id: str
    project_id: str | None
    action: PreviewAction
    reason: str
    permission_status: str
    sync_status: str
    checksum_status: str
    citation_status: str
    evidence_kind: str
    content_evidence_available: bool
    last_event_id: int
    writes_db: bool = False
    writes_documents: bool = False
    writes_chunks: bool = False
    writes_opensearch: bool = False
    writes_qdrant: bool = False


@dataclass(frozen=True)
class AssetCatalogMirrorPreviewSummary:
    dry_run: bool
    item_count: int
    denied_count: int
    requires_human_review_count: int
    last_event_id_candidate: int | None
    writes_db: bool = False
    writes_documents: bool = False
    writes_chunks: bool = False
    writes_opensearch: bool = False
    writes_qdrant: bool = False


@dataclass(frozen=True)
class AssetCatalogMirrorPreview:
    items: tuple[AssetCatalogMirrorPreviewItem, ...]
    summary: AssetCatalogMirrorPreviewSummary


class AssetCatalogMirrorPreviewer:
    """Dry-run DB-2 catalog mirror preview over the DB-1 fake View adapter."""

    def __init__(self, adapter: FakePlatformAssetCatalogAdapter) -> None:
        self.adapter = adapter

    def preview(self, *, after_event_id: int | None = None) -> AssetCatalogMirrorPreview:
        records_by_key = self._records_by_source()
        events = self.adapter.list_audit_events(after_event_id=after_event_id).items
        items = tuple(
            self._preview_event(event=event, records_by_key=records_by_key)
            for event in events
        )
        return AssetCatalogMirrorPreview(
            items=items,
            summary=AssetCatalogMirrorPreviewSummary(
                dry_run=True,
                item_count=len(items),
                denied_count=sum(item.action == "would_deny" for item in items),
                requires_human_review_count=sum(
                    item.action == "would_require_human_review" for item in items
                ),
                last_event_id_candidate=max(
                    (item.last_event_id for item in items),
                    default=after_event_id,
                ),
            ),
        )

    def _preview_event(
        self,
        *,
        event: AssetViewRecord,
        records_by_key: dict[tuple[SourceView, str], AssetViewRecord],
    ) -> AssetCatalogMirrorPreviewItem:
        event_payload = event.to_dict()
        source_view = event_payload.get("source_view_ref") or event.source_view
        record = records_by_key.get((source_view, event.source_id))
        if record is None:
            return self._preview_missing_record(event, source_view)

        action, reason = self._action_for_record(record)
        return AssetCatalogMirrorPreviewItem(
            asset_uid=record.asset_uid,
            source_view=record.source_view,
            contract_version=record.contract_version,
            source_id=record.source_id,
            project_id=record.project_id,
            action=action,
            reason=reason,
            permission_status=record.permission_status,
            sync_status=record.sync_status,
            checksum_status=record.checksum_status,
            citation_status=record.citation_status,
            evidence_kind=record.evidence_kind,
            content_evidence_available=record.content_evidence_available,
            last_event_id=int(event_payload["event_id"]),
        )

    def _preview_missing_record(
        self,
        event: AssetViewRecord,
        source_view: SourceView,
    ) -> AssetCatalogMirrorPreviewItem:
        event_payload = event.to_dict()
        return AssetCatalogMirrorPreviewItem(
            asset_uid=event.asset_uid,
            source_view=source_view,
            contract_version=event.contract_version,
            source_id=event.source_id,
            project_id=event.project_id,
            action="would_skip",
            reason="asset_record_not_found",
            permission_status=event.permission_status,
            sync_status="missing",
            checksum_status="not_applicable",
            citation_status="metadata_only",
            evidence_kind="asset_catalog_evidence",
            content_evidence_available=False,
            last_event_id=int(event_payload["event_id"]),
        )

    def _records_by_source(self) -> dict[tuple[SourceView, str], AssetViewRecord]:
        pages = (
            self.adapter.list_project_assets(),
            self.adapter.list_file_assets(),
            self.adapter.list_model_assets(),
        )
        return {
            (record.source_view, record.source_id): record
            for page in pages
            for record in page.items
        }

    def _action_for_record(self, record: AssetViewRecord) -> tuple[PreviewAction, str]:
        if record.permission_status == "denied":
            return "would_deny", record.permission_reason or "permission_denied"
        if record.sync_status == "moved":
            return "would_mark_moved", "asset_moved"
        if record.sync_status == "stale":
            return "would_mark_stale", "asset_stale"
        if record.sync_status == "missing":
            return "would_mark_missing", "asset_missing"
        if record.checksum_status == "missing":
            return "would_require_human_review", "checksum_missing"
        if record.sync_status == "active":
            return "would_upsert", "active_catalog_record"
        return "would_skip", "unsupported_sync_status"
