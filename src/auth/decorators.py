"""
Authentication helpers used across all blueprints.
"""
from functools import wraps

from flask import redirect, session, url_for


def login_required(f):
    """Redirect unauthenticated requests to the login page."""
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get("user"):
            from flask import request
            session["next"] = request.url
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return decorated


def current_user() -> dict | None:
    """Return the current user dict from session, or None."""
    return session.get("user")
