# Site Neanuphar — règles du projet

Site perso qui regroupe des petits outils utilisables dans le navigateur.
En ligne sur neanuphar.fr, hébergé par GitHub Pages (branche `main`, dossier racine). Chaque envoi sur `main` met le site à jour.
Objectif : un site simple et fiable, pas un projet d'apprentissage. Le code est écrit par l'IA, la propriétaire valide visuellement dans le navigateur.

## Structure

```
/
├── CLAUDE.md          ← ce fichier
├── index.html         ← page d'accueil : une carte par outil
├── silhouette/
│   └── index.html     ← Atelier Silhouette
├── smash/
│   └── index.html     ← Checklist Smash Ultimate
├── recettes/
│   └── index.html     ← Mes recettes (liste dans le tableau RECETTES)
└── CNAME              ← créé par GitHub Pages pour neanuphar.fr : ne pas supprimer
```

- Un outil = un dossier = un seul fichier `index.html`.
- HTML, CSS et JavaScript sont dans ce même fichier (pas de fichier externe).
- Les liens entre pages sont relatifs et pointent vers le fichier complet (`silhouette/index.html`, `../index.html`). Un lien vers un simple dossier (`silhouette/`) marche en ligne mais ouvre une liste de fichiers en local.

## Règles techniques

- Zéro framework, zéro npm, zéro étape de compilation. Du HTML/CSS/JS simple que GitHub Pages sert tel quel.
- Pas de bibliothèque externe ni de police externe : tout doit marcher hors ligne en double-cliquant sur le fichier.
- Tout s'exécute dans le navigateur du visiteur : aucune donnée envoyée nulle part.
- Pas de secret, mot de passe, clé API ou info perso dans le repo : il peut devenir public.
- Les données qu'on peut vouloir modifier à la main (listes, réglages par défaut) sont regroupées en haut du script, dans un tableau ou un objet clairement nommé.
- Sauvegarde locale (localStorage) : toujours dans un try/catch, la page doit marcher sans.

## Règles visuelles

- Tout le texte visible est en français.
- Mode sombre automatique selon le système (`prefers-color-scheme`).
- Mêmes couleurs partout, définies en variables CSS en haut de chaque fichier :

```css
:root {
  --fond: #f4f1ea;  --carte: #ffffff;  --texte: #1f1d1a;
  --doux: #6b665e;  --accent: #2f7d6d; --bord: #e2ddd2;
}
@media (prefers-color-scheme: dark) {
  :root {
    --fond: #16181b;  --carte: #202328;  --texte: #ece9e2;
    --doux: #9a968e;  --accent: #5cc2aa; --bord: #2e3238;
  }
}
```

- Police : `system-ui, -apple-system, "Segoe UI", sans-serif`.
- Coins arrondis 12px sur les cartes et panneaux, bordure 1px `var(--bord)`.
- Chaque outil a un lien « ← Accueil » en haut à gauche, qui mène à `../index.html`.
- La page doit rester utilisable sur téléphone (pas de défilement horizontal).

## Ajouter un outil

1. Créer `nom-de-l-outil/index.html` en respectant les règles ci-dessus.
2. Ajouter une carte dans `index.html` à la racine (copier un bloc `<a class="carte">`).
3. Tester en local, puis faire un commit.

## Méthode de travail

- Un commit après chaque modification qui marche, avec un message clair en français.
- Ne jamais modifier un outil quand on travaille sur un autre.
- Garder la V1 simple : on ajoute des fonctions seulement quand la base marche et est en ligne.
