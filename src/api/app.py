from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from src.config import settings
from src.domain.exceptions import AppError
from src.logging import setup_logging
from src.api.routers import auth_router, users_router, electives_router, choices_router
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from src.api.error_handler import code_map


def create_app() -> FastAPI:
    setup_logging()

    app = FastAPI(title=settings.APP_NAME, openapi_prefix="/api")

    @app.exception_handler(AppError)
    async def app_error_handler(request: Request, exc: AppError):
        status_code = code_map.get(type(exc), status.HTTP_500_INTERNAL_SERVER_ERROR)
        return JSONResponse(status_code=status_code, content={"detail": str(exc)})

    app.add_middleware(
        SessionMiddleware,
        secret_key=settings.SESSION_SECRET_KEY,
        session_cookie="session",
        max_age=14 * 24 * 3600,
        same_site="lax",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=[settings.FRONTEND_URL],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(auth_router, prefix="/auth", tags=["auth"])
    app.include_router(users_router, prefix="/users", tags=["users"])
    app.include_router(electives_router, tags=["electives"])
    app.include_router(choices_router, tags=["choices"])

    return app


app = create_app()
