from fastapi import APIRouter, Request, HTTPException, status, Depends
import jwt

from src.config import settings

from src.api.models import UserResponse

router = APIRouter()


def get_current_user(request: Request) -> UserResponse:
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated"
        )

    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
        )
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token",
        )

    return UserResponse(
        sub=payload["sub"],
        email=payload.get("email", ""),
        name=payload.get("name", ""),
        is_admin=payload.get("is_admin", False),
    )


@router.get("/me", response_model=UserResponse)
async def me(user: UserResponse = Depends(get_current_user)):
    """
    Returns the current logged-in user, or 401 if not authenticated.
    """
    return user
