from typing import Annotated

from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.retrieval import SearchRequest, SearchResponse
from app.services.retrieval.service import RetrievalService

router = APIRouter()


@router.post("/search", response_model=SearchResponse)
def search(
    request: SearchRequest,
    db: Session = Depends(get_db),
    x_requester_id: Annotated[str | None, Header(alias="X-Requester-Id")] = None,
    x_tenant_id: Annotated[str | None, Header(alias="X-Tenant-Id")] = None,
    x_requester_role: Annotated[str | None, Header(alias="X-Requester-Role")] = None,
) -> SearchResponse:
    extra = dict(request.filters.extra or {})
    if x_requester_id:
        request.user_id = request.user_id or x_requester_id
        extra.setdefault("requester_id", x_requester_id)
    if x_tenant_id:
        extra.setdefault("tenant_id", x_tenant_id)
    if x_requester_role:
        extra.setdefault("role", x_requester_role)
    request.filters.extra = extra
    service = RetrievalService(db=db)
    return service.search(request)
