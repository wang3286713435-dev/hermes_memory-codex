from hashlib import sha256
from pathlib import Path

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

        document = Document(
            title=request.title or stored_file.file_name,
            source_type=request.source_type,
            source_uri=request.source_uri,
            storage_uri=stored_file.storage_uri,
            document_type=request.document_type or self._document_type_from_path(stored_file.local_path),
            owner_id=request.owner_id,
            department_id=request.department_id,
            project_id=request.project_id,
            confidentiality_level=request.confidentiality_level,
            status="active",
            metadata_json={"content_type": stored_file.content_type},
        )
        self.db.add(document)
        self.db.flush()

        file_bytes = stored_file.local_path.read_bytes()
        version = DocumentVersion(
            document_id=document.id,
            version_name="v1",
            version_number="1",
            file_hash=sha256(file_bytes).hexdigest(),
            is_latest=True,
            parse_status="processing",
            metadata_json={},
        )
        self.db.add(version)
        self.db.flush()

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
                "dense_ingestion": dense_summary.as_dict(),
            }

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
