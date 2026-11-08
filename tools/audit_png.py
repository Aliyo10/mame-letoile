"""Audit des PNG : canal alpha, part de transparence, couleur des bords, voile, liseré.

Usage : python tools/audit_png.py [dossier]
Sans argument, audite les originaux. Ne modifie aucun fichier.

Colonnes :
  transp%   pixels totalement transparents
  bord op%  anneau extérieur de l'image encore visible
  RGB bords couleur moyenne de cet anneau
  voile%    pixels semi-transparents éloignés (> 8 px) de l'objet : halo diffus
  frange    luminance des pixels semi-transparents du contour / celle de l'objet juste
            à côté. Sous ~0,75, le contour est plus sombre que l'objet : liseré.
"""

import sys
from pathlib import Path

import numpy as np
from PIL import Image
from scipy import ndimage

from assets_map import MAPPING, source

LUMA = np.array([0.2126, 0.7152, 0.0722], dtype=np.float32)


def audit(path: Path) -> dict:
    img = Image.open(path)
    has_alpha = img.mode in ("RGBA", "LA", "PA") or "transparency" in img.info
    arr = np.asarray(img.convert("RGBA")).astype(np.float32)
    rgb, alpha = arr[..., :3], arr[..., 3]
    h, w = alpha.shape

    t = 2  # étroit : les images nettoyées sont recadrées au plus près de l'objet
    ring = np.ones_like(alpha, dtype=bool)
    ring[t:h - t, t:w - t] = False

    transparent = float((alpha < 3).mean() * 100)
    ring_opaque = float((alpha[ring] > 10).mean() * 100)
    ring_rgb = tuple(int(v) for v in rgb[ring].mean(axis=0))

    solid = alpha >= 250
    haze = fringe = float("nan")
    if solid.any() and not solid.all():
        dist = ndimage.distance_transform_edt(~solid)
        semi = (alpha >= 3) & (alpha < 250)
        haze = float((semi & (dist > 8)).mean() * 100)
        lum = rgb @ LUMA
        edge = semi & (dist <= 8) & (alpha >= 40)
        inside = ndimage.distance_transform_edt(solid)
        rim = solid & (inside <= 6)
        if edge.any() and rim.any():
            fringe = float(lum[edge].mean() / max(lum[rim].mean(), 1))

    reasons = []
    if not has_alpha:
        reasons.append("pas d'alpha")
    if transparent < 5:
        reasons.append("fond opaque")
    if ring_opaque > 5:
        reasons.append("bords opaques")
    if haze == haze and haze > 0.25:
        reasons.append("voile")
    if fringe == fringe and fringe < 0.75:
        reasons.append("liseré sombre")

    return dict(size=f"{w}x{h}", alpha=has_alpha, transparent=transparent, ring_opaque=ring_opaque,
                ring_rgb=ring_rgb, haze=haze, fringe=fringe,
                status="KO" if reasons else "OK", reasons=", ".join(reasons))


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    folder = Path(sys.argv[1]) if len(sys.argv) > 1 else None
    paths = sorted(folder.glob("*.png")) if folder else [source(name) for name in MAPPING]
    print(f"{'image':24} {'taille':10} {'alpha':5} {'transp%':>7} {'bord op%':>8} "
          f"{'RGB bords':>15} {'voile%':>7} {'frange':>6}  statut")
    for path in paths:
        r = audit(path)
        name = MAPPING.get(path.name, path.stem)
        print(f"{name:24} {r['size']:10} {'oui' if r['alpha'] else 'non':5} {r['transparent']:7.1f} "
              f"{r['ring_opaque']:8.1f} {str(r['ring_rgb']):>15} {r['haze']:7.2f} {r['fringe']:6.2f}"
              f"  {r['status']} {r['reasons']}")


if __name__ == "__main__":
    main()
