from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import httpx

from app.core.config import settings
from app.services.embedding import AliyunTextEmbeddingV3
from app.schemas.retrieval import SearchRequest, SearchResult, RetrievalStatus


@dataclass
class DenseSearchOutcome:
    results: list[SearchResult] = field(default_factory=list)
    status: RetrievalStatus = "not_executed"
    trace: dict[str, Any] = field(default_factory=dict)


class ExistingVectorStoreDenseRetriever:
    """Adapter for the existing 1024-dimensional vector retrieval backend.

    The existing vector store is intentionally accessed through a narrow HTTP
    contract. Phase 2 does not own embedding generation; the backend may accept
    raw query text, a precomputed query vector, or both.
    """

    def search(self, request: SearchRequest, applied_filters: dict[str, Any]) -> DenseSearchOutcome:
        if not settings.vector_store_url:
            return DenseSearchOutcome(
                status="unavailable",
                trace={"reason": "VECTOR_STORE_URL is not configured"},
            )

        if request.query_vector is not None and len(request.query_vector) != settings.vector_dimension:
            return DenseSearchOutcome(
                status="failed",
                trace={
                    "reason": "query_vector_dimension_mismatch",
                    "expected_dimension": settings.vector_dimension,
                    "actual_dimension": len(request.query_vector),
                },
            )

        payload = {
            "query": request.query,
            "query_vector": request.query_vector,
            "top_k": request.top_k,
            "filters": applied_filters,
            "vector_dimension": settings.vector_dimension,
        }
        headers = {}
        if settings.vector_store_api_key:
            headers["Authorization"] = f"Bearer {settings.vector_store_api_key}"

        try:
            response = httpx.post(
                settings.vector_store_url.rstrip("/") + "/search",
                json=payload,
                headers=headers,
                timeout=5,
            )
            response.raise_for_status()
            data = response.json()
        except Exception as exc:
            return DenseSearchOutcome(status="failed", trace={"error": str(exc)})

        raw_items = data.get("results") or data.get("items") or []
        results: list[SearchResult] = []
        skipped = 0
        for item in raw_items:
            normalized = self._result_from_raw(item)
            if not normalized.chunk_id:
                skipped += 1
                continue
            results.append(normalized)
        return DenseSearchOutcome(
            results=results,
            status="executed",
            trace={
                "backend": "existing_vector_store",
                "endpoint": settings.vector_store_url,
                "returned": len(raw_items),
                "normalized": len(results),
                "skipped": skipped,
                "vector_dimension": settings.vector_dimension,
                "request_contract": "phase2.1_dense_search_v1",
            },
        )

    def _result_from_raw(self, raw: dict[str, Any]) -> SearchResult:
        metadata = dict(raw.get("metadata") or raw.get("metadata_json") or {})
        if raw.get("embedding") is not None:
            metadata["embedding"] = raw.get("embedding")
        score = float(raw.get("score") or raw.get("_score") or 0.0)
        chunk_id = raw.get("chunk_id") or metadata.get("chunk_id") or raw.get("id")
        document_id = raw.get("document_id") or metadata.get("document_id")
        version_id = raw.get("version_id") or metadata.get("version_id")
        source_type = raw.get("source_type") or metadata.get("source_type")
        return SearchResult(
            chunk_id=str(chunk_id or ""),
            document_id=str(document_id or ""),
            version_id=str(version_id or ""),
            chunk_index=raw.get("chunk_index") or metadata.get("chunk_index"),
            text=str(raw.get("text") or raw.get("snippet") or raw.get("content") or ""),
            score=score,
            source_name=raw.get("source_name") or metadata.get("source_name"),
            source_uri=raw.get("source_uri") or metadata.get("source_uri"),
            source_type=source_type,
            version_name=raw.get("version_name") or metadata.get("version_name"),
            heading_path=list(raw.get("heading_path") or metadata.get("heading_path") or []),
            section_path=list(
                raw.get("section_path")
                or metadata.get("section_path")
                or raw.get("heading_path")
                or metadata.get("heading_path")
                or []
            ),
            page_start=raw.get("page_start") or metadata.get("page_start"),
            page_end=raw.get("page_end") or metadata.get("page_end"),
            metadata=metadata,
            retrieval_sources=["dense"],
            scores={"dense": score},
        )


class QdrantDenseRetriever:
    """Qdrant dense retrieval adapter for the Phase 2.1 retrieval contract."""

    def __init__(self, embedding: AliyunTextEmbeddingV3 | None = None) -> None:
        self.embedding = embedding or AliyunTextEmbeddingV3()

    def ensure_collection(self) -> dict[str, Any]:
        headers = self._headers()
        collection_url = self._url(f"/collections/{settings.qdrant_collection}")
        response = httpx.get(collection_url, headers=headers, timeout=5)
        if response.status_code == 200:
            return {"status": "exists", "collection": settings.qdrant_collection}

        payload = {
            "vectors": {
                "size": settings.qdrant_vector_size,
                "distance": "Cosine",
            }
        }
        create_response = httpx.put(collection_url, json=payload, headers=headers, timeout=10)
        create_response.raise_for_status()
        return {"status": "created", "collection": settings.qdrant_collection}

    def upsert_chunk(
        self,
        *,
        chunk_id: str,
        vector: list[float],
        payload: dict[str, Any],
    ) -> dict[str, Any]:
        if len(vector) != settings.qdrant_vector_size:
            raise ValueError(
                f"Qdrant vector dimension mismatch: expected {settings.qdrant_vector_size}, got {len(vector)}"
            )
        self.ensure_collection()
        upsert_payload = {
            "points": [
                {
                    "id": chunk_id,
                    "vector": vector,
                    "payload": {"chunk_id": chunk_id, **payload},
                }
            ]
        }
        response = httpx.put(
            self._url(f"/collections/{settings.qdrant_collection}/points"),
            params={"wait": "true"},
            json=upsert_payload,
            headers=self._headers(),
            timeout=15,
        )
        response.raise_for_status()
        return response.json()

    def search(self, request: SearchRequest, applied_filters: dict[str, Any]) -> DenseSearchOutcome:
        query_vector = request.query_vector
        embedding_trace: dict[str, Any] = {"status": "provided_query_vector"}
        if query_vector is None:
            embedding_outcome = self.embedding.embed_query(request.query)
            embedding_trace = {"status": embedding_outcome.status, **embedding_outcome.trace}
            query_vector = embedding_outcome.vector
            if query_vector is None:
                return DenseSearchOutcome(
                    status="unavailable" if embedding_outcome.status == "unavailable" else "failed",
                    trace={
                        "backend": "qdrant_dense",
                        "reason": "query_vector_unavailable",
                        "embedding": embedding_trace,
                    },
                )

        if len(query_vector) != settings.qdrant_vector_size:
            return DenseSearchOutcome(
                status="failed",
                trace={
                    "backend": "qdrant_dense",
                    "reason": "query_vector_dimension_mismatch",
                    "expected_dimension": settings.qdrant_vector_size,
                    "actual_dimension": len(query_vector),
                },
            )

        payload = {
            "vector": query_vector,
            "limit": request.top_k,
            "filter": self._build_filter(applied_filters),
            "with_payload": True,
            "with_vector": False,
        }
        try:
            response = httpx.post(
                self._url(f"/collections/{settings.qdrant_collection}/points/search"),
                json=payload,
                headers=self._headers(),
                timeout=10,
            )
            response.raise_for_status()
            data = response.json()
        except Exception as exc:
            return DenseSearchOutcome(
                status="failed",
                trace={
                    "backend": "qdrant_dense",
                    "error": str(exc),
                    "collection": settings.qdrant_collection,
                },
            )

        raw_items = data.get("result") or []
        results: list[SearchResult] = []
        skipped = 0
        for item in raw_items:
            normalized = self._result_from_qdrant(item)
            if not normalized.chunk_id:
                skipped += 1
                continue
            results.append(normalized)

        return DenseSearchOutcome(
            results=results,
            status="executed",
            trace={
                "backend": "qdrant_dense",
                "provider": "qdrant",
                "collection": settings.qdrant_collection,
                "returned": len(raw_items),
                "normalized": len(results),
                "skipped": skipped,
                "vector_dimension": settings.qdrant_vector_size,
                "filter": payload["filter"],
                "embedding": embedding_trace,
                "request_contract": "phase2.1_qdrant_dense_v1",
            },
        )

    def _headers(self) -> dict[str, str]:
        headers: dict[str, str] = {}
        if settings.qdrant_api_key:
            headers["api-key"] = settings.qdrant_api_key
        return headers

    def _url(self, path: str) -> str:
        return settings.qdrant_url.rstrip("/") + path

    def _build_filter(self, applied_filters: dict[str, Any]) -> dict[str, Any] | None:
        must = []
        for field in ("source_type", "document_id", "document_type", "is_latest"):
            if field in applied_filters:
                must.append({"key": field, "match": {"value": applied_filters[field]}})
        if "version_id" in applied_filters:
            must.append({"key": "version_id", "match": {"value": applied_filters["version_id"]}})
        if not must:
            return None
        return {"must": must}

    def set_payload_by_filter(self, *, payload: dict[str, Any], filter_must: list[dict[str, Any]]) -> dict[str, Any]:
        self.ensure_collection()
        response = httpx.post(
            self._url(f"/collections/{settings.qdrant_collection}/points/payload"),
            json={"payload": payload, "filter": {"must": filter_must}},
            headers=self._headers(),
            timeout=15,
        )
        response.raise_for_status()
        return response.json()

    def _result_from_qdrant(self, raw: dict[str, Any]) -> SearchResult:
        payload = dict(raw.get("payload") or {})
        score = float(raw.get("score") or 0.0)
        chunk_id = payload.get("chunk_id") or raw.get("id")
        text = payload.get("text") or payload.get("snippet") or payload.get("content") or ""
        metadata = dict(payload.get("metadata") or payload.get("metadata_json") or {})
        return SearchResult(
            chunk_id=str(chunk_id or ""),
            document_id=str(payload.get("document_id") or metadata.get("document_id") or ""),
            version_id=str(payload.get("version_id") or metadata.get("version_id") or ""),
            chunk_index=payload.get("chunk_index") or metadata.get("chunk_index"),
            text=str(text),
            score=score,
            source_name=payload.get("source_name") or metadata.get("source_name"),
            source_uri=payload.get("source_uri") or metadata.get("source_uri"),
            source_type=payload.get("source_type") or metadata.get("source_type"),
            version_name=payload.get("version_name") or metadata.get("version_name"),
            heading_path=list(payload.get("heading_path") or metadata.get("heading_path") or []),
            section_path=list(
                payload.get("section_path")
                or metadata.get("section_path")
                or payload.get("heading_path")
                or metadata.get("heading_path")
                or []
            ),
            page_start=payload.get("page_start") or metadata.get("page_start"),
            page_end=payload.get("page_end") or metadata.get("page_end"),
            metadata=metadata,
            retrieval_sources=["dense"],
            scores={"dense": score},
        )
