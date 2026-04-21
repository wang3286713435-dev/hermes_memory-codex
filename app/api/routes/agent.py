from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.agent import AskRequest, AskResponse
from app.services.agent.service import AgentService

router = APIRouter()


@router.post("/ask", response_model=AskResponse)
def ask(request: AskRequest, db: Session = Depends(get_db)) -> AskResponse:
    service = AgentService(db=db)
    return service.ask(request)

