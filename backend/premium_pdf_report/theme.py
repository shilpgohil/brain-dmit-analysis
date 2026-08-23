"""
Premium DMIT Report - Theme Constants and ReportLab Styles
==========================================================
Ivory/gold palette, Times New Roman throughout, no em dashes.
"""

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate
from reportlab.lib.pagesizes import A4

# ---------------------------------------------------------------------------
# Colour palette
# ---------------------------------------------------------------------------
IVORY        = colors.HexColor('#FFFDF4')
CREAM_ALT    = colors.HexColor('#FAF7EC')
CREAM_ROW    = colors.HexColor('#F5EDD3')
GOLD         = colors.HexColor('#C9A441')
GOLD_DARK    = colors.HexColor('#8B6914')
GOLD_LIGHT   = colors.HexColor('#E8D5A3')
GOLD_PALE    = colors.HexColor('#F5EBD0')
NAVY         = colors.HexColor('#0D1B3E')
NAVY_LIGHT   = colors.HexColor('#1A2F5A')
GREY_TEXT    = colors.HexColor('#2C2C2C')
GREY_LIGHT   = colors.HexColor('#D4C9A8')
SAGE         = colors.HexColor('#5A7A6A')
PLUM         = colors.HexColor('#6B3D6B')
TERRACOTTA   = colors.HexColor('#B05030')
GREEN_STRONG = colors.HexColor('#2E7D32')
AMBER_MID    = colors.HexColor('#F57F17')
RED_WEAK     = colors.HexColor('#C62828')
WHITE        = colors.white

# Hex strings for matplotlib (no 'colors.' prefix)
HEX = {
    'ivory':        '#FFFDF4',
    'cream_alt':    '#FAF7EC',
    'cream_row':    '#F5EDD3',
    'gold':         '#C9A441',
    'gold_dark':    '#8B6914',
    'gold_light':   '#E8D5A3',
    'gold_pale':    '#F5EBD0',
    'navy':         '#0D1B3E',
    'navy_light':   '#1A2F5A',
    'grey_text':    '#2C2C2C',
    'grey_light':   '#D4C9A8',
    'sage':         '#5A7A6A',
    'plum':         '#6B3D6B',
    'terracotta':   '#B05030',
    'green_strong': '#2E7D32',
    'amber_mid':    '#F57F17',
    'red_weak':     '#C62828',
}

# Score tier colours
def score_color(score: float):
    """Return (reportlab_color, label) based on 0-1 score."""
    if score >= 0.75:
        return GREEN_STRONG, 'Outstanding'
    if score >= 0.60:
        return GOLD_DARK, 'High'
    if score >= 0.45:
        return AMBER_MID, 'Moderate'
    if score >= 0.30:
        return TERRACOTTA, 'Developing'
    return RED_WEAK, 'Needs Focus'

def score_color_hex(score: float) -> str:
    if score >= 0.75: return HEX['green_strong']
    if score >= 0.60: return HEX['gold_dark']
    if score >= 0.45: return HEX['amber_mid']
    if score >= 0.30: return HEX['terracotta']
    return HEX['red_weak']

# ---------------------------------------------------------------------------
# ReportLab style sheet (Times New Roman everywhere)
# ---------------------------------------------------------------------------

def build_styles():
    """Build and return the complete premium style sheet."""
    base = getSampleStyleSheet()

    styles = {}

    # Report title (cover)
    styles['report_title'] = ParagraphStyle(
        'ReportTitle',
        fontName='Times-Bold',
        fontSize=26,
        leading=32,
        textColor=NAVY,
        alignment=TA_CENTER,
        spaceAfter=8,
    )

    # Cover subtitle
    styles['report_subtitle'] = ParagraphStyle(
        'ReportSubtitle',
        fontName='Times-BoldItalic',
        fontSize=14,
        leading=18,
        textColor=GOLD_DARK,
        alignment=TA_CENTER,
        spaceAfter=4,
    )

    # Section heading (e.g. "Section 9 : Multiple Intelligence Profile")
    styles['section_heading'] = ParagraphStyle(
        'SectionHeading',
        fontName='Times-Bold',
        fontSize=16,
        leading=20,
        textColor=WHITE,
        alignment=TA_LEFT,
        spaceAfter=0,
        spaceBefore=0,
        leftIndent=10,
    )

    # Sub-section heading
    styles['sub_heading'] = ParagraphStyle(
        'SubHeading',
        fontName='Times-Bold',
        fontSize=12,
        leading=16,
        textColor=GOLD_DARK,
        alignment=TA_LEFT,
        spaceAfter=6,
        spaceBefore=10,
    )

    # Body text
    styles['body'] = ParagraphStyle(
        'Body',
        fontName='Times-Roman',
        fontSize=10,
        leading=14,
        textColor=GREY_TEXT,
        alignment=TA_JUSTIFY,
        spaceAfter=6,
    )

    # Body left-aligned
    styles['body_left'] = ParagraphStyle(
        'BodyLeft',
        fontName='Times-Roman',
        fontSize=10,
        leading=14,
        textColor=GREY_TEXT,
        alignment=TA_LEFT,
        spaceAfter=4,
    )

    # Small caption / footnote
    styles['caption'] = ParagraphStyle(
        'Caption',
        fontName='Times-Italic',
        fontSize=8,
        leading=11,
        textColor=GOLD_DARK,
        alignment=TA_CENTER,
        spaceAfter=4,
    )

    # Table cell (normal)
    styles['table_cell'] = ParagraphStyle(
        'TableCell',
        fontName='Times-Roman',
        fontSize=9,
        leading=12,
        textColor=GREY_TEXT,
        alignment=TA_LEFT,
    )

    # Table cell bold
    styles['table_cell_bold'] = ParagraphStyle(
        'TableCellBold',
        fontName='Times-Bold',
        fontSize=9,
        leading=12,
        textColor=NAVY,
        alignment=TA_LEFT,
    )

    # Table header
    styles['table_header'] = ParagraphStyle(
        'TableHeader',
        fontName='Times-Bold',
        fontSize=9,
        leading=12,
        textColor=WHITE,
        alignment=TA_CENTER,
    )

    # Score badge (inside gauge / tile)
    styles['score_badge'] = ParagraphStyle(
        'ScoreBadge',
        fontName='Times-Bold',
        fontSize=22,
        leading=26,
        textColor=NAVY,
        alignment=TA_CENTER,
    )

    # Cover tagline
    styles['tagline'] = ParagraphStyle(
        'Tagline',
        fontName='Times-BoldItalic',
        fontSize=13,
        leading=18,
        textColor=GOLD,
        alignment=TA_CENTER,
        spaceAfter=4,
    )

    # Bullet point
    styles['bullet'] = ParagraphStyle(
        'Bullet',
        fontName='Times-Roman',
        fontSize=10,
        leading=14,
        textColor=GREY_TEXT,
        leftIndent=14,
        firstLineIndent=-14,
        spaceAfter=3,
    )

    # Intro / scientific text (slightly larger body)
    styles['intro_body'] = ParagraphStyle(
        'IntroBody',
        fontName='Times-Roman',
        fontSize=10,
        leading=15,
        textColor=GREY_TEXT,
        alignment=TA_JUSTIFY,
        spaceAfter=8,
    )

    # Bold label inline
    styles['label'] = ParagraphStyle(
        'Label',
        fontName='Times-Bold',
        fontSize=10,
        leading=14,
        textColor=NAVY,
        alignment=TA_LEFT,
    )

    # --- Cover: text sitting on the navy anchor band (needs light colours,
    # unlike every other style above which assumes an ivory background) ---
    styles['cover_band_headline'] = ParagraphStyle(
        'CoverBandHeadline',
        fontName='Times-BoldItalic',
        fontSize=16,
        leading=20,
        textColor=GOLD,
        alignment=TA_CENTER,
        spaceAfter=4,
    )

    styles['cover_band_label'] = ParagraphStyle(
        'CoverBandLabel',
        fontName='Times-Bold',
        fontSize=8,
        leading=11,
        textColor=GOLD_LIGHT,
        alignment=TA_LEFT,
        spaceAfter=1,
    )

    styles['cover_band_value'] = ParagraphStyle(
        'CoverBandValue',
        fontName='Times-Bold',
        fontSize=11,
        leading=14,
        textColor=WHITE,
        alignment=TA_LEFT,
    )

    styles['cover_band_disclaimer'] = ParagraphStyle(
        'CoverBandDisclaimer',
        fontName='Times-Italic',
        fontSize=7.5,
        leading=10,
        textColor=GOLD_LIGHT,
        alignment=TA_CENTER,
    )

    # Cover: short italic descriptor line under the subtitle
    styles['cover_lede'] = ParagraphStyle(
        'CoverLede',
        fontName='Times-Italic',
        fontSize=10.5,
        leading=15,
        textColor=GREY_TEXT,
        alignment=TA_CENTER,
        spaceAfter=4,
        leftIndent=40,
        rightIndent=40,
    )

    # Counsellor note (slightly italic body)
    styles['counsellor'] = ParagraphStyle(
        'Counsellor',
        fontName='Times-Italic',
        fontSize=10,
        leading=15,
        textColor=GREY_TEXT,
        alignment=TA_JUSTIFY,
        spaceAfter=6,
        leftIndent=12,
        rightIndent=12,
    )

    return styles


# Singleton
STYLES = build_styles()


# ---------------------------------------------------------------------------
# Document factory
# ---------------------------------------------------------------------------

# Margins shared between make_document() and any code (e.g. cover.py) that
# needs to compute exact on-page positions of flowables independent of the
# Frame/doc machinery.
TOP_MARGIN = 0.65 * inch
BOTTOM_MARGIN = 0.7 * inch
SIDE_MARGIN = 0.75 * inch


def make_document(output_path: str) -> SimpleDocTemplate:
    return SimpleDocTemplate(
        output_path,
        pagesize=A4,
        rightMargin=SIDE_MARGIN,
        leftMargin=SIDE_MARGIN,
        topMargin=TOP_MARGIN,
        bottomMargin=BOTTOM_MARGIN,
    )


# ---------------------------------------------------------------------------
# Page dimensions helpers
# ---------------------------------------------------------------------------
PAGE_W, PAGE_H = A4
CONTENT_W = PAGE_W - 1.5 * inch   # usable width with 0.75in margins
CONTENT_H = PAGE_H - 1.35 * inch  # usable height
