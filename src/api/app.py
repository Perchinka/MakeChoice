from fastapi import FastAPI
from src.config import settings
from src.logging import setup_logging
from src.infrastructure.db.session import engine
from src.infrastructure.db.models import Base
from src.api.routers import admin_router, auth_router
from src.api.routers.user import router as users_router
from starlette.middleware.sessions import SessionMiddleware


def create_app() -> FastAPI:
    setup_logging()

    app = FastAPI(title=settings.APP_NAME)

    app.add_middleware(
        SessionMiddleware,
        secret_key=settings.SESSION_SECRET_KEY,
        session_cookie="session",
        max_age=14 * 24 * 3600,  # session lifetime in seconds
        same_site="lax",
    )

    app.include_router(admin_router)
    app.include_router(auth_router, prefix="/auth", tags=["auth"])
    app.include_router(users_router, prefix="/users", tags=["users"])

    return app


app = create_app()
