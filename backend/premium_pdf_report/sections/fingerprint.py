"""
Section 5 : Fingerprint Collection Quality
Section 6 : Finger-wise Pattern Analysis
"""

from typing import Dict, Any, List
from reportlab.platypus import Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.units import inch

from ..theme import (STYLES, NAVY, GOLD, GOLD_DARK, GOLD_LIGHT, GOLD_PALE,
                     IVORY, WHITE, GREEN_STRONG, AMBER_MID, TERRACOTTA,
                     CONTENT_W, score_color)
from .helpers import section_header, section_header_plain, sub_heading, chart_image, shrink_block


PATTERN_DESCRIPTIONS = {
    'whorl': 'Whorl patterns indicate a strong sense of self, strategic thinking, and goal-oriented behaviour. Associated with high spatial and intrapersonal intelligence.',
    'loop': 'Loop patterns are the most common type, indicating flexibility, adaptability, and social awareness. Associated with interpersonal and linguistic intelligence.',
    'arch': 'Arch patterns suggest reliability, practicality, and persistence. Associated with bodily-kinesthetic and logical-mathematical intelligence.',
    'accidental': 'Composite/Accidental patterns combine traits of multiple pattern types, indicating versatility, creativity, and multi-dimensional thinking.',
    'unknown': 'Pattern classification pending further analysis.',
}

FINGER_BRAIN_MAP = {
    'R1': ('Prefrontal Cortex', 'Leadership, Executive Function, Decision-Making'),
    'R2': ('Frontal Lobe',      'Logic, Analysis, Planning, Sequential Thinking'),
    'R3': ('Parietal Lobe',     'Spatial Awareness, Sensory Integration'),
    'R4': ('Temporal Lobe',     'Language, Music, Memory, Emotional Recall'),
    'R5': ('Occipital Lobe',    'Visual Processing, Pattern Recognition, Creativity'),
    'L1': ('Prefrontal Cortex', 'Willpower, Emotional Regulation, Self-Control'),
    'L2': ('Frontal Lobe',      'Critical Thinking, Analytical Depth'),
    'L3': ('Parietal Lobe',     'Tactile Intelligence, Kinaesthetic Ability'),
    'L4': ('Temporal Lobe',     'Auditory Processing, Social Communication'),
    'L5': ('Occipital Lobe',    'Artistic Vision, Aesthetic Sensitivity'),
}

FINGER_NAMES = {
    'R1': 'Right Thumb',   'R2': 'Right Index',  'R3': 'Right Middle',
    'R4': 'Right Ring',    'R5': 'Right Little',
    'L1': 'Left Thumb',    'L2': 'Left Index',   'L3': 'Left Middle',
    'L4': 'Left Ring',     'L5': 'Left Little',
}


def _quality_level(q: float) -> str:
    if q >= 0.80: return 'Outstanding'
    if q >= 0.65: return 'Good'
    if q >= 0.50: return 'Adequate'
    return 'Needs Review'


def build_fingerprint_quality(per_finger: List[Dict[str, Any]]) -> list:
    """Section 5 - quality table + bar chart."""
    story = []
    # Whole section (header included) goes in one shrink block: Section 4
    # no longer forces a PageBreak before this section, so it may start
    # partway down a page with limited room left. Keeping it atomic means
    # it either fits in place or moves whole to a fresh page — never splits
    # its table and strands a couple of rows above a blank page.
    block = []
    block += section_header_plain(5, 'Fingerprint Collection and Quality Analysis')
    block.append(Spacer(1, 6))

    block.append(Paragraph(
        'The following table summarises the biometric quality metrics for each '
        'fingerprint collected. Ridge clarity, minutiae extraction confidence, and '
        'overall quality determine the accuracy of the intelligence mapping.',
        STYLES['body']
    ))
    block.append(Spacer(1, 6))

    # Quality chart + Pattern distribution side by side
    from ..charts import create_finger_quality_bar, create_pattern_donut
    from .helpers import two_col
    q_b64       = create_finger_quality_bar(per_finger)
    donut_b64   = create_pattern_donut(per_finger)
    if q_b64 and donut_b64:
        left_items  = chart_image(q_b64,     width=CONTENT_W * 0.50,
                                  caption='Quality Score per Finger')
        right_items = chart_image(donut_b64, width=CONTENT_W * 0.46,
                                  caption='Pattern Type Distribution')
        block.append(two_col(left_items, right_items,
                             left_w=CONTENT_W * 0.52, right_w=CONTENT_W * 0.44))
    elif q_b64:
        block += chart_image(q_b64, caption='Fingerprint Quality Score per Finger')
    elif donut_b64:
        block += chart_image(donut_b64, caption='Pattern Type Distribution')
    block.append(Spacer(1, 8))

    # Quality table
    block += sub_heading('Detailed Quality Metrics')
    header_row = [Paragraph(h, STYLES['table_header']) for h in
                  ['Finger', 'Slot', 'Pattern', 'Ridge Count',
                   'Quality %', 'Minutiae', 'Level']]
    rows = [header_row]
    for f in per_finger:
        slot  = f.get('finger_position', '')
        fname = FINGER_NAMES.get(slot, f.get('finger_type', slot))
        pat   = str(f.get('pattern_type') or 'Unknown').title()
        rc_raw = f.get('tfrc') or f.get('ridge_count')
        rc    = str(int(rc_raw)) if isinstance(rc_raw, (int, float)) and rc_raw else 'N/A'
        q_raw = f.get('image_quality') if f.get('image_quality') is not None \
                else f.get('quality_score')
        if isinstance(q_raw, (int, float)) and q_raw > 0:
            q_pct = q_raw * 100 if q_raw <= 1.0 else q_raw
            q_str = f'{q_pct:.0f}%'
            level = _quality_level(q_pct / 100.0)
        else:
            q_str = 'N/A'
            level = 'N/A'
        min_raw = f.get('minutiae_count')
        min_c = str(int(min_raw)) if isinstance(min_raw, (int, float)) and min_raw else 'N/A'
        rows.append([Paragraph(c, STYLES['table_cell']) for c in
                     [fname, slot, pat, rc, q_str, min_c, level]])

    cw = [CONTENT_W * 0.20, CONTENT_W * 0.09, CONTENT_W * 0.13,
          CONTENT_W * 0.13, CONTENT_W * 0.12, CONTENT_W * 0.12, CONTENT_W * 0.17]
    qt = Table(rows, colWidths=cw, repeatRows=1, splitByRow=1)
    qt.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), NAVY),
        ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [GOLD_PALE, IVORY]),
        ('FONTSIZE', (0, 0), (-1, -1), 8.5),
        ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('GRID', (0, 0), (-1, -1), 0.4, GOLD_LIGHT),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))
    block.append(qt)

    # TFRC summary — only show when real ridge count data is present
    rc_values = [float(f.get('tfrc') or f.get('ridge_count') or 0)
                 for f in per_finger
                 if isinstance(f.get('tfrc') or f.get('ridge_count'), (int, float))
                 and (f.get('tfrc') or f.get('ridge_count', 0)) > 0]
    if rc_values:
        total_rc = sum(rc_values)
        block.append(Spacer(1, 8))
        block.append(Paragraph(
            f'Total Finger Ridge Count (TFRC): {int(total_rc)}   '
            f'Fingers Analysed: {len(per_finger)}',
            STYLES['label']
        ))

    story.append(shrink_block(block, _label='fingerprint_quality'))
    return story


def _finger_card(f: Dict[str, Any], width: float) -> Table:
    """Build a single compact per-finger detail card at the given width."""
    slot  = f.get('finger_position', '')
    fname = FINGER_NAMES.get(slot, f.get('finger_type', slot))
    pat   = str(f.get('pattern_type', 'unknown')).lower()
    lobe, func = FINGER_BRAIN_MAP.get(slot, ('Brain Region', 'Cognitive Function'))
    desc  = PATTERN_DESCRIPTIONS.get(pat, PATTERN_DESCRIPTIONS['unknown'])
    q_raw = f.get('image_quality') if f.get('image_quality') is not None \
            else f.get('quality_score')
    if isinstance(q_raw, (int, float)) and q_raw > 0:
        q_pct = q_raw * 100 if q_raw <= 1.0 else q_raw
        q_str = f'{q_pct:.0f}%'
    else:
        q_str = 'N/A'
    conf_raw = f.get('feature_confidence') or f.get('fractal_dimension')
    conf_str = (f'{float(conf_raw):.3f}' if conf_raw else 'N/A')

    card_rows = [
        [Paragraph(f'{fname} ({slot})', STYLES['table_cell_bold']),
         Paragraph(pat.title(), STYLES['table_cell'])],
        [Paragraph('Brain Lobe', STYLES['table_cell_bold']),
         Paragraph(lobe, STYLES['table_cell'])],
        [Paragraph('Function', STYLES['table_cell_bold']),
         Paragraph(func, STYLES['table_cell'])],
        [Paragraph('Quality / Fractal', STYLES['table_cell_bold']),
         Paragraph(f'{q_str}   /   {conf_str}', STYLES['table_cell'])],
        [Paragraph('Interpretation', STYLES['table_cell_bold']),
         Paragraph(desc, STYLES['body'])],
    ]
    label_w = width * 0.30
    cw = [label_w, width - label_w]
    card = Table(card_rows, colWidths=cw)
    card.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), GOLD_PALE),
        ('ROWBACKGROUNDS', (0, 0), (-1, -1), [GOLD_PALE, IVORY]),
        ('BOX', (0, 0), (-1, -1), 1.2, GOLD),
        ('LINEBELOW', (0, 0), (-1, -2), 0.3, GOLD_LIGHT),
        ('FONTNAME', (0, 0), (0, -1), 'Times-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 8.5),
        ('LEFTPADDING', (0, 0), (-1, -1), 7),
        ('RIGHTPADDING', (0, 0), (-1, -1), 7),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    return card


def build_finger_analysis(per_finger: List[Dict[str, Any]]) -> list:
    """
    Section 6 - per-finger analysis cards.

    Rendered as a 2-per-row grid (rather than one full-width card each)
    so 10 fingers pack into roughly half as many pages. The previous
    single-column layout fit exactly 3 cards per page, so 10 cards spilled
    3+3+3+1 across four pages — the last holding a single card above a
    page that was ~90% blank. Pairing cards side by side fills each page
    far more evenly and removes that near-empty trailing page.
    """
    from reportlab.platypus import KeepTogether
    story = []
    story += section_header(6, 'Finger-wise Pattern Analysis')
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        'Each finger\'s ridge pattern is linked to a specific brain region. '
        'The following analysis describes the cognitive and behavioural '
        'significance of the pattern detected on each finger.',
        STYLES['body']
    ))
    story.append(Spacer(1, 10))

    gutter = 0.24 * inch
    col_w = (CONTENT_W - gutter) / 2

    for i in range(0, len(per_finger), 2):
        pair = per_finger[i:i + 2]
        left_card = _finger_card(pair[0], col_w)
        if len(pair) == 2:
            right_card = _finger_card(pair[1], col_w)
            row = Table([[left_card, right_card]],
                        colWidths=[col_w, col_w], hAlign='LEFT')
            row.setStyle(TableStyle([
                ('LEFTPADDING', (0, 0), (-1, -1), 0),
                ('RIGHTPADDING', (0, 0), (0, 0), gutter),
                ('RIGHTPADDING', (1, 0), (1, 0), 0),
                ('TOPPADDING', (0, 0), (-1, -1), 0),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ]))
            story.append(KeepTogether([row, Spacer(1, 10)]))
        else:
            story.append(KeepTogether([left_card, Spacer(1, 10)]))

    return story
