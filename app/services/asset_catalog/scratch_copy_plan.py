from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Literal, Protocol

from app.services.asset_catalog.contracts import AssetViewPage, AssetViewRecord, SourceView

AssetScratchCopyAction = Literal["would_copy", "skipped_requires_review", "denied"]

COPY_ELIGIBLE_INDEX_VALUES = frozenset(
    {"preview_allowed", "full_text_allowed", "semantic_allowed"}
)
COPY_ELIGIBLE_EXTENSIONS = (
    ".doc",
    ".docx",
    ".pdf",
    ".ppt",
    ".pptx",
    ".txt",
    ".md",
    ".csv",
    ".xls",
    ".xlsx",
)
DEFAULT_SCRATCH_ROOT = Path("/Users/hermes/runtime/nas_scratch")
DEFAULT_MAX_FILES = 10
DEFAULT_MAX_TOTAL_BYTES = 2 * 1024 * 1024 * 1024
DEFAULT_MAX_SINGLE_FILE_BYTES = 512 * 1024 * 1024


class AssetCatalogCopyPlanAdapter(Protocol):
    def list_file_assets(self) -> AssetViewPage: ...

    def list_model_assets(self) -> AssetViewPage: ...


@dataclass(frozen=True)
class AssetScratchCopyPlanRequest:
    project_id: str
    allowed_project_ids: tuple[str, ...]
    scratch_root: Path | str = DEFAULT_SCRATCH_ROOT
    job_id: str = "dry-run"
    max_files: int = DEFAULT_MAX_FILES
    max_total_bytes: int = DEFAULT_MAX_TOTAL_BYTES
    max_single_file_bytes: int = DEFAULT_MAX_SINGLE_FILE_BYTES
    allowed_extensions: tuple[str, ...] = COPY_ELIGIBLE_EXTENSIONS


@dataclass(frozen=True)
class AssetScratchCopyPlanItem:
    asset_uid: str
    source_view: SourceView
    source_id: str
    project_id: str
    action: AssetScratchCopyAction
    reason: str
    file_ext: str | None
    size_bytes: int | None
    index_eligibility: str
    lifecycle_status: str
    confidentiality_level: str
    storage_locator: str | None
    scratch_path: str | None
    content_hash: str | None
    local_copy_performed: bool = False
    writes_nas: bool = False
    writes_documents: bool = False
    writes_chunks: bool = False
    writes_opensearch: bool = False
    writes_qdrant: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "asset_uid": self.asset_uid,
            "source_view": self.source_view,
            "source_id": self.source_id,
            "project_id": self.project_id,
            "action": self.action,
            "reason": self.reason,
            "file_ext": self.file_ext,
            "size_bytes": self.size_bytes,
            "index_eligibility": self.index_eligibility,
            "lifecycle_status": self.lifecycle_status,
            "confidentiality_level": self.confidentiality_level,
            "storage_locator_present": bool(self.storage_locator),
            "scratch_path": self.scratch_path,
            "content_hash_present": bool(self.content_hash),
            "local_copy_performed": self.local_copy_performed,
            "writes_nas": self.writes_nas,
            "writes_documents": self.writes_documents,
            "writes_chunks": self.writes_chunks,
            "writes_opensearch": self.writes_opensearch,
            "writes_qdrant": self.writes_qdrant,
        }


@dataclass(frozen=True)
class AssetScratchCopyPlanSummary:
    dry_run: bool
    item_count: int
    would_copy_count: int
    denied_count: int
    skipped_requires_review_count: int
    total_would_copy_bytes: int
    max_files: int
    max_total_bytes: int
    max_single_file_bytes: int
    scratch_root: str
    job_id: str
    local_copy_performed: bool = False
    writes_nas: bool = False
    writes_documents: bool = False
    writes_chunks: bool = False
    writes_opensearch: bool = False
    writes_qdrant: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "dry_run": self.dry_run,
            "item_count": self.item_count,
            "would_copy_count": self.would_copy_count,
            "denied_count": self.denied_count,
            "skipped_requires_review_count": self.skipped_requires_review_count,
            "total_would_copy_bytes": self.total_would_copy_bytes,
            "max_files": self.max_files,
            "max_total_bytes": self.max_total_bytes,
            "max_single_file_bytes": self.max_single_file_bytes,
            "scratch_root": self.scratch_root,
            "job_id": self.job_id,
            "local_copy_performed": self.local_copy_performed,
            "writes_nas": self.writes_nas,
            "writes_documents": self.writes_documents,
            "writes_chunks": self.writes_chunks,
            "writes_opensearch": self.writes_opensearch,
            "writes_qdrant": self.writes_qdrant,
        }


@dataclass(frozen=True)
class AssetScratchCopyPlan:
    request: AssetScratchCopyPlanRequest
    items: tuple[AssetScratchCopyPlanItem, ...]
    summary: AssetScratchCopyPlanSummary

    def to_dict(self) -> dict[str, Any]:
        return {
            "request": {
                "project_id": self.request.project_id,
                "allowed_project_ids": list(self.request.allowed_project_ids),
                "scratch_root": str(self.request.scratch_root),
                "job_id": self.request.job_id,
            },
            "summary": self.summary.to_dict(),
            "items": [item.to_dict() for item in self.items],
        }


class AssetScratchCopyPlanner:
    """Dry-run NAS scratch copy planner over authorized asset catalog metadata."""

    def __init__(self, adapter: AssetCatalogCopyPlanAdapter) -> None:
        self.adapter = adapter

    def plan(self, request: AssetScratchCopyPlanRequest) -> AssetScratchCopyPlan:
        if request.max_files <= 0:
            raise ValueError("max_files must be positive")
        if request.max_total_bytes <= 0:
            raise ValueError("max_total_bytes must be positive")
        if request.max_single_file_bytes <= 0:
            raise ValueError("max_single_file_bytes must be positive")

        items: list[AssetScratchCopyPlanItem] = []
        would_copy_count = 0
        total_would_copy_bytes = 0
        for record in self._candidate_records(request.project_id):
            item = self._item_for_record(
                record=record,
                request=request,
                current_would_copy_count=would_copy_count,
                current_total_would_copy_bytes=total_would_copy_bytes,
            )
            items.append(item)
            if item.action == "would_copy":
                would_copy_count += 1
                total_would_copy_bytes += item.size_bytes or 0

        summary = AssetScratchCopyPlanSummary(
            dry_run=True,
            item_count=len(items),
            would_copy_count=would_copy_count,
            denied_count=sum(item.action == "denied" for item in items),
            skipped_requires_review_count=sum(
                item.action == "skipped_requires_review" for item in items
            ),
            total_would_copy_bytes=total_would_copy_bytes,
            max_files=request.max_files,
            max_total_bytes=request.max_total_bytes,
            max_single_file_bytes=request.max_single_file_bytes,
            scratch_root=str(request.scratch_root),
            job_id=request.job_id,
        )
        return AssetScratchCopyPlan(request=request, items=tuple(items), summary=summary)

    def _candidate_records(self, project_id: str) -> tuple[AssetViewRecord, ...]:
        records = [
            *self.adapter.list_file_assets().items,
            *self.adapter.list_model_assets().items,
        ]
        return tuple(record for record in records if record.project_id == project_id)

    def _item_for_record(
        self,
        *,
        record: AssetViewRecord,
        request: AssetScratchCopyPlanRequest,
        current_would_copy_count: int,
        current_total_would_copy_bytes: int,
    ) -> AssetScratchCopyPlanItem:
        reason = self._skip_reason(record, request)
        action: AssetScratchCopyAction
        if reason == "permission_scope_required" or reason == "permission_denied":
            action = "denied"
        elif reason is not None:
            action = "skipped_requires_review"
        else:
            size_bytes = self._size_bytes(record)
            if current_would_copy_count >= request.max_files:
                action = "skipped_requires_review"
                reason = "batch_limit_exceeded"
            elif current_total_would_copy_bytes + size_bytes > request.max_total_bytes:
                action = "skipped_requires_review"
                reason = "total_size_limit_exceeded"
            else:
                action = "would_copy"
                reason = "copy_eligible"

        return AssetScratchCopyPlanItem(
            asset_uid=record.asset_uid,
            source_view=record.source_view,
            source_id=record.source_id,
            project_id=record.project_id or "",
            action=action,
            reason=reason,
            file_ext=self._file_ext(record),
            size_bytes=self._size_bytes(record),
            index_eligibility=record.index_eligibility,
            lifecycle_status=record.lifecycle_status,
            confidentiality_level=record.confidentiality_level,
            storage_locator=self._storage_locator(record),
            scratch_path=(
                self._scratch_path(record, request)
                if action == "would_copy"
                else None
            ),
            content_hash=record.row.get("content_hash"),
        )

    def _skip_reason(
        self,
        record: AssetViewRecord,
        request: AssetScratchCopyPlanRequest,
    ) -> str | None:
        if record.project_id not in set(request.allowed_project_ids):
            return "permission_scope_required"
        if record.permission_status != "allowed":
            return "permission_denied"
        if record.lifecycle_status != "active" or record.sync_status != "active":
            return "lifecycle_not_active"
        if not self._storage_locator(record):
            return "missing_storage_locator"
        if record.index_eligibility not in COPY_ELIGIBLE_INDEX_VALUES:
            return "catalog_only"
        if record.confidentiality_level == "UNKNOWN":
            return "confidentiality_unknown"
        if self._file_ext(record) not in self._allowed_extensions(request):
            return "unsupported_file_type"
        if self._size_bytes(record) > request.max_single_file_bytes:
            return "size_limit_exceeded"
        return None

    def _allowed_extensions(self, request: AssetScratchCopyPlanRequest) -> set[str]:
        return {self._normalize_extension(item) for item in request.allowed_extensions}

    def _file_ext(self, record: AssetViewRecord) -> str | None:
        raw_extension = record.row.get("file_ext")
        if raw_extension is None:
            return None
        return self._normalize_extension(str(raw_extension))

    def _normalize_extension(self, value: str) -> str:
        normalized = value.strip().lower()
        if not normalized:
            return ""
        return normalized if normalized.startswith(".") else f".{normalized}"

    def _size_bytes(self, record: AssetViewRecord) -> int:
        raw_size = record.row.get("file_size") or record.row.get("size_bytes") or 0
        return int(raw_size)

    def _storage_locator(self, record: AssetViewRecord) -> str | None:
        raw_locator = record.row.get("source_path") or record.row.get("storage_path")
        if raw_locator is None:
            return None
        locator = str(raw_locator).strip()
        return locator or None

    def _scratch_path(
        self,
        record: AssetViewRecord,
        request: AssetScratchCopyPlanRequest,
    ) -> str:
        file_ext = self._file_ext(record) or ""
        safe_source_id = "".join(
            character if character.isalnum() or character in {"-", "_"} else "_"
            for character in record.source_id
        )
        return str(Path(request.scratch_root) / request.job_id / f"{safe_source_id}{file_ext}")
