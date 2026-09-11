#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Сборка статического сайта Evolution Car Service."""

import os, re, json, html

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "site")

# Адрес, под который собирается сайт. По умолчанию — GitHub Pages этого
# репозитория. Под свой домен: SITE_URL=https://example.com python3 pages.py
SITE = os.environ.get("SITE_URL", "https://yura-web-create.github.io/evolution-car-service").rstrip("/")

# Пока сайт живёт на служебном адресе, он закрыт от поисковиков: копия не должна
# конкурировать в выдаче с будущим боевым сайтом. Когда переедет на свой домен —
# открыть индексацию: INDEXABLE=1 python3 pages.py
INDEXABLE = os.environ.get("INDEXABLE") == "1"
ROBOTS = ("index, follow, max-image-preview:large, max-snippet:-1"
          if INDEXABLE else "noindex, nofollow")
PHONE = "+7 993 952-18-26"
PHONE_HREF = "+79939521826"
WA = "79939521826"
WA_URL = "https://wa.me/%s" % WA
ADDRESS = "Новосибирск, Сухарная улица, 35 к13"
STREET = "Сухарная улица, 35 к13"
CITY = "Новосибирск"
HOURS = "Уточняйте по телефону"
YEAR = 2026
MAPS = "https://yandex.ru/maps/?text=" + ADDRESS.replace(" ", "%20").replace(",", "%2C")

with open(os.path.join(ROOT, "imgdims.json"), encoding="utf-8") as f:
    DIMS = json.load(f)

# ─────────────────────────────────────────────── иконки

ICON = {
    "to": '<path d="M14.7 6.3a4 4 0 0 1-5.4 5.4L4 17v3h3l5.3-5.3a4 4 0 0 1 5.4-5.4l-2.3 2.3 1.6 1.6 2.3-2.3a4 4 0 0 1-4.6-4.6z"/>',
    "diag": '<path d="M3 12h3l2-5 4 12 2.5-7H21"/>',
    "susp": '<path d="M12 3v3M12 18v3M8 6h8M8 18h8M9 6c0 2 6 2 6 4s-6 2-6 4 6 2 6 4"/>',
    "brake": '<circle cx="12" cy="12" r="8"/><circle cx="12" cy="12" r="3"/><path d="M12 4v3M20 12h-3M12 20v-3M4 12h3"/>',
    "elec": '<rect x="7" y="7" width="10" height="10" rx="2"/><path d="M10 3v4M14 3v4M10 17v4M14 17v4M3 10h4M3 14h4M17 10h4M17 14h4"/>',
    "soft": '<path d="M8 8l-4 4 4 4M16 8l4 4-4 4M13.5 5l-3 14"/>',
    "rus": '<path d="M4 5h9M8.5 5v3c0 4-1.8 7-4.5 9M7 13c1.6 3 3.9 4.7 6 5.4M13 20l4-11 4 11M14.6 16.5h4.8"/>',
    "parts": '<path d="M21 8l-9-5-9 5 9 5 9-5z"/><path d="M3 12l9 5 9-5M3 16l9 5 9-5"/>',
    "shield": '<path d="M12 3l8 3v6c0 5-3.4 8.4-8 9.5C7.4 20.4 4 17 4 12V6l8-3z"/><path d="M9 12l2 2 4-4"/>',
    "car": '<path d="M5 16h14M6.5 16v2H4v-2M20 18h-2.5v-2"/><path d="M4 16l1.6-5.2A2 2 0 0 1 7.5 9.4h9a2 2 0 0 1 1.9 1.4L20 16z"/><circle cx="7.5" cy="16" r="1.4"/><circle cx="16.5" cy="16" r="1.4"/>',
    "chat": '<path d="M21 12a8 8 0 0 1-11.6 7.1L4 20.5l1.4-5.2A8 8 0 1 1 21 12z"/>',
}


def svg(name):
    return ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" '
            'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">%s</svg>' % ICON[name])


ARROW = ('<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.8" '
         'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
         '<path d="M2.5 8h11M9 3.5L13.5 8 9 12.5"/></svg>')

# ─────────────────────────────────────────────── данные

SERVICES = [
    ("to", "tehnicheskoe-obsluzhivanie.html", "Техническое обслуживание",
     "Плановое ТО с заменой необходимых расходных материалов и проверкой состояния автомобиля.", "oil-change"),
    ("diag", "diagnostika.html", "Компьютерная диагностика",
     "Проверяем не только наличие ошибок, но и причину их появления.", "diag-laptop"),
    ("susp", "podveska.html", "Подвеска и ходовая",
     "Диагностика и ремонт элементов подвески и ходовой части.", "suspension"),
    ("brake", "tormoznaya-sistema.html", "Тормозная система",
     "Обслуживание и ремонт тормозов, замена колодок, дисков и других элементов.", "brake-disc"),
    ("elec", "elektronika.html", "Электроника автомобиля",
     "Диагностика электронных систем, блоков и связанных между собой компонентов.", "engine-bay"),
    ("soft", "programmnye-raboty.html", "Программные работы",
     "Работа с доступными программными функциями: обновления, настройки, интернет, приложения.", "dash-screen"),
    ("rus", "rusifikaciya.html", "Русификация",
     "Адаптация интерфейса автомобиля для поддерживаемых марок и версий ПО.", "dash-night"),
    ("parts", "zapchasti.html", "Запчасти",
     "Подбор и поставка деталей и расходных материалов для обслуживания и ремонта.", "coilovers"),
]

BRANDS = [
    ("Li Auto", "L6, L7, L8, L9 и другие поддерживаемые версии.", "li-auto.html"),
    ("ZEEKR", "Диагностика, обслуживание, механические и программные работы.", "zeekr.html"),
    ("VOYAH", "Обслуживание электрических и гибридных моделей.", "voyah.html"),
    ("BYD", "Диагностика и обслуживание электрических и гибридных автомобилей.", "byd.html"),
    ("AVATR", "Диагностика, техническое обслуживание и доступные программные работы.", "avatr.html"),
]

NAV = [
    ("uslugi.html", "Услуги"),
    ("marki.html", "Марки"),
    ("ceny.html", "Цены"),
    ("praktika.html", "Кейсы"),
    ("garantiya.html", "Гарантия"),
    ("o-servise.html", "О сервисе"),
    ("kontakty.html", "Контакты"),
]

TICKER = ["Li Auto", "ZEEKR", "VOYAH", "BYD", "AVATR", "Техническое обслуживание", "Диагностика",
          "Подвеска и ходовая", "Тормозная система", "Электроника", "Программные работы",
          "Русификация", "Запчасти", "Гибриды", "Электромобили"]

# ─────────────────────────────────────────────── утилиты


SHORT = re.compile(r"(?<![^\s(«\u2014-])([А-Яа-яЁёA-Za-z]{1,2}|\d{1,4})\s+(?=[^\s])")


def typo(t):
    """Короткие слова не должны висеть в конце строки."""
    for _ in range(3):
        t = SHORT.sub("\\1\u00a0", t)
    t = t.replace(" — ", "\u00a0— ").replace(" – ", "\u00a0– ")
    return t


def esc_plain(t):
    return html.escape(str(t), quote=False)


def esc(t):
    return typo(html.escape(str(t), quote=False))


def attr(t):
    return html.escape(str(t), quote=True)


def rich(t):
    t = esc(t)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    return t.replace("->", "→")


VARIANTS = {
    # набор -> (ширины, соотношение сторон исходника)
    "box": ((640, 1000, 1600), (4, 3)),      # герой и блоки со сплитом
    "card": ((640, 1000), (16, 10)),          # карточки услуг и кейсов
}


# Первые кадры страницы грузятся сразу: при быстрой прокрутке отложенная загрузка
# не успевает, и человек видит размытую заглушку вместо фотографии.
EAGER_FIRST = 6
_img_n = [0]


def picture(name, alt, cls="", sizes="100vw", eager=False, variant="box"):
    """AVIF + WebP под нужное соотношение сторон. Пока грузится — размытая заглушка."""
    _img_n[0] += 1
    early = eager or _img_n[0] <= EAGER_FIRST
    widths, (rw, rh) = VARIANTS[variant]
    w = widths[-1]
    h = round(w * rh / rw)

    def ss(ext):
        return ", ".join("img/%s-%s-%d.%s %dw" % (name, variant, x, ext, x) for x in widths)

    wrap = "%s lqip ph-%s" % (cls, name)
    return ('<div class="%s"><picture>'
            '<source type="image/avif" srcset="%s" sizes="%s">'
            '<source type="image/webp" srcset="%s" sizes="%s">'
            '<img src="img/%s-%s-%d.webp" width="%d" height="%d" alt="%s" decoding="async"%s>'
            '</picture></div>'
            % (wrap,
               ss("avif"), sizes, ss("webp"), sizes,
               name, variant, w, w, h, attr(alt),
               ' fetchpriority="high"' if eager else ('' if early else ' loading="lazy"')))


def buttons(items, big=False):
    out = []
    for it in items:
        kind = it.get("kind", "dark")
        size = " btn--lg" if big else ""
        ico = '<span class="btn__ico">%s</span>' % ARROW if it.get("arrow", True) else ""
        ext = ' target="_blank" rel="noopener"' if it["href"].startswith("http") else ""
        out.append('<a class="btn btn--%s%s" href="%s"%s>%s%s</a>'
                   % (kind, size, it["href"], ext, esc_plain(it["text"]), ico))
    return "".join(out)


def head_block(d):
    out = ""
    if d.get("eyebrow"):
        out += '<p class="eyebrow">%s</p>' % esc(d["eyebrow"])
    if d.get("title"):
        out += "<h2>%s</h2>" % rich(d["title"])
    if d.get("lead"):
        out += "".join('<p class="lead">%s</p>' % rich(p) for p in d["lead"])
    if not out:
        return ""
    cls = ""
    if d.get("wide"):
        cls += " sec-head--wide"
    lvl = d.get("_level")
    if lvl:
        cls += " sec-head--" + lvl
    return '<div class="sec-head%s rv">%s</div>' % (cls, out)


def foot_block(d):
    if not d.get("foot"):
        return ""
    return '<div class="btn-row sec-foot rv">%s</div>' % buttons(d["foot"])


# ─────────────────────────────────────────────── блоки


def b_hero(d):
    crumbs = ""
    if d.get("crumbs"):
        items = ['<a href="index.html">Главная</a><span>/</span>']
        for c in d["crumbs"][:-1]:
            items.append('<a href="%s">%s</a><span>/</span>' % (c[1], esc(c[0])))
        items.append("<span>%s</span>" % esc(d["crumbs"][-1][0]))
        crumbs = '<nav class="crumbs" aria-label="Навигационная цепочка">%s</nav>' % "".join(items)

    leads = "".join('<p class="hero__lead">%s</p>' % rich(p) for p in d.get("lead", []))
    chips = ""
    if d.get("chips", True):
        chips = '<div class="hero__facts">%s</div>' % "".join(
            '<a class="chip" href="%s">%s</a>' % (b[2], esc_plain(b[0])) for b in BRANDS)
    ctas = '<div class="btn-row hero__cta">%s</div>' % buttons(d["cta"], big=True) if d.get("cta") else ""
    media = picture(d["img"], d.get("alt", "Evolution Car Service, Новосибирск"), cls="hero__media",
                    sizes="(max-width: 900px) 100vw, 46vw", eager=True)
    ticker = ""
    if d.get("ticker", not d.get("sub")):
        row = "".join('<span class="ticker__i">%s</span>' % esc(t) for t in TICKER)
        ticker = '<div class="ticker" aria-hidden="true"><div class="ticker__row">%s</div></div>' % row
    return f"""<section class="hero{' hero--sub' if d.get('sub') else ''}">
  <div class="container hero__in">
    <div class="hero__copy">
      {crumbs}
      <h1 data-lines>{esc(d['title'])}</h1>
      {leads}
      {ctas}
      {chips}
    </div>
    {media}
  </div>
  {ticker}
</section>"""


def b_cards(d):
    cards = []
    for it in d["items"]:
        ico = '<div class="card__ico">%s</div>' % svg(it["icon"]) if it.get("icon") else ""
        txt = "".join("<p>%s</p>" % rich(p) for p in it.get("text", []))
        if it.get("href"):
            more = '<span class="card__more">%s %s</span>' % (esc(it.get("more", "Подробнее")), ARROW)
            cards.append('<a class="card rv" href="%s">%s<h3>%s</h3>%s%s</a>'
                         % (it["href"], ico, esc(it["title"]), txt, more))
        else:
            cards.append('<div class="card card--hover rv">%s<h3>%s</h3>%s</div>'
                         % (ico, esc(it["title"]), txt))
    return '%s<div class="grid grid--%d" data-stagger>%s</div>%s' % (
        head_block(d), d.get("cols", 3), "".join(cards), foot_block(d))


def b_svc(d):
    """feat=N — первые N услуг занимают по половине ряда: в сетке появляется главное."""
    cards = []
    feat = d.get("feat", 0)
    for i, (key, href, name, txt, img) in enumerate(d["items"], 1):
        big = i <= feat
        pic = picture(img, name + " — Evolution Car Service", cls="svc__img", variant="card",
                      sizes="(max-width: 640px) 100vw, (max-width: 1140px) 50vw, %s" % ("46vw" if big else "24vw"))
        cards.append(f"""<a class="svc rv{' svc--feat' if big else ''}" href="{href}">{pic}<span class="svc__n">{i:02d}</span>
  <div class="svc__body"><h3>{esc(name)}</h3><p>{esc(txt)}</p>
    <span class="svc__more">Подробнее {ARROW}</span></div></a>""")
    if d.get("tail"):
        cards.append(
            '<a class="svc svc--tail rv" href="%s" target="_blank" rel="noopener">'
            '<div class="svc__body"><div class="card__ico">%s</div>'
            '<h3>Другая задача</h3>'
            '<p>Не нашли нужную работу? Напишите марку, модель и что требуется — '
            'подскажем, можем ли выполнить это в сервисе.</p>'
            '<span class="svc__more">Написать нам %s</span></div></a>' % (WA_URL, svg("chat"), ARROW))
    grid = "grid grid--feat" if feat else "grid grid--%d" % d.get("cols", 4)
    return '%s<div class="%s" data-stagger>%s</div>%s' % (
        head_block(d), grid, "".join(cards), foot_block(d))


def b_gallery(d):
    row = "".join(
        '<div class="gal__i lqip ph-%s"><picture>'
        '<source type="image/avif" srcset="img/%s-card-640.avif">'
        '<source type="image/webp" srcset="img/%s-card-640.webp">'
        '<img src="img/%s-card-640.webp" width="640" height="400" alt="%s" loading="lazy" decoding="async">'
        '</picture></div>' % (n, n, n, n, attr(alt)) for n, alt in d["items"])
    return ('%s<div class="gal rv"><div class="gal__row">%s</div></div>%s'
            % (head_block(d), row, foot_block(d)))


SHOWCASE = [
    ("Двигатель и техническое обслуживание",
     "Масло, фильтры, технические жидкости, регламент по пробегу",
     "tehnicheskoe-obsluzhivanie.html"),
    ("Мультимедиа и программная часть",
     "Русификация, интернет, приложения, обновления системы",
     "programmnye-raboty.html"),
    ("Электроника автомобиля",
     "Блоки управления, датчики, проводка, питание, поиск причины",
     "elektronika.html"),
    ("Подвеска и ходовая часть",
     "Амортизаторы, рычаги, сайлентблоки, шаровые, ступичные узлы",
     "podveska.html"),
    ("Тормозная система",
     "Колодки, диски, суппорты, тормозная жидкость, датчики",
     "tormoznaya-sistema.html"),
]


def b_showcase(d):
    items = "".join(
        '<a class="shl__i" href="%s"><span class="shl__n">%02d</span>'
        '<span class="shl__b"><span class="shl__t">%s</span>'
        '<span class="shl__s">%s</span></span>%s</a>'
        % (href, i, esc_plain(name), esc(sub), ARROW)
        for i, (name, sub, href) in enumerate(d.get("items", SHOWCASE), 1))
    cta = ""
    if d.get("cta"):
        cta = '<div class="btn-row shl__cta">%s</div>' % buttons(d["cta"])
    pic = picture(d.get("img", "byd-seal"), d.get("alt", "Автомобиль в сервисе"),
                  cls="shw__pic", sizes="(max-width: 900px) 100vw, 50vw")
    return ('%s<div class="shw rv">%s<div class="shl">%s%s</div></div>%s'
            % (head_block(d), pic, items, cta, foot_block(d)))


def b_photocards(d):
    cards = []
    for it in d["items"]:
        pic = picture(it["img"], it.get("alt", it["title"]), cls="svc__img", variant="card",
                      sizes="(max-width: 640px) 100vw, (max-width: 1140px) 50vw, 32vw")
        body = "".join("<p>%s</p>" % rich(t) for t in it.get("text", []))
        more = ('<span class="svc__more">%s %s</span>' % (esc_plain(it.get("more", "Подробнее")), ARROW)
                if it.get("href") else "")
        tag = "a" if it.get("href") else "div"
        href = ' href="%s"' % it["href"] if it.get("href") else ""
        cards.append('<%s class="svc rv"%s>%s<div class="svc__body"><h3>%s</h3>%s%s</div></%s>'
                     % (tag, href, pic, esc(it["title"]), body, more, tag))
    return '%s<div class="grid grid--%d" data-stagger>%s</div>%s' % (
        head_block(d), d.get("cols", 3), "".join(cards), foot_block(d))


def b_split(d):
    body = head_block({k: v for k, v in d.items() if k in ("eyebrow", "title", "lead", "_level")})
    inner = ""
    if d.get("ticks"):
        inner += '<ul class="ticks%s">%s</ul>' % (" ticks--2" if d.get("two") else "",
                                                  "".join("<li>%s</li>" % rich(x) for x in d["ticks"]))
    if d.get("dots"):
        inner += '<ul class="dots%s">%s</ul>' % (" dots--2" if d.get("two") else "",
                                                 "".join("<li>%s</li>" % rich(x) for x in d["dots"]))
    if d.get("after"):
        inner += "".join('<p class="lead" style="margin-top:22px">%s</p>' % rich(p) for p in d["after"])
    if d.get("cta"):
        inner += '<div class="btn-row" style="margin-top:30px">%s</div>' % buttons(d["cta"])
    if inner:
        body += '<div class="rv">%s</div>' % inner
    media = picture(d["img"], d.get("alt", ""), cls="split__media",
                    sizes="(max-width: 900px) 100vw, 46vw")
    return '<div class="split%s"><div class="split__body">%s</div>%s</div>' % (
        " split--rev" if d.get("rev") else "", body, media)


def b_steps(d):
    st = []
    for i, it in enumerate(d["items"], 1):
        p = "<p>%s</p>" % rich(it[1]) if len(it) > 1 and it[1] else ""
        st.append('<div class="step rv"><span class="step__n">%02d</span><h3>%s</h3>%s</div>'
                  % (i, esc(it[0]), p))
    cols = d.get("cols", 4)
    # если в последнем ряду не хватает одной ячейки — растягиваем последний шаг
    fill = " steps--fill" if len(d["items"]) % cols == cols - 1 else ""
    return '%s<div class="steps steps--line steps--c%d%s" data-stagger>%s</div>%s' % (
        head_block(d), cols, fill, "".join(st), foot_block(d))


def b_flow(d):
    n = len(d["items"])
    items = ""
    for i, x in enumerate(d["items"], 1):
        items += '<div class="flow__i rv"><b>%02d</b><span>%s</span></div>' % (i, esc(x))
        if i < n:
            items += ('<span class="flow__arrow" aria-hidden="true">'
                      '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.6" '
                      'stroke-linecap="round" stroke-linejoin="round">'
                      '<path d="M3 8h10M9.5 4.5 13 8l-3.5 3.5"/></svg></span>')
    return '%s<div class="flow" data-stagger>%s</div>%s' % (head_block(d), items, foot_block(d))


def b_brands(d):
    items = [b for b in BRANDS if b[2] != d.get("exclude")]
    cards = "".join(
        '<a class="brand rv" href="%s"><span class="brand__name">%s</span><p>%s</p>'
        '<span class="brand__more">Сервис %s %s</span></a>' % (href, esc_plain(n), esc(t), esc_plain(n), ARROW)
        for n, t, href in items)
    return '%s<div class="brands brands--%d" data-stagger>%s</div>%s' % (
        head_block(d), len(items), cards, foot_block(d))


def b_cases(d):
    cards = []
    for it in d["items"]:
        steps = "".join('<li><b>%s</b><span>%s</span></li>' % (esc(a), esc(b)) for a, b in it["steps"])
        pic = picture(it["img"], it["title"], cls="case__img", variant="card",
                      sizes="(max-width: 640px) 100vw, (max-width: 1140px) 50vw, 24vw")
        cards.append(f"""<article class="case rv">{pic}<span class="case__tag">{esc(it['tag'])}</span>
  <div class="case__body"><h3>{esc(it['title'])}</h3><ul class="case__steps">{steps}</ul></div></article>""")
    return '%s<div class="grid grid--%d" data-stagger>%s</div>%s' % (
        head_block(d), d.get("cols", 4), "".join(cards), foot_block(d))


def b_reviews(d):
    cards = "".join(f"""<article class="review rv">
  <div class="review__head"><span class="review__car">{esc(it['car'])}</span><span class="review__stars" aria-label="Оценка 5 из 5">★★★★★</span></div>
  <div class="review__task">{esc(it['task'])}</div><p>{esc(it['text'])}</p>
  <div class="review__src">{esc(it['src'])}</div></article>""" for it in d["items"])
    return '%s<div class="grid grid--%d" data-stagger>%s</div>' % (head_block(d), d.get("cols", 3), cards)


def b_panel(d):
    inner = ""
    if d.get("eyebrow"):
        inner += '<p class="eyebrow">%s</p>' % esc(d["eyebrow"])
    if d.get("title"):
        lvl = ' class="h-%s"' % d["_level"] if d.get("_level") else ""
        inner += "<h2%s>%s</h2>" % (lvl, rich(d["title"]))
    if d.get("lead"):
        inner += "".join('<p class="lead" style="margin-top:18px">%s</p>' % rich(p) for p in d["lead"])
    if d.get("ticks"):
        inner += '<ul class="ticks ticks--2">%s</ul>' % "".join("<li>%s</li>" % rich(x) for x in d["ticks"])
    if d.get("dots"):
        inner += '<ul class="dots dots--2">%s</ul>' % "".join("<li>%s</li>" % rich(x) for x in d["dots"])
    if d.get("html"):
        inner += d["html"]
    if d.get("cta"):
        inner += '<div class="btn-row" style="margin-top:30px">%s</div>' % buttons(d["cta"])
    return '<div class="panel rv">%s</div>' % inner


def b_cta(d):
    body = "<h2>%s</h2>" % rich(d["title"])
    body += "".join("<p>%s</p>" % rich(p) for p in d.get("lead", []))
    body += '<div class="btn-row">%s</div>' % buttons(d["cta"], big=True)
    return '<div class="bigcta rv">%s</div>' % body


def b_stats(d):
    cells = "".join('<div class="stat rv"><div class="stat__v">%s</div><div class="stat__l">%s</div></div>'
                    % (v, esc(l)) for v, l in d["items"])
    return '<div class="stats" data-stagger>%s</div>' % cells


def b_faq(d):
    items = "".join(f"""<div class="faq__i">
  <button class="faq__q" type="button" aria-expanded="false">{esc(q)}</button>
  <div class="faq__a"><div><p>{rich(a)}</p></div></div></div>""" for q, a in d["items"])
    aside = f"""<aside class="faq__side rv" style="--d:.1s">
  <div class="faq__ico">{svg("chat")}</div>
  <h3>Не нашли свой вопрос?</h3>
  <p class="lead">Напишите марку, модель и что беспокоит — ответим и подскажем,
    с чего начать и сколько это займёт.</p>
  <div class="btn-row" style="margin-top:24px">
    <a class="btn btn--dark" href="{WA_URL}" target="_blank" rel="noopener">Спросить в WhatsApp<span class="btn__ico">{ARROW}</span></a>
  </div>
  <a class="faq__tel" href="tel:{PHONE_HREF}">{PHONE}</a>
</aside>"""
    return '%s<div class="faqwrap"><div class="faq rv">%s</div>%s</div>' % (head_block(d), items, aside)


def b_form(d):
    return f"""{head_block(d)}
<div class="formwrap">
  <form class="form rv" id="zapis-form">
    <div class="field"><label for="f-name">Как к вам обращаться</label>
      <input id="f-name" name="name" type="text" placeholder="Имя" autocomplete="name"></div>
    <div class="field"><label for="f-car">Марка и модель автомобиля</label>
      <input id="f-car" name="car" type="text" placeholder="Например: Li Auto L7, 2023"></div>
    <div class="field"><label for="f-task">Что нужно сделать или что беспокоит</label>
      <textarea id="f-task" name="task" placeholder="Опишите симптомы, ошибку на панели или нужную работу"></textarea></div>
    <div class="btn-row" style="margin-top:6px">
      <button class="btn btn--wa" type="submit">Отправить в WhatsApp<span class="btn__ico">{ARROW}</span></button>
      <a class="btn btn--light" href="tel:{PHONE_HREF}">Позвонить {PHONE}</a>
    </div>
    <p class="form__note">Кнопка откроет WhatsApp с уже готовым сообщением — останется только отправить.
      Данные никуда не сохраняются.</p>
  </form>
  <div class="panel rv" style="--d:.1s">
    <h3>Что указать в сообщении</h3>
    <ul class="ticks">
      <li>марку и модель автомобиля</li>
      <li>год выпуска, если знаете</li>
      <li>что нужно сделать или что беспокоит</li>
      <li>ошибку на панели, звук или изменение в работе</li>
      <li>удобное время для визита</li>
    </ul>
    <p class="lead" style="margin-top:24px;font-size:15px">Если точная причина неисправности неизвестна —
      достаточно описать, что происходит с автомобилем. Подскажем, с чего начать: с осмотра, диагностики
      или конкретной сервисной работы.</p>
  </div>
</div>"""


def b_price(d):
    rows = []
    for it in d["items"]:
        href = it.get("href")
        name = ('<a href="%s">%s %s</a>' % (href, esc(it["name"]), ARROW)) if href else esc(it["name"])
        rows.append('<div class="prow rv"><div class="prow__n">%s</div>'
                    '<div class="prow__d">%s</div><div class="prow__p">%s</div></div>'
                    % (name, esc(it["text"]), esc(it["price"])))
    note = '<p class="lead price-note rv">%s</p>' % rich(d["note"]) if d.get("note") else ""
    return '%s<div class="ptable">%s</div>%s%s' % (head_block(d), "".join(rows), note, foot_block(d))


def b_map(d):
    q = "Новосибирск, Сухарная улица, 35к13".replace(" ", "%20").replace(",", "%2C")
    return (f'{head_block(d)}<div class="map rv">'
            f'<iframe src="https://yandex.ru/map-widget/v1/?text={q}&z=17" '
            f'title="Evolution Car Service на карте Новосибирска" loading="lazy" allowfullscreen></iframe></div>')


def b_html(d):
    return d["html"]


RENDER = {"price": b_price, "cards": b_cards, "showcase": b_showcase, "photocards": b_photocards, "gallery": b_gallery, "svc": b_svc, "split": b_split, "steps": b_steps, "flow": b_flow,
          "brands": b_brands, "cases": b_cases, "reviews": b_reviews, "panel": b_panel,
          "cta": b_cta, "stats": b_stats, "faq": b_faq, "form": b_form, "map": b_map, "html": b_html}


# служебные блоки не спорят с главами за внимание
COMPACT_HEAD = {"cta", "form", "map", "stats", "flow", "html"}


def render_sections(blocks):
    """Задаёт странице три уровня: опорная глава, обычная секция, служебный блок."""
    lead_done = False
    for b in blocks:
        if b["type"] in COMPACT_HEAD:
            b["_level"] = "compact"
        elif not lead_done and b.get("title"):
            b["_level"] = "major"
            b["major"] = True
            lead_done = True

    out = []
    for b in blocks:
        cls = "section"
        for k in ("soft", "tint", "dark"):
            if b.get(k):
                cls += " section--" + k
        if b.get("major"):
            cls += " section--major"
        if b.get("tight"):
            cls += " section--tight"
        sid = ' id="%s"' % b["id"] if b.get("id") else ""
        out.append('<section class="%s"%s><div class="container">%s</div></section>'
                   % (cls, sid, RENDER[b["type"]](b)))
    return "\n".join(out)


# ─────────────────────────────────────────────── каркас


def header(active):
    nav = "".join('<a href="%s"%s>%s</a>' % (h, ' class="is-active" aria-current="page"' if h == active else "", esc_plain(t))
                  for h, t in NAV)
    mob = "".join('<a class="mm" href="%s" style="--i:%d">%s</a>' % (h, i, esc(t))
                  for i, (h, t) in enumerate(NAV))
    return f"""<header class="hdr">
  <div class="container hdr__in">
    <a class="logo" href="index.html" aria-label="Evolution Car Service — на главную">
      <span class="logo__mark" aria-hidden="true">E</span>
      <span class="logo__txt"><span class="logo__name">Evolution</span><span class="logo__sub">Car Service</span></span>
    </a>
    <nav class="nav" aria-label="Основное меню">{nav}</nav>
    <div class="hdr__act">
      <a class="hdr__tel" href="tel:{PHONE_HREF}">{PHONE}</a>
      <a class="btn btn--dark btn--sm" href="#zapis">Записаться<span class="btn__ico">{ARROW}</span></a>
    </div>
    <button class="burger" type="button" aria-label="Открыть меню" aria-expanded="false"><span></span></button>
  </div>
</header>
<div class="mobmenu">{mob}
  <div class="mobmenu__foot">
    <a class="btn btn--dark btn--lg" href="tel:{PHONE_HREF}">Позвонить {PHONE}</a>
    <a class="btn btn--light btn--lg" href="{WA_URL}" target="_blank" rel="noopener">Написать в WhatsApp</a>
  </div>
</div>"""


def footer():
    su = "".join('<li><a href="%s">%s</a></li>' % (s[1], esc_plain(s[2])) for s in SERVICES)
    co = "".join('<li><a href="%s">%s</a></li>' % (h, esc_plain(t)) for h, t in NAV)
    brands = "".join('<li><a href="%s">Сервис %s</a></li>' % (b[2], esc_plain(b[0])) for b in BRANDS)
    co += '<li><a href="zapchasti.html">Запчасти</a></li>' 
    return f"""<footer class="footer">
  <div class="container">
    <div class="footer__top">
      <div>
        <a class="logo" href="index.html">
          <span class="logo__mark" aria-hidden="true">E</span>
          <span class="logo__txt"><span class="logo__name">Evolution</span><span class="logo__sub">Car Service</span></span>
        </a>
        <p class="footer__about">Технический сервис современных автомобилей в Новосибирске: автомобили с двигателем,
          гибриды и электромобили. Отдельное направление — Li&nbsp;Auto, ZEEKR, VOYAH, BYD и AVATR.</p>
      </div>
      <div><h4>Услуги</h4><ul>{su}</ul></div>
      <div><h4>Марки</h4><ul>{brands}</ul></div>
      <div><h4>Сервис</h4><ul>{co}</ul></div>
      <div>
        <h4>Контакты</h4>
        <ul>
          <li><a href="{MAPS}" target="_blank" rel="noopener">{ADDRESS}</a></li>
          <li><a href="tel:{PHONE_HREF}">{PHONE}</a></li>
          <li><a href="{WA_URL}" target="_blank" rel="noopener">WhatsApp</a></li>
          <li><span>Режим работы: {HOURS}</span></li>
        </ul>
      </div>
    </div>
    <div class="footer__bottom">
      <span>© {YEAR} Evolution Car Service, Новосибирск</span>
      <span>Информация на сайте не является публичной офертой</span>
    </div>
  </div>
</footer>
<div class="callbar">
  <a class="btn btn--dark" href="tel:{PHONE_HREF}">Позвонить</a>
  <a class="btn btn--wa" href="{WA_URL}" target="_blank" rel="noopener">WhatsApp</a>
</div>"""


# ─────────────────────────────────────────────── микроразметка

BIZ = {
    "@type": "AutoRepair",
    "@id": SITE + "/#org",
    "name": "Evolution Car Service",
    "url": SITE + "/",
    "telephone": PHONE_HREF,
    "image": SITE + "/img/og.jpg",
    "description": "Технический сервис современных автомобилей в Новосибирске: техническое обслуживание, "
                   "компьютерная диагностика, подвеска и ходовая, тормозная система, электроника, "
                   "программные работы, русификация и запчасти. Li Auto, ZEEKR, VOYAH, BYD, AVATR.",
    "address": {"@type": "PostalAddress", "streetAddress": STREET, "addressLocality": CITY,
                "addressRegion": "Новосибирская область", "addressCountry": "RU"},
    "areaServed": {"@type": "City", "name": CITY},
    "priceRange": "₽₽",
    "currenciesAccepted": "RUB",
    "makesOffer": [{"@type": "Offer", "itemOffered": {"@type": "Service", "name": s[2]}} for s in SERVICES],
    "brand": [{"@type": "Brand", "name": b[0]} for b in BRANDS],
}


def ld_json(slug, title, desc, blocks, crumbs=None, service=None):
    url = "%s/%s" % (SITE, "" if slug == "index.html" else slug)
    graph = [BIZ,
             {"@type": "WebSite", "@id": SITE + "/#site", "url": SITE + "/",
              "name": "Evolution Car Service", "inLanguage": "ru-RU",
              "publisher": {"@id": SITE + "/#org"}},
             {"@type": "WebPage", "@id": url + "#page", "url": url, "name": title, "description": desc,
              "isPartOf": {"@id": SITE + "/#site"}, "inLanguage": "ru-RU"}]

    if crumbs:
        items = [{"@type": "ListItem", "position": 1, "name": "Главная", "item": SITE + "/"}]
        for i, (name, href) in enumerate(crumbs, 2):
            it = {"@type": "ListItem", "position": i, "name": name}
            if href and href != "#":
                it["item"] = "%s/%s" % (SITE, href)
            items.append(it)
        graph.append({"@type": "BreadcrumbList", "itemListElement": items})

    faq = [b for b in blocks if b.get("type") == "faq"]
    if faq:
        graph.append({"@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q,
             "acceptedAnswer": {"@type": "Answer", "text": a.replace("**", "")}}
            for q, a in faq[0]["items"]]})

    if service:
        graph.append({"@type": "Service", "name": service, "serviceType": service,
                      "provider": {"@id": SITE + "/#org"},
                      "areaServed": {"@type": "City", "name": CITY}})

    return json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False)


# ─────────────────────────────────────────────── страница


def page(slug, title, desc, hero, blocks, active=None, service=None):
    _img_n[0] = 0
    url = "%s/%s" % (SITE, "" if slug == "index.html" else slug)
    ld = ld_json(slug, title, desc, blocks, hero.get("crumbs"), service)
    hi = hero["img"]
    doc = f"""<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc_plain(title)}</title>
<meta name="description" content="{attr(desc)}">
<link rel="canonical" href="{url}">
<meta name="robots" content="{ROBOTS}">
<meta name="geo.region" content="RU-NVS">
<meta name="geo.placename" content="Новосибирск">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Evolution Car Service">
<meta property="og:locale" content="ru_RU">
<meta property="og:title" content="{attr(title)}">
<meta property="og:description" content="{attr(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/img/og.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{attr(title)}">
<meta name="twitter:description" content="{attr(desc)}">
<meta name="twitter:image" content="{SITE}/img/og.jpg">
<meta name="theme-color" content="#ffffff">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="favicon.svg">
<link rel="preload" href="fonts/inter-cyrillic-wght-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" as="image" type="image/avif" imagesrcset="img/{hi}-box-640.avif 640w, img/{hi}-box-1000.avif 1000w, img/{hi}-box-1600.avif 1600w" imagesizes="(max-width: 900px) 100vw, 46vw" fetchpriority="high">
<script>document.documentElement.classList.add('js')</script>
<link rel="stylesheet" href="css/style.css">
<script type="application/ld+json">{ld}</script>
</head>
<body>
{header(active or slug)}
<main>
{b_hero(hero)}
{render_sections(blocks)}
</main>
{footer()}
<script src="js/app.js" defer></script>
</body>
</html>"""
    with open(os.path.join(OUT, slug), "w", encoding="utf-8") as f:
        f.write(doc)


# ─────────────────────────────────────────────── переиспользуемые блоки


def svc_cards(exclude=None, cols=4, eyebrow="Услуги", title=None, lead=None, foot=None, **kw):
    items = [s for s in SERVICES if s[1] != exclude]
    d = {"type": "svc", "items": items, "cols": cols, "eyebrow": eyebrow,
         "tail": exclude is not None and len(items) % cols != 0}
    if title:
        d["title"] = title
    if lead:
        d["lead"] = lead
    if foot:
        d["foot"] = foot
    d.update(kw)
    return d


def final_cta(title, lead, primary="Записаться в сервис", **kw):
    d = {"type": "cta", "title": title, "lead": lead, "cta": [
        {"text": primary, "href": "#zapis"},
        {"text": "Написать в WhatsApp", "href": WA_URL, "kind": "ghost"}]}
    d.update(kw)
    return d


def form_block(title="Запись в Evolution Car Service", eyebrow="Запись",
               lead=("Напишите марку, модель и что нужно сделать. Ответим и подскажем, с чего начать.",), **kw):
    d = {"type": "form", "id": "zapis", "eyebrow": eyebrow, "title": title, "lead": list(lead), "soft": True}
    d.update(kw)
    return d


def contacts_block():
    pic = picture("workshop", "Рабочая зона Evolution Car Service в Новосибирске",
                  cls="split__media", sizes="(max-width: 900px) 100vw, 46vw")
    return [{"type": "html", "id": "kontakty", "html": f"""
<div class="sec-head rv"><p class="eyebrow">Контакты</p><h2>Evolution Car Service в Новосибирске</h2></div>
<div class="split">
  <div class="split__body">
    <dl class="contact-list rv">
      <div class="contact-row"><dt>Адрес</dt><dd>{ADDRESS}<small>Заезд на территорию сервиса — по указателям</small></dd></div>
      <div class="contact-row"><dt>Телефон</dt><dd><a href="tel:{PHONE_HREF}">{PHONE}</a></dd></div>
      <div class="contact-row"><dt>WhatsApp</dt><dd><a href="{WA_URL}" target="_blank" rel="noopener">Написать в WhatsApp</a></dd></div>
      <div class="contact-row"><dt>Режим работы</dt><dd>{HOURS}</dd></div>
    </dl>
    <div class="btn-row rv" style="margin-top:30px">
      <a class="btn btn--dark" href="#zapis">Записаться в сервис<span class="btn__ico">{ARROW}</span></a>
      <a class="btn btn--light" href="{MAPS}" target="_blank" rel="noopener">Открыть в Яндекс Картах</a>
    </div>
    <p class="lead rv" style="margin-top:26px;font-size:15px">Перед визитом лучше записаться: так подготовим
      место на посту и заранее проверим, какие расходники понадобятся для вашей модели.</p>
  </div>
  {pic}
</div>"""}]
