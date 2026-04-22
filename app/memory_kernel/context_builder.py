from app.memory_kernel.contracts import ContextItem, MemoryContext, QueryRoute
from app.schemas.agent import Citation
from app.schemas.retrieval import SearchResponse


class ContextBuilder:
    """Builds the canonical memory context passed to Hermes answer generation."""

    def build(
        self,
        query: str,
        route: QueryRoute,
        search_response: SearchResponse,
        citations: list[Citation],
    ) -> MemoryContext:
        items = [
            ContextItem(
                chunk_id=result.chunk_id,
                document_id=result.document_id,
                version_id=result.version_id,
                text=result.text,
                source_name=result.source_name,
                heading_path=result.heading_path,
                page_start=result.page_start,
                page_end=result.page_end,
            )
            for result in search_response.results
        ]
        return MemoryContext(
            query=query,
            route=route,
            items=items,
            citations=citations,
            backend=search_response.backend,
            dense_retrieval_status=search_response.dense_retrieval_status,
            sparse_retrieval_status=search_response.sparse_status,
            retrieval_mode=search_response.retrieval_mode,
            applied_filters=search_response.applied_filters,
            ignored_filters=search_response.ignored_filters,
        )
