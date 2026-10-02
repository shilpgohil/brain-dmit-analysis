from __future__ import annotations

from typing import Any, Dict, List, Tuple

from reportlab.platypus import Paragraph, Spacer, Table, TableStyle, HRFlowable, PageBreak
from reportlab.lib.units import inch
from reportlab.lib import colors

from ..theme import (
    STYLES, NAVY, GOLD, GOLD_DARK, GOLD_LIGHT, GOLD_PALE,
    IVORY, WHITE, CONTENT_W,
)
from .helpers import shrink_block, SectionHeader, chart_image, institutional_table
from ..charts import generate_horizontal_progress_bars


def build_pages_20_22_academic_talents(report_data: Dict[str, Any]) -> list:
    pages: list = []
    mi = report_data.get('intelligence_scores', {})
    bm = report_data.get('brain_mapping', {})

    p20_block = []
    p20_block.append(SectionHeader(7, "CORE PERFORMANCE SECTORS: ACADEMIC VS. PHYSICAL"))
    p20_block.append(HRFlowable(width=CONTENT_W, thickness=1.0, color=GOLD, spaceAfter=12, spaceBefore=4))

    acad_score = float(mi.get('logical_mathematical', 0.74) * 0.5 + mi.get('linguistic', 0.70) * 0.5)
    phys_score = float(mi.get('bodily_kinesthetic', 0.68) * 0.7 + mi.get('spatial', 0.66) * 0.3)

    p20_intro = (
        '<font size="10.5" color="#162035"><b>Bilateral Aptitude: Intellectual Processing vs. Somatic Execution</b></font><br/>'
        '<font size="8.5" color="#334155">'
        'Human achievement depends upon harmonious integration between intellectual academic endurance and physical '
        'somatic stamina. This assessment contrasts the candidate’s capacity for sedentary conceptual focus against '
        'dynamic bodily-kinesthetic execution.'
        '</font>'
    )
    p20_block.append(Paragraph(p20_intro, STYLES['body']))
    p20_block.append(Spacer(1, 10))

    perf_items = [
        ('Academic Cognitive Aptitude', acad_score, 'High endurance in analytical calculation, reading comprehension, and structured testing.'),
        ('Physical / Somatic Agility', phys_score, 'Good fine-motor precision, bodily balance, athletic proprioception, and spatial reaction.'),
    ]
    p_chart_b64 = generate_horizontal_progress_bars("Bilateral Performance Sector Comparison", perf_items)
    p_imgs = chart_image(p_chart_b64, width=CONTENT_W * 0.88)
    if p_imgs:
        p20_block.extend(p_imgs)
        p20_block.append(Spacer(1, 12))

    t_recs_data = [
        [
            Paragraph('<b>Performance Domain</b>', STYLES['table_header']),
            Paragraph('<b>Capacity Index</b>', STYLES['table_header']),
            Paragraph('<b>Neurological Driver</b>', STYLES['table_header']),
            Paragraph('<b>Optimization Strategy</b>', STYLES['table_header']),
        ],
        [
            Paragraph('Academic Aptitude', STYLES['table_cell_bold']),
            Paragraph(f'<b>{acad_score*100:.1f}%</b>', STYLES['table_cell_bold']),
            Paragraph('Prefrontal & Frontal lobe synaptic density.', STYLES['table_cell']),
            Paragraph('Structured 45-minute deep focus sprints.', STYLES['table_cell']),
        ],
        [
            Paragraph('Physical Performance', STYLES['table_cell_bold']),
            Paragraph(f'<b>{phys_score*100:.1f}%</b>', STYLES['table_cell_bold']),
            Paragraph('Parietal lobe somatosensory motor cortex.', STYLES['table_cell']),
            Paragraph('Daily rhythmic athletics, swimming, or martial arts.', STYLES['table_cell']),
        ],
    ]
    t_recs = institutional_table(
        t_recs_data,
        col_widths=[CONTENT_W * 0.25, CONTENT_W * 0.16, CONTENT_W * 0.30, CONTENT_W * 0.29],
        center_cols=[1],
    )
    p20_block.append(t_recs)

    pages.append(shrink_block(p20_block, max_height=9.2 * inch, _label='performance_page_20'))
    pages.append(PageBreak())

    p21_block = []
    p21_block.append(SectionHeader(7, "RECOMMENDED ACADEMIC STREAM PATHWAYS"))
    p21_block.append(HRFlowable(width=CONTENT_W, thickness=1.0, color=GOLD, spaceAfter=12, spaceBefore=4))

    sci_score = float(mi.get('logical_mathematical', 0.74) * 0.6 + mi.get('spatial', 0.66) * 0.4)
    comm_score = float(mi.get('logical_mathematical', 0.74) * 0.5 + mi.get('interpersonal', 0.70) * 0.5)
    hum_score = float(mi.get('linguistic', 0.70) * 0.6 + mi.get('intrapersonal', 0.72) * 0.4)

    streams_data = [
        ('Science & Technology (STEM)', sci_score, 'Advanced physics, chemistry, engineering, computer sciences, mathematics.'),
        ('Commerce & Financial Management', comm_score, 'Economics, accounting, business administration, actuarial sciences.'),
        ('Humanities, Arts & Social Sciences', hum_score, 'Psychology, literature, law, political sciences, international relations.'),
    ]
    s_chart_b64 = generate_horizontal_progress_bars("Academic Stream Suitability Rankings", streams_data)
    s_imgs = chart_image(s_chart_b64, width=CONTENT_W * 0.88)
    if s_imgs:
        p21_block.extend(s_imgs)
        p21_block.append(Spacer(1, 10))

    stream_table_data = [
        [
            Paragraph('<b>Stream Pathway</b>', STYLES['table_header']),
            Paragraph('<b>Affinity</b>', STYLES['table_header']),
            Paragraph('<b>Suitability Level</b>', STYLES['table_header']),
            Paragraph('<b>Core Analytical Strengths</b>', STYLES['table_header']),
        ],
        [
            Paragraph('Science & Technology', STYLES['table_cell_bold']),
            Paragraph(f'<b>{sci_score*100:.1f}%</b>', STYLES['table_cell_bold']),
            Paragraph('<font color="#059669"><b>● High Priority Fit</b></font>', STYLES['table_cell']),
            Paragraph('Strong quantitative logic, pattern deduction, spatial modeling.', STYLES['table_cell']),
        ],
        [
            Paragraph('Commerce & Economics', STYLES['table_cell_bold']),
            Paragraph(f'<b>{comm_score*100:.1f}%</b>', STYLES['table_cell_bold']),
            Paragraph('<font color="#059669"><b>● High Priority Fit</b></font>', STYLES['table_cell']),
            Paragraph('Numerical acumen combined with strategic commercial awareness.', STYLES['table_cell']),
        ],
        [
            Paragraph('Humanities & Social Sciences', STYLES['table_cell_bold']),
            Paragraph(f'<b>{hum_score*100:.1f}%</b>', STYLES['table_cell_bold']),
            Paragraph('<font color="#D97706"><b>● Secondary Alternative</b></font>', STYLES['table_cell']),
            Paragraph('Reflective philosophy, narrative articulation, social observation.', STYLES['table_cell']),
        ],
    ]
    t_stream = institutional_table(
        stream_table_data,
        col_widths=[CONTENT_W * 0.28, CONTENT_W * 0.14, CONTENT_W * 0.24, CONTENT_W * 0.34],
        center_cols=[1],
    )
    p21_block.append(t_stream)

    pages.append(shrink_block(p21_block, max_height=9.2 * inch, _label='streams_page_21'))
    pages.append(PageBreak())

    p22_block = []
    p22_block.append(SectionHeader(7, "SKILL & CO-CURRICULAR TALENT MAPPING (14 DOMAINS)"))
    p22_block.append(HRFlowable(width=CONTENT_W, thickness=1.0, color=GOLD, spaceAfter=10, spaceBefore=4))

    p22_intro = (
        '<font size="10" color="#162035"><b>Holistic Extra-Curricular Potential Matrix</b></font><br/>'
        '<font size="8.5" color="#334155">'
        'Talent development accelerates when co-curricular hobbies engage the exact cerebral lobe circuits that support '
        'primary academic and executive functions. The table below maps 14 specialized extra-curricular activity domains.'
        '</font>'
    )
    p22_block.append(Paragraph(p22_intro, STYLES['body']))
    p22_block.append(Spacer(1, 8))

    log = float(mi.get('logical_mathematical', 0.74))
    mus = float(mi.get('musical', 0.68))
    kin = float(mi.get('bodily_kinesthetic', 0.70))
    spa = float(mi.get('spatial', 0.68))
    lin = float(mi.get('linguistic', 0.72))
    nat = float(mi.get('naturalistic', 0.65))
    intra = float(mi.get('intrapersonal', 0.75))
    inter = float(mi.get('interpersonal', 0.73))

    talents = [
        ('01', 'Vocal Music', mus * 0.90 + lin * 0.10),
        ('02', 'Instrumental Music', mus * 0.80 + kin * 0.20),
        ('03', 'Performing Arts / Dance', kin * 0.75 + mus * 0.25),
        ('04', 'Yoga & Mindfulness', intra * 0.70 + kin * 0.30),
        ('05', 'Foreign Languages', lin * 0.85 + inter * 0.15),
        ('06', 'Strategic Games (Chess)', log * 0.75 + spa * 0.25),
        ('07', 'Robotics & Coding', log * 0.70 + spa * 0.30),
        ('08', 'Equestrian Sports', kin * 0.70 + nat * 0.30),
        ('09', 'Swimming & Aquatics', kin * 0.85 + intra * 0.15),
        ('10', 'Target Shooting / Archery', spa * 0.65 + kin * 0.35),
        ('11', 'Fine Arts & Design', spa * 0.80 + nat * 0.20),
        ('12', 'Visual Photography', spa * 0.85 + intra * 0.15),
        ('13', 'Dramatics & Public Speaking', lin * 0.60 + inter * 0.40),
        ('14', 'Horticulture / Earth Studies', nat * 0.85 + kin * 0.15),
    ]

    t_rows = [
        [
            Paragraph('<b>S.No.</b>', STYLES['table_header']),
            Paragraph('<b>Activity Domain</b>', STYLES['table_header']),
            Paragraph('<b>Match %</b>', STYLES['table_header']),
            Paragraph('<b>S.No.</b>', STYLES['table_header']),
            Paragraph('<b>Activity Domain</b>', STYLES['table_header']),
            Paragraph('<b>Match %</b>', STYLES['table_header']),
        ]
    ]

    for i in range(7):
        s1, n1, v1 = talents[i]
        s2, n2, v2 = talents[i + 7]
        t_rows.append([
            Paragraph(s1, STYLES['table_cell_bold']),
            Paragraph(n1, STYLES['table_cell']),
            Paragraph(f'<b>{v1*100:.0f}%</b>', STYLES['table_cell_bold']),
            Paragraph(s2, STYLES['table_cell_bold']),
            Paragraph(n2, STYLES['table_cell']),
            Paragraph(f'<b>{v2*100:.0f}%</b>', STYLES['table_cell_bold']),
        ])

    cw22 = [CONTENT_W * 0.08, CONTENT_W * 0.32, CONTENT_W * 0.10,
            CONTENT_W * 0.08, CONTENT_W * 0.32, CONTENT_W * 0.10]
    t_talents = institutional_table(
        t_rows,
        col_widths=cw22,
        center_cols=[0, 2, 3, 5],
    )
    p22_block.append(t_talents)

    pages.append(shrink_block(p22_block, max_height=9.2 * inch, _label='talents_page_22'))

    return pages
