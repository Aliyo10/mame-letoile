# MAME L'Étoile

Site vitrine de la Maison d'Assistantes Maternelles L'Étoile, à Valence. Astro en sortie statique, déployé sur GitHub Pages.

## Travailler en local

```bash
npm install
npm run dev
```

Le site est alors sur `http://localhost:4321/mame-letoile/`.

## Mettre à jour les informations

Tout est dans **`src/data/site.ts`** : adresse, téléphone, email, jours, horaires, fermetures, prénoms, thème pédagogique, clé du formulaire. Pages, footer et données SEO lisent ce fichier.

Avant la mise en ligne, traiter les commentaires `// À VALIDER` et `// À METTRE À JOUR` de ce fichier.

Pour activer le formulaire, créer une clé sur [web3forms.com](https://web3forms.com) avec l'adresse qui doit recevoir les demandes, puis remplacer `[CLÉ_WEB3FORMS]` dans `web3formsKey`. Tant que le remplacement n'est pas fait, le formulaire renvoie le visiteur vers l'email.

## Remplacer le logo

Déposer le fichier dans `src/assets/logo/` sous le nom `logo.png` (ou `.webp`, `.svg`) ; il doit avoir un fond transparent. Sans fichier, le wordmark de secours s'affiche. Pour détourer un logo fourni sur fond blanc : le placer en `tools/sources/logo-fond-blanc.webp`, puis lancer `python tools/make_logo.py`.

## Remplacer une image de parallaxe

Les images du site sont dans `src/assets/parallax/`. Pour en remplacer une, il suffit de déposer un PNG détouré **sans ombre** (l'ombre est faite en CSS) sous le même nom. Si un PNG manque, une forme CSS s'affiche à sa place.

Pour repasser par le nettoyage automatique :

```bash
python -m venv .venv
.venv/Scripts/python -m pip install pillow numpy scipy "rembg[cpu]"
```

1. Déclarer l'original dans `tools/assets_map.py`. Il est cherché dans `tools/sources/`, puis dans le dossier `Asset3DMame` (chemin modifiable avec la variable `MAME_ASSETS`).
2. Contrôler : `python tools/audit_png.py`.
3. Nettoyer : `python tools/clean_png.py nom-de-l-image`. Ajouter l'image à `REMBG` (halo réel) ou à `EROSION` (frange) dans ce script si l'audit la signale.
4. Vérifier à l'œil : `python tools/contact_sheet.py tools/out/planche.png src/assets/parallax`.

Les emplacements de départ des cubes du hero sont définis dans `src/components/Hero.astro` ; les lettres s'y répartissent au hasard à chaque chargement.

## Déployer

La branche `dev` sert au travail, `main` est la branche en ligne : tout push sur `main` déclenche `.github/workflows/deploy.yml`.

```bash
git checkout main
git merge dev
git push origin main
```

Une seule fois, dans le repo GitHub : **Settings > Pages > Source : GitHub Actions**.

Avec un domaine personnalisé, mettre à jour `site` et retirer `base` dans `astro.config.mjs`, puis corriger `url` dans `src/data/site.ts`.
