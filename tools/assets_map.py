"""Correspondance entre les fichiers générés (Asset3DMame/) et les noms du site."""

import os
from pathlib import Path

# Les originaux restent hors du repo. Surcharger avec la variable MAME_ASSETS si besoin.
SRC = Path(os.environ.get("MAME_ASSETS", r"C:\Users\aliyo\OneDrive\Documents\Asset3DMame"))

MAPPING = {
    "cube-M.webp": "cube-M",
    "cube-A.webp": "cube-A",
    "Bloc en bois doré avec lettre É.png": "cube-E-accent",
    "Cube en bois doré avec lettre T.png": "cube-T",
    "Cube jouet en bois avec lettre O.png": "cube-O",
    "Cube en bois doré avec lettre I.png": "cube-I",
    "Bloc jouet en bois avec lettre L dorée.png": "cube-L",
    "Cube en bois doré avec lettre E.png": "cube-E",
    "Étoile en bois doré patiné.png": "etoile",
    "Sphère en bois clair détaillée.png": "sphere-bois",
    "Sphère ivoire satinée sur fond noir.png": "sphere-ivoire",
    "Anneau torsadé ivoire brillant.png": "anneau",
    "Croissant de lune ivoire bordé d’or.png": "lune",
    "Hochet en bois et or sur fond noir.png": "hochet",
    "Lapin en peluche au nœud crème.png": "doudou-lapin",
    "Xylophone en bois et maillet doré.png": "xylophone",
    "Livre sensoriel ouvert _ ours et lune étoiles.png": "livre",
    "Pot à pinceaux étoilé doré.png": "pinceaux",
    "Jeune pousse dans un pot doré.png": "pousse",
    "Coussin nuage souriant ivoire.png": "nuage",
    "Arc-en-ciel en bois aux accents dorés.png": "arc-en-ciel",
    "Blocs en bois dorés ÉTO étoiles.png": "blocs-eto",
    "logo-mame-transparent.png": "logo-mame",
    "logo-mame-sans-contact.png": "logo-mame-sans-contact",
}


def source(name: str) -> Path:
    """Chemin d'un original : tools/sources/ (fournis à part) puis le dossier principal."""
    local = Path(__file__).resolve().parent / "sources" / name
    return local if local.exists() else SRC / name
