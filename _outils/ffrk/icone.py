#!/usr/bin/env python3
"""Découpe en cercle l'icône d'une capacité FFRK depuis l'écran de détail.

Usage : python3 icone.py <capture.jpg> <sortie.webp> [--y Y] [--apercu apercu.png]

L'icône ronde est à gauche, sous le titre de la capacité. Sa hauteur varie
selon la longueur du texte : le script la cherche tout seul sur toute la
hauteur (ou autour de --y, en pixels d'une capture de 1080 px de large).
Il ajuste le cercle sur l'anneau métallique de l'icône, puis l'exporte
en 160 × 160 avec fond transparent.
Utiliser la capture du HAUT de l'écran de détail (celle qui montre l'icône).
"""
import argparse
import numpy as np
from PIL import Image, ImageDraw

p = argparse.ArgumentParser()
p.add_argument("capture"); p.add_argument("sortie")
p.add_argument("--y", type=int); p.add_argument("--apercu")
a = p.parse_args()

im = Image.open(a.capture).convert("RGB")
k = im.width / 1080
A = np.asarray(im).astype(int)
t = np.linspace(0, 2 * np.pi, 180, endpoint=False)
garde = ~((t > 5.2) | (t < .3)) & ~((t > 1.0) & (t < 2.2))   # évite l'étiquette et « MASTER »

def score(cx, cy, r):
    xs = (cx + r * np.cos(t[garde])).astype(int); ys = (cy + r * np.sin(t[garde])).astype(int)
    xo = (cx + (r + 6 * k) * np.cos(t[garde])).astype(int); yo = (cy + (r + 6 * k) * np.sin(t[garde])).astype(int)
    if ys.min() < 0 or yo.max() >= A.shape[0]: return -1e9
    return A[ys, xs].sum(1).mean() - A[yo, xo].sum(1).mean()

def chercher(cx_min, cx_max, cy_min, cy_max, pas):
    best = None
    for cx in range(cx_min, cx_max + 1, pas):
        for cy in range(cy_min, cy_max + 1, pas):
            for r in range(round(72 * k), round(90 * k) + 1, max(1, pas // 2)):
                s = score(cx, cy, r)
                if best is None or s > best[0]: best = (s, cx, cy, r)
    return best

cx0 = round(150 * k)
if a.y:
    s, cx, cy, r = chercher(cx0 - 30, cx0 + 30, round(a.y * k) - 40, round(a.y * k) + 40, 2)
else:
    s, cx, cy, r = chercher(cx0 - 10, cx0 + 10, round(400 * k), round(1300 * k), 8)
    s, cx, cy, r = chercher(cx - 10, cx + 10, cy - 10, cy + 10, 1)
r += round(2 * k)
c = im.crop((cx - r, cy - r, cx + r, cy + r)).convert("RGBA")
m = Image.new("L", (8 * r, 8 * r), 0); ImageDraw.Draw(m).ellipse((0, 0, 8 * r - 1, 8 * r - 1), fill=255)
c.putalpha(m.resize((2 * r, 2 * r), Image.LANCZOS))
c = c.resize((160, 160), Image.LANCZOS)
c.save(a.sortie, quality=90)
print(f"icône centre ({cx}, {cy}) rayon {r} score {s:.0f}" + ("  ⚠ score faible : vérifier l'image, ou relancer avec --y" if s < 250 else ""))
if a.apercu:
    f = Image.new("RGBA", (180, 180), (40, 44, 52, 255)); f.alpha_composite(c, (10, 10)); f.save(a.apercu)
