#!/usr/bin/env python3
"""Скачивает варианты фото под нужные пропорции: card 16:10, box 4:3."""
import urllib.request, os, sys
from concurrent.futures import ThreadPoolExecutor

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "site", "img")
SPECS = [("card", 640, 400), ("card", 1000, 625),
         ("box", 640, 480), ("box", 1000, 750), ("box", 1600, 1200)]
Q = 64
# у этих кадров автообрезка по «энтропии» срезала главное — берём центр
CENTER = {"toolchest"}
# точное кадрирование для отдельных кадров: имя -> строка параметров Unsplash
FOCAL = {
    "byd-seal": "crop=focalpoint&fp-x=0.5&fp-y=0.5&fp-z=1.18",
    "suv-city": "crop=focalpoint&fp-x=0.35&fp-y=0.42&fp-z=1.7",
    "ev-charge": "crop=focalpoint&fp-x=0.68&fp-y=0.58&fp-z=1.5",
    "service-desk": "crop=focalpoint&fp-x=0.60&fp-y=0.70&fp-z=1.6",
}

pairs = []
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "images.txt")) as f:
    for line in f:
        line = line.split()
        if len(line) == 2:
            pairs.append((line[0], line[1]))

jobs = []
for name, pid in pairs:
    for kind, w, h in SPECS:
        for fmt in ("avif", "webp"):
            if name in FOCAL:
                crop = FOCAL[name]
            else:
                crop = "crop=" + ("center" if name in CENTER else "entropy")
            url = ("https://images.unsplash.com/photo-%s?fm=%s&fit=crop&%s"
                   "&w=%d&h=%d&q=%d" % (pid, fmt, crop, w, h, Q))
            jobs.append((url, os.path.join(OUT, "%s-%s-%d.%s" % (name, kind, w, fmt))))

def get(job):
    url, path = job
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            data = urllib.request.urlopen(req, timeout=60).read()
            if len(data) < 400:
                raise ValueError("слишком маленький ответ")
            open(path, "wb").write(data)
            return None
        except Exception as e:
            if attempt == 2:
                return "%s — %s" % (os.path.basename(path), e)

with ThreadPoolExecutor(max_workers=12) as ex:
    errors = [e for e in ex.map(get, jobs) if e]

print("скачано: %d из %d" % (len(jobs) - len(errors), len(jobs)))
for e in errors[:10]:
    print("  ошибка:", e)
sys.exit(1 if errors else 0)
