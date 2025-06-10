from fastapi import APIRouter, Depends
from src.api.models import UserResponse

from .auth import get_current_user

router = APIRouter()


@router.get("/me", response_model=UserResponse)
async def me(user: UserResponse = Depends(get_current_user)):
    """
    Returns the current logged-in user, or 401 if not authenticated.
    """
    return user
