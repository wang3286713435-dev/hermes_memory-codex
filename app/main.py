from fastapi import FastAPI

from app.api.router import api_router
from app.api.routes.health import router as health_router
from app.core.config import settings
from app.core.logging import configure_logging
from app.db.base import Base
from app.db.session import engine
from app import models  # noqa: F401


def create_app() -> FastAPI:
    configure_logging()
    app = FastAPI(
        title=settings.app_name,
        debug=settings.app_debug,
        version="0.1.0",
    )
    app.include_router(api_router, prefix=settings.api_v1_prefix)
    app.include_router(health_router, tags=["health"])
    app.include_router(health_router, prefix=settings.api_v1_prefix, tags=["health"])

    @app.on_event("startup")
    def create_tables_for_mvp() -> None:
        if settings.db_auto_create_tables:
            Base.metadata.create_all(bind=engine)

    return app


app = create_app()
