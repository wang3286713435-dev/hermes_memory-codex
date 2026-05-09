from __future__ import annotations

from app.services.asset_catalog import (
    AssetCatalogMirrorPreviewer,
    AssetCatalogRetrievalGuard,
    AssetCatalogRetrievalRequest,
    FakePlatformAssetCatalogAdapter,
)

PROJECT_101 = "101-C\u5854"
PROJECT_98 = "98-\u6df1\u5733\u53e3\u5cb8\u9879\u76ee"


def _preview():
    return AssetCatalogMirrorPreviewer(FakePlatformAssetCatalogAdapter()).preview()


def test_catalog_lookup_returns_only_authorized_metadata_and_never_prompt_items() -> None:
    decision = AssetCatalogRetrievalGuard().evaluate(
        _preview(),
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
    assert decision.missing_evidence is False
    assert decision.writes_documents is False
    assert decision.writes_chunks is False
    assert decision.writes_opensearch is False
    assert decision.writes_qdrant is False


def test_content_answer_request_returns_asset_catalog_only_missing_evidence() -> None:
    decision = AssetCatalogRetrievalGuard().evaluate(
        _preview(),
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


def test_denied_count_does_not_leak_assets_outside_allowed_projects() -> None:
    decision = AssetCatalogRetrievalGuard().evaluate(
        _preview(),
        AssetCatalogRetrievalRequest(
            query="list visible catalog assets",
            intent="catalog_lookup",
            allowed_project_ids=(PROJECT_101,),
        ),
    )

    assert decision.denied_count == 0


def test_missing_project_scope_denies_catalog_and_prompt_context() -> None:
    decision = AssetCatalogRetrievalGuard().evaluate(
        _preview(),
        AssetCatalogRetrievalRequest(
            query="list all catalog assets",
            intent="catalog_lookup",
            allowed_project_ids=(),
        ),
    )

    assert decision.catalog_items == ()
    assert decision.prompt_items == ()
    assert decision.missing_evidence is True
    assert decision.missing_evidence_reason == "permission_scope_required"


def test_denied_or_non_active_assets_do_not_become_catalog_results() -> None:
    decision = AssetCatalogRetrievalGuard().evaluate(
        _preview(),
        AssetCatalogRetrievalRequest(
            query="list visible port project files",
            intent="catalog_lookup",
            allowed_project_ids=(PROJECT_98,),
        ),
    )

    assert decision.catalog_items == ()
    assert decision.prompt_items == ()
    assert decision.denied_count == 1
    assert decision.skipped_count == 5
