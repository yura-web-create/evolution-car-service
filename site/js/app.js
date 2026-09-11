(function () {
  'use strict';

  var WA = '79939521826';
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ───────── шапка: приклеивание ───────── */
  var hdr = document.querySelector('.hdr');
  var callbar = document.querySelector('.callbar');
  var lastY = 0, ticking = false;

  function onScroll() {
    var y = window.scrollY || document.documentElement.scrollTop;
    if (hdr) hdr.classList.toggle('is-stuck', y > 12);
    if (callbar) callbar.classList.toggle('is-on', y > 420);
    lastY = y;
    ticking = false;
  }
  window.addEventListener('scroll', function () {
    if (!ticking) { ticking = true; requestAnimationFrame(onScroll); }
  }, { passive: true });
  onScroll();

  /* ───────── мобильное меню ───────── */
  var burger = document.querySelector('.burger');
  if (burger) {
    burger.addEventListener('click', function () {
      var open = document.body.classList.toggle('menu-open');
      burger.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    document.querySelectorAll('.mobmenu a').forEach(function (a) {
      a.addEventListener('click', function () {
        document.body.classList.remove('menu-open');
        burger.setAttribute('aria-expanded', 'false');
      });
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && document.body.classList.contains('menu-open')) {
        document.body.classList.remove('menu-open');
        burger.setAttribute('aria-expanded', 'false');
      }
    });
  }

  /* ───────── заголовок героя по строкам ───────── */
  function splitLines(el) {
    if (!el || reduce) return;
    var words = el.textContent.trim().split(/\s+/);
    var probe = document.createElement('span');
    el.textContent = '';
    words.forEach(function (w, i) {
      var s = document.createElement('span');
      s.className = 'w';
      s.textContent = w + (i < words.length - 1 ? ' ' : '');
      el.appendChild(s);
    });
    var rows = [], cur = null, top = null;
    el.querySelectorAll('.w').forEach(function (w) {
      var t = Math.round(w.offsetTop);
      if (t !== top) { top = t; cur = []; rows.push(cur); }
      cur.push(w.textContent);
    });
    el.textContent = '';
    el.classList.add('lines');
    rows.forEach(function (r, i) {
      var ln = document.createElement('span');
      ln.className = 'ln';
      var inner = document.createElement('span');
      inner.style.setProperty('--i', i);
      inner.textContent = r.join('');
      ln.appendChild(inner);
      el.appendChild(ln);
    });
    probe = null;
    requestAnimationFrame(function () { el.classList.add('is-in'); });
  }
  splitLines(document.querySelector('[data-lines]'));

  /* ───────── появление блоков ───────── */
  var els = document.querySelectorAll('.rv');
  if ('IntersectionObserver' in window && !reduce) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add('is-in'); io.unobserve(e.target); }
      });
    }, { rootMargin: '700px 0px 200px 0px', threshold: 0.01 });
    els.forEach(function (el) { io.observe(el); });
  } else {
    els.forEach(function (el) { el.classList.add('is-in'); });
  }

  /* лесенка внутри сеток */
  document.querySelectorAll('[data-stagger]').forEach(function (wrap) {
    Array.prototype.forEach.call(wrap.children, function (ch, i) {
      ch.style.setProperty('--d', Math.min(i, 5) * 0.035 + 's');
    });
  });

  /* ───────── догрузка остальных фото ─────────
     Отложенная загрузка ждёт, пока картинка подойдёт к экрану. При быстрой прокрутке
     она не успевает, и вместо фотографии видно размытую заглушку. Поэтому, как только
     страница загрузилась, снимаем отложенность со всех оставшихся картинок.
     Приоритет низкий: они не отнимают канал у того, что уже на экране. */
  function preloadRest() {
    var conn = navigator.connection;
    // экономия трафика и очень медленная связь — оставляем как было, по мере прокрутки
    if (conn && (conn.saveData || /(^|-)2g$/.test(conn.effectiveType || ''))) return;
    document.querySelectorAll('img[loading="lazy"]').forEach(function (img) {
      img.fetchPriority = 'low';   // не спорят за канал с тем, что уже на экране
      img.loading = 'eager';
    });
  }
  if (document.readyState === 'complete') preloadRest();
  else window.addEventListener('load', preloadRest);

  /* ───────── счётчики ───────── */
  function animateCount(el) {
    var target = parseFloat(el.dataset.count);
    if (isNaN(target)) return;
    if (reduce) { el.textContent = target; return; }
    var dur = 1100, t0 = null;
    function step(t) {
      if (!t0) t0 = t;
      var p = Math.min((t - t0) / dur, 1);
      var eased = 1 - Math.pow(1 - p, 3);
      el.textContent = Math.round(target * eased);
      if (p < 1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
  }
  var counters = document.querySelectorAll('[data-count]');
  if (counters.length && 'IntersectionObserver' in window) {
    var cio = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { animateCount(e.target); cio.unobserve(e.target); }
      });
    }, { threshold: 0.6 });
    counters.forEach(function (c) { cio.observe(c); });
  } else {
    counters.forEach(function (c) { c.textContent = c.dataset.count; });
  }

  /* ───────── FAQ ───────── */
  document.querySelectorAll('.faq__i').forEach(function (item) {
    var btn = item.querySelector('.faq__q');
    btn.addEventListener('click', function () {
      var open = item.classList.toggle('is-open');
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  });

  /* ───────── бегущая строка: дублируем ряд ───────── */
  document.querySelectorAll('.ticker__row').forEach(function (row) {
    row.innerHTML += row.innerHTML;
  });

  /* ───────── форма записи → WhatsApp ───────── */
  var form = document.getElementById('zapis-form');
  if (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      function v(n) { var f = form.querySelector('[name=' + n + ']'); return f ? f.value.trim() : ''; }
      var lines = ['Здравствуйте! Хочу записаться в Evolution Car Service.'];
      if (v('name')) lines.push('Меня зовут: ' + v('name'));
      if (v('car')) lines.push('Автомобиль: ' + v('car'));
      if (v('task')) lines.push('Задача: ' + v('task'));
      lines.push('Подскажите, пожалуйста, когда можно приехать.');
      window.open('https://wa.me/' + WA + '?text=' + encodeURIComponent(lines.join('\n')), '_blank', 'noopener');
    });
  }

  /* ───────── подсветка за курсором на тёмной плашке ───────── */
  if (!reduce && window.matchMedia('(hover: hover)').matches) {
    document.querySelectorAll('.bigcta').forEach(function (el) {
      el.addEventListener('pointermove', function (e) {
        var r = el.getBoundingClientRect();
        el.style.setProperty('--mx', (e.clientX - r.left) + 'px');
        el.style.setProperty('--my', (e.clientY - r.top) + 'px');
      });
    });

  }

  /* ───────── фотолента: дублируем ряд для бесшовной прокрутки ───────── */
  document.querySelectorAll('.gal__row').forEach(function (row) {
    row.innerHTML += row.innerHTML;
  });

  /* ───────── переход к форме ───────── */
  document.querySelectorAll('a[href="#zapis"]').forEach(function (a) {
    a.addEventListener('click', function (e) {
      var target = document.getElementById('zapis');
      if (!target) return;
      e.preventDefault();
      var top = target.getBoundingClientRect().top + window.pageYOffset - 96;
      window.scrollTo({ top: top, behavior: reduce ? 'auto' : 'smooth' });
      var first = target.querySelector('input');
      if (first) setTimeout(function () { first.focus({ preventScroll: true }); }, reduce ? 0 : 500);
    });
  });
})();
