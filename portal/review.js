// Scholar review of the practice-question banks (admin only). Left: Level > Chapter tree with progress counts; right: every
// question of the chosen chapter with the correct answer and all option explanations, an Approve toggle and a comment thread.
// The server (tests_api.py, /api/tests/review/*) stores approvals/comments against the question's content hash.
// Globals used from index.html: lang, LEVELS, escapeHtml, currentView.
const ReviewUI = (() => {
  const STR = {
    en: {
      sub: 'Check each question: the correct answer, every wrong option, and each explanation. Approve it, or leave a comment. Comments are collected so the questions can be corrected; approved questions can later be shown to students as scholar-approved.',
      chapters: 'Chapters', master: 'Master Exam', week: 'Week', all: 'All', todo: 'Not approved', open: 'Open comments', approved: 'Approved',
      exportOpen: 'Export open comments (CSV)', exportAll: 'Export all comments (CSV)', pick: 'Choose a chapter on the left to start.',
      loading: 'Loading…', error: 'Could not load. Are you signed in as an admin?', shown: (n, t) => `${n} of ${t} questions shown`,
      correct: 'Correct answer', quote: "Qur'an", topic: 'Topic', approve: '✓ Approve', unapprove: 'Remove approval',
      approvedBy: (w, d) => `Approved by ${w} · ${d}`, staleApproval: 'An earlier version was approved; this text has changed since, so it needs approving again.',
      comments: 'Comments', none: 'No comments yet.', add: 'Add comment', placeholder: 'Write what should change (answer, wording, explanation, Turkish, ayah…)',
      resolve: 'Mark resolved', reopen: 'Reopen', del: 'Delete', delConfirm: 'Delete this comment?', changedSince: 'question changed since this comment',
      resolved: 'resolved', notReviewed: 'Not reviewed', diff: 'Difficulty', empty: 'No questions match this filter.',
    },
    tr: {
      sub: 'Her soruyu kontrol edin: doğru cevap, her yanlış seçenek ve her açıklama. Onaylayın ya da yorum bırakın. Yorumlar toplanır, sorular buna göre düzeltilir; onaylanan sorular daha sonra öğrencilere "âlim onaylı" olarak gösterilebilir.',
      chapters: 'Bölümler', master: 'Ana Sınav', week: 'Hafta', all: 'Tümü', todo: 'Onaylanmamış', open: 'Açık yorumlar', approved: 'Onaylı',
      exportOpen: 'Açık yorumları indir (CSV)', exportAll: 'Tüm yorumları indir (CSV)', pick: 'Başlamak için soldan bir bölüm seçin.',
      loading: 'Yükleniyor…', error: 'Yüklenemedi. Yönetici olarak giriş yaptınız mı?', shown: (n, t) => `${t} sorudan ${n} tanesi gösteriliyor`,
      correct: 'Doğru cevap', quote: "Kur'an", topic: 'Konu', approve: '✓ Onayla', unapprove: 'Onayı kaldır',
      approvedBy: (w, d) => `${w} onayladı · ${d}`, staleApproval: 'Önceki sürüm onaylanmıştı; metin sonradan değişti, yeniden onaylanmalı.',
      comments: 'Yorumlar', none: 'Henüz yorum yok.', add: 'Yorum ekle', placeholder: 'Neyin değişmesi gerektiğini yazın (cevap, ifade, açıklama, Türkçe, ayet…)',
      resolve: 'Çözüldü say', reopen: 'Yeniden aç', del: 'Sil', delConfirm: 'Bu yorum silinsin mi?', changedSince: 'bu yorumdan sonra soru değişti',
      resolved: 'çözüldü', notReviewed: 'İncelenmedi', diff: 'Zorluk', empty: 'Bu filtreye uyan soru yok.',
    },
  };
  const tx = (k, ...a) => { const v = (STR[lang] || STR.en)[k] ?? STR.en[k]; return typeof v === 'function' ? v(...a) : v; };
  const esc = (s) => escapeHtml(String(s ?? ''));
  const loc = (o) => (o && (o[lang] || o.en)) || '';

  let counts = {};            // chapter id -> {total, approved, open}
  let cur = null;             // chapter id being reviewed
  let questions = [];
  let filter = 'all';
  let openLevels = { 1: true };

  async function api(path, body, method) {
    try {
      const res = await fetch('/api/tests/review/' + path, {
        method: method || (body === undefined ? 'GET' : 'POST'), credentials: 'same-origin',
        headers: body === undefined ? {} : { 'Content-Type': 'application/json' },
        body: body === undefined ? undefined : JSON.stringify(body),
      });
      return { ok: res.ok, data: await res.json().catch(() => ({})) };
    } catch { return { ok: false, data: {} }; }
  }

  // ── tree ──────────────────────────────────────────────────────────────────
  function badge(c) {
    if (!c) return '';
    const done = c.total && c.approved === c.total;
    return `<span class="rv-cnt ${done ? 'done' : ''}">${c.approved}/${c.total}</span>${c.open ? `<span class="rv-open">💬 ${c.open}</span>` : ''}`;
  }
  function treeHtml() {
    let h = `<div class="rv-tree-h">${tx('chapters')}</div>`;
    LEVELS.slice(0, 3).forEach((lv, i) => {
      const L = i + 1;
      const ids = lv.lessons.map(l => `L${L}W${l.week}`);
      const sum = ids.reduce((a, id) => { const c = counts[id]; if (c) { a.total += c.total; a.approved += c.approved; a.open += c.open; } return a; }, { total: 0, approved: 0, open: 0 });
      h += `<div class="rv-level" onclick="ReviewUI.toggleLevel(${L})"><span>${openLevels[L] ? '▾' : '▸'} ${esc(loc(lv.title))}</span><span>${badge(sum)}</span></div>`;
      if (openLevels[L]) {
        h += lv.lessons.map(l => {
          const id = `L${L}W${l.week}`;
          return `<div class="rv-ch ${cur === id ? 'active' : ''}" onclick="ReviewUI.open('${id}')"><span class="rv-chn"><b>${tx('week')} ${l.week}</b> ${esc(loc(l.title))}</span><span>${badge(counts[id])}</span></div>`;
        }).join('');
      }
    });
    h += `<div class="rv-level rv-master ${cur === 'MASTER' ? 'active' : ''}" onclick="ReviewUI.open('MASTER')"><span>🏆 ${tx('master')}</span><span>${badge(counts.MASTER)}</span></div>`;
    return h;
  }
  function paintTree() { const el = document.getElementById('rv-tree'); if (el) el.innerHTML = treeHtml(); }
  async function refreshCounts() {
    const r = await api('tree');
    if (r.ok) { counts = r.data.chapters || {}; paintTree(); }
  }

  // ── question cards ────────────────────────────────────────────────────────
  function fmtDate(iso) { try { return new Date(iso).toLocaleString(lang === 'tr' ? 'tr-TR' : 'en-GB', { dateStyle: 'medium', timeStyle: 'short' }); } catch { return iso; } }

  function optHtml(q, o, i) {
    const right = i === q.correct;
    const txt = o.ar ? `<span class="rv-ar">${esc(o.ar)}</span>` : `${esc(o.text.en)}<div class="rv-tr">${esc(o.text.tr)}</div>`;
    return `<div class="rv-opt ${right ? 'right' : ''}">
      <div class="rv-opt-h"><b>${'ABCD'[i]}</b> ${txt}${right ? `<span class="rv-ok">✔ ${tx('correct')}</span>` : ''}</div>
      <div class="rv-why">${esc(o.why.en)}</div><div class="rv-why rv-tr">${esc(o.why.tr)}</div></div>`;
  }
  function commentHtml(c) {
    return `<div class="rv-cm ${c.resolved ? 'res' : ''}">
      <div class="rv-cm-b">${esc(c.body)}</div>
      <div class="rv-cm-m">${esc(c.by)} · ${esc(fmtDate(c.at))}${c.resolved ? ` · ✔ ${tx('resolved')}` : ''}${c.stale ? ` · <span class="rv-stale">⚠ ${tx('changedSince')}</span>` : ''}
        <span class="rv-cm-a"><a onclick="ReviewUI.resolve(${c.id},${c.resolved ? 'false' : 'true'})">${c.resolved ? tx('reopen') : tx('resolve')}</a> · <a onclick="ReviewUI.delComment(${c.id})">${tx('del')}</a></span></div></div>`;
  }
  function cardInner(q) {
    const r = q.review;
    const t = q.topicTitle ? loc(q.topicTitle) : q.topic;
    const status = r.approved
      ? `<div class="rv-appr">✅ ${esc(tx('approvedBy', r.approvedBy, fmtDate(r.approvedAt)))} <a onclick="ReviewUI.unapprove('${q.id}')">${tx('unapprove')}</a></div>`
      : `<div class="rv-act"><button class="btn-primary rv-btn" onclick="ReviewUI.approve('${q.id}')">${tx('approve')}</button>${r.approvedStale ? `<span class="rv-stale">⚠ ${tx('staleApproval')}</span>` : ''}</div>`;
    return `<div class="rv-qh"><b>${esc(q.id)}</b><span>${q.chapter && cur === 'MASTER' ? esc(q.chapter) + ' · ' : ''}${tx('topic')}: ${esc(t)} · ${tx('diff')} ${q.difficulty}</span></div>
      <div class="rv-quote"><span class="rv-ref">${tx('quote')} ${esc(q.ref)}</span><span class="rv-ar rv-q-ar">${esc(q.quote)}</span></div>
      <div class="rv-stem">${esc(q.stem.en)}</div><div class="rv-stem rv-tr">${esc(q.stem.tr)}</div>
      ${q.options.map((o, i) => optHtml(q, o, i)).join('')}
      ${status}
      <div class="rv-cms"><div class="rv-cms-h">💬 ${tx('comments')} (${r.comments.length})</div>
        ${r.comments.length ? r.comments.map(commentHtml).join('') : `<div class="rv-none">${tx('none')}</div>`}
        <textarea id="rv-ta-${q.id}" rows="2" placeholder="${esc(tx('placeholder'))}"></textarea>
        <button class="btn-secondary rv-btn" onclick="ReviewUI.comment('${q.id}')">${tx('add')}</button></div>`;
  }
  const matches = (q) => filter === 'all' || (filter === 'todo' && !q.review.approved) || (filter === 'approved' && q.review.approved)
    || (filter === 'open' && q.review.comments.some(c => !c.resolved));
  function paintList() {
    const el = document.getElementById('rv-list');
    if (!el) return;
    const shown = questions.filter(matches);
    const sc = document.getElementById('rv-shown');
    if (sc) sc.textContent = tx('shown', shown.length, questions.length);
    el.innerHTML = shown.length ? shown.map(q => `<div class="rv-card ${q.review.approved ? 'ok' : ''}" id="rv-c-${q.id}">${cardInner(q)}</div>`).join('') : `<div class="rv-none">${tx('empty')}</div>`;
  }
  function repaintCard(qid) {
    const q = questions.find(x => x.id === qid);
    const el = document.getElementById('rv-c-' + qid);
    if (q && el) { el.className = 'rv-card ' + (q.review.approved ? 'ok' : ''); el.innerHTML = cardInner(q); }
    refreshCounts();
  }
  function setReview(qid, r) { const q = questions.find(x => x.id === qid); if (q && r) q.review = r; repaintCard(qid); }

  // ── actions ───────────────────────────────────────────────────────────────
  async function approve(qid) { const r = await api(`${qid}/approve`, {}); if (r.ok) setReview(qid, r.data.review); }
  async function unapprove(qid) { const r = await api(`${qid}/unapprove`, {}); if (r.ok) setReview(qid, r.data.review); }
  async function comment(qid) {
    const ta = document.getElementById('rv-ta-' + qid);
    const body = ta && ta.value.trim();
    if (!body) return;
    const r = await api(`${qid}/comment`, { body });
    if (r.ok) setReview(qid, r.data.review);
  }
  function qidOfComment(cid) { const q = questions.find(x => x.review.comments.some(c => c.id === cid)); return q && q.id; }
  async function resolve(cid, resolved) { const qid = qidOfComment(cid); const r = await api(`comment/${cid}/resolve`, { resolved }); if (r.ok) setReview(qid, r.data.review); }
  async function delComment(cid) {
    if (!confirm(tx('delConfirm'))) return;
    const qid = qidOfComment(cid); const r = await api(`comment/${cid}`, undefined, 'DELETE'); if (r.ok) setReview(qid, r.data.review);
  }
  function toggleLevel(L) { openLevels[L] = !openLevels[L]; paintTree(); }
  function setFilter(f) { filter = f; document.querySelectorAll('.rv-f').forEach(b => b.classList.toggle('on', b.dataset.f === f)); paintList(); }

  async function open(id) {
    cur = id; paintTree();
    const list = document.getElementById('rv-list');
    list.innerHTML = `<div class="rv-none">${tx('loading')}</div>`;
    const r = await api('chapter/' + id);
    if (!r.ok) { list.innerHTML = `<div class="rv-none">${tx('error')}</div>`; return; }
    questions = r.data.questions || [];
    document.getElementById('rv-title').textContent = id === 'MASTER' ? tx('master') : id;
    document.getElementById('rv-bar').style.display = '';
    paintList();
    document.getElementById('rv-right').scrollTop = 0;
  }

  async function render(ref) {
    const main = document.getElementById('main');
    cur = null; questions = [];
    main.innerHTML = `
      <div class="topic-header"><h2>${esc(loc(ref.title))}</h2><p>${esc(tx('sub'))}</p></div>
      <div class="rv-wrap">
        <div class="rv-left" id="rv-tree"></div>
        <div class="rv-right" id="rv-right">
          <div class="rv-bar" id="rv-bar" style="display:none">
            <b id="rv-title"></b>
            ${['all', 'todo', 'open', 'approved'].map(f => `<button class="rv-f ${f === filter ? 'on' : ''}" data-f="${f}" onclick="ReviewUI.setFilter('${f}')">${tx(f)}</button>`).join('')}
            <span id="rv-shown" class="rv-shown"></span>
          </div>
          <div class="rv-exports"><a href="/api/tests/review/export?open=1">${tx('exportOpen')}</a> · <a href="/api/tests/review/export">${tx('exportAll')}</a></div>
          <div id="rv-list"><div class="rv-none">${tx('pick')}</div></div>
        </div>
      </div>`;
    paintTree();
    await refreshCounts();
  }

  const css = `
    .rv-wrap{display:flex;gap:18px;align-items:flex-start}
    .rv-left{flex:0 0 320px;max-height:calc(100vh - 190px);overflow:auto;position:sticky;top:8px;background:#fff;border:1px solid var(--border);border-radius:10px;padding:8px}
    .rv-right{flex:1;min-width:0;max-height:calc(100vh - 190px);overflow:auto;padding-right:4px}
    .rv-tree-h{font-weight:700;color:var(--green);padding:6px 8px;font-size:.9rem}
    .rv-level,.rv-ch{display:flex;justify-content:space-between;gap:8px;align-items:center;padding:7px 8px;border-radius:7px;cursor:pointer;font-size:.84rem}
    .rv-level{font-weight:700;margin-top:4px;background:var(--green-pale)}.rv-ch{padding-left:16px}.rv-ch:hover,.rv-level:hover{background:#dff0e6}
    .rv-ch.active,.rv-master.active{background:var(--green);color:#fff}.rv-ch.active .rv-cnt,.rv-master.active .rv-cnt{background:#fff;color:var(--green)}
    .rv-chn{min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
    .rv-cnt{background:#e5e7eb;border-radius:10px;padding:1px 8px;font-size:.74rem;font-weight:600;white-space:nowrap}.rv-cnt.done{background:#bbf7d0;color:#166534}
    .rv-open{margin-left:5px;font-size:.74rem;color:#b45309;white-space:nowrap}
    .rv-bar{display:flex;align-items:center;gap:8px;flex-wrap:wrap;position:sticky;top:0;background:var(--bg,#fff);padding:6px 0 10px;z-index:2}
    .rv-f{border:1.5px solid var(--border);background:#fff;border-radius:16px;padding:4px 12px;font:inherit;font-size:.8rem;cursor:pointer}.rv-f.on{background:var(--green);color:#fff;border-color:var(--green)}
    .rv-shown{font-size:.78rem;color:var(--muted);margin-left:auto}.rv-exports{font-size:.8rem;margin-bottom:10px}.rv-exports a{color:var(--green)}
    .rv-card{background:#fff;border:1px solid var(--border);border-left:5px solid #f59e0b;border-radius:10px;padding:14px 16px;margin-bottom:14px}.rv-card.ok{border-left-color:#16a34a}
    .rv-qh{display:flex;justify-content:space-between;gap:10px;flex-wrap:wrap;font-size:.78rem;color:var(--muted);margin-bottom:6px}
    .rv-quote{display:flex;justify-content:space-between;align-items:center;gap:10px;background:var(--green-pale);border-radius:8px;padding:8px 12px;margin-bottom:8px}
    .rv-ref{font-size:.76rem;color:var(--muted)}.rv-ar{font-family:var(--font-quran,'Amiri Quran','Amiri',serif);direction:rtl;font-size:1.25rem}.rv-q-ar{font-size:1.4rem}
    .rv-stem{font-weight:600;margin:4px 0}.rv-tr{color:var(--muted);font-weight:400;font-size:.88rem}
    .rv-opt{border:1px solid var(--border);border-radius:8px;padding:8px 10px;margin-top:8px}.rv-opt.right{border-color:#16a34a;background:#f0fdf4}
    .rv-opt-h{display:flex;gap:8px;align-items:center;flex-wrap:wrap}.rv-ok{margin-left:auto;font-size:.74rem;font-weight:700;color:#166534}
    .rv-why{font-size:.84rem;margin-top:4px;line-height:1.5}
    .rv-act,.rv-appr{margin-top:12px;display:flex;gap:10px;align-items:center;flex-wrap:wrap;font-size:.84rem}.rv-appr{color:#166534;font-weight:600}.rv-appr a{font-weight:400;color:var(--muted);cursor:pointer;text-decoration:underline}
    .rv-btn{padding:7px 16px;font-size:.84rem}.rv-stale{color:#b45309;font-size:.78rem}
    .rv-cms{margin-top:12px;border-top:1px dashed var(--border);padding-top:10px}.rv-cms-h{font-weight:700;font-size:.84rem;margin-bottom:6px}
    .rv-cms textarea{width:100%;box-sizing:border-box;border:1.5px solid var(--border);border-radius:8px;padding:8px;font:inherit;font-size:.86rem;margin:6px 0}
    .rv-cm{background:#fffbeb;border:1px solid #fde68a;border-radius:8px;padding:7px 10px;margin-bottom:6px}.rv-cm.res{background:#f3f4f6;border-color:var(--border);opacity:.75}
    .rv-cm-b{white-space:pre-wrap;font-size:.86rem}.rv-cm-m{font-size:.74rem;color:var(--muted);margin-top:3px}.rv-cm-a{float:right}.rv-cm-a a{cursor:pointer;color:var(--green);text-decoration:underline}
    .rv-none{color:var(--muted);font-size:.86rem;padding:10px 0}
    body.rtl .rv-wrap{flex-direction:row-reverse}
    @media(max-width:900px){.rv-wrap{flex-direction:column}.rv-left{position:static;flex:none;width:100%;max-height:260px;box-sizing:border-box}.rv-right{max-height:none}}
  `;
  const style = document.createElement('style');
  style.textContent = css;
  document.head.appendChild(style);

  return { render, open, toggleLevel, setFilter, approve, unapprove, comment, resolve, delComment };
})();
