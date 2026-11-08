// @ts-check
import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

// Sans domaine perso, `base` doit rester le nom du repo. Avec un domaine : retirer `base`
// et mettre le domaine dans `site` (ainsi que `url` dans src/data/site.ts).
export default defineConfig({
  site: 'https://aliyo10.github.io',
  base: '/mame-letoile',
  build: { format: 'file' },
  integrations: [
    sitemap({
      // Mêmes URLs que les canoniques : le build produit des fichiers .html.
      serialize(item) {
        if (!item.url.endsWith('/')) item.url += '.html';
        return item;
      },
    }),
  ],
});
