"""
Authentication routes: login, OIDC callback, logout, and self-service
registration via the Okta Users API.
"""
import logging
import re

import requests as http_requests
from flask import current_app, redirect, render_template, request, session, url_for

from . import auth_bp
from ..extensions import oauth
from ..database import service as db_svc

logger = logging.getLogger(__name__)

_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


# ── Login ──────────────────────────────────────────────────────────────────

@auth_bp.route("/login")
def login():
    if session.get("user"):
        return redirect(url_for("main.dashboard"))

    okta_domain = current_app.config["OKTA_DOMAIN"]
    client_id = current_app.config["OKTA_CLIENT_ID"]

    if not okta_domain or not client_id:
        return render_template("login.html", okta_configured=False)

    redirect_uri = url_for("auth.callback", _external=True)
    return oauth.okta.authorize_redirect(redirect_uri)


# ── OIDC Callback ──────────────────────────────────────────────────────────

@auth_bp.route("/authorization-code/callback")
def callback():
    token = oauth.okta.authorize_access_token()
    user_info = token.get("userinfo") or {}

    full_name   = user_info.get("name", "")
    given_name  = user_info.get("given_name", "")
    family_name = user_info.get("family_name", "")

    if not given_name and full_name and " " in full_name:
        parts = full_name.split(" ", 1)
        given_name  = parts[0]
        family_name = parts[1] if not family_name else family_name

    email = user_info.get("email", "")
    if not given_name:
        given_name = email.split("@")[0].split(".")[0].capitalize()

    okta_sub = user_info.get("sub", "")

    user = db_svc.get_or_create_user(
        okta_sub=okta_sub,
        email=email,
        given_name=given_name,
        family_name=family_name,
    )

    session["user"] = user.to_session_dict()
    next_url = session.pop("next", url_for("main.dashboard"))
    return redirect(next_url)


# ── Logout ─────────────────────────────────────────────────────────────────

@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))


# ── Self-service registration ──────────────────────────────────────────────

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if session.get("user"):
        return redirect(url_for("main.dashboard"))

    if request.method == "GET":
        return render_template("register.html", error=None, success=False, form={})

    # ── Collect form fields ────────────────────────────────────────────────
    first_name       = request.form.get("first_name", "").strip()
    last_name        = request.form.get("last_name",  "").strip()
    email            = request.form.get("email",      "").strip().lower()
    password         = request.form.get("password",   "")
    confirm_password = request.form.get("confirm_password", "")

    form = {
        "first_name": first_name,
        "last_name":  last_name,
        "email":      email,
    }

    # ── Validate ───────────────────────────────────────────────────────────
    error = _validate(first_name, last_name, email, password, confirm_password)
    if error:
        return render_template("register.html", error=error, success=False, form=form)

    # ── reCAPTCHA verification ─────────────────────────────────────────────
    captcha_error = _verify_recaptcha(request.form.get("g-recaptcha-response", ""))
    if captcha_error:
        return render_template("register.html", error=captcha_error, success=False, form=form)

    api_token   = current_app.config["OKTA_API_TOKEN"]
    okta_domain = current_app.config["OKTA_DOMAIN"]

    if not api_token:
        return render_template(
            "register.html",
            error="Registration is currently unavailable. Contact the administrator.",
            success=False, form=form,
        )

    headers = {
        "Authorization": f"SSWS {api_token}",
        "Content-Type":  "application/json",
        "Accept":        "application/json",
    }

    # ── Create + activate user with password in one API call ───────────────
    payload = {
        "profile": {
            "firstName": first_name,
            "lastName":  last_name,
            "email":     email,
            "login":     email,
        },
        "credentials": {
            "password": {"value": password},
        },
    }

    try:
        resp = http_requests.post(
            f"https://{okta_domain}/api/v1/users?activate=true",
            headers=headers,
            json=payload,
            timeout=15,
        )

        if resp.status_code not in (200, 201):
            return render_template(
                "register.html",
                error=_okta_error(resp),
                success=False, form=form,
            )

        logger.info("Registered new user: %s", email)
        return render_template(
            "register.html",
            error=None,
            success=True,
            first_name=first_name,
            email=email,
            form={},
        )

    except Exception as exc:
        logger.error("Okta registration error: %s", exc)
        return render_template(
            "register.html",
            error="Could not reach authentication server. Please try again.",
            success=False, form=form,
        )


# ── Helpers ────────────────────────────────────────────────────────────────

def _validate(first_name, last_name, email, password, confirm_password) -> str | None:
    if not all([first_name, last_name, email, password, confirm_password]):
        return "All fields are required."
    if not _EMAIL_RE.match(email):
        return "Please enter a valid email address."
    if len(password) < 8:
        return "Password must be at least 8 characters."
    if not any(c.isupper() for c in password):
        return "Password must contain at least one uppercase letter."
    if not any(c.islower() for c in password):
        return "Password must contain at least one lowercase letter."
    if not any(c.isdigit() for c in password):
        return "Password must contain at least one number."
    if password != confirm_password:
        return "Passwords do not match."
    return None


def _verify_recaptcha(token: str) -> str | None:
    """Verify a reCAPTCHA v2 token. Returns an error string or None on success.
    Skipped silently if RECAPTCHA_SECRET_KEY is not configured."""
    secret = current_app.config["RECAPTCHA_SECRET_KEY"]
    if not secret:
        return None  # reCAPTCHA not configured — skip verification

    if not token:
        return "Please complete the CAPTCHA verification."

    try:
        resp = http_requests.post(
            "https://www.google.com/recaptcha/api/siteverify",
            data={"secret": secret, "response": token},
            timeout=10,
        )
        result = resp.json()
        if not result.get("success"):
            logger.warning("reCAPTCHA failed: %s", result.get("error-codes"))
            return "CAPTCHA verification failed. Please try again."
    except Exception as exc:
        logger.error("reCAPTCHA request error: %s", exc)
        return "CAPTCHA verification could not be completed. Please try again."

    return None


def _okta_error(resp) -> str:
    try:
        data = resp.json()
        causes = data.get("errorCauses", [])
        cause_msg = causes[0].get("errorSummary", "") if causes else ""
        return cause_msg or data.get("errorSummary") or f"Okta error {resp.status_code}"
    except Exception:
        return f"Okta error {resp.status_code}"
