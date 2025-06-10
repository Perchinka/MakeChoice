from fastapi import APIRouter, Request, HTTPException, status, Response
from authlib.integrations.starlette_client import OAuthError

from src.infrastructure.sso.innopolis_oidc import oauth
from src.infrastructure.db.uow import UnitOfWork
from src.services.user_service import UserService
from src.config import settings

router = APIRouter()


@router.get("/login")
async def login(request: Request):
    """
    Redirect the user to the Innopolis SSO authorization endpoint.
    """
    redirect_uri = request.url_for("auth_callback")
    return await oauth.innopolis_sso.authorize_redirect(request, redirect_uri)


import logging

logger = logging.getLogger(__name__)


@router.get("/callback")
async def auth_callback(request: Request):
    """
    Handle the OIDC callback: exchange code, parse ID token (or hit userinfo),
    create/update local user, then issue a JWT in a cookie.
    """
    try:
        token = await oauth.innopolis_sso.authorize_access_token(request)
        logger.debug("SSO token response keys: %s", list(token.keys()))

        # 1) Authlib may already have decoded the id_token into userinfo:
        userinfo = token.get("userinfo")

        # 2) If not, but we have a raw id_token, parse it:
        if not userinfo and token.get("id_token"):
            userinfo = await oauth.innopolis_sso.parse_id_token(request, token)

        # 3) As a last resort, call the userinfo endpoint:
        if not userinfo:
            userinfo = await oauth.innopolis_sso.userinfo(request, token)

    except OAuthError as err:
        logger.error("SSO login failed: %s", err)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="SSO login failed",
        )

    if not userinfo:
        logger.error("No userinfo could be extracted from token: %s", token)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not obtain user info from SSO",
        )

    # Now you have a fully populated userinfo dict
    sso_id = userinfo["sub"]
    email = userinfo.get("email", "")
    name = userinfo.get("name") or userinfo.get("commonname", "")
    is_admin = "Innopoints_Admins" in userinfo.get("group", [])

    with UnitOfWork() as uow:
        svc = UserService(uow)
        user = uow.users.get_by_sso_id(sso_id)
        if not user:
            user = svc.register_sso(
                sso_id=sso_id,
                name=name,
                email=email,
                is_admin=is_admin,
            )
        else:
            user.name = name
            user.email = email
            user.is_admin = is_admin
            uow.users.update(user)

    access_token = svc.create_access_token(user)

    # Issue JWT in a cookie and redirect home
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
