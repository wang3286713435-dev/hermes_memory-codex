from opensearchpy import OpenSearch

from app.core.config import settings
from app.core.logging import get_logger
from app.models.chunk import Chunk
from app.models.document import Document, DocumentVersion

logger = get_logger(__name__)


class OpenSearchChunkIndexer:
    def __init__(self) -> None:
        self.client = OpenSearch(settings.opensearch_url, timeout=5)
        self.index_name = settings.opensearch_index_chunks

    def ensure_index(self) -> None:
        if self.client.indices.exists(index=self.index_name):
            return
        self.client.indices.create(
            index=self.index_name,
            body={
                "settings": {
                    "index": {"number_of_shards": 1, "number_of_replicas": 0},
                    "analysis": {
                        "analyzer": {
                            "default": {"type": "standard"},
                        }
                    },
                },
                "mappings": {
                    "properties": {
                        "chunk_id": {"type": "keyword"},
                        "document_id": {"type": "keyword"},
                        "version_id": {"type": "keyword"},
                        "chunk_index": {"type": "integer"},
                        "text": {"type": "text"},
                        "source_name": {"type": "text", "fields": {"keyword": {"type": "keyword"}}},
                        "source_uri": {"type": "keyword"},
                        "source_type": {"type": "keyword"},
                        "document_type": {"type": "keyword"},
                        "version_name": {"type": "keyword"},
                        "heading_path": {"type": "keyword"},
                        "page_start": {"type": "integer"},
                        "page_end": {"type": "integer"},
                        "is_latest": {"type": "boolean"},
                        "status": {"type": "keyword"},
                        "metadata_json": {"type": "object", "enabled": True},
                        "vector": {"type": "float"},
                    }
                },
            },
        )

    def index_chunk(self, chunk: Chunk, document: Document, version: DocumentVersion) -> bool:
        self.ensure_index()
        body = {
            "chunk_id": chunk.id,
            "document_id": document.id,
            "version_id": version.id,
            "chunk_index": chunk.chunk_index,
            "text": chunk.text,
            "source_name": document.title,
            "source_uri": document.source_uri,
            "source_type": chunk.source_type,
            "document_type": document.document_type,
            "version_name": version.version_name,
            "heading_path": chunk.heading_path or [],
            "page_start": chunk.page_start,
            "page_end": chunk.page_end,
            "is_latest": version.is_latest,
            "status": document.status,
            "metadata_json": chunk.metadata_json or {},
            "vector": [],
        }
        self.client.index(index=self.index_name, id=chunk.id, body=body, refresh=True)
        logger.info("chunk_indexed", extra={"chunk_id": chunk.id})
        return True

