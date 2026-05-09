from __future__ import annotations

import pytest

from app.services.asset_catalog import (
    AssetCatalogMetadataItem,
    AssetCatalogMirrorPreviewer,
    AssetCatalogMissingEvidenceResponse,
    AssetCatalogRetrievalDecision,
    AssetCatalogRetrievalGuard,
    AssetCatalogRetrievalRequest,
    FakePlatformAssetCatalogAdapter,
)

PROJECT_101 = "101-C\u5854"


def _decision(request: AssetCatalogRetrievalRequest):
    preview = AssetCatalogMirrorPreviewer(FakePlatformAssetCatalogAdapter()).preview()
    return AssetCatalogRetrievalGuard().evaluate(preview, request)


def test_missing_evidence_response_for_catalog_only_content_answer() -> None:
    request = AssetCatalogRetrievalRequest(
        query="summarize the model index file contents",
        intent="content_answer",
        allowed_project_ids=(PROJECT_101,),
    )

    response = AssetCatalogMissingEvidenceResponse.from_decision(
        request,
        _decision(request),
    )

    assert response.missing_evidence is True
    assert response.reason == "asset_catalog_only"
    assert response.prompt_items == ()
    assert response.catalog_items == ()
    assert response.writes_documents is False
    assert response.writes_chunks is False
    assert response.writes_opensearch is False
    assert response.writes_qdrant is False
    assert response.to_dict() == {
        "response_kind": "missing_evidence",
        "query": "summarize the model index file contents",
        "intent": "content_answer",
        "missing_evidence": True,
        "reason": "asset_catalog_only",
        "catalog_items": [],
        "prompt_items": [],
        "writes_documents": False,
        "writes_chunks": False,
        "writes_opensearch": False,
        "writes_qdrant": False,
    }


def test_missing_evidence_response_for_missing_permission_scope() -> None:
    request = AssetCatalogRetrievalRequest(
        query="list all catalog assets",
        intent="catalog_lookup",
        allowed_project_ids=(),
    )

    response = AssetCatalogMissingEvidenceResponse.from_decision(
        request,
        _decision(request),
    )

    assert response.reason == "permission_scope_required"
    assert response.prompt_items == ()
    assert response.catalog_items == ()


def test_missing_evidence_response_for_no_authorized_catalog_metadata() -> None:
    request = AssetCatalogRetrievalRequest(
        query="summarize unavailable project assets",
        intent="content_answer",
        allowed_project_ids=("project-not-visible",),
    )

    response = AssetCatalogMissingEvidenceResponse.from_decision(
        request,
        _decision(request),
    )

    assert response.reason == "no_authorized_catalog_metadata"
    assert response.prompt_items == ()
    assert response.catalog_items == ()


def test_missing_evidence_response_rejects_catalog_lookup_decision() -> None:
    request = AssetCatalogRetrievalRequest(
        query="list visible catalog assets",
        intent="catalog_lookup",
        allowed_project_ids=(PROJECT_101,),
    )

    with pytest.raises(ValueError, match="missing evidence decision"):
        AssetCatalogMissingEvidenceResponse.from_decision(request, _decision(request))


def test_missing_evidence_response_rejects_missing_reason() -> None:
    request = AssetCatalogRetrievalRequest(
        query="summarize missing reason",
        intent="content_answer",
        allowed_project_ids=(PROJECT_101,),
    )
    unsafe_decision = AssetCatalogRetrievalDecision(
        intent="content_answer",
        catalog_items=(),
        prompt_items=(),
        missing_evidence=True,
        missing_evidence_reason=None,
        denied_count=0,
        skipped_count=0,
    )

    with pytest.raises(ValueError, match="requires a reason"):
        AssetCatalogMissingEvidenceResponse.from_decision(request, unsafe_decision)


def test_missing_evidence_response_rejects_prompt_items() -> None:
    request = AssetCatalogRetrievalRequest(
        query="summarize unsafe prompt item",
        intent="content_answer",
        allowed_project_ids=(PROJECT_101,),
    )
    unsafe_item = AssetCatalogMetadataItem(
        asset_uid="delivery_platform:FileAssetView:file-unsafe",
        source_view="FileAssetView",
        source_id="file-unsafe",
        project_id=PROJECT_101,
        evidence_kind="asset_catalog_evidence",
        citation_status="metadata_only",
        content_evidence_available=False,
    )
    unsafe_decision = AssetCatalogRetrievalDecision(
        intent="content_answer",
        catalog_items=(),
        prompt_items=(unsafe_item,),
        missing_evidence=True,
        missing_evidence_reason="asset_catalog_only",
        denied_count=0,
        skipped_count=0,
    )

    with pytest.raises(ValueError, match="cannot include prompt items"):
        AssetCatalogMissingEvidenceResponse.from_decision(request, unsafe_decision)
