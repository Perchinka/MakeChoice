import os
from typing import Any


class Settings:
    APP_NAME: str = os.getenv("APP_NAME", "elec-api")
    ENV: str = os.getenv("ENV", "development")  # development|staging|production

    # Database (required)
    DATABASE_URL: str = os.environ["DATABASE_URL"]
    SQL_ECHO: bool = os.getenv("SQL_ECHO", "false").lower() in ("1", "true", "yes")

    # JWT (required)
    JWT_SECRET_KEY: str = os.environ["JWT_SECRET_KEY"]
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(
        os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60")
    )

    SSO_CLIENT_ID: str = os.getenv("SSO_CLIENT_ID", "your-client-id")
    SSO_CLIENT_SECRET: str = os.getenv("SSO_CLIENT_SECRET", "your-client-secret")
    SSO_DISCOVERY_URL: str = os.getenv(
        "SSO_DISCOVERY_URL", "http://sso/.well-known/openid-configuration"
    )

    SESSION_SECRET_KEY: str = os.getenv("SESSION_SECRET_KEY", "some-random-key")


# from src.config import settings
settings = Settings()
