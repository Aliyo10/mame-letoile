"""Détoure le logo fourni sur fond blanc et écrit src/assets/logo/logo.png.

Le fond est repéré par sa couleur : le blanc relié au bord de l'image (le logo est fait de
morceaux séparés, que rembg couperait), plus les grands blancs enfermés, comme l'intérieur
des lettres. Les petits reflets blancs des yeux sont conservés.
"""

from pathlib import Path

import numpy as np
from PIL import Image
from scipy import ndimage

ROOT = Path(__file__).resolve().parent.parent
SOURCE = Path(__file__).resolve().parent / "sources" / "logo-fond-blanc.webp"
OUT = ROOT / "src" / "assets" / "logo" / "logo.png"
WHITE_MIN = 238  # canal minimal à partir duquel un pixel compte comme fond
ENCLOSED_MIN = 120  # surface minimale (px) d'un blanc enfermé considéré comme fond
BAND = 2  # largeur du contour recalculé, en pixels
SIDE = 640


def main() -> None:
    rgb = np.asarray(Image.open(SOURCE).convert("RGB")).astype(np.float32)
    h, w, _ = rgb.shape

    labels, count = ndimage.label(rgb.min(axis=2) >= WHITE_MIN)
    sizes = ndimage.sum_labels(np.ones((h, w)), labels, index=range(1, count + 1))
    border = set(labels[0]) | set(labels[-1]) | set(labels[:, 0]) | set(labels[:, -1])
    keep = [i + 1 for i, size in enumerate(sizes) if i + 1 in border or size >= ENCLOSED_MIN]
    background = np.isin(labels, keep)

    # Contour : opacité déduite du mélange entre le blanc et la couleur pleine la plus proche.
    distance = ndimage.distance_transform_edt(~background)
    solid = ~background & (distance > BAND)
    nearest = ndimage.distance_transform_edt(~solid, return_distances=False, return_indices=True)
    foreground = rgb[nearest[0], nearest[1]]

    alpha = np.ones((h, w), np.float32)
    alpha[background] = 0
    edge = ~background & ~solid
    white = np.array([255, 255, 255], np.float32)
    span = np.linalg.norm(foreground[edge] - white, axis=1)
    alpha[edge] = np.clip(np.linalg.norm(rgb[edge] - white, axis=1) / np.maximum(span, 1), 0, 1)

    colour = rgb.copy()
    colour[edge] = foreground[edge]
    colour[background] = foreground[background]

    data = np.dstack([colour, alpha * 255]).round().astype(np.uint8)
    ys, xs = np.nonzero(data[..., 3] > 8)
    data = data[ys.min():ys.max() + 1, xs.min():xs.max() + 1]

    OUT.parent.mkdir(parents=True, exist_ok=True)
    image = Image.fromarray(data, "RGBA")
    image.thumbnail((SIDE, SIDE), Image.LANCZOS)
    image.save(OUT, optimize=True)
    print(OUT, image.size)


if __name__ == "__main__":
    main()
