from pydantic import BaseModel, Field

from app.schemas.retrieval import RetrievalFilter


class AskRequest(BaseModel):
    query: str
    user_id: str
    session_id: str | None = None
    filters: RetrievalFilter = Field(default_factory=RetrievalFilter)
    citation_required: bool = True


class Citation(BaseModel):
    document_id: str
    version_id: str
    chunk_id: str
    source_name: str | None = None
    source_uri: str | None = None
    version_name: str | None = None
    page_start: int | None = None
    page_end: int | None = None
    heading_path: list[str] = Field(default_factory=list)
    section_path: list[str] = Field(default_factory=list)
    quote_text: str


class AskResponse(BaseModel):
    answer: str
    citations: list[Citation] = Field(default_factory=list)
    confidence: str = "low"
    memory_kernel_trace: dict = Field(default_factory=dict)
