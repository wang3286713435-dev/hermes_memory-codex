from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.retrieval import SearchRequest, SearchResponse
from app.services.retrieval.service import RetrievalService

router = APIRouter()


@router.post("/search", response_model=SearchResponse)
def search(request: SearchRequest, db: Session = Depends(get_db)) -> SearchResponse:
    service = RetrievalService(db=db)
    return service.search(request)

