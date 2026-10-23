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
├── detourage/
│   └── index.html     ← Détourage (fond auto, baguette, gomme, restaurer)
├── smash/
│   └── index.html     ← Checklist Smash Ultimate
├── recettes/
│   └── index.html     ← Mes recettes (liste dans le tableau RECETTES)
├── ffrk/
│   ├── index.html     ← Wiki FFRK (persos et capacités spéciales)
│   ├── donnees.json   ← données du wiki (créé au premier enregistrement)
│   ├── fond.jpg       ← illustration officielle FFRK, déjà floutée, en fond de page
│   └── images/<perso>/← sprites et icônes de capacités
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

## Recettes (`recettes/index.html`)

- Chaque recette est un bloc du tableau `RECETTES`, en haut du script.
- Les quantités qui doivent changer quand on double la recette sont entre crochets : `"[185] g de beurre"`, `"[0.75] c. à café de bicarbonate"`, `"[8] à [12] parts"`. Mettre aussi les crochets dans `portions`.
- `{s}` ajoute un « s » si le nombre juste avant dépasse 1 : `"[1] œuf{s} + [1] jaune{s} d'œuf"` devient « 2 œufs + 2 jaunes d'œuf ».
- Pas de crochets pour ce qui ne double pas : températures, temps, taille des boules, dimensions du plat.
- Les étapes et les notes ne sont pas recalculées : y éviter les quantités, renvoyer plutôt aux ingrédients (« le sucre pour les fruits »).
- Quand une info manque dans une recette donnée, la compléter seulement avec une valeur standard et le signaler (« environ », estimation).

## Wiki FFRK (`ffrk/`) — exception aux règles « un seul fichier » et « hors ligne »

- Les données sont dans `ffrk/donnees.json`, les images dans `ffrk/images/<id-du-perso>/`. Les chemins d'images dans le JSON sont relatifs au dossier `ffrk/` (`images/relm/xxx.webp`).
- Format : `{ revision, maj, persos: [{ id, nom, nomJP, serie, categorie, elements, sprite, capacites: [{ id, type, categorie, nomJP, nomFR, elements, effet, image }] }] }`. `serie` vaut une valeur de `SERIES`, `categorie` (perso et capacité) vaut `"physique"`, `"magique"`, `"soutien"` ou `""` (non précisée), et pour un perso seulement `"mixte"`, `elements` des `id` de `ELEMENTS` (voir le haut du script).
- `recheck: true` sur un perso affiche une pastille « À revérifier » : persos faits par une autre session, dont les traductions sont à recontrôler avec les captures. Retirer le champ une fois vérifié.
- La recherche ne porte que sur les persos : nom, nom japonais, jeu, et les `elements` du perso (un perso s'affiche s'il a au moins un des éléments cochés). Les éléments des capacités servent seulement à l'affichage du détail.
- La page enregistre elle-même dans ce repo via l'API GitHub, avec une clé (token) que la propriétaire colle dans la page. La clé reste dans son navigateur : ne jamais l'écrire dans le repo.
- Chaque enregistrement depuis la page fait un seul commit (« Wiki FFRK : mise à jour »). La page refuse d'écraser le fichier s'il a changé ailleurs entre-temps.
- Pour modifier `donnees.json` directement (par exemple pour ajouter un perso à partir de captures d'écran) : `git pull` d'abord, garder le format, augmenter `revision` de 1, puis commit et push.
- Icônes de capacité : environ 160 px, fond transparent. Sprites : PNG sans lissage.

### Ajouter un perso à partir de captures d'écran (procédure habituelle)

La propriétaire envoie, pour un perso : la grille de l'onglet 必殺技 (fiche du perso, avec le sprite en haut à gauche et le type, par ex. 「魔女/魔法万能タイプ」), puis l'écran de détail de chaque capacité **possédée** (cercles en couleur dans la grille ; les grisés ne sont pas possédés et ne vont pas dans le wiki). Les longues capacités arrivent en plusieurs captures (défilement). Ignorer les écrans 英雄の記憶 et セット可能種別.

0. Faire l'inventaire : pour chaque cercle en couleur de la grille, retrouver sa capture (type + nom en haut de l'écran de détail). Une capacité longue est complète quand on voit du haut jusqu'au bloc 超錬効果 (ou 修得時). Signaler à la fin ce qui manque, sans l'inventer. Les captures peuvent couvrir plusieurs persos d'un coup.
1. `git pull`. Outils : `pip install pillow numpy --break-system-packages` si besoin.
2. Sprite : `python3 _outils/ffrk/sprite.py <grille.jpg> ffrk/images/<id>/sprite.png --apercu /tmp/apercu.png`. Regarder l'aperçu ; s'il est brouillé, relancer avec `--pas 5.1` ; si le perso est coupé (vêtement blanc pris pour du fond, comme Arc), ajouter `--blanc 235`.
3. Icônes : pour chaque capacité, sur la capture du **haut** de son écran de détail, `python3 _outils/ffrk/icone.py <capture.jpg> ffrk/images/<id>/<nom-de-la-capacite>.webp`. Un score < 250 veut dire que ce n'est pas la bonne capture (souvent une capture défilée) ou qu'il faut `--y`. Vérifier toutes les icônes ensemble sur une planche avant de continuer : `python3 _outils/ffrk/planche.py <id> [<id>…] <sortie.png>` puis regarder l'image. Bien associer chaque capture à sa capacité, l'ordre d'envoi n'est pas fiable (l'icône porte le badge du type : S, M, D, chaîne…).
4. Ajouter le perso dans `ffrk/donnees.json` (format ci-dessus), `revision` +1. Écrire le fichier avec un petit script Python : `json.dump(..., ensure_ascii=False, indent=1)`, sans saut de ligne final, `maj` au format `2026-10-22T04:30:59.000Z`. Insérer le perso après le dernier perso de la même série. Le nom de fichier d'une icône = l'`id` de la capacité sans le `c-`.
   - `id` : nom français en minuscules avec tirets. `nom` : nom français usuel (Guerrier de la Lumière, Voleur, Super Moine…). `serie` : le chiffre romain affiché.
   - `categorie` du perso : 物理… → physique, 魔法… (y compris 魔法万能) → magique, 回復/支援 → soutien. Type mixte (魔法回復, 物理補助…) : classer selon ce que fait le kit (Minwu attaque surtout → magique ; Gordon fait surtout du soutien → soutien), et le dire dans la réponse. Perso qui attaque vraiment des deux façons (versions ・力 physiques et ・魔 magiques, comme le Chevalier Oignon) → `"mixte"` (affiché « Physique et magique », trouvé par les filtres Physique et Magique ; jamais sur une capacité).
   - `elements` du perso : les éléments de ses capacités d'attaque (pas « neutre »). Un perso qui ne fait que soigner n'en a pas.
   - Capacités rangées par type : 初期, 専用, 超必殺, Burst, 超絶, Chain, LB閃, 閃技, OFlow, 覚醒, S奥義, O奥義, 真奥義, A神技, C神技, O神技, M神技, 究極, D覚醒, T覚醒. Ajouter un type nouveau à `TYPES` dans `ffrk/index.html`.
   - Capacité : `categorie` physique / magique selon 物理 / 魔法 dans le texte ; soutien si elle n'attaque pas. `elements` : ceux du texte, avec « neutre » pour 無属性.
5. Traduction de l'effet (`effet`), en français, complète, avec le même style que les persos existants (relire Garland ou le Voleur comme modèle) :
   - Commencer par « Réservée à X. » puis « Utilisable N fois. » si 回数 est indiqué.
   - Sections en MAJUSCULES : ATTAQUE / EFFET, puis chaque mode, compétences Burst ou Synchro, attaque supplémentaire, BONUS D'ENTRAÎNEMENT (超錬, avec le niveau d'entraînement qui débloque), BONUS D'APPRENTISSAGE (修得時).
   - Lexique déjà utilisé : まとい = imprégnation, 【重式】 = renforcée [重式], 限界突破 = plafond de dégâts, 待機時間 = temps d'attente, アビリティ = compétence, 追撃 = attaque supplémentaire, ヘイスト = Hâte, プロテス = Carapace, シェル = Blindage, リジェネ = Récup, エスナ = Esuna, 踏みとどまる = Tenir bon, 必殺技ゲージ = jauge de capacités spéciales, リミットゲージ = jauge de Limite, ATBゲージの蓄積時間を1回なしにする = la prochaine jauge ATB se remplit instantanément (1 fois), 英雄強化 = renforcement du héros, ヘヴィチャージ = Charge lourde, 真奥義解放 = Libération du vrai arcane, 真奥義強化・X = état [Vrai arcane renforcé – X], 奥義 = arcane (jamais « Ougi »), 真限界突破 = vrai plafond de dégâts, デプロテ = Déprotection, 分身 = Image, 微弱 = légèrement faible, 遠距離 = à distance, 滞空時間 = temps en l'air, ジャンプ攻撃 = attaque Saut, 白魔法 = Magie blanche, 黒魔法 = Magie noire, モンク = Moine, 竜騎士 = Chevalier dragon, シーフ = Voleur, 物理補助 = Soutien physique (validé ; 魔法補助 = Soutien magique), ホーリー = Miracle, サンダー = Foudre, ジョブリミットチェイン = chaîne de métier, 属性リミットチェイン = chaîne élémentaire, 万象剥離 = laissé en japonais (effet inconnu), 修得時 = BONUS D'APPRENTISSAGE, 錬度 = niveau d'entraînement, スロウ = Lenteur, 暗黒 = Arts sombres (école, validé), トライエレメントモード = mode Triple élément, 魔界 = Outre-monde, 魔法剣 = Magilame, 魔法剣士 = Chevalier mystique, リジェネガ = Récup forte, écoles physiques (validées) : 物理攻撃 = Attaque physique, 物理補助 = Soutien physique, 物理スピード = Vitesse physique, 物理ヘヴィ = Physique lourd, 魔法剣 = Magilame, 疾風 = bourrasque, 暴風 = tempête, 悠久 = éternel, 行動キャンセル = annuler l'action, 召喚魔法 = Invocation, クリスタルモード = mode Cristal, クリスタルフォース = Force du cristal, 防御&魔法防御貫通 = les attaques percent la défense et la défense magique, ブレイブモード = mode Brave, 女性英雄 = héroïne, 自身と同じ列 = de la même rangée, ソウルドライブ = Soul Drive, 護衛モード = mode Escorte, …・力 / …・魔 (variantes d'une capacité) = « … – Force » / « … – Magie », だいまほう = grande magie, 精錬度 = niveau d'affinage, クアッドエレメントモード = mode Quadruple élément, ツインエレメントモード = mode Double élément, 波動砲 = canon à ondes, 波動球 = sphère d'ondes, 触手 = tentacules, 氾濫 = débordement, 死の宣告 = Arrêt de mort, シリーズリミットチェイン = chaîne de série, ドラグーンプライド = Fierté du dragon, 即時着地攻撃 = attaque à atterrissage immédiat, 幻獣 = chimère, デシェル = Déblindage, 忍術 = ninjutsu, 正体不明 = Identité inconnue, へんげんじざい = Protéiforme, 継続ダメージ = dégâts continus, アビリティバーサク = Furie de compétences (à confirmer), 必殺剣 = Bushido (à confirmer), T覚醒モード = mode T-Éveil (jauge TP), ウェポンスキル = compétence d'arme, 邪悪な心 = Cœur malveillant, ものまね = imitation / mime, かまえる = se mettre en garde, ひきつけ = attirer les attaques, デスペル = Dissipation, 天命の共鳴 = Résonance du destin, Wジョブ = Double métier, グロシアーナ = Grociana (à confirmer), 老賢者 = vieux sage, 無手勝流 = style libre, 記憶の共鳴 = Écho des souvenirs (≠ 記憶の共振 = Résonance des souvenirs), 全属性 = tous les éléments, 猛進モード = mode Ruée, ふたりがけ = double incantation, アクセルモード = mode Accélération, Noms de persos : nom de la version française (ギルバート = Edward, アーシュラ = Ursula, ルーネス = Luneth), 幻界 = monde des chimères, 召喚魔法攻撃 = attaque d'Invocation, LBG召喚 = Limit Break d'invocation de gardien (ガーディアン = gardien), 自身のステータスで種別が変わる = « physique ou de Magie blanche selon les statistiques de X »., 光撃 = Frappe radieuse, フェイタルダメージ = dégâts fatals, ソーサリーダメージ = dégâts de sorcellerie, 暗闇 (altération) = Cécité, 麻痺 = Paralysie, 親分の教え = Enseignement du chef, いかりばくはつ = Explosion de colère, アビリティバーサク = Furie de compétences (à confirmer), 超装 = Super-armure (à confirmer), 女性 = héroïnes. Toujours « attaques physiques » (jamais « coups physiques »).
   - Écoles de compétences (onglets de l'écran アビリティ生成), noms validés ou en usage : Magie : 黒魔法 = Magie noire, 白魔法 = Magie blanche, 召喚魔法 = Invocation. Physique : 物理攻撃 = Attaque physique, 物理補助 = Soutien physique, 物理スピード = Vitesse physique, 魔法剣 = Magilame, 物理ヘヴィ = Physique lourd. Métiers 1 : 竜騎士 = Chevalier dragon, モンク = Moine, シーフ = Voleur, ナイト = Chevalier, 侍 = Samouraï, 忍者 = Ninja. Métiers 2 : 吟遊詩人 = Barde, 踊り子 = Danseuse, 機工士 = Machiniste, 暗黒 = Arts sombres, シューター = Tireur, 魔女 = Sorcière. 魔法補助 = Soutien magique.
   - Noms de capacités récurrents : 極星… (M神技) = « … polaire », …・極 (真奥義) = « … suprême », 究極… = « … ultime », 絆・X天命 = « Lien – Destin de X », 熟練の… = « … de l'expert », 星撃・X = Frappe stellaire – X, 心撃・X = Frappe du cœur – X, …改 = « … Kai ».
   - Modèles à copier selon le type : M神技 → Wol ou Minwu ; 真奥義 → Maria ou Josef ; 究極 → Maria ou Minwu ; D覚醒 → Guerrier de la Lumière ou Minwu ; Chain → Matoya ou Richard ; S奥義 → Maria ou Josef. Toujours « Réservée à X. » (féminin, c'est la capacité), même pour un perso masculin.
   - Noms de capacités : traduire le sens (ou l'anglais caché derrière le katakana) en français, garder le japonais dans `nomJP`.
   - Ce qui est incertain : le signaler à la fin de l'effet par « À VÉRIFIER : … ». Ne jamais inventer.
6. Tester : `python3 _outils/ffrk/tester.py <id> [<id>…]` (lance son propre serveur ; vérifie cercles, images, largeur téléphone, erreurs JS). Ne pas faire `pkill -f http.server` : ça tue aussi le shell. Puis commit « Wiki FFRK : <perso> », push.
7. Répondre avec un tableau type / nom japonais / traduction / catégorie, et la liste de ce qui est à vérifier.

Les dossiers qui commencent par `_` (comme `_outils/`) ne sont pas publiés par GitHub Pages.

## Méthode de travail

- Un commit après chaque modification qui marche, avec un message clair en français.
- Ne jamais modifier un outil quand on travaille sur un autre.
- Garder la V1 simple : on ajoute des fonctions seulement quand la base marche et est en ligne.
