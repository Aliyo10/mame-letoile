"""Génère public/og-image.png (1200x630) à partir de l'image « Blocs ÉTO »."""

from pathlib import Path

from PIL import Image, ImageOps

from assets_map import SRC

ROOT = Path(__file__).resolve().parent.parent
image = Image.open(SRC / "Blocs en bois dorés ÉTO étoiles.png").convert("RGB")
ImageOps.fit(image, (1200, 630), Image.LANCZOS).save(ROOT / "public" / "og-image.png", optimize=True)
