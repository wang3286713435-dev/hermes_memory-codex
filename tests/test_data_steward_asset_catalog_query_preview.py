from __future__ import annotations

from app.services.asset_catalog import (
    AssetCatalogMirrorPreviewer,
    AssetCatalogQueryPreviewer,
    AssetCatalogRetrievalRequest,
    FakePlatformAssetCatalogAdapter,
)

PROJECT_101 = "101-C\u5854"
PROJECT_98 = "98-\u6df1\u5733\u53e3\u5cb8\u9879\u76ee"


def _preview():
    return AssetCatalogMirrorPreviewer(FakePlatformAssetCatalogAdapter()).preview()


def test_catalog_lookup_preview_returns_metadata_without_prompt_evidence_or_writes() -> None:
    response = AssetCatalogQueryPreviewer().preview(
        _preview(),
        AssetCatalogRetrievalRequest(
            query="列出 101-C塔 可见 BIM 资产目录",
            intent="catalog_lookup",
            allowed_project_ids=(PROJECT_101,),
        ),
    )

    assert response.response_kind == "catalog_preview"
    assert response.missing_evidence is False
    assert response.missing_evidence_reason is None
    assert [item.source_id for item in response.catalog_items] == [
        "file-101-model-index"
    ]
    assert response.prompt_items == ()
    assert response.content_evidence_available is False
    assert response.asset_catalog_only is True
    assert response.writes_documents is False
    assert response.writes_chunks is False
    assert response.writes_opensearch is False
    assert response.writes_qdrant is False

    payload = response.to_dict()
    assert payload["catalog_items"][0]["index_eligibility"] == "catalog_only"
    assert payload["catalog_items"][0]["confidentiality_level"] == "UNKNOWN"
    assert payload["catalog_items"][0]["content_evidence_available"] is False
    assert "storage_path" not in payload["catalog_items"][0]
    assert "raw_row" not in payload["catalog_items"][0]


def test_content_answer_preview_returns_asset_catalog_only_missing_evidence() -> None:
    response = AssetCatalogQueryPreviewer().preview(
        _preview(),
        AssetCatalogRetrievalRequest(
            query="总结 101-C塔 模型文件正文内容",
            intent="content_answer",
            allowed_project_ids=(PROJECT_101,),
        ),
    )

    assert response.response_kind == "missing_evidence"
    assert response.missing_evidence is True
    assert response.missing_evidence_reason == "asset_catalog_only"
    assert response.catalog_items == ()
    assert response.prompt_items == ()
    assert response.content_answer_blocked is True
    assert response.asset_catalog_only is True
    assert response.to_dict()["reason"] == "asset_catalog_only"


def test_missing_project_scope_fails_closed_without_catalog_leakage() -> None:
    response = AssetCatalogQueryPreviewer().preview(
        _preview(),
        AssetCatalogRetrievalRequest(
            query="列出所有 BIM 资产",
            intent="catalog_lookup",
            allowed_project_ids=(),
        ),
    )

    assert response.response_kind == "missing_evidence"
    assert response.missing_evidence_reason == "permission_scope_required"
    assert response.catalog_items == ()
    assert response.prompt_items == ()
    assert response.permission_fail_closed is True
    assert response.to_dict()["permission_fail_closed"] is True


def test_denied_project_scope_does_not_return_catalog_items() -> None:
    response = AssetCatalogQueryPreviewer().preview(
        _preview(),
        AssetCatalogRetrievalRequest(
            query="列出深圳口岸项目可见资产",
            intent="catalog_lookup",
            allowed_project_ids=(PROJECT_98,),
        ),
    )

    assert response.response_kind == "catalog_preview"
    assert response.catalog_items == ()
    assert response.prompt_items == ()
    assert response.denied_count == 1
    assert response.skipped_count == 5
    assert response.to_dict()["catalog_items"] == []
