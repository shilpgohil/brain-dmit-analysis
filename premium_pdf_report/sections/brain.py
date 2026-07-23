"""
Section 7 : Brain Hemisphere Analysis
Section 8 : Brain Lobe Mapping
"""

from typing import Dict, Any
from reportlab.platypus import Paragraph, Spacer, Table, TableStyle
from reportlab.lib.units import inch

from ..theme import (STYLES, NAVY, GOLD, GOLD_DARK, GOLD_LIGHT, GOLD_PALE,
                     IVORY, WHITE, CONTENT_W)
from .helpers import section_header, sub_heading, chart_image

LOBE_INFO = {
    'prefrontal_lobe': (
        'Prefrontal Cortex',
        'Executive function, decision-making, planning, leadership, impulse control.',
        'High activity indicates strong leadership potential, goal-setting ability, and strategic thinking.'
    ),
    'posterior_frontal': (
        'Frontal Lobe',
        'Motor control, language production, logical reasoning, analytical thinking.',
        'High activity supports strong analytical ability, verbal fluency, and sequential learning.'
    ),
    'parietal_lobe': (
        'Parietal Lobe',
        'Spatial processing, sensory integration, mathematical reasoning.',
        'High activity indicates strong spatial intelligence, problem-solving, and kinaesthetic ability.'
    ),
    'temporal_lobe': (
        'Temporal Lobe',
        'Auditory processing, memory formation, language comprehension, emotional processing.',
        'High activity supports musical aptitude, language skills, and strong memory retention.'
    ),
    'occipital_lobe': (
        'Occipital Lobe',
        'Visual processing, pattern recognition, artistic and creative perception.',
        'High activity indicates strong visual intelligence, artistic potential, and creative thinking.'
    ),
}

LEFT_TRAITS = [
    'Logical and analytical thinking',
    'Sequential and structured reasoning',
    'Language and verbal communication',
    'Mathematical computation',
    'Detail orientation and precision',
    'Fact-based decision-making',
]

RIGHT_TRAITS = [
    'Creativity and imagination',
    'Intuition and holistic thinking',
    'Visual and spatial reasoning',
    'Musical and artistic expression',
    'Emotional processing and empathy',
    'Pattern recognition and innovation',
]


def build_brain_hemisphere(brain_mapping: Dict[str, float]) -> list:
    story = []
    story += section_header(7, 'Brain Hemisphere Analysis')
    story.append(Spacer(1, 6))

    l = brain_mapping.get('left_hemisphere', brain_mapping.get('left_hemisphere_bias'))
    r = brain_mapping.get('right_hemisphere', brain_mapping.get('right_hemisphere_bias'))
    # Use actual values; only fall back to 0.5 if genuinely absent
    l = l if isinstance(l, (int, float)) and l > 0 else None
    r = r if isinstance(r, (int, float)) and r > 0 else None
    if l is None and r is None:
        l_pct, r_pct = 0.5, 0.5
    else:
        l = l or 0.0
        r = r or 0.0
        total = l + r if (l + r) > 0 else 1.0
        l_pct = l / total
        r_pct = r / total

    story.append(Paragraph(
        'Brain hemisphere dominance reflects the degree to which the left (analytical) '
        'or right (creative) hemisphere contributes to your natural cognitive style. '
        'A balanced score indicates whole-brain thinking ability.',
        STYLES['body']
    ))
    story.append(Spacer(1, 6))

    from ..charts import create_hemisphere_bar
    hb64 = create_hemisphere_bar(l_pct, r_pct)
    story += chart_image(hb64, caption='Brain Hemisphere Dominance Distribution')
    story.append(Spacer(1, 8))

    dom = 'Left' if l_pct >= r_pct else 'Right'
    balance = abs(l_pct - r_pct)
    balance_desc = ('Well-balanced (whole-brain thinker)' if balance < 0.10
                    else f'{dom}-brain dominant')

    story += sub_heading('Hemisphere Profile Summary')
    sum_rows = [
        [Paragraph('Parameter', STYLES['table_header']),
         Paragraph('Value', STYLES['table_header'])],
        ['Left Hemisphere Activity', f'{l_pct*100:.1f}%'],
        ['Right Hemisphere Activity', f'{r_pct*100:.1f}%'],
        ['Dominant Hemisphere', dom],
        ['Balance Classification', balance_desc],
    ]
    for i in range(1, len(sum_rows)):
        sum_rows[i] = [Paragraph(str(c), STYLES['table_cell'])
                       for c in sum_rows[i]]
    cw = [CONTENT_W * 0.50, CONTENT_W * 0.46]
    ht = Table(sum_rows, colWidths=cw)
    ht.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), NAVY),
        ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [GOLD_PALE, IVORY]),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 0.4, GOLD_LIGHT),
    ]))
    story.append(ht)
    story.append(Spacer(1, 10))

    # Trait columns
    story += sub_heading('Hemisphere Trait Profiles')
    trait_rows = [[
        Paragraph('Left Brain Traits', STYLES['table_header']),
        Paragraph('Right Brain Traits', STYLES['table_header']),
    ]]
    max_r = max(len(LEFT_TRAITS), len(RIGHT_TRAITS))
    for i in range(max_r):
        l_trait = LEFT_TRAITS[i] if i < len(LEFT_TRAITS) else ''
        r_trait = RIGHT_TRAITS[i] if i < len(RIGHT_TRAITS) else ''
        trait_rows.append([
            Paragraph(f'  {l_trait}', STYLES['table_cell']),
            Paragraph(f'  {r_trait}', STYLES['table_cell']),
        ])
    tt = Table(trait_rows, colWidths=[CONTENT_W * 0.48, CONTENT_W * 0.48])
    tt.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, 0), NAVY),
        ('BACKGROUND', (1, 0), (1, 0), GOLD_DARK),
        ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [GOLD_PALE, IVORY]),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 0.4, GOLD_LIGHT),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(tt)

    return story


def build_brain_lobes(brain_mapping: Dict[str, float]) -> list:
    story = []
    story += section_header(8, 'Brain Lobe Mapping')
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        'Brain lobe activity percentages are derived from the aggregate ridge pattern '
        'analysis across all ten fingerprints. Each lobe governs distinct cognitive '
        'functions and intelligence clusters.',
        STYLES['body']
    ))
    story.append(Spacer(1, 6))

    from ..charts import create_brain_lobe_bar
    bb64 = create_brain_lobe_bar(brain_mapping)
    story += chart_image(bb64, caption='Brain Lobe Activity Profile')
    story.append(Spacer(1, 8))

    story += sub_heading('Lobe Activity and Interpretation')
    header_row = [Paragraph(h, STYLES['table_header']) for h in
                  ['Brain Area', 'Function', 'Activity', 'Interpretation']]
    rows = [header_row]
    for key, (name, func, interp) in LOBE_INFO.items():
        val = brain_mapping.get(key)
        val_str = f'{val*100:.0f}%' if isinstance(val, (int, float)) and val > 0 else 'N/A'
        rows.append([
            Paragraph(name, STYLES['table_cell_bold']),
            Paragraph(func, STYLES['table_cell']),
            Paragraph(val_str, STYLES['table_cell_bold']),
            Paragraph(interp, STYLES['table_cell']),
        ])
    cw = [CONTENT_W * 0.21, CONTENT_W * 0.28, CONTENT_W * 0.10, CONTENT_W * 0.37]
    lt = Table(rows, colWidths=cw, repeatRows=1, splitByRow=1)
    lt.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), NAVY),
        ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [GOLD_PALE, IVORY]),
        ('FONTSIZE', (0, 0), (-1, -1), 8.5),
        ('ALIGN', (2, 0), (2, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 0.4, GOLD_LIGHT),
        ('LEFTPADDING', (0, 0), (-1, -1), 7),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(lt)

    return story
