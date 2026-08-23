"""
Rebuild cover_brain_watermark.png at exact A4 portrait (1240 x 1754 px).

- Crops out corner constellation decorations from source art
- Scales the brain neural mesh to cover the full page (cover fit, no stretch)

Run from repo root:
  python premium_pdf_report/scripts/build_cover_watermark.py
"""

from __future__ import annotations

from pathlib import Path

from PIL import Image

A4_W, A4_H = 1240, 1754
IVORY = (255, 253, 244)

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "assets" / "cover_brain_watermark_source.png"
OUT = ROOT / "assets" / "cover_brain_watermark.png"

# Trim corner clusters from source; keep central brain only
CROP_X = 0.13
CROP_Y = 0.11


def build() -> None:
    if not SOURCE.is_file():
        raise FileNotFoundError(f"Missing source art: {SOURCE}")

    src = Image.open(SOURCE).convert("RGB")
    sw, sh = src.size

    left = int(sw * CROP_X)
    top = int(sh * CROP_Y)
    right = int(sw * (1 - CROP_X))
    bottom = int(sh * (1 - CROP_Y))
    brain = src.crop((left, top, right, bottom))
    bw, bh = brain.size

    # Cover entire A4 (like CSS background-size: cover) — proportional, no squash
    scale = max(A4_W / bw, A4_H / bh)
    nw, nh = int(bw * scale), int(bh * scale)
    scaled = brain.resize((nw, nh), Image.Resampling.LANCZOS)

    page = Image.new("RGB", (A4_W, A4_H), IVORY)
    paste_x = (A4_W - nw) // 2
    paste_y = (A4_H - nh) // 2
    page.paste(scaled, (paste_x, paste_y))

    OUT.parent.mkdir(parents=True, exist_ok=True)
    page.save(OUT, "PNG", optimize=True)
    print(
        f"Wrote {OUT} ({A4_W}x{A4_H}), "
        f"brain crop {bw}x{bh}, scaled {nw}x{nh}, scale={scale:.4f}"
    )


if __name__ == "__main__":
    build()
