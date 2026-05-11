from __future__ import annotations

from app.services.asset_catalog import (
    AssetCatalogMirrorPreviewer,
    FakePlatformAssetCatalogAdapter,
)


def _preview():
    return AssetCatalogMirrorPreviewer(FakePlatformAssetCatalogAdapter()).preview()


def test_asset_catalog_mirror_preview_never_writes_db_documents_or_indexes() -> None:
    preview = _preview()

    assert preview.summary.dry_run is True
    assert preview.summary.writes_db is False
    assert preview.summary.writes_documents is False
    assert preview.summary.writes_chunks is False
    assert preview.summary.writes_opensearch is False
    assert preview.summary.writes_qdrant is False
    assert preview.items
    assert all(item.writes_db is False for item in preview.items)
    assert all(item.writes_documents is False for item in preview.items)
    assert all(item.writes_chunks is False for item in preview.items)
    assert all(item.writes_opensearch is False for item in preview.items)
    assert all(item.writes_qdrant is False for item in preview.items)


def test_asset_catalog_mirror_preview_actions_from_fake_events() -> None:
    actions = {item.source_id: item.action for item in _preview().items}

    assert actions["file-101-model-index"] == "would_upsert"
    assert actions["file-101-checksum-missing"] == "would_require_human_review"
    assert actions["file-98-internal-review-no-tags"] == "would_deny"
    assert actions["file-99-model-moved"] == "would_mark_moved"
    assert actions["file-99-stale-old-path"] == "would_mark_stale"
    assert actions["file-98-missing-file"] == "would_mark_missing"


def test_asset_catalog_mirror_preview_keeps_permission_and_evidence_boundary() -> None:
    items = {item.source_id: item for item in _preview().items}

    denied = items["file-98-internal-review-no-tags"]
    assert denied.permission_status == "denied"
    assert denied.reason == "missing_permission_tags"

    for item in items.values():
        assert item.citation_status == "metadata_only"
        assert item.content_evidence_available is False
        assert item.evidence_kind == "asset_catalog_evidence"


def test_asset_catalog_mirror_preview_checkpoint_uses_event_id() -> None:
    preview = _preview()

    assert [item.last_event_id for item in preview.items] == [1001, 1002, 1003, 1004, 1005, 1006]
    assert preview.summary.last_event_id_candidate == 1006


def test_asset_catalog_mirror_preview_after_event_id_filters_checkpoint_window() -> None:
    preview = AssetCatalogMirrorPreviewer(FakePlatformAssetCatalogAdapter()).preview(
        after_event_id=1002
    )

    assert [item.last_event_id for item in preview.items] == [1003, 1004, 1005, 1006]
    assert preview.summary.last_event_id_candidate == 1006


def test_asset_catalog_mirror_preview_summary_counts_denied_and_review_items() -> None:
    summary = _preview().summary

    assert summary.denied_count == 1
    assert summary.requires_human_review_count == 1
