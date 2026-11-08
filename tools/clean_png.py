"""Nettoie les PNG de parallaxe et écrit le résultat dans src/assets/parallax/.

Usage : python tools/clean_png.py [slug ...]
Ne modifie jamais les originaux.

Pour chaque image :
  - halo réel (REMBG) : détourage rembg (isnet-general-use), combiné à l'alpha d'origine ;
  - franges (EROSION) : érosion de l'alpha de 1 à 2 px ;
  - toutes : suppression des poussières isolées, décontamination des couleurs de bord,
    recadrage sur l'objet, réduction à 1000 px maximum.
"""

import sys
from pathlib import Path

import numpy as np
from PIL import Image
from scipy import ndimage

from assets_map import MAPPING, source

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "src" / "assets" / "parallax"
MAX_SIDE = 1000
PADDING = 6

# Vrai halo : l'alpha d'origine est inutilisable.
REMBG = {"pousse"}
# KO à l'audit, mais alpha d'origine meilleur que rembg (qui troue le ruban du lapin et
# l'étoile de l'arc-en-ciel) : poussières retirées et érosion seulement.
# Érosion en pixels : 1 px sur la peluche pour préserver le poil.
EROSION = {"pousse": 2, "doudou-lapin": 1, "arc-en-ciel": 2}
# Cubes fournis à part, plus jaunes que la série : teinte alignée sur cube-E (copies du site).
MATCH_TONE = {"cube-M", "cube-A"}
# Hors parallaxe : l'image OG et les logos ne passent pas par ce script.
SKIP = {"blocs-eto", "logo-mame", "logo-mame-sans-contact"}


def rembg_alpha(rgba: Image.Image, session) -> np.ndarray:
    from rembg import remove

    # On aplatit sur un gris neutre : le RVB caché sous la transparence serait trompeur.
    flat = Image.new("RGBA", rgba.size, (128, 128, 128, 255))
    flat.alpha_composite(rgba)
    cut = remove(flat.convert("RGB"), session=session)
    return np.asarray(cut.convert("RGBA"))[..., 3].astype(np.float32)


def despeckle(alpha: np.ndarray) -> np.ndarray:
    """Ne garde que les composantes significatives (les anses d'un hochet restent)."""
    labels, count = ndimage.label(alpha > 12)
    if count <= 1:
        return alpha * (labels > 0)
    sizes = ndimage.sum_labels(np.ones_like(alpha), labels, index=range(1, count + 1))
    keep = np.flatnonzero(sizes >= max(sizes.max() * 0.01, 400)) + 1
    return alpha * np.isin(labels, keep)


def erode(alpha: np.ndarray, px: int) -> np.ndarray:
    eroded = ndimage.grey_erosion(alpha, size=(2 * px + 1, 2 * px + 1))
    return ndimage.gaussian_filter(eroded, 0.6)


def decontaminate(rgb: np.ndarray, alpha: np.ndarray) -> np.ndarray:
    """Les pixels du contour reprennent la couleur de l'objet, 3 px à l'intérieur."""
    solid = alpha >= 250
    if not solid.any():
        return rgb
    core = ndimage.binary_erosion(solid, iterations=3)
    if not core.any():
        core = solid
    idx = ndimage.distance_transform_edt(~core, return_distances=False, return_indices=True)
    out = rgb.copy()
    fix = ~core
    out[fix] = rgb[idx[0][fix], idx[1][fix]]
    return out


def process(name: str, slug: str, session) -> None:
    rgba = Image.open(source(name)).convert("RGBA")
    arr = np.asarray(rgba).astype(np.float32)
    rgb, alpha = arr[..., :3], arr[..., 3]

    if slug in REMBG:
        alpha = np.minimum(alpha, rembg_alpha(rgba, session))
    alpha = despeckle(alpha)
    if slug in EROSION:
        alpha = erode(alpha, EROSION[slug])
        alpha[alpha < 8] = 0
    rgb = decontaminate(rgb, alpha)
    if slug in MATCH_TONE:
        ref = np.asarray(Image.open(OUT / "cube-E.png").convert("RGBA")).astype(np.float32)
        gain = ref[ref[..., 3] > 250][:, :3].mean(axis=0) / rgb[alpha > 250].mean(axis=0)
        rgb = rgb * gain

    ys, xs = np.nonzero(alpha > 8)
    y0, y1 = max(ys.min() - PADDING, 0), min(ys.max() + PADDING + 1, alpha.shape[0])
    x0, x1 = max(xs.min() - PADDING, 0), min(xs.max() + PADDING + 1, alpha.shape[1])

    data = np.dstack([rgb, alpha])[y0:y1, x0:x1]
    result = Image.fromarray(np.clip(data, 0, 255).astype(np.uint8), "RGBA")
    result.thumbnail((MAX_SIDE, MAX_SIDE), Image.LANCZOS)
    result.save(OUT / f"{slug}.png", optimize=True)
    print(f"{slug:16} {'rembg' if slug in REMBG else 'léger':6} {result.size}", flush=True)


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    only = set(sys.argv[1:])
    OUT.mkdir(parents=True, exist_ok=True)
    session = None
    if not only or only & REMBG:
        from rembg import new_session

        session = new_session("isnet-general-use")
    for name, slug in MAPPING.items():
        if slug in SKIP or (only and slug not in only):
            continue
        process(name, slug, session)


if __name__ == "__main__":
    main()
