from __future__ import annotations

import base64
import json
from pathlib import Path
from typing import Any

from app.services.asset_catalog.contracts import (
    DEFAULT_SOURCE_SYSTEM,
    MAX_PAGE_LIMIT,
    SOURCE_VIEWS,
    VIEW_CONTRACT_VERSIONS,
    AssetViewPage,
    AssetViewRecord,
    SourceView,
)

DEFAULT_FIXTURE_DIR = Path(__file__).resolve().parent / "fixtures"
FIXTURE_FILES: dict[SourceView, str] = {
    "ProjectAssetView": "project_asset_view.json",
    "FileAssetView": "file_asset_view.json",
    "ModelAssetView": "model_asset_view.json",
    "AuditEventView": "audit_event_view.json",
}


class FakePlatformAssetCatalogAdapter:
    """Read-only fake adapter for DB-1a platform asset View contract tests."""

    def __init__(self, fixture_dir: Path | None = None) -> None:
        self.fixture_dir = fixture_dir or DEFAULT_FIXTURE_DIR
        self._records: dict[SourceView, tuple[AssetViewRecord, ...]] = {
            view: self._load_records(view) for view in SOURCE_VIEWS
        }

    def list_project_assets(
        self,
        *,
        limit: int = MAX_PAGE_LIMIT,
        cursor: str | None = None,
        filters: dict[str, Any] | None = None,
    ) -> AssetViewPage:
        return self.list_view("ProjectAssetView", limit=limit, cursor=cursor, filters=filters)

    def list_file_assets(
        self,
        *,
        limit: int = MAX_PAGE_LIMIT,
        cursor: str | None = None,
        filters: dict[str, Any] | None = None,
    ) -> AssetViewPage:
        return self.list_view("FileAssetView", limit=limit, cursor=cursor, filters=filters)

    def list_model_assets(
        self,
        *,
        limit: int = MAX_PAGE_LIMIT,
        cursor: str | None = None,
        filters: dict[str, Any] | None = None,
    ) -> AssetViewPage:
        return self.list_view("ModelAssetView", limit=limit, cursor=cursor, filters=filters)

    def list_audit_events(
        self,
        *,
        limit: int = MAX_PAGE_LIMIT,
        cursor: str | None = None,
        after_event_id: int | None = None,
        filters: dict[str, Any] | None = None,
    ) -> AssetViewPage:
        event_filters = dict(filters or {})
        if after_event_id is not None:
            event_filters["event_id_gt"] = after_event_id
        return self.list_view(
            "AuditEventView",
            limit=limit,
            cursor=cursor,
            filters=event_filters or None,
        )

    def list_view(
        self,
        source_view: SourceView,
        *,
        limit: int = MAX_PAGE_LIMIT,
        cursor: str | None = None,
        filters: dict[str, Any] | None = None,
    ) -> AssetViewPage:
        page_limit = self._normalize_limit(limit)
        normalized_filters = filters or {}
        start = self._decode_cursor(cursor, source_view, normalized_filters) if cursor else 0
        records = self._filter_records(self._records[source_view], normalized_filters)
        page_items = records[start : start + page_limit]
        next_offset = start + len(page_items)
        has_more = next_offset < len(records)
        next_cursor = (
            self._encode_cursor(source_view, next_offset, normalized_filters)
            if has_more
            else None
        )

        return AssetViewPage(
            source_view=source_view,
            contract_version=VIEW_CONTRACT_VERSIONS[source_view],
            items=tuple(page_items),
            limit=page_limit,
            next_cursor=next_cursor,
            has_more=has_more,
        )

    def _load_records(self, source_view: SourceView) -> tuple[AssetViewRecord, ...]:
        fixture_path = self.fixture_dir / FIXTURE_FILES[source_view]
        with fixture_path.open(encoding="utf-8") as fixture_file:
            fixture = json.load(fixture_file)

        contract_version = fixture.get("contract_version")
        if fixture.get("source_view") != source_view:
            raise ValueError(f"fixture source_view mismatch for {source_view}")
        if contract_version != VIEW_CONTRACT_VERSIONS[source_view]:
            raise ValueError(f"fixture contract_version mismatch for {source_view}")

        records = [
            self._normalize_record(
                source_view=source_view,
                contract_version=contract_version,
                source_system=fixture.get("source_system") or DEFAULT_SOURCE_SYSTEM,
                row=row,
            )
            for row in fixture.get("records", [])
        ]

        if source_view == "AuditEventView":
            records.sort(key=lambda item: int(item.row["event_id"]))
        return tuple(records)

    def _normalize_record(
        self,
        *,
        source_view: SourceView,
        contract_version: str,
        source_system: str,
        row: dict[str, Any],
    ) -> AssetViewRecord:
        normalized = dict(row)
        row_source_system = normalized.get("source_system") or source_system
        source_id = str(normalized["source_id"])
        asset_uid = f"{row_source_system}:{source_id}"
        if normalized.get("asset_uid", asset_uid) != asset_uid:
            raise ValueError(f"asset_uid mismatch for {source_view}:{source_id}")

        row_contract_version = normalized.get("contract_version") or contract_version
        if row_contract_version != contract_version:
            raise ValueError(f"record contract_version mismatch for {source_view}:{source_id}")

        project_id = normalized.get("project_id")
        project_scope = tuple(
            normalized.get("project_scope") or ([project_id] if project_id else [])
        )
        permission_tags = tuple(normalized.get("permission_tags") or [])
        if permission_tags:
            permission_status = normalized.get("permission_status") or "allowed"
            permission_reason = normalized.get("permission_reason")
        else:
            permission_status = "denied"
            permission_reason = "missing_permission_tags"

        sync_status = normalized.get("sync_status") or "active"
        checksum_status = self._checksum_status(source_view, normalized)
        citation_status = normalized.get("citation_status") or "metadata_only"
        metadata_evidence_available = permission_status == "allowed" and sync_status == "active"

        normalized.update(
            {
                "source_view": source_view,
                "contract_version": contract_version,
                "source_system": row_source_system,
                "asset_uid": asset_uid,
                "project_scope": list(project_scope),
                "permission_tags": list(permission_tags),
                "permission_status": permission_status,
                "permission_reason": permission_reason,
                "sync_status": sync_status,
                "checksum_status": checksum_status,
                "citation_status": citation_status,
                "evidence_kind": "asset_catalog_evidence",
                "metadata_evidence_available": metadata_evidence_available,
                "content_evidence_available": False,
            }
        )

        return AssetViewRecord(
            source_view=source_view,
            contract_version=contract_version,
            source_system=row_source_system,
            source_id=source_id,
            asset_uid=asset_uid,
            project_id=project_id,
            project_scope=project_scope,
            permission_tags=permission_tags,
            permission_status=permission_status,
            permission_reason=permission_reason,
            sync_status=sync_status,
            checksum_status=checksum_status,
            citation_status=citation_status,
            evidence_kind="asset_catalog_evidence",
            metadata_evidence_available=metadata_evidence_available,
            content_evidence_available=False,
            row=normalized,
        )

    def _filter_records(
        self,
        records: tuple[AssetViewRecord, ...],
        filters: dict[str, Any],
    ) -> tuple[AssetViewRecord, ...]:
        if not filters:
            return records
        return tuple(record for record in records if self._matches_filters(record, filters))

    def _matches_filters(self, record: AssetViewRecord, filters: dict[str, Any]) -> bool:
        payload = record.to_dict()
        for key, expected in filters.items():
            if key == "event_id_gt":
                if int(payload.get("event_id", -1)) <= int(expected):
                    return False
                continue
            if key not in payload:
                return False
            actual = payload[key]
            if isinstance(expected, (list, tuple, set)):
                if isinstance(actual, list):
                    if not set(actual).intersection(expected):
                        return False
                elif actual not in expected:
                    return False
            elif actual != expected:
                return False
        return True

    def _checksum_status(self, source_view: SourceView, row: dict[str, Any]) -> str:
        if source_view not in {"FileAssetView", "ModelAssetView"}:
            return row.get("checksum_status") or "not_applicable"
        return "present" if row.get("content_hash") else "missing"

    def _normalize_limit(self, limit: int) -> int:
        if limit <= 0:
            raise ValueError("limit must be positive")
        return min(limit, MAX_PAGE_LIMIT)

    def _encode_cursor(
        self,
        source_view: SourceView,
        offset: int,
        filters: dict[str, Any],
    ) -> str:
        payload = json.dumps(
            {
                "source_view": source_view,
                "offset": offset,
                "filter_fingerprint": self._filter_fingerprint(filters),
            },
            ensure_ascii=False,
            separators=(",", ":"),
        )
        return base64.urlsafe_b64encode(payload.encode("utf-8")).decode("ascii")

    def _decode_cursor(
        self,
        cursor: str,
        expected_view: SourceView,
        filters: dict[str, Any],
    ) -> int:
        try:
            raw = base64.urlsafe_b64decode(cursor.encode("ascii")).decode("utf-8")
            payload = json.loads(raw)
        except (ValueError, json.JSONDecodeError) as exc:
            raise ValueError("invalid cursor") from exc

        if payload.get("source_view") != expected_view:
            raise ValueError("cursor source_view mismatch")
        if payload.get("filter_fingerprint") != self._filter_fingerprint(filters):
            raise ValueError("cursor filter mismatch")
        offset = int(payload["offset"])
        if offset < 0:
            raise ValueError("cursor offset must be non-negative")
        return offset

    def _filter_fingerprint(self, filters: dict[str, Any]) -> str:
        return json.dumps(
            self._canonical_filter_value(filters),
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        )

    def _canonical_filter_value(self, value: Any) -> Any:
        if isinstance(value, dict):
            return {
                str(key): self._canonical_filter_value(value[key])
                for key in sorted(value, key=str)
            }
        if isinstance(value, (list, tuple, set)):
            items = [self._canonical_filter_value(item) for item in value]
            return sorted(
                items,
                key=lambda item: json.dumps(
                    item,
                    ensure_ascii=False,
                    separators=(",", ":"),
                    sort_keys=True,
                ),
            )
        return value
