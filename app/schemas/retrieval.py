from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


RetrievalMode = Literal["sparse", "dense", "hybrid"]
RetrievalStatus = Literal["executed", "skipped", "unavailable", "failed", "not_executed"]


class RetrievalFilter(BaseModel):
    model_config = ConfigDict(extra="allow")

    source_type: str | None = None
    document_id: str | None = None
    document_type: str | None = None
    project_id: str | None = None
    customer_id: str | None = None
    is_latest: bool | None = True
    confidentiality_level: str | None = None
    permission_tags: list[str] = Field(default_factory=list)
    extra: dict = Field(default_factory=dict)


class SearchRequest(BaseModel):
    query: str
    route_type: str | None = None
    retrieval_mode: RetrievalMode = "hybrid"
    user_id: str | None = None
    top_k: int = 10
    filters: RetrievalFilter = Field(default_factory=RetrievalFilter)
    enable_dense: bool = True
    enable_sparse: bool = True
    enable_hybrid: bool = True
    include_citations: bool = True
    debug: bool = False
    query_vector: list[float] | None = None


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
    retrieval_sources: list[str] = Field(default_factory=list)
    scores: dict[str, float] = Field(default_factory=dict)


class SearchResponse(BaseModel):
    query: str
    results: list[SearchResult]
    items: list[SearchResult] = Field(default_factory=list)
    backend: str = "opensearch"
    retrieval_mode: RetrievalMode = "hybrid"
    dense_status: RetrievalStatus = "not_executed"
    sparse_status: RetrievalStatus = "not_executed"
    dense_retrieval_status: str = "not_executed"
    citations: list[dict] = Field(default_factory=list)
    applied_filters: dict = Field(default_factory=dict)
    ignored_filters: dict = Field(default_factory=dict)
    trace: dict = Field(default_factory=dict)

    @model_validator(mode="after")
    def fill_items_alias(self) -> "SearchResponse":
        if not self.items:
            self.items = self.results
        return self
