from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

from app.core.config import settings
from app.core.logging import get_logger
from app.models.chunk import Chunk
from app.models.document import Document, DocumentVersion
from app.services.embedding import AliyunTextEmbeddingV3
from app.services.retrieval.dense import QdrantDenseRetriever

logger = get_logger(__name__)


@dataclass
class DenseIndexingSummary:
    status: str
    indexed_count: int = 0
    failed_count: int = 0
    skipped_count: int = 0
    embedding_model: str | None = None
    embedding_dimension: int | None = None
    qdrant_collection: str | None = None
    errors: list[dict[str, Any]] = field(default_factory=list)

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


class DenseChunkIndexer:
    """Indexes chunks into Qdrant without blocking sparse ingestion on failure."""

    def __init__(
        self,
        embedding: AliyunTextEmbeddingV3 | None = None,
        qdrant: QdrantDenseRetriever | None = None,
    ) -> None:
        self.embedding = embedding or AliyunTextEmbeddingV3()
        self.qdrant = qdrant or QdrantDenseRetriever(embedding=self.embedding)

    def index_chunks(
        self,
        chunks: list[Chunk],
        document: Document,
        version: DocumentVersion,
    ) -> DenseIndexingSummary:
        if settings.vector_store_provider != "qdrant":
            return DenseIndexingSummary(
                status="skipped",
                skipped_count=len(chunks),
                embedding_model=settings.aliyun_embedding_model,
                embedding_dimension=settings.aliyun_embedding_dimension,
                qdrant_collection=settings.qdrant_collection,
                errors=[{"reason": "vector_store_provider_not_qdrant", "provider": settings.vector_store_provider}],
            )

        summary = DenseIndexingSummary(
            status="executed",
            embedding_model=settings.aliyun_embedding_model,
            embedding_dimension=settings.aliyun_embedding_dimension,
            qdrant_collection=settings.qdrant_collection,
        )
        for chunk in chunks:
            try:
                embedding_outcome = self.embedding.embed_query(chunk.text)
                if embedding_outcome.vector is None:
                    summary.failed_count += 1
                    summary.errors.append(
                        {
                            "chunk_id": chunk.id,
                            "reason": "embedding_unavailable",
                            "embedding_status": embedding_outcome.status,
                            "trace": embedding_outcome.trace,
                        }
                    )
                    continue

                self.qdrant.upsert_chunk(
                    chunk_id=chunk.id,
                    vector=embedding_outcome.vector,
                    payload=self._payload_for_chunk(chunk, document, version),
                )
                chunk.embedding_id = chunk.id
                summary.indexed_count += 1
            except Exception as exc:  # noqa: BLE001 - fail-open by design.
                summary.failed_count += 1
                summary.errors.append({"chunk_id": chunk.id, "reason": "dense_upsert_failed", "error": str(exc)})

        if summary.indexed_count and summary.failed_count:
            summary.status = "partial"
        elif summary.failed_count and not summary.indexed_count:
            summary.status = "failed"
        elif not chunks:
            summary.status = "skipped"

        logger.info(
            "dense_ingestion_completed",
            extra={
                "document_id": document.id,
                "version_id": version.id,
                "dense_ingestion_status": summary.status,
                "dense_indexed_count": summary.indexed_count,
                "dense_failed_count": summary.failed_count,
            },
        )
        return summary

    def _payload_for_chunk(self, chunk: Chunk, document: Document, version: DocumentVersion) -> dict[str, Any]:
        return {
            "document_id": document.id,
            "version_id": version.id,
            "chunk_id": chunk.id,
            "source_type": chunk.source_type,
            "document_type": document.document_type,
            "title": document.title,
            "source_name": document.title,
            "source_uri": document.source_uri,
            "chunk_index": chunk.chunk_index,
            "is_latest": version.is_latest,
            "text": chunk.text,
            "heading_path": chunk.heading_path or [],
            "title_path": chunk.title_path or [],
            "section_path": chunk.section_path or [],
            "page_start": chunk.page_start,
            "page_end": chunk.page_end,
            "metadata_json": chunk.metadata_json or {},
            "metadata": chunk.metadata_json or {},
        }
