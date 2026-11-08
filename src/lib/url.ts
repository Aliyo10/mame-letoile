/** Préfixe un chemin interne avec `base`, pour que les liens survivent à GitHub Pages. */
export const url = (path = '') =>
  `${import.meta.env.BASE_URL.replace(/\/$/, '')}/${path.replace(/^\//, '')}`;
