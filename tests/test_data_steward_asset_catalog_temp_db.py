from __future__ import annotations

import sqlite3
from pathlib import Path

import pytest

from app.services.asset_catalog import (
    AssetCatalogMirrorPreviewer,
    AssetCatalogTemporaryMirrorStore,
    FakePlatformAssetCatalogAdapter,
)


def _preview():
    return AssetCatalogMirrorPreviewer(FakePlatformAssetCatalogAdapter()).preview()


def _table_names(connection: sqlite3.Connection) -> set[str]:
    return {
        row[0]
        for row in connection.execute(
            "SELECT name FROM sqlite_master WHERE type = 'table'"
        ).fetchall()
    }


def test_temporary_mirror_store_creates_only_catalog_contract_table() -> None:
    connection = sqlite3.connect(":memory:")
    store = AssetCatalogTemporaryMirrorStore(connection)

    store.create_schema()

    assert _table_names(connection) == {"external_asset_catalog_contract"}


def test_temporary_mirror_store_writes_preview_rows_without_indexes_or_documents() -> None:
    connection = sqlite3.connect(":memory:")
    store = AssetCatalogTemporaryMirrorStore(connection)
    store.create_schema()

    summary = store.apply_preview(_preview())

    assert summary.temporary_db is True
    assert summary.writes_production_db is False
    assert summary.writes_documents is False
    assert summary.writes_chunks is False
    assert summary.writes_opensearch is False
    assert summary.writes_qdrant is False
    assert summary.rows_written == 6
    assert summary.last_event_id_candidate == 1006
    assert _table_names(connection) == {"external_asset_catalog_contract"}


def test_temporary_mirror_store_preserves_permission_and_evidence_boundaries() -> None:
    connection = sqlite3.connect(":memory:")
    store = AssetCatalogTemporaryMirrorStore(connection)
    store.create_schema()
    store.apply_preview(_preview())

    denied = connection.execute(
        """
        SELECT preview_action, preview_reason, permission_status, citation_status,
               evidence_kind, content_evidence_available
        FROM external_asset_catalog_contract
        WHERE source_id = ?
        """,
        ("file-98-internal-review-no-tags",),
    ).fetchone()

    assert denied == (
        "would_deny",
        "missing_permission_tags",
        "denied",
        "metadata_only",
        "asset_catalog_evidence",
        0,
    )


def test_temporary_mirror_store_upsert_is_idempotent_by_asset_uid() -> None:
    connection = sqlite3.connect(":memory:")
    store = AssetCatalogTemporaryMirrorStore(connection)
    store.create_schema()

    store.apply_preview(_preview())
    store.apply_preview(_preview())

    row_count = connection.execute(
        "SELECT COUNT(*) FROM external_asset_catalog_contract"
    ).fetchone()[0]
    last_event_id = connection.execute(
        "SELECT MAX(last_event_id) FROM external_asset_catalog_contract"
    ).fetchone()[0]

    assert row_count == 6
    assert last_event_id == 1006


def test_temporary_mirror_store_rejects_file_backed_sqlite(tmp_path: Path) -> None:
    connection = sqlite3.connect(tmp_path / "asset_catalog.db")
    store = AssetCatalogTemporaryMirrorStore(connection)

    with pytest.raises(ValueError, match="in-memory SQLite"):
        store.create_schema()
