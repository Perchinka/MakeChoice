from fastapi import APIRouter, Request, HTTPException, status, Depends
from pydantic import BaseModel
import jwt

from src.services.user_service import UserService
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
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    try:
        payload = jwt.decode(
            token,
            settings.SESSION_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
        )
    except jwt.PyJWTError:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication token"
        )

    # you can also verify against the DB if needed:
    # svc = UserService(uow)
    # user = svc.get_by_id(payload["sub"])

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
