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
        self._filter_field_cache: dict[str, str] = {}

    def ensure_index(self) -> None:
        if self.client.indices.exists(index=self.index_name):
            self._ensure_mapping_fields()
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
                        "title_path": {"type": "keyword"},
                        "section_path": {"type": "keyword"},
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
        self._ensure_mapping_fields()

    def _ensure_mapping_fields(self) -> None:
        mapping = self.client.indices.get_mapping(index=self.index_name)
        props = ((mapping.get(self.index_name) or {}).get("mappings") or {}).get("properties") or {}
        missing: dict[str, dict] = {}
        for field in ("title_path", "section_path"):
            if field not in props:
                missing[field] = {"type": "keyword"}
        if missing:
            self.client.indices.put_mapping(index=self.index_name, body={"properties": missing})

    def _resolve_filter_field(self, field: str) -> str:
        cached = self._filter_field_cache.get(field)
        if cached:
            return cached
        try:
            mapping = self.client.indices.get_mapping(index=self.index_name)
            props = ((mapping.get(self.index_name) or {}).get("mappings") or {}).get("properties") or {}
            field_def = props.get(field) or {}
            if field_def.get("type") == "text" and (field_def.get("fields") or {}).get("keyword"):
                resolved = f"{field}.keyword"
            else:
                resolved = field
        except Exception:
            resolved = field
        self._filter_field_cache[field] = resolved
        return resolved

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
            "title_path": chunk.title_path or [],
            "section_path": chunk.section_path or [],
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

    def mark_version_latest(
        self,
        version_id: str,
        *,
        is_latest: bool,
        document_id: str | None = None,
        superseded_by_version_id: str | None = None,
    ) -> None:
        self.ensure_index()
        script_lines = ["ctx._source.is_latest = params.is_latest"]
        params: dict = {"is_latest": is_latest}
        if not is_latest:
            script_lines.append("ctx._source.status = params.status")
            params["status"] = "superseded"
            if superseded_by_version_id:
                script_lines.append("ctx._source.superseded_by_version_id = params.superseded_by_version_id")
                params["superseded_by_version_id"] = superseded_by_version_id
        filters = [{"term": {self._resolve_filter_field("version_id"): version_id}}]
        if document_id:
            filters.append({"term": {self._resolve_filter_field("document_id"): document_id}})
        self.client.update_by_query(
            index=self.index_name,
            body={
                "script": {
                    "source": "; ".join(script_lines),
                    "lang": "painless",
                    "params": params,
                },
                "query": {"bool": {"filter": filters}},
            },
            refresh=True,
            conflicts="proceed",
        )
