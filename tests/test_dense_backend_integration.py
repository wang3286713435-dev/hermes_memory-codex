from __future__ import annotations

import json
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

from app.core.config import settings
from app.schemas.retrieval import RetrievalFilter, SearchRequest, SearchResult
from app.services.retrieval.service import RetrievalService


class _VectorSearchHandler(BaseHTTPRequestHandler):
    captured: dict = {}

    def do_POST(self):  # noqa: N802
        length = int(self.headers.get("content-length", "0"))
        payload = json.loads(self.rfile.read(length) or b"{}")
        type(self).captured = {"path": self.path, "payload": payload}
        body = {
            "results": [
                {
                    "chunk_id": "chunk-dense",
                    "score": 0.91,
                    "snippet": "dense backend snippet",
                    "metadata": {
                        "document_id": payload["filters"].get("document_id", "doc-dense"),
                        "version_id": "ver-dense",
                        "source_type": payload["filters"].get("source_type", "upload"),
                        "heading_path": ["Dense", "Section"],
                    },
                    "embedding": [0.0, 0.1],
                }
            ]
        }
        data = json.dumps(body).encode()
        self.send_response(200)
        self.send_header("content-type", "application/json")
        self.send_header("content-length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, *_args):
        return None


def _start_vector_backend():
    server = HTTPServer(("127.0.0.1", 0), _VectorSearchHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server


def test_dense_backend_real_http_contract(monkeypatch):
    server = _start_vector_backend()
    monkeypatch.setattr(settings, "vector_store_provider", "existing")
    monkeypatch.setattr(settings, "vector_store_url", f"http://127.0.0.1:{server.server_port}")
    monkeypatch.setattr(settings, "vector_dimension", 1024)

    service = RetrievalService(db=None)  # type: ignore[arg-type]
    monkeypatch.setattr(service, "_write_log", lambda *args, **kwargs: None)

    response = service.search(
        SearchRequest(
            query="投标截止日期",
            retrieval_mode="dense",
            enable_sparse=False,
            top_k=3,
            filters=RetrievalFilter(source_type="upload", document_id="doc-1"),
        )
    )

    server.shutdown()

    captured = _VectorSearchHandler.captured
    assert captured["path"] == "/search"
    assert captured["payload"]["query"] == "投标截止日期"
    assert captured["payload"]["top_k"] == 3
    assert captured["payload"]["filters"] == {
        "source_type": "upload",
        "document_id": "doc-1",
        "is_latest": True,
    }
    assert captured["payload"]["vector_dimension"] == 1024
    assert response.dense_status == "executed"
    assert response.results[0].chunk_id == "chunk-dense"
    assert response.results[0].document_id == "doc-1"
    assert response.results[0].source_type == "upload"
    assert response.results[0].retrieval_sources == ["dense"]
    assert response.results[0].metadata["embedding"] == [0.0, 0.1]


def test_hybrid_real_dense_backend_merges_with_sparse(monkeypatch):
    server = _start_vector_backend()
    monkeypatch.setattr(settings, "vector_store_provider", "existing")
    monkeypatch.setattr(settings, "vector_store_url", f"http://127.0.0.1:{server.server_port}")
    monkeypatch.setattr(settings, "vector_dimension", 1024)

    service = RetrievalService(db=None)  # type: ignore[arg-type]
    monkeypatch.setattr(service, "_write_log", lambda *args, **kwargs: None)

    def fake_sparse(_request, _applied_filters):
        return [
            SearchResult(
                chunk_id="chunk-dense",
                document_id="doc-1",
                version_id="ver-dense",
                text="sparse copy",
                score=2.0,
                retrieval_sources=["sparse"],
                scores={"sparse": 2.0},
            ),
            SearchResult(
                chunk_id="chunk-sparse",
                document_id="doc-2",
                version_id="ver-sparse",
                text="sparse only",
                score=1.0,
                retrieval_sources=["sparse"],
                scores={"sparse": 1.0},
            ),
        ]

    monkeypatch.setattr(service, "_sparse_search", fake_sparse)
    response = service.search(SearchRequest(query="投标截止日期", retrieval_mode="hybrid", top_k=5))

    server.shutdown()

    shared = next(item for item in response.results if item.chunk_id == "chunk-dense")
    assert response.backend == "hybrid"
    assert response.dense_status == "executed"
    assert response.sparse_status == "executed"
    assert shared.retrieval_sources == ["dense", "sparse"]
    assert shared.scores == {"dense": 0.91, "sparse": 2.0}
    assert shared.score == 2.91
    assert response.trace["dense"]["request_contract"] == "phase2.1_dense_search_v1"
    assert response.trace["hybrid"]["dedupe_key"] == "chunk_id"


def test_dense_backend_failure_is_fail_open_for_hybrid(monkeypatch):
    monkeypatch.setattr(settings, "vector_store_provider", "existing")
    monkeypatch.setattr(settings, "vector_store_url", "http://127.0.0.1:1")
    service = RetrievalService(db=None)  # type: ignore[arg-type]
    monkeypatch.setattr(service, "_write_log", lambda *args, **kwargs: None)
    monkeypatch.setattr(
        service,
        "_sparse_search",
        lambda _request, _filters: [
            SearchResult(
                chunk_id="chunk-sparse",
                document_id="doc-1",
                version_id="ver-1",
                text="sparse survives",
                score=1.0,
                retrieval_sources=["sparse"],
                scores={"sparse": 1.0},
            )
        ],
    )

    response = service.search(SearchRequest(query="投标截止日期", retrieval_mode="hybrid"))

    assert response.dense_status == "failed"
    assert response.sparse_status == "executed"
    assert [item.chunk_id for item in response.results] == ["chunk-sparse"]
