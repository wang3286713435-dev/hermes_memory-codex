from app.schemas.retrieval import SearchResult


class NoopReranker:
    def rerank(self, query: str, candidates: list[SearchResult], top_k: int) -> list[SearchResult]:
        return sorted(candidates, key=lambda item: item.score, reverse=True)[:top_k]

