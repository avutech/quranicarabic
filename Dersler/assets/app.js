/* Tashîh-i Hurûf Dersleri — belge / sunum modu denetleyicisi */
(function () {
  'use strict';

  /* ---------- tema ---------- */
  var root = document.documentElement;
  try {
    var saved = localStorage.getItem('th-theme');
    if (saved) root.setAttribute('data-theme', saved);
    else if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches)
      root.setAttribute('data-theme', 'dark');
    else root.setAttribute('data-theme', 'light');
  } catch (e) { root.setAttribute('data-theme', 'light'); }

  function toggleTheme() {
    var next = root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
    root.setAttribute('data-theme', next);
    try { localStorage.setItem('th-theme', next); } catch (e) {}
  }

  /* ---------- sol ders menüsü ---------- */
  var scrim = document.querySelector('.nav-scrim');
  var navBtn = document.querySelector('.nav-toggle');

  function navOpen() { return document.body.classList.contains('nav-open'); }
  function setNav(on) {
    document.body.classList.toggle('nav-open', on);
    if (scrim) scrim.hidden = !on;
    if (navBtn) navBtn.setAttribute('aria-expanded', on ? 'true' : 'false');
  }

  // açık dersi menüde görünür kıl
  (function () {
    var cur = document.querySelector('.sidenav-body a.active');
    if (!cur) return;
    var box = document.querySelector('.sidenav-body');
    if (!box) return;
    var d = cur.offsetTop - box.clientHeight / 2 + cur.offsetHeight / 2;
    if (d > 0) box.scrollTop = d;
  })();

  /* ---------- slaytlar ---------- */
  var slides = Array.prototype.slice.call(document.querySelectorAll('.slide'));
  var idx = 0;
  var presenting = false;

  // slayt numaralarını yerleştir
  slides.forEach(function (s, i) {
    var tag = s.querySelector('.slide-no');
    if (!tag) {
      tag = document.createElement('div');
      tag.className = 'slide-no';
      s.insertBefore(tag, s.firstChild);
    }
    tag.textContent = 'SLAYT ' + (i + 1) + ' / ' + slides.length;
    s.id = s.id || ('slayt-' + (i + 1));
  });

  var bar = document.querySelector('.deck-bar');
  var countEl = bar ? bar.querySelector('.count') : null;
  var prog = document.querySelector('.progress');

  function show(n) {
    if (!slides.length) return;
    idx = Math.max(0, Math.min(slides.length - 1, n));
    slides.forEach(function (s, i) { s.classList.toggle('active', i === idx); });
    if (countEl) countEl.textContent = (idx + 1) + ' / ' + slides.length;
    if (prog) prog.style.width = ((idx + 1) / slides.length * 100) + '%';
    var act = slides[idx];
    if (act) act.scrollTop = 0;
  }

  function setPresent(on) {
    presenting = on;
    if (on) setNav(false);
    document.body.classList.toggle('present', on);
    var b = document.getElementById('mode-btn');
    if (b) b.textContent = on ? 'Belge modu' : 'Sunum modu';
    if (on) show(idx); else {
      slides.forEach(function (s) { s.classList.remove('active'); });
      var t = slides[idx];
      if (t) t.scrollIntoView({ block: 'start' });
    }
  }

  function next() { if (idx < slides.length - 1) show(idx + 1); }
  function prev() { if (idx > 0) show(idx - 1); }

  function fullscreen() {
    if (!document.fullscreenElement) {
      (document.documentElement.requestFullscreen || function () {}).call(document.documentElement);
      if (!presenting) setPresent(true);
    } else if (document.exitFullscreen) document.exitFullscreen();
  }

  /* ---------- klavye ---------- */
  document.addEventListener('keydown', function (e) {
    var tag = (e.target.tagName || '').toLowerCase();
    if (tag === 'input' || tag === 'textarea' || e.target.isContentEditable) return;

    if (e.key === 'p' || e.key === 'P') { e.preventDefault(); setPresent(!presenting); return; }
    if (e.key === 'f' || e.key === 'F') { e.preventDefault(); fullscreen(); return; }
    if (e.key === 't' || e.key === 'T') { e.preventDefault(); toggleTheme(); return; }
    if (e.key === 'm' || e.key === 'M') { e.preventDefault(); setNav(!navOpen()); return; }
    if (e.key === 'Escape' && navOpen()) { e.preventDefault(); setNav(false); return; }

    if (!presenting) return;   // belge modunda oklar normal kaydırır

    switch (e.key) {
      case 'ArrowRight': case 'ArrowDown': case ' ': case 'PageDown':
        e.preventDefault(); next(); break;
      case 'ArrowLeft': case 'ArrowUp': case 'PageUp':
        e.preventDefault(); prev(); break;
      case 'Home': e.preventDefault(); show(0); break;
      case 'End':  e.preventDefault(); show(slides.length - 1); break;
      case 'Escape': e.preventDefault(); setPresent(false); break;
    }
  });

  /* ---------- düğmeler ---------- */
  document.addEventListener('click', function (e) {
    var el = e.target.closest('[data-act]');
    if (!el) return;
    var a = el.getAttribute('data-act');
    if (a === 'mode')   { e.preventDefault(); setPresent(!presenting); }
    if (a === 'next')   { e.preventDefault(); next(); }
    if (a === 'prev')   { e.preventDefault(); prev(); }
    if (a === 'theme')  { e.preventDefault(); toggleTheme(); }
    if (a === 'nav')       { e.preventDefault(); setNav(!navOpen()); }
    if (a === 'nav-close') { e.preventDefault(); setNav(false); }
    if (a === 'full')   { e.preventDefault(); fullscreen(); }
    if (a === 'print')  { e.preventDefault(); if (presenting) setPresent(false); setTimeout(function(){ window.print(); }, 60); }
  });

  /* ---------- dokunmatik ---------- */
  var x0 = null;
  document.addEventListener('touchstart', function (e) { x0 = e.changedTouches[0].clientX; }, { passive: true });
  document.addEventListener('touchend', function (e) {
    if (!presenting || x0 === null) return;
    var dx = e.changedTouches[0].clientX - x0;
    if (Math.abs(dx) > 60) { dx < 0 ? next() : prev(); }
    x0 = null;
  }, { passive: true });

  show(0);
  slides.forEach(function (s) { s.classList.remove('active'); });
})();
