from fastapi import APIRouter
from .auth import router as auth_router
from .choices import router as choices_router

__all__ = ["auth_router"]

admin_router = APIRouter(
    prefix="/admin",
    tags=["admin"],
)

# # /admin/courses/*
# admin_router.include_router(
#     courses_router,
#     prefix="/courses",
#     tags=["admin-courses"],
# )

# /admin/choices/*
admin_router.include_router(
    choices_router,
    prefix="/choices",
    tags=["admin-choices"],
)
