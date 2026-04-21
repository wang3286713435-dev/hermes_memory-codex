from sqlalchemy.orm import Session

from app.memory_kernel.contracts import MemoryKernelRequest, MemoryKernelResult
from app.models.memory import ConversationMemory


class MemoryWriteback:
    """Writes durable interaction memory after kernel orchestration."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def write(self, request: MemoryKernelRequest, result: MemoryKernelResult) -> None:
        if not request.session_id:
            return
        self.db.add(
            ConversationMemory(
                user_id=request.user_id,
                conversation_id=request.session_id,
                memory_type="query_context_trace",
                content=self._summarize(request, result),
                source="memory_kernel",
                permission_scope="user_session",
            )
        )
        self.db.commit()

    def _summarize(self, request: MemoryKernelRequest, result: MemoryKernelResult) -> str:
        return (
            f"query={request.query}; "
            f"route={result.context.route.route_type}; "
            f"backend={result.context.backend}; "
            f"context_items={len(result.context.items)}; "
            f"citations={len(result.context.citations)}"
        )

