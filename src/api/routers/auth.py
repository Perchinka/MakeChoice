import logging
from uuid import UUID

import jwt
from fastapi import APIRouter, Depends, Request, HTTPException, Response, status
from fastapi.responses import RedirectResponse
from authlib.integrations.starlette_client import OAuthError

from src.api.dependencies import get_uow
from src.api.models import UserResponse
from src.infrastructure.sso.innopolis_oidc import oauth
from src.services.user_service import UserService
from src.config import settings

router = APIRouter(tags=["auth"])


@router.post("/logout", status_code=204)
def logout(response: Response):
    """
    Clear the access_token cookie to log out the user.
    """
    response.delete_cookie(
        key="access_token",
        path="/",
        httponly=True,
        samesite="lax",
    )
    response.status_code = 204
    return response


@router.get("/login")
async def login(request: Request):
    """
    Redirect the user to the Innopolis SSO authorization endpoint.
    """
    redirect_uri = request.url_for("auth_callback")
    return await oauth.innopolis_sso.authorize_redirect(request, redirect_uri)  # type: ignore


@router.get("/callback")
async def auth_callback(
    request: Request,
    user_service: UserService = Depends(),
    uow=Depends(get_uow),
):
    """
    Handle the OIDC callback.
    """
    try:
        token = await oauth.innopolis_sso.authorize_access_token(request)  # type: ignore
        userinfo = token.get("userinfo") or {}
        if not userinfo and token.get("id_token"):
            userinfo = await oauth.innopolis_sso.parse_id_token(request, token)  # type: ignore
        if not userinfo:
            userinfo = await oauth.innopolis_sso.userinfo(request, token)  # type: ignore
    except OAuthError as err:
        logging.error("SSO login failed: %s", err)
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "SSO login failed")

    sub = userinfo["sub"]
    email = userinfo.get("email", "")
    name = userinfo.get("name") or userinfo.get("commonname") or ""
    role = "Admin" if "Innopoints_Admins" in userinfo.get("group", []) else "Student"

    user = user_service.register_sso(
        sso_id=sub, name=name, email=email, role=role, uow=uow
    )

    access_token = user_service.create_access_token(user)
    resp = RedirectResponse(settings.FRONTEND_URL, status_code=status.HTTP_302_FOUND)
    resp.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=(settings.ENV == "production"),
        max_age=60 * settings.ACCESS_TOKEN_EXPIRE_MINUTES,
        samesite="lax",
    )
    return resp


def get_current_user(
    request: Request,
    uow=Depends(get_uow),
) -> UserResponse:
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Not authenticated")

    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
        )
    except jwt.PyJWTError:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid token")

    user_id = UUID(payload["sub"])
    with uow:
        user = uow.users.get(user_id)
    if not user:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "User not found")

    return UserResponse(
        sub=str(user.id),
        email=user.email,
        name=user.name,
        role=user.role,
    )


def require_roles(*allowed: str):
    """
    Dependency factory: e.g. dependencies=[require_roles("Admin","Instructor")]
    """

    def _checker(user: UserResponse = Depends(get_current_user)):
        if user.role not in allowed:
            raise HTTPException(status.HTTP_403_FORBIDDEN, "Forbidden")
        return user

    return Depends(_checker)


# convenience aliases
require_admin = require_roles("Admin")
require_student = require_roles("Student")
require_instructor = require_roles("Instructor")
