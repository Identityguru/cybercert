"""
Database models for CyberCert.

Schema:
    User          — one row per authenticated person (keyed by Okta sub)
    TopicProgress — tracks which study topics a user has viewed
    QuizAttempt   — one row per quiz submission
"""
from __future__ import annotations

import uuid
from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import db


# ── Helpers ────────────────────────────────────────────────────────────────

def _uuid() -> str:
    return str(uuid.uuid4())


def _now() -> datetime:
    return datetime.now(timezone.utc)


# ── User ───────────────────────────────────────────────────────────────────

class User(db.Model):
    """
    One row per person. Created / updated on first login via Okta callback.
    okta_sub is the immutable Okta subject ID.
    """
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    okta_sub: Mapped[str] = mapped_column(String(128), unique=True, nullable=False, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    given_name: Mapped[str] = mapped_column(String(100), nullable=False, default="")
    family_name: Mapped[str] = mapped_column(String(100), nullable=False, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now, onupdate=_now)

    # Relationships
    topic_progress: Mapped[list["TopicProgress"]] = relationship(
        "TopicProgress", back_populates="user", cascade="all, delete-orphan"
    )
    quiz_attempts: Mapped[list["QuizAttempt"]] = relationship(
        "QuizAttempt", back_populates="user", cascade="all, delete-orphan",
        order_by="QuizAttempt.completed_at.desc()"
    )

    def __repr__(self) -> str:
        return f"<User {self.email}>"

    @property
    def full_name(self) -> str:
        return f"{self.given_name} {self.family_name}".strip()

    def to_session_dict(self) -> dict:
        return {
            "name":        self.full_name,
            "given_name":  self.given_name,
            "family_name": self.family_name,
            "email":       self.email,
            "sub":         self.okta_sub,
        }


# ── TopicProgress ──────────────────────────────────────────────────────────

class TopicProgress(db.Model):
    """Tracks which study topics a user has read and how many times."""
    __tablename__ = "topic_progress"
    __table_args__ = (UniqueConstraint("user_id", "topic_slug"),)

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    topic_slug: Mapped[str] = mapped_column(String(100), nullable=False)
    first_viewed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)
    last_viewed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)
    view_count: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    user: Mapped["User"] = relationship("User", back_populates="topic_progress")

    def __repr__(self) -> str:
        return f"<TopicProgress {self.topic_slug} user={self.user_id}>"


# ── QuizAttempt ────────────────────────────────────────────────────────────

class QuizAttempt(db.Model):
    """One row per quiz submission."""
    __tablename__ = "quiz_attempts"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    topic_slug: Mapped[str] = mapped_column(String(100), nullable=False)
    score_pct: Mapped[int] = mapped_column(Integer, nullable=False)       # 0–100
    correct_count: Mapped[int] = mapped_column(Integer, nullable=False)
    total_questions: Mapped[int] = mapped_column(Integer, nullable=False)
    answers_json: Mapped[str] = mapped_column(Text, nullable=False)        # JSON: {q_index: chosen_option}
    completed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)

    user: Mapped["User"] = relationship("User", back_populates="quiz_attempts")

    def __repr__(self) -> str:
        return f"<QuizAttempt {self.topic_slug} {self.score_pct}%>"
