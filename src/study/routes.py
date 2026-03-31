"""
Study blueprint: topic list and individual topic pages.
"""
from flask import abort, render_template, session

from . import study_bp
from ..auth.decorators import login_required
from ..database import service as db_svc
from ..content.topics_registry import TOPICS_LIST
from ..content.okta_professional import TOPICS


@study_bp.route("/")
@login_required
def index():
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
            "best_score": best_scores.get(slug),
        })

    return render_template("study/index.html", topics=topics_with_status)


@study_bp.route("/<topic_slug>")
@login_required
def topic(topic_slug: str):
    if topic_slug not in TOPICS:
        abort(404)

    user = session["user"]
    db_user = db_svc.get_user_by_sub(user["sub"])
    db_svc.mark_topic_viewed(db_user.id, topic_slug)

    content = TOPICS[topic_slug]
    best_scores = db_svc.get_best_scores(db_user.id)

    # Previous / next navigation
    slugs = [t["slug"] for t in TOPICS_LIST]
    idx = slugs.index(topic_slug)
    prev_slug = slugs[idx - 1] if idx > 0 else None
    next_slug = slugs[idx + 1] if idx < len(slugs) - 1 else None

    return render_template(
        "study/topic.html",
        topic=content,
        topic_slug=topic_slug,
        best_score=best_scores.get(topic_slug),
        prev_slug=prev_slug,
        next_slug=next_slug,
    )
