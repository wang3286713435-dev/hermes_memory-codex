from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal

from app.services.asset_catalog.mirror_preview import AssetCatalogMirrorPreview
from app.services.asset_catalog.retrieval_guard import (
    AssetCatalogMetadataItem,
    AssetCatalogRetrievalDecision,
    AssetCatalogRetrievalGuard,
    AssetCatalogRetrievalIntent,
    AssetCatalogRetrievalRequest,
)

AssetCatalogQueryPreviewResponseKind = Literal["catalog_preview", "missing_evidence"]


@dataclass(frozen=True)
class AssetCatalogQueryPreviewResponse:
    query: str
    intent: AssetCatalogRetrievalIntent
    response_kind: AssetCatalogQueryPreviewResponseKind
    catalog_items: tuple[AssetCatalogMetadataItem, ...]
    prompt_items: tuple[AssetCatalogMetadataItem, ...]
    missing_evidence: bool
    missing_evidence_reason: str | None
    denied_count: int
    skipped_count: int
    content_answer_blocked: bool
    permission_fail_closed: bool
    asset_catalog_only: bool = True
    content_evidence_available: bool = False
    writes_documents: bool = False
    writes_chunks: bool = False
    writes_opensearch: bool = False
    writes_qdrant: bool = False

    @classmethod
    def from_decision(
        cls,
        request: AssetCatalogRetrievalRequest,
        decision: AssetCatalogRetrievalDecision,
    ) -> AssetCatalogQueryPreviewResponse:
        if decision.prompt_items:
            raise ValueError("asset catalog query preview cannot include prompt items")
        if (
            decision.writes_documents
            or decision.writes_chunks
            or decision.writes_opensearch
            or decision.writes_qdrant
        ):
            raise ValueError("asset catalog query preview cannot include write side effects")

        response_kind: AssetCatalogQueryPreviewResponseKind = (
            "missing_evidence" if decision.missing_evidence else "catalog_preview"
        )
        missing_reason = decision.missing_evidence_reason
        return cls(
            query=request.query,
            intent=decision.intent,
            response_kind=response_kind,
            catalog_items=decision.catalog_items,
            prompt_items=decision.prompt_items,
            missing_evidence=decision.missing_evidence,
            missing_evidence_reason=missing_reason,
            denied_count=decision.denied_count,
            skipped_count=decision.skipped_count,
            content_answer_blocked=request.intent == "content_answer",
            permission_fail_closed=missing_reason == "permission_scope_required",
            asset_catalog_only=(
                not decision.catalog_items
                or all(not item.content_evidence_available for item in decision.catalog_items)
            ),
            content_evidence_available=False,
            writes_documents=decision.writes_documents,
            writes_chunks=decision.writes_chunks,
            writes_opensearch=decision.writes_opensearch,
            writes_qdrant=decision.writes_qdrant,
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "response_kind": self.response_kind,
            "query": self.query,
            "intent": self.intent,
            "missing_evidence": self.missing_evidence,
            "missing_evidence_reason": self.missing_evidence_reason,
            "reason": self.missing_evidence_reason,
            "catalog_items": [self._metadata_item_to_dict(item) for item in self.catalog_items],
            "prompt_items": [self._metadata_item_to_dict(item) for item in self.prompt_items],
            "denied_count": self.denied_count,
            "skipped_count": self.skipped_count,
            "content_answer_blocked": self.content_answer_blocked,
            "permission_fail_closed": self.permission_fail_closed,
            "asset_catalog_only": self.asset_catalog_only,
            "content_evidence_available": self.content_evidence_available,
            "writes_documents": self.writes_documents,
            "writes_chunks": self.writes_chunks,
            "writes_opensearch": self.writes_opensearch,
            "writes_qdrant": self.writes_qdrant,
        }

    def _metadata_item_to_dict(self, item: AssetCatalogMetadataItem) -> dict[str, Any]:
        return {
            "asset_uid": item.asset_uid,
            "source_view": item.source_view,
            "source_id": item.source_id,
            "project_id": item.project_id,
            "evidence_kind": item.evidence_kind,
            "citation_status": item.citation_status,
            "content_evidence_available": item.content_evidence_available,
            "permission_tags": list(item.permission_tags),
            "confidentiality_level": item.confidentiality_level,
            "last_seen_at": item.last_seen_at,
            "lifecycle_status": item.lifecycle_status,
            "index_eligibility": item.index_eligibility,
        }


class AssetCatalogQueryPreviewer:
    """Readonly catalog query preview that never promotes DB metadata to answer evidence."""

    def __init__(self, guard: AssetCatalogRetrievalGuard | None = None) -> None:
        self.guard = guard or AssetCatalogRetrievalGuard()

    def preview(
        self,
        mirror_preview: AssetCatalogMirrorPreview,
        request: AssetCatalogRetrievalRequest,
    ) -> AssetCatalogQueryPreviewResponse:
        return AssetCatalogQueryPreviewResponse.from_decision(
            request,
            self.guard.evaluate(mirror_preview, request),
        )
