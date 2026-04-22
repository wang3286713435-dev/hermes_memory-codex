from __future__ import annotations

import json
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

import pytest

from app.core.config import settings
from app.schemas.retrieval import RetrievalFilter, SearchRequest, SearchResult
from app.services.retrieval.service import RetrievalService
from app.services.retrieval.dense import QdrantDenseRetriever


VECTOR = [0.01] * 1024


class _QdrantHandler(BaseHTTPRequestHandler):
    captured: dict = {}
    collection_exists = False

    def do_GET(self):  # noqa: N802
        if self.path.startswith("/collections/hermes_test_chunks") and type(self).collection_exists:
            self._send({"result": {"status": "green"}})
            return
        self.send_response(404)
        self.end_headers()

    def do_PUT(self):  # noqa: N802
        length = int(self.headers.get("content-length", "0"))
        payload = json.loads(self.rfile.read(length) or b"{}")
        if self.path.startswith("/collections/hermes_test_chunks/points"):
            type(self).captured["upsert"] = payload
            self._send({"result": {"operation_id": 1, "status": "completed"}})
            return
        if self.path.startswith("/collections/hermes_test_chunks"):
            type(self).captured["collection"] = payload
            type(self).collection_exists = True
            self._send({"result": True})
            return
        self.send_response(404)
        self.end_headers()

    def do_POST(self):  # noqa: N802
        length = int(self.headers.get("content-length", "0"))
        payload = json.loads(self.rfile.read(length) or b"{}")
        type(self).captured["search"] = {"path": self.path, "payload": payload}
        self._send(
            {
                "result": [
                    {
                        "id": "11111111-1111-1111-1111-111111111111",
                        "score": 0.93,
                        "payload": {
                            "chunk_id": "11111111-1111-1111-1111-111111111111",
                            "document_id": "doc-1",
                            "version_id": "ver-1",
                            "text": "Qdrant dense hit",
                            "source_type": "upload",
                            "document_type": "tender",
                            "is_latest": True,
                            "heading_path": ["Qdrant", "Dense"],
                        },
                    }
                ]
            }
        )

    def log_message(self, *_args):
        return None

    def _send(self, body: dict) -> None:
        data = json.dumps(body).encode()
        self.send_response(200)
        self.send_header("content-type", "application/json")
        self.send_header("content-length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)


def _start_qdrant_backend():
    _QdrantHandler.captured = {}
    _QdrantHandler.collection_exists = False
    server = HTTPServer(("127.0.0.1", 0), _QdrantHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server


def test_qdrant_collection_upsert_and_search_contract(monkeypatch):
    server = _start_qdrant_backend()
    monkeypatch.setattr(settings, "qdrant_url", f"http://127.0.0.1:{server.server_port}")
    monkeypatch.setattr(settings, "qdrant_collection", "hermes_test_chunks")
    monkeypatch.setattr(settings, "qdrant_vector_size", 1024)

    retriever = QdrantDenseRetriever()
    retriever.upsert_chunk(
        chunk_id="11111111-1111-1111-1111-111111111111",
        vector=VECTOR,
        payload={
            "document_id": "doc-1",
            "version_id": "ver-1",
            "text": "Qdrant dense hit",
            "source_type": "upload",
            "document_type": "tender",
            "is_latest": True,
        },
    )
    outcome = retriever.search(
        SearchRequest(
            query="投标截止日期",
            retrieval_mode="dense",
            query_vector=VECTOR,
            top_k=3,
            filters=RetrievalFilter(source_type="upload", document_id="doc-1"),
        ),
        {"source_type": "upload", "document_id": "doc-1", "is_latest": True},
    )

    server.shutdown()

    assert _QdrantHandler.captured["collection"]["vectors"] == {
        "size": 1024,
        "distance": "Cosine",
    }
    assert _QdrantHandler.captured["upsert"]["points"][0]["payload"]["chunk_id"]
    search_payload = _QdrantHandler.captured["search"]["payload"]
    assert search_payload["limit"] == 3
    assert search_payload["with_payload"] is True
    assert search_payload["with_vector"] is False
    assert search_payload["filter"] == {
        "must": [
            {"key": "source_type", "match": {"value": "upload"}},
            {"key": "document_id", "match": {"value": "doc-1"}},
            {"key": "is_latest", "match": {"value": True}},
        ]
    }
    assert outcome.status == "executed"
    assert outcome.trace["backend"] == "qdrant_dense"
    assert outcome.trace["request_contract"] == "phase2.1_qdrant_dense_v1"
    assert outcome.results[0].chunk_id == "11111111-1111-1111-1111-111111111111"
    assert outcome.results[0].document_id == "doc-1"
    assert outcome.results[0].retrieval_sources == ["dense"]
    assert outcome.results[0].scores == {"dense": 0.93}


def test_qdrant_dense_service_result_contract(monkeypatch):
    server = _start_qdrant_backend()
    monkeypatch.setattr(settings, "vector_store_provider", "qdrant")
    monkeypatch.setattr(settings, "qdrant_url", f"http://127.0.0.1:{server.server_port}")
    monkeypatch.setattr(settings, "qdrant_collection", "hermes_test_chunks")
    monkeypatch.setattr(settings, "qdrant_vector_size", 1024)

    service = RetrievalService(db=None)  # type: ignore[arg-type]
    monkeypatch.setattr(service, "_write_log", lambda *args, **kwargs: None)
    response = service.search(
        SearchRequest(
            query="投标截止日期",
            retrieval_mode="dense",
            enable_sparse=False,
            query_vector=VECTOR,
            filters=RetrievalFilter(source_type="upload", document_id="doc-1"),
        )
    )

    server.shutdown()

    assert response.backend == "qdrant_dense"
    assert response.dense_status == "executed"
    assert response.sparse_status == "skipped"
    assert response.results[0].text == "Qdrant dense hit"
    assert response.trace["dense"]["backend"] == "qdrant_dense"


def test_qdrant_hybrid_merges_and_fail_opens(monkeypatch):
    server = _start_qdrant_backend()
    monkeypatch.setattr(settings, "vector_store_provider", "qdrant")
    monkeypatch.setattr(settings, "qdrant_url", f"http://127.0.0.1:{server.server_port}")
    monkeypatch.setattr(settings, "qdrant_collection", "hermes_test_chunks")
    monkeypatch.setattr(settings, "qdrant_vector_size", 1024)

    service = RetrievalService(db=None)  # type: ignore[arg-type]
    monkeypatch.setattr(service, "_write_log", lambda *args, **kwargs: None)

    def fake_sparse(_request, _applied_filters):
        return [
            SearchResult(
                chunk_id="11111111-1111-1111-1111-111111111111",
                document_id="doc-1",
                version_id="ver-1",
                text="sparse copy",
                score=2.0,
                retrieval_sources=["sparse"],
                scores={"sparse": 2.0},
            )
        ]

    monkeypatch.setattr(service, "_sparse_search", fake_sparse)
    response = service.search(
        SearchRequest(query="投标截止日期", retrieval_mode="hybrid", query_vector=VECTOR)
    )
    server.shutdown()

    shared = response.results[0]
    assert response.backend == "hybrid"
    assert response.dense_status == "executed"
    assert response.sparse_status == "executed"
    assert shared.retrieval_sources == ["dense", "sparse"]
    assert shared.scores == {"dense": 0.93, "sparse": 2.0}
    assert shared.score == 2.93
    assert response.trace["dense"]["backend"] == "qdrant_dense"
    assert response.trace["hybrid"]["dedupe_key"] == "chunk_id"


def test_qdrant_failure_fail_opens_to_sparse(monkeypatch):
    monkeypatch.setattr(settings, "vector_store_provider", "qdrant")
    monkeypatch.setattr(settings, "qdrant_url", "http://127.0.0.1:1")
    monkeypatch.setattr(settings, "qdrant_collection", "hermes_test_chunks")

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

    response = service.search(
        SearchRequest(query="投标截止日期", retrieval_mode="hybrid", query_vector=VECTOR)
    )

    assert response.dense_status == "failed"
    assert response.sparse_status == "executed"
    assert [item.chunk_id for item in response.results] == ["chunk-sparse"]


@pytest.mark.skipif(
    not settings.qdrant_url or settings.qdrant_url == "http://localhost:6333",
    reason="Set QDRANT_URL to run against a real external Qdrant environment.",
)
def test_real_qdrant_environment_is_configurable():
    assert settings.qdrant_vector_size == 1024
