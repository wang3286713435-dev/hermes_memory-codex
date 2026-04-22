from typing import Protocol

from app.schemas.retrieval import SearchRequest, SearchResult
from app.services.retrieval.rerank import RerankOutcome, RerankRequest


class DenseRetriever(Protocol):
    def search(self, request: SearchRequest) -> list[SearchResult]:
        """Return dense vector candidates."""


class SparseRetriever(Protocol):
    def search(self, request: SearchRequest) -> list[SearchResult]:
        """Return BM25 or sparse candidates."""


class Reranker(Protocol):
    def rerank(self, request: RerankRequest) -> RerankOutcome:
        """Rerank retrieval candidates."""
