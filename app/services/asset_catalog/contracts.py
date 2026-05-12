from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal

SourceView = Literal[
    "ProjectAssetView",
    "FileAssetView",
    "ModelAssetView",
    "AuditEventView",
]

SOURCE_VIEWS: tuple[SourceView, ...] = (
    "ProjectAssetView",
    "FileAssetView",
    "ModelAssetView",
    "AuditEventView",
)

VIEW_CONTRACT_VERSIONS: dict[SourceView, str] = {
    "ProjectAssetView": "delivery_platform.asset_views.v1.1",
    "FileAssetView": "delivery_platform.asset_views.v1.1",
    "ModelAssetView": "delivery_platform.asset_views.v1.1",
    "AuditEventView": "delivery_platform.asset_views.v1.1",
}

DEFAULT_SOURCE_SYSTEM = "delivery_platform"
MAX_PAGE_LIMIT = 100


@dataclass(frozen=True)
class AssetViewRecord:
    source_view: SourceView
    contract_version: str
    source_system: str
    source_id: str
    asset_uid: str
    project_id: str | None
    project_scope: tuple[str, ...]
    permission_tags: tuple[str, ...]
    permission_status: str
    permission_reason: str | None
    confidentiality_level: str
    last_seen_at: str | None
    lifecycle_status: str
    index_eligibility: str
    sync_status: str
    checksum_status: str
    citation_status: str
    evidence_kind: str
    metadata_evidence_available: bool
    content_evidence_available: bool
    row: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        payload = dict(self.row)
        payload.update(
            {
                "source_view": self.source_view,
                "contract_version": self.contract_version,
                "source_system": self.source_system,
                "source_id": self.source_id,
                "asset_uid": self.asset_uid,
                "project_id": self.project_id,
                "project_scope": list(self.project_scope),
                "permission_tags": list(self.permission_tags),
                "permission_status": self.permission_status,
                "permission_reason": self.permission_reason,
                "confidentiality_level": self.confidentiality_level,
                "last_seen_at": self.last_seen_at,
                "lifecycle_status": self.lifecycle_status,
                "index_eligibility": self.index_eligibility,
                "sync_status": self.sync_status,
                "checksum_status": self.checksum_status,
                "citation_status": self.citation_status,
                "evidence_kind": self.evidence_kind,
                "metadata_evidence_available": self.metadata_evidence_available,
                "content_evidence_available": self.content_evidence_available,
            }
        )
        return payload


@dataclass(frozen=True)
class AssetViewPage:
    source_view: SourceView
    contract_version: str
    items: tuple[AssetViewRecord, ...]
    limit: int
    next_cursor: str | None
    has_more: bool

    def to_dict(self) -> dict[str, Any]:
        return {
            "source_view": self.source_view,
            "contract_version": self.contract_version,
            "items": [item.to_dict() for item in self.items],
            "limit": self.limit,
            "next_cursor": self.next_cursor,
            "has_more": self.has_more,
        }
