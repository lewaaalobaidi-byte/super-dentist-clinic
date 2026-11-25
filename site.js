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
    readMore: { ar: 'اقرأ المزيد', en: 'Read more', ku: 'زیاتر بخوێنەوە' },
    less: { ar: 'عرض أقل', en: 'Show less', ku: 'کەمتر' }
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

    document.querySelectorAll('[data-month]').forEach(function (el) {
      if (window.__monthLabel) el.textContent = window.__monthLabel(el.getAttribute('data-month'), lang);
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

  // ---------- Google reviews (homepage) ----------
  function monthLabel(ym, lang) {
    var p = ym.split('-'), d = new Date(+p[0], +p[1] - 1, 15);
    try { return new Intl.DateTimeFormat(lang === 'en' ? 'en-GB' : 'ar-IQ-u-nu-latn', { month: 'long', year: 'numeric' }).format(d); }
    catch (e) { return ym; }
  }
  window.__monthLabel = monthLabel;
  var COLORS = ['#1a73e8', '#0f9d58', '#f4b400', '#db4437', '#7b1fa2', '#00838f', '#5d4037', '#c2185b'];
  function avatar(name, photo) {
    var el;
    if (photo) {
      el = document.createElement('img');
      el.src = photo; el.alt = ''; el.referrerPolicy = 'no-referrer'; el.loading = 'lazy';
      el.className = 'w-11 h-11 rounded-full object-cover shrink-0';
      return el;
    }
    el = document.createElement('div');
    var h = 0; for (var i = 0; i < name.length; i++) h = (h * 31 + name.charCodeAt(i)) >>> 0;
    el.className = 'w-11 h-11 rounded-full shrink-0 flex items-center justify-center text-white font-black text-lg';
    el.style.background = COLORS[h % COLORS.length];
    el.textContent = (name.trim()[0] || '?').toUpperCase();
    return el;
  }

  function reviewCard(r) {
    var card = document.createElement('article');
    card.className = 'card snap-start shrink-0 w-[85%] sm:w-[46%] lg:w-[31.5%] rounded-3xl p-6 flex flex-col gap-4';

    var head = document.createElement('div'); head.className = 'flex items-center gap-3';
    head.appendChild(avatar(r.name, r.photo));
    var who = document.createElement('div'); who.className = 'min-w-0 flex-1';
    var nm = document.createElement(r.url ? 'a' : 'div');
    if (r.url) { nm.href = r.url; nm.target = '_blank'; nm.rel = 'noopener'; }
    nm.className = 'block font-bold text-navyBlue truncate hover:text-deepBlue text-left rtl:text-right'; nm.textContent = r.name; nm.style.unicodeBidi = 'plaintext';
    var dt = document.createElement('div'); dt.className = 'text-xs font-semibold text-slate-500 text-left rtl:text-right';
    if (r.month) { dt.setAttribute('data-month', r.month); dt.textContent = monthLabel(r.month, current); } else dt.textContent = r.date || '';
    who.appendChild(nm); who.appendChild(dt);
    var g = document.createElement('span');
    g.innerHTML = '<svg class="w-5 h-5" viewBox="0 0 24 24" aria-label="Google"><path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" fill="#4285F4"/><path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853"/><path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z" fill="#FBBC05"/><path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" fill="#EA4335"/></svg>';
    head.appendChild(who); head.appendChild(g);

    var stars = document.createElement('div');
    stars.className = 'text-yellow-400 text-lg tracking-wider leading-none'; stars.setAttribute('aria-label', (r.stars || 5) + ' / 5');
    var n = Math.round(r.stars || 5); stars.innerHTML = '★★★★★'.slice(0, n) + '<span class="text-slate-200">' + '★★★★★'.slice(0, 5 - n) + '</span>';

    var txt = document.createElement('p');
    txt.className = 'text-slate-700 font-normal leading-relaxed line-clamp-5 whitespace-pre-line'; txt.setAttribute('dir', 'auto');
    txt.textContent = r.text || '';
    var more = document.createElement('button');
    more.type = 'button'; more.className = 'hidden self-start text-sm font-bold text-deepBlue hover:underline';
    more.setAttribute('data-i18n', 'readMore'); more.textContent = UI.readMore[current];
    more.addEventListener('click', function () {
      var open = txt.classList.toggle('line-clamp-5');
      more.setAttribute('data-i18n', open ? 'readMore' : 'less');
      more.textContent = UI[open ? 'readMore' : 'less'][current];
    });
    [head, stars, txt, more].forEach(function (el) { card.appendChild(el); });
    requestAnimationFrame(function () { if (txt.scrollHeight > txt.clientHeight + 2) more.classList.remove('hidden'); });
    return card;
  }

  function showReviews(list, fromGoogle) {
    var wrap = document.getElementById('reviews-wrap');
    var track = document.getElementById('reviews-track');
    if (!wrap || !track || !list.length) return;
    track.innerHTML = '';
    list.forEach(function (r) { track.appendChild(reviewCard(r)); });
    crystalizeAll(track);
    wrap.classList.remove('hidden');
    var empty = document.getElementById('reviews-empty'); if (empty) empty.classList.add('hidden');
    var at = document.getElementById('rv-attrib'); if (at) at.classList.toggle('hidden', !fromGoogle);

    // dots + arrows + gentle auto-play
    var dots = document.getElementById('rv-dots'); dots.innerHTML = '';
    var cards = track.children;
    Array.prototype.forEach.call(cards, function (c, i) {
      var d = document.createElement('button'); d.type = 'button'; d.setAttribute('aria-label', 'Review ' + (i + 1));
      d.className = 'w-2.5 h-2.5 rounded-full bg-navyBlue/20 transition-all';
      d.addEventListener('click', function () { go(i); }); dots.appendChild(d);
    });
    var idx = 0;
    function go(i) {
      idx = (i + cards.length) % cards.length;
      var c = cards[idx];
      track.scrollTo({ left: c.offsetLeft - track.offsetLeft - (root.dir === 'rtl' ? track.clientWidth - c.offsetWidth : 0), behavior: 'smooth' });
    }
    function step(dir) {
      var maxed = Math.abs(track.scrollLeft) + track.clientWidth >= track.scrollWidth - 8;
      if (dir > 0 && maxed) go(0); else go(idx + dir);
    }
    track.addEventListener('scroll', function () {
      var best = 0, bestD = Infinity, tr = track.getBoundingClientRect(), rtl = root.dir === 'rtl';
      Array.prototype.forEach.call(cards, function (c, i) {
        var r = c.getBoundingClientRect(), dd = rtl ? Math.abs(r.right - tr.right) : Math.abs(r.left - tr.left);
        if (dd < bestD) { bestD = dd; best = i; }
      });
      idx = best;
      Array.prototype.forEach.call(dots.children, function (d, i) {
        d.className = 'h-2.5 rounded-full transition-all ' + (i === best ? 'w-6 bg-deepBlue' : 'w-2.5 bg-navyBlue/20');
      });
    }, { passive: true });
    track.dispatchEvent(new Event('scroll'));
    document.getElementById('rv-prev').onclick = function () { step(-1); };
    document.getElementById('rv-next').onclick = function () { step(1); };
    var paused = false;
    wrap.addEventListener('mouseenter', function () { paused = true; });
    wrap.addEventListener('mouseleave', function () { paused = false; });
    track.addEventListener('touchstart', function () { paused = true; }, { passive: true });
    if (!window.matchMedia('(prefers-reduced-motion: reduce)').matches && cards.length > 1) {
      setInterval(function () { if (!paused && !document.hidden) step(1); }, 6000);
    }
  }

  function renderReviews() {
    if (!document.getElementById('reviews-track')) return;
    // Trustindex widget: use it when it loads, otherwise fall back to the manual list
    var ti = document.getElementById('ti-widget');
    if (ti) {
      var hasWidget = function () {
        return Array.prototype.some.call(ti.children, function (c) { return c.tagName !== 'SCRIPT' && c.offsetHeight > 20; });
      };
      var done = false;
      var useWidget = function () {
        if (done) return; done = true;
        var sum = document.getElementById('g-summary'); if (sum) sum.classList.add('hidden');
        var empty = document.getElementById('reviews-empty'); if (empty) empty.classList.add('hidden');
      };
      new MutationObserver(function () { if (hasWidget()) useWidget(); }).observe(ti, { childList: true, subtree: true });
      setTimeout(function () {
        if (hasWidget()) { useWidget(); return; }
        done = true;
        ti.classList.add('hidden');
        showReviews(window.REVIEWS || [], false);
      }, 8000);
      return;
    }
    var cfg = window.GOOGLE_REVIEWS || {};
    if (cfg.apiKey && cfg.placeId) {
      loadGoogleReviews(cfg).catch(function () { showReviews(window.REVIEWS || [], false); });
    } else {
      showReviews(window.REVIEWS || [], false);
    }
  }

  // Live reviews from Google (Places API, New). Needs apiKey + placeId in index.html.
  function loadGoogleReviews(cfg) {
    return new Promise(function (resolve, reject) {
      window.__sdGoogleReady = resolve;
      var sc = document.createElement('script');
      sc.src = 'https://maps.googleapis.com/maps/api/js?key=' + encodeURIComponent(cfg.apiKey) +
               '&v=weekly&loading=async&language=' + (current === 'ku' ? 'ar' : current) + '&callback=__sdGoogleReady';
      sc.async = true; sc.onerror = reject;
      document.head.appendChild(sc);
    }).then(function () {
      return google.maps.importLibrary('places');
    }).then(function (lib) {
      var place = new lib.Place({ id: cfg.placeId });
      return place.fetchFields({ fields: ['rating', 'userRatingCount', 'reviews', 'googleMapsURI'] }).then(function () { return place; });
    }).then(function (place) {
      if (place.rating) document.getElementById('g-rating').textContent = place.rating.toFixed(1);
      if (place.userRatingCount) document.getElementById('g-count').textContent = place.userRatingCount;
      if (place.googleMapsURI) document.getElementById('g-count-link').href = place.googleMapsURI;
      document.getElementById('g-write').href = 'https://search.google.com/local/writereview?placeid=' + encodeURIComponent(cfg.placeId);
      var list = (place.reviews || []).filter(function (r) { return r.text; }).map(function (r) {
        var a = r.authorAttribution || {};
        return { name: a.displayName || 'Google user', photo: a.photoURI, url: a.uri, stars: r.rating,
                 date: r.relativePublishTimeDescription, text: r.text };
      });
      if (!list.length) throw new Error('no reviews');
      showReviews(list, true);
    });
  }

  // Load an image off-screen; resolve true if it exists
  function probe(src) {
    return new Promise(function (res) { var i = new Image(); i.onload = function () { res(i.naturalWidth > 0); }; i.onerror = function () { res(false); }; i.src = src; });
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
    var knob = document.createElement('div'); knob.className = 'ba-knob'; knob.innerHTML = '<i class="fa-solid fa-arrows-left-right" aria-hidden="true"></i>';
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
    if (!grid) return;
    var empty = document.getElementById('gallery-empty');
    var buttons = document.querySelectorAll('.filter-btn');
    var bar = document.getElementById('gallery-filters');
    Promise.all((window.CASES || []).map(function (c) {
      return Promise.all([probe(c.before), probe(c.after)]).then(function (r) { return r[0] && r[1] ? c : null; });
    })).then(function (found) {
      var cases = found.filter(Boolean);
      // hide filter buttons for categories with no real cases
      buttons.forEach(function (b) {
        var cat = b.getAttribute('data-cat');
        if (cat !== 'all' && !cases.some(function (c) { return c.cat === cat; })) b.classList.add('hidden');
      });
      if (bar) bar.classList.toggle('hidden', cases.length === 0);
      function show(cat) {
        grid.innerHTML = '';
        var shown = cases.filter(function (c) { return cat === 'all' || c.cat === cat; });
        shown.forEach(function (c) {
          var fig = document.createElement('figure');
          fig.className = 'card rounded-[20px] p-3';
          fig.appendChild(makeSlider(c));
          if (c.caption) {
            var cap = document.createElement('figcaption');
            cap.className = 'px-2 pt-3 pb-1 font-semibold text-navyBlue';
            ['ar', 'en', 'ku'].forEach(function (l) {
              if (!c.caption[l]) return;
              var sp = document.createElement('span'); sp.className = 'lang-text lang-' + l; sp.textContent = c.caption[l]; cap.appendChild(sp);
            });
            fig.appendChild(cap);
          }
          grid.appendChild(fig);
        });
        crystalizeAll(grid);
        if (empty) empty.classList.toggle('hidden', shown.length > 0);
        buttons.forEach(function (b) { b.classList.toggle('is-active', b.getAttribute('data-cat') === cat); });
      }
      buttons.forEach(function (b) {
        b.addEventListener('click', function () {
          var cat = b.getAttribute('data-cat'); show(cat);
          history.replaceState(null, '', cat === 'all' ? location.pathname : '#' + cat);
        });
      });
      var start = (location.hash || '').replace('#', '');
      var valid = cases.some(function (c) { return c.cat === start; });
      show(valid ? start : 'all');
    });
  }

  // ---------- Clinic tour + lightbox ----------
  function renderTour() {
    var grid = document.getElementById('tour-grid');
    var photos = window.TOUR || [];
    if (!grid) return;
    var box = document.getElementById('lightbox');
    var boxImg = document.getElementById('lightbox-img');

    var tourEmpty = document.getElementById('tour-empty');
    Promise.all(photos.map(function (p) { return probe(p.src).then(function (ok) { return ok ? p : null; }); })).then(function (found) {
    found = found.filter(Boolean);
    if (tourEmpty) tourEmpty.classList.toggle('hidden', found.length > 0);
    found.forEach(function (p) {
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
    crystalizeAll(grid);
    });

    if (box) {
      box.addEventListener('click', function () { box.classList.add('hidden'); box.classList.remove('flex'); });
      document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape') { box.classList.add('hidden'); box.classList.remove('flex'); }
      });
    }
  }

  // ---------- Phone booking bar ----------
  function initMobileCta() {
    var bar = document.getElementById('mobile-cta');
    var heroBtns = document.querySelector('#home .wa-link');
    if (!bar || !heroBtns || !('IntersectionObserver' in window)) return;
    new IntersectionObserver(function (e) {
      bar.style.transform = e[0].isIntersecting ? 'translateY(110%)' : 'translateY(0)';
    }).observe(heroBtns);
  }


  // ---------- Crystal glass (adapted from "Glass Card" by educalvolpz, 21st.dev) ----------
  var CG_LAYERS = ['cg-lens', 'cg-spec'];
  var fineHover = window.matchMedia('(hover: hover) and (pointer: fine)').matches &&
                  !window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  function crystalize(el) {
    if (!el || el.classList.contains('crystal-ready')) return;
    el.classList.add('crystal', 'crystal-ready');
    CG_LAYERS.forEach(function (c) {
      var d = document.createElement('span'); d.className = 'cg ' + c; d.setAttribute('aria-hidden', 'true');
      el.insertBefore(d, el.firstChild);
    });
    if (!fineHover) return;
    el.addEventListener('pointermove', function (e) {
      var r = el.getBoundingClientRect(), x = e.clientX - r.left, y = e.clientY - r.top;
      el.style.setProperty('--sx', (x - r.width * 0.3) + 'px');
      el.style.setProperty('--sy', (y - r.height * 0.28) + 'px');
      el.style.setProperty('--wx', (x - r.width / 2) + 'px');
      el.style.setProperty('--rx', ((x / r.width - 0.5) * 6) + 'px');
      el.style.setProperty('--ry', ((y / r.height - 0.5) * 6) + 'px');
    });
    el.addEventListener('pointerleave', function () {
      ['--sx', '--sy', '--wx', '--rx', '--ry'].forEach(function (v) { el.style.setProperty(v, '0px'); });
    });
  }
  function crystalizeAll(root) {
    (root || document).querySelectorAll('.card, .glass-panel, .stat-tile, .crystal-panel').forEach(crystalize);
  }
  window.crystalizeAll = crystalizeAll;


  // ---------- Service photos: use services/<slug>.jpg when it exists ----------
  function serviceCovers() {
    document.querySelectorAll('.svc-cover[data-photo]').forEach(function (box) {
      var src = box.getAttribute('data-photo');
      probe(src).then(function (ok) {
        if (!ok) return;
        var img = box.querySelector('img');
        if (!img) { img = document.createElement('img'); img.alt = ''; box.insertBefore(img, box.firstChild); }
        img.src = src; box.classList.add('has-photo');
      });
    });
  }


  // ---------- Aurora background (adapted from "Aurora Background" by pulkitxm, 21st.dev; "ice" palette) ----------
  function initAurora() {
    var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    var c = document.createElement('canvas');
    c.id = 'aurora-bg'; c.setAttribute('aria-hidden', 'true');
    document.body.insertBefore(c, document.body.firstChild);
    var ctx = c.getContext('2d'); if (!ctx) return;
    var SCALE = 0.25; // draw small, CSS scales it up (gradients stay smooth, very cheap)
    var palette = [
      ['hsla(38, 75%, 82%, 0.55)', 'hsla(32, 60%, 72%, 0.30)', 'rgba(0,0,0,0)'],
      ['hsla(28, 55%, 66%, 0.40)', 'rgba(0,0,0,0)', 'rgba(0,0,0,0)'],
      ['hsla(44, 80%, 88%, 0.45)', 'hsla(35, 55%, 78%, 0.22)', 'rgba(0,0,0,0)']
    ];
    var blobCount = 5, t = Math.random() * 10, speed = 0.55, last = 0;
    function resize() { c.width = Math.max(1, Math.round(innerWidth * SCALE)); c.height = Math.max(1, Math.round(innerHeight * SCALE)); }
    resize(); addEventListener('resize', resize);
    function draw() {
      var w = c.width, h = c.height, R = Math.max(w, h);
      ctx.clearRect(0, 0, w, h);
      for (var i = 0; i < blobCount; i++) {
        var L = palette[i % palette.length], ph = (i / blobCount) * Math.PI * 2 + t;
        var x = w / 2 + Math.sin(ph) * (w * .32) + Math.cos(t * .5) * (w * .12);
        var y = h / 2 + Math.cos(ph * .7) * (h * .3) + Math.sin(t * .3) * (h * .12);
        var g = ctx.createRadialGradient(x, y, 0, x, y, R * .45);
        g.addColorStop(0, L[0]); g.addColorStop(.5, L[1]); g.addColorStop(1, L[2]);
        ctx.fillStyle = g; ctx.fillRect(0, 0, w, h);
      }
      ctx.globalCompositeOperation = 'screen';
      for (var k = 0; k < 2; k++) {
        var ph2 = (k / 2) * Math.PI + t * .8;
        var x2 = w / 2 + Math.sin(ph2 * 1.2) * (w * .22), y2 = h / 2 + Math.cos(ph2 * .9) * (h * .22);
        var g2 = ctx.createRadialGradient(x2, y2, 0, x2, y2, R * .38);
        g2.addColorStop(0, palette[k][0]); g2.addColorStop(1, 'rgba(0,0,0,0)');
        ctx.fillStyle = g2; ctx.fillRect(0, 0, w, h);
      }
      ctx.globalCompositeOperation = 'source-over';
    }
    function loop(now) {
      if (!document.hidden && now - last > 42) { last = now; t += 0.01 * speed * 2.4; draw(); }
      requestAnimationFrame(loop);
    }
    draw();
    if (!reduce) requestAnimationFrame(loop);
  }


  // ---------- Crystal bubbles: glass spheres drifting up over the aurora, behind every page ----------
  function initBubbles() {
    var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    var c = document.createElement('canvas');
    c.id = 'bubbles-bg'; c.setAttribute('aria-hidden', 'true');
    var aur = document.getElementById('aurora-bg');
    document.body.insertBefore(c, aur ? aur.nextSibling : document.body.firstChild);
    var ctx = c.getContext('2d'); if (!ctx) return;
    var dpr = Math.min(1.5, window.devicePixelRatio || 1), W, H;
    // One glass-bubble sprite, scaled for every bubble
    var S = 256, sp = document.createElement('canvas'); sp.width = sp.height = S;
    var g = sp.getContext('2d'), r = S / 2 - 2;
    var body = g.createRadialGradient(S / 2, S / 2, r * .55, S / 2, S / 2, r);
    body.addColorStop(0, 'rgba(255,255,255,0.02)');
    body.addColorStop(.78, 'rgba(255,240,215,0.16)');
    body.addColorStop(.93, 'rgba(255,236,205,0.45)');
    body.addColorStop(1, 'rgba(255,255,255,0.75)');
    g.fillStyle = body; g.beginPath(); g.arc(S / 2, S / 2, r, 0, Math.PI * 2); g.fill();
    // faint iridescent rim
    var iri = g.createLinearGradient(0, 0, S, S);
    iri.addColorStop(0, 'rgba(160,230,255,0.35)'); iri.addColorStop(.5, 'rgba(210,190,255,0.25)'); iri.addColorStop(1, 'rgba(140,255,230,0.3)');
    g.lineWidth = 3; g.strokeStyle = iri; g.beginPath(); g.arc(S / 2, S / 2, r - 2, 0, Math.PI * 2); g.stroke();
    // main specular highlight (top-left)
    g.save(); g.translate(S * .34, S * .3); g.rotate(-0.7);
    var hl = g.createRadialGradient(0, 0, 0, 0, 0, S * .17);
    hl.addColorStop(0, 'rgba(255,255,255,0.95)'); hl.addColorStop(.45, 'rgba(255,255,255,0.45)'); hl.addColorStop(1, 'rgba(255,255,255,0)');
    g.scale(1, .55); g.fillStyle = hl; g.beginPath(); g.arc(0, 0, S * .17, 0, Math.PI * 2); g.fill(); g.restore();
    // small reflected glint (bottom-right)
    var gl = g.createRadialGradient(S * .7, S * .74, 0, S * .7, S * .74, S * .07);
    gl.addColorStop(0, 'rgba(255,255,255,0.7)'); gl.addColorStop(1, 'rgba(255,255,255,0)');
    g.fillStyle = gl; g.beginPath(); g.arc(S * .7, S * .74, S * .07, 0, Math.PI * 2); g.fill();

    var bubbles = [], mx = -1e4, my = -1e4;
    function make(anyY) {
      var small = W < 768, rad = (small ? 10 : 14) + Math.pow(Math.random(), 1.8) * (small ? 42 : 70);
      return { x: Math.random() * W, y: anyY ? Math.random() * H : H + rad + Math.random() * 80, r: rad,
        vy: .12 + Math.random() * .28 + rad * .002, ph: Math.random() * 6.28, sw: .25 + Math.random() * .5,
        a: .55 + Math.random() * .45, px: 0, py: 0 };
    }
    function size() {
      W = innerWidth; H = innerHeight;
      c.width = Math.round(W * dpr); c.height = Math.round(H * dpr); ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      var n = W < 768 ? 11 : 20;
      while (bubbles.length < n) bubbles.push(make(true));
      bubbles.length = n;
    }
    size(); addEventListener('resize', size);
    addEventListener('pointermove', function (e) { mx = e.clientX; my = e.clientY; }, { passive: true });
    function draw() {
      ctx.clearRect(0, 0, W, H);
      for (var i = 0; i < bubbles.length; i++) {
        var b = bubbles[i], d = b.r * 2;
        ctx.globalAlpha = b.a;
        ctx.drawImage(sp, b.x + b.px - b.r, b.y + b.py - b.r, d, d);
      }
      ctx.globalAlpha = 1;
    }
    var last = 0;
    function step(now) {
      var dt = last ? Math.min(50, now - last) / 16.7 : 1; last = now;
      if (!document.hidden) {
        for (var i = 0; i < bubbles.length; i++) {
          var b = bubbles[i];
          b.y -= b.vy * dt; b.ph += .012 * dt; b.x += Math.sin(b.ph) * b.sw * .35 * dt;
          // gently drift away from the pointer
          var dx = b.x + b.px - mx, dy = b.y + b.py - my, dd = Math.sqrt(dx * dx + dy * dy), lim = b.r + 90;
          if (dd < lim && dd > .1) { var f = (1 - dd / lim) * 2.2; b.px += dx / dd * f; b.py += dy / dd * f; }
          b.px *= .96; b.py *= .96;
          if (b.y < -b.r - 20) bubbles[i] = make(false);
        }
        draw();
      }
      requestAnimationFrame(step);
    }
    draw();
    if (!reduce) requestAnimationFrame(step);
  }

  // ---------- Dental network (footer / Contact) ----------
  function initNetwork() {
    var host = document.getElementById('contact'); if (!host) return;
    var c = document.createElement('canvas'); c.className = 'net-canvas'; c.setAttribute('aria-hidden', 'true');
    host.insertBefore(c, host.firstChild);
    var ctx = c.getContext('2d'), W, H, dpr = Math.min(2, window.devicePixelRatio || 1);
    var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    var path = [[-.38,-.48],[-.55,-.42],[-.6,-.2],[-.55,.02],[-.48,.2],[-.44,.45],[-.34,.66],[-.22,.62],[-.16,.4],[-.08,.24],[0,.22],[.08,.24],[.16,.4],[.22,.62],[.34,.66],[.44,.45],[.48,.2],[.55,.02],[.6,-.2],[.55,-.42],[.38,-.48],[.2,-.44],[0,-.4],[-.2,-.44]];
    var targets = [];
    for (var i = 0; i < path.length; i++) { var a = path[i], b = path[(i + 1) % path.length]; for (var s = 0; s < 1; s += .34) targets.push([a[0] + (b[0] - a[0]) * s, a[1] + (b[1] - a[1]) * s]); }
    var pts = [];
    function size() { W = c.clientWidth; H = c.clientHeight; c.width = W * dpr; c.height = H * dpr; ctx.setTransform(dpr, 0, 0, dpr, 0, 0); }
    size(); addEventListener('resize', size);
    for (var k = 0; k < targets.length + 34; k++) pts.push({ x: Math.random() * W, y: Math.random() * H, vx: (Math.random() - .5) * .35, vy: (Math.random() - .5) * .35, t: k < targets.length ? targets[k] : null });
    var visible = false, start = performance.now();
    if ('IntersectionObserver' in window) new IntersectionObserver(function (e) { visible = e[0].isIntersecting; }).observe(host); else visible = true;
    function frame(now) {
      if (visible && !document.hidden) {
        var phase = (Math.sin((now - start) / 4500) + 1) / 2;
        var rtl = root.dir === 'rtl', small = W < 768;
        var cx = small ? W * .5 : (rtl ? W * .84 : W * .16), cy = small ? H * .2 : H * .62, sc = Math.min(W, H) * (small ? .3 : .42);
        ctx.clearRect(0, 0, W, H);
        pts.forEach(function (p) {
          p.x += p.vx; p.y += p.vy;
          if (p.x < 0 || p.x > W) p.vx *= -1; if (p.y < 0 || p.y > H) p.vy *= -1;
          if (p.t) { var tx = cx + p.t[0] * sc, ty = cy + p.t[1] * sc; p.x += (tx - p.x) * .03 * phase; p.y += (ty - p.y) * .03 * phase; }
        });
        for (var i = 0; i < pts.length; i++) for (var j = i + 1; j < pts.length; j++) {
          var dx = pts[i].x - pts[j].x, dy = pts[i].y - pts[j].y, d = Math.sqrt(dx * dx + dy * dy);
          if (d < 85) { ctx.strokeStyle = 'rgba(125,211,252,' + (.32 * (1 - d / 85)) + ')'; ctx.lineWidth = 1; ctx.beginPath(); ctx.moveTo(pts[i].x, pts[i].y); ctx.lineTo(pts[j].x, pts[j].y); ctx.stroke(); }
        }
        pts.forEach(function (p) {
          var g = ctx.createRadialGradient(p.x, p.y, 0, p.x, p.y, 5); g.addColorStop(0, 'rgba(186,230,253,.9)'); g.addColorStop(1, 'rgba(56,189,248,0)');
          ctx.fillStyle = g; ctx.beginPath(); ctx.arc(p.x, p.y, 5, 0, 6.283); ctx.fill();
        });
      }
      if (!reduce) requestAnimationFrame(frame);
    }
    requestAnimationFrame(frame);
  }

  // ---------- Start ----------
  document.querySelectorAll('img').forEach(fallback);
  var saved = 'ar';
  try { saved = localStorage.getItem('sd-lang') || 'ar'; } catch (e) {}
  current = saved;
  crystalizeAll();
  renderReviews();
  renderGallery();
  renderTour();
  changeLang(saved);
  initMenu();
  initCards();
  initMobileCta();

  initNetwork();
  serviceCovers();

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
