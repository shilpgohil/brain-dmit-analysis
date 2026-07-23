"""
Cover Page - DNA helix watermark background, gold branding.
"""

import math
import numpy as np
from datetime import datetime
from typing import Dict, Any

from reportlab.platypus import Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus.flowables import Flowable

from ..theme import (STYLES, NAVY, GOLD, GOLD_DARK, GOLD_LIGHT, GOLD_PALE,
                     IVORY, CREAM_ROW, WHITE, GREY_TEXT, CONTENT_W)


class DNAHelixWatermark(Flowable):
    """Draws a subtle DNA double-helix watermark using ReportLab canvas."""

    def __init__(self, width: float, height: float):
        super().__init__()
        self.width = width
        self.height = height

    def draw(self):
        c = self.canv
        c.saveState()
        # Use transparency via color alpha channel instead of setAlpha
        from reportlab.lib.colors import HexColor
        dna_color = HexColor('#E8D59A')  # pale gold for DNA strands
        c.setStrokeColor(dna_color)
        c.setFillColor(dna_color)
        c.setLineWidth(1.2)

        w, h = self.width, self.height
        cx = w / 2
        strand_amp = w * 0.22
        freq = 2.5 * math.pi / h
        n_pts = 200

        # Strand 1 (sine)
        pts1 = [(cx + strand_amp * math.sin(freq * y), y)
                for y in np.linspace(0, h, n_pts)]
        # Strand 2 (cosine offset)
        pts2 = [(cx - strand_amp * math.sin(freq * y + math.pi), y)
                for y in np.linspace(0, h, n_pts)]

        # Draw strand 1
        p = c.beginPath()
        p.moveTo(*pts1[0])
        for x, y in pts1[1:]:
            p.lineTo(x, y)
        c.drawPath(p, stroke=1, fill=0)

        # Draw strand 2
        p = c.beginPath()
        p.moveTo(*pts2[0])
        for x, y in pts2[1:]:
            p.lineTo(x, y)
        c.drawPath(p, stroke=1, fill=0)

        # Cross-links (rungs)
        n_rungs = 18
        for i in range(n_rungs):
            t = i / (n_rungs - 1)
            y = t * h
            x1 = cx + strand_amp * math.sin(freq * y)
            x2 = cx - strand_amp * math.sin(freq * y + math.pi)
            c.setLineWidth(0.7)
            c.line(x1, y, x2, y)
            # Nodes at rung ends
            c.circle(x1, y, 3, stroke=0, fill=1)
            c.circle(x2, y, 3, stroke=0, fill=1)

        c.restoreState()


class GoldRule(Flowable):
    """A double gold rule line."""

    def __init__(self, width: float, thick=2.0, thin=0.6, gap=3):
        super().__init__()
        self.width = width
        self.thick = thick
        self.thin = thin
        self.gap = gap
        self.height = thick + gap + thin + 2

    def draw(self):
        c = self.canv
        c.saveState()
        c.setStrokeColor(GOLD)
        c.setLineWidth(self.thick)
        c.line(0, self.thin + self.gap + self.thick / 2,
               self.width, self.thin + self.gap + self.thick / 2)
        c.setLineWidth(self.thin)
        c.line(0, self.thin / 2, self.width, self.thin / 2)
        c.restoreState()


def build_cover(report_data: Dict[str, Any], session: Dict[str, Any]) -> list:
    """Return list of flowables for the cover page."""
    story = []
    meta = report_data.get('report_metadata', {})
    subject_name = session.get('subject_name') or meta.get('subject_name', 'Subject Name')
    subject_age  = session.get('subject_age') or meta.get('subject_age', '')
    subject_dob  = session.get('subject_dob') or meta.get('subject_dob', '')
    subject_gender = session.get('subject_gender') or meta.get('subject_gender', '')
    counsellor   = session.get('counsellor') or meta.get('counsellor', 'Ridge Analysis Counsellor')
    report_id    = meta.get('report_id', f"RA-{datetime.now().strftime('%Y%m%d')}-001")
    test_date    = meta.get('test_date', datetime.now().strftime('%d %B %Y'))
    school       = session.get('school') or meta.get('school', '')

    # Top rule (brain neural watermark is drawn on the page canvas in generator.py)
    story.append(Spacer(1, 8))
    story.append(GoldRule(CONTENT_W))
    story.append(Spacer(1, 20))

    # Logo placeholder
    logo_data = [['[ LOGO ]']]
    logo_t = Table(logo_data, colWidths=[1.4 * inch])
    logo_t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, -1), 'Times-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('TEXTCOLOR', (0, 0), (-1, -1), GOLD_DARK),
        ('BOX', (0, 0), (-1, -1), 1.2, GOLD),
        ('ROUNDEDCORNERS', [6, 6, 6, 6]),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    logo_row = Table([[logo_t]], colWidths=[CONTENT_W])
    logo_row.setStyle(TableStyle([('ALIGN', (0, 0), (-1, -1), 'CENTER')]))
    story.append(logo_row)
    story.append(Spacer(1, 18))

    # Main title
    story.append(Paragraph(
        'Dermatoglyphics Multiple Intelligence<br/>Analysis Report',
        STYLES['report_title']
    ))
    story.append(Spacer(1, 6))

    # Subtitle with gold ornament
    story.append(Paragraph(
        'Advanced Biometric Intelligence Assessment',
        STYLES['report_subtitle']
    ))
    story.append(Spacer(1, 8))

    # Short ornament line
    story.append(HRFlowable(width=CONTENT_W * 0.4, thickness=1, color=GOLD,
                             spaceAfter=18, spaceBefore=4, hAlign='CENTER'))

    # Profile card table
    rows = []
    fields = [
        ('Candidate Name', subject_name),
        ('Date of Birth', subject_dob or (f'Age: {subject_age}' if subject_age else '')),
        ('Gender', subject_gender),
        ('School / Institution', school),
        ('Test Date', test_date),
        ('Report ID', report_id),
        ('Counsellor', counsellor),
    ]
    for label, value in fields:
        if value:
            rows.append([
                Paragraph(label, STYLES['table_cell_bold']),
                Paragraph(str(value), STYLES['table_cell']),
            ])

    if rows:
        card = Table(rows, colWidths=[2.0 * inch, CONTENT_W - 2.2 * inch])
        card.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), GOLD_PALE),
            ('ROWBACKGROUNDS', (0, 0), (-1, -1), [GOLD_PALE, IVORY]),
            ('LEFTPADDING', (0, 0), (-1, -1), 12),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 7),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 7),
            ('BOX', (0, 0), (-1, -1), 1.5, GOLD),
            ('LINEBELOW', (0, 0), (-1, -2), 0.4, GOLD_LIGHT),
            ('ROUNDEDCORNERS', [5, 5, 5, 5]),
        ]))
        # Center the card
        centered = Table([[card]], colWidths=[CONTENT_W])
        centered.setStyle(TableStyle([('ALIGN', (0, 0), (-1, -1), 'CENTER')]))
        story.append(centered)

    story.append(Spacer(1, 22))

    # Tagline
    story.append(Paragraph('Discover Your Inborn Potential', STYLES['tagline']))
    story.append(Spacer(1, 18))

    # Bottom rule
    story.append(GoldRule(CONTENT_W))
    story.append(Spacer(1, 8))

    # Footer disclaimer
    story.append(Paragraph(
        'Confidential Report. For Educational and Counselling Purposes Only.',
        STYLES['caption']
    ))

    return story
