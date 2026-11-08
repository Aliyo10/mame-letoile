// Source unique des informations factuelles : pages, footer et JSON-LD lisent ce fichier.

export const site = {
  name: "MAME L'Étoile",
  shortName: "L'Étoile",
  type: "Maison d'Assistantes Maternelles",
  foundedLabel: 'août 2023',
  url: 'https://aliyo10.github.io/mame-letoile',

  team: {
    names: ['Sabira', 'Claire'],
  },

  address: {
    street: '5 cours Saint Félix',
    postalCode: '26000',
    city: 'Valence',
    region: 'Drôme',
    country: 'FR',
  },

  geo: { latitude: 44.933, longitude: 4.881 },

  phone: {
    display: '06 51 79 50 80',
    href: 'tel:+33651795080',
    international: '+33651795080',
  },

  // À VALIDER : « myyahoo » ressemble à une coquille.
  email: 'mame26@myyahoo.com',

  hours: {
    dayLabels: ['Lundi', 'Mardi', 'Jeudi', 'Vendredi'],
    daysSummary: 'Lundi, mardi, jeudi et vendredi',
    schemaDays: ['Monday', 'Tuesday', 'Thursday', 'Friday'],
    // À VALIDER : le site actuel indique 17h30, une autre source indique 18h00.
    opens: '08:00',
    closes: '17:30',
    label: '8h00 – 17h30',
  },

  // À VALIDER : source externe.
  closures: [
    'Deux semaines à Noël',
    "La deuxième semaine des vacances d'hiver",
    'La deuxième semaine des vacances de printemps',
    "Tout le mois d'août",
    "Les jours fériés et le pont de l'Ascension",
  ],

  // À METTRE À JOUR chaque année : thème du projet pédagogique en cours.
  pedagogicalTheme: 'Les saisons et la nature',

  // Clé d'accès Web3Forms, à créer sur web3forms.com avec l'adresse de réception.
  web3formsKey: '[CLÉ_WEB3FORMS]',
} as const;

export const duo = site.team.names.join(' et ');

export const fullAddress = `${site.address.street}, ${site.address.postalCode} ${site.address.city}`;

export const nav = [
  { href: 'presentation.html', label: 'La maison' },
  { href: 'services.html', label: 'Le quotidien' },
  { href: 'contact.html', label: 'Contact' },
] as const;
