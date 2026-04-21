from pydantic import BaseModel, Field


class DocumentIngestRequest(BaseModel):
    source_uri: str = Field(..., description="Original file path, object URI, or external URL.")
    title: str | None = None
    source_type: str = "manual"
    document_type: str | None = None
    owner_id: str | None = None
    department_id: str | None = None
    project_id: str | None = None
    confidentiality_level: str = "internal"
    permission_tags: list[str] = Field(default_factory=list)


class DocumentIngestResponse(BaseModel):
    job_id: str
    status: str
    message: str
    document_id: str | None = None
    version_id: str | None = None
    chunk_count: int = 0
    indexed_count: int = 0
