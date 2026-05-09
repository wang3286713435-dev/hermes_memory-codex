from __future__ import annotations

import sqlite3

import pytest

from app.services.asset_catalog import (
    AssetCatalogMirrorPreviewer,
    AssetCatalogMissingEvidenceResponse,
    AssetCatalogRetrievalRequest,
    AssetCatalogTemporaryMirrorStore,
    FakePlatformAssetCatalogAdapter,
)

PROJECT_101 = "101-C\u5854"


def _retrieval_preview_from_temp_db():
    connection = sqlite3.connect(":memory:")
    store = AssetCatalogTemporaryMirrorStore(connection)
    store.create_schema()
    store.apply_preview(
        AssetCatalogMirrorPreviewer(FakePlatformAssetCatalogAdapter()).preview(),
    )
    return store.load_retrieval_preview()


def test_temp_db_backed_content_answer_builds_missing_evidence_response() -> None:
    request = AssetCatalogRetrievalRequest(
        query="summarize the model index file contents",
        intent="content_answer",
        allowed_project_ids=(PROJECT_101,),
    )

    response = AssetCatalogMissingEvidenceResponse.from_preview(
        _retrieval_preview_from_temp_db(),
        request,
    )

    assert response.reason == "asset_catalog_only"
    assert response.catalog_items == ()
    assert response.prompt_items == ()
    assert response.writes_documents is False
    assert response.writes_chunks is False
    assert response.writes_opensearch is False
    assert response.writes_qdrant is False
    assert response.to_dict()["prompt_items"] == []


def test_temp_db_backed_missing_scope_builds_missing_evidence_response() -> None:
    request = AssetCatalogRetrievalRequest(
        query="list all catalog assets",
        intent="catalog_lookup",
        allowed_project_ids=(),
    )

    response = AssetCatalogMissingEvidenceResponse.from_preview(
        _retrieval_preview_from_temp_db(),
        request,
    )

    assert response.reason == "permission_scope_required"
    assert response.catalog_items == ()
    assert response.prompt_items == ()


def test_temp_db_backed_catalog_lookup_response_is_rejected() -> None:
    request = AssetCatalogRetrievalRequest(
        query="list visible catalog assets",
        intent="catalog_lookup",
        allowed_project_ids=(PROJECT_101,),
    )

    with pytest.raises(ValueError, match="missing evidence decision"):
        AssetCatalogMissingEvidenceResponse.from_preview(
            _retrieval_preview_from_temp_db(),
            request,
        )
