from __future__ import annotations

import sqlite3
from dataclasses import dataclass

from app.services.asset_catalog.mirror_preview import AssetCatalogMirrorPreview

TEMP_MIRROR_TABLE = "external_asset_catalog_contract"
TEMP_MIRROR_SCHEMA_VERSION = "db2.temp.external_asset_catalog_contract.v1"


@dataclass(frozen=True)
class AssetCatalogTemporaryMirrorWriteSummary:
    temporary_db: bool
    rows_written: int
    last_event_id_candidate: int | None
    writes_production_db: bool = False
    writes_documents: bool = False
    writes_chunks: bool = False
    writes_opensearch: bool = False
    writes_qdrant: bool = False


class AssetCatalogTemporaryMirrorStore:
    """Temporary SQLite proof store for DB-2 catalog mirror contract tests."""

    def __init__(self, connection: sqlite3.Connection) -> None:
        self.connection = connection

    def create_schema(self) -> None:
        self._ensure_temporary_database()
        self.connection.execute(
            f"""
            CREATE TABLE IF NOT EXISTS {TEMP_MIRROR_TABLE} (
                asset_uid TEXT PRIMARY KEY NOT NULL,
                source_view TEXT NOT NULL,
                contract_version TEXT NOT NULL,
                source_id TEXT NOT NULL,
                project_id TEXT,
                preview_action TEXT NOT NULL,
                preview_reason TEXT NOT NULL,
                permission_status TEXT NOT NULL,
                sync_status TEXT NOT NULL,
                checksum_status TEXT NOT NULL,
                citation_status TEXT NOT NULL,
                evidence_kind TEXT NOT NULL,
                content_evidence_available INTEGER NOT NULL,
                last_event_id INTEGER NOT NULL,
                schema_version TEXT NOT NULL
            )
            """
        )
        self.connection.commit()

    def apply_preview(
        self,
        preview: AssetCatalogMirrorPreview,
    ) -> AssetCatalogTemporaryMirrorWriteSummary:
        self._ensure_temporary_database()
        self.connection.executemany(
            f"""
            INSERT INTO {TEMP_MIRROR_TABLE} (
                asset_uid,
                source_view,
                contract_version,
                source_id,
                project_id,
                preview_action,
                preview_reason,
                permission_status,
                sync_status,
                checksum_status,
                citation_status,
                evidence_kind,
                content_evidence_available,
                last_event_id,
                schema_version
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(asset_uid) DO UPDATE SET
                source_view = excluded.source_view,
                contract_version = excluded.contract_version,
                source_id = excluded.source_id,
                project_id = excluded.project_id,
                preview_action = excluded.preview_action,
                preview_reason = excluded.preview_reason,
                permission_status = excluded.permission_status,
                sync_status = excluded.sync_status,
                checksum_status = excluded.checksum_status,
                citation_status = excluded.citation_status,
                evidence_kind = excluded.evidence_kind,
                content_evidence_available = excluded.content_evidence_available,
                last_event_id = excluded.last_event_id,
                schema_version = excluded.schema_version
            """,
            [
                (
                    item.asset_uid,
                    item.source_view,
                    item.contract_version,
                    item.source_id,
                    item.project_id,
                    item.action,
                    item.reason,
                    item.permission_status,
                    item.sync_status,
                    item.checksum_status,
                    item.citation_status,
                    item.evidence_kind,
                    int(item.content_evidence_available),
                    item.last_event_id,
                    TEMP_MIRROR_SCHEMA_VERSION,
                )
                for item in preview.items
            ],
        )
        self.connection.commit()
        return AssetCatalogTemporaryMirrorWriteSummary(
            temporary_db=True,
            rows_written=len(preview.items),
            last_event_id_candidate=preview.summary.last_event_id_candidate,
        )

    def _ensure_temporary_database(self) -> None:
        databases = self.connection.execute("PRAGMA database_list").fetchall()
        file_paths = [
            row[2]
            for row in databases
            if row[1] not in {"temp"} and row[2] not in {"", None}
        ]
        if file_paths:
            raise ValueError("temporary mirror store only accepts in-memory SQLite")
