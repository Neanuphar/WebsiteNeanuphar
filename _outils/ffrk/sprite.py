#!/usr/bin/env python3
"""Extrait le sprite d'un perso FFRK depuis une capture d'écran de sa fiche.

Usage : python3 sprite.py <capture.jpg> <sortie.png> [--apercu apercu.png] [--pas 5.1]

La capture doit montrer la fiche du perso (grille 必殺技 ou écran de stats) :
le petit sprite est en haut à gauche, à côté du nom. Le script :
  1. retrouve la grille de pixels du sprite (environ 5,1 pixels d'écran par pixel),
  2. reconstruit le sprite à sa taille d'origine (environ 16 × 24),
  3. retire le fond gris et les lignes du cadre.
Si le sprite paraît brouillé, relancer avec --pas 5.1 (valeur habituelle).
"""
import argparse
from collections import deque
import numpy as np
from PIL import Image

p = argparse.ArgumentParser()
p.add_argument("capture"); p.add_argument("sortie")
p.add_argument("--apercu"); p.add_argument("--pas", type=float)
p.add_argument("--blanc", type=float, default=999, help="ex. 225 : un gris plus clair n'est pas du fond (perso en blanc coupé)")
a = p.parse_args()

im = Image.open(a.capture).convert("RGB")
k = im.width / 1080                      # captures de référence : 1080 px de large
A = np.asarray(im).astype(int)
x0, y0, x1, y1 = [round(v * k) for v in (30, 270, 150, 430)]
zone = A[y0:y1, x0:x1].astype(float)

def bords(axe):
    d = np.abs(np.diff(zone.mean(2), axis=axe)).mean(1 - axe)
    return d - d.mean()

def phase(axe, pas):
    d = bords(axe)
    return max(np.arange(0, pas, 0.25), key=lambda ph: d[np.round(np.arange(ph, len(d) - 1, pas)).astype(int)].mean())

def grille(axe):
    d = bords(axe); best = None
    for p10 in range(round(45 * k), round(58 * k) + 1):
        pas = p10 / 10
        ph = phase(axe, pas)
        s = d[np.round(np.arange(ph, len(d) - 1, pas)).astype(int)].mean()
        if best is None or s > best[0]: best = (s, pas, ph)
    return best[1], best[2]

if a.pas:
    px = py = a.pas * k; phx, phy = phase(1, px), phase(0, py)
else:
    (px, phx), (py, phy) = grille(1), grille(0)

C = int((x1 - x0 - phx) // px) - 1; R = int((y1 - y0 - phy) // py) - 1
n = np.zeros((R, C, 3), int)
for j in range(R):
    for i in range(C):
        cx = x0 + phx + px * i + px / 2 + .5; cy = y0 + phy + py * j + py / 2 + .5
        n[j, i] = np.median(A[int(cy) - 1:int(cy) + 2, int(cx) - 1:int(cx) + 2].reshape(-1, 3), axis=0)

lum = n.mean(2); sat = n.max(2) - n.min(2)
gris = (lum > 30) & (sat <= 8) & (lum < a.blanc)   # le blanc pur (vêtement) n'est jamais du fond
fond = np.zeros((R, C), bool); q = deque()
for j in range(R):
    for i in range(C):
        if (j in (0, R - 1) or i in (0, C - 1)) and gris[j, i]: fond[j, i] = True; q.append((j, i))
while q:
    j, i = q.popleft()
    for dj, di in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        y, x = j + dj, i + di
        if 0 <= y < R and 0 <= x < C and not fond[y, x] and gris[y, x]: fond[y, x] = True; q.append((y, x))
for j in range(R):                       # lignes sombres du cadre, sur toute la largeur
    if (~fond[j]).sum() >= C - 2 and lum[j][~fond[j]].mean() < 40: fond[j] = True

# garder le plus gros bloc de pixels : le perso
lab = np.zeros((R, C), int); tailles = {}; num = 0
for j in range(R):
    for i in range(C):
        if not fond[j, i] and not lab[j, i]:
            num += 1; q = deque([(j, i)]); lab[j, i] = num; tailles[num] = 0
            while q:
                y, x = q.popleft(); tailles[num] += 1
                for dj in (-1, 0, 1):
                    for di in (-1, 0, 1):
                        yy, xx = y + dj, x + di
                        if 0 <= yy < R and 0 <= xx < C and not fond[yy, xx] and not lab[yy, xx]:
                            lab[yy, xx] = num; q.append((yy, xx))
perso = max(tailles, key=tailles.get)
alpha = (lab == perso).astype(np.uint8) * 255
ys, xs = np.where(alpha > 0)
rgba = np.dstack([n.clip(0, 255).astype(np.uint8), alpha])[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
sp = Image.fromarray(rgba, "RGBA"); sp.save(a.sortie, optimize=True)
print(f"sprite {sp.size[0]}×{sp.size[1]} (grille {px / k:.2f} × {py / k:.2f})")
if a.apercu:
    w, h = sp.size; f = Image.new("RGBA", (w * 8 + 10, h * 8 + 20), (185, 182, 174, 255))
    f.alpha_composite(sp.resize((w * 8, h * 8), Image.NEAREST), (5, 10)); f.save(a.apercu)
