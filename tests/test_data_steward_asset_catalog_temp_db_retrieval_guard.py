from __future__ import annotations

import sqlite3
from pathlib import Path

import pytest

from app.services.asset_catalog import (
    AssetCatalogMirrorPreviewer,
    AssetCatalogRetrievalGuard,
    AssetCatalogRetrievalRequest,
    AssetCatalogTemporaryMirrorStore,
    FakePlatformAssetCatalogAdapter,
)

PROJECT_101 = "101-C\u5854"


def _store_with_preview() -> AssetCatalogTemporaryMirrorStore:
    connection = sqlite3.connect(":memory:")
    store = AssetCatalogTemporaryMirrorStore(connection)
    store.create_schema()
    preview = AssetCatalogMirrorPreviewer(FakePlatformAssetCatalogAdapter()).preview()
    store.apply_preview(preview)
    return store


def test_temp_db_backed_guard_returns_authorized_catalog_metadata_only() -> None:
    decision = AssetCatalogRetrievalGuard().evaluate(
        _store_with_preview().load_retrieval_preview(),
        AssetCatalogRetrievalRequest(
            query="list visible catalog assets",
            intent="catalog_lookup",
            allowed_project_ids=(PROJECT_101,),
        ),
    )

    assert [item.source_id for item in decision.catalog_items] == [
        "file-101-model-index"
    ]
    assert decision.prompt_items == ()
    assert decision.writes_documents is False
    assert decision.writes_chunks is False
    assert decision.writes_opensearch is False
    assert decision.writes_qdrant is False


def test_temp_db_backed_content_answer_returns_asset_catalog_only() -> None:
    decision = AssetCatalogRetrievalGuard().evaluate(
        _store_with_preview().load_retrieval_preview(),
        AssetCatalogRetrievalRequest(
            query="summarize the model index file contents",
            intent="content_answer",
            allowed_project_ids=(PROJECT_101,),
        ),
    )

    assert decision.catalog_items == ()
    assert decision.prompt_items == ()
    assert decision.missing_evidence is True
    assert decision.missing_evidence_reason == "asset_catalog_only"


def test_temp_db_backed_guard_rejects_file_backed_sqlite(tmp_path: Path) -> None:
    store = AssetCatalogTemporaryMirrorStore(sqlite3.connect(tmp_path / "mirror.db"))

    with pytest.raises(ValueError, match="in-memory SQLite"):
        store.load_retrieval_preview()
