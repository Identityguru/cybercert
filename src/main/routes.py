"""
Main blueprint: landing page, dashboard, profile.
"""
from flask import redirect, render_template, session, url_for

from . import main_bp
from ..auth.decorators import login_required
from ..database import service as db_svc
from ..content.topics_registry import TOPICS_LIST


@main_bp.route("/")
def index():
    if session.get("user"):
        return redirect(url_for("main.dashboard"))
    return render_template("landing.html")


@main_bp.route("/dashboard")
@login_required
def dashboard():
    user = session["user"]
    db_user = db_svc.get_user_by_sub(user["sub"])

    progress = db_svc.get_user_progress(db_user.id)
    best_scores = db_svc.get_best_scores(db_user.id)

    topics_with_status = []
    for topic in TOPICS_LIST:
        slug = topic["slug"]
        topics_with_status.append({
            **topic,
            "viewed": slug in progress,
            "view_count": progress[slug].view_count if slug in progress else 0,
            "best_score": best_scores.get(slug),
        })

    viewed_count = sum(1 for t in topics_with_status if t["viewed"])
    total = len(TOPICS_LIST)

    return render_template(
        "dashboard.html",
        topics=topics_with_status,
        viewed_count=viewed_count,
        total_topics=total,
        progress_pct=int((viewed_count / total) * 100) if total else 0,
    )


@main_bp.route("/profile")
@login_required
def profile():
    return render_template("profile.html")
