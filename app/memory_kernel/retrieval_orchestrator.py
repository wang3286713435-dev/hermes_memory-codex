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
                retrieval_mode=request.retrieval_mode,
                dense_retrieval_status="not_executed",
                dense_status="not_executed",
                sparse_status="not_executed",
                applied_filters=governance.filters.model_dump(exclude_none=True),
                trace={"reason": governance.reason},
            )
        return self.retrieval.search(
            SearchRequest(
                query=request.query,
                route_type=route.route_type,
                retrieval_mode=request.retrieval_mode,  # type: ignore[arg-type]
                user_id=request.user_id,
                top_k=request.top_k,
                filters=governance.filters,
                enable_dense=request.enable_dense,
                enable_sparse=request.enable_sparse,
                enable_hybrid=request.enable_hybrid,
                include_citations=request.citation_required,
                debug=request.debug,
                query_vector=request.query_vector,
            )
        )
