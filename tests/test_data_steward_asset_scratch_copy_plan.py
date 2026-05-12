from __future__ import annotations

import json
from pathlib import Path

from app.core.config import Settings
from app.services.asset_catalog import (
    AssetScratchCopyPlanner,
    AssetScratchCopyPlanRequest,
    FakePlatformAssetCatalogAdapter,
)

PROJECT_101 = "101-C\u5854"


def test_scratch_copy_feature_flags_default_off() -> None:
    assert Settings.model_fields["platform_asset_scratch_copy_enabled"].default is False
    assert Settings.model_fields["platform_asset_batch_copy_enabled"].default is False


def test_missing_project_scope_denies_without_creating_scratch_dir(tmp_path: Path) -> None:
    scratch_root = tmp_path / "scratch"
    plan = AssetScratchCopyPlanner(FakePlatformAssetCatalogAdapter()).plan(
        AssetScratchCopyPlanRequest(
            project_id=PROJECT_101,
            allowed_project_ids=(),
            scratch_root=scratch_root,
            job_id="job-missing-scope",
        )
    )

    assert plan.summary.dry_run is True
    assert plan.summary.would_copy_count == 0
    assert {item.reason for item in plan.items} == {"permission_scope_required"}
    assert all(item.action == "denied" for item in plan.items)
    assert plan.summary.local_copy_performed is False
    assert plan.summary.writes_nas is False
    assert scratch_root.exists() is False


def test_catalog_only_assets_are_not_copied_from_default_v1_1_fixtures(tmp_path: Path) -> None:
    plan = AssetScratchCopyPlanner(FakePlatformAssetCatalogAdapter()).plan(
        AssetScratchCopyPlanRequest(
            project_id=PROJECT_101,
            allowed_project_ids=(PROJECT_101,),
            scratch_root=tmp_path / "scratch",
            job_id="job-catalog-only",
        )
    )

    assert plan.summary.would_copy_count == 0
    assert plan.summary.skipped_requires_review_count == len(plan.items)
    assert {item.reason for item in plan.items} == {"catalog_only"}
    assert {item.source_id for item in plan.items} == {
        "file-101-model-index",
        "file-101-checksum-missing",
        "model-101-c-tower-ifc",
    }


def test_mixed_project_plan_only_copies_small_allowed_internal_files(tmp_path: Path) -> None:
    adapter = FakePlatformAssetCatalogAdapter(_fixture_dir(tmp_path))
    scratch_root = tmp_path / "scratch"
    plan = AssetScratchCopyPlanner(adapter).plan(
        AssetScratchCopyPlanRequest(
            project_id=PROJECT_101,
            allowed_project_ids=(PROJECT_101,),
            scratch_root=scratch_root,
            job_id="job-mixed",
        )
    )

    would_copy = [item for item in plan.items if item.action == "would_copy"]
    skipped = {item.source_id: item.reason for item in plan.items if item.action != "would_copy"}

    assert [item.source_id for item in would_copy] == [
        "file-copyable-docx",
        "file-copyable-pdf",
    ]
    assert skipped == {
        "file-catalog-only": "catalog_only",
        "file-unknown-confidentiality": "confidentiality_unknown",
        "file-large-xlsx": "size_limit_exceeded",
        "file-unsupported-rvt": "unsupported_file_type",
        "file-missing-locator": "missing_storage_locator",
        "file-archived": "lifecycle_not_active",
        "model-copyable-ifc": "unsupported_file_type",
    }
    assert plan.summary.would_copy_count == 2
    assert plan.summary.total_would_copy_bytes == 2_621_440
    assert plan.summary.local_copy_performed is False
    assert plan.to_dict()["items"][0]["scratch_path"].startswith(str(scratch_root))


def test_batch_limits_skip_later_copyable_files_without_touching_filesystem(tmp_path: Path) -> None:
    adapter = FakePlatformAssetCatalogAdapter(_fixture_dir(tmp_path))
    scratch_root = tmp_path / "scratch"
    plan = AssetScratchCopyPlanner(adapter).plan(
        AssetScratchCopyPlanRequest(
            project_id=PROJECT_101,
            allowed_project_ids=(PROJECT_101,),
            scratch_root=scratch_root,
            job_id="job-limited",
            max_files=1,
        )
    )

    assert [item.source_id for item in plan.items if item.action == "would_copy"] == [
        "file-copyable-docx"
    ]
    assert {
        item.source_id: item.reason
        for item in plan.items
        if item.source_id == "file-copyable-pdf"
    } == {"file-copyable-pdf": "batch_limit_exceeded"}
    assert scratch_root.exists() is False


def _fixture_dir(tmp_path: Path) -> Path:
    fixture_dir = tmp_path / "fixtures"
    fixture_dir.mkdir()
    _write_fixture(fixture_dir, "ProjectAssetView", [])
    _write_fixture(fixture_dir, "AuditEventView", [])
    _write_fixture(
        fixture_dir,
        "FileAssetView",
        [
            _file_row("file-copyable-docx", ".docx", 1_048_576, "preview_allowed"),
            _file_row("file-copyable-pdf", ".pdf", 1_572_864, "full_text_allowed"),
            _file_row("file-catalog-only", ".txt", 10_240, "catalog_only"),
            _file_row(
                "file-unknown-confidentiality",
                ".md",
                10_240,
                "preview_allowed",
                confidentiality_level="UNKNOWN",
            ),
            _file_row("file-large-xlsx", ".xlsx", 600 * 1024 * 1024, "preview_allowed"),
            _file_row("file-unsupported-rvt", ".rvt", 10_240, "preview_allowed"),
            _file_row(
                "file-missing-locator",
                ".docx",
                10_240,
                "preview_allowed",
                source_path="",
            ),
            _file_row(
                "file-archived",
                ".pdf",
                10_240,
                "preview_allowed",
                lifecycle_status="archived",
            ),
        ],
    )
    _write_fixture(
        fixture_dir,
        "ModelAssetView",
        [
            {
                **_file_row("model-copyable-ifc", ".ifc", 10_240, "preview_allowed"),
                "model_format": "IFC",
                "source_view_ref": "ModelAssetView",
            }
        ],
    )
    return fixture_dir


def _write_fixture(fixture_dir: Path, source_view: str, records: list[dict[str, object]]) -> None:
    file_name_by_view = {
        "ProjectAssetView": "project_asset_view.json",
        "FileAssetView": "file_asset_view.json",
        "ModelAssetView": "model_asset_view.json",
        "AuditEventView": "audit_event_view.json",
    }
    (fixture_dir / file_name_by_view[source_view]).write_text(
        json.dumps(
            {
                "source_view": source_view,
                "contract_version": "delivery_platform.asset_views.v1.1",
                "source_system": "delivery_platform",
                "records": records,
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )


def _file_row(
    source_id: str,
    file_ext: str,
    file_size: int,
    index_eligibility: str,
    *,
    confidentiality_level: str = "INTERNAL",
    lifecycle_status: str = "active",
    source_path: str | None = None,
) -> dict[str, object]:
    return {
        "source_id": source_id,
        "asset_uid": f"delivery_platform:{source_id}",
        "project_id": PROJECT_101,
        "project_scope": [PROJECT_101],
        "source_path": source_path if source_path is not None else f"nas://fake/{source_id}",
        "file_name": f"{source_id}{file_ext}",
        "file_ext": file_ext,
        "file_size": file_size,
        "content_hash": f"sha256:{source_id}",
        "created_at": "2026-05-12T00:00:00Z",
        "updated_at": "2026-05-12T00:00:00Z",
        "modified_at": "2026-05-12T00:00:00Z",
        "last_seen_at": "2026-05-12T00:00:00Z",
        "lifecycle_status": lifecycle_status,
        "sync_status": "active",
        "index_eligibility": index_eligibility,
        "citation_status": "metadata_only",
        "confidentiality_level": confidentiality_level,
        "permission_tags": [f"project:{PROJECT_101}", "role:delivery"],
    }
