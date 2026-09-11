#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Нарезает сгенерированные кадры под пропорции сайта и кодирует в AVIF и WebP.

Исходники — PNG 4:3 из site/img-new/. На выходе для каждого слота сайта:
  <слот>-card-640.avif|webp    16:10, карточки услуг и кейсов
  <слот>-card-1000.avif|webp
  <слот>-box-640.avif|webp     4:3, первые экраны и блоки со сплитом
  <слот>-box-1000.avif|webp
  <слот>-box-1600.avif|webp

AVIF кодируется ffmpeg (libsvtav1), WebP — cwebp. Оба есть локально.
"""

import os, subprocess, shutil, sys
from PIL import Image

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "site", "img-new")
OUT = os.path.join(ROOT, "site", "img")
TMP = os.path.join(ROOT, ".img-tmp")

# слот на сайте  ->  исходный кадр
MAP = {
    "oil-change":     "to-oil",
    "diag-laptop":    "diag-laptop",
    "suspension":     "susp-arm",
    "brake-disc":     "brake-disc",
    "engine-bay":     "elec-harness",
    "dash-screen":    "screen",
    "dash-night":     "dash-cluster",
    "coilovers":      "parts-box",
    "lift-garage":    "lift-bay",
    "workshop":       "workshop",
    "engine-work":    "hands-work",
    "mechanic-check": "desk-tablet",
    "diag-tools":     "diag-stand",
    "toolchest":      "tools",
    "brakes":         "brake-hands",
    "ev-battery":     "hv-battery",
    "ev-plug":        "ev-plug",
    "keys":           "keys",
    "service-desk":   "car-rear",
    "suv-neon":       "car-side",
    "byd-seal":       "car-front",
    "byd-suv":        "car-side",
    "estimate":       "desk-tablet",
}

SPECS = [("card", 640, 400), ("card", 1000, 625),
         ("box", 640, 480), ("box", 1000, 750), ("box", 1600, 1200)]

WEBP_Q = 74
AVIF_CRF = 34


def crop_resize(im, w, h):
    """Обрезает по центру под нужное соотношение и масштабирует."""
    target = w / h
    src = im.width / im.height
    if src > target:                      # исходник шире — режем по бокам
        nw = round(im.height * target)
        box = ((im.width - nw) // 2, 0, (im.width - nw) // 2 + nw, im.height)
    else:                                 # исходник выше — режем сверху и снизу
        nh = round(im.width / target)
        top = round((im.height - nh) * 0.45)   # чуть выше центра: небо важнее пола
        box = (0, top, im.width, top + nh)
    return im.crop(box).resize((w, h), Image.LANCZOS)


def encode(png, base):
    subprocess.run(["cwebp", "-quiet", "-q", str(WEBP_Q), png, "-o", base + ".webp"], check=True)
    subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
                    "-i", png, "-c:v", "libsvtav1", "-crf", str(AVIF_CRF),
                    "-frames:v", "1", base + ".avif"], check=True)


def main():
    missing = [s for s in set(MAP.values()) if not os.path.exists(os.path.join(SRC, s + ".png"))]
    if missing:
        sys.exit("нет исходников: " + ", ".join(sorted(missing)))

    os.makedirs(TMP, exist_ok=True)
    os.makedirs(OUT, exist_ok=True)
    made = 0
    for slot, src in sorted(MAP.items()):
        im = Image.open(os.path.join(SRC, src + ".png")).convert("RGB")
        for kind, w, h in SPECS:
            tmp = os.path.join(TMP, "%s-%s-%d.png" % (slot, kind, w))
            crop_resize(im, w, h).save(tmp)
            encode(tmp, os.path.join(OUT, "%s-%s-%d" % (slot, kind, w)))
            os.remove(tmp)
            made += 2
        print("  %-16s <- %s" % (slot, src))
    shutil.rmtree(TMP, ignore_errors=True)
    print("готово: %d слотов, %d файлов" % (len(MAP), made))


if __name__ == "__main__":
    main()
