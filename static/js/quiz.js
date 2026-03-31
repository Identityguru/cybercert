// CyberCert — quiz.js
// Handles answer selection, progress tracking, submit, and inline results.

(function () {
  const answers = {};        // { qIndex: chosenOption }
  const total = QUESTIONS_DATA.length;

  const submitBtn = document.getElementById('submit-btn');
  const progressEl = document.getElementById('answer-progress');
  const resultsPanel = document.getElementById('results-panel');

  function updateProgress() {
    const answered = Object.keys(answers).length;
    progressEl.textContent = `${answered} / ${total} answered`;
    submitBtn.disabled = answered < total;
  }

  // Option selection
  document.querySelectorAll('.option-label').forEach(label => {
    label.addEventListener('click', () => {
      const radio = label.querySelector('.option-radio');
      const qIndex = parseInt(radio.dataset.q, 10);
      const optIndex = parseInt(radio.dataset.opt, 10);

      // Deselect siblings
      const block = label.closest('.question-block');
      block.querySelectorAll('.option-label').forEach(l => l.classList.remove('selected'));

      label.classList.add('selected');
      radio.checked = true;
      answers[qIndex] = optIndex;
      updateProgress();
    });
  });

  // Submit
  submitBtn.addEventListener('click', async () => {
    submitBtn.disabled = true;
    submitBtn.textContent = 'Submitting…';

    try {
      const resp = await fetch(SUBMIT_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ answers }),
      });

      if (!resp.ok) throw new Error('Server error');

      const data = await resp.json();
      showResults(data);

      // Scroll to results
      setTimeout(() => resultsPanel.scrollIntoView({ behavior: 'smooth' }), 100);

    } catch (err) {
      submitBtn.disabled = false;
      submitBtn.textContent = 'Submit Quiz';
      alert('Failed to submit quiz. Please try again.');
    }
  });

  function showResults(data) {
    // Lock question UI
    document.querySelectorAll('.option-radio').forEach(r => r.disabled = true);
    document.getElementById('quiz-container').style.pointerEvents = 'none';

    // Mark correct/wrong on UI
    data.results.forEach((r, i) => {
      const block = document.querySelector(`.question-block[data-index="${i}"]`);
      if (!block) return;
      block.querySelectorAll('.option-label').forEach((label, optIdx) => {
        if (optIdx === r.answer) label.classList.add('correct');
        if (optIdx === r.chosen && !r.correct) label.classList.add('incorrect');
      });
    });

    // Render results panel
    const pct = data.score_pct;
    const grade = pct >= 80 ? 'score-good' : pct >= 60 ? 'score-ok' : 'score-low';
    const verdict = pct >= 80
      ? 'Excellent! You\'re well-prepared on this topic.'
      : pct >= 60
        ? 'Good effort. Review the explanations below.'
        : 'Keep studying! Focus on the questions you missed.';

    resultsPanel.innerHTML = `
      <div class="score-card score-card--${pct >= 80 ? 'pass' : pct >= 60 ? 'ok' : 'fail'}" style="margin-top:2rem;">
        <div class="score-badge ${grade}">${pct}%</div>
        <div class="score-detail">
          <h2>Your Score</h2>
          <p>${data.correct} / ${data.total} correct</p>
          <p class="score-verdict ${grade}">${verdict}</p>
        </div>
      </div>
      <div style="margin-top:1rem;display:flex;gap:.75rem;flex-wrap:wrap;">
        <a href="${window.location.href}" class="btn btn-primary">Retake Quiz</a>
        <a href="/quiz/results/${data.attempt_id}" class="btn btn-ghost">Full Review</a>
        <a href="/quiz" class="btn btn-ghost">All Quizzes</a>
      </div>
    `;
    resultsPanel.style.display = 'block';
  }

  updateProgress();
})();
