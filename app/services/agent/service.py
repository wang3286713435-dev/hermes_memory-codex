from sqlalchemy.orm import Session

from app.memory_kernel.contracts import MemoryKernelRequest
from app.memory_kernel.kernel import MemoryKernel
from app.schemas.agent import AskRequest, AskResponse


class AgentService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.memory_kernel = MemoryKernel(db=db)

    def ask(self, request: AskRequest) -> AskResponse:
        kernel_result = self.memory_kernel.run(
            MemoryKernelRequest(
                query=request.query,
                user_id=request.user_id,
                session_id=request.session_id,
                filters=request.filters,
                top_k=10,
                citation_required=request.citation_required,
            )
        )
        if not kernel_result.context.items:
            return AskResponse(
                answer=kernel_result.answer_basis,
                citations=[],
                confidence="low",
                memory_kernel_trace=kernel_result.trace,
            )
        return AskResponse(
            answer=(
                "已通过 Hermes memory kernel 构建企业知识上下文。"
                "后续 LLM 生成层应仅基于该上下文和引用生成最终回答。\n\n"
                f"{kernel_result.answer_basis}"
            ),
            citations=kernel_result.context.citations,
            confidence=kernel_result.confidence,
            memory_kernel_trace=kernel_result.trace,
        )
