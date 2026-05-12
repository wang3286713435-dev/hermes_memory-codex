from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from app.services.asset_catalog.contracts import SourceView
from app.services.asset_catalog.mirror_preview import (
    AssetCatalogMirrorPreview,
    AssetCatalogMirrorPreviewItem,
)

AssetCatalogRetrievalIntent = Literal["catalog_lookup", "content_answer"]


@dataclass(frozen=True)
class AssetCatalogRetrievalRequest:
    query: str
    intent: AssetCatalogRetrievalIntent
    allowed_project_ids: tuple[str, ...] = ()


@dataclass(frozen=True)
class AssetCatalogMetadataItem:
    asset_uid: str
    source_view: SourceView
    source_id: str
    project_id: str
    evidence_kind: str
    citation_status: str
    content_evidence_available: bool
    permission_tags: tuple[str, ...] = ()
    confidentiality_level: str = "UNKNOWN"
    last_seen_at: str | None = None
    lifecycle_status: str = "unknown"
    index_eligibility: str = "catalog_only"


@dataclass(frozen=True)
class AssetCatalogRetrievalDecision:
    intent: AssetCatalogRetrievalIntent
    catalog_items: tuple[AssetCatalogMetadataItem, ...]
    prompt_items: tuple[AssetCatalogMetadataItem, ...]
    missing_evidence: bool
    missing_evidence_reason: str | None
    denied_count: int
    skipped_count: int
    writes_documents: bool = False
    writes_chunks: bool = False
    writes_opensearch: bool = False
    writes_qdrant: bool = False


class AssetCatalogRetrievalGuard:
    """DB-3A guard that keeps catalog metadata separate from answer evidence."""

    def evaluate(
        self,
        preview: AssetCatalogMirrorPreview,
        request: AssetCatalogRetrievalRequest,
    ) -> AssetCatalogRetrievalDecision:
        allowed_projects = set(request.allowed_project_ids)
        if not allowed_projects:
            return AssetCatalogRetrievalDecision(
                intent=request.intent,
                catalog_items=(),
                prompt_items=(),
                missing_evidence=True,
                missing_evidence_reason="permission_scope_required",
                denied_count=0,
                skipped_count=len(preview.items),
            )

        visible_items: list[AssetCatalogMetadataItem] = []
        denied_count = 0
        skipped_count = 0
        for item in preview.items:
            if item.project_id not in allowed_projects:
                skipped_count += 1
                continue
            if item.permission_status == "denied":
                denied_count += 1
                continue
            if not self._is_catalog_visible(item, allowed_projects):
                skipped_count += 1
                continue
            visible_items.append(self._metadata_item(item))

        if request.intent == "content_answer":
            return AssetCatalogRetrievalDecision(
                intent=request.intent,
                catalog_items=(),
                prompt_items=(),
                missing_evidence=True,
                missing_evidence_reason=(
                    "asset_catalog_only" if visible_items else "no_authorized_catalog_metadata"
                ),
                denied_count=denied_count,
                skipped_count=skipped_count,
            )

        return AssetCatalogRetrievalDecision(
            intent=request.intent,
            catalog_items=tuple(visible_items),
            prompt_items=(),
            missing_evidence=False,
            missing_evidence_reason=None,
            denied_count=denied_count,
            skipped_count=skipped_count,
        )

    def _is_catalog_visible(
        self,
        item: AssetCatalogMirrorPreviewItem,
        allowed_projects: set[str],
    ) -> bool:
        return (
            item.action == "would_upsert"
            and item.project_id in allowed_projects
            and item.permission_status == "allowed"
            and item.evidence_kind == "asset_catalog_evidence"
            and item.citation_status == "metadata_only"
            and item.content_evidence_available is False
        )

    def _metadata_item(
        self,
        item: AssetCatalogMirrorPreviewItem,
    ) -> AssetCatalogMetadataItem:
        if item.project_id is None:
            raise ValueError("catalog metadata item requires project_id")
        return AssetCatalogMetadataItem(
            asset_uid=item.asset_uid,
            source_view=item.source_view,
            source_id=item.source_id,
            project_id=item.project_id,
            evidence_kind=item.evidence_kind,
            citation_status=item.citation_status,
            content_evidence_available=item.content_evidence_available,
            permission_tags=item.permission_tags,
            confidentiality_level=item.confidentiality_level,
            last_seen_at=item.last_seen_at,
            lifecycle_status=item.lifecycle_status,
            index_eligibility=item.index_eligibility,
        )
