"""
Cover Page - DNA helix / brain watermark hero, navy anchor band footer.
"""

from pathlib import Path
from datetime import datetime
from typing import Dict, Any

from reportlab.platypus import Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.platypus import Image as RLImage
from reportlab.lib.units import inch
from reportlab.platypus.flowables import Flowable, _listWrapOn

from ..theme import (STYLES, NAVY, GOLD, GOLD_LIGHT, CONTENT_W, CONTENT_H,
                     PAGE_W, PAGE_H, TOP_MARGIN, BOTTOM_MARGIN)
from .. import cover_background

_MONOGRAM = Path(__file__).resolve().parent.parent / "assets" / "logo.png"
_MONOGRAM_SIZE = 1.15 * inch


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
    meta = report_data.get('report_metadata', {})
    subject_name = session.get('subject_name') or meta.get('subject_name', 'Subject Name')
    subject_age  = session.get('subject_age') or meta.get('subject_age', '')
    subject_dob  = session.get('subject_dob') or meta.get('subject_dob', '')
    subject_gender = session.get('subject_gender') or meta.get('subject_gender', '')
    counsellor   = session.get('counsellor') or meta.get('counsellor', 'Ridge Analysis Counsellor')
    report_id    = meta.get('report_id', f"RA-{datetime.now().strftime('%Y%m%d')}-001")
    test_date    = meta.get('test_date', datetime.now().strftime('%d %B %Y'))
    school       = session.get('school') or meta.get('school', '')

    # =======================================================================
    # HERO (upper ~2/3 of the page, over the ivory brain-neural watermark)
    # =======================================================================
    hero = []
    pre_monogram = [Spacer(1, 6), GoldRule(CONTENT_W), Spacer(1, 22)]
    hero += pre_monogram

    # Official brand mark (logo.png): a gold-ringed medallion with a
    # fingerprint-whorl / neural-circuit fusion face, supplied as the final
    # approved logo. Used identically on the website nav bar and favicon --
    # see frontend/src/components/layout/NavBrandMark.tsx.
    if _MONOGRAM.is_file():
        mono = RLImage(str(_MONOGRAM), width=_MONOGRAM_SIZE, height=_MONOGRAM_SIZE)
        mono.hAlign = 'CENTER'
        hero.append(mono)
        hero.append(Spacer(1, 14))

        # The monogram's fine gold linework was clashing/merging visually
        # with the fingerprint watermark directly behind it. Compute the
        # monogram's exact on-page centre (same maths the Frame itself
        # will use: content flows down from the top margin) and register
        # it so cover_background can paint a soft feathered clearing there
        # before the watermark, ahead of the monogram flowable drawing on
        # top of it.
        from reportlab.pdfgen.canvas import Canvas as _CanvasCls
        import io as _io
        _, pre_h = _listWrapOn(pre_monogram, CONTENT_W, _CanvasCls(_io.BytesIO()))
        mono_center_y = PAGE_H - TOP_MARGIN - pre_h - _MONOGRAM_SIZE / 2
        cover_background.set_monogram_center(PAGE_W / 2, mono_center_y)

    hero.append(Paragraph(
        'Dermatoglyphics Multiple Intelligence<br/>Analysis Report',
        STYLES['report_title']
    ))
    hero.append(Spacer(1, 6))
    hero.append(Paragraph(
        'Advanced Biometric Intelligence Assessment',
        STYLES['report_subtitle']
    ))
    hero.append(Spacer(1, 10))
    hero.append(HRFlowable(width=CONTENT_W * 0.32, thickness=1, color=GOLD,
                            spaceAfter=12, spaceBefore=0, hAlign='CENTER'))
    hero.append(Paragraph(
        'A scientific analysis of innate cognitive strengths, learning style, and '
        'brain-lobe dominance, mapped from dermatoglyphic fingerprint biometrics.',
        STYLES['cover_lede']
    ))

    # =======================================================================
    # NAVY ANCHOR BAND CONTENT (drawn over the navy band painted by
    # cover_background.draw_cover_bottom_band; must use light-on-navy
    # styles, not the standard dark-on-ivory ones used everywhere else)
    # =======================================================================
    band = []
    band.append(Spacer(1, 14))
    band.append(Paragraph('Discover Your Inborn Potential', STYLES['cover_band_headline']))
    band.append(HRFlowable(width=CONTENT_W * 0.22, thickness=0.8, color=GOLD_LIGHT,
                            spaceAfter=12, spaceBefore=6, hAlign='CENTER'))

    # Candidate info as a 2x2 label/value grid in light text directly on the
    # band (no boxed card) -- the band itself is the card.
    fields = [
        ('CANDIDATE NAME', subject_name),
        ('REPORT ID', report_id),
        ('TEST DATE', test_date),
        ('COUNSELLOR', counsellor),
    ]
    extra = subject_dob or (f'Age {subject_age}' if subject_age else '') or subject_gender or school
    if extra:
        fields.insert(1, ('DETAILS', extra))

    cells = []
    for lbl, val in fields:
        cells.append(Table(
            [[Paragraph(lbl, STYLES['cover_band_label'])],
             [Paragraph(str(val) if val else '\u2014', STYLES['cover_band_value'])]],
            colWidths=[CONTENT_W / 2 - 6]
        ))
    # Lay the label/value tiles out two-per-row.
    grid_rows = []
    for i in range(0, len(cells), 2):
        row = cells[i:i + 2]
        if len(row) == 1:
            row.append('')
        grid_rows.append(row)
    grid = Table(grid_rows, colWidths=[CONTENT_W / 2] * 2)
    grid.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))
    band.append(grid)
    band.append(Spacer(1, 10))
    band.append(HRFlowable(width=CONTENT_W, thickness=0.5, color=NAVY,
                            spaceAfter=8, spaceBefore=0))
    band.append(Paragraph(
        'Confidential Report. For Educational and Counselling Purposes Only.',
        STYLES['cover_band_disclaimer']
    ))

    # =======================================================================
    # Assemble: hero, then a spacer sized so the band content lands flush
    # inside the navy band painted on the canvas (see cover_background.py).
    # Measuring both blocks and filling the exact remainder (rather than a
    # guessed constant) keeps the band content correctly positioned even as
    # optional fields (DOB/age/school) change how tall the grid is.
    # =======================================================================
    from reportlab.pdfgen.canvas import Canvas
    import io
    _c = Canvas(io.BytesIO())
    _, hero_h = _listWrapOn(hero, CONTENT_W, _c)
    _, band_h = _listWrapOn(band, CONTENT_W, _c)
    # SimpleDocTemplate's default Frame reserves its own small internal
    # padding (on top of the doc margins already baked into CONTENT_H), so
    # filling the frame to exactly CONTENT_H measured here still overflowed
    # onto a second page in practice. Reserve a safety margin to guarantee
    # everything -- including the disclaimer line -- lands on page one.
    _SAFETY = 0.35 * inch
    filler = CONTENT_H - hero_h - band_h - _SAFETY
    # Guard against negative spacers (e.g. many optional fields present)
    # collapsing the layout -- clamp to a small minimum gap instead.
    filler = max(filler, 6)

    # The navy rectangle painted on the canvas (cover_background.py) is a
    # fixed shape decided before any flowable is measured, but band_h
    # varies with how many optional candidate fields are present (a 5th
    # field adds a 3rd grid row, ~0.6in taller). Register the exact height
    # this page's band content needs -- content bottom always lands
    # _SAFETY above the frame's bottom margin (0.7in) regardless of
    # hero/band size, since the stack always fills to CONTENT_H - _SAFETY
    # -- plus a cushion above the headline so it never touches the seam.
    _BOTTOM_MARGIN = 0.7 * inch
    _TOP_CUSHION = 0.3 * inch
    cover_background.set_band_height(_BOTTOM_MARGIN + _SAFETY + band_h + _TOP_CUSHION)

    story = list(hero)
    story.append(Spacer(1, filler))
    story += band
    return story
