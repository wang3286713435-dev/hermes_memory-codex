from __future__ import annotations

import hashlib
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Literal
from urllib.parse import unquote, urlparse

from app.services.asset_catalog.scratch_copy_plan import (
    AssetScratchCopyPlan,
    AssetScratchCopyPlanItem,
)

AssetScratchRuntimeCopyStatus = Literal[
    "copied",
    "skipped_not_would_copy",
    "blocked_not_authorized",
    "blocked_feature_disabled",
    "copy_failed",
]
AssetScratchRuntimeCleanupStatus = Literal[
    "deleted",
    "nothing_to_cleanup",
    "cleanup_failed",
]


@dataclass(frozen=True)
class AssetScratchRuntimeOptions:
    runtime_authorized: bool = False
    scratch_copy_enabled: bool = False
    batch_copy_enabled: bool = False


@dataclass(frozen=True)
class AssetScratchRuntimeRunItem:
    asset_uid: str
    source_view: str
    source_id: str
    project_id: str
    content_hash_present: bool
    copied_hash: str | None
    copy_status: AssetScratchRuntimeCopyStatus
    cleanup_status: AssetScratchRuntimeCleanupStatus
    bytes_copied: int
    parser_invoked: bool = False
    writes_documents: bool = False
    writes_chunks: bool = False
    writes_opensearch: bool = False
    writes_qdrant: bool = False
    writes_minio: bool = False
    writes_db: bool = False
    writes_nas: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "asset_uid": self.asset_uid,
            "source_view": self.source_view,
            "source_id": self.source_id,
            "project_id": self.project_id,
            "content_hash_present": self.content_hash_present,
            "copied_hash": self.copied_hash,
            "copy_status": self.copy_status,
            "cleanup_status": self.cleanup_status,
            "bytes_copied": self.bytes_copied,
            "parser_invoked": self.parser_invoked,
            "writes_documents": self.writes_documents,
            "writes_chunks": self.writes_chunks,
            "writes_opensearch": self.writes_opensearch,
            "writes_qdrant": self.writes_qdrant,
            "writes_minio": self.writes_minio,
            "writes_db": self.writes_db,
            "writes_nas": self.writes_nas,
        }


@dataclass(frozen=True)
class AssetScratchRuntimeRunSummary:
    item_count: int
    copied_count: int
    skipped_count: int
    failed_count: int
    bytes_copied: int
    local_copy_performed: bool
    parser_invoked: bool = False
    writes_documents: bool = False
    writes_chunks: bool = False
    writes_opensearch: bool = False
    writes_qdrant: bool = False
    writes_minio: bool = False
    writes_db: bool = False
    writes_nas: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "item_count": self.item_count,
            "copied_count": self.copied_count,
            "skipped_count": self.skipped_count,
            "failed_count": self.failed_count,
            "bytes_copied": self.bytes_copied,
            "local_copy_performed": self.local_copy_performed,
            "parser_invoked": self.parser_invoked,
            "writes_documents": self.writes_documents,
            "writes_chunks": self.writes_chunks,
            "writes_opensearch": self.writes_opensearch,
            "writes_qdrant": self.writes_qdrant,
            "writes_minio": self.writes_minio,
            "writes_db": self.writes_db,
            "writes_nas": self.writes_nas,
        }


@dataclass(frozen=True)
class AssetScratchRuntimeRunRecord:
    plan_job_id: str
    project_id: str
    summary: AssetScratchRuntimeRunSummary
    items: tuple[AssetScratchRuntimeRunItem, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "plan_job_id": self.plan_job_id,
            "project_id": self.project_id,
            "summary": self.summary.to_dict(),
            "items": [item.to_dict() for item in self.items],
        }


class AssetScratchRuntime:
    """Controlled local fixture scratch-copy runtime.

    This runtime intentionally copies only local paths or file:// fixtures. It
    never scans NAS, calls parsers, or writes memory/index/object stores.
    """

    def run(
        self,
        plan: AssetScratchCopyPlan,
        options: AssetScratchRuntimeOptions,
    ) -> AssetScratchRuntimeRunRecord:
        run_items = tuple(self._run_item(item, options) for item in plan.items)
        summary = AssetScratchRuntimeRunSummary(
            item_count=len(run_items),
            copied_count=sum(item.copy_status == "copied" for item in run_items),
            skipped_count=sum(
                item.copy_status
                in {
                    "skipped_not_would_copy",
                    "blocked_not_authorized",
                    "blocked_feature_disabled",
                }
                for item in run_items
            ),
            failed_count=sum(item.copy_status == "copy_failed" for item in run_items),
            bytes_copied=sum(item.bytes_copied for item in run_items),
            local_copy_performed=any(item.copy_status == "copied" for item in run_items),
        )
        return AssetScratchRuntimeRunRecord(
            plan_job_id=plan.request.job_id,
            project_id=plan.request.project_id,
            summary=summary,
            items=run_items,
        )

    def _run_item(
        self,
        item: AssetScratchCopyPlanItem,
        options: AssetScratchRuntimeOptions,
    ) -> AssetScratchRuntimeRunItem:
        if item.action != "would_copy":
            return self._record_item(item, "skipped_not_would_copy", "nothing_to_cleanup")
        if not options.runtime_authorized:
            return self._record_item(item, "blocked_not_authorized", "nothing_to_cleanup")
        if not options.scratch_copy_enabled or not options.batch_copy_enabled:
            return self._record_item(item, "blocked_feature_disabled", "nothing_to_cleanup")

        target_path = Path(item.scratch_path) if item.scratch_path else None
        source_path = self._local_source_path(item.storage_locator)
        if target_path is None or source_path is None:
            return self._record_item(item, "copy_failed", "nothing_to_cleanup")

        copied_hash: str | None = None
        bytes_copied = 0
        copy_status: AssetScratchRuntimeCopyStatus = "copy_failed"
        try:
            if not source_path.is_file():
                return self._record_item(item, "copy_failed", "nothing_to_cleanup")

            target_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source_path, target_path)
            copied_hash = self._sha256(target_path)
            bytes_copied = target_path.stat().st_size
            copy_status = "copied"
        finally:
            cleanup_status = self._cleanup(target_path)

        return self._record_item(
            item,
            copy_status,
            cleanup_status,
            copied_hash=copied_hash,
            bytes_copied=bytes_copied,
        )

    def _record_item(
        self,
        item: AssetScratchCopyPlanItem,
        copy_status: AssetScratchRuntimeCopyStatus,
        cleanup_status: AssetScratchRuntimeCleanupStatus,
        *,
        copied_hash: str | None = None,
        bytes_copied: int = 0,
    ) -> AssetScratchRuntimeRunItem:
        return AssetScratchRuntimeRunItem(
            asset_uid=item.asset_uid,
            source_view=item.source_view,
            source_id=item.source_id,
            project_id=item.project_id,
            content_hash_present=bool(item.content_hash),
            copied_hash=copied_hash,
            copy_status=copy_status,
            cleanup_status=cleanup_status,
            bytes_copied=bytes_copied,
        )

    def _local_source_path(self, storage_locator: str | None) -> Path | None:
        if not storage_locator:
            return None
        parsed = urlparse(storage_locator)
        if parsed.scheme == "file":
            return Path(unquote(parsed.path))
        if parsed.scheme:
            return None
        return Path(storage_locator)

    def _sha256(self, path: Path) -> str:
        digest = hashlib.sha256()
        with path.open("rb") as file:
            for chunk in iter(lambda: file.read(1024 * 1024), b""):
                digest.update(chunk)
        return digest.hexdigest()

    def _cleanup(self, target_path: Path | None) -> AssetScratchRuntimeCleanupStatus:
        if target_path is None or not target_path.exists():
            return "nothing_to_cleanup"
        try:
            target_path.unlink()
            self._remove_empty_dir(target_path.parent)
            return "deleted"
        except OSError:
            return "cleanup_failed"

    def _remove_empty_dir(self, path: Path) -> None:
        if not path.exists():
            return
        try:
            path.rmdir()
        except OSError:
            return
