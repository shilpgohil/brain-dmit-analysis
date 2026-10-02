from __future__ import annotations

from typing import Any, Dict

from reportlab.platypus import Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.units import inch
from reportlab.lib import colors

from ..theme import (
    STYLES, NAVY, GOLD, GOLD_DARK, GOLD_LIGHT, GOLD_PALE,
    IVORY, WHITE, CONTENT_W,
)
from .helpers import shrink_block, SectionHeader, sub_heading, chart_image, institutional_table, institutional_card
from ..charts import create_hemisphere_bar


def build_page_16_brain_architecture(report_data: Dict[str, Any]) -> list:
    block: list = []
    block.append(SectionHeader(5, "CEREBRAL RIDGE DENSITY & NEURAL POTENTIAL DISTRIBUTION"))
    block.append(HRFlowable(width=CONTENT_W, thickness=1.0, color=GOLD, spaceAfter=8, spaceBefore=4))

    bm = report_data.get('brain_mapping', {})
    lobe_hemi = bm.get('lobe_hemispheres', {})

    raw_scores = [
        ('Left Pre-Frontal', 'Planning, Self-Motivation, Decision-Making',
         lobe_hemi.get('left_prefrontal') or bm.get('prefrontal_l') or 10.5),
        ('Left Frontal', 'Logical Reasoning, Analytical & Mathematical Thought',
         lobe_hemi.get('left_frontal') or bm.get('frontal_l') or 11.2),
        ('Left Parietal', 'Fine Motor Control, Written Expression, Dexterity',
         lobe_hemi.get('left_parietal') or bm.get('parietal_l') or 10.0),
        ('Left Temporal', 'Language Acquisition, Phonetic Processing, Verbal Memory',
         lobe_hemi.get('left_temporal') or bm.get('temporal_l') or 10.2),
        ('Left Occipital', 'Visual Identification, Reading Focus, Detail Observation',
         lobe_hemi.get('left_occipital') or bm.get('occipital_l') or 10.0),
        ('Right Pre-Frontal', 'Interpersonal Intuition, Leadership, Negotiation',
         lobe_hemi.get('right_prefrontal') or bm.get('prefrontal_r') or 10.4),
        ('Right Frontal', 'Visual Imagination, 3D Spatial Thinking, Creativity',
         lobe_hemi.get('right_frontal') or bm.get('frontal_r') or 10.2),
        ('Right Parietal', 'Gross Motor Control, Body Kinesthetics, Athleticism',
         lobe_hemi.get('right_parietal') or bm.get('parietal_r') or 9.8),
        ('Right Temporal', 'Auditory Perception, Tone Recognition, Musical Aptitude',
         lobe_hemi.get('right_temporal') or bm.get('temporal_r') or 9.2),
        ('Right Occipital', 'Visual-Spatial Perception, Aesthetic & Art Processing',
         lobe_hemi.get('right_occipital') or bm.get('occipital_r') or 8.0),
    ]

    total_val = sum(float(x[2]) for x in raw_scores) or 100.0
    normalized_scores = []
    for hemi_lobe, func, raw_val in raw_scores:
        pct = (float(raw_val) / total_val) * 100.0
        normalized_scores.append((hemi_lobe, func, pct))

    left_total_pct = sum(x[2] for x in normalized_scores[:5])
    right_total_pct = sum(x[2] for x in normalized_scores[5:])

    intro_text = (
        'Brain hemisphere dominance reflects the proportion to which the left (analytical, execution) '
        'or right (conceptual, holistic) hemisphere governs cognitive information processing. Contralateral '
        'wiring established during neurogenesis links right-hand digits to left-hemisphere lobes and left-hand '
        'digits to right-hemisphere lobes.'
    )
    block.append(Paragraph(intro_text, STYLES['body']))
    block.append(Spacer(1, 4))

    hb64 = create_hemisphere_bar(left_total_pct / 100.0, right_total_pct / 100.0)
    c_imgs = chart_image(hb64, width=CONTENT_W * 0.94, caption="Bilateral Cerebral Hemisphere Distribution")
    if c_imgs:
        block.extend(c_imgs)
        block.append(Spacer(1, 6))

    block.extend(sub_heading("10-Lobe Cerebral Ridge Density & Capacity Distribution"))

    table_rows = [
        [
            Paragraph('<b>Cerebral Lobe &amp; Side</b>', STYLES['table_header']),
            Paragraph('<b>Associated Cognitive Function</b>', STYLES['table_header']),
            Paragraph('<b>Estimated Ridge Density</b>', STYLES['table_header']),
            Paragraph('<b>Dominance</b>', STYLES['table_header']),
        ]
    ]

    for i, (hemi_lobe, func, pct) in enumerate(normalized_scores):
        is_left = i < 5
        dom_label = 'Left Focus' if is_left else 'Right Focus'
        name_p = Paragraph(f'<b>{hemi_lobe}</b>', STYLES['table_cell_bold'])
        func_p = Paragraph(func, STYLES['table_cell'])
        pct_p = Paragraph(f'<b>{pct:.1f}%</b>', STYLES['table_cell_bold'])
        dom_p = Paragraph(dom_label, STYLES['table_cell'])
        table_rows.append([name_p, func_p, pct_p, dom_p])

    cw = [CONTENT_W * 0.28, CONTENT_W * 0.44, CONTENT_W * 0.16, CONTENT_W * 0.12]
    t_lobes = institutional_table(table_rows, col_widths=cw, center_cols=[2, 3])
    block.append(t_lobes)
    block.append(Spacer(1, 6))

    footnote = (
        f'<b>ANALYTICAL INTERPRETATION:</b> Left Hemisphere capacity accounts for {left_total_pct:.1f}% '
        f'(sequential logic, precision, execution). Right Hemisphere capacity accounts for {right_total_pct:.1f}% '
        '(holistic integration, creative synthesis). Balanced bilateral distribution indicates versatile cognitive equilibrium.'
    )
    p_footnote = Paragraph(f'<font size="7.5" color="{NAVY.hexval()}">{footnote}</font>', STYLES['body'])
    card_footnote = institutional_card([p_footnote], width=CONTENT_W, border_color=GOLD, bg_color=GOLD_PALE)
    block.append(card_footnote)

    return [shrink_block(block, max_height=9.2 * inch, _label='brain_architecture_page_16')]
