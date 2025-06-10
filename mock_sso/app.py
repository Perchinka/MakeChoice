import os
import time
import base64
from uuid import uuid4
from fastapi import FastAPI, Request, HTTPException, Form, Header
from fastapi.responses import RedirectResponse
from jose import jwt

app = FastAPI()

ISSUER_URL = os.getenv("ISSUER_URL", "http://sso:80")
CLIENT_ID = os.getenv("CLIENT_ID", "your-client-id")
CLIENT_SECRET = os.getenv("CLIENT_SECRET", "your-client-secret")
SECRET_KEY = os.getenv("SECRET_KEY", "dev_sso_secret")

# In‐memory store: code, nonce
nonce_store: dict[str, str] = {}


@app.get("/.well-known/openid-configuration")
def discovery():
    return {
        "issuer": ISSUER_URL,
        "authorization_endpoint": f"{ISSUER_URL}/authorize",
        "token_endpoint": f"{ISSUER_URL}/token",
        "jwks_uri": f"{ISSUER_URL}/jwks",
        "response_types_supported": ["code"],
        "grant_types_supported": ["authorization_code"],
        "scopes_supported": ["openid", "email", "profile"],
        "id_token_signing_alg_values_supported": ["HS256"],
        "token_endpoint_auth_methods_supported": [
            "client_secret_basic",
            "client_secret_post",
        ],
    }


@app.get("/authorize")
def authorize(
    response_type: str,
    client_id: str,
    redirect_uri: str,
    scope: str,
    state: str,
    nonce: str,
):
    if response_type != "code":
        raise HTTPException(400, "Only response_type=code is supported")
    if client_id != CLIENT_ID:
        raise HTTPException(400, "Invalid client_id")

    # generate a one‐time code and remember its nonce
    code = uuid4().hex
    nonce_store[code] = nonce

    # redirect back with code and state
    return RedirectResponse(f"{redirect_uri}?code={code}&state={state}")


@app.post("/token")
async def token(
    request: Request,
    grant_type: str = Form(...),
    code: str = Form(...),
    redirect_uri: str = Form(...),
    client_id: str = Form(None),
    client_secret: str = Form(None),
    authorization: str = Header(None),
):
    # allow HTTP Basic as well as client_secret_post
    if authorization and authorization.startswith("Basic "):
        import base64 as _b64

        creds = _b64.b64decode(authorization[6:]).decode()
        client_id, client_secret = creds.split(":", 1)

    if grant_type != "authorization_code" or code not in nonce_store:
        raise HTTPException(400, "Invalid grant_type or code")

    if client_id != CLIENT_ID or client_secret != CLIENT_SECRET:
        raise HTTPException(401, "Invalid client credentials")

    # retrieve and remove the nonce
    nonce = nonce_store.pop(code, "")

    now = int(time.time())
    payload = {
        "iss": ISSUER_URL,
        "sub": "dev-user-123",
        "aud": client_id,
        "exp": now + 3600,
        "iat": now,
        "nonce": nonce,  # ← embed correct nonce
        "email": "dev@example.com",
        "commonname": "Dev User",
        "group": ["Innopoints_Admins"],
    }
    id_token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

    payload = {
        "access_token": "dev-access-token",
        "token_type": "Bearer",
        "expires_in": 3600,
        "id_token": id_token,
    }

    __import__("pprint").pprint(payload)

    return payload


@app.get("/jwks")
def jwks():
    k = base64.urlsafe_b64encode(SECRET_KEY.encode()).rstrip(b"=").decode()
    return {"keys": [{"kty": "oct", "kid": "dev-key", "k": k}]}
