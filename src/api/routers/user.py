from fastapi import APIRouter, Request, HTTPException, status, Depends
from pydantic import BaseModel
import jwt

from src.config import settings

router = APIRouter()


class MeResponse(BaseModel):
    sub: str
    email: str
    name: str
    is_admin: bool


def get_current_user(request: Request) -> MeResponse:
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated"
        )

    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,  # ←– use JWT_SECRET_KEY
            algorithms=[settings.JWT_ALGORITHM],
        )
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token",
        )

    return MeResponse(
        sub=payload["sub"],
        email=payload.get("email", ""),
        name=payload.get("name", ""),
        is_admin=payload.get("is_admin", False),
    )


@router.get("/me", response_model=MeResponse)
async def me(user: MeResponse = Depends(get_current_user)):
    """
    Returns the current logged-in user, or 401 if not authenticated.
    """
    return user
