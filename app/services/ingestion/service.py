from hashlib import sha256
from pathlib import Path
from datetime import datetime

from sqlalchemy.orm import Session

from app.core.logging import get_logger
from app.models.chunk import Chunk
from app.models.citation import CitationRecord
from app.models.document import Document, DocumentVersion
from app.models.ingestion import IngestionJob
from app.schemas.documents import DocumentIngestRequest
from app.services.chunking.service import ChunkingService
from app.services.indexing.dense import DenseChunkIndexer, DenseIndexingSummary
from app.services.indexing.opensearch import OpenSearchChunkIndexer
from app.services.meeting_transcript import enrich_meeting_metadata, is_meeting_document
from app.services.parsing.registry import ParserRegistry
from app.services.storage.service import StoredFile

logger = get_logger(__name__)


class DocumentIngestionService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.parsers = ParserRegistry()
        self.chunker = ChunkingService()

    def create_ingestion_job(self, request: DocumentIngestRequest) -> IngestionJob:
        job = IngestionJob(source_uri=request.source_uri, status="accepted", stage="created")
        self.db.add(job)
        self.db.commit()
        self.db.refresh(job)
        return job

    def ingest_uploaded_file(
        self,
        request: DocumentIngestRequest,
        stored_file: StoredFile,
    ) -> IngestionJob:
        job = IngestionJob(source_uri=request.source_uri, status="processing", stage="metadata")
        self.db.add(job)
        self.db.flush()

        file_bytes = stored_file.local_path.read_bytes()
        file_hash = sha256(file_bytes).hexdigest()
        title = request.title or stored_file.file_name
        document_type = request.document_type or self._document_type_from_path(stored_file.local_path)
        document = self._find_existing_document(title=title, source_type=request.source_type, document_type=document_type)
        duplicate_version = self._find_duplicate_version(document, file_hash)
        if duplicate_version is not None:
            job.document_id = document.id
            job.version_id = duplicate_version.id
            job.status = "completed"
            job.stage = "duplicate"
            job.chunk_count = self.db.query(Chunk).filter(Chunk.version_id == duplicate_version.id).count()
            job.indexed_count = job.chunk_count
            duplicate_version.metadata_json = {
                **(duplicate_version.metadata_json or {}),
                "duplicate_upload_detected": True,
                "last_duplicate_source_uri": request.source_uri,
            }
            self.db.commit()
            self.db.refresh(job)
            return job

        if document is None:
            document = Document(
                title=title,
                source_type=request.source_type,
                source_uri=request.source_uri,
                storage_uri=stored_file.storage_uri,
                document_type=document_type,
                owner_id=request.owner_id,
                department_id=request.department_id,
                project_id=request.project_id,
                confidentiality_level=request.confidentiality_level,
                status="active",
                metadata_json={"content_type": stored_file.content_type},
            )
            self.db.add(document)
            self.db.flush()
        else:
            document.source_uri = request.source_uri
            document.storage_uri = stored_file.storage_uri
            document.status = "active"
            document.metadata_json = {
                **(document.metadata_json or {}),
                "content_type": stored_file.content_type,
                "version_match_status": "matched_by_title_source_type_document_type",
            }

        previous_latest_versions = (
            self.db.query(DocumentVersion)
            .filter(DocumentVersion.document_id == document.id)
            .filter(DocumentVersion.is_latest.is_(True))
            .all()
        )
        next_version_number = self._next_version_number(document.id)
        version = DocumentVersion(
            document_id=document.id,
            version_name=f"v{next_version_number}",
            version_number=str(next_version_number),
            file_hash=file_hash,
            is_latest=True,
            parse_status="processing",
            metadata_json={"version_status": "active"},
        )
        self.db.add(version)
        self.db.flush()
        self._mark_previous_versions_superseded(previous_latest_versions, superseded_by_version_id=version.id)
        document.metadata_json = {
            **(document.metadata_json or {}),
            "current_version_id": version.id,
        }

        job.document_id = document.id
        job.version_id = version.id

        try:
            job.stage = "parse"
            parsed = self.parsers.get_parser(stored_file.local_path).parse(stored_file.local_path)
            version.content_hash = sha256(
                "\n".join(block.text for block in parsed.blocks).encode("utf-8")
            ).hexdigest()
            version.metadata_json = parsed.metadata

            job.stage = "chunk"
            chunk_candidates = self.chunker.chunk(parsed)
            chunks: list[Chunk] = []
            is_meeting_scope = is_meeting_document(
                source_type=document.source_type,
                document_type=document.document_type,
                title=document.title,
                source_uri=document.source_uri,
            )
            for index, candidate in enumerate(chunk_candidates):
                metadata = candidate.metadata
                if is_meeting_scope:
                    metadata = enrich_meeting_metadata(
                        text=candidate.text,
                        metadata=candidate.metadata,
                        source_type=document.source_type,
                        document_type=document.document_type,
                        source_name=document.title,
                        source_uri=document.source_uri,
                        source_location=" > ".join(candidate.title_path or candidate.section_path or [])
                        or f"chunk_index={index}",
                    )
                chunk = Chunk(
                    document_id=document.id,
                    version_id=version.id,
                    chunk_index=index,
                    text=candidate.text,
                    heading_path=candidate.title_path,
                    title_path=candidate.title_path,
                    section_path=candidate.section_path,
                    page_start=candidate.page_start,
                    page_end=candidate.page_end,
                    char_count=len(candidate.text),
                    token_count=len(candidate.text),
                    content_hash=candidate.content_hash,
                    source_type=document.source_type,
                    metadata_json=metadata,
                    permission_tags=request.permission_tags,
                )
                self.db.add(chunk)
                chunks.append(chunk)
            self.db.flush()

            if is_meeting_scope:
                for chunk in chunks:
                    chunk.metadata_json = {
                        **(chunk.metadata_json or {}),
                        "source_chunk_id": chunk.id,
                    }
                self.db.flush()

            for chunk in chunks:
                self.db.add(
                    CitationRecord(
                        document_id=document.id,
                        version_id=version.id,
                        chunk_id=chunk.id,
                        source_name=document.title,
                        source_uri=document.source_uri,
                        page_start=chunk.page_start,
                        page_end=chunk.page_end,
                        heading_path=chunk.heading_path,
                        quote_text=chunk.text[:500],
                    )
                )

            job.stage = "index"
            indexed_count = self._index_chunks(chunks, document, version)
            for chunk in chunks[:indexed_count]:
                chunk.sparse_id = chunk.id
            dense_summary = self._index_dense_chunks(chunks, document, version)
            version.metadata_json = {
                **(version.metadata_json or {}),
                "version_status": "active",
                "dense_ingestion": dense_summary.as_dict(),
            }
            self._sync_superseded_indexes(previous_latest_versions)

            version.parse_status = "completed"
            job.status = "completed"
            job.stage = "completed"
            job.chunk_count = len(chunks)
            job.indexed_count = indexed_count
            self.db.commit()
            self.db.refresh(job)
            return job
        except Exception as exc:
            logger.exception("document_ingestion_failed")
            self._restore_previous_versions(previous_latest_versions)
            version.parse_status = "failed"
            version.error_message = str(exc)
            job.status = "failed"
            job.stage = "failed"
            job.error_message = str(exc)
            self.db.commit()
            self.db.refresh(job)
            return job

    def _index_chunks(
        self,
        chunks: list[Chunk],
        document: Document,
        version: DocumentVersion,
    ) -> int:
        try:
            indexer = OpenSearchChunkIndexer()
            indexed_count = 0
            for chunk in chunks:
                if indexer.index_chunk(chunk, document, version):
                    indexed_count += 1
            return indexed_count
        except Exception:
            logger.exception("opensearch_indexing_failed_falling_back_to_db_only")
            return 0

    def _index_dense_chunks(
        self,
        chunks: list[Chunk],
        document: Document,
        version: DocumentVersion,
    ) -> DenseIndexingSummary:
        try:
            return DenseChunkIndexer().index_chunks(chunks, document, version)
        except Exception as exc:  # noqa: BLE001 - dense indexing must fail open.
            logger.exception(
                "dense_indexing_failed_falling_back_to_sparse_only",
                extra={
                    "document_id": document.id,
                    "version_id": version.id,
                    "dense_ingestion_status": "failed",
                    "dense_failed_count": len(chunks),
                },
            )
            return DenseIndexingSummary(
                status="failed",
                failed_count=len(chunks),
                embedding_model=None,
                embedding_dimension=None,
                qdrant_collection=None,
                errors=[{"reason": "dense_indexer_exception", "error": str(exc)}],
            )

    def _document_type_from_path(self, path: Path) -> str:
        suffix = path.suffix.lower().lstrip(".")
        return suffix or "unknown"

    def _find_existing_document(
        self,
        *,
        title: str,
        source_type: str,
        document_type: str,
    ) -> Document | None:
        normalized_title = self._normalize_title(title)
        candidates = (
            self.db.query(Document)
            .filter(Document.status == "active")
            .filter(Document.source_type == source_type)
            .filter(Document.document_type == document_type)
            .all()
        )
        for candidate in candidates:
            if self._normalize_title(candidate.title) == normalized_title:
                return candidate
        return None

    def _find_duplicate_version(self, document: Document | None, file_hash: str) -> DocumentVersion | None:
        if document is None:
            return None
        return (
            self.db.query(DocumentVersion)
            .filter(DocumentVersion.document_id == document.id)
            .filter(DocumentVersion.file_hash == file_hash)
            .first()
        )

    def _next_version_number(self, document_id: str) -> int:
        count = self.db.query(DocumentVersion).filter(DocumentVersion.document_id == document_id).count()
        return count + 1

    def _mark_previous_versions_superseded(
        self,
        versions: list[DocumentVersion],
        *,
        superseded_by_version_id: str,
    ) -> None:
        now = datetime.utcnow()
        for previous in versions:
            previous.is_latest = False
            previous.expired_at = now
            previous.metadata_json = {
                **(previous.metadata_json or {}),
                "version_status": "superseded",
                "superseded_by_version_id": superseded_by_version_id,
            }

    def _sync_superseded_indexes(self, versions: list[DocumentVersion]) -> None:
        if not versions:
            return
        for previous in versions:
            try:
                OpenSearchChunkIndexer().mark_version_latest(
                    previous.id,
                    is_latest=False,
                    document_id=previous.document_id,
                    superseded_by_version_id=(previous.metadata_json or {}).get("superseded_by_version_id"),
                )
            except Exception:
                logger.warning(
                    "opensearch_superseded_version_update_failed",
                    extra={"version_id": previous.id},
                    exc_info=True,
                )
            try:
                DenseChunkIndexer().mark_version_latest(
                    previous.id,
                    is_latest=False,
                    document_id=previous.document_id,
                    superseded_by_version_id=(previous.metadata_json or {}).get("superseded_by_version_id"),
                )
            except Exception:
                logger.warning(
                    "qdrant_superseded_version_update_failed",
                    extra={"version_id": previous.id},
                    exc_info=True,
                )

    def _normalize_title(self, title: str) -> str:
        return Path(title or "").stem.strip().lower().replace(" ", "")

    def _restore_previous_versions(self, versions: list[DocumentVersion]) -> None:
        for previous in versions:
            previous.is_latest = True
            previous.expired_at = None
            metadata = dict(previous.metadata_json or {})
            metadata.pop("superseded_by_version_id", None)
            metadata["version_status"] = "active"
            previous.metadata_json = metadata
