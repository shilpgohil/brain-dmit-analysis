"""
Cover page brain neural watermark.

Uses cover_brain_watermark.png (1240x1754, A4 portrait). Rebuild from source art:
  python premium_pdf_report/scripts/build_cover_watermark.py
Source: assets/cover_brain_watermark_source.png (scaled proportionally, never stretched).
"""

from __future__ import annotations

from pathlib import Path

from reportlab.lib.utils import ImageReader

_WATERMARK = Path(__file__).resolve().parent / "assets" / "cover_brain_watermark.png"


def draw_brain_neural_watermark(canvas, page_w: float, page_h: float) -> None:
    """Full-page pale gold brain neural ghost (image asset)."""
    if not _WATERMARK.is_file():
        return

    canvas.saveState()
    img = ImageReader(str(_WATERMARK))
    # Full-bleed A4 asset (1240x1754) — 1:1 page map, no stretch
    canvas.drawImage(
        img,
        0,
        0,
        width=page_w,
        height=page_h,
        preserveAspectRatio=False,
        mask="auto",
    )
    canvas.restoreState()
