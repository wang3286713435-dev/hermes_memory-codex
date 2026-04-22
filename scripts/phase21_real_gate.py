from __future__ import annotations

import json
import os
import sys

import httpx

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.core.config import settings
from app.schemas.retrieval import RetrievalFilter, SearchRequest
from app.services.embedding import AliyunTextEmbeddingV3
from app.services.retrieval.dense import QdrantDenseRetriever
from app.services.retrieval.service import RetrievalService


def _ensure_opensearch_index(index: str) -> None:
    # OpenSearch security is disabled in docker-compose; expect unauthenticated HTTP.
    base = settings.opensearch_url.rstrip("/")
    with httpx.Client(timeout=30, trust_env=False) as client:
        expected_mapping = {
            "mappings": {
                "properties": {
                    "chunk_id": {"type": "keyword"},
                    "document_id": {"type": "keyword"},
                    "version_id": {"type": "keyword"},
                    "status": {"type": "keyword"},
                    "source_type": {"type": "keyword"},
                    "document_type": {"type": "keyword"},
                    "is_latest": {"type": "boolean"},
                    "text": {"type": "text"},
                }
            }
        }

        exists = client.head(f"{base}/{index}")
        if exists.status_code == 200:
            mapping = client.get(f"{base}/{index}/_mapping").json()
            props = ((mapping.get(index) or {}).get("mappings") or {}).get("properties") or {}
            if (props.get("document_id") or {}).get("type") == "keyword":
                return
            client.delete(f"{base}/{index}").raise_for_status()

        resp = client.put(f"{base}/{index}", json=expected_mapping)
        resp.raise_for_status()


def _opensearch_upsert_doc(index: str, doc_id: str, body: dict) -> None:
    base = settings.opensearch_url.rstrip("/")
    with httpx.Client(timeout=30, trust_env=False) as client:
        resp = client.put(f"{base}/{index}/_doc/{doc_id}", json=body)
        resp.raise_for_status()
        client.post(f"{base}/{index}/_refresh")


def main() -> None:
    collection = settings.qdrant_collection
    index = settings.opensearch_index_chunks
    retriever = QdrantDenseRetriever()

    query = "gatekey"
    original_qdrant_url = settings.qdrant_url

    embedding_client = AliyunTextEmbeddingV3()
    embedding_probe = embedding_client.embed_query(query)
    if embedding_probe.vector is not None:
        vector_a = embedding_probe.vector
        vector_b = list(vector_a)
        vector_b[0] = float(vector_b[0]) + 0.0001
    else:
        vector_a = [0.01] * settings.qdrant_vector_size
        vector_b = [0.02] * settings.qdrant_vector_size

    # Qdrant point ids must be UUID or integer; use fixed UUIDs for deterministic gate checks.
    chunk_a = "11111111-1111-1111-1111-111111111111"
    chunk_b = "22222222-2222-2222-2222-222222222222"

    # 1) Ensure Qdrant collection + upsert minimal payloads.
    retriever.ensure_collection()
    retriever.upsert_chunk(
        chunk_id=chunk_a,
        vector=vector_a,
        payload={
            "document_id": "doc-1",
            "version_id": "ver-1",
            "text": f"Qdrant dense hit A: {query}",
            "source_type": "upload",
            "document_type": "tender",
            "is_latest": True,
            "heading_path": ["Gate", "Qdrant", "A"],
        },
    )
    retriever.upsert_chunk(
        chunk_id=chunk_b,
        vector=vector_b,
        payload={
            "document_id": "doc-2",
            "version_id": "ver-2",
            "text": f"Qdrant dense hit B: {query}",
            "source_type": "upload",
            "document_type": "tender",
            "is_latest": True,
            "heading_path": ["Gate", "Qdrant", "B"],
        },
    )

    # 2) Ensure OpenSearch index + seed a sparse doc that shares chunk_id with dense A.
    _ensure_opensearch_index(index)
    _opensearch_upsert_doc(
        index,
        chunk_a,
        {
            "chunk_id": chunk_a,
            "document_id": "doc-1",
            "version_id": "ver-1",
            "chunk_index": 0,
            "text": f"OpenSearch sparse hit A: {query}",
            "status": "active",
            "source_type": "upload",
            "document_type": "tender",
            "is_latest": True,
            "source_name": "gate-doc",
            "heading_path": ["Gate", "OpenSearch", "A"],
            "metadata_json": {},
        },
    )

    # 3) Run RetrievalService dense-only + hybrid through the real Qdrant/OpenSearch backends.
    service = RetrievalService(db=None)  # type: ignore[arg-type]
    service._write_log = lambda *_args, **_kwargs: None  # type: ignore[method-assign]

    dense_req = SearchRequest(
        query=query,
        retrieval_mode="dense",
        enable_sparse=False,
        top_k=5,
        query_vector=vector_a,
        filters=RetrievalFilter(source_type="upload", document_id="doc-1", document_type="tender", is_latest=True),
    )
    dense_resp = service.search(dense_req)

    dense_embed_req = SearchRequest(
        query=query,
        retrieval_mode="dense",
        enable_sparse=False,
        top_k=5,
        query_vector=None,
        filters=RetrievalFilter(source_type="upload", document_id="doc-1", document_type="tender", is_latest=True),
    )
    dense_embed_resp = service.search(dense_embed_req)

    hybrid_req = SearchRequest(
        query=query,
        retrieval_mode="hybrid",
        top_k=5,
        query_vector=vector_a,
        filters=RetrievalFilter(source_type="upload", document_id="doc-1", document_type="tender", is_latest=True),
    )
    hybrid_resp = service.search(hybrid_req)

    hybrid_embed_req = SearchRequest(
        query=query,
        retrieval_mode="hybrid",
        top_k=5,
        query_vector=None,
        filters=RetrievalFilter(source_type="upload", document_id="doc-1", document_type="tender", is_latest=True),
    )
    hybrid_embed_resp = service.search(hybrid_embed_req)

    # 3.1) Fail-open: make Qdrant unreachable and ensure sparse still returns.
    settings.qdrant_url = "http://127.0.0.1:1"
    fail_open_resp = service.search(hybrid_req)

    # 4) Emit a compact machine-readable summary for gate sign-off.
    summary = {
        "settings": {
            "qdrant_url": original_qdrant_url,
            "qdrant_collection": collection,
            "qdrant_vector_size": settings.qdrant_vector_size,
            "opensearch_url": settings.opensearch_url,
            "opensearch_index": index,
        },
        "aliyun_embedding_probe": {
            "status": embedding_probe.status,
            "dimension": len(embedding_probe.vector) if embedding_probe.vector is not None else None,
            "trace": embedding_probe.trace,
        },
        "dense_only": {
            "backend": dense_resp.backend,
            "dense_status": dense_resp.dense_status,
            "sparse_status": dense_resp.sparse_status,
            "top_chunk_id": dense_resp.results[0].chunk_id if dense_resp.results else None,
            "trace_dense": dense_resp.trace.get("dense"),
        },
        "dense_only_aliyun": {
            "backend": dense_embed_resp.backend,
            "dense_status": dense_embed_resp.dense_status,
            "sparse_status": dense_embed_resp.sparse_status,
            "top_chunk_id": dense_embed_resp.results[0].chunk_id if dense_embed_resp.results else None,
            "trace_dense": dense_embed_resp.trace.get("dense"),
        },
        "hybrid": {
            "backend": hybrid_resp.backend,
            "dense_status": hybrid_resp.dense_status,
            "sparse_status": hybrid_resp.sparse_status,
            "result_count": len(hybrid_resp.results),
            "top_result": hybrid_resp.results[0].model_dump() if hybrid_resp.results else None,
            "trace_dense": hybrid_resp.trace.get("dense"),
            "trace_sparse": hybrid_resp.trace.get("sparse"),
            "trace_hybrid": hybrid_resp.trace.get("hybrid"),
        },
        "hybrid_aliyun": {
            "backend": hybrid_embed_resp.backend,
            "dense_status": hybrid_embed_resp.dense_status,
            "sparse_status": hybrid_embed_resp.sparse_status,
            "result_count": len(hybrid_embed_resp.results),
            "top_result": hybrid_embed_resp.results[0].model_dump() if hybrid_embed_resp.results else None,
            "trace_dense": hybrid_embed_resp.trace.get("dense"),
            "trace_sparse": hybrid_embed_resp.trace.get("sparse"),
            "trace_hybrid": hybrid_embed_resp.trace.get("hybrid"),
        },
        "fail_open": {
            "qdrant_url": settings.qdrant_url,
            "backend": fail_open_resp.backend,
            "dense_status": fail_open_resp.dense_status,
            "sparse_status": fail_open_resp.sparse_status,
            "result_count": len(fail_open_resp.results),
            "top_result": fail_open_resp.results[0].model_dump() if fail_open_resp.results else None,
            "trace_dense": fail_open_resp.trace.get("dense"),
            "trace_sparse": fail_open_resp.trace.get("sparse"),
        },
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
