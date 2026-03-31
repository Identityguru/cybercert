"""
Quiz blueprint: quiz selection, question delivery, scoring, results.
"""
import json
import logging

from flask import abort, jsonify, render_template, request, session

from . import quiz_bp
from ..auth.decorators import login_required
from ..database import service as db_svc
from ..content.topics_registry import TOPICS_LIST
from ..content.okta_professional import TOPICS

logger = logging.getLogger(__name__)


@quiz_bp.route("/")
@login_required
def index():
    user = session["user"]
    db_user = db_svc.get_user_by_sub(user["sub"])
    best_scores = db_svc.get_best_scores(db_user.id)

    topics_with_scores = []
    for topic in TOPICS_LIST:
        slug = topic["slug"]
        content = TOPICS.get(slug, {})
        topics_with_scores.append({
            **topic,
            "question_count": len(content.get("quiz_questions", [])),
            "best_score": best_scores.get(slug),
        })

    return render_template("quiz/index.html", topics=topics_with_scores)


@quiz_bp.route("/<topic_slug>")
@login_required
def take(topic_slug: str):
    if topic_slug not in TOPICS:
        abort(404)

    content = TOPICS[topic_slug]
    questions = content.get("quiz_questions", [])

    # Strip correct answers before sending to template
    safe_questions = [
        {"q": q["q"], "options": q["options"]}
        for q in questions
    ]

    return render_template(
        "quiz/question.html",
        topic=content,
        topic_slug=topic_slug,
        questions=safe_questions,
        questions_json=json.dumps(safe_questions),
    )


@quiz_bp.route("/<topic_slug>/submit", methods=["POST"])
@login_required
def submit(topic_slug: str):
    if topic_slug not in TOPICS:
        abort(404)

    data = request.get_json(silent=True) or {}
    submitted_answers = data.get("answers", {})  # {str(q_index): int(chosen_option)}

    questions = TOPICS[topic_slug].get("quiz_questions", [])
    total = len(questions)
    correct = 0
    results = []

    for i, q in enumerate(questions):
        chosen = submitted_answers.get(str(i))
        is_correct = chosen == q["answer"]
        if is_correct:
            correct += 1
        results.append({
            "q": q["q"],
            "options": q["options"],
            "chosen": chosen,
            "answer": q["answer"],
            "correct": is_correct,
            "explanation": q.get("explanation", ""),
        })

    score_pct = int((correct / total) * 100) if total else 0

    user = session["user"]
    db_user = db_svc.get_user_by_sub(user["sub"])
    attempt = db_svc.save_quiz_attempt(
        user_id=db_user.id,
        topic_slug=topic_slug,
        score_pct=score_pct,
        correct_count=correct,
        total_questions=total,
        answers=submitted_answers,
    )

    return jsonify({
        "attempt_id": attempt.id,
        "score_pct": score_pct,
        "correct": correct,
        "total": total,
        "results": results,
    })


@quiz_bp.route("/results/<attempt_id>")
@login_required
def results(attempt_id: str):
    user = session["user"]
    db_user = db_svc.get_user_by_sub(user["sub"])

    attempt = db_svc.get_quiz_attempt(attempt_id)
    if not attempt or attempt.user_id != db_user.id:
        abort(404)

    answers = json.loads(attempt.answers_json)
    questions = TOPICS[attempt.topic_slug].get("quiz_questions", [])
    topic = TOPICS[attempt.topic_slug]

    detailed = []
    for i, q in enumerate(questions):
        chosen = answers.get(str(i))
        detailed.append({
            "q": q["q"],
            "options": q["options"],
            "chosen": chosen,
            "answer": q["answer"],
            "correct": chosen == q["answer"],
            "explanation": q.get("explanation", ""),
        })

    return render_template(
        "quiz/results.html",
        attempt=attempt,
        topic=topic,
        topic_slug=attempt.topic_slug,
        detailed=detailed,
    )
