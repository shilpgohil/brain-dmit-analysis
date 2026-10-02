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
NAVY_C  = HexColor("#0D1B3E")
GOLD_C  = HexColor("#D4AF37")
GOLD_LT = HexColor("#E8D5A3")
GOLD_PL = HexColor("#F5EBD0")
TERRA_C = HexColor("#C46849")
SAGE_C  = HexColor("#5A7865")
SAND_C  = HexColor("#E5D3B3")
CHAR_C  = HexColor("#1F2937")
IVORY_C = HexColor("#FFFDF4")
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
        p_arch = Path(fillColor=SAND_C, strokeColor=NAVY_C, strokeWidth=0.8)
        p_arch.moveTo(cx - 24, cy - 26)
        p_arch.lineTo(cx - 24, cy + 4)
        p_arch.curveTo(cx - 24, cy + 26, cx + 24, cy + 26, cx + 24, cy + 4)
        p_arch.lineTo(cx + 24, cy - 26)
        p_arch.closePath()
        d.add(p_arch)
        d.add(Circle(cx, cy - 8, 14, fillColor=TERRA_C, strokeColor=None))
        for deg in (25, 50, 75, 90, 105, 130, 155):
            rad = math.radians(deg)
            r1, r2 = 16.0, 23.0
            x1 = cx + r1 * math.cos(rad)
            y1 = (cy - 8) + r1 * math.sin(rad)
            x2 = cx + r2 * math.cos(rad)
            y2 = (cy - 8) + r2 * math.sin(rad)
            d.add(Line(x1, y1, x2, y2, strokeColor=GOLD_C, strokeWidth=1.0))
        d.add(Line(cx - 26, cy - 26, cx + 26, cy - 26, strokeColor=NAVY_C, strokeWidth=1.2))
    elif letter.upper() == "W":
        d.add(Line(cx, cy - 26, cx, cy + 24, strokeColor=GOLD_LT, strokeWidth=0.6))              
        d.add(Ellipse(cx, cy - 20, 22, 6, fillColor=TERRA_C, strokeColor=NAVY_C, strokeWidth=0.7))
        d.add(Ellipse(cx, cy - 10, 17, 5, fillColor=SAND_C, strokeColor=NAVY_C, strokeWidth=0.7))
        d.add(Ellipse(cx + 1, cy - 1, 12, 4.5, fillColor=SAGE_C, strokeColor=NAVY_C, strokeWidth=0.7))
        d.add(Ellipse(cx, cy + 7, 7, 3.5, fillColor=GOLD_C, strokeColor=NAVY_C, strokeWidth=0.7))
        d.add(Circle(cx, cy + 18, 1.5, fillColor=GOLD_C, strokeColor=None))
    elif letter.upper() == "O":
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
        p_hill = Path(fillColor=SAGE_C, strokeColor=None)
        p_hill.moveTo(cx - 16, cy - 26)
        p_hill.curveTo(cx - 8, cy - 18, cx + 8, cy - 18, cx + 16, cy - 26)
        p_hill.closePath()
        d.add(p_hill)
        star_y = cy + 10
        d.add(Line(cx - 5, star_y, cx + 5, star_y, strokeColor=GOLD_C, strokeWidth=1.0))
        d.add(Line(cx, star_y - 5, cx, star_y + 5, strokeColor=GOLD_C, strokeWidth=1.0))
        d.add(Line(cx - 3, star_y - 3, cx + 3, star_y + 3, strokeColor=GOLD_C, strokeWidth=0.6))
        d.add(Line(cx - 3, star_y + 3, cx + 3, star_y - 3, strokeColor=GOLD_C, strokeWidth=0.6))
        d.add(Circle(cx, star_y, 1.2, fillColor=GOLD_C, strokeColor=None))
    elif letter.upper() == "T":
        for r, col, sw in ((24, GOLD_LT, 0.6), (19, SAND_C, 0.8), (14, GOLD_C, 1.0)):
            p_shell = Path(fillColor=None, strokeColor=col, strokeWidth=sw)
            p_shell.moveTo(cx - r, cy - 16)
            p_shell.curveTo(cx - r, cy + r * 0.8, cx + r, cy + r * 0.8, cx + r, cy - 16)
            d.add(p_shell)
        d.add(Circle(cx, cy - 8, 8, fillColor=NAVY_C, strokeColor=GOLD_C, strokeWidth=1.0))
        d.add(Circle(cx, cy - 8, 3, fillColor=TERRA_C, strokeColor=None))
        d.add(Line(cx - 26, cy - 20, cx + 26, cy - 20, strokeColor=NAVY_C, strokeWidth=1.2))
        d.add(Line(cx, cy - 26, cx, cy - 20, strokeColor=GOLD_C, strokeWidth=1.2))
    return d
def draw_boho_legal_seal(width: float = 460, height: float = 48) -> Drawing:
    """
    Artisanal Legal Endorsement Emblem for Page 7.
    Features twin laurel sprigs, balance scales of justice, and concentric golden rings.
    """
    d = Drawing(width, height)
    cx, cy = width / 2.0, 28.0
    d.add(Line(40, cy, cx - 55, cy, strokeColor=GOLD_LT, strokeWidth=0.7))
    d.add(Line(cx + 55, cy, width - 40, cy, strokeColor=GOLD_LT, strokeWidth=0.7))
    d.add(Circle(40, cy, 2, fillColor=GOLD_C, strokeColor=None))
    d.add(Circle(width - 40, cy, 2, fillColor=GOLD_C, strokeColor=None))
    d.add(Circle(cx, cy, 14, fillColor=IVORY_C, strokeColor=GOLD_C, strokeWidth=0.9))
    d.add(Circle(cx, cy, 11, fillColor=None, strokeColor=GOLD_LT, strokeWidth=0.5))
    d.add(Circle(cx, cy, 9.5, fillColor=GOLD_PL, strokeColor=None))
    d.add(Line(cx, cy - 7, cx, cy + 6, strokeColor=NAVY_C, strokeWidth=1.0))
    d.add(Circle(cx, cy + 6, 1.2, fillColor=GOLD_C, strokeColor=None))
    d.add(Line(cx - 6, cy + 2.5, cx + 6, cy + 2.5, strokeColor=NAVY_C, strokeWidth=0.8))
    d.add(Line(cx - 6, cy + 2.5, cx - 8, cy - 2, strokeColor=GOLD_C, strokeWidth=0.5))
    d.add(Line(cx - 6, cy + 2.5, cx - 4, cy - 2, strokeColor=GOLD_C, strokeWidth=0.5))
    d.add(Line(cx - 9, cy - 2, cx - 3, cy - 2, strokeColor=NAVY_C, strokeWidth=0.7))
    d.add(Line(cx + 6, cy + 2.5, cx + 4, cy - 2, strokeColor=GOLD_C, strokeWidth=0.5))
    d.add(Line(cx + 6, cy + 2.5, cx + 8, cy - 2, strokeColor=GOLD_C, strokeWidth=0.5))
    d.add(Line(cx + 3, cy - 2, cx + 9, cy - 2, strokeColor=NAVY_C, strokeWidth=0.7))
    d.add(Line(cx - 5, cy - 7, cx + 5, cy - 7, strokeColor=NAVY_C, strokeWidth=1.0))
    for side in (-1, 1):
        for deg in (25, 60, 95, 130, 165):
            rad = math.radians(deg)
            r = 18.0
            lx = cx + side * (r * math.sin(rad))
            ly = cy + (r * 0.7 * math.cos(rad))
            d.add(Circle(lx, ly, 1.2, fillColor=SAGE_C, strokeColor=None))
    d.add(String(cx - 82, 5.0, "EPHEMERAL BIOMETRIC INTEGRITY  —  ZERO DATA STORAGE",
                 fontName="Times-Italic", fontSize=5.5, fillColor=HexColor("#64748B")))
    return d
def draw_boho_embryo_seedling(width: float = 460, height: float = 60) -> Drawing:
    """
    Artisanal Developmental Vignette for Page 8 (Science & Historical Foundations).
    Illustrates the synchronous embryonic morphogenesis of volar pads and cerebral neocortex.
    """
    d = Drawing(width, height)
    cy = height / 2.0 - 4
    d.add(Line(30, cy, width - 30, cy, strokeColor=GOLD_LT, strokeWidth=0.8))
    nodes = [
        (80, "WEEK 10–13", "Volar Pad Emergence", SAND_C),
        (230, "WEEK 13–19", "Primary Ridge Budding", TERRA_C),
        (380, "WEEK 24+", "Neural Invariance", SAGE_C),
    ]
    for nx, stage_tag, stage_desc, fill_c in nodes:
        d.add(Circle(nx, cy, 3, fillColor=NAVY_C, strokeColor=None))
        d.add(Line(nx, cy, nx, cy + 18, strokeColor=GOLD_C, strokeWidth=1.0))
        if "10" in stage_tag:
            p = Path(fillColor=fill_c, strokeColor=NAVY_C, strokeWidth=0.7)
            p.moveTo(nx - 10, cy + 18)
            p.curveTo(nx - 10, cy + 30, nx + 10, cy + 30, nx + 10, cy + 18)
            p.closePath()
            d.add(p)
        elif "13" in stage_tag:
            for r in (5, 9, 13):
                p = Path(fillColor=None, strokeColor=GOLD_C if r == 9 else fill_c, strokeWidth=0.8)
                p.moveTo(nx - r, cy + 18)
                p.curveTo(nx - r, cy + 18 + r * 1.1, nx + r, cy + 18 + r * 1.1, nx + r, cy + 18)
                d.add(p)
        else:
            d.add(Circle(nx, cy + 22, 6, fillColor=fill_c, strokeColor=NAVY_C, strokeWidth=0.7))
            d.add(Ellipse(nx - 8, cy + 25, 4, 2, fillColor=SAGE_C, strokeColor=None))
            d.add(Ellipse(nx + 8, cy + 25, 4, 2, fillColor=SAGE_C, strokeColor=None))
            d.add(Circle(nx, cy + 31, 1.2, fillColor=GOLD_C, strokeColor=None))
        d.add(String(nx - 22, cy - 10, stage_tag, fontName="Times-Bold", fontSize=7, fillColor=NAVY_C))
        d.add(String(nx - 36, cy - 18, stage_desc, fontName="Times-Roman", fontSize=6.5, fillColor=HexColor("#475569")))
    return d
def draw_boho_academic_somatic_balance(width: float = 460, height: float = 70) -> Drawing:
    """
    Bespoke Triptych for Page 20 (Intellectual vs Somatic Performance).
    Harmonizes intellectual focus (compass/quill) with somatic agility (kinetic arc).
    """
    d = Drawing(width, height)
    cx, cy = width / 2.0, height / 2.0 - 2
    p_fulcrum = Path(fillColor=NAVY_C, strokeColor=None)
    p_fulcrum.moveTo(cx - 10, cy - 14)
    p_fulcrum.lineTo(cx, cy + 4)
    p_fulcrum.lineTo(cx + 10, cy - 14)
    p_fulcrum.closePath()
    d.add(p_fulcrum)
    d.add(Circle(cx, cy + 4, 2.5, fillColor=GOLD_C, strokeColor=None))
    d.add(Line(cx - 90, cy + 4, cx + 90, cy + 4, strokeColor=GOLD_C, strokeWidth=1.2))
    d.add(Line(cx, cy - 14, cx, cy - 20, strokeColor=NAVY_C, strokeWidth=0.8))
    d.add(Circle(cx, cy - 21, 1.5, fillColor=GOLD_C, strokeColor=None))
    lx = cx - 80
    d.add(Line(lx, cy + 4, lx, cy - 8, strokeColor=GOLD_LT, strokeWidth=0.8))
    p_arch = Path(fillColor=SAND_C, strokeColor=NAVY_C, strokeWidth=0.8)
    p_arch.moveTo(lx - 16, cy - 20)
    p_arch.lineTo(lx - 16, cy - 8)
    p_arch.curveTo(lx - 16, cy + 6, lx + 16, cy + 6, lx + 16, cy - 8)
    p_arch.lineTo(lx + 16, cy - 20)
    p_arch.closePath()
    d.add(p_arch)
    d.add(Line(lx - 6, cy - 7, lx + 6, cy - 7, strokeColor=GOLD_C, strokeWidth=0.8))
    d.add(Line(lx, cy - 13, lx, cy - 1, strokeColor=GOLD_C, strokeWidth=0.8))
    d.add(Circle(lx, cy - 7, 1.2, fillColor=TERRA_C, strokeColor=None))
    d.add(String(lx - 34, cy - 29, "INTELLECTUAL COGNITION", fontName="Times-Bold", fontSize=6.5, fillColor=NAVY_C))
    rx = cx + 80
    d.add(Line(rx, cy + 4, rx, cy - 8, strokeColor=GOLD_LT, strokeWidth=0.8))
    for r, col, sw in ((16, SAGE_C, 1.2), (12, TERRA_C, 0.9), (8, GOLD_C, 0.7)):
        p_wave = Path(fillColor=None, strokeColor=col, strokeWidth=sw)
        p_wave.moveTo(rx - r, cy - 8)
        p_wave.curveTo(rx - r * 0.5, cy - 8 + r * 0.8, rx + r * 0.5, cy - 8 - r * 0.8, rx + r, cy - 8)
        d.add(p_wave)
    d.add(Circle(rx, cy - 8, 2, fillColor=NAVY_C, strokeColor=None))
    d.add(String(rx - 28, cy - 29, "SOMATIC KINESTHETICS", fontName="Times-Bold", fontSize=6.5, fillColor=NAVY_C))
    return d
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
        d.add(Circle(cx, cy, 26, fillColor=GOLD_PL, strokeColor=GOLD_C, strokeWidth=0.8))
        p_prism = Path(fillColor=SAND_C, strokeColor=NAVY_C, strokeWidth=1.0)
        p_prism.moveTo(cx, cy + 16)
        p_prism.lineTo(cx - 16, cy - 12)
        p_prism.lineTo(cx + 16, cy - 12)
        p_prism.closePath()
        d.add(p_prism)
        for deg in (-25, 0, 25):
            rad = math.radians(deg)
            d.add(Line(cx, cy + 2, cx + 22 * math.cos(rad), (cy + 2) + 22 * math.sin(rad),
                       strokeColor=TERRA_C if deg == 0 else GOLD_C, strokeWidth=0.9))
        d.add(Circle(cx, cy + 2, 2.5, fillColor=NAVY_C, strokeColor=None))
    elif modality.lower() == "auditory":
        d.add(Circle(cx, cy, 26, fillColor=GOLD_PL, strokeColor=GOLD_C, strokeWidth=0.8))
        for r, col in ((18, SAGE_C), (14, GOLD_C), (10, TERRA_C), (6, NAVY_C)):
            p_arc = Path(fillColor=None, strokeColor=col, strokeWidth=1.0)
            p_arc.moveTo(cx - r, cy)
            p_arc.curveTo(cx - r, cy + r * 1.1, cx + r, cy + r * 1.1, cx + r, cy)
            p_arc.curveTo(cx + r, cy - r * 0.9, cx - r * 0.6, cy - r * 0.9, cx - r * 0.6, cy)
            d.add(p_arc)
        d.add(Circle(cx, cy, 2, fillColor=GOLD_C, strokeColor=None))
    elif modality.lower() == "kinesthetic":
        d.add(Circle(cx, cy, 26, fillColor=GOLD_PL, strokeColor=GOLD_C, strokeWidth=0.8))
        d.add(Ellipse(cx - 9, cy, 8, 14, fillColor=None, strokeColor=TERRA_C, strokeWidth=1.1))
        d.add(Ellipse(cx + 9, cy, 8, 14, fillColor=None, strokeColor=SAGE_C, strokeWidth=1.1))
        d.add(Circle(cx, cy, 3, fillColor=NAVY_C, strokeColor=GOLD_C, strokeWidth=0.8))
        d.add(Line(cx - 16, cy + 14, cx + 16, cy - 14, strokeColor=GOLD_C, strokeWidth=0.8))
        d.add(Circle(cx + 16, cy - 14, 1.5, fillColor=TERRA_C, strokeColor=None))
    return d
def draw_boho_career_journey(width: float = 460, height: float = 55) -> Drawing:
    """
    Bespoke Vocational Journey Vignette for Page 43 (Career Pathways Intro).
    Illustrates a winding organic path traversing rolling hills toward a celestial north star.
    """
    d = Drawing(width, height)
    cx, cy = width / 2.0, height / 2.0
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
    p_path = Path(fillColor=None, strokeColor=GOLD_C, strokeWidth=1.4)
    p_path.moveTo(30, cy - 18)
    p_path.curveTo(100, cy - 4, 160, cy - 14, 230, cy - 2)
    p_path.curveTo(300, cy + 10, 360, cy - 6, 420, cy + 14)
    d.add(p_path)
    for wx, wy in ((100, cy - 6), (230, cy - 2), (360, cy + 3)):
        d.add(Circle(wx, wy, 2, fillColor=NAVY_C, strokeColor=GOLD_C, strokeWidth=0.8))
    star_x, star_y = 420, cy + 14
    d.add(Line(star_x - 6, star_y, star_x + 6, star_y, strokeColor=GOLD_C, strokeWidth=1.1))
    d.add(Line(star_x, star_y - 6, star_x, star_y + 6, strokeColor=GOLD_C, strokeWidth=1.1))
    d.add(Line(star_x - 3.5, star_y - 3.5, star_x + 3.5, star_y + 3.5, strokeColor=GOLD_C, strokeWidth=0.7))
    d.add(Line(star_x - 3.5, star_y + 3.5, star_x + 3.5, star_y - 3.5, strokeColor=GOLD_C, strokeWidth=0.7))
    d.add(Circle(star_x, star_y, 1.8, fillColor=TERRA_C, strokeColor=None))
    d.add(String(cx - 75, cy - 24, "THE VOCATIONAL PILGRIMAGE  —  INNATE APTITUDE REALIZATION",
                 fontName="Times-Italic", fontSize=6.5, fillColor=HexColor("#64748B")))
    return d
def draw_boho_counseling_seal(width: float = 460, height: float = 52) -> Drawing:
    """
    Subtle closing seal arch framing the signature block on Page 60.
    Engineered with strict vertical zoning so text and graphics NEVER collide.
    """
    d = Drawing(width, height)
    cx = width / 2.0
    cy = height - 18.0
    d.add(Line(40, cy, cx - 36, cy, strokeColor=GOLD_LT, strokeWidth=0.8))
    d.add(Line(cx + 36, cy, width - 40, cy, strokeColor=GOLD_LT, strokeWidth=0.8))
    d.add(Circle(40, cy, 2, fillColor=GOLD_C, strokeColor=None))
    d.add(Circle(width - 40, cy, 2, fillColor=GOLD_C, strokeColor=None))
    d.add(Circle(cx, cy, 14, fillColor=GOLD_PL, strokeColor=GOLD_C, strokeWidth=0.9))
    d.add(Circle(cx, cy, 11, fillColor=IVORY_C, strokeColor=GOLD_LT, strokeWidth=0.5))
    d.add(Line(cx, cy - 7, cx, cy + 7, strokeColor=NAVY_C, strokeWidth=0.8))
    for dy in (-3.5, 0, 3.5):
        d.add(Line(cx, cy + dy, cx - 3.2, cy + dy + 2.2, strokeColor=SAGE_C, strokeWidth=0.7))
        d.add(Line(cx, cy + dy, cx + 3.2, cy + dy + 2.2, strokeColor=SAGE_C, strokeWidth=0.7))
    d.add(String(cx - 96, 4, "VERIFIED CONSULTATION SIGN-OFF  —  ETHICAL COMPLIANCE",
                 fontName="Times-Bold", fontSize=6.5, fillColor=GOLD_C))
    return d
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
    for deg in range(0, 360, 30):
        rad = math.radians(deg)
        x = cx + 20 * math.cos(rad)
        y = cy + 20 * math.sin(rad)
        d.add(Circle(x, y, 0.8, fillColor=GOLD_C, strokeColor=None))
    d.add(Line(cx - 6, cy, cx + 6, cy, strokeColor=GOLD_C, strokeWidth=1.0))
    d.add(Line(cx, cy - 6, cx, cy + 6, strokeColor=GOLD_C, strokeWidth=1.0))
    d.add(Line(cx - 3.5, cy - 3.5, cx + 3.5, cy + 3.5, strokeColor=NAVY_C, strokeWidth=0.7))
    d.add(Line(cx - 3.5, cy + 3.5, cx + 3.5, cy - 3.5, strokeColor=NAVY_C, strokeWidth=0.7))
    d.add(Circle(cx, cy, 1.5, fillColor=TERRA_C, strokeColor=None))
    return d
def draw_boho_learning_visual(width: float = 460, height: float = 110) -> Drawing:
    d = Drawing(width, height)
    cx, cy = width / 2.0, height / 2.0 + 4
    p_arch = Path(fillColor=SAND_C, strokeColor=NAVY_C, strokeWidth=0.8)
    p_arch.moveTo(cx - 50, cy - 35)
    p_arch.lineTo(cx - 50, cy + 10)
    p_arch.curveTo(cx - 50, cy + 45, cx + 50, cy + 45, cx + 50, cy + 10)
    p_arch.lineTo(cx + 50, cy - 35)
    p_arch.closePath()
    d.add(p_arch)
    p_sun = Path(fillColor=TERRA_C, strokeColor=None)
    p_sun.moveTo(cx - 36, cy - 10)
    p_sun.curveTo(cx - 36, cy + 26, cx + 36, cy + 26, cx + 36, cy - 10)
    p_sun.closePath()
    d.add(p_sun)
    for deg in range(30, 155, 18):
        rad = math.radians(deg)
        r1, r2 = 38.0, 48.0
        x1, y1 = cx + r1 * math.cos(rad), (cy - 10) + r1 * math.sin(rad)
        x2, y2 = cx + r2 * math.cos(rad), (cy - 10) + r2 * math.sin(rad)
        d.add(Line(x1, y1, x2, y2, strokeColor=GOLD_C, strokeWidth=1.0))
    p_eye = Path(fillColor=IVORY_C, strokeColor=NAVY_C, strokeWidth=1.1)
    p_eye.moveTo(cx - 24, cy - 10)
    p_eye.curveTo(cx - 12, cy + 8, cx + 12, cy + 8, cx + 24, cy - 10)
    p_eye.curveTo(cx + 12, cy - 22, cx - 12, cy - 22, cx - 24, cy - 10)
    p_eye.closePath()
    d.add(p_eye)
    d.add(Circle(cx, cy - 10, 7, fillColor=NAVY_C, strokeColor=None))
    d.add(Circle(cx, cy - 10, 3, fillColor=GOLD_C, strokeColor=None))
    branch_points = [
        (-80, cy + 15, -45, cy + 8, SAGE_C),
        (-95, cy - 10, -50, cy - 12, TERRA_C),
        (-75, cy - 28, -48, cy - 25, GOLD_C),
        (80, cy + 15, 45, cy + 8, SAGE_C),
        (95, cy - 10, 50, cy - 12, TERRA_C),
        (75, cy - 28, 48, cy - 25, GOLD_C),
    ]
    for x_end, y_end, x_start, y_start, col in branch_points:
        d.add(Line(cx + x_start, y_start, cx + x_end, y_end, strokeColor=GOLD_LT, strokeWidth=0.8))
        d.add(Circle(cx + x_end, y_end, 3.5, fillColor=col, strokeColor=NAVY_C, strokeWidth=0.6))
    for deg in range(0, 185, 12):
        rad = math.radians(deg)
        ox = cx + 125 * math.cos(rad)
        oy = (cy - 30) + 60 * math.sin(rad)
        d.add(Circle(ox, oy, 0.7, fillColor=GOLD_C, strokeColor=None))
    d.add(String(cx - 110, cy - 44, "SPATIAL MENTAL RETRIEVAL  &  CHROMATIC MIND MAPPING",
                 fontName="Times-Italic", fontSize=6.5, fillColor=HexColor("#64748B")))
    return d
def draw_boho_learning_auditory(width: float = 460, height: float = 110) -> Drawing:
    d = Drawing(width, height)
    cx, cy = width / 2.0, height / 2.0 + 4
    p_bg = Path(fillColor=GOLD_PL, strokeColor=None)
    p_bg.moveTo(cx - 60, cy - 35)
    p_bg.curveTo(cx - 60, cy + 40, cx + 60, cy + 40, cx + 60, cy - 35)
    p_bg.closePath()
    d.add(p_bg)
    for wave_col, amp, y_off in ((SAGE_C, 12, 10), (TERRA_C, 16, -2), (GOLD_C, 10, -14)):
        p_wave = Path(fillColor=None, strokeColor=wave_col, strokeWidth=1.2)
        p_wave.moveTo(cx - 130, cy + y_off)
        p_wave.curveTo(cx - 65, cy + y_off + amp, cx - 35, cy + y_off - amp, cx, cy + y_off)
        p_wave.curveTo(cx + 35, cy + y_off + amp, cx + 65, cy + y_off - amp, cx + 130, cy + y_off)
        d.add(p_wave)
    p_lyre = Path(fillColor=IVORY_C, strokeColor=NAVY_C, strokeWidth=1.2)
    p_lyre.moveTo(cx - 18, cy + 24)
    p_lyre.lineTo(cx - 18, cy - 4)
    p_lyre.curveTo(cx - 18, cy - 24, cx + 18, cy - 24, cx + 18, cy - 4)
    p_lyre.lineTo(cx + 18, cy + 24)
    p_lyre.closePath()
    d.add(p_lyre)
    for sx in (-10, -5, 0, 5, 10):
        d.add(Line(cx + sx, cy - 14, cx + sx, cy + 22, strokeColor=GOLD_C, strokeWidth=0.8))
    d.add(Circle(cx - 18, cy + 24, 2.5, fillColor=GOLD_C, strokeColor=NAVY_C, strokeWidth=0.6))
    d.add(Circle(cx + 18, cy + 24, 2.5, fillColor=GOLD_C, strokeColor=NAVY_C, strokeWidth=0.6))
    for rx in (-40, -55, 40, 55):
        d.add(Circle(cx + rx, cy, 1.5, fillColor=TERRA_C, strokeColor=None))
    d.add(String(cx - 105, cy - 44, "PHONETIC CADENCE  &  AUDITORY WORKING MEMORY",
                 fontName="Times-Italic", fontSize=6.5, fillColor=HexColor("#64748B")))
    return d
def draw_boho_learning_kinesthetic(width: float = 460, height: float = 110) -> Drawing:
    d = Drawing(width, height)
    cx, cy = width / 2.0, height / 2.0 + 4
    d.add(Ellipse(cx, cy - 30, 36, 7, fillColor=SAND_C, strokeColor=NAVY_C, strokeWidth=0.8))
    d.add(Ellipse(cx + 4, cy - 20, 26, 6, fillColor=TERRA_C, strokeColor=NAVY_C, strokeWidth=0.8))
    d.add(Ellipse(cx - 2, cy - 11, 16, 5, fillColor=SAGE_C, strokeColor=NAVY_C, strokeWidth=0.8))
    for sw, sc in ((28, GOLD_C), (20, SAGE_C), (12, TERRA_C)):
        p_kin = Path(fillColor=None, strokeColor=sc, strokeWidth=1.1)
        p_kin.moveTo(cx - 80, cy - 8)
        p_kin.curveTo(cx - 40, cy + sw, cx + 40, cy - sw, cx + 80, cy + 18)
        d.add(p_kin)
    p_hand = Path(fillColor=IVORY_C, strokeColor=NAVY_C, strokeWidth=1.3)
    p_hand.moveTo(cx - 12, cy - 10)
    p_hand.curveTo(cx - 22, cy + 12, cx - 18, cy + 28, cx - 6, cy + 32)
    p_hand.curveTo(cx + 6, cy + 32, cx + 18, cy + 26, cx + 14, cy + 10)
    p_hand.curveTo(cx + 10, cy - 4, cx + 2, cy - 10, cx - 12, cy - 10)
    p_hand.closePath()
    d.add(p_hand)
    for deg in range(0, 540, 15):
        rad = math.radians(deg)
        r = 1.0 + 0.024 * deg
        x = (cx - 2) + r * math.cos(rad)
        y = (cy + 12) + r * math.sin(rad)
        d.add(Circle(x, y, 0.7, fillColor=GOLD_C, strokeColor=None))
    d.add(String(cx - 110, cy - 44, "SOMATOSENSORY DEXTERITY  &  KINETIC MOTOR MEMORY",
                 fontName="Times-Italic", fontSize=6.5, fillColor=HexColor("#64748B")))
    return d
def draw_boho_habits_vision(width: float = 460, height: float = 120) -> Drawing:
    d = Drawing(width, height)
    cx, cy = width / 2.0, height / 2.0 + 4
    d.add(Rect(cx - 60, cy - 42, 120, 6, fillColor=SAND_C, strokeColor=NAVY_C, strokeWidth=0.8))
    d.add(Rect(cx - 46, cy - 36, 92, 5, fillColor=GOLD_PL, strokeColor=NAVY_C, strokeWidth=0.8))
    p_arch = Path(fillColor=IVORY_C, strokeColor=NAVY_C, strokeWidth=1.1)
    p_arch.moveTo(cx - 36, cy - 31)
    p_arch.lineTo(cx - 36, cy + 12)
    p_arch.curveTo(cx - 36, cy + 42, cx + 36, cy + 42, cx + 36, cy + 12)
    p_arch.lineTo(cx + 36, cy - 31)
    p_arch.closePath()
    d.add(p_arch)
    p_sun = Path(fillColor=TERRA_C, strokeColor=None)
    p_sun.moveTo(cx - 26, cy - 4)
    p_sun.curveTo(cx - 26, cy + 22, cx + 26, cy + 22, cx + 26, cy - 4)
    p_sun.closePath()
    d.add(p_sun)
    d.add(Line(cx - 14, cy - 31, cx, cy - 4, strokeColor=GOLD_C, strokeWidth=1.0))
    d.add(Line(cx + 14, cy - 31, cx, cy - 4, strokeColor=GOLD_C, strokeWidth=1.0))
    star_x, star_y = cx, cy + 22
    d.add(Line(star_x - 8, star_y, star_x + 8, star_y, strokeColor=GOLD_C, strokeWidth=1.2))
    d.add(Line(star_x, star_y - 8, star_x, star_y + 8, strokeColor=GOLD_C, strokeWidth=1.2))
    d.add(Line(star_x - 5, star_y - 5, star_x + 5, star_y + 5, strokeColor=NAVY_C, strokeWidth=0.7))
    d.add(Line(star_x - 5, star_y + 5, star_x + 5, star_y - 5, strokeColor=NAVY_C, strokeWidth=0.7))
    d.add(Circle(star_x, star_y, 2, fillColor=GOLD_C, strokeColor=None))
    for sign in (-1, 1):
        for dy in (-15, 0, 15):
            d.add(Ellipse(cx + sign * 55, cy + dy, 4.5, 2, fillColor=SAGE_C, strokeColor=NAVY_C, strokeWidth=0.5))
    d.add(String(cx - 125, cy - 52, "PROACTIVE INITIATIVE  &  LONG-TERM TELEOLOGICAL PURPOSE",
                 fontName="Times-Italic", fontSize=6.5, fillColor=HexColor("#64748B")))
    return d
def draw_boho_habits_synergy(width: float = 460, height: float = 120) -> Drawing:
    d = Drawing(width, height)
    cx, cy = width / 2.0, height / 2.0 + 4
    p_arch1 = Path(fillColor=SAND_C, strokeColor=NAVY_C, strokeWidth=0.9)
    p_arch1.moveTo(cx - 52, cy - 30)
    p_arch1.lineTo(cx - 52, cy + 8)
    p_arch1.curveTo(cx - 52, cy + 36, cx - 4, cy + 36, cx - 4, cy + 8)
    p_arch1.lineTo(cx - 4, cy - 30)
    p_arch1.closePath()
    d.add(p_arch1)
    p_arch2 = Path(fillColor=GOLD_PL, strokeColor=NAVY_C, strokeWidth=0.9)
    p_arch2.moveTo(cx + 4, cy - 30)
    p_arch2.lineTo(cx + 4, cy + 8)
    p_arch2.curveTo(cx + 4, cy + 36, cx + 52, cy + 36, cx + 52, cy + 8)
    p_arch2.lineTo(cx + 52, cy - 30)
    p_arch2.closePath()
    d.add(p_arch2)
    p_key = Path(fillColor=GOLD_C, strokeColor=NAVY_C, strokeWidth=1.0)
    p_key.moveTo(cx - 10, cy + 18)
    p_key.lineTo(cx - 6, cy + 38)
    p_key.lineTo(cx + 6, cy + 38)
    p_key.lineTo(cx + 10, cy + 18)
    p_key.closePath()
    d.add(p_key)
    d.add(Line(cx - 65, cy - 10, cx + 65, cy - 10, strokeColor=NAVY_C, strokeWidth=1.3))
    d.add(Circle(cx, cy - 10, 3, fillColor=GOLD_C, strokeColor=None))
    for pan_x in (cx - 55, cx + 55):
        d.add(Line(pan_x, cy - 10, pan_x, cy - 22, strokeColor=GOLD_LT, strokeWidth=0.8))
        d.add(Ellipse(pan_x, cy - 22, 12, 3.5, fillColor=TERRA_C, strokeColor=NAVY_C, strokeWidth=0.7))
    d.add(String(cx - 128, cy - 52, "QUADRANT II PRIORITIZATION  &  MUTUAL PSYCHOLOGICAL SAFETY",
                 fontName="Times-Italic", fontSize=6.5, fillColor=HexColor("#64748B")))
    return d
def draw_boho_habits_empathy(width: float = 460, height: float = 120) -> Drawing:
    d = Drawing(width, height)
    cx, cy = width / 2.0, height / 2.0 + 4
    p_stream_l = Path(fillColor=None, strokeColor=NAVY_C, strokeWidth=1.4)
    p_stream_l.moveTo(cx - 85, cy - 35)
    p_stream_l.curveTo(cx - 50, cy - 30, cx - 35, cy - 10, cx, cy + 2)
    d.add(p_stream_l)
    p_stream_r = Path(fillColor=None, strokeColor=TERRA_C, strokeWidth=1.4)
    p_stream_r.moveTo(cx + 85, cy - 35)
    p_stream_r.curveTo(cx + 50, cy - 30, cx + 35, cy - 10, cx, cy + 2)
    d.add(p_stream_r)
    d.add(Line(cx, cy + 2, cx, cy + 22, strokeColor=GOLD_C, strokeWidth=1.6))
    d.add(Circle(cx, cy + 28, 16, fillColor=SAGE_C, strokeColor=NAVY_C, strokeWidth=0.8))
    d.add(Circle(cx - 10, cy + 24, 11, fillColor=GOLD_PL, strokeColor=NAVY_C, strokeWidth=0.7))
    d.add(Circle(cx + 10, cy + 24, 11, fillColor=SAND_C, strokeColor=NAVY_C, strokeWidth=0.7))
    d.add(Circle(cx, cy + 34, 10, fillColor=IVORY_C, strokeColor=GOLD_C, strokeWidth=0.8))
    for fx, fy in ((cx - 8, cy + 28), (cx + 8, cy + 28), (cx, cy + 35), (cx - 4, cy + 20), (cx + 4, cy + 20)):
        d.add(Circle(fx, fy, 2, fillColor=GOLD_C, strokeColor=None))
    d.add(String(cx - 130, cy - 52, "SOCRATIC ACTIVE LISTENING  &  CREATIVE COLLABORATIVE SYNTHESIS",
                 fontName="Times-Italic", fontSize=6.5, fillColor=HexColor("#64748B")))
    return d
def draw_boho_habits_renewal(width: float = 460, height: float = 130) -> Drawing:
    d = Drawing(width, height)
    cx, cy = width / 2.0, height / 2.0 + 4
    for deg in range(0, 360, 10):
        rad = math.radians(deg)
        d.add(Circle(cx + 46 * math.cos(rad), cy + 46 * math.sin(rad), 0.75, fillColor=GOLD_C, strokeColor=None))
    d.add(Circle(cx, cy, 40, fillColor=IVORY_C, strokeColor=NAVY_C, strokeWidth=1.0))
    quads = [
        (cx - 16, cy + 16, SAGE_C, "Physical"),
        (cx + 16, cy + 16, TERRA_C, "Mental"),
        (cx - 16, cy - 16, GOLD_C, "Emotional"),
        (cx + 16, cy - 16, SAND_C, "Spiritual"),
    ]
    for qx, qy, col, _lbl in quads:
        d.add(Circle(qx, qy, 11, fillColor=col, strokeColor=NAVY_C, strokeWidth=0.6))
    d.add(Circle(cx, cy, 9, fillColor=GOLD_C, strokeColor=NAVY_C, strokeWidth=0.8))
    d.add(Circle(cx, cy, 4, fillColor=IVORY_C, strokeColor=None))
    d.add(Line(cx - 36, cy, cx + 36, cy, strokeColor=GOLD_LT, strokeWidth=0.6))
    d.add(Line(cx, cy - 36, cx, cy + 36, strokeColor=GOLD_LT, strokeWidth=0.6))
    d.add(String(cx - 135, cy - 54, "HOLISTIC RENEWAL OF PHYSICAL, COGNITIVE & EMOTIONAL EQUILIBRIUM",
                 fontName="Times-Italic", fontSize=6.5, fillColor=HexColor("#64748B")))
    return d
def draw_boho_leadership_alignment(width: float = 460, height: float = 110) -> Drawing:
    d = Drawing(width, height)
    cx, cy = width / 2.0, height / 2.0 + 4
    d.add(Line(cx - 95, cy, cx + 95, cy, strokeColor=GOLD_LT, strokeWidth=0.8))
    d.add(Circle(cx - 95, cy, 2, fillColor=GOLD_C, strokeColor=None))
    d.add(Circle(cx + 95, cy, 2, fillColor=GOLD_C, strokeColor=None))
    lx = cx - 55
    d.add(Rect(lx - 18, cy - 18, 36, 36, fillColor=SAND_C, strokeColor=NAVY_C, strokeWidth=0.8))
    for grid_y in (-9, 0, 9):
        d.add(Line(lx - 16, cy + grid_y, lx + 16, cy + grid_y, strokeColor=IVORY_C, strokeWidth=0.6))
    d.add(Circle(lx, cy, 3, fillColor=NAVY_C, strokeColor=None))
    d.add(String(lx - 20, cy - 28, "TASK RIGOR", fontName="Times-Bold", fontSize=6.5, fillColor=NAVY_C))
    rx = cx + 55
    d.add(Circle(rx, cy, 18, fillColor=GOLD_PL, strokeColor=GOLD_C, strokeWidth=0.8))
    for deg in (30, 90, 150, 210, 270, 330):
        rad = math.radians(deg)
        d.add(Ellipse(rx + 15 * math.cos(rad), cy + 15 * math.sin(rad), 4, 2, fillColor=SAGE_C, strokeColor=None))
    d.add(Circle(rx, cy, 4, fillColor=TERRA_C, strokeColor=None))
    d.add(String(rx - 25, cy - 28, "PEOPLE EMPATHY", fontName="Times-Bold", fontSize=6.5, fillColor=NAVY_C))
    d.add(Circle(cx, cy, 4, fillColor=GOLD_C, strokeColor=NAVY_C, strokeWidth=0.7))
    d.add(String(cx - 145, cy - 44, "BALANCED EXECUTIVE STEWARDSHIP: RIGOROUS EXECUTION & EMPATHETIC CULTURE",
                 fontName="Times-Italic", fontSize=6.5, fillColor=HexColor("#64748B")))
    return d
def draw_boho_cognitive_processing(width: float = 460, height: float = 110) -> Drawing:
    d = Drawing(width, height)
    cx, cy = width / 2.0, height / 2.0 + 4
    d.add(Circle(cx, cy + 30, 3, fillColor=GOLD_C, strokeColor=NAVY_C, strokeWidth=0.8))
    d.add(Line(cx, cy + 30, cx, cy - 10, strokeColor=GOLD_LT, strokeWidth=0.8))
    d.add(Circle(cx, cy - 10, 5, fillColor=TERRA_C, strokeColor=NAVY_C, strokeWidth=0.8))
    lx = cx - 60
    p_cube = Path(fillColor=NAVY_C, strokeColor=GOLD_C, strokeWidth=0.8)
    p_cube.moveTo(lx - 20, cy - 15)
    p_cube.lineTo(lx, cy - 25)
    p_cube.lineTo(lx + 20, cy - 15)
    p_cube.lineTo(lx, cy - 5)
    p_cube.closePath()
    d.add(p_cube)
    d.add(String(lx - 26, cy - 35, "ANALYSIS TANK", fontName="Times-Bold", fontSize=6.5, fillColor=NAVY_C))
    rx = cx + 60
    p_wave = Path(fillColor=None, strokeColor=TERRA_C, strokeWidth=1.4)
    p_wave.moveTo(rx - 25, cy - 18)
    p_wave.curveTo(rx - 10, cy, rx + 10, cy - 25, rx + 25, cy - 10)
    d.add(p_wave)
    d.add(Line(rx + 25, cy - 10, rx + 18, cy - 8, strokeColor=TERRA_C, strokeWidth=1.4))
    d.add(Line(rx + 25, cy - 10, rx + 20, cy - 16, strokeColor=TERRA_C, strokeWidth=1.4))
    d.add(Circle(rx - 25, cy - 18, 2.5, fillColor=SAGE_C, strokeColor=None))
    d.add(String(rx - 24, cy - 35, "ACTION CATALYST", fontName="Times-Bold", fontSize=6.5, fillColor=NAVY_C))
    d.add(String(cx - 145, cy - 48, "PRE-COMPUTATIONAL SCENARIO MODELING & RAPID IMPLEMENTATION CADENCE",
                 fontName="Times-Italic", fontSize=6.5, fillColor=HexColor("#64748B")))
    return d
def draw_boho_collaboration_dynamics(width: float = 460, height: float = 120) -> Drawing:
    d = Drawing(width, height)
    cx, cy = width / 2.0, height / 2.0 + 4
    col_w, col_h = 16, 42
    lx = cx - 60
    d.add(Rect(lx - col_w/2, cy - 25, col_w, col_h, fillColor=SAND_C, strokeColor=NAVY_C, strokeWidth=0.8))
    d.add(Rect(lx - col_w/2 - 3, cy + 17, col_w + 6, 4, fillColor=GOLD_C, strokeColor=NAVY_C, strokeWidth=0.7))
    d.add(Rect(lx - col_w/2 - 3, cy - 29, col_w + 6, 4, fillColor=GOLD_C, strokeColor=NAVY_C, strokeWidth=0.7))
    d.add(String(lx - 25, cy - 39, "DIRECTING LEAD", fontName="Times-Bold", fontSize=6.5, fillColor=NAVY_C))
    rx = cx + 60
    d.add(Rect(rx - col_w/2, cy - 25, col_w, col_h, fillColor=GOLD_PL, strokeColor=NAVY_C, strokeWidth=0.8))
    d.add(Rect(rx - col_w/2 - 3, cy + 17, col_w + 6, 4, fillColor=SAGE_C, strokeColor=NAVY_C, strokeWidth=0.7))
    d.add(Rect(rx - col_w/2 - 3, cy - 29, col_w + 6, 4, fillColor=SAGE_C, strokeColor=NAVY_C, strokeWidth=0.7))
    d.add(String(rx - 26, cy - 39, "SUPPORTING PILLAR", fontName="Times-Bold", fontSize=6.5, fillColor=NAVY_C))
    p_arch = Path(fillColor=None, strokeColor=GOLD_C, strokeWidth=1.2)
    p_arch.moveTo(lx, cy + 21)
    p_arch.curveTo(lx, cy + 48, rx, cy + 48, rx, cy + 21)
    d.add(p_arch)
    d.add(Circle(cx, cy + 42, 8, fillColor=IVORY_C, strokeColor=GOLD_C, strokeWidth=0.9))
    d.add(Circle(cx, cy + 42, 4, fillColor=TERRA_C, strokeColor=None))
    d.add(String(cx - 135, cy - 52, "AUTONOMOUS SQUAD GOVERNANCE & CROSS-FUNCTIONAL COHESION",
                 fontName="Times-Italic", fontSize=6.5, fillColor=HexColor("#64748B")))
    return d
def draw_boho_behavioral_ambition(width: float = 460, height: float = 120) -> Drawing:
    d = Drawing(width, height)
    cx, cy = width / 2.0, height / 2.0 + 4
    d.add(Rect(cx - 60, cy - 36, 120, 6, fillColor=SAND_C, strokeColor=NAVY_C, strokeWidth=0.8))
    d.add(Rect(cx - 42, cy - 30, 84, 5, fillColor=GOLD_PL, strokeColor=NAVY_C, strokeWidth=0.8))
    d.add(Rect(cx - 24, cy - 25, 48, 5, fillColor=IVORY_C, strokeColor=NAVY_C, strokeWidth=0.8))
    p_flame1 = Path(fillColor=TERRA_C, strokeColor=None)
    p_flame1.moveTo(cx - 18, cy - 20)
    p_flame1.curveTo(cx - 24, cy + 6, cx - 6, cy + 24, cx, cy + 38)
    p_flame1.curveTo(cx + 6, cy + 24, cx + 24, cy + 6, cx + 18, cy - 20)
    p_flame1.closePath()
    d.add(p_flame1)
    p_flame2 = Path(fillColor=GOLD_C, strokeColor=None)
    p_flame2.moveTo(cx - 10, cy - 20)
    p_flame2.curveTo(cx - 14, cy, cx - 3, cy + 16, cx, cy + 26)
    p_flame2.curveTo(cx + 3, cy + 16, cx + 14, cy, cx + 10, cy - 20)
    p_flame2.closePath()
    d.add(p_flame2)
    for sign in (-1, 1):
        for dy in (-10, 2, 14):
            d.add(Ellipse(cx + sign * 36, cy + dy, 5, 2.2, fillColor=SAGE_C, strokeColor=NAVY_C, strokeWidth=0.5))
    d.add(String(cx - 135, cy - 52, "INTRINSIC MASTERY DRIVE  &  BENCHMARKED COHORT EXCELLENCE",
                 fontName="Times-Italic", fontSize=6.5, fillColor=HexColor("#64748B")))
    return d
def draw_boho_behavioral_equilibrium(width: float = 460, height: float = 120) -> Drawing:
    d = Drawing(width, height)
    cx, cy = width / 2.0, height / 2.0 + 4
    lx = cx - 55
    d.add(Line(lx, cy - 32, lx, cy + 24, strokeColor=GOLD_LT, strokeWidth=0.6))
    d.add(Ellipse(lx, cy - 24, 24, 6.5, fillColor=SAND_C, strokeColor=NAVY_C, strokeWidth=0.8))
    d.add(Ellipse(lx, cy - 14, 18, 5.5, fillColor=SAGE_C, strokeColor=NAVY_C, strokeWidth=0.8))
    d.add(Ellipse(lx, cy - 5, 12, 4.5, fillColor=TERRA_C, strokeColor=NAVY_C, strokeWidth=0.8))
    d.add(Circle(lx, cy + 5, 2, fillColor=GOLD_C, strokeColor=None))
    d.add(String(lx - 26, cy - 38, "CRISIS POISE", fontName="Times-Bold", fontSize=6.5, fillColor=NAVY_C))
    rx = cx + 55
    p_sail = Path(fillColor=GOLD_PL, strokeColor=GOLD_C, strokeWidth=1.1)
    p_sail.moveTo(rx - 15, cy - 25)
    p_sail.curveTo(rx + 22, cy - 15, rx + 22, cy + 18, rx - 10, cy + 26)
    p_sail.curveTo(rx + 5, cy + 6, rx + 5, cy - 14, rx - 15, cy - 25)
    p_sail.closePath()
    d.add(p_sail)
    d.add(Line(rx + 15, cy + 24, rx + 25, cy + 24, strokeColor=TERRA_C, strokeWidth=1.0))
    d.add(Line(rx + 20, cy + 19, rx + 20, cy + 29, strokeColor=TERRA_C, strokeWidth=1.0))
    d.add(Circle(rx + 20, cy + 24, 1.8, fillColor=GOLD_C, strokeColor=None))
    d.add(String(rx - 28, cy - 38, "RISK APPETITE", fontName="Times-Bold", fontSize=6.5, fillColor=NAVY_C))
    d.add(String(cx - 145, cy - 52, "RATIONAL CRISIS POISE  &  CALCULATED INNOVATION APPETITE",
                 fontName="Times-Italic", fontSize=6.5, fillColor=HexColor("#64748B")))
    return d
def draw_boho_organization_pillars(width: float = 460, height: float = 75) -> Drawing:
    d = Drawing(width, height)
    cx, cy = width / 2.0, height / 2.0 + 3
    d.add(Line(40, cy, width - 40, cy, strokeColor=GOLD_LT, strokeWidth=0.9))
    d.add(Circle(40, cy, 2, fillColor=GOLD_C, strokeColor=None))
    d.add(Circle(width - 40, cy, 2, fillColor=GOLD_C, strokeColor=None))
    nodes = [
        (85, "COGNITION", TERRA_C),
        (185, "MAPPING", SAGE_C),
        (285, "COACHING", SAND_C),
        (385, "ACCELERATION", GOLD_C),
    ]
    for nx, tag, col in nodes:
        d.add(Circle(nx, cy, 14, fillColor=GOLD_PL, strokeColor=GOLD_C, strokeWidth=0.8))
        d.add(Circle(nx, cy, 11, fillColor=IVORY_C, strokeColor=NAVY_C, strokeWidth=0.6))
        d.add(Circle(nx, cy, 4, fillColor=col, strokeColor=None))
        d.add(String(nx - 24, cy - 20, tag, fontName="Times-Bold", fontSize=6, fillColor=NAVY_C))
    d.add(String(cx - 150, cy - 30, "EVIDENCE-BASED NEUROLOGICAL ASSESSMENT & ACTIONABLE DEVELOPMENTAL CLARITY",
                 fontName="Times-Italic", fontSize=6.5, fillColor=HexColor("#64748B")))
    return d
def draw_boho_literature_heritage(width: float = 460, height: float = 110) -> Drawing:
    d = Drawing(width, height)
    cx, cy = width / 2.0, height / 2.0 + 4
    p_canopy = Path(fillColor=GOLD_PL, strokeColor=GOLD_LT, strokeWidth=0.8)
    p_canopy.moveTo(cx - 70, cy - 25)
    p_canopy.curveTo(cx - 70, cy + 42, cx + 70, cy + 42, cx + 70, cy - 25)
    p_canopy.closePath()
    d.add(p_canopy)
    d.add(Line(cx, cy - 25, cx, cy + 15, strokeColor=NAVY_C, strokeWidth=1.8))
    d.add(Line(cx, cy + 5, cx - 25, cy + 22, strokeColor=GOLD_C, strokeWidth=1.0))
    d.add(Line(cx, cy + 8, cx + 25, cy + 22, strokeColor=GOLD_C, strokeWidth=1.0))
    d.add(Line(cx, cy + 12, cx - 12, cy + 28, strokeColor=GOLD_C, strokeWidth=0.8))
    d.add(Line(cx, cy + 12, cx + 12, cy + 28, strokeColor=GOLD_C, strokeWidth=0.8))
    star_positions = [
        (cx - 45, cy + 20, "Cummins"),
        (cx - 25, cy + 32, "Penrose"),
        (cx, cy + 38, "Babler"),
        (cx + 25, cy + 32, "Gardner"),
        (cx + 45, cy + 20, "Schaumann"),
        (cx, cy + 18, "Goleman"),
    ]
    for sx, sy, _name in star_positions:
        d.add(Circle(sx, sy, 2.2, fillColor=GOLD_C, strokeColor=NAVY_C, strokeWidth=0.5))
    for rx in (-35, -20, 0, 20, 35):
        p_root = Path(fillColor=None, strokeColor=TERRA_C, strokeWidth=0.8)
        p_root.moveTo(cx + rx * 0.4, cy - 25)
        p_root.curveTo(cx + rx * 0.6, cy - 32, cx + rx * 0.8, cy - 35, cx + rx, cy - 40)
        d.add(p_root)
    d.add(String(cx - 135, cy - 50, "EIGHT DECADES OF EMPIRICAL DERMATOGLYPHIC & NEUROANATOMICAL INQUIRY",
                 fontName="Times-Italic", fontSize=6.5, fillColor=HexColor("#64748B")))
    return d
def draw_boho_quotients_emblem(width: float = 460, height: float = 65) -> Drawing:
    d = Drawing(width, height)
    cx, cy = width / 2.0, height / 2.0 + 3
    d.add(Line(60, cy, width - 60, cy, strokeColor=GOLD_LT, strokeWidth=0.8))
    nodes = [
        (90, "IQ", "Logic", TERRA_C),
        (165, "EQ", "Empathy", SAGE_C),
        (230, "CQ", "Creative", GOLD_C),
        (295, "AQ", "Resilience", NAVY_C),
        (370, "SQ", "Social", SAND_C),
    ]
    for nx, qk, _desc, col in nodes:
        d.add(Circle(nx, cy, 12, fillColor=GOLD_PL, strokeColor=GOLD_C, strokeWidth=0.8))
        d.add(Circle(nx, cy, 9, fillColor=IVORY_C, strokeColor=NAVY_C, strokeWidth=0.5))
        d.add(Circle(nx, cy, 3, fillColor=col, strokeColor=None))
        d.add(String(nx - 7, cy - 18, qk, fontName="Times-Bold", fontSize=6.5, fillColor=NAVY_C))
    d.add(String(cx - 130, cy - 26, "MULTI-DIMENSIONAL COGNITIVE CAPACITY & ADAPTIVE INTELLIGENCE",
                 fontName="Times-Italic", fontSize=6, fillColor=HexColor("#64748B")))
    return d
def draw_boho_academic_streams(width: float = 460, height: float = 100) -> Drawing:
    d = Drawing(width, height)
    cx, cy = width / 2.0, height / 2.0 + 4
    triptych = [
        (cx - 100, "STEM", TERRA_C, "Compass"),
        (cx, "COMMERCE", GOLD_C, "Scales"),
        (cx + 100, "HUMANITIES", SAGE_C, "Scroll"),
    ]
    for px, title, col, _symbol in triptych:
        p_arch = Path(fillColor=GOLD_PL, strokeColor=NAVY_C, strokeWidth=0.8)
        p_arch.moveTo(px - 28, cy - 25)
        p_arch.lineTo(px - 28, cy + 12)
        p_arch.curveTo(px - 28, cy + 34, px + 28, cy + 34, px + 28, cy + 12)
        p_arch.lineTo(px + 28, cy - 25)
        p_arch.closePath()
        d.add(p_arch)
        d.add(Circle(px, cy + 8, 8, fillColor=IVORY_C, strokeColor=col, strokeWidth=1.0))
        d.add(Circle(px, cy + 8, 3, fillColor=col, strokeColor=None))
        d.add(String(px - 18, cy - 34, title, fontName="Times-Bold", fontSize=6.5, fillColor=NAVY_C))
    d.add(String(cx - 145, cy - 44, "CROSS-DISCIPLINARY ALIGNMENT ACROSS NATURAL, COMMERCIAL & SOCIAL SCIENCES",
                 fontName="Times-Italic", fontSize=6.5, fillColor=HexColor("#64748B")))
    return d
def draw_boho_counseling_roadmap(width: float = 460, height: float = 75) -> Drawing:
    d = Drawing(width, height)
    cx, cy = width / 2.0, height / 2.0 + 3
    d.add(Line(50, cy, width - 50, cy, strokeColor=GOLD_LT, strokeWidth=0.8))
    d.add(Circle(50, cy, 2, fillColor=GOLD_C, strokeColor=None))
    d.add(Circle(width - 50, cy, 2, fillColor=GOLD_C, strokeColor=None))
    d.add(Circle(cx, cy, 16, fillColor=GOLD_PL, strokeColor=GOLD_C, strokeWidth=0.9))
    d.add(Circle(cx, cy, 12, fillColor=IVORY_C, strokeColor=GOLD_LT, strokeWidth=0.5))
    d.add(Line(cx - 10, cy, cx + 10, cy, strokeColor=NAVY_C, strokeWidth=1.0))
    d.add(Line(cx, cy - 10, cx, cy + 10, strokeColor=NAVY_C, strokeWidth=1.0))
    d.add(Line(cx - 6, cy - 6, cx + 6, cy + 6, strokeColor=GOLD_C, strokeWidth=0.8))
    d.add(Line(cx - 6, cy + 6, cx + 6, cy - 6, strokeColor=GOLD_C, strokeWidth=0.8))
    d.add(Circle(cx, cy, 2, fillColor=TERRA_C, strokeColor=None))
    for mx, mlabel in ((cx - 110, "DIAGNOSTIC BASELINE"), (cx + 110, "ACTION TRAJECTORY")):
        d.add(Circle(mx, cy, 3, fillColor=SAGE_C, strokeColor=NAVY_C, strokeWidth=0.6))
        d.add(String(mx - 35, cy - 14, mlabel, fontName="Times-Bold", fontSize=5.5, fillColor=NAVY_C))
    d.add(String(cx - 130, cy - 24, "HOLISTIC DEVELOPMENTAL MILESTONES & 30-DAY STRATEGIC TRAJECTORY",
                 fontName="Times-Italic", fontSize=6.5, fillColor=HexColor("#64748B")))
    return d
