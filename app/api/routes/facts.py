from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.document import DocumentVersion
from app.schemas.facts import FactCreateFromEvidenceRequest, FactResponse, FactStatusUpdateRequest
from app.services.facts import FactService, FactValidationError, FactView

router = APIRouter()


@router.post("", response_model=FactResponse)
def create_fact_from_evidence(
    request: FactCreateFromEvidenceRequest,
    db: Session = Depends(get_db),
) -> FactResponse:
    service = FactService(db)
    try:
        fact = service.create_fact_from_evidence(**request.model_dump())
        version = db.get(DocumentVersion, fact.source_version_id)
        return _to_response(FactView(fact=fact, source_version_is_latest=bool(version and version.is_latest)))
    except FactValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/by-document/{document_id}", response_model=list[FactResponse])
def list_facts_by_document(document_id: str, db: Session = Depends(get_db)) -> list[FactResponse]:
    return [_to_response(view) for view in FactService(db).list_facts_by_document(document_id)]


@router.get("/by-subject/{subject}", response_model=list[FactResponse])
def list_facts_by_subject(subject: str, db: Session = Depends(get_db)) -> list[FactResponse]:
    return [_to_response(view) for view in FactService(db).list_facts_by_subject(subject)]


@router.post("/{fact_id}/confirm", response_model=FactResponse)
def confirm_fact(
    fact_id: str,
    request: FactStatusUpdateRequest,
    db: Session = Depends(get_db),
) -> FactResponse:
    service = FactService(db)
    try:
        fact = service.confirm_fact(fact_id, actor_id=request.actor_id)
        version = db.get(DocumentVersion, fact.source_version_id)
        return _to_response(FactView(fact=fact, source_version_is_latest=bool(version and version.is_latest)))
    except FactValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/{fact_id}/reject", response_model=FactResponse)
def reject_fact(
    fact_id: str,
    request: FactStatusUpdateRequest,
    db: Session = Depends(get_db),
) -> FactResponse:
    service = FactService(db)
    try:
        fact = service.mark_fact_rejected(fact_id, actor_id=request.actor_id)
        version = db.get(DocumentVersion, fact.source_version_id)
        return _to_response(FactView(fact=fact, source_version_is_latest=bool(version and version.is_latest)))
    except FactValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


def _to_response(view: FactView) -> FactResponse:
    fact = view.fact
    return FactResponse(
        id=fact.id,
        fact_type=fact.fact_type,
        subject=fact.subject,
        predicate=fact.predicate,
        value=fact.value,
        source_document_id=fact.source_document_id,
        source_version_id=fact.source_version_id,
        source_chunk_id=fact.source_chunk_id,
        confidence=fact.confidence,
        verification_status=fact.verification_status,
        created_by=fact.created_by,
        confirmed_by=fact.confirmed_by,
        audit_event_id=fact.audit_event_id,
        stale_source_version=view.stale_source_version,
        source_version_is_latest=view.source_version_is_latest,
        created_at=fact.created_at.isoformat(),
        updated_at=fact.updated_at.isoformat(),
    )
