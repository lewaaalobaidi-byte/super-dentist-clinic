// Shared script for every page of the Super Dentist Clinic site.
(function () {
  var root = document.documentElement;

  var WA_TEXT = {
    ar: 'مرحباً، أود حجز موعد في عيادة سوبر دينتست',
    en: "Hello, I'd like to book an appointment at Super Dentist Clinic",
    ku: 'سڵاو، دەمەوێت نۆرەیەک بگرم لە کلینیکی سوپەر دێنتست'
  };
  var UI = {
    before: { ar: 'قبل', en: 'Before', ku: 'پێش' },
    after: { ar: 'بعد', en: 'After', ku: 'دوای' },
    original: { ar: 'بلغة المراجع الأصلية', en: 'Original language', ku: 'بە زمانی ڕەسەن' }
  };
  var current = 'ar';

  // ---------- Language ----------
  function changeLang(lang) {
    if (['ar', 'en', 'ku'].indexOf(lang) < 0) lang = 'ar';
    current = lang;
    root.setAttribute('lang', lang);
    root.setAttribute('dir', lang === 'en' ? 'ltr' : 'rtl');
    var t = root.getAttribute('data-title-' + lang);
    if (t) document.title = t;

    ['ar', 'en', 'ku'].forEach(function (b) {
      var el = document.getElementById('btn-' + b);
      if (!el) return;
      var on = b === lang;
      el.classList.toggle('bg-navyBlue', on);
      el.classList.toggle('text-white', on);
      el.classList.toggle('text-navyBlue', !on);
      el.setAttribute('aria-pressed', on ? 'true' : 'false');
    });

    document.querySelectorAll('a.wa-link').forEach(function (a) {
      var base = a.getAttribute('href').split('?')[0];
      var text = a.getAttribute('data-wa-' + lang) || WA_TEXT[lang];
      a.setAttribute('href', base + '?text=' + encodeURIComponent(text));
    });

    document.querySelectorAll('[data-i18n]').forEach(function (el) {
      var key = el.getAttribute('data-i18n');
      if (UI[key]) el.textContent = UI[key][lang];
    });

    try { localStorage.setItem('sd-lang', lang); } catch (e) {}
  }
  window.changeLang = changeLang;

  // ---------- Image fallback (shows a grey box while photos are missing) ----------
  function fallback(img) {
    img.addEventListener('error', function () {
      if (img.dataset.fallback) return;
      img.dataset.fallback = '1';
      img.src = 'https://placehold.co/800x600/e2e8f0/1a365d?text=' + encodeURIComponent(img.getAttribute('data-label') || img.alt || 'Photo');
    }, { once: true });
  }

  // ---------- Mobile menu ----------
  function initMenu() {
    var btn = document.getElementById('mobile-menu-btn');
    var menu = document.getElementById('mobile-menu');
    if (!btn || !menu) return;
    function set(open) {
      menu.classList.toggle('hidden', !open);
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
    }
    btn.addEventListener('click', function (e) { e.stopPropagation(); set(menu.classList.contains('hidden')); });
    menu.querySelectorAll('a').forEach(function (a) { a.addEventListener('click', function () { set(false); }); });
    document.addEventListener('click', function (e) { if (!menu.contains(e.target)) set(false); });
  }

  // ---------- Doctor cards on the homepage ----------
  function initCards() {
    var cards = document.querySelectorAll('.specialist-card');
    cards.forEach(function (card) {
      card.addEventListener('click', function () {
        cards.forEach(function (c) { c.classList.remove('active'); });
        card.classList.add('active');
      });
    });
  }

  // ---------- Reviews (homepage) ----------
  function renderReviews() {
    var box = document.getElementById('reviews-list');
    var list = window.REVIEWS || [];
    if (!box || !list.length) return;
    box.innerHTML = '';
    list.forEach(function (r) {
      var card = document.createElement('div');
      card.className = 'glass-panel p-5 md:p-6 rounded-2xl md:rounded-3xl bg-white/80';
      var head = document.createElement('div');
      head.className = 'flex justify-between items-start mb-2 gap-3';
      var name = document.createElement('h4');
      name.className = 'font-bold text-navyBlue text-base md:text-lg';
      name.textContent = r.name;
      var stars = document.createElement('span');
      stars.className = 'text-yellow-500 text-sm whitespace-nowrap';
      stars.textContent = '★★★★★'.slice(0, r.stars || 5);
      head.appendChild(name); head.appendChild(stars);
      var p = document.createElement('p');
      p.className = 'text-navyBlue/90 font-semibold text-sm md:text-base leading-relaxed';
      p.textContent = '"' + r.text + '"';
      if (r.lang) p.setAttribute('lang', r.lang);
      if (r.lang) p.setAttribute('dir', r.lang === 'en' ? 'ltr' : 'rtl');
      card.appendChild(head); card.appendChild(p);
      if (r.date) {
        var d = document.createElement('span');
        d.className = 'block mt-2 text-xs text-navyBlue/60';
        d.textContent = 'Google · ' + r.date;
        card.appendChild(d);
      }
      box.appendChild(card);
    });
    box.classList.remove('hidden');
  }

  // ---------- Before / after gallery ----------
  function makeSlider(item) {
    var wrap = document.createElement('div');
    wrap.className = 'ba rounded-2xl';
    wrap.setAttribute('dir', 'ltr');
    wrap.style.setProperty('--pos', '50%');

    var after = document.createElement('img');
    after.src = item.after; after.alt = 'After'; after.loading = 'lazy';
    after.setAttribute('data-label', 'After');
    var before = document.createElement('img');
    before.src = item.before; before.alt = 'Before'; before.loading = 'lazy';
    before.className = 'ba-before'; before.setAttribute('data-label', 'Before');
    fallback(after); fallback(before);

    var line = document.createElement('div'); line.className = 'ba-line';
    var knob = document.createElement('div'); knob.className = 'ba-knob'; knob.textContent = '⇆';
    line.appendChild(knob);

    var tagB = document.createElement('span'); tagB.className = 'ba-tag'; tagB.style.left = '10px';
    tagB.setAttribute('data-i18n', 'before'); tagB.textContent = UI.before[current];
    var tagA = document.createElement('span'); tagA.className = 'ba-tag'; tagA.style.right = '10px';
    tagA.setAttribute('data-i18n', 'after'); tagA.textContent = UI.after[current];

    var range = document.createElement('input');
    range.type = 'range'; range.min = 0; range.max = 100; range.value = 50;
    range.setAttribute('aria-label', 'Before / after');
    range.addEventListener('input', function () { wrap.style.setProperty('--pos', range.value + '%'); });

    [after, before, line, tagB, tagA, range].forEach(function (el) { wrap.appendChild(el); });
    return wrap;
  }

  function renderGallery() {
    var grid = document.getElementById('gallery-grid');
    var cases = window.CASES || [];
    if (!grid) return;
    var empty = document.getElementById('gallery-empty');
    var buttons = document.querySelectorAll('.filter-btn');

    function show(cat) {
      grid.innerHTML = '';
      var shown = cases.filter(function (c) { return cat === 'all' || c.cat === cat; });
      shown.forEach(function (c) {
        var fig = document.createElement('figure');
        fig.className = 'card rounded-3xl p-3';
        fig.appendChild(makeSlider(c));
        if (c.caption) {
          var cap = document.createElement('figcaption');
          cap.className = 'px-2 pt-3 pb-1 font-bold text-navyBlue';
          ['ar', 'en', 'ku'].forEach(function (l) {
            if (!c.caption[l]) return;
            var s = document.createElement('span');
            s.className = 'lang-text lang-' + l;
            s.textContent = c.caption[l];
            cap.appendChild(s);
          });
          fig.appendChild(cap);
        }
        grid.appendChild(fig);
      });
      if (empty) empty.classList.toggle('hidden', shown.length > 0);
      buttons.forEach(function (b) { b.classList.toggle('is-active', b.getAttribute('data-cat') === cat); });
    }

    buttons.forEach(function (b) {
      b.addEventListener('click', function () {
        var cat = b.getAttribute('data-cat');
        show(cat);
        history.replaceState(null, '', cat === 'all' ? location.pathname : '#' + cat);
      });
    });
    var start = (location.hash || '').replace('#', '');
    var valid = Array.prototype.some.call(buttons, function (b) { return b.getAttribute('data-cat') === start; });
    show(valid ? start : 'all');
  }

  // ---------- Clinic tour + lightbox ----------
  function renderTour() {
    var grid = document.getElementById('tour-grid');
    var photos = window.TOUR || [];
    if (!grid) return;
    var box = document.getElementById('lightbox');
    var boxImg = document.getElementById('lightbox-img');

    photos.forEach(function (p) {
      var btn = document.createElement('button');
      btn.type = 'button';
      btn.className = 'group card rounded-3xl overflow-hidden text-start';
      var img = document.createElement('img');
      img.src = p.src; img.alt = p.caption.en; img.loading = 'lazy';
      img.setAttribute('data-label', p.caption.en);
      img.className = 'w-full aspect-[4/3] object-cover group-hover:scale-105 transition-transform duration-500';
      fallback(img);
      var cap = document.createElement('div');
      cap.className = 'p-4 font-bold text-navyBlue';
      ['ar', 'en', 'ku'].forEach(function (l) {
        var s = document.createElement('span');
        s.className = 'lang-text lang-' + l;
        s.textContent = p.caption[l];
        cap.appendChild(s);
      });
      var imgWrap = document.createElement('div'); imgWrap.className = 'overflow-hidden';
      imgWrap.appendChild(img);
      btn.appendChild(imgWrap); btn.appendChild(cap);
      btn.addEventListener('click', function () {
        if (!box) return;
        boxImg.src = img.src; boxImg.alt = img.alt;
        box.classList.remove('hidden'); box.classList.add('flex');
      });
      grid.appendChild(btn);
    });

    if (box) {
      box.addEventListener('click', function () { box.classList.add('hidden'); box.classList.remove('flex'); });
      document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape') { box.classList.add('hidden'); box.classList.remove('flex'); }
      });
    }
  }

  // ---------- Start ----------
  document.querySelectorAll('img').forEach(fallback);
  var saved = 'ar';
  try { saved = localStorage.getItem('sd-lang') || 'ar'; } catch (e) {}
  current = saved;
  renderReviews();
  renderGallery();
  renderTour();
  changeLang(saved);
  initMenu();
  initCards();

  // Background video: pause when scrolled out of view (saves battery and data)
  var v = document.getElementById('bg-video');
  if (v) {
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
      v.pause();
    } else if ('IntersectionObserver' in window) {
      new IntersectionObserver(function (entries) {
        entries.forEach(function (e) {
          if (e.isIntersecting) { var p = v.play(); if (p && p.catch) p.catch(function () {}); }
          else v.pause();
        });
      }).observe(v);
    }
  }

  var y = document.getElementById('year');
  if (y) y.textContent = new Date().getFullYear();
})();
