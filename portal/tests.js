// Practice tests, level exams and the Master Exam (UI). The server (tests_api.py) samples, grades and explains;
// this file only renders. Globals used from index.html: lang, LEVELS, escapeHtml, clickLesson, currentView, renderSidebar.
const TestsUI = (() => {
  const STR = {
    en: {
      chapterTitle: 'Chapter Test', levelTitle: 'Level Exam', masterTitle: 'Master Exam', drillTitle: 'Topic Practice',
      chapterDesc: (n, k, q) => `${q} questions, mixed fresh every time from a pool of ${n} questions, balanced across the ${k} topics of this chapter. Every example is from the Qur'an.`,
      levelDesc: (c, q) => `${q} questions from the ${c} chapters of this level, balanced across chapters and topics.`,
      masterDesc: (q) => `The capstone: ${q} questions from all three levels together, balanced across levels, chapters and topics. Take it whenever you like.`,
      start: 'Start', startNew: 'New test', best: 'Best', attempts: 'attempts', learnNote: 'This is for learning, not for grading you: every answer comes with an explanation, and a hint costs only a little.',
      question: 'Question', of: 'of', points: 'points', pts: 'pts',
      hint: '💡 Hint (costs 25% of this question)', hintTitle: 'Rule from the lesson', endTest: 'End test',
      endConfirm: 'End the test now? Unanswered questions will score 0.',
      next: 'Next question', finish: 'See my results', tryAgain: 'Try again',
      correct: (p) => `✅ Correct! +${p} points`, notThis: (p) => `❌ Not this one. Read why below, then try again (worth ${p} now).`,
      outOfTries: 'The correct answer is marked in green. Read every explanation: they are the lesson.',
      wasRight: 'Right', wasWrong: 'Not this one', correctMark: 'Correct answer', yourPick: 'Your choice',
      report: 'Report a problem with this question', reportPrompt: 'What is wrong with this question? (answer, explanation, Arabic, translation...)', reportThanks: 'Thank you, we will check it.',
      surah: "Qur'an",
      results: 'Your results', score: 'Score', mastery: 'Knew it first time', masteryNote: 'Right on the first try without a hint. This is the number that shows what you really know.',
      hintsUsed: 'Hints used', retries: 'Retries', weak: 'Topics to strengthen', strong: 'Your strongest topics', noWeak: 'No weak topics this time. Excellent! Take another test to keep them sharp.',
      study: 'Study this topic', drill: 'Practice this topic', byLevel: 'By level', allTopics: 'All topics in this test', history: 'Your earlier scores on this test',
      tryNewTest: 'Take a new test', back: 'Back', week: 'Week', level: 'Level', firstTry: 'first try', lifetime: 'overall', loading: 'Loading…',
      locked: 'This chapter is not unlocked yet.', unavailable: 'Questions for this test are not available yet.', error: 'Something went wrong. Please try again.',
    },
    tr: {
      chapterTitle: 'Bölüm Testi', levelTitle: 'Seviye Sınavı', masterTitle: 'Ana Sınav', drillTitle: 'Konu Alıştırması',
      chapterDesc: (n, k, q) => `${q} soru; her seferinde ${n} soruluk havuzdan yeniden karıştırılır ve bölümün ${k} konusuna dengeli dağıtılır. Tüm örnekler Kur'an'dandır.`,
      levelDesc: (c, q) => `Bu seviyenin ${c} bölümünden, bölümlere ve konulara dengeli dağıtılmış ${q} soru.`,
      masterDesc: (q) => `Büyük final: üç seviyeden birlikte ${q} soru; seviyelere, bölümlere ve konulara dengeli dağıtılır. İstediğiniz zaman çözebilirsiniz.`,
      start: 'Başla', startNew: 'Yeni test', best: 'En iyi', attempts: 'deneme', learnNote: 'Amaç sizi notlamak değil öğretmektir: her cevabın açıklaması vardır, ipucunun bedeli de küçüktür.',
      question: 'Soru', of: '/', points: 'puan', pts: 'p',
      hint: '💡 İpucu (bu sorunun %25\'ine mal olur)', hintTitle: 'Dersten kural', endTest: 'Testi bitir',
      endConfirm: 'Test şimdi bitirilsin mi? Cevaplanmayan sorular 0 puan alır.',
      next: 'Sonraki soru', finish: 'Sonuçlarımı gör', tryAgain: 'Tekrar dene',
      correct: (p) => `✅ Doğru! +${p} puan`, notThis: (p) => `❌ Bu değil. Aşağıdaki açıklamayı okuyun, sonra tekrar deneyin (şimdi ${p} puan).`,
      outOfTries: 'Doğru cevap yeşil ile gösterildi. Bütün açıklamaları okuyun: ders onlardır.',
      wasRight: 'Doğru', wasWrong: 'Bu değil', correctMark: 'Doğru cevap', yourPick: 'Seçiminiz',
      report: 'Bu soruyla ilgili sorun bildir', reportPrompt: 'Bu soruda ne yanlış? (cevap, açıklama, Arapça, çeviri...)', reportThanks: 'Teşekkürler, kontrol edeceğiz.',
      surah: "Kur'an",
      results: 'Sonuçlarınız', score: 'Puan', mastery: 'İlk seferde bildiniz', masteryNote: 'İpucu almadan ilk denemede doğru. Gerçekte neyi bildiğinizi gösteren sayı budur.',
      hintsUsed: 'Kullanılan ipucu', retries: 'Tekrar deneme', weak: 'Güçlendirilecek konular', strong: 'En güçlü konularınız', noWeak: 'Bu sefer zayıf konu yok. Harika! Taze kalmaları için yeni bir test çözün.',
      study: 'Bu konuyu çalış', drill: 'Bu konuyu alıştır', byLevel: 'Seviyeye göre', allTopics: 'Bu testteki tüm konular', history: 'Bu testteki önceki puanlarınız',
      tryNewTest: 'Yeni test çöz', back: 'Geri', week: 'Hafta', level: 'Seviye', firstTry: 'ilk deneme', lifetime: 'genel', loading: 'Yükleniyor…',
      locked: 'Bu bölümün kilidi henüz açılmadı.', unavailable: 'Bu test için sorular henüz hazır değil.', error: 'Bir şeyler ters gitti. Lütfen tekrar deneyin.',
    },
  };
  const L = () => (lang === 'tr' ? 'tr' : 'en');          // question content exists in en + tr; Arabic UI shows English
  const tx = k => STR[L()][k] ?? STR.en[k];
  const pick = o => (o ? (o[L()] || o.en || '') : '');
  const esc = s => escapeHtml(String(s ?? ''));
  const fmt = n => (Math.round(n * 100) / 100).toString();
  const LETTERS = ['A', 'B', 'C', 'D'];

  let catalog = null;
  let S = null;                                           // running test

  async function api(path, body) {
    try {
      const res = await fetch('/api/tests/' + path, {
        method: body === undefined ? 'GET' : 'POST', credentials: 'same-origin',
        headers: body === undefined ? {} : { 'Content-Type': 'application/json' },
        body: body === undefined ? undefined : JSON.stringify(body),
      });
      return { ok: res.ok, status: res.status, data: await res.json().catch(() => ({})) };
    } catch { return { ok: false, status: 0, data: {} }; }
  }

  async function loadCatalog(force) {
    if (catalog && !force) return catalog;
    const r = await api('catalog');
    catalog = r.ok ? r.data : { chapters: {}, chaptersPerLevel: {}, master: { pool: 0 }, lengths: {}, best: {} };
    return catalog;
  }

  // ─── Entry cards ────────────────────────────────────────────────────────────
  function bestHtml(key) {
    const b = catalog.best[key];
    return b ? `<div class="tq-best">${tx('best')}: <strong>${b.best}%</strong> · ${b.attempts} ${tx('attempts')}</div>` : '';
  }

  function card(title, desc, key, spec, extra = '') {
    return `<div class="tq-entry"><h3>${esc(title)}</h3><p>${esc(desc)}</p><p class="tq-note">${esc(tx('learnNote'))}</p>
      ${bestHtml(key)}${extra}
      <button class="btn-primary" onclick='TestsUI.start(${JSON.stringify(spec)})'>${tx('start')}</button></div>`;
  }

  async function mountChapter(levelNum, week) {
    const slot = document.getElementById('lesson-tests-section');
    if (!slot) return;
    await loadCatalog();
    const id = `L${levelNum}W${week}`;
    const ch = catalog.chapters[id];
    if (!ch || !ch.open) { slot.remove(); return; }
    slot.innerHTML = `<div class="section-title">${tx('chapterTitle')}</div>` +
      card(tx('chapterTitle'), tx('chapterDesc')(ch.pool, ch.topics.length, catalog.lengths.chapter), `chapter:${id}`, { kind: 'chapter', chapter: id });
  }

  async function mountLevel(levelNum) {
    const slot = document.getElementById('level-exam-slot');
    if (!slot) return;
    await loadCatalog();
    const n = catalog.chaptersPerLevel[String(levelNum)] || 0;
    if (n < 14) { slot.remove(); return; }       // a level exam needs all 14 chapters of the level
    slot.innerHTML = `<div class="section-title">${tx('levelTitle')}</div>` +
      card(tx('levelTitle'), tx('levelDesc')(n, catalog.lengths.level), `level:L${levelNum}`, { kind: 'level', level: levelNum });
  }

  async function renderMaster(ref) {
    const main = document.getElementById('main');
    main.innerHTML = `<div class="topic-header"><h2>${esc(ref.title[lang] || ref.title.en)}</h2></div><div class="section" id="master-slot">${tx('loading')}</div>`;
    await loadCatalog(true);
    const slot = document.getElementById('master-slot');
    if (!catalog.master.pool) { slot.innerHTML = `<div class="tq-entry"><p>${tx('unavailable')}</p></div>`; return; }
    slot.innerHTML = card(tx('masterTitle'), tx('masterDesc')(catalog.lengths.master), 'master:ALL', { kind: 'master' });
  }

  // ─── Running a test ─────────────────────────────────────────────────────────
  async function start(spec) {
    const main = document.getElementById('main');
    main.innerHTML = `<div class="section">${tx('loading')}</div>`;
    const r = await api('start', spec);
    if (!r.ok) {
      main.innerHTML = `<div class="section"><div class="tq-entry"><p>${esc(r.status === 403 ? tx('locked') : r.status === 404 ? tx('unavailable') : tx('error'))}</p></div></div>`;
      return;
    }
    S = { spec, ...r.data, idx: 0, st: r.data.items.map(() => ({ tries: [], why: {}, done: false, hint: null, points: 0 })) };
    renderQuestion();
  }

  function nextPoints(st) {
    const base = S.tryPoints[Math.min(st.tries.length, S.tryPoints.length - 1)];
    return fmt(base * (st.hint ? S.hintFactor : 1));
  }

  function runningPoints() { return S.st.reduce((a, s) => a + s.points, 0); }

  function titleOf(spec) {
    return spec.kind === 'chapter' ? tx('chapterTitle') : spec.kind === 'level' ? tx('levelTitle') : spec.kind === 'master' ? tx('masterTitle') : tx('drillTitle');
  }

  function optionHtml(o) {
    return o.ar ? `<span class="tq-ar">${esc(o.ar)}</span>` : esc(pick(o.text));
  }

  function renderQuestion() {
    const it = S.items[S.idx], st = S.st[S.idx], total = S.total;
    const topic = S.topics[`${it.chapter}:${it.topic}`];
    const optionsHtml = it.options.map((o, i) => {
      const tried = st.tries.includes(i);
      let cls = 'tq-opt', why = '';
      if (st.done) {
        const rv = st.reveal[i];
        cls += rv.correct ? ' correct' : (tried ? ' wrong' : ' neutral');
        why = `<div class="tq-why ${rv.correct ? 'ok' : 'no'}"><strong>${rv.correct ? tx('correctMark') : (tried ? tx('yourPick') + ' · ' + tx('wasWrong') : tx('wasWrong'))}.</strong> ${esc(pick(rv.why))}</div>`;
      } else if (tried) {
        cls += ' wrong';
        why = `<div class="tq-why no"><strong>${tx('wasWrong')}.</strong> ${esc(pick(st.why[i]))}</div>`;
      }
      const disabled = st.done || tried ? 'disabled' : '';
      return `<div class="tq-opt-wrap"><button class="${cls}" ${disabled} onclick="TestsUI.answer(${i})"><span class="tq-letter">${LETTERS[i]}</span><span class="tq-opt-text">${optionHtml(o)}</span></button>${why}</div>`;
    }).join('');

    let banner = '';
    if (st.done) banner = st.points > 0 ? `<div class="tq-banner ok">${tx('correct')(fmt(st.points))}</div>` : `<div class="tq-banner no">${tx('outOfTries')}</div>`;
    else if (st.tries.length) banner = `<div class="tq-banner no">${tx('notThis')(nextPoints(st))}</div>`;

    const hintBox = st.hint ? `<div class="tq-hint"><strong>${tx('hintTitle')} · ${esc(pick(st.hint.title))}</strong><br>${esc(pick(st.hint.rule))}</div>` : '';
    const hintBtn = (!st.done && !st.hint) ? `<button class="btn-secondary" onclick="TestsUI.hint()">${tx('hint')}</button>` : '';
    const last = S.idx === total - 1;
    const nextBtn = st.done ? `<button class="btn-primary" onclick="TestsUI.next()">${last ? tx('finish') : tx('next')}</button>` : '';

    document.getElementById('main').innerHTML = `
      <div class="topic-header"><h2>${esc(titleOf(S.spec))}</h2>
        <p>${tx('question')} ${S.idx + 1} ${tx('of')} ${total} · ${fmt(runningPoints())} ${tx('points')}</p></div>
      <div class="section"><div class="quiz-card tq-card">
        <div class="q-progress-bar"><div class="q-progress-fill" style="width:${Math.round(S.idx / total * 100)}%"></div></div>
        <div class="tq-chip">${esc(pick(topic.title))}</div>
        <div class="quiz-arabic tq-quote">${esc(it.quote)}</div>
        <div class="tq-ref">${tx('surah')} ${esc(it.ref)}</div>
        <div class="tq-stem">${esc(pick(it.stem))}</div>
        <div class="tq-options">${optionsHtml}</div>
        ${banner}${hintBox}
        <div class="q-actions tq-actions">${hintBtn}<span class="spacer"></span>${nextBtn}</div>
        <div class="tq-foot"><a href="#" onclick="TestsUI.reportQuestion();return false">${tx('report')}</a> · <a href="#" onclick="TestsUI.end();return false">${tx('endTest')}</a></div>
      </div></div>`;
    document.getElementById('main').scrollTop = 0;
  }

  async function answer(i) {
    const it = S.items[S.idx], st = S.st[S.idx];
    if (st.done || st.tries.includes(i)) return;
    const r = await api('answer', { attemptId: S.attemptId, pos: it.pos, choice: i });
    if (!r.ok) { alert(tx('error')); return; }
    const d = r.data;
    st.tries.push(i);
    st.why[i] = d.chosen.why;
    if (d.done) { st.done = true; st.points = d.points; st.reveal = d.options; }
    renderQuestion();
  }

  async function hint() {
    const it = S.items[S.idx], st = S.st[S.idx];
    const r = await api('hint', { attemptId: S.attemptId, pos: it.pos });
    if (!r.ok) return;
    st.hint = r.data;
    renderQuestion();
  }

  function next() {
    if (S.idx < S.total - 1) { S.idx++; renderQuestion(); } else finish();
  }

  function end() {
    if (confirm(tx('endConfirm'))) finish();
  }

  async function reportQuestion() {
    const note = prompt(tx('reportPrompt'));
    if (!note || !note.trim()) return;
    const r = await api('report-question', { qid: S.items[S.idx].id, note });
    alert(r.ok ? tx('reportThanks') : tx('error'));
  }

  // ─── Results ────────────────────────────────────────────────────────────────
  const bar = pct => `<div class="tq-bar"><div class="tq-bar-fill ${pct >= 75 ? 'hi' : pct >= 50 ? 'mid' : 'lo'}" style="width:${pct}%"></div></div>`;

  function topicRow(t, withActions) {
    const where = `${tx('level')} ${t.level} · ${tx('week')} ${t.week}`;
    const life = t.lifetime ? ` · ${tx('lifetime')} ${t.lifetime.mastery}% (${t.lifetime.n})` : '';
    const actions = withActions ? `<div class="tq-row-actions">
        <button class="btn-secondary" onclick="TestsUI.study(${t.level},${t.week},${t.section ?? 0})">📖 ${tx('study')}</button>
        <button class="btn-primary" onclick='TestsUI.start(${JSON.stringify({ kind: 'drill', chapter: t.chapter, topic: t.topic })})'>${tx('drill')}</button></div>` : '';
    return `<div class="tq-topic"><div class="tq-topic-head"><strong>${esc(pick(t.title))}</strong><span class="tq-where">${where}</span></div>
      ${bar(t.mastery)}<div class="tq-topic-sub">${t.mastered}/${t.n} ${tx('firstTry')} (${t.mastery}%)${life}</div>${actions}</div>`;
  }

  async function finish() {
    const r = await api('finish', { attemptId: S.attemptId });
    const main = document.getElementById('main');
    if (!r.ok) { main.innerHTML = `<div class="section"><div class="tq-entry"><p>${tx('error')}</p></div></div>`; return; }
    const d = r.data;
    catalog = null;                                        // refresh best scores next time
    const levelsHtml = (S.spec.kind === 'level' || S.spec.kind === 'master') && Object.keys(d.levels).length > 1
      ? `<div class="section"><div class="section-title">${tx('byLevel')}</div>${Object.keys(d.levels).sort().map(k =>
        `<div class="tq-topic"><div class="tq-topic-head"><strong>${tx('level')} ${k}</strong></div>${bar(d.levels[k].mastery)}<div class="tq-topic-sub">${d.levels[k].mastered}/${d.levels[k].n} ${tx('firstTry')} (${d.levels[k].mastery}%)</div></div>`).join('')}</div>` : '';
    const hist = d.history.length ? `<div class="tq-hist">${tx('history')}: ${d.history.map(h => Math.round(100 * h.points / h.max) + '%').join(' · ')}</div>` : '';
    main.innerHTML = `
      <div class="topic-header"><h2>${tx('results')} · ${esc(titleOf(S.spec))}</h2></div>
      <div class="section"><div class="score-card">
        <div class="score-num">${fmt(d.points)} / ${d.max}</div>
        <div class="score-label">${d.percent}% · ${tx('score')}</div>
        <div class="tq-stats">
          <div><strong>${d.masteredCount}/${d.questions}</strong><br>${tx('mastery')}</div>
          <div><strong>${d.hintsUsed}</strong><br>${tx('hintsUsed')}</div>
          <div><strong>${d.retries}</strong><br>${tx('retries')}</div></div>
        <p class="tq-note">${tx('masteryNote')}</p>${hist}
        <div class="score-actions"><button class="btn-primary" onclick='TestsUI.start(${JSON.stringify(S.spec)})'>${tx('tryNewTest')}</button>
          <button class="btn-secondary" onclick="TestsUI.leave()">${tx('back')}</button></div>
      </div></div>
      <div class="section"><div class="section-title">${tx('weak')}</div>
        ${d.weak.length ? d.weak.map(t => topicRow(t, true)).join('') : `<div class="tq-entry"><p>${tx('noWeak')}</p></div>`}</div>
      ${d.strong.length ? `<div class="section"><div class="section-title">${tx('strong')}</div>${d.strong.map(t => topicRow(t, false)).join('')}</div>` : ''}
      ${levelsHtml}
      <div class="section"><details class="tq-all"><summary>${tx('allTopics')}</summary>${d.topics.map(t => topicRow(t, true)).join('')}</details></div>`;
    document.getElementById('main').scrollTop = 0;
  }

  // Open the lesson and scroll to the lecture section a weak topic belongs to.
  function study(level, week, section) {
    const lv = LEVELS[level - 1];
    const idx = lv ? lv.lessons.findIndex(l => l.week === week) : -1;
    if (idx < 0) return;
    clickLesson(lv.id, idx);
    let tries = 0;
    const timer = setInterval(() => {
      const el = document.getElementById('lec-sec-' + section);
      if (el) {
        clearInterval(timer);
        el.scrollIntoView({ behavior: 'smooth', block: 'start' });
        el.classList.add('tq-flash');
        setTimeout(() => el.classList.remove('tq-flash'), 2500);
      } else if (++tries > 30) clearInterval(timer);
    }, 100);
  }

  function leave() {
    S = null;
    if (typeof showWelcome === 'function') {
      if (currentView && currentView.type === 'lesson') clickLesson(currentView.level.id, currentView.level.lessons.indexOf(currentView.lesson));
      else if (currentView && currentView.type === 'level') renderLevelOverview(currentView.level);
      else if (currentView && currentView.type === 'reference') renderMaster(currentView.ref);
      else showWelcome();
    }
  }

  const css = `
    .tq-entry{background:var(--card);border:1px solid var(--border);border-radius:var(--radius);padding:24px;box-shadow:var(--shadow)}
    .tq-entry h3{color:var(--green);margin-bottom:6px;font-size:1.1rem}.tq-entry p{color:var(--mid);font-size:.9rem;line-height:1.6;margin-bottom:10px}
    .tq-note{color:var(--muted)!important;font-size:.82rem!important}.tq-best{font-size:.85rem;color:var(--green);margin-bottom:12px}
    .tq-chip{display:inline-block;background:var(--green-pale);color:var(--green);border-radius:12px;padding:3px 12px;font-size:.78rem;font-weight:600;margin-bottom:8px}
    .tq-quote{font-size:2rem!important;margin:8px 0 6px!important;padding:20px 14px!important}.tq-ref{text-align:center;color:var(--muted);font-size:.78rem;margin-bottom:16px}
    .tq-stem{font-size:1.05rem;font-weight:600;color:var(--dark);margin:6px 0 16px;line-height:1.5}
    .tq-options{display:flex;flex-direction:column;gap:10px}.tq-opt-wrap{display:flex;flex-direction:column;gap:6px}
    .tq-opt{display:flex;align-items:center;gap:12px;width:100%;text-align:left;padding:12px 14px;background:var(--card);border:1.5px solid var(--border);border-radius:8px;cursor:pointer;font-size:.95rem;line-height:1.4;transition:all .15s}
    .tq-opt:hover:not(:disabled){border-color:var(--green);background:var(--green-pale)}.tq-opt:disabled{cursor:default}
    .tq-opt.correct{border-color:var(--green);background:#d4f1de;color:#0e4f29}.tq-opt.wrong{border-color:#dc2626;background:#fef2f2;color:#991b1b}.tq-opt.neutral{opacity:.8}
    .tq-letter{flex:none;width:26px;height:26px;border-radius:50%;background:var(--bg);display:flex;align-items:center;justify-content:center;font-size:.78rem;font-weight:700;color:var(--mid)}
    .tq-ar{font-family:'Amiri Quran','Amiri','Scheherazade New',serif;font-size:1.7rem;direction:rtl;line-height:1.5}
    .tq-why{font-size:.86rem;line-height:1.55;padding:8px 12px;border-radius:6px;margin:0 4px}.tq-why.ok{background:#eaf7ef;color:#14532d}.tq-why.no{background:#fdf2f2;color:#7f1d1d}
    .tq-banner{margin-top:16px;padding:10px 14px;border-radius:8px;font-weight:600;font-size:.92rem}.tq-banner.ok{background:#d4f1de;color:#0e4f29}.tq-banner.no{background:#fff4e5;color:#7a4a00}
    .tq-hint{margin-top:14px;padding:12px 14px;background:#fffbea;border:1px solid var(--gold);border-radius:8px;font-size:.88rem;line-height:1.55}
    .tq-actions{margin-top:18px;display:flex;gap:10px;align-items:center}.tq-foot{margin-top:14px;font-size:.76rem;color:var(--muted);text-align:center}.tq-foot a{color:var(--muted)}
    .tq-stats{display:flex;justify-content:center;gap:34px;margin:6px 0 14px;font-size:.82rem;color:var(--muted)}.tq-stats strong{font-size:1.3rem;color:var(--dark)}
    .tq-topic{background:var(--card);border:1px solid var(--border);border-radius:var(--radius);padding:14px 16px;margin-bottom:10px}
    .tq-topic-head{display:flex;justify-content:space-between;gap:10px;flex-wrap:wrap;margin-bottom:8px}.tq-where{font-size:.78rem;color:var(--muted)}
    .tq-topic-sub{font-size:.8rem;color:var(--muted);margin-top:6px}.tq-row-actions{display:flex;gap:10px;flex-wrap:wrap;margin-top:12px}
    .tq-row-actions .btn-primary,.tq-row-actions .btn-secondary{padding:8px 16px;font-size:.84rem}
    .tq-bar{height:8px;background:var(--border);border-radius:4px;overflow:hidden}.tq-bar-fill{height:100%;border-radius:4px}
    .tq-bar-fill.hi{background:var(--green)}.tq-bar-fill.mid{background:var(--gold)}.tq-bar-fill.lo{background:#dc2626}
    .tq-hist{font-size:.82rem;color:var(--muted);margin-bottom:16px}.tq-all summary{cursor:pointer;color:var(--green);font-weight:600;margin-bottom:12px}
    .tq-flash{animation:tqflash 2.4s ease}@keyframes tqflash{0%,60%{background:#fff4c2}100%{background:transparent}}
    body.rtl .tq-opt{text-align:right}
  `;
  const style = document.createElement('style');
  style.textContent = css;
  document.head.appendChild(style);

  return { mountChapter, mountLevel, renderMaster, start, answer, hint, next, end, reportQuestion, study, leave };
})();
