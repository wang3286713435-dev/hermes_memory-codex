from sqlalchemy.orm import Session

from app.memory_kernel.citation_generator import CitationGenerator
from app.memory_kernel.context_builder import ContextBuilder
from app.memory_kernel.contracts import MemoryContext, MemoryKernelRequest, MemoryKernelResult
from app.memory_kernel.governance import MemoryGovernance
from app.memory_kernel.query_router import QueryRouter
from app.memory_kernel.retrieval_orchestrator import RetrievalOrchestrator
from app.memory_kernel.writeback import MemoryWriteback


class MemoryKernel:
    """Built-in Hermes memory kernel.

    This layer is central to the agent request path. It is not a plugin hook and
    should be treated as Hermes core infrastructure.
    """

    def __init__(self, db: Session) -> None:
        self.router = QueryRouter()
        self.governance = MemoryGovernance()
        self.retrieval = RetrievalOrchestrator(db=db)
        self.citations = CitationGenerator()
        self.context_builder = ContextBuilder()
        self.writeback = MemoryWriteback(db=db)

    def run(self, request: MemoryKernelRequest) -> MemoryKernelResult:
        route = self.router.route(request.query)
        governance = self.governance.authorize(request)
        search_response = self.retrieval.retrieve(request, route, governance)
        citations = self.citations.generate(search_response.results)
        context = self.context_builder.build(
            query=request.query,
            route=route,
            search_response=search_response,
            citations=citations,
        )
        result = MemoryKernelResult(
            context=context,
            retrieval_results=search_response.results,
            answer_basis=self._build_answer_basis(context),
            confidence=self._confidence(context),
            trace={
                "route_type": route.route_type,
                "retrieval_mode": route.retrieval_mode,
                "route_reason": route.reason,
                "governance_allowed": governance.allowed,
                "governance_reason": governance.reason,
                "backend": context.backend,
                "dense_retrieval_status": context.dense_retrieval_status,
                "context_items": len(context.items),
                "citations": len(context.citations),
            },
        )
        self.writeback.write(request, result)
        return result

    def _build_answer_basis(self, context: MemoryContext) -> str:
        if not context.items:
            return "未检索到可引用依据，当前无法基于企业知识库给出确定回答。"
        return "\n\n".join(f"[{index + 1}] {item.text}" for index, item in enumerate(context.items[:5]))

    def _confidence(self, context: MemoryContext) -> str:
        if not context.items:
            return "low"
        if context.backend == "opensearch" and len(context.citations) >= 2:
            return "medium"
        return "low"

