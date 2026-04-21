from pydantic import BaseModel, Field


class RetrievalFilter(BaseModel):
    source_type: str | None = None
    document_id: str | None = None
    document_type: str | None = None
    project_id: str | None = None
    customer_id: str | None = None
    is_latest: bool | None = True
    confidentiality_level: str | None = None
    permission_tags: list[str] = Field(default_factory=list)


class SearchRequest(BaseModel):
    query: str
    user_id: str | None = None
    top_k: int = 10
    filters: RetrievalFilter = Field(default_factory=RetrievalFilter)
    include_citations: bool = True


class SearchResult(BaseModel):
    chunk_id: str
    document_id: str
    version_id: str
    chunk_index: int | None = None
    text: str
    score: float
    source_name: str | None = None
    source_uri: str | None = None
    source_type: str | None = None
    version_name: str | None = None
    heading_path: list[str] = Field(default_factory=list)
    section_path: list[str] = Field(default_factory=list)
    page_start: int | None = None
    page_end: int | None = None
    metadata: dict = Field(default_factory=dict)


class SearchResponse(BaseModel):
    query: str
    results: list[SearchResult]
    backend: str = "opensearch"
    dense_retrieval_status: str = "todo"
