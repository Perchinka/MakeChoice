from fastapi import FastAPI
from src.config import settings
from src.logging import setup_logging
from src.infrastructure.db.session import engine
from src.infrastructure.db.models import Base
from src.api.routers import admin_router, auth_router


def create_app() -> FastAPI:
    setup_logging()

    app = FastAPI(title=settings.APP_NAME)

    app.include_router(admin_router)
    app.include_router(auth_router, prefix="/auth", tags=["auth"])
    # app.include_router(courses.router, prefix="/courses", tags=["courses"])
    # app.include_router(choices.router, prefix="/choices", tags=["choices"])

    return app


app = create_app()
