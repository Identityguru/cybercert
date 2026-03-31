"""
Authentication routes: login, OIDC callback, logout, and self-service
registration via the Okta Users API.
"""
import logging

import requests as http_requests
from flask import current_app, redirect, render_template, session, url_for

from . import auth_bp
from ..extensions import oauth
from ..database import service as db_svc

logger = logging.getLogger(__name__)


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

    full_name = user_info.get("name", "")
    given_name = user_info.get("given_name", "")
    family_name = user_info.get("family_name", "")

    # Fallback: split full name
    if not given_name and full_name and " " in full_name:
        parts = full_name.split(" ", 1)
        given_name = parts[0]
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
    from flask import request

    if session.get("user"):
        return redirect(url_for("main.dashboard"))

    if request.method == "GET":
        return render_template("register.html", error=None, success=False)

    first_name = request.form.get("first_name", "").strip()
    last_name  = request.form.get("last_name",  "").strip()
    email      = request.form.get("email",      "").strip()

    if not all([first_name, last_name, email]):
        return render_template(
            "register.html",
            error="Please fill in all required fields.",
            success=False,
        )

    api_token   = current_app.config["OKTA_API_TOKEN"]
    okta_domain = current_app.config["OKTA_DOMAIN"]

    if not api_token:
        return render_template(
            "register.html",
            error="Registration is currently unavailable. Please contact the administrator.",
            success=False,
        )

    profile = {
        "firstName": first_name,
        "lastName":  last_name,
        "email":     email,
        "login":     email,
    }

    headers = {
        "Authorization": f"SSWS {api_token}",
        "Content-Type":  "application/json",
        "Accept":        "application/json",
    }

    try:
        # Step 1 — create user in STAGED state
        create_resp = http_requests.post(
            f"https://{okta_domain}/api/v1/users?activate=false",
            headers=headers,
            json={"profile": profile},
            timeout=15,
        )
        if create_resp.status_code not in (200, 201):
            return render_template(
                "register.html",
                error=_okta_error(create_resp),
                success=False,
            )

        user_id = create_resp.json().get("id")

        # Step 2 — send activation email
        act_resp = http_requests.post(
            f"https://{okta_domain}/api/v1/users/{user_id}/lifecycle/activate?sendEmail=true",
            headers=headers,
            timeout=15,
        )
        if act_resp.status_code not in (200, 201):
            logger.warning("Okta activate failed: %s", act_resp.text)

        return render_template(
            "register.html",
            error=None,
            success=True,
            first_name=first_name,
            email=email,
        )

    except Exception as exc:
        logger.error("Okta registration error: %s", exc)
        return render_template(
            "register.html",
            error="Could not reach authentication server. Please try again.",
            success=False,
        )


# ── Helpers ────────────────────────────────────────────────────────────────

def _okta_error(resp) -> str:
    try:
        data = resp.json()
        causes = data.get("errorCauses", [])
        cause_msg = causes[0].get("errorSummary", "") if causes else ""
        return cause_msg or data.get("errorSummary") or f"Okta error {resp.status_code}"
    except Exception:
        return f"Okta error {resp.status_code}"
