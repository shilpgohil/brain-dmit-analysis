"""
Shared helper flowables used across all section builders.
"""

import base64
import io
from typing import Optional

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
    """Return [SectionHeader, gold_rule_spacer] flowables kept together."""
    from reportlab.platypus import KeepTogether
    return [KeepTogether([
        SectionHeader(number, title),
        HRFlowable(width=CONTENT_W, thickness=1.2, color=GOLD,
                   spaceAfter=10, spaceBefore=0),
        Spacer(1, 4),
    ])]


# ---------------------------------------------------------------------------
# Sub-section heading with gold underline
# ---------------------------------------------------------------------------

def sub_heading(text: str) -> list:
    # keepWithNext on the paragraph keeps sub-heading pinned to next flowable
    p = Paragraph(text, STYLES['sub_heading'])
    p.keepWithNext = 1
    return [
        p,
        HRFlowable(width=CONTENT_W * 0.35, thickness=0.8, color=GOLD_LIGHT,
                   spaceAfter=6, spaceBefore=0),
    ]


# ---------------------------------------------------------------------------
# Chart image from base64
# ---------------------------------------------------------------------------

def chart_image(b64: str, width: float = None, caption: str = '') -> list:
    """Embed a base64 chart PNG as a ReportLab Image flowable."""
    if not b64:
        return []
    try:
        from reportlab.platypus import Image as RLImage, KeepTogether
        data = base64.b64decode(b64)
        buf = io.BytesIO(data)
        img = RLImage(buf, width=width or CONTENT_W * 0.88,
                      kind='proportional')
        items = [img]
        if caption:
            items.append(Paragraph(caption, STYLES['caption']))
        # Keep image and caption together so caption never orphans on next page
        return [KeepTogether(items)]
    except Exception:
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
    # Use 'overflow' mode so charts never get silently shrunk to nothing
    lkf = KeepInFrame(lw, 999 * inch, left_items, mode='overflow')
    rkf = KeepInFrame(rw, 999 * inch, right_items, mode='overflow')
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

def info_card(title: str, body: str, color=None) -> Table:
    color = color or GOLD_PALE
    inner = [
        Paragraph(title, STYLES['sub_heading']),
        Paragraph(body, STYLES['body']),
    ]
    from reportlab.platypus import KeepInFrame
    kf = KeepInFrame(CONTENT_W - 0.3 * inch, 999 * inch, inner, mode='shrink')
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
