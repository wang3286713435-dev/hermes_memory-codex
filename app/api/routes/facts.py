from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi import Header
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.facts import (
    FactCreateFromEvidenceRequest,
    FactResponse,
    FactReviewAuditResponse,
    FactStatusUpdateRequest,
)
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
        return _to_response(service.view_for_fact(fact))
    except FactValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("", response_model=list[FactResponse])
def list_facts(
    verification_status: str | None = None,
    source_document_id: str | None = None,
    source_version_id: str | None = None,
    subject: str | None = None,
    predicate: str | None = None,
    fact_type: str | None = None,
    created_by: str | None = None,
    confirmed_by: str | None = None,
    db: Session = Depends(get_db),
    x_requester_id: Annotated[str | None, Header(alias="X-Requester-Id")] = None,
    x_tenant_id: Annotated[str | None, Header(alias="X-Tenant-Id")] = None,
    x_requester_role: Annotated[str | None, Header(alias="X-Requester-Role")] = None,
) -> list[FactResponse]:
    try:
        return [
            _to_response(view)
            for view in FactService(db).list_facts(
                verification_status=verification_status,
                source_document_id=source_document_id,
                source_version_id=source_version_id,
                subject=subject,
                predicate=predicate,
                fact_type=fact_type,
                created_by=created_by,
                confirmed_by=confirmed_by,
                requester_id=x_requester_id,
                tenant_id=x_tenant_id,
                role=x_requester_role,
            )
        ]
    except FactValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/confirmed", response_model=list[FactResponse])
def search_confirmed_facts(
    subject: str | None = None,
    predicate: str | None = None,
    fact_type: str | None = None,
    source_document_id: str | None = None,
    source_version_id: str | None = None,
    db: Session = Depends(get_db),
    x_requester_id: Annotated[str | None, Header(alias="X-Requester-Id")] = None,
    x_tenant_id: Annotated[str | None, Header(alias="X-Tenant-Id")] = None,
    x_requester_role: Annotated[str | None, Header(alias="X-Requester-Role")] = None,
) -> list[FactResponse]:
    return [
        _to_response(view)
        for view in FactService(db).search_confirmed_facts(
            subject=subject,
            predicate=predicate,
            fact_type=fact_type,
            source_document_id=source_document_id,
            source_version_id=source_version_id,
            requester_id=x_requester_id,
            tenant_id=x_tenant_id,
            role=x_requester_role,
        )
    ]


@router.get("/pending", response_model=list[FactResponse])
def list_pending_facts(
    db: Session = Depends(get_db),
    x_requester_id: Annotated[str | None, Header(alias="X-Requester-Id")] = None,
    x_tenant_id: Annotated[str | None, Header(alias="X-Tenant-Id")] = None,
    x_requester_role: Annotated[str | None, Header(alias="X-Requester-Role")] = None,
) -> list[FactResponse]:
    return [
        _to_response(view)
        for view in FactService(db).list_pending_facts(
            requester_id=x_requester_id,
            tenant_id=x_tenant_id,
            role=x_requester_role,
        )
    ]


@router.get("/by-document/{document_id}", response_model=list[FactResponse])
def list_facts_by_document(
    document_id: str,
    db: Session = Depends(get_db),
    x_requester_id: Annotated[str | None, Header(alias="X-Requester-Id")] = None,
    x_tenant_id: Annotated[str | None, Header(alias="X-Tenant-Id")] = None,
    x_requester_role: Annotated[str | None, Header(alias="X-Requester-Role")] = None,
) -> list[FactResponse]:
    return [
        _to_response(view)
        for view in FactService(db).list_facts_by_document(
            document_id,
            requester_id=x_requester_id,
            tenant_id=x_tenant_id,
            role=x_requester_role,
        )
    ]


@router.get("/by-subject/{subject}", response_model=list[FactResponse])
def list_facts_by_subject(
    subject: str,
    db: Session = Depends(get_db),
    x_requester_id: Annotated[str | None, Header(alias="X-Requester-Id")] = None,
    x_tenant_id: Annotated[str | None, Header(alias="X-Tenant-Id")] = None,
    x_requester_role: Annotated[str | None, Header(alias="X-Requester-Role")] = None,
) -> list[FactResponse]:
    return [
        _to_response(view)
        for view in FactService(db).list_facts_by_subject(
            subject,
            requester_id=x_requester_id,
            tenant_id=x_tenant_id,
            role=x_requester_role,
        )
    ]


@router.post("/{fact_id}/confirm", response_model=FactResponse)
def confirm_fact(
    fact_id: str,
    request: FactStatusUpdateRequest,
    db: Session = Depends(get_db),
) -> FactResponse:
    service = FactService(db)
    try:
        fact = service.confirm_fact(fact_id, confirmed_by=request.confirmed_by, actor_id=request.actor_id)
        return _to_response(service.view_for_fact(fact))
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
        fact = service.reject_fact(
            fact_id,
            rejected_by=request.rejected_by,
            rejection_reason=request.rejection_reason,
            actor_id=request.actor_id,
        )
        return _to_response(service.view_for_fact(fact))
    except FactValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/{fact_id}/review-history", response_model=list[FactReviewAuditResponse])
def list_fact_review_history(
    fact_id: str,
    db: Session = Depends(get_db),
) -> list[FactReviewAuditResponse]:
    try:
        return [
            FactReviewAuditResponse(
                event_type=event.event_type,
                actor=event.actor,
                timestamp=event.timestamp.isoformat(),
                reason=event.reason,
                metadata=event.metadata,
            )
            for event in FactService(db).list_review_history(fact_id)
        ]
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
        confirmed_at=fact.confirmed_at.isoformat() if fact.confirmed_at else None,
        rejected_by=fact.rejected_by,
        rejected_at=fact.rejected_at.isoformat() if fact.rejected_at else None,
        rejection_reason=fact.rejection_reason,
        audit_event_id=fact.audit_event_id,
        stale_source_version=view.stale_source_version,
        source_version_is_latest=view.source_version_is_latest,
        latest_version_id=view.latest_version_id,
        source_excerpt=view.source_excerpt,
        source_location=view.source_location,
        created_at=fact.created_at.isoformat(),
        updated_at=fact.updated_at.isoformat(),
    )
