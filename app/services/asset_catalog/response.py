from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal

from app.services.asset_catalog.retrieval_guard import (
    AssetCatalogMetadataItem,
    AssetCatalogRetrievalDecision,
    AssetCatalogRetrievalIntent,
    AssetCatalogRetrievalRequest,
)

AssetCatalogResponseKind = Literal["missing_evidence"]


@dataclass(frozen=True)
class AssetCatalogMissingEvidenceResponse:
    query: str
    intent: AssetCatalogRetrievalIntent
    reason: str
    catalog_items: tuple[AssetCatalogMetadataItem, ...]
    prompt_items: tuple[AssetCatalogMetadataItem, ...]
    missing_evidence: bool = True
    response_kind: AssetCatalogResponseKind = "missing_evidence"
    writes_documents: bool = False
    writes_chunks: bool = False
    writes_opensearch: bool = False
    writes_qdrant: bool = False

    @classmethod
    def from_decision(
        cls,
        request: AssetCatalogRetrievalRequest,
        decision: AssetCatalogRetrievalDecision,
    ) -> AssetCatalogMissingEvidenceResponse:
        if not decision.missing_evidence:
            raise ValueError("expected missing evidence decision")
        if decision.missing_evidence_reason is None:
            raise ValueError("missing evidence decision requires a reason")
        if decision.prompt_items:
            raise ValueError("missing evidence response cannot include prompt items")
        if (
            decision.writes_documents
            or decision.writes_chunks
            or decision.writes_opensearch
            or decision.writes_qdrant
        ):
            raise ValueError("missing evidence response cannot include write side effects")
        return cls(
            query=request.query,
            intent=decision.intent,
            reason=decision.missing_evidence_reason,
            catalog_items=decision.catalog_items,
            prompt_items=decision.prompt_items,
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
            "reason": self.reason,
            "catalog_items": [self._metadata_item_to_dict(item) for item in self.catalog_items],
            "prompt_items": [self._metadata_item_to_dict(item) for item in self.prompt_items],
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
        }
