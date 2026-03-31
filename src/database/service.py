"""
Database service layer.

All database operations go through this module — routes never call
db.session directly.
"""
from __future__ import annotations

import json
import logging
from datetime import datetime, timezone
from typing import Optional

from . import db
from .models import QuizAttempt, TopicProgress, User

logger = logging.getLogger(__name__)


# ── User ───────────────────────────────────────────────────────────────────

def get_or_create_user(okta_sub: str, email: str, given_name: str, family_name: str) -> User:
    """Fetch user by Okta sub, creating if they don't exist. Called on every OIDC callback."""
    user = User.query.filter_by(okta_sub=okta_sub).first()
    if user is None:
        user = User(
            okta_sub=okta_sub,
            email=email,
            given_name=given_name,
            family_name=family_name,
        )
        db.session.add(user)
        db.session.commit()
        logger.info("Created new user: %s", email)
    return user


def get_user_by_sub(okta_sub: str) -> Optional[User]:
    return User.query.filter_by(okta_sub=okta_sub).first()


# ── Topic Progress ─────────────────────────────────────────────────────────

def mark_topic_viewed(user_id: str, topic_slug: str) -> TopicProgress:
    """Upsert a topic view — increments view_count if already viewed."""
    progress = TopicProgress.query.filter_by(
        user_id=user_id, topic_slug=topic_slug
    ).first()

    if progress is None:
        progress = TopicProgress(user_id=user_id, topic_slug=topic_slug)
        db.session.add(progress)
    else:
        progress.view_count += 1
        progress.last_viewed_at = datetime.now(timezone.utc)

    db.session.commit()
    return progress


def get_user_progress(user_id: str) -> dict[str, TopicProgress]:
    """Return a dict mapping topic_slug → TopicProgress for the user."""
    rows = TopicProgress.query.filter_by(user_id=user_id).all()
    return {r.topic_slug: r for r in rows}


# ── Quiz Attempts ──────────────────────────────────────────────────────────

def save_quiz_attempt(
    user_id: str,
    topic_slug: str,
    score_pct: int,
    correct_count: int,
    total_questions: int,
    answers: dict,
) -> QuizAttempt:
    attempt = QuizAttempt(
        user_id=user_id,
        topic_slug=topic_slug,
        score_pct=score_pct,
        correct_count=correct_count,
        total_questions=total_questions,
        answers_json=json.dumps(answers),
    )
    db.session.add(attempt)
    db.session.commit()
    return attempt


def get_quiz_attempt(attempt_id: str) -> Optional[QuizAttempt]:
    return QuizAttempt.query.get(attempt_id)


def get_best_scores(user_id: str) -> dict[str, int]:
    """Return a dict mapping topic_slug → best score_pct for the user."""
    attempts = QuizAttempt.query.filter_by(user_id=user_id).all()
    best: dict[str, int] = {}
    for a in attempts:
        if a.topic_slug not in best or a.score_pct > best[a.topic_slug]:
            best[a.topic_slug] = a.score_pct
    return best


def get_quiz_history(user_id: str, topic_slug: str | None = None) -> list[QuizAttempt]:
    q = QuizAttempt.query.filter_by(user_id=user_id)
    if topic_slug:
        q = q.filter_by(topic_slug=topic_slug)
    return q.order_by(QuizAttempt.completed_at.desc()).all()
