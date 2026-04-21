from app.memory_kernel.contracts import QueryRoute


class QueryRouter:
    """Routes a query to the memory capability that should own context building."""

    def route(self, query: str) -> QueryRoute:
        normalized = query.strip()
        if any(term in normalized for term in ["多少", "数量", "金额", "日期", "截止", "状态"]):
            return QueryRoute(
                route_type="document_first_structured_aware",
                retrieval_mode="hybrid_bm25_first",
                reason="Query may contain structured facts; Phase 1 uses document-first retrieval.",
            )
        return QueryRoute(
            route_type="document_knowledge",
            retrieval_mode="hybrid_bm25_first",
            reason="Phase 1 routes enterprise knowledge questions through document memory.",
        )

