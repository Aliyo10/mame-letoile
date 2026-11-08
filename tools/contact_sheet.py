"""Planche de contrôle : chaque image sur fond ivoire et sur fond encre.

Usage : python tools/contact_sheet.py sortie.png [dossier] [taille_cellule]
Sans dossier, utilise les originaux.
"""

import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from assets_map import MAPPING, source

IVOIRE = (247, 241, 232)
ENCRE = (43, 36, 32)
COLS = 4  # paires ivoire + encre par ligne


def main() -> None:
    out = Path(sys.argv[1])
    folder = Path(sys.argv[2]) if len(sys.argv) > 2 and sys.argv[2] != "-" else None
    cell = int(sys.argv[3]) if len(sys.argv) > 3 else 240
    if folder:
        items = [(p, p.stem) for p in sorted(folder.glob("*.png"))]
    else:
        items = [(source(name), slug) for name, slug in MAPPING.items()]

    label_h = 26
    rows = (len(items) + COLS - 1) // COLS
    sheet = Image.new("RGB", (COLS * cell * 2, rows * (cell + label_h)), "white")
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.truetype("arial.ttf", 16)

    for i, (path, name) in enumerate(items):
        img = Image.open(path).convert("RGBA")
        img.thumbnail((cell - 12, cell - 12), Image.LANCZOS)
        x0 = (i % COLS) * cell * 2
        y0 = (i // COLS) * (cell + label_h)
        for j, bg in enumerate((IVOIRE, ENCRE)):
            tile = Image.new("RGBA", (cell, cell), bg + (255,))
            tile.alpha_composite(img, ((cell - img.width) // 2, (cell - img.height) // 2))
            sheet.paste(tile.convert("RGB"), (x0 + j * cell, y0 + label_h))
        draw.text((x0 + 6, y0 + 4), name, fill="black", font=font)

    out.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(out)
    print(out, sheet.size)


if __name__ == "__main__":
    main()
