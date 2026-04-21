from typing import Protocol

from app.schemas.retrieval import SearchRequest, SearchResult


class DenseRetriever(Protocol):
    def search(self, request: SearchRequest) -> list[SearchResult]:
        """Return dense vector candidates."""


class SparseRetriever(Protocol):
    def search(self, request: SearchRequest) -> list[SearchResult]:
        """Return BM25 or sparse candidates."""


class Reranker(Protocol):
    def rerank(self, query: str, candidates: list[SearchResult], top_k: int) -> list[SearchResult]:
        """Rerank retrieval candidates."""

