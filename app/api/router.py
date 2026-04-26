from fastapi import APIRouter

from app.api.routes import agent, documents, facts, retrieval

api_router = APIRouter()
api_router.include_router(documents.router, prefix="/documents", tags=["documents"])
api_router.include_router(retrieval.router, prefix="/retrieval", tags=["retrieval"])
api_router.include_router(agent.router, prefix="/agent", tags=["agent"])
api_router.include_router(facts.router, prefix="/facts", tags=["facts"])
