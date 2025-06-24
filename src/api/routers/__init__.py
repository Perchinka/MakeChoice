from .auth import router as auth_router
from .choices import router as choices_router
from .users import router as users_router
from .courses import router as courses_router

__all__ = ["users_router", "choices_router", "auth_router", "courses_router"]
