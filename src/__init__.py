"""
CyberCert — application factory.

Usage:
    from src import create_app
    app = create_app()
"""
from __future__ import annotations

import logging
import os
from logging.handlers import RotatingFileHandler

from dotenv import load_dotenv
from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix

from .config import Config
from .database import db, migrate
from .extensions import oauth


def create_app(config_class: type = Config) -> Flask:
    """Create and configure the Flask application."""
    load_dotenv()

    app = Flask(
        __name__,
        template_folder="../templates",
        static_folder="../static",
    )
    app.config.from_object(config_class)

    # Trust X-Forwarded-Proto from Cloud Run / reverse proxy
    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

    # ── Extensions ─────────────────────────────────────────────────────────
    oauth.init_app(app)
    _register_okta(app)
    db.init_app(app)
    migrate.init_app(app, db)

    # Create tables if they don't exist (idempotent)
    with app.app_context():
        from .database import models  # noqa: F401
        db.create_all()

    # ── Blueprints ─────────────────────────────────────────────────────────
    from .auth import auth_bp
    from .main import main_bp
    from .study import study_bp
    from .quiz import quiz_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(study_bp)
    app.register_blueprint(quiz_bp)

    # ── Jinja globals ──────────────────────────────────────────────────────
    from .auth.decorators import current_user
    app.jinja_env.globals["current_user"] = current_user

    # ── Logging ────────────────────────────────────────────────────────────
    _configure_logging(app)

    return app


def _configure_logging(app: Flask) -> None:
    """Write INFO+ logs to logs/cybercert.log with rotation."""
    os.makedirs("logs", exist_ok=True)
    handler = RotatingFileHandler(
        "logs/cybercert.log", maxBytes=2_000_000, backupCount=5
    )
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    ))
    app.logger.setLevel(logging.DEBUG)
    app.logger.addHandler(handler)
    # Also capture werkzeug and root logger to the same file
    for name in ("werkzeug", "src"):
        lg = logging.getLogger(name)
        lg.setLevel(logging.DEBUG)
        lg.addHandler(handler)


def _register_okta(app: Flask) -> None:
    """Register the Okta OIDC client with authlib."""
    okta_domain = app.config["OKTA_DOMAIN"]
    if not okta_domain:
        return
    oauth.register(
        name="okta",
        client_id=app.config["OKTA_CLIENT_ID"],
        client_secret=app.config["OKTA_CLIENT_SECRET"],
        server_metadata_url=(
            f"https://{okta_domain}/oauth2/default/.well-known/openid-configuration"
        ),
        client_kwargs={
            "scope": "openid profile email",
            "code_challenge_method": "S256",  # PKCE
        },
    )
