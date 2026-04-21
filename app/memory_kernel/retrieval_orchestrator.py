from sqlalchemy.orm import Session

from app.memory_kernel.contracts import GovernanceDecision, MemoryKernelRequest, QueryRoute
from app.schemas.retrieval import SearchRequest, SearchResponse
from app.services.retrieval.service import RetrievalService


class RetrievalOrchestrator:
    """Coordinates memory retrieval for kernel-owned context building."""

    def __init__(self, db: Session) -> None:
        self.retrieval = RetrievalService(db=db)

    def retrieve(
        self,
        request: MemoryKernelRequest,
        route: QueryRoute,
        governance: GovernanceDecision,
    ) -> SearchResponse:
        if not governance.allowed:
            return SearchResponse(
                query=request.query,
                results=[],
                backend="governance_denied",
                dense_retrieval_status="not_executed",
            )
        return self.retrieval.search(
            SearchRequest(
                query=request.query,
                user_id=request.user_id,
                top_k=request.top_k,
                filters=governance.filters,
                include_citations=request.citation_required,
            )
        )

