import base64
import os
import time
from uuid import uuid4
from fastapi import FastAPI, Header, Request, Form, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from jose import jwt

app = FastAPI()

ISSUER_URL = os.getenv("ISSUER_URL", "http://sso:80")
CLIENT_ID = os.getenv("CLIENT_ID", "your-client-id")
CLIENT_SECRET = os.getenv("CLIENT_SECRET", "your-client-secret")
SECRET_KEY = os.getenv("SECRET_KEY", "dev_sso_secret")

# in-memory: auth code → (nonce, user)
nonce_store: dict[str, tuple[str, str]] = {}


@app.get("/.well-known/openid-configuration")
def discovery():
    return {
        "issuer": ISSUER_URL,
        "authorization_endpoint": f"http://localhost:8080/authorize",
        "token_endpoint": f"{ISSUER_URL}/token",
        "jwks_uri": f"{ISSUER_URL}/jwks",
        "response_types_supported": ["code"],
        "grant_types_supported": ["authorization_code"],
        "scopes_supported": ["openid", "email", "profile"],
        "id_token_signing_alg_values_supported": ["HS256"],
    }


@app.get("/authorize", response_class=HTMLResponse)
async def authorize_form(
    response_type: str,
    client_id: str,
    redirect_uri: str,
    scope: str,
    state: str,
    nonce: str,
):
    if response_type != "code" or client_id != CLIENT_ID:
        raise HTTPException(400, "Bad authorize request")
    return f"""
    <!DOCTYPE html>
    <html><head><meta charset="utf-8"><title>Mock SSO</title></head>
    <body style="text-align:center;font-family:sans-serif;margin-top:50px;">
      <h1>Mock SSO Login</h1>
      <form method="post" action="/authorize">
        <input type="hidden" name="response_type" value="{response_type}"/>
        <input type="hidden" name="client_id"      value="{client_id}"/>
        <input type="hidden" name="redirect_uri"   value="{redirect_uri}"/>
        <input type="hidden" name="state"          value="{state}"/>
        <input type="hidden" name="nonce"          value="{nonce}"/>
        <button name="user" value="student-001" style="margin:0 1em;padding:1em 2em;">
          Login as Student
        </button>
        <button name="user" value="admin-001" style="margin:0 1em;padding:1em 2em;">
          Login as Admin
        </button>
      </form>
    </body>
    </html>
    """


@app.post("/authorize")
async def authorize_submit(
    response_type: str = Form(...),
    client_id: str = Form(...),
    redirect_uri: str = Form(...),
    state: str = Form(...),
    nonce: str = Form(...),
    user: str = Form(...),
):
    if response_type != "code" or client_id != CLIENT_ID:
        raise HTTPException(400, "Invalid authorize submission")

    code = uuid4().hex
    nonce_store[code] = (nonce, user)

    # 302 so browser will GET callback
    return RedirectResponse(
        url=f"{redirect_uri}?code={code}&state={state}", status_code=302
    )


@app.post("/token")
async def token(
    grant_type: str = Form(...),
    code: str = Form(...),
    redirect_uri: str = Form(...),
    client_id: str = Form(None),
    client_secret: str = Form(None),
    authorization: str = Header(None),
):
    if authorization and authorization.startswith("Basic "):
        creds = base64.b64decode(authorization[6:]).decode()
        client_id, client_secret = creds.split(":", 1)

    if grant_type != "authorization_code" or code not in nonce_store:
        raise HTTPException(400, "Bad grant or code")

    if client_id != CLIENT_ID or client_secret != CLIENT_SECRET:
        raise HTTPException(401, "Invalid client credentials")

    nonce, user = nonce_store.pop(code)

    now = int(time.time())

    is_admin = user.startswith("admin-")
    id_payload = {
        "iss": ISSUER_URL,
        "sub": user,
        "aud": client_id,
        "exp": now + 3600,
        "iat": now,
        "nonce": nonce,
        "email": f"{user}@example.com",
        "commonname": "Admin User" if is_admin else "Student User",
        "group": ["Innopoints_Admins"] if is_admin else [],
    }
    id_token = jwt.encode(id_payload, SECRET_KEY, algorithm="HS256")

    return {
        "access_token": "dev-access-token",
        "token_type": "Bearer",
        "expires_in": 3600,
        "id_token": id_token,
    }


@app.get("/jwks")
def jwks():
    k = base64.urlsafe_b64encode(SECRET_KEY.encode()).rstrip(b"=").decode()
    return {"keys": [{"kty": "oct", "kid": "dev-key", "k": k}]}
