"""Planche de vérification : sprite + toutes les icônes d'un ou plusieurs persos, avec leur nom.

Usage : python3 _outils/ffrk/planche.py <id> [<id> ...] <sortie.png>
À lancer depuis la racine du repo. Ouvrir l'image pour vérifier que chaque icône
correspond bien à sa capacité (l'ordre d'envoi des captures n'est pas fiable).
"""
import sys, glob, os
from PIL import Image, ImageDraw

ids, sortie = sys.argv[1:-1], sys.argv[-1]
if not ids:
    sys.exit(__doc__)

CASE, COLS = 170, 6
lignes = []
for pid in ids:
    icones = sorted(glob.glob(f"ffrk/images/{pid}/*.webp"))
    lignes.append((pid, icones))

hauteur = sum(((len(ic) + 1 + COLS - 1) // COLS) * (CASE + 20) for _, ic in lignes)
W = Image.new("RGB", (CASE * COLS, hauteur), (90, 90, 90))
d = ImageDraw.Draw(W)
y = 0
for pid, icones in lignes:
    cases = [f"ffrk/images/{pid}/sprite.png"] + icones
    for i, f in enumerate(cases):
        x, yy = (i % COLS) * CASE, y + (i // COLS) * (CASE + 20)
        if os.path.exists(f):
            im = Image.open(f).convert("RGBA")
            if f.endswith("sprite.png"):
                im = im.resize((im.width * 6, im.height * 6), Image.NEAREST)
            im.thumbnail((CASE - 10, CASE - 10))
            W.paste(im, (x + 5, yy + 5), im)
        nom = pid + " sprite" if f.endswith("sprite.png") else os.path.basename(f)[:-5]
        d.text((x + 5, yy + CASE + 2), nom[:26], fill=(255, 255, 0))
    y += ((len(cases) + COLS - 1) // COLS) * (CASE + 20)
W.save(sortie)
print(f"planche : {sortie}")
