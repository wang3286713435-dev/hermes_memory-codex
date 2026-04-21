from dataclasses import dataclass, field

from app.schemas.agent import Citation
from app.schemas.retrieval import RetrievalFilter, SearchResult


@dataclass(frozen=True)
class MemoryKernelRequest:
    query: str
    user_id: str
    session_id: str | None
    filters: RetrievalFilter
    top_k: int = 10
    citation_required: bool = True


@dataclass(frozen=True)
class QueryRoute:
    route_type: str
    retrieval_mode: str
    reason: str


@dataclass(frozen=True)
class GovernanceDecision:
    allowed: bool
    filters: RetrievalFilter
    reason: str


@dataclass(frozen=True)
class ContextItem:
    chunk_id: str
    document_id: str
    version_id: str
    text: str
    source_name: str | None
    heading_path: list[str] = field(default_factory=list)
    page_start: int | None = None
    page_end: int | None = None


@dataclass(frozen=True)
class MemoryContext:
    query: str
    route: QueryRoute
    items: list[ContextItem]
    citations: list[Citation]
    backend: str
    dense_retrieval_status: str


@dataclass(frozen=True)
class MemoryKernelResult:
    context: MemoryContext
    retrieval_results: list[SearchResult]
    answer_basis: str
    confidence: str
    trace: dict

