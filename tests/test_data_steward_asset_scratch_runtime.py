from __future__ import annotations

import hashlib
from pathlib import Path

from app.services.asset_catalog import (
    AssetScratchCopyPlan,
    AssetScratchCopyPlanItem,
    AssetScratchCopyPlanRequest,
    AssetScratchCopyPlanSummary,
    AssetScratchRuntime,
    AssetScratchRuntimeOptions,
)


def test_runtime_requires_authorization_and_feature_flags(tmp_path: Path) -> None:
    source = tmp_path / "source.docx"
    source.write_bytes(b"fixture-doc")
    plan = _plan(tmp_path, [_copy_item(tmp_path, "file-doc", source)])

    record = AssetScratchRuntime().run(
        plan,
        AssetScratchRuntimeOptions(
            runtime_authorized=False,
            scratch_copy_enabled=True,
            batch_copy_enabled=True,
        ),
    )

    assert record.summary.copied_count == 0
    assert record.summary.failed_count == 0
    assert record.summary.skipped_count == 1
    assert record.items[0].copy_status == "blocked_not_authorized"
    assert record.summary.local_copy_performed is False
    assert (tmp_path / "scratch").exists() is False

    disabled_record = AssetScratchRuntime().run(
        plan,
        AssetScratchRuntimeOptions(
            runtime_authorized=True,
            scratch_copy_enabled=False,
            batch_copy_enabled=True,
        ),
    )

    assert disabled_record.items[0].copy_status == "blocked_feature_disabled"
    assert disabled_record.summary.local_copy_performed is False
    assert (tmp_path / "scratch").exists() is False


def test_runtime_only_copies_would_copy_items(tmp_path: Path) -> None:
    source = tmp_path / "source.docx"
    source.write_bytes(b"fixture-doc")
    plan = _plan(
        tmp_path,
        [
            _copy_item(tmp_path, "file-doc", source),
            _skipped_item("file-bim"),
        ],
    )

    record = AssetScratchRuntime().run(plan, _enabled_options())

    assert [item.copy_status for item in record.items] == ["copied", "skipped_not_would_copy"]
    assert record.summary.copied_count == 1
    assert record.summary.skipped_count == 1
    assert record.summary.local_copy_performed is True
    assert not any((tmp_path / "scratch").rglob("*"))


def test_runtime_copies_local_fixture_computes_hash_and_cleans_up(tmp_path: Path) -> None:
    payload = b"office fixture"
    source = tmp_path / "source.docx"
    source.write_bytes(payload)
    plan = _plan(tmp_path, [_copy_item(tmp_path, "file-doc", source)])

    record = AssetScratchRuntime().run(plan, _enabled_options())
    item = record.items[0]

    assert item.copy_status == "copied"
    assert item.cleanup_status == "deleted"
    assert item.copied_hash == hashlib.sha256(payload).hexdigest()
    assert item.bytes_copied == len(payload)
    assert (tmp_path / "scratch").exists()
    assert not any((tmp_path / "scratch").rglob("*"))


def test_runtime_failed_copy_still_cleans_scratch(tmp_path: Path) -> None:
    missing_source = tmp_path / "missing.docx"
    plan = _plan(tmp_path, [_copy_item(tmp_path, "file-doc", missing_source)])

    record = AssetScratchRuntime().run(plan, _enabled_options())
    item = record.items[0]

    assert item.copy_status == "copy_failed"
    assert item.cleanup_status in {"nothing_to_cleanup", "deleted"}
    assert item.copied_hash is None
    assert record.summary.failed_count == 1
    assert not any((tmp_path / "scratch").rglob("*"))


def test_runtime_record_is_sanitized_and_safety_flags_stay_false(tmp_path: Path) -> None:
    source = tmp_path / "sensitive" / "source.docx"
    source.parent.mkdir()
    source.write_bytes(b"fixture-doc")
    plan = _plan(tmp_path, [_copy_item(tmp_path, "file-doc", source)])

    record = AssetScratchRuntime().run(plan, _enabled_options())
    payload = record.to_dict()
    payload_text = str(payload)

    assert str(source) not in payload_text
    assert str(tmp_path / "scratch") not in payload_text
    assert "storage_locator" not in payload_text
    assert "scratch_path" not in payload_text
    assert payload["summary"]["parser_invoked"] is False
    assert payload["summary"]["writes_documents"] is False
    assert payload["summary"]["writes_chunks"] is False
    assert payload["summary"]["writes_opensearch"] is False
    assert payload["summary"]["writes_qdrant"] is False


def _enabled_options() -> AssetScratchRuntimeOptions:
    return AssetScratchRuntimeOptions(
        runtime_authorized=True,
        scratch_copy_enabled=True,
        batch_copy_enabled=True,
    )


def _plan(
    tmp_path: Path,
    items: list[AssetScratchCopyPlanItem],
) -> AssetScratchCopyPlan:
    request = AssetScratchCopyPlanRequest(
        project_id="101-C塔",
        allowed_project_ids=("101-C塔",),
        scratch_root=tmp_path / "scratch",
        job_id="job-runtime",
    )
    would_copy_count = sum(item.action == "would_copy" for item in items)
    return AssetScratchCopyPlan(
        request=request,
        items=tuple(items),
        summary=AssetScratchCopyPlanSummary(
            dry_run=True,
            item_count=len(items),
            would_copy_count=would_copy_count,
            denied_count=sum(item.action == "denied" for item in items),
            skipped_requires_review_count=sum(
                item.action == "skipped_requires_review" for item in items
            ),
            total_would_copy_bytes=sum(item.size_bytes or 0 for item in items),
            max_files=request.max_files,
            max_total_bytes=request.max_total_bytes,
            max_single_file_bytes=request.max_single_file_bytes,
            scratch_root=str(request.scratch_root),
            job_id=request.job_id,
        ),
    )


def _copy_item(
    tmp_path: Path,
    source_id: str,
    source: Path,
) -> AssetScratchCopyPlanItem:
    return AssetScratchCopyPlanItem(
        asset_uid=f"delivery_platform:{source_id}",
        source_view="FileAssetView",
        source_id=source_id,
        project_id="101-C塔",
        action="would_copy",
        reason="copy_eligible",
        file_ext=".docx",
        size_bytes=1024,
        index_eligibility="preview_allowed",
        lifecycle_status="active",
        confidentiality_level="INTERNAL",
        storage_locator=source.as_uri(),
        scratch_path=str(tmp_path / "scratch" / "job-runtime" / f"{source_id}.docx"),
        content_hash="sha256:fixture",
    )


def _skipped_item(source_id: str) -> AssetScratchCopyPlanItem:
    return AssetScratchCopyPlanItem(
        asset_uid=f"delivery_platform:{source_id}",
        source_view="ModelAssetView",
        source_id=source_id,
        project_id="101-C塔",
        action="skipped_requires_review",
        reason="unsupported_file_type",
        file_ext=".ifc",
        size_bytes=1024,
        index_eligibility="preview_allowed",
        lifecycle_status="active",
        confidentiality_level="INTERNAL",
        storage_locator=None,
        scratch_path=None,
        content_hash=None,
    )
