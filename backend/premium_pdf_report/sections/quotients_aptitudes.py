from __future__ import annotations

from typing import Any, Dict, List, Tuple

from reportlab.platypus import Paragraph, Spacer, Table, TableStyle, HRFlowable, PageBreak
from reportlab.lib.units import inch
from reportlab.lib import colors

from ..theme import (
    STYLES, NAVY, GOLD, GOLD_DARK, GOLD_LIGHT, GOLD_PALE,
    IVORY, WHITE, CONTENT_W, score_color,
)
from .helpers import shrink_block, SectionHeader, sub_heading, chart_image, institutional_table, institutional_card
from ..charts import (
    generate_quotient_10_radar,
    generate_horizontal_progress_bars,
    create_gauge_chart,
)
from ..assets.boho_vectors import draw_boho_quotients_emblem


def build_pages_17_19_quotients(report_data: Dict[str, Any], quotients: Dict[str, float]) -> list:
    pages: list = []
    mi = report_data.get('intelligence_scores', {})
    bm = report_data.get('brain_mapping', {})

    p17_block = []
    p17_block.append(SectionHeader(6, "CRITICAL ACADEMIC SUBJECT ORIENTATIONS"))
    p17_block.append(HRFlowable(width=CONTENT_W, thickness=1.0, color=GOLD, spaceAfter=10, spaceBefore=4))

    stem_val = float(mi.get('naturalistic', 0.68) * 0.4 + mi.get('logical_mathematical', 0.72) * 0.6)
    math_val = float(mi.get('logical_mathematical', 0.75))
    ling_val = float(mi.get('linguistic', 0.70))

    categories = [
        ('STEM & Natural Sciences', stem_val, 'High empirical curiosity; thrives in laboratory research and system modeling.'),
        ('Quantitative & Mathematical Logic', math_val, 'Superior deductive reasoning; rapid abstraction and numerical precision.'),
        ('Linguistics & Communication', ling_val, 'Articulate semantic comprehension; high verbal agility and expressive syntax.'),
    ]

    p17_intro = (
        'Subject affinities reflect underlying neuro-cognitive efficiencies. By aligning academic focus areas '
        'with innate synaptic transmission channels, learning friction is minimized and retention is maximized.'
    )
    p17_block.extend(sub_heading("Academic Aptitude & Curricular Alignment"))
    p17_block.append(Paragraph(p17_intro, STYLES['body']))
    p17_block.append(Spacer(1, 6))

    chart_b64 = generate_horizontal_progress_bars("Academic Domain Affinity Rankings", categories)
    c_imgs = chart_image(chart_b64, width=CONTENT_W * 0.88)
    if c_imgs:
        p17_block.extend(c_imgs)
        p17_block.append(Spacer(1, 8))

    sub_rows = [
        [
            Paragraph('<b>Academic Subject Domain</b>', STYLES['table_header']),
            Paragraph('<b>Innate Fit</b>', STYLES['table_header']),
            Paragraph('<b>Cognitive Driving Mechanism</b>', STYLES['table_header']),
            Paragraph('<b>Pedagogical Focus</b>', STYLES['table_header']),
        ],
        [
            Paragraph('STEM & Natural Sciences', STYLES['table_cell_bold']),
            Paragraph(f'<b>{stem_val*100:.1f}%</b>', STYLES['table_cell_bold']),
            Paragraph('Parietal-Frontal sensory integration; empirical observation.', STYLES['table_cell']),
            Paragraph('Laboratory experiments, algorithmic modeling, science fairs.', STYLES['table_cell']),
        ],
        [
            Paragraph('Quantitative Logic & Mathematics', STYLES['table_cell_bold']),
            Paragraph(f'<b>{math_val*100:.1f}%</b>', STYLES['table_cell_bold']),
            Paragraph('Left Posterior Frontal lobe deductive processing.', STYLES['table_cell']),
            Paragraph('Competitive mathematics, logic puzzles, coding challenges.', STYLES['table_cell']),
        ],
        [
            Paragraph('Linguistics & Foreign Languages', STYLES['table_cell_bold']),
            Paragraph(f'<b>{ling_val*100:.1f}%</b>', STYLES['table_cell_bold']),
            Paragraph('Left Temporal lobe phonetic and syntactic memory.', STYLES['table_cell']),
            Paragraph('Creative writing, parliamentary debate, dual-language immersion.', STYLES['table_cell']),
        ],
    ]
    cw17 = [CONTENT_W * 0.28, CONTENT_W * 0.14, CONTENT_W * 0.30, CONTENT_W * 0.28]
    t_sub = institutional_table(sub_rows, col_widths=cw17, center_cols=[1])
    p17_block.append(t_sub)

    pages.append(shrink_block(p17_block, max_height=9.2 * inch, _label='quotients_page_17'))
    pages.append(PageBreak())

    p18_block = []
    p18_block.append(SectionHeader(6, "THE 10 INTELLIGENCE QUOTIENTS: COGNITIVE & PHYSICAL (1-5)"))
    p18_block.append(HRFlowable(width=CONTENT_W, thickness=1.0, color=GOLD, spaceAfter=10, spaceBefore=4))

    q1_5 = [
        ('IQ', 'Intelligence Quotient', quotients.get('IQ', 0.76),
         'Reasoning & problem solving; abstract data deduction.'),
        ('EQ', 'Emotional Quotient', quotients.get('EQ', 0.72),
         'Emotional self-regulation; empathic awareness and poise.'),
        ('CQ', 'Creativity Quotient', quotients.get('CQ', 0.70),
         'Divergent thinking; innovative lateral problem solving.'),
        ('AQ', 'Adaptability Quotient', quotients.get('AQ', 0.68),
         'Resilience under uncertainty; rapid recovery from stress.'),
        ('SQ', 'Social Quotient', quotients.get('SQ', 0.74),
         'Interpersonal dynamics; collaborative team synergy.'),
    ]

    gauge_cells = []
    for qk, qname, qval, qdesc in q1_5:
        gb64 = create_gauge_chart(qval, qk)
        g_img = chart_image(gb64, width=CONTENT_W * 0.18)
        content_cell = [
            Paragraph(f'<b><font size="8" color="{NAVY.hexval()}">{qk}: {qname.upper()}</font></b>', STYLES['body']),
            Spacer(1, 2),
            Paragraph(f'<font size="7" color="#2C2C2C">{qdesc}</font>', STYLES['body']),
            Spacer(1, 3),
            Paragraph(f'<font size="11" color="{GOLD_DARK.hexval()}"><b>{qval*100:.0f}%</b></font>', STYLES['body']),
        ]
        if g_img:
            g_table = Table([[g_img[0], content_cell]], colWidths=[CONTENT_W * 0.22, CONTENT_W * 0.68])
            g_table.setStyle(TableStyle([
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('LEFTPADDING', (0, 0), (-1, -1), 4),
                ('RIGHTPADDING', (0, 0), (-1, -1), 4),
                ('TOPPADDING', (0, 0), (-1, -1), 3),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
            ]))
            gauge_cells.append(g_table)

    t_g1_5 = Table([[gc] for gc in gauge_cells], colWidths=[CONTENT_W])
    t_g1_5.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), GOLD_PALE),
        ('BOX', (0, 0), (-1, -1), 1.0, GOLD),
        ('LINEBELOW', (0, 0), (-1, -2), 0.4, GOLD_LIGHT),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('ROUNDEDCORNERS', [4, 4, 4, 4]),
    ]))
    p18_block.append(t_g1_5)
    p18_block.append(Spacer(1, 6))
    p18_block.append(draw_boho_quotients_emblem(width=CONTENT_W, height=48))

    pages.append(shrink_block(p18_block, max_height=9.2 * inch, _label='quotients_page_18'))
    pages.append(PageBreak())

    p19_block = []
    p19_block.append(SectionHeader(6, "THE 10 INTELLIGENCE QUOTIENTS: OPERATIONAL & STRATEGIC (6-10)"))
    p19_block.append(HRFlowable(width=CONTENT_W, thickness=1.0, color=GOLD, spaceAfter=8, spaceBefore=4))

    q6_10 = [
        ('PQ', 'Physical Quotient', quotients.get('PQ', 0.66),
         'Motor execution & somatic coordination.'),
        ('LQ', 'Leadership Quotient', quotients.get('LQ', 0.75),
         'Visionary influence & executive command.'),
        ('MQ', 'Motivation Quotient', quotients.get('MQ', 0.78),
         'Intrinsic persistence & stamina drive.'),
        ('FQ', 'Focus Quotient', quotients.get('FQ', 0.72),
         'Attention span & mental discipline.'),
        ('DQ', 'Decision Quotient', quotients.get('DQ', 0.74),
         'Tactical judgment speed & acumen.'),
    ]

    p19_cards = []
    for qk, qname, qval, qdesc in q6_10:
        c_html = (
            f'<font size="8" color="{NAVY.hexval()}"><b>{qk} • {qname}</b></font><br/>'
            f'<font size="7" color="#2C2C2C">{qdesc}</font><br/>'
            f'<font size="11" color="{GOLD_DARK.hexval()}"><b>{qval*100:.0f}%</b></font>'
        )
        tc = Table([[Paragraph(c_html, STYLES['body'])]], colWidths=[CONTENT_W * 0.185])
        tc.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), GOLD_PALE),
            ('BOX', (0, 0), (-1, -1), 1.0, GOLD),
            ('LEFTPADDING', (0, 0), (-1, -1), 4),
            ('RIGHTPADDING', (0, 0), (-1, -1), 4),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ('ROUNDEDCORNERS', [4, 4, 4, 4]),
        ]))
        p19_cards.append(tc)

    t_qrow = Table([[p19_cards[0], p19_cards[1], p19_cards[2], p19_cards[3], p19_cards[4]]],
                   colWidths=[CONTENT_W * 0.195, CONTENT_W * 0.195, CONTENT_W * 0.195, CONTENT_W * 0.195, CONTENT_W * 0.195])
    t_qrow.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 1),
        ('RIGHTPADDING', (0, 0), (-1, -1), 1),
        ('TOPPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
    ]))
    p19_block.append(t_qrow)
    p19_block.append(Spacer(1, 8))

    radar10_b64 = generate_quotient_10_radar(quotients)
    r10_imgs = chart_image(radar10_b64, width=CONTENT_W * 0.72, caption="10-Quotient Holistic Biometric Spider Map")
    if r10_imgs:
        p19_block.extend(r10_imgs)

    pages.append(shrink_block(p19_block, max_height=9.2 * inch, _label='quotients_page_19'))
    return pages
