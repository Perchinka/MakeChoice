from authlib.integrations.starlette_client import OAuth
from src.config import settings

oauth = OAuth()

oauth.register(
    name="innopolis_sso",
    server_metadata_url=settings.SSO_DISCOVERY_URL,
    client_id=settings.SSO_CLIENT_ID,
    client_secret=settings.SSO_CLIENT_SECRET,
    client_kwargs={"scope": "openid email profile"},
)
