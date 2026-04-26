from pydantic import BaseModel, Field


class FactCreateFromEvidenceRequest(BaseModel):
    fact_type: str = Field(..., min_length=1)
    subject: str = Field(..., min_length=1)
    predicate: str = Field(..., min_length=1)
    value: str = Field(..., min_length=1)
    source_chunk_id: str = Field(..., min_length=1)
    confidence: float | None = Field(default=None, ge=0.0, le=1.0)
    created_by: str | None = None
    audit_event_id: str | None = None


class FactStatusUpdateRequest(BaseModel):
    actor_id: str | None = None
    confirmed_by: str | None = None
    rejected_by: str | None = None
    rejection_reason: str | None = None


class FactResponse(BaseModel):
    id: str
    fact_type: str
    subject: str
    predicate: str
    value: str
    source_document_id: str
    source_version_id: str
    source_chunk_id: str
    confidence: float | None = None
    verification_status: str
    created_by: str | None = None
    confirmed_by: str | None = None
    confirmed_at: str | None = None
    rejected_by: str | None = None
    rejected_at: str | None = None
    rejection_reason: str | None = None
    audit_event_id: str | None = None
    stale_source_version: bool
    source_version_is_latest: bool
    created_at: str
    updated_at: str


class FactReviewAuditResponse(BaseModel):
    event_type: str
    actor: str | None = None
    timestamp: str
    reason: str | None = None
    metadata: dict
