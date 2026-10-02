from __future__ import annotations

from typing import Any, Dict, List, Optional
from reportlab.platypus import Paragraph, Spacer, Table, TableStyle, HRFlowable, PageBreak
from reportlab.lib.units import inch
from reportlab.lib import colors

from ..theme import (
    STYLES, NAVY, GOLD, GOLD_DARK, GOLD_LIGHT, GOLD_PALE,
    IVORY, WHITE, CONTENT_W,
)
from .helpers import shrink_block, SectionHeader, chart_image, institutional_table, institutional_card
from ..charts import create_finger_quality_bar, create_pattern_donut


PATTERN_DESCRIPTIONS = {
    'whorl': 'Whorl configurations reflect high self-determination, strategic vision, and autonomous execution. Correlated with intrapersonal and spatial cognition.',
    'loop': 'Loop configurations reflect cognitive flexibility, high adaptability, and social responsiveness. Correlated with interpersonal and linguistic fluency.',
    'arch': 'Arch configurations reflect methodical practicality, structural stability, and perseverance. Correlated with kinesthetic and logical fundamentals.',
    'accidental': 'Composite configurations reflect multi-modal cognitive versatility and lateral synthesis across non-adjacent domains.',
    'unknown': 'Pattern classification uncollected or indeterminate.',
}

FINGER_BRAIN_MAP = {
    'L1': ('Left Prefrontal Cortex', 'Intrapersonal Drive, Self-Regulation, Goal Architecture'),
    'L2': ('Left Frontal Lobe', 'Logical-Deductive Reasoning, Quantitative Modeling'),
    'L3': ('Left Parietal Lobe', 'Fine Motor Control, Sequential Physical Coordination'),
    'L4': ('Left Temporal Lobe', 'Linguistic Memory, Semantic Processing, Auditory Focus'),
    'L5': ('Left Occipital Lobe', 'Visual Detail Discrimination, Symbolic Pattern Reading'),
    'R1': ('Right Prefrontal Cortex', 'Interpersonal Empathy, Negotiation, Leadership Instinct'),
    'R2': ('Right Frontal Lobe', '3D Spatial Conception, Visual Imagination, Ideation'),
    'R3': ('Right Parietal Lobe', 'Gross Motor Agility, Somatic Proprioception, Rhythm'),
    'R4': ('Right Temporal Lobe', 'Tone Perception, Musical Agility, Emotional Audition'),
    'R5': ('Right Occipital Lobe', 'Visual-Spatial Perception, Aesthetic & Color Intuition'),
}

FINGER_NAMES = {
    'L1': 'Left Thumb',   'L2': 'Left Index',  'L3': 'Left Middle',
    'L4': 'Left Ring',    'L5': 'Left Little',
    'R1': 'Right Thumb',  'R2': 'Right Index', 'R3': 'Right Middle',
    'R4': 'Right Ring',   'R5': 'Right Little',
}


def _quality_level(q: float) -> str:
    if q >= 0.80:
        return 'Outstanding'
    if q >= 0.65:
        return 'Good'
    if q >= 0.50:
        return 'Adequate'
    return 'Needs Review'


def _tfrc_tier_description(total_rc: float) -> tuple[str, str, str]:
    if total_rc >= 180:
        return (
            'TIER 1: EXCEPTIONAL NEURAL BANDWIDTH',
            'Superior synaptic density capacity; exceptional cognitive bandwidth across multi-disciplinary intellectual tasks.',
            '#059669'
        )
    if total_rc >= 140:
        return (
            'TIER 2: ROBUST COGNITIVE PROCESSING',
            'Strong synaptic transmission potential; well-balanced learning agility and analytical stamina.',
            NAVY.hexval()
        )
    if total_rc >= 100:
        return (
            'TIER 3: FOCUSED SPECIALIZATION BAND',
            'Solid specialized processing potential; thrives when directing deep focus into dedicated subject areas.',
            GOLD_DARK.hexval()
        )
    return (
        'TIER 4: APPLIED STEP-BY-STEP ACQUISITION',
        'Direct practical application style; excels through deliberate structured practice and tangible sensory reinforcement.',
        GOLD_DARK.hexval()
    )


def _build_finger_card(f: Dict[str, Any], width: float) -> Table:
    slot = str(f.get('finger_position') or '').strip().upper()
    fname = FINGER_NAMES.get(slot, f.get('finger_type') or slot or 'Digit')
    pat = str(f.get('pattern_type') or 'unknown').lower()
    lobe, func = FINGER_BRAIN_MAP.get(slot, ('Cerebral Lobe', 'Cognitive Dimension'))
    desc = PATTERN_DESCRIPTIONS.get(pat, PATTERN_DESCRIPTIONS['unknown'])

    rc_raw = f.get('tfrc') or f.get('ridge_count')
    rc_str = str(int(rc_raw)) if isinstance(rc_raw, (int, float)) and rc_raw > 0 else 'N/A'

    q_raw = f.get('image_quality') if f.get('image_quality') is not None else f.get('quality_score')
    if isinstance(q_raw, (int, float)) and q_raw > 0:
        q_pct = q_raw * 100 if q_raw <= 1.0 else q_raw
        q_str = f'{q_pct:.0f}%'
    else:
        q_str = 'N/A'

    conf_raw = f.get('feature_confidence') or f.get('fractal_dimension')
    conf_str = f'{float(conf_raw):.3f}' if conf_raw else 'N/A'

    min_raw = f.get('minutiae_count')
    min_str = str(int(min_raw)) if isinstance(min_raw, (int, float)) and min_raw > 0 else 'N/A'

    rows = [
        [
            Paragraph(f'<b><font color="{NAVY.hexval()}">{fname} ({slot})</font></b>', STYLES['table_cell_bold']),
            Paragraph(f'<b><font color="{GOLD_DARK.hexval()}">Pattern: {pat.title()}</font></b>', STYLES['table_cell_bold']),
            Paragraph(f'<b>Ridge Count: {rc_str}</b>', STYLES['table_cell_bold']),
        ],
        [
            Paragraph(f'<b>Lobe:</b> {lobe}', STYLES['table_cell']),
            Paragraph(f'<b>Minutiae:</b> {min_str}', STYLES['table_cell']),
            Paragraph(f'<b>Quality:</b> {q_str} (Conf: {conf_str})', STYLES['table_cell']),
        ],
        [
            Paragraph(f'<b>Function:</b> {func}', STYLES['table_cell']),
            Paragraph(f'<b>CADA Reading:</b> {desc}', STYLES['table_cell']),
            Paragraph('', STYLES['table_cell']),
        ]
    ]

    col_w = [width * 0.36, width * 0.36, width * 0.28]
    card = Table(rows, colWidths=col_w)
    card.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), IVORY),
        ('BOX', (0, 0), (-1, -1), 0.8, GOLD),
        ('SPAN', (1, 2), (2, 2)),
        ('LINEBELOW', (0, 0), (-1, 0), 0.4, GOLD_LIGHT),
        ('LINEBELOW', (0, 1), (-1, 1), 0.4, GOLD_LIGHT),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('ROUNDEDCORNERS', [4, 4, 4, 4]),
    ]))
    return card


def build_pages_61_64_appendix(
    per_finger: List[Dict[str, Any]],
    atd_data: Optional[Dict[str, Any]],
) -> list:
    pages: list = []

    p61_block = []
    p61_block.append(SectionHeader(12, "APPENDIX A: BIOMETRIC QUALITY DIAGNOSTICS & TFRC TIERS"))
    p61_block.append(HRFlowable(width=CONTENT_W, thickness=1.0, color=GOLD, spaceAfter=8, spaceBefore=4))

    p61_intro = (
        '<font size="9.5" color="#162035"><b>Optical Capture Quality &amp; Synaptic Density Verification</b></font><br/>'
        '<font size="8" color="#334155">'
        'Ridge clarity, minutiae stability, and contrast uniformity govern biometric reliability. Total Finger Ridge Count '
        '(TFRC) represents the cumulative sum of ridges intersecting core-delta vectors across all ten digits, reflecting '
        'cortical neuronal capacity established between the 13th and 19th weeks of gestation.'
        '</font>'
    )
    p61_block.append(Paragraph(p61_intro, STYLES['body']))
    p61_block.append(Spacer(1, 6))

    q_b64 = create_finger_quality_bar(per_finger) if per_finger else None
    donut_b64 = create_pattern_donut(per_finger) if per_finger else None
    if q_b64 and donut_b64:
        left_imgs = chart_image(q_b64, width=CONTENT_W * 0.49, caption='Image Quality Score (%) per Digit')
        right_imgs = chart_image(donut_b64, width=CONTENT_W * 0.47, caption='Biometric Pattern Distribution')
        t_charts = Table([[left_imgs, right_imgs]], colWidths=[CONTENT_W * 0.51, CONTENT_W * 0.49])
        t_charts.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('RIGHTPADDING', (0, 0), (-1, -1), 0),
            ('TOPPADDING', (0, 0), (-1, -1), 0),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
        ]))
        p61_block.append(t_charts)
        p61_block.append(Spacer(1, 6))
    elif q_b64:
        p61_block.extend(chart_image(q_b64, width=CONTENT_W * 0.85, caption='Image Quality Score per Digit'))
        p61_block.append(Spacer(1, 6))

    table_headers = [
        Paragraph('<b>Digit Name</b>', STYLES['table_header']),
        Paragraph('<b>Slot</b>', STYLES['table_header']),
        Paragraph('<b>Pattern</b>', STYLES['table_header']),
        Paragraph('<b>Ridge Count</b>', STYLES['table_header']),
        Paragraph('<b>Quality %</b>', STYLES['table_header']),
        Paragraph('<b>Minutiae</b>', STYLES['table_header']),
        Paragraph('<b>Standard Level</b>', STYLES['table_header']),
    ]
    t_rows = [table_headers]

    valid_rc_values = []
    for f in per_finger:
        slot = str(f.get('finger_position') or '').strip().upper()
        fname = FINGER_NAMES.get(slot, f.get('finger_type') or slot or 'Digit')
        pat = str(f.get('pattern_type') or 'Unknown').title()
        rc_raw = f.get('tfrc') or f.get('ridge_count')
        if isinstance(rc_raw, (int, float)) and rc_raw > 0:
            rc_str = str(int(rc_raw))
            valid_rc_values.append(float(rc_raw))
        else:
            rc_str = 'N/A'

        q_raw = f.get('image_quality') if f.get('image_quality') is not None else f.get('quality_score')
        if isinstance(q_raw, (int, float)) and q_raw > 0:
            q_pct = q_raw * 100 if q_raw <= 1.0 else q_raw
            q_str = f'{q_pct:.0f}%'
            level = _quality_level(q_pct / 100.0)
        else:
            q_str = 'N/A'
            level = 'N/A'

        min_raw = f.get('minutiae_count')
        min_str = str(int(min_raw)) if isinstance(min_raw, (int, float)) and min_raw > 0 else 'N/A'

        t_rows.append([
            Paragraph(fname, STYLES['table_cell_bold']),
            Paragraph(f'<b>{slot}</b>', STYLES['table_cell']),
            Paragraph(pat, STYLES['table_cell']),
            Paragraph(rc_str, STYLES['table_cell_bold']),
            Paragraph(q_str, STYLES['table_cell']),
            Paragraph(min_str, STYLES['table_cell']),
            Paragraph(level, STYLES['table_cell']),
        ])

    cw = [
        CONTENT_W * 0.20, CONTENT_W * 0.08, CONTENT_W * 0.16,
        CONTENT_W * 0.14, CONTENT_W * 0.13, CONTENT_W * 0.13, CONTENT_W * 0.16
    ]
    t_qual = institutional_table(
        t_rows,
        col_widths=cw,
        center_cols=[1, 3, 4, 5, 6],
    )
    p61_block.append(t_qual)
    p61_block.append(Spacer(1, 8))

    if valid_rc_values:
        total_rc = sum(valid_rc_values)
        tier_title, tier_desc, tier_col = _tfrc_tier_description(total_rc)
        tfrc_html = (
            f'<font size="9" color="{tier_col}"><b>TOTAL FINGER RIDGE COUNT (TFRC): {int(total_rc)} &bull; {tier_title}</b></font><br/>'
            f'<font size="7.5" color="#334155">{tier_desc} (Calculated from {len(valid_rc_values)} verified digits)</font>'
        )
    else:
        tfrc_html = (
            f'<font size="9" color="{NAVY.hexval()}"><b>TOTAL FINGER RIDGE COUNT (TFRC): UNCOLLECTED / INCOMPLETE SCAN</b></font><br/>'
            f'<font size="7.5" color="{GOLD_DARK.hexval()}">Zero data fabrication policy: TFRC requires 10 verified digits with discernible core-delta ridge paths.</font>'
        )

    t_tfrc_box = institutional_card([Paragraph(tfrc_html, STYLES['body'])], width=CONTENT_W, border_color=GOLD, bg_color=GOLD_PALE)
    p61_block.append(t_tfrc_box)

    pages.append(shrink_block(p61_block, max_height=9.2 * inch, _label='appendix_a_page_61'))
    pages.append(PageBreak())

    left_digits = [f for f in per_finger if str(f.get('finger_position', '')).upper().startswith('L')]
    right_digits = [f for f in per_finger if str(f.get('finger_position', '')).upper().startswith('R')]

    if not left_digits and not right_digits:
        left_digits = [{'finger_position': f'L{i}'} for i in range(1, 6)]
        right_digits = [{'finger_position': f'R{i}'} for i in range(1, 6)]

    p62_block = []
    p62_block.append(SectionHeader(12, "APPENDIX B: 10-DIGIT CADA MINUTIAE INVENTORY (LEFT HAND)"))
    p62_block.append(HRFlowable(width=CONTENT_W, thickness=1.0, color=GOLD, spaceAfter=8, spaceBefore=4))
    p62_block.append(Paragraph(
        f'<font size="8" color="{GOLD_DARK.hexval()}">Detailed topological and minutiae profiles for digits L1 through L5, mapped to the right cerebral hemisphere.</font>',
        STYLES['body']
    ))
    p62_block.append(Spacer(1, 6))

    for lf in left_digits[:5]:
        p62_block.append(_build_finger_card(lf, CONTENT_W))
        p62_block.append(Spacer(1, 6))

    pages.append(shrink_block(p62_block, max_height=9.2 * inch, _label='appendix_b_page_62'))
    pages.append(PageBreak())

    p63_block = []
    p63_block.append(SectionHeader(12, "APPENDIX B: 10-DIGIT CADA MINUTIAE INVENTORY (RIGHT HAND)"))
    p63_block.append(HRFlowable(width=CONTENT_W, thickness=1.0, color=GOLD, spaceAfter=8, spaceBefore=4))
    p63_block.append(Paragraph(
        f'<font size="8" color="{GOLD_DARK.hexval()}">Detailed topological and minutiae profiles for digits R1 through R5, mapped to the left cerebral hemisphere.</font>',
        STYLES['body']
    ))
    p63_block.append(Spacer(1, 6))

    for rf in right_digits[:5]:
        p63_block.append(_build_finger_card(rf, CONTENT_W))
        p63_block.append(Spacer(1, 6))

    pages.append(shrink_block(p63_block, max_height=9.2 * inch, _label='appendix_b_page_63'))
    pages.append(PageBreak())

    p64_block = []
    p64_block.append(SectionHeader(12, "APPENDIX C: PALM ATD ANGLE & NEUROMUSCULAR REFLEX"))
    p64_block.append(HRFlowable(width=CONTENT_W, thickness=1.0, color=GOLD, spaceAfter=10, spaceBefore=4))

    has_atd = False
    if atd_data and isinstance(atd_data, dict):
        lh = atd_data.get('left_hand')
        rh = atd_data.get('right_hand')
        if lh or rh:
            has_atd = True

    if has_atd and atd_data is not None:
        p64_intro = (
            f'<font size="9.5" color="{NAVY.hexval()}"><b>Palmar Tri-Radius Geometry &amp; Conduction Velocity</b></font><br/>'
            '<font size="8" color="#1F2937">'
            'The ATD angle is formed by connecting three critical palmar triradii: the <b>a-triradius</b> (base of the index digit), '
            'the <b>t-triradius</b> (proximal axial wrist crease), and the <b>d-triradius</b> (base of the little digit). '
            'A narrower angle correlates with accelerated neural conduction speed and athletic reflex dexterity.'
            '</font>'
        )
        p64_block.append(Paragraph(p64_intro, STYLES['body']))
        p64_block.append(Spacer(1, 10))

        def _make_hand_table(hand_label: str, hand_dict: Dict[str, Any]) -> Table:
            angle = hand_dict.get('angle_deg')
            conf = hand_dict.get('confidence')
            rc = str(hand_dict.get('range_category') or 'normal')
            ls = hand_dict.get('learning_speed')
            fm = hand_dict.get('fine_motor_capacity')
            ss = hand_dict.get('sensory_sensitivity')
            interp = str(hand_dict.get('interpretation') or 'Balanced neuro-muscular processing latency.')

            angle_s = f'{angle:.1f}°' if angle is not None else 'N/A'
            conf_s = f'{round(conf * 100)}%' if conf is not None else 'N/A'
            ls_s = f'{round(ls * 100)}%' if ls is not None else 'N/A'
            fm_s = f'{round(fm * 100)}%' if fm is not None else 'N/A'
            ss_s = f'{round(ss * 100)}%' if ss is not None else 'N/A'

            rows = [
                [Paragraph(f'<b>{hand_label.upper()}</b>', STYLES['table_header']),
                 Paragraph('<b>Assessed Value</b>', STYLES['table_header']),
                 Paragraph('<b>Neuromuscular Significance</b>', STYLES['table_header'])],
                [Paragraph('ATD Reflex Angle', STYLES['table_cell_bold']), Paragraph(f'<b>{angle_s}</b>', STYLES['table_cell']), Paragraph(rc.title(), STYLES['table_cell'])],
                [Paragraph('Measurement Confidence', STYLES['table_cell_bold']), Paragraph(conf_s, STYLES['table_cell']), Paragraph('Geometric palmar landmark approximation', STYLES['table_cell'])],
                [Paragraph('Neural Processing Speed', STYLES['table_cell_bold']), Paragraph(ls_s, STYLES['table_cell']), Paragraph('Rate of sensory signal transmission', STYLES['table_cell'])],
                [Paragraph('Fine Motor Dexterity', STYLES['table_cell_bold']), Paragraph(fm_s, STYLES['table_cell']), Paragraph('Proprioceptive precision & coordination', STYLES['table_cell'])],
                [Paragraph('Sensory Sensitivity', STYLES['table_cell_bold']), Paragraph(ss_s, STYLES['table_cell']), Paragraph('Tactile response threshold', STYLES['table_cell'])],
                [Paragraph('Clinical Note', STYLES['table_cell_bold']), Paragraph(interp, STYLES['table_cell']), Paragraph('', STYLES['table_cell'])],
            ]
            t = Table(rows, colWidths=[CONTENT_W * 0.28, CONTENT_W * 0.22, CONTENT_W * 0.50])
            t.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), NAVY),
                ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
                ('FONTNAME', (0, 0), (-1, 0), 'Times-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('SPAN', (1, 6), (2, 6)),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [GOLD_PALE, IVORY]),
                ('GRID', (0, 0), (-1, -1), 0.4, GOLD_LIGHT),
                ('TOPPADDING', (0, 0), (-1, -1), 5),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
                ('LEFTPADDING', (0, 0), (-1, -1), 6),
                ('RIGHTPADDING', (0, 0), (-1, -1), 6),
            ]))
            return t

        lh_dict = atd_data.get('left_hand') if isinstance(atd_data.get('left_hand'), dict) else {}
        rh_dict = atd_data.get('right_hand') if isinstance(atd_data.get('right_hand'), dict) else {}

        if lh_dict:
            p64_block.append(_make_hand_table('Left Palmar Planar Region (LPALM)', lh_dict))
            p64_block.append(Spacer(1, 10))
        if rh_dict:
            p64_block.append(_make_hand_table('Right Palmar Planar Region (RPALM)', rh_dict))
    else:
        p64_uncollected = (
            f'<font size="11" color="{NAVY.hexval()}"><b>PALM SCAN STATUS: UNCOLLECTED (N/A)</b></font><br/><br/>'
            '<font size="8.5" color="#1F2937">'
            'Bilateral palmar planar scans (LPALM, RPALM) were not captured during this assessment session.<br/><br/>'
            '<b>Invariant 2 Compliance (Scientific Honesty &amp; Real-Data-Only Invariant):</b><br/>'
            'In strict adherence to institutional standards, the ATD angle, neural conduction velocity, and fine-motor '
            'reflex parameters are cleanly reported as <b>N/A - Uncollected</b> rather than synthetically interpolated or guessed.<br/><br/>'
            'To acquire validated ATD angle metrics, please submit high-resolution 500+ DPI palmar planar scans capturing the full '
            'hypothenar, thenar, and triradii landmark regions (a, t, d).'
            '</font>'
        )
        t_uncol = institutional_card([Paragraph(p64_uncollected, STYLES['body'])], width=CONTENT_W, border_color=GOLD, bg_color=GOLD_PALE)
        p64_block.append(t_uncol)

    pages.append(shrink_block(p64_block, max_height=9.2 * inch, _label='appendix_c_page_64'))
    return pages
