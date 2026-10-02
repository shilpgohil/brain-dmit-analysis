"""
Bespoke Boho-Modernist Vector Art Library for DMIT Luxury Report.
All illustrations are 100% native vector graphics (ReportLab Drawing / Path / Line / Circle).
Zero external bitmap dependencies, zero raster pixelation, zero layout shift (CLS = 0).
Colors strictly mirror the DMIT luxury editorial palette.
"""
from __future__ import annotations

import math
from reportlab.graphics.shapes import (
    Drawing, Group, Circle, Line, Rect, Path, Polygon, PolyLine, String, Ellipse
)
from reportlab.lib.colors import HexColor

# ── Luxury Palette Tokens ───────────────────────────────────────────────────
NAVY_C  = HexColor("#0D1B3E")
GOLD_C  = HexColor("#D4AF37")
GOLD_LT = HexColor("#E8D5A3")
GOLD_PL = HexColor("#F5EBD0")
TERRA_C = HexColor("#C46849")
SAGE_C  = HexColor("#5A7865")
SAND_C  = HexColor("#E5D3B3")
CHAR_C  = HexColor("#1F2937")
IVORY_C = HexColor("#FFFDF4")


# ── 1. SWOT Quadrant Vector Badges (Pages 11–14) ───────────────────────────

def draw_boho_swot_badge(letter: str, width: float = 64, height: float = 64) -> Drawing:
    """
    Renders an artisanal Boho emblem for each SWOT quadrant:
      S (Strengths): Rising sun with fine golden rays over a solid Roman keystone arch.
      W (Weaknesses): Zen cairn of 4 smooth river balancing stones in equilibrium.
      O (Opportunities): Arched portal opening to distant horizon ridges & 8-point star.
      T (Threats): Concentric sacred nautilus shell with a protective grounded core.
    """
    d = Drawing(width, height)
    cx, cy = width / 2.0, height / 2.0

    if letter.upper() == "S":
        # Warm Sandstone Arch
        p_arch = Path(fillColor=SAND_C, strokeColor=NAVY_C, strokeWidth=0.8)
        p_arch.moveTo(cx - 24, cy - 26)
        p_arch.lineTo(cx - 24, cy + 4)
        p_arch.curveTo(cx - 24, cy + 26, cx + 24, cy + 26, cx + 24, cy + 4)
        p_arch.lineTo(cx + 24, cy - 26)
        p_arch.closePath()
        d.add(p_arch)

        # Rising Terracotta Sun
        d.add(Circle(cx, cy - 8, 14, fillColor=TERRA_C, strokeColor=None))

        # Fine Golden Sun Rays
        for deg in (25, 50, 75, 90, 105, 130, 155):
            rad = math.radians(deg)
            r1, r2 = 16.0, 23.0
            x1 = cx + r1 * math.cos(rad)
            y1 = (cy - 8) + r1 * math.sin(rad)
            x2 = cx + r2 * math.cos(rad)
            y2 = (cy - 8) + r2 * math.sin(rad)
            d.add(Line(x1, y1, x2, y2, strokeColor=GOLD_C, strokeWidth=1.0))

        # Keystone Baseline
        d.add(Line(cx - 26, cy - 26, cx + 26, cy - 26, strokeColor=NAVY_C, strokeWidth=1.2))

    elif letter.upper() == "W":
        # Balanced Zen Stones Cairn (Self-awareness, equilibrium, inner grounding)
        d.add(Line(cx, cy - 26, cx, cy + 24, strokeColor=GOLD_LT, strokeWidth=0.6))  # plumb-line

        # Base Stone (Terracotta)
        d.add(Ellipse(cx, cy - 20, 22, 6, fillColor=TERRA_C, strokeColor=NAVY_C, strokeWidth=0.7))
        # Second Stone (Sandstone)
        d.add(Ellipse(cx, cy - 10, 17, 5, fillColor=SAND_C, strokeColor=NAVY_C, strokeWidth=0.7))
        # Third Stone (Sage)
        d.add(Ellipse(cx + 1, cy - 1, 12, 4.5, fillColor=SAGE_C, strokeColor=NAVY_C, strokeWidth=0.7))
        # Keystone Top Pebble (Gold)
        d.add(Ellipse(cx, cy + 7, 7, 3.5, fillColor=GOLD_C, strokeColor=NAVY_C, strokeWidth=0.7))
        # Zen Accent Star at Apex
        d.add(Circle(cx, cy + 18, 1.5, fillColor=GOLD_C, strokeColor=None))

    elif letter.upper() == "O":
        # Arched Portal to Expanding Horizon
        p_outer = Path(fillColor=GOLD_PL, strokeColor=GOLD_C, strokeWidth=0.8)
        p_outer.moveTo(cx - 22, cy - 26)
        p_outer.lineTo(cx - 22, cy + 6)
        p_outer.curveTo(cx - 22, cy + 26, cx + 22, cy + 26, cx + 22, cy + 6)
        p_outer.lineTo(cx + 22, cy - 26)
        p_outer.closePath()
        d.add(p_outer)

        p_inner = Path(fillColor=IVORY_C, strokeColor=NAVY_C, strokeWidth=0.8)
        p_inner.moveTo(cx - 16, cy - 26)
        p_inner.lineTo(cx - 16, cy + 4)
        p_inner.curveTo(cx - 16, cy + 20, cx + 16, cy + 20, cx + 16, cy + 4)
        p_inner.lineTo(cx + 16, cy - 26)
        p_inner.closePath()
        d.add(p_inner)

        # Distant Horizon Arc
        p_hill = Path(fillColor=SAGE_C, strokeColor=None)
        p_hill.moveTo(cx - 16, cy - 26)
        p_hill.curveTo(cx - 8, cy - 18, cx + 8, cy - 18, cx + 16, cy - 26)
        p_hill.closePath()
        d.add(p_hill)

        # 8-Point Guiding Star in Portal Apex
        star_y = cy + 10
        d.add(Line(cx - 5, star_y, cx + 5, star_y, strokeColor=GOLD_C, strokeWidth=1.0))
        d.add(Line(cx, star_y - 5, cx, star_y + 5, strokeColor=GOLD_C, strokeWidth=1.0))
        d.add(Line(cx - 3, star_y - 3, cx + 3, star_y + 3, strokeColor=GOLD_C, strokeWidth=0.6))
        d.add(Line(cx - 3, star_y + 3, cx + 3, star_y - 3, strokeColor=GOLD_C, strokeWidth=0.6))
        d.add(Circle(cx, star_y, 1.2, fillColor=GOLD_C, strokeColor=None))

    elif letter.upper() == "T":
        # Protective Sacred Shield / Concentric Nautilus Arcs
        for r, col, sw in ((24, GOLD_LT, 0.6), (19, SAND_C, 0.8), (14, GOLD_C, 1.0)):
            p_shell = Path(fillColor=None, strokeColor=col, strokeWidth=sw)
            p_shell.moveTo(cx - r, cy - 16)
            p_shell.curveTo(cx - r, cy + r * 0.8, cx + r, cy + r * 0.8, cx + r, cy - 16)
            d.add(p_shell)

        # Grounded Central Pearl / Core
        d.add(Circle(cx, cy - 8, 8, fillColor=NAVY_C, strokeColor=GOLD_C, strokeWidth=1.0))
        d.add(Circle(cx, cy - 8, 3, fillColor=TERRA_C, strokeColor=None))

        # Triangular Shield Baseline
        d.add(Line(cx - 26, cy - 20, cx + 26, cy - 20, strokeColor=NAVY_C, strokeWidth=1.2))
        d.add(Line(cx, cy - 26, cx, cy - 20, strokeColor=GOLD_C, strokeWidth=1.2))

    return d


# ── 2. Legal Notarial Seal (Page 7) ─────────────────────────────────────────

def draw_boho_legal_seal(width: float = 460, height: float = 48) -> Drawing:
    """
    Artisanal Legal Endorsement Emblem for Page 7.
    Features twin laurel sprigs, balance scales of justice, and concentric golden rings.
    """
    d = Drawing(width, height)
    cx, cy = width / 2.0, 28.0

    # Horizontal delicate connecting rules
    d.add(Line(40, cy, cx - 55, cy, strokeColor=GOLD_LT, strokeWidth=0.7))
    d.add(Line(cx + 55, cy, width - 40, cy, strokeColor=GOLD_LT, strokeWidth=0.7))
    d.add(Circle(40, cy, 2, fillColor=GOLD_C, strokeColor=None))
    d.add(Circle(width - 40, cy, 2, fillColor=GOLD_C, strokeColor=None))

    # Concentric Medallion Rings
    d.add(Circle(cx, cy, 14, fillColor=IVORY_C, strokeColor=GOLD_C, strokeWidth=0.9))
    d.add(Circle(cx, cy, 11, fillColor=None, strokeColor=GOLD_LT, strokeWidth=0.5))
    d.add(Circle(cx, cy, 9.5, fillColor=GOLD_PL, strokeColor=None))

    # Central Scales of Balance / Truth
    # Vertical Mast
    d.add(Line(cx, cy - 7, cx, cy + 6, strokeColor=NAVY_C, strokeWidth=1.0))
    d.add(Circle(cx, cy + 6, 1.2, fillColor=GOLD_C, strokeColor=None))
    # Horizontal Beam
    d.add(Line(cx - 6, cy + 2.5, cx + 6, cy + 2.5, strokeColor=NAVY_C, strokeWidth=0.8))
    # Left Pan
    d.add(Line(cx - 6, cy + 2.5, cx - 8, cy - 2, strokeColor=GOLD_C, strokeWidth=0.5))
    d.add(Line(cx - 6, cy + 2.5, cx - 4, cy - 2, strokeColor=GOLD_C, strokeWidth=0.5))
    d.add(Line(cx - 9, cy - 2, cx - 3, cy - 2, strokeColor=NAVY_C, strokeWidth=0.7))
    # Right Pan
    d.add(Line(cx + 6, cy + 2.5, cx + 4, cy - 2, strokeColor=GOLD_C, strokeWidth=0.5))
    d.add(Line(cx + 6, cy + 2.5, cx + 8, cy - 2, strokeColor=GOLD_C, strokeWidth=0.5))
    d.add(Line(cx + 3, cy - 2, cx + 9, cy - 2, strokeColor=NAVY_C, strokeWidth=0.7))
    # Base
    d.add(Line(cx - 5, cy - 7, cx + 5, cy - 7, strokeColor=NAVY_C, strokeWidth=1.0))

    # Symmetrical Botanical Laurel Sprigs
    for side in (-1, 1):
        for deg in (25, 60, 95, 130, 165):
            rad = math.radians(deg)
            r = 18.0
            lx = cx + side * (r * math.sin(rad))
            ly = cy + (r * 0.7 * math.cos(rad))
            d.add(Circle(lx, ly, 1.2, fillColor=SAGE_C, strokeColor=None))

    # Inscribed Tiny Subtext cleanly below the medallion
    d.add(String(cx - 82, 5.0, "EPHEMERAL BIOMETRIC INTEGRITY  —  ZERO DATA STORAGE",
                 fontName="Times-Italic", fontSize=5.5, fillColor=HexColor("#64748B")))
    return d


# ── 3. Volar Pad & Neural Synchrony Triptych (Page 8) ──────────────────────

def draw_boho_embryo_seedling(width: float = 460, height: float = 60) -> Drawing:
    """
    Artisanal Developmental Vignette for Page 8 (Science & Historical Foundations).
    Illustrates the synchronous embryonic morphogenesis of volar pads and cerebral neocortex.
    """
    d = Drawing(width, height)
    cy = height / 2.0 - 4

    # Baseline connecting axis
    d.add(Line(30, cy, width - 30, cy, strokeColor=GOLD_LT, strokeWidth=0.8))

    nodes = [
        (80, "WEEK 10–13", "Volar Pad Emergence", SAND_C),
        (230, "WEEK 13–19", "Primary Ridge Budding", TERRA_C),
        (380, "WEEK 24+", "Neural Invariance", SAGE_C),
    ]

    for nx, stage_tag, stage_desc, fill_c in nodes:
        # Base Plinth
        d.add(Circle(nx, cy, 3, fillColor=NAVY_C, strokeColor=None))

        # Vertical stem
        d.add(Line(nx, cy, nx, cy + 18, strokeColor=GOLD_C, strokeWidth=1.0))

        if "10" in stage_tag:
            # Embryonic smooth arch
            p = Path(fillColor=fill_c, strokeColor=NAVY_C, strokeWidth=0.7)
            p.moveTo(nx - 10, cy + 18)
            p.curveTo(nx - 10, cy + 30, nx + 10, cy + 30, nx + 10, cy + 18)
            p.closePath()
            d.add(p)
        elif "13" in stage_tag:
            # Concentric ridge arcs
            for r in (5, 9, 13):
                p = Path(fillColor=None, strokeColor=GOLD_C if r == 9 else fill_c, strokeWidth=0.8)
                p.moveTo(nx - r, cy + 18)
                p.curveTo(nx - r, cy + 18 + r * 1.1, nx + r, cy + 18 + r * 1.1, nx + r, cy + 18)
                d.add(p)
        else:
            # Blooming Seedling / Neural Arbor
            d.add(Circle(nx, cy + 22, 6, fillColor=fill_c, strokeColor=NAVY_C, strokeWidth=0.7))
            # Twin leaves
            d.add(Ellipse(nx - 8, cy + 25, 4, 2, fillColor=SAGE_C, strokeColor=None))
            d.add(Ellipse(nx + 8, cy + 25, 4, 2, fillColor=SAGE_C, strokeColor=None))
            # Apex star
            d.add(Circle(nx, cy + 31, 1.2, fillColor=GOLD_C, strokeColor=None))

        # Labels
        d.add(String(nx - 22, cy - 10, stage_tag, fontName="Times-Bold", fontSize=7, fillColor=NAVY_C))
        d.add(String(nx - 36, cy - 18, stage_desc, fontName="Times-Roman", fontSize=6.5, fillColor=HexColor("#475569")))

    return d


# ── 4. Academic & Somatic Harmony Balance (Page 20) ─────────────────────────

def draw_boho_academic_somatic_balance(width: float = 460, height: float = 70) -> Drawing:
    """
    Bespoke Triptych for Page 20 (Intellectual vs Somatic Performance).
    Harmonizes intellectual focus (compass/quill) with somatic agility (kinetic arc).
    """
    d = Drawing(width, height)
    cx, cy = width / 2.0, height / 2.0 - 2

    # Central Balance Fulcrum
    p_fulcrum = Path(fillColor=NAVY_C, strokeColor=None)
    p_fulcrum.moveTo(cx - 10, cy - 14)
    p_fulcrum.lineTo(cx, cy + 4)
    p_fulcrum.lineTo(cx + 10, cy - 14)
    p_fulcrum.closePath()
    d.add(p_fulcrum)
    d.add(Circle(cx, cy + 4, 2.5, fillColor=GOLD_C, strokeColor=None))

    # Horizontal Balance Beam
    d.add(Line(cx - 90, cy + 4, cx + 90, cy + 4, strokeColor=GOLD_C, strokeWidth=1.2))

    # Plumb line
    d.add(Line(cx, cy - 14, cx, cy - 20, strokeColor=NAVY_C, strokeWidth=0.8))
    d.add(Circle(cx, cy - 21, 1.5, fillColor=GOLD_C, strokeColor=None))

    # ── Left Side: Intellectual / Academic Focus ──
    lx = cx - 80
    d.add(Line(lx, cy + 4, lx, cy - 8, strokeColor=GOLD_LT, strokeWidth=0.8))
    # Roman Keystone Arch
    p_arch = Path(fillColor=SAND_C, strokeColor=NAVY_C, strokeWidth=0.8)
    p_arch.moveTo(lx - 16, cy - 20)
    p_arch.lineTo(lx - 16, cy - 8)
    p_arch.curveTo(lx - 16, cy + 6, lx + 16, cy + 6, lx + 16, cy - 8)
    p_arch.lineTo(lx + 16, cy - 20)
    p_arch.closePath()
    d.add(p_arch)
    # Quill / Compass Star inside
    d.add(Line(lx - 6, cy - 7, lx + 6, cy - 7, strokeColor=GOLD_C, strokeWidth=0.8))
    d.add(Line(lx, cy - 13, lx, cy - 1, strokeColor=GOLD_C, strokeWidth=0.8))
    d.add(Circle(lx, cy - 7, 1.2, fillColor=TERRA_C, strokeColor=None))
    d.add(String(lx - 34, cy - 29, "INTELLECTUAL COGNITION", fontName="Times-Bold", fontSize=6.5, fillColor=NAVY_C))

    # ── Right Side: Physical / Somatic Agility ──
    rx = cx + 80
    d.add(Line(rx, cy + 4, rx, cy - 8, strokeColor=GOLD_LT, strokeWidth=0.8))
    # Kinetic Dynamic Arcs (Athleticism, somatosensory motor control)
    for r, col, sw in ((16, SAGE_C, 1.2), (12, TERRA_C, 0.9), (8, GOLD_C, 0.7)):
        p_wave = Path(fillColor=None, strokeColor=col, strokeWidth=sw)
        p_wave.moveTo(rx - r, cy - 8)
        p_wave.curveTo(rx - r * 0.5, cy - 8 + r * 0.8, rx + r * 0.5, cy - 8 - r * 0.8, rx + r, cy - 8)
        d.add(p_wave)
    d.add(Circle(rx, cy - 8, 2, fillColor=NAVY_C, strokeColor=None))
    d.add(String(rx - 28, cy - 29, "SOMATIC KINESTHETICS", fontName="Times-Bold", fontSize=6.5, fillColor=NAVY_C))

    return d


# ── 5. VAK Sensory Modality Vector Badges (Pages 23–25) ─────────────────────

def draw_boho_sensory_badge(modality: str, width: float = 64, height: float = 64) -> Drawing:
    """
    Bespoke sensory emblems for VAK Learning Style pages:
      Visual: Optical refractive prism casting golden spectral rays.
      Auditory: Fibonacci acoustic nautilus shell with sound wave whorls.
      Kinesthetic: Fluid continuous-stroke kinetic lemniscate (infinity motion).
    """
    d = Drawing(width, height)
    cx, cy = width / 2.0, height / 2.0

    if modality.lower() == "visual":
        # Background Ivory Circle with Gold rim
        d.add(Circle(cx, cy, 26, fillColor=GOLD_PL, strokeColor=GOLD_C, strokeWidth=0.8))
        # Refractive Triangular Prism
        p_prism = Path(fillColor=SAND_C, strokeColor=NAVY_C, strokeWidth=1.0)
        p_prism.moveTo(cx, cy + 16)
        p_prism.lineTo(cx - 16, cy - 12)
        p_prism.lineTo(cx + 16, cy - 12)
        p_prism.closePath()
        d.add(p_prism)
        # Radiant Refracted Beams
        for deg in (-25, 0, 25):
            rad = math.radians(deg)
            d.add(Line(cx, cy + 2, cx + 22 * math.cos(rad), (cy + 2) + 22 * math.sin(rad),
                       strokeColor=TERRA_C if deg == 0 else GOLD_C, strokeWidth=0.9))
        d.add(Circle(cx, cy + 2, 2.5, fillColor=NAVY_C, strokeColor=None))

    elif modality.lower() == "auditory":
        # Background Soft Sandstone Circle
        d.add(Circle(cx, cy, 26, fillColor=GOLD_PL, strokeColor=GOLD_C, strokeWidth=0.8))
        # Fibonacci Acoustic Spiral (Auditory Cochlea)
        for r, col in ((18, SAGE_C), (14, GOLD_C), (10, TERRA_C), (6, NAVY_C)):
            p_arc = Path(fillColor=None, strokeColor=col, strokeWidth=1.0)
            p_arc.moveTo(cx - r, cy)
            p_arc.curveTo(cx - r, cy + r * 1.1, cx + r, cy + r * 1.1, cx + r, cy)
            p_arc.curveTo(cx + r, cy - r * 0.9, cx - r * 0.6, cy - r * 0.9, cx - r * 0.6, cy)
            d.add(p_arc)
        d.add(Circle(cx, cy, 2, fillColor=GOLD_C, strokeColor=None))

    elif modality.lower() == "kinesthetic":
        # Background Ivory Circle
        d.add(Circle(cx, cy, 26, fillColor=GOLD_PL, strokeColor=GOLD_C, strokeWidth=0.8))
        # Kinetic Motion Figure / Dynamic Lemniscate
        d.add(Ellipse(cx - 9, cy, 8, 14, fillColor=None, strokeColor=TERRA_C, strokeWidth=1.1))
        d.add(Ellipse(cx + 9, cy, 8, 14, fillColor=None, strokeColor=SAGE_C, strokeWidth=1.1))
        d.add(Circle(cx, cy, 3, fillColor=NAVY_C, strokeColor=GOLD_C, strokeWidth=0.8))
        # Tangent Directional Arcs
        d.add(Line(cx - 16, cy + 14, cx + 16, cy - 14, strokeColor=GOLD_C, strokeWidth=0.8))
        d.add(Circle(cx + 16, cy - 14, 1.5, fillColor=TERRA_C, strokeColor=None))

    return d


# ── 6. Career Pilgrimage Pathway (Page 43) ──────────────────────────────────

def draw_boho_career_journey(width: float = 460, height: float = 55) -> Drawing:
    """
    Bespoke Vocational Journey Vignette for Page 43 (Career Pathways Intro).
    Illustrates a winding organic path traversing rolling hills toward a celestial north star.
    """
    d = Drawing(width, height)
    cx, cy = width / 2.0, height / 2.0

    # Rolling Hill Contours (Sandstone & Sage)
    p_hill1 = Path(fillColor=SAND_C, strokeColor=None)
    p_hill1.moveTo(20, cy - 18)
    p_hill1.curveTo(120, cy + 6, 220, cy - 10, 320, cy - 18)
    p_hill1.lineTo(20, cy - 18)
    p_hill1.closePath()
    d.add(p_hill1)

    p_hill2 = Path(fillColor=GOLD_PL, strokeColor=None)
    p_hill2.moveTo(180, cy - 18)
    p_hill2.curveTo(280, cy + 12, 380, cy - 4, 440, cy - 18)
    p_hill2.lineTo(180, cy - 18)
    p_hill2.closePath()
    d.add(p_hill2)

    # Winding Organic Pilgrimage Path (Continuous gold hairline)
    p_path = Path(fillColor=None, strokeColor=GOLD_C, strokeWidth=1.4)
    p_path.moveTo(30, cy - 18)
    p_path.curveTo(100, cy - 4, 160, cy - 14, 230, cy - 2)
    p_path.curveTo(300, cy + 10, 360, cy - 6, 420, cy + 14)
    d.add(p_path)

    # Waypoint Stations
    for wx, wy in ((100, cy - 6), (230, cy - 2), (360, cy + 3)):
        d.add(Circle(wx, wy, 2, fillColor=NAVY_C, strokeColor=GOLD_C, strokeWidth=0.8))

    # Celestial Guiding North Star at Destination
    star_x, star_y = 420, cy + 14
    d.add(Line(star_x - 6, star_y, star_x + 6, star_y, strokeColor=GOLD_C, strokeWidth=1.1))
    d.add(Line(star_x, star_y - 6, star_x, star_y + 6, strokeColor=GOLD_C, strokeWidth=1.1))
    d.add(Line(star_x - 3.5, star_y - 3.5, star_x + 3.5, star_y + 3.5, strokeColor=GOLD_C, strokeWidth=0.7))
    d.add(Line(star_x - 3.5, star_y + 3.5, star_x + 3.5, star_y - 3.5, strokeColor=GOLD_C, strokeWidth=0.7))
    d.add(Circle(star_x, star_y, 1.8, fillColor=TERRA_C, strokeColor=None))

    d.add(String(cx - 75, cy - 24, "THE VOCATIONAL PILGRIMAGE  —  INNATE APTITUDE REALIZATION",
                 fontName="Times-Italic", fontSize=6.5, fillColor=HexColor("#64748B")))
    return d


# ── 7. Counseling Signature Seal (Page 60) ──────────────────────────────────

def draw_boho_counseling_seal(width: float = 460, height: float = 45) -> Drawing:
    """
    Subtle closing seal arch framing the signature block on Page 60.
    """
    d = Drawing(width, height)
    cx, cy = width / 2.0, height / 2.0

    # Delicate framing baseline with central medallion arch
    d.add(Line(40, cy, cx - 60, cy, strokeColor=GOLD_LT, strokeWidth=0.8))
    d.add(Line(cx + 60, cy, width - 40, cy, strokeColor=GOLD_LT, strokeWidth=0.8))
    d.add(Circle(40, cy, 2, fillColor=GOLD_C, strokeColor=None))
    d.add(Circle(width - 40, cy, 2, fillColor=GOLD_C, strokeColor=None))

    # Central Medallion
    d.add(Circle(cx, cy, 18, fillColor=GOLD_PL, strokeColor=GOLD_C, strokeWidth=0.9))
    d.add(Circle(cx, cy, 15, fillColor=IVORY_C, strokeColor=GOLD_LT, strokeWidth=0.5))

    # Wax Seal Monogram / Olive sprig
    d.add(Line(cx, cy - 10, cx, cy + 10, strokeColor=NAVY_C, strokeWidth=0.8))
    for dy in (-5, 0, 5):
        d.add(Line(cx, cy + dy, cx - 4, cy + dy + 3, strokeColor=SAGE_C, strokeWidth=0.7))
        d.add(Line(cx, cy + dy, cx + 4, cy + dy + 3, strokeColor=SAGE_C, strokeWidth=0.7))

    d.add(String(cx - 82, cy - 18, "VERIFIED CONSULTATION SIGN-OFF  —  ETHICAL COMPLIANCE",
                 fontName="Times-Bold", fontSize=6, fillColor=GOLD_C))
    return d


# ── 8. Profiler Accreditation Wax Seal (Page 2) ────────────────────────────

def draw_boho_wax_seal(width: float = 48, height: float = 48) -> Drawing:
    """
    Artisanal accreditation wax seal for Page 2.
    Concentric gold/navy rings with delicate stippled perimeter and central star.
    """
    d = Drawing(width, height)
    cx, cy = width / 2.0, height / 2.0

    d.add(Circle(cx, cy, 22, fillColor=GOLD_PL, strokeColor=GOLD_C, strokeWidth=1.0))
    d.add(Circle(cx, cy, 18, fillColor=IVORY_C, strokeColor=GOLD_LT, strokeWidth=0.6))
    d.add(Circle(cx, cy, 14, fillColor=None, strokeColor=NAVY_C, strokeWidth=0.8))

    # Fine perimeter stippling
    for deg in range(0, 360, 30):
        rad = math.radians(deg)
        x = cx + 20 * math.cos(rad)
        y = cy + 20 * math.sin(rad)
        d.add(Circle(x, y, 0.8, fillColor=GOLD_C, strokeColor=None))

    # Central 8-Point Star
    d.add(Line(cx - 6, cy, cx + 6, cy, strokeColor=GOLD_C, strokeWidth=1.0))
    d.add(Line(cx, cy - 6, cx, cy + 6, strokeColor=GOLD_C, strokeWidth=1.0))
    d.add(Line(cx - 3.5, cy - 3.5, cx + 3.5, cy + 3.5, strokeColor=NAVY_C, strokeWidth=0.7))
    d.add(Line(cx - 3.5, cy + 3.5, cx + 3.5, cy - 3.5, strokeColor=NAVY_C, strokeWidth=0.7))
    d.add(Circle(cx, cy, 1.5, fillColor=TERRA_C, strokeColor=None))

    return d

