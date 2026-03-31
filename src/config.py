import os
import secrets


class Config:
    SECRET_KEY: str = os.environ.get("SECRET_KEY", secrets.token_hex(32))

    # Database — SQLite locally, PostgreSQL in production via DATABASE_URL
    SQLALCHEMY_DATABASE_URI: str = os.environ.get(
        "DATABASE_URL", "sqlite:///cybercert.db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    SQLALCHEMY_ENGINE_OPTIONS: dict = {
        "pool_pre_ping": True,
        "pool_recycle": 300,
    }

    # Okta OIDC
    OKTA_DOMAIN: str = os.environ.get("OKTA_DOMAIN", "")
    OKTA_CLIENT_ID: str = os.environ.get("OKTA_CLIENT_ID", "")
    OKTA_CLIENT_SECRET: str = os.environ.get("OKTA_CLIENT_SECRET", "")
    OKTA_API_TOKEN: str = os.environ.get("OKTA_API_TOKEN", "")

    # Application
    ADMIN_EMAIL: str = os.environ.get("ADMIN_EMAIL", "")
    APP_NAME: str = "CyberCert"
    PHASE: str = "Phase 1 — Okta Professional"
