"""
Cover page fingerprint watermark.

Uses cover_fingerprint_watermark.png (1024x1536), a single large fingerprint
whorl rendered as very faint gold linework (alpha capped ~23%). Replaces an
earlier full-bleed brain-neural-network graphic that read as too loud/literal
a "brain" image for a dermatoglyphics (fingerprint) report and was dropped
per user feedback. The fingerprint motif is directly on-theme instead.
"""

from __future__ import annotations

from pathlib import Path

from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import ImageReader

_WATERMARK = Path(__file__).resolve().parent / "assets" / "cover_fingerprint_watermark.png"
_HALO = Path(__file__).resolve().parent / "assets" / "cover_monogram_halo.png"

_NAVY = HexColor('#0D1B3E')
_GOLD = HexColor('#C9A441')
_GOLD_LIGHT = HexColor('#E8D5A3')

# Default height of the solid navy "anchor band" across the bottom of the
# cover, used only as a fallback before cover.py computes the real value.
COVER_BAND_HEIGHT = 3.05 * inch

# cover.py measures its own band content (which varies in height depending
# on how many optional candidate fields -- DOB, gender, school -- are
# present) and calls set_band_height() with the exact figure before
# doc.build() runs, so the painted rectangle always matches. Without this,
# a fixed-height rectangle either wasted space (few fields) or let content
# spill above it onto the ivory background (many fields, observed with 5
# candidate fields producing a 3-row grid).
_dynamic_band_height = None


def set_band_height(height: float) -> None:
    global _dynamic_band_height
    _dynamic_band_height = height


# cover.py also computes exactly where the monogram flowable will land
# (centre-x is always the page centre, centre-y depends on the fixed hero
# spacing above it) and registers it here so the halo can be centred under
# it precisely, the same coordination pattern used for the band height.
_monogram_center = None


def set_monogram_center(x: float, y: float) -> None:
    global _monogram_center
    _monogram_center = (x, y)


def draw_fingerprint_watermark(canvas, page_w: float, page_h: float) -> None:
    """Single large, very faint fingerprint whorl centered on the cover page.

    Sized to fit page height (never stretched -- the source is 1024x1536,
    a narrower aspect than A4, so fitting to height and centering
    horizontally shows the true whorl shape instead of distorting it).
    """
    if not _WATERMARK.is_file():
        return

    canvas.saveState()
    img = ImageReader(str(_WATERMARK))
    native_w, native_h = img.getSize()
    draw_h = page_h * 0.95
    draw_w = draw_h * (native_w / native_h)
    x = (page_w - draw_w) / 2
    y = (page_h - draw_h) / 2
    canvas.drawImage(
        img,
        x,
        y,
        width=draw_w,
        height=draw_h,
        preserveAspectRatio=True,
        mask="auto",
    )
    canvas.restoreState()


def draw_monogram_halo(canvas, diameter: float = 2.5 * inch) -> None:
    """
    Soft feathered ivory glow behind the monogram, painted after the
    fingerprint watermark but before the monogram flowable renders on top.

    The monogram's own fine gold linework was visually clashing/merging
    with the fingerprint ridge lines directly behind it (both are thin gold
    strokes at similar scale, so they read as one tangled mess rather than
    a clean logo). A hard-edge circular cutout would fix the clash but look
    like a sticker patched onto the page; this radial gradient (opaque at
    centre, cosine-eased to fully transparent at the edge) clears the
    watermark only in the logo's immediate footprint while blending
    invisibly back into the surrounding pattern everywhere else.
    """
    if not _HALO.is_file() or _monogram_center is None:
        return
    canvas.saveState()
    img = ImageReader(str(_HALO))
    cx, cy = _monogram_center
    canvas.drawImage(
        img,
        cx - diameter / 2,
        cy - diameter / 2,
        width=diameter,
        height=diameter,
        mask="auto",
    )
    canvas.restoreState()


def draw_cover_bottom_band(canvas, page_w: float,
                           band_height: float = None) -> None:
    """
    Solid navy 'anchor band' across the bottom of the cover page.

    The hero content above (title, monogram, watermark) previously left the
    bottom ~40% of the cover completely empty. This band gives the page a
    deliberate, weighted bottom edge (like a boarding-pass stub) and hosts
    the candidate info grid + disclaimer in light text drawn by cover.py's
    flowables on top of it. A gold double-rule marks the seam so it reads
    as an intentional design element rather than a stray colour block.
    """
    if band_height is None:
        band_height = _dynamic_band_height or COVER_BAND_HEIGHT
    canvas.saveState()
    canvas.setFillColor(_NAVY)
    canvas.rect(0, 0, page_w, band_height, stroke=0, fill=1)

    canvas.setStrokeColor(_GOLD)
    canvas.setLineWidth(2.2)
    canvas.line(0, band_height, page_w, band_height)
    canvas.setStrokeColor(_GOLD_LIGHT)
    canvas.setLineWidth(0.6)
    canvas.line(0, band_height - 4, page_w, band_height - 4)
    canvas.restoreState()
