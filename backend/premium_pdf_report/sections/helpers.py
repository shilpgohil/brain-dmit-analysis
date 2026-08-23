"""
Shared helper flowables used across all section builders.
"""

import base64
import io
import logging
from typing import Optional

logger = logging.getLogger(__name__)

from reportlab.platypus import Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.platypus.flowables import Flowable
from reportlab.lib.units import inch
from reportlab.lib import colors

from ..theme import (STYLES, NAVY, GOLD, GOLD_DARK, GOLD_LIGHT, GOLD_PALE,
                     IVORY, CREAM_ROW, CREAM_ALT, WHITE, CONTENT_W)


# ---------------------------------------------------------------------------
# Section header banner (navy bar + gold rule)
# ---------------------------------------------------------------------------

class SectionHeader(Flowable):
    """Full-width navy band with white Times-Bold section title."""

    # Tell ReportLab to keep this flowable on the same page as the next one
    keepWithNext = 1

    def __init__(self, number: int, title: str, width: float = None):
        super().__init__()
        self.number = number
        self.title = title
        self.width = width or CONTENT_W
        self.height = 32

    def draw(self):
        c = self.canv
        c.saveState()
        # Navy background
        c.setFillColor(NAVY)
        c.roundRect(0, 0, self.width, self.height, 4, stroke=0, fill=1)
        # Gold left accent bar
        c.setFillColor(GOLD)
        c.roundRect(0, 0, 5, self.height, 2, stroke=0, fill=1)
        # White title text
        c.setFillColor(colors.white)
        c.setFont('Times-Bold', 13)
        label = f'Section {self.number}  :  {self.title}'
        c.drawString(14, 10, label)
        c.restoreState()


def section_header(number: int, title: str) -> list:
    """
    Return [SectionHeader, gold_rule, spacer] bundled in one KeepTogether.

    The bundle itself is also marked keepWithNext=1. Most call sites use
    this for sections that no longer get a forced PageBreak beforehand
    (they flow straight on from the previous section), so the banner can
    land with little space left on the current page. Without this, the
    banner alone could fit and render at the very bottom of a page while
    its intro paragraph got pushed to the top of the next one — the exact
    "heading on one page, content on the next" split this is meant to
    prevent. Marking it keepWithNext pulls the very next story flowable
    (almost always the section's short intro paragraph) into the same
    unbreakable group.
    """
    from reportlab.platypus import KeepTogether
    kt = KeepTogether([
        SectionHeader(number, title),
        HRFlowable(width=CONTENT_W, thickness=1.2, color=GOLD,
                   spaceAfter=10, spaceBefore=0),
        Spacer(1, 4),
    ])
    kt.keepWithNext = 1
    return [kt]


def section_header_plain(number: int, title: str) -> list:
    """
    Same visual as section_header() but WITHOUT the KeepTogether wrapper.

    Use this when the header is going inside a KeepInFrame (e.g. via
    shrink_block) — some ReportLab versions call .draw() directly on nested
    children and choke on a bare KeepTogether there
    ('KeepTogether' object has no attribute 'draw'), the same incompatibility
    already worked around for chart_image(). The banner + rule are a single
    tiny unbreakable unit in practice, so dropping KeepTogether here carries
    no real risk of them splitting across a page on their own.
    """
    return [
        SectionHeader(number, title),
        HRFlowable(width=CONTENT_W, thickness=1.2, color=GOLD,
                   spaceAfter=10, spaceBefore=0),
        Spacer(1, 4),
    ]


# ---------------------------------------------------------------------------
# Sub-section heading with gold underline
# ---------------------------------------------------------------------------

def sub_heading(text: str) -> list:
    """
    Sub-section heading (bold label + short gold underline rule).

    Both the label and the rule get keepWithNext=1. ReportLab's
    handle_keepWithNext() walks a *chain* of consecutive keepWithNext=True
    flowables and then pulls in exactly one more flowable after the chain
    ends into the same unbreakable KeepTogether group. Marking only the
    Paragraph (as before) chains just the heading to its own underline rule
    — the rule itself ends the chain, so the real body content right after
    it (a Paragraph or Table) was never protected and could be pushed alone
    to the next page while the heading stayed behind (observed e.g. on the
    "Howard Gardner's Multiple Intelligence Theory" heading spilling its
    paragraph onto the next page). Marking the rule too extends the chain
    one flowable further, so heading + rule + the first body flowable that
    follows always land on the same page together.
    """
    p = Paragraph(text, STYLES['sub_heading'])
    p.keepWithNext = 1
    hr = HRFlowable(width=CONTENT_W * 0.35, thickness=0.8, color=GOLD_LIGHT,
                     spaceAfter=6, spaceBefore=0)
    hr.keepWithNext = 1
    return [p, hr]


# ---------------------------------------------------------------------------
# Chart image from base64
# ---------------------------------------------------------------------------

def chart_image(b64: str, width: float = None, caption: str = '') -> list:
    """Embed a base64 chart PNG as a ReportLab Image flowable."""
    if not b64:
        return []
    try:
        from reportlab.platypus import Image as RLImage
        data = base64.b64decode(b64)
        buf = io.BytesIO(data)
        target_w = width or CONTENT_W * 0.88

        # kind='proportional' needs BOTH width and height to compute a fit-
        # within-box scale factor (reportlab does
        # min(width/imageWidth, height/imageHeight)); passing width alone
        # always raised TypeError('NoneType') and silently dropped every
        # chart from the report. Read the PNG's native size ourselves and
        # derive a height that preserves its aspect ratio instead.
        try:
            from PIL import Image as PILImage
            buf.seek(0)
            native_w, native_h = PILImage.open(buf).size
            buf.seek(0)
            target_h = target_w * (native_h / native_w) if native_w else target_w
        except Exception:
            target_h = target_w * 0.7  # reasonable fallback aspect ratio

        img = RLImage(buf, width=target_w, height=target_h, kind='direct')
        # NOTE: intentionally NOT wrapped in KeepTogether — this list is also
        # placed inside KeepInFrame boxes (see two_col()), and some ReportLab
        # versions call .draw() on nested content in a way KeepTogether does
        # not support there ('KeepTogether' object has no attribute 'draw').
        # Plain flowables work uniformly at top-level and inside KeepInFrame.
        items = [img]
        if caption:
            items.append(Paragraph(caption, STYLES['caption']))
        return items
    except Exception:
        logger.exception("chart_image failed to embed chart (caption=%r)", caption)
        return []


# ---------------------------------------------------------------------------
# Score row table (label | bar | score | level)
# ---------------------------------------------------------------------------

def score_table(rows_data: list, col_widths=None) -> Table:
    """
    rows_data: list of [label, score_0_to_1, level_str] tuples.
    """
    from ..theme import score_color

    header = [
        Paragraph('Attribute', STYLES['table_header']),
        Paragraph('Score', STYLES['table_header']),
        Paragraph('Level', STYLES['table_header']),
    ]
    table_rows = [header]
    fill_colors_map = {}

    for i, (lbl, score, level) in enumerate(rows_data, start=1):
        rl_color, _ = score_color(score)
        fill_colors_map[i] = rl_color
        table_rows.append([
            Paragraph(str(lbl), STYLES['table_cell']),
            Paragraph(f'{score * 100:.0f}%', STYLES['table_cell_bold']),
            Paragraph(str(level), STYLES['table_cell']),
        ])

    cw = col_widths or [CONTENT_W * 0.55, CONTENT_W * 0.18, CONTENT_W * 0.22]
    t = Table(table_rows, colWidths=cw)

    ts = [
        ('BACKGROUND', (0, 0), (-1, 0), NAVY),
        ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
        ('FONTNAME', (0, 0), (-1, 0), 'Times-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 0.4, GOLD_LIGHT),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [GOLD_PALE, IVORY]),
    ]
    t.setStyle(TableStyle(ts))
    return t


# ---------------------------------------------------------------------------
# Two-column layout helper
# ---------------------------------------------------------------------------

def two_col(left_items: list, right_items: list,
            left_w: float = None, right_w: float = None) -> Table:
    """Wrap two lists of flowables in a side-by-side 2-column table."""
    lw = left_w or CONTENT_W * 0.50
    rw = right_w or CONTENT_W * 0.46
    from reportlab.platypus import KeepInFrame
    # Use 'overflow' mode so charts never get silently shrunk to nothing. The
    # max height just needs to comfortably exceed any real chart+caption
    # (a few inches); a previous 999in placeholder made ReportLab size the
    # KeepInFrame's own space requirement at ~1000ft tall once real chart
    # images started rendering, blowing the enclosing table off the page.
    lkf = KeepInFrame(lw, 9 * inch, left_items, mode='overflow')
    rkf = KeepInFrame(rw, 9 * inch, right_items, mode='overflow')
    t = Table([[lkf, rkf]], colWidths=[lw, rw])
    t.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ('TOPPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
    ]))
    return t


# ---------------------------------------------------------------------------
# Pill badge (inline colored label)
# ---------------------------------------------------------------------------

def pill_table(labels: list, color) -> Table:
    """Row of colored pill badges."""
    cells = []
    for lbl in labels:
        p = Paragraph(lbl, STYLES['table_header'])
        cells.append(p)
    if not cells:
        return Table([['']])
    t = Table([cells], colWidths=[CONTENT_W / max(1, len(cells))] * len(cells))
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), color),
        ('ROUNDEDCORNERS', [6, 6, 6, 6]),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ]))
    return t


# ---------------------------------------------------------------------------
# Info card (gold-bordered box with title + body text)
# ---------------------------------------------------------------------------

def shrink_block(items: list, max_height: float = 8.7 * inch, width: float = None,
                  _label: str = None) -> Table:
    """
    Force a whole chart+table (or any flowable group) onto a single page.

    Several sections build a bar/radar chart followed by a ranked score
    table (e.g. Cognitive, Leadership, Emotional Intelligence). When the
    combined height slightly exceeds one page, ReportLab's default table
    splitting left the last 2-3 rows stranded alone at the top of the next
    page, followed immediately by the next section's forced PageBreak —
    producing a near-empty page. KeepInFrame(mode='shrink') uniformly scales
    the whole block down just enough to fit in max_height, so it always
    renders intact on a single page instead of splitting across two.
    """
    from reportlab.platypus import KeepInFrame
    from reportlab.platypus.flowables import _listWrapOn
    w = width or CONTENT_W
    try:
        from reportlab.pdfgen.canvas import Canvas
        import io as _io
        _, _needed_h = _listWrapOn(items, w, Canvas(_io.BytesIO()))
        if _needed_h > max_height:
            logger.warning(
                "shrink_block[%s]: content needs %.2fin but only %.2fin available "
                "(scale ~%.2f) - fonts/images in this block will be shrunk",
                _label or '?', _needed_h / inch, max_height / inch, max_height / _needed_h)
    except Exception:
        pass
    kf = KeepInFrame(w, max_height, items, mode='shrink')
    t = Table([[kf]], colWidths=[w])
    t.setStyle(TableStyle([
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ('TOPPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
    ]))
    return t


def info_card(title: str, body: str, color=None) -> Table:
    color = color or GOLD_PALE
    inner = [
        Paragraph(title, STYLES['sub_heading']),
        Paragraph(body, STYLES['body']),
    ]
    from reportlab.platypus import KeepInFrame
    kf = KeepInFrame(CONTENT_W - 0.3 * inch, 9 * inch, inner, mode='shrink')
    t = Table([[kf]], colWidths=[CONTENT_W])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), color),
        ('BOX', (0, 0), (-1, -1), 1.2, GOLD),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('ROUNDEDCORNERS', [4, 4, 4, 4]),
    ]))
    return t
