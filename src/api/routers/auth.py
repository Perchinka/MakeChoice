import logging
from uuid import UUID
import jwt

from fastapi import APIRouter, Depends, Request, HTTPException, status, Response
from authlib.integrations.starlette_client import OAuthError

from src.api.dependencies import get_uow
from src.api.models import UserResponse

from src.infrastructure.sso.innopolis_oidc import oauth
from src.services.user_service import UserService
from src.config import settings

router = APIRouter()


@router.get("/login")
async def login(request: Request):
    """
    Redirect the user to the Innopolis SSO authorization endpoint.
    """
    redirect_uri = request.url_for("auth_callback")
    return await oauth.innopolis_sso.authorize_redirect(request, redirect_uri)  # type: ignore


@router.get("/callback")
async def auth_callback(
    request: Request, user_service=Depends(UserService), uow=Depends(get_uow)
):
    """
    Handle the OIDC callback: exchange code, parse ID token (or hit userinfo),
    create/update local user, then issue a JWT in a cookie.
    """
    try:
        token = await oauth.innopolis_sso.authorize_access_token(request)  # type: ignore
        logging.debug("SSO token response keys: %s", list(token.keys()))

        userinfo = token.get("userinfo")

        if not userinfo and token.get("id_token"):
            userinfo = await oauth.innopolis_sso.parse_id_token(request, token)  # type: ignore

        if not userinfo:
            userinfo = await oauth.innopolis_sso.userinfo(request, token)  # type: ignore

    except OAuthError as err:
        logging.error("SSO login failed: %s", err)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="SSO login failed",
        )

    if not userinfo:
        logging.error("No userinfo could be extracted from token: %s", token)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not obtain user info from SSO",
        )

    sso_id = userinfo["sub"]
    email = userinfo.get("email", "")
    name = userinfo.get("name") or userinfo.get("commonname", "")
    is_admin = "Innopoints_Admins" in userinfo.get("group", [])

    user = user_service.register_sso(
        sso_id=sso_id, name=name, email=email, is_admin=is_admin, uow=uow
    )
    access_token = user_service.create_access_token(user)

    resp = Response(status_code=status.HTTP_302_FOUND)
    resp.headers["Location"] = "/"
    resp.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=(settings.ENV == "production"),
        max_age=60 * settings.ACCESS_TOKEN_EXPIRE_MINUTES,
        samesite="lax",
    )
    return resp


def get_current_user(request: Request) -> UserResponse:
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated"
        )

    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
        )
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )

    return UserResponse(
        sub=payload["sub"], email=payload["email"], name=payload["name"]
    )


def require_admin(
    user: UserResponse = Depends(get_current_user),
    uow=Depends(get_uow),
    user_service: UserService = Depends(UserService),
) -> UserResponse:
    try:
        user_id = UUID(user.sub)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid user id")

    if not user_service.is_admin(user_id, uow=uow):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Admin privileges required"
        )

    return user
