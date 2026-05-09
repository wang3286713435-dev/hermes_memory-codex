from __future__ import annotations

import pytest

from app.core.config import Settings
from app.services.asset_catalog import VIEW_CONTRACT_VERSIONS, FakePlatformAssetCatalogAdapter


def _items(page):
    return [item.to_dict() for item in page.items]


def test_data_steward_feature_flags_default_off() -> None:
    assert Settings.model_fields["platform_asset_catalog_enabled"].default is False
    assert Settings.model_fields["platform_asset_sync_write_enabled"].default is False
    assert Settings.model_fields["platform_asset_mcp_enabled"].default is False
    assert Settings.model_fields["platform_asset_semantic_index_enabled"].default is False


def test_fake_fixtures_cover_required_views_and_projects() -> None:
    adapter = FakePlatformAssetCatalogAdapter()

    projects = _items(adapter.list_project_assets())
    project_ids = {project["project_id"] for project in projects}

    assert project_ids == {
        "101-C塔",
        "98-深圳口岸项目",
        "99-丰图既有建模项目",
    }
    assert {project["source_view"] for project in projects} == {"ProjectAssetView"}
    assert all(
        project["contract_version"] == VIEW_CONTRACT_VERSIONS["ProjectAssetView"]
        for project in projects
    )


def test_fake_adapter_paginates_with_limit_and_cursor() -> None:
    adapter = FakePlatformAssetCatalogAdapter()

    first_page = adapter.list_file_assets(limit=2)
    second_page = adapter.list_file_assets(limit=2, cursor=first_page.next_cursor)

    first_ids = {item.asset_uid for item in first_page.items}
    second_ids = {item.asset_uid for item in second_page.items}

    assert first_page.limit == 2
    assert first_page.has_more is True
    assert first_page.next_cursor is not None
    assert len(first_page.items) == 2
    assert len(second_page.items) == 2
    assert first_ids.isdisjoint(second_ids)


def test_contract_version_and_asset_uid_are_bound_for_all_views() -> None:
    adapter = FakePlatformAssetCatalogAdapter()

    pages = [
        adapter.list_project_assets(),
        adapter.list_file_assets(),
        adapter.list_model_assets(),
        adapter.list_audit_events(),
    ]

    for page in pages:
        assert page.contract_version == VIEW_CONTRACT_VERSIONS[page.source_view]
        for item in _items(page):
            assert item["contract_version"] == page.contract_version
            assert item["asset_uid"] == f"{item['source_system']}:{item['source_id']}"
            assert item["evidence_kind"] == "asset_catalog_evidence"
            assert item["citation_status"] == "metadata_only"
            assert item["content_evidence_available"] is False


def test_permission_tags_missing_defaults_to_denied() -> None:
    adapter = FakePlatformAssetCatalogAdapter()

    page = adapter.list_file_assets(filters={"source_id": "file-98-internal-review-no-tags"})
    record = _items(page)[0]

    assert record["permission_tags"] == []
    assert record["permission_status"] == "denied"
    assert record["permission_reason"] == "missing_permission_tags"
    assert record["metadata_evidence_available"] is False


def test_abnormal_sync_and_checksum_states_stay_catalog_only() -> None:
    adapter = FakePlatformAssetCatalogAdapter()

    records = {
        item["source_id"]: item
        for item in _items(
            adapter.list_file_assets(
                filters={
                    "source_id": [
                        "file-101-checksum-missing",
                        "file-99-model-moved",
                        "file-99-stale-old-path",
                        "file-98-missing-file",
                    ]
                }
            )
        )
    }

    assert records["file-101-checksum-missing"]["checksum_status"] == "missing"
    assert records["file-99-model-moved"]["sync_status"] == "moved"
    assert records["file-99-stale-old-path"]["sync_status"] == "stale"
    assert records["file-98-missing-file"]["sync_status"] == "missing"
    assert all(record["citation_status"] == "metadata_only" for record in records.values())
    assert all(record["content_evidence_available"] is False for record in records.values())


def test_audit_event_checkpoint_uses_event_id_order() -> None:
    adapter = FakePlatformAssetCatalogAdapter()

    page = adapter.list_audit_events(after_event_id=1002, limit=2)
    events = _items(page)

    assert [event["event_id"] for event in events] == [1003, 1004]
    assert page.next_cursor is not None

    next_page = adapter.list_audit_events(after_event_id=1002, limit=2, cursor=page.next_cursor)
    assert [event["event_id"] for event in _items(next_page)] == [1005, 1006]


def test_unmatched_filter_returns_empty_page_with_correct_metadata() -> None:
    adapter = FakePlatformAssetCatalogAdapter()

    page = adapter.list_file_assets(filters={"source_id": "does-not-exist"})

    assert page.items == ()
    assert page.has_more is False
    assert page.next_cursor is None
    assert page.source_view == "FileAssetView"
    assert page.contract_version == VIEW_CONTRACT_VERSIONS["FileAssetView"]


def test_unknown_filter_field_returns_empty_page() -> None:
    adapter = FakePlatformAssetCatalogAdapter()

    page = adapter.list_file_assets(filters={"not_a_contract_field": None})

    assert page.items == ()
    assert page.has_more is False
    assert page.next_cursor is None


def test_cursor_source_view_mismatch_raises_value_error() -> None:
    adapter = FakePlatformAssetCatalogAdapter()

    first_page = adapter.list_file_assets(limit=1)
    assert first_page.next_cursor is not None

    with pytest.raises(ValueError, match="cursor source_view mismatch"):
        adapter.list_project_assets(cursor=first_page.next_cursor)


def test_cursor_filter_context_mismatch_raises_value_error() -> None:
    adapter = FakePlatformAssetCatalogAdapter()

    first_page = adapter.list_file_assets(limit=1, filters={"project_id": "101-C塔"})
    assert first_page.next_cursor is not None

    with pytest.raises(ValueError, match="cursor filter"):
        adapter.list_file_assets(
            cursor=first_page.next_cursor,
            filters={"project_id": "99-丰图既有建模项目"},
        )
