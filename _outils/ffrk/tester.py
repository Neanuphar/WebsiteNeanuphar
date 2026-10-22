"""Test des fiches de persos du wiki dans un vrai navigateur (Playwright, sans réseau).

Usage : python3 _outils/ffrk/tester.py <id> [<id> ...]
À lancer depuis la racine du repo. Lance lui-même un petit serveur local.
Vérifie pour chaque perso : nombre de cercles = nombre de capacités du JSON,
toutes les images chargées, pas de défilement horizontal sur téléphone, aucune erreur JS.
"""
import sys, json, threading, functools, http.server, socketserver
from playwright.sync_api import sync_playwright

ids = sys.argv[1:]
if not ids:
    sys.exit(__doc__)

donnees = json.load(open("ffrk/donnees.json", encoding="utf-8"))
persos = {p["id"]: p for p in donnees["persos"]}

class Silencieux(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a):
        pass

Handler = functools.partial(Silencieux, directory=".")
serveur = socketserver.TCPServer(("127.0.0.1", 0), Handler)
port = serveur.server_address[1]
threading.Thread(target=serveur.serve_forever, daemon=True).start()

ok = True
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 390, "height": 844})
    erreurs = []
    pg.on("pageerror", lambda e: erreurs.append(str(e)))
    pg.on("console", lambda m: m.type == "error" and erreurs.append(m.text))
    pg.route("https://api.github.com/**", lambda r: r.abort())
    for pid in ids:
        if pid not in persos:
            print(f"{pid} : ABSENT du JSON"); ok = False; continue
        pg.goto(f"http://127.0.0.1:{port}/ffrk/index.html#/perso/{pid}")
        pg.wait_for_timeout(1200)
        cercles = pg.locator(".grille-capacites .cercle:not(.plus)").count()
        imgs, cassees, largeur = pg.evaluate(
            """p => { const i = [...document.images].filter(x => x.src.includes('/' + p + '/'));
                     return [i.length, i.filter(x => !x.naturalWidth).map(x => x.src), document.documentElement.scrollWidth]; }""", pid)
        attendu = len(persos[pid]["capacites"])
        bon = cercles == attendu and not cassees and largeur <= 390
        ok &= bon
        print(f"{pid} : {cercles}/{attendu} cercles, {imgs} images, cassées {cassees or 'aucune'}, largeur {largeur} {'OK' if bon else 'PROBLÈME'}")
    if erreurs:
        ok = False
    print("erreurs JS :", erreurs or "aucune")
    b.close()
serveur.shutdown()
sys.exit(0 if ok else 1)
