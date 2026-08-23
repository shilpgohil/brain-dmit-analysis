"""
Section 4 : Executive Summary Dashboard
Circular gauges (Style E), key tiles, strengths/development areas.
"""

from typing import Dict, Any, List
from reportlab.platypus import Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.units import inch

from ..theme import (STYLES, NAVY, GOLD, GOLD_DARK, GOLD_LIGHT, GOLD_PALE,
                     IVORY, CREAM_ROW, WHITE, GREEN_STRONG, TERRACOTTA,
                     CONTENT_W, score_color)
from .helpers import section_header_plain, sub_heading, chart_image, two_col, shrink_block


def _dominant_mi(mi: Dict[str, float]) -> tuple:
    if not mi:
        return (None, None)
    return max(mi.items(), key=lambda x: x[1])


def _weakest_mi(mi: Dict[str, float]) -> tuple:
    if not mi:
        return (None, None)
    return min(mi.items(), key=lambda x: x[1])


def _label(key: str) -> str:
    return key.replace('_', ' ').title()


def _get_ext_score(ext_results: list, name_fragment: str,
                   score_key: str = None):
    """Return a real numeric score from extension data, or None if unavailable."""
    for e in ext_results:
        if name_fragment.lower() in e.get('name', '').lower():
            val = None
            if score_key:
                val = e.get('scores', {}).get(score_key) or e.get('primary_score')
            else:
                val = e.get('primary_score')
            if isinstance(val, (int, float)):
                return float(val)
    return None


def _personality_archetype(personality: Dict[str, float]) -> str:
    if not personality:
        return 'Well-Rounded'
    o = personality.get('openness', 0)
    c = personality.get('conscientiousness', 0)
    e = personality.get('extraversion', 0)
    a = personality.get('agreeableness', 0)
    n = personality.get('neuroticism', 0)

    if o > 0.7 and c > 0.65:
        return 'The Strategic Innovator'
    if o > 0.7 and e > 0.65:
        return 'The Creative Leader'
    if c > 0.7 and a > 0.65:
        return 'The Reliable Achiever'
    if e > 0.7 and a > 0.65:
        return 'The Social Connector'
    if o > 0.7 and a > 0.65:
        return 'The Empathetic Visionary'
    if c > 0.7 and n < 0.40:
        return 'The Disciplined Performer'
    if e < 0.40 and c > 0.65:
        return 'The Quiet Strategist'
    return 'The Balanced Thinker'


def _dominant_learning(learning: Dict[str, float]) -> str:
    if not learning:
        return 'N/A'
    return max(learning.items(), key=lambda x: x[1])[0].title()


def _hemisphere_dom(brain: Dict[str, float]) -> str:
    l = brain.get('left_hemisphere', brain.get('left_hemisphere_bias'))
    r = brain.get('right_hemisphere', brain.get('right_hemisphere_bias'))
    if not isinstance(l, (int, float)) or not isinstance(r, (int, float)):
        return 'N/A'
    if l > r:
        return f'Left Brain ({int(l*100)}%)'
    return f'Right Brain ({int(r*100)}%)'


# ---------------------------------------------------------------------------
# Quotient summary panel (IQ/EQ/CQ/AQ/SQ/PQ/LQ/MQ/FQ/DQ)
# ---------------------------------------------------------------------------

_QUOTIENT_KEYS = ['IQ', 'EQ', 'CQ', 'AQ', 'SQ', 'PQ', 'LQ', 'MQ', 'FQ', 'DQ']
_QUOTIENT_SHORT = {
    'IQ': 'Intelligence', 'EQ': 'Emotional',   'CQ': 'Creativity',
    'AQ': 'Adaptability', 'SQ': 'Social',       'PQ': 'Physical',
    'LQ': 'Leadership',   'MQ': 'Motivation',   'FQ': 'Focus',
    'DQ': 'Decision',
}


def build_executive_summary_quotients(quotients: Dict[str, Any]) -> list:
    """Build a 5x2 quotient summary panel — two columns of 5 quotients each."""
    if not quotients:
        return []

    items: list = []
    items += sub_heading('Quotient Profile Summary')

    header_row = [Paragraph(h, STYLES['table_header'])
                  for h in ['Quotient', 'Score', 'Level',
                             'Quotient', 'Score', 'Level']]
    rows = [header_row]

    for i in range(0, len(_QUOTIENT_KEYS), 2):
        row = []
        for j in range(2):
            idx = i + j
            if idx < len(_QUOTIENT_KEYS):
                k = _QUOTIENT_KEYS[idx]
                short = _QUOTIENT_SHORT.get(k, k)
                cell_label = f'{k} \u2013 {short}'
                val = quotients.get(k)
                if isinstance(val, (int, float)):
                    _, level = score_color(val)
                    score_str = f'{val * 100:.0f}%'
                else:
                    level = 'N/A'
                    score_str = 'N/A'
                row += [
                    Paragraph(cell_label, STYLES['table_cell_bold']),
                    Paragraph(score_str, STYLES['table_cell_bold']),
                    Paragraph(level, STYLES['table_cell']),
                ]
            else:
                row += [Paragraph('', STYLES['body'])] * 3
        rows.append(row)

    # 6 columns: [label, score, level] * 2 halves
    cw = [
        CONTENT_W * 0.26, CONTENT_W * 0.10, CONTENT_W * 0.14,
        CONTENT_W * 0.26, CONTENT_W * 0.10, CONTENT_W * 0.14,
    ]
    t = Table(rows, colWidths=cw, repeatRows=1)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), NAVY),
        ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [GOLD_PALE, IVORY]),
        ('FONTSIZE', (0, 0), (-1, -1), 8.5),
        ('ALIGN', (1, 0), (1, -1), 'CENTER'),
        ('ALIGN', (2, 0), (2, -1), 'CENTER'),
        ('ALIGN', (4, 0), (4, -1), 'CENTER'),
        ('ALIGN', (5, 0), (5, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 0.4, GOLD_LIGHT),
        ('LINEAFTER', (2, 0), (2, -1), 1.5, GOLD),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))
    items.append(t)
    items.append(Spacer(1, 6))
    return items


def build_executive_summary(report_data: Dict[str, Any],
                             session: Dict[str, Any]) -> list:
    # Whole dashboard (2 gauge grids + tiles + summary table + strength
    # pills) is ~1.3 pages of unscaled content. Previously it split across
    # 2 pages with the 2nd page barely used (a table's last few rows plus
    # 2 pill rows, ~35% of the page) before an unconditional PageBreak into
    # Section 5. Wrapping it all in one shrink block keeps the whole
    # dashboard on a single, fully-packed page instead.
    block = []
    block += section_header_plain(4, 'Executive Summary Dashboard')
    block.append(Spacer(1, 8))

    mi = report_data.get('intelligence_scores', {})
    brain = report_data.get('brain_mapping', {})
    learning = report_data.get('learning_styles', {})
    personality = report_data.get('personality_behavior', {})
    ext_results = report_data.get('extension_results', {})

    dom_mi, dom_score = _dominant_mi(mi)
    weak_mi, weak_score = _weakest_mi(mi)

    # Only assign scores when explicitly present in extension data — never default to 0
    eq_score = None
    creativity_score = None
    if isinstance(ext_results, dict):
        eq_data = ext_results.get('EmotionalIntelligenceExtension', {})
        if isinstance(eq_data, dict):
            raw = eq_data.get('emotional_intelligence_score',
                              eq_data.get('overall', eq_data.get('score')))
            if isinstance(raw, (int, float)):
                eq_score = float(raw)
        cre_data = ext_results.get('CreativityIndexExtension',
                   ext_results.get('CreativityExtension', {}))
        if isinstance(cre_data, dict):
            raw = cre_data.get('creativity_index_score',
                               cre_data.get('creativity_score',
                               cre_data.get('overall', cre_data.get('score'))))
            if isinstance(raw, (int, float)):
                creativity_score = float(raw)

    l_hem = brain.get('left_hemisphere', brain.get('left_hemisphere_bias'))
    r_hem = brain.get('right_hemisphere', brain.get('right_hemisphere_bias'))
    # Only compute brain dominance when both hemisphere values are present
    brain_dom_score = None
    brain_dom_label = 'Brain Dominance'
    if isinstance(l_hem, (int, float)) and isinstance(r_hem, (int, float)):
        brain_dom_score = max(l_hem, r_hem)
        brain_dom_label = f'Brain Dominance\n{"Right" if r_hem >= l_hem else "Left"}'

    # ---- Gauge grid — only include gauges where real data exists ----
    from ..charts import create_gauge_grid
    gauge_scores = {}
    if dom_score is not None:
        gauge_scores[f'Dominant Intelligence\n{_label(dom_mi)}'] = dom_score
    if eq_score is not None:
        gauge_scores['Emotional Intelligence'] = eq_score
    if creativity_score is not None:
        gauge_scores['Creativity Index'] = creativity_score
    if brain_dom_score is not None:
        gauge_scores[brain_dom_label] = brain_dom_score
    gauge_b64 = create_gauge_grid(gauge_scores, cols=4)

    # ---- Tile cards (right column) ----
    archetype = _personality_archetype(personality)
    dom_ls = _dominant_learning(learning)
    hem_dom = _hemisphere_dom(brain)

    # Top career from ext
    top_career = 'See Career Section'
    if isinstance(ext_results, dict):
        cg = ext_results.get('CareerGuidanceExtension', {})
        if isinstance(cg, dict):
            top_career = cg.get('primary_career_aptitude', 'See Career Section')
            top_career = _label(top_career)

    tile_rows = [
        ('Primary Learning Style', dom_ls, GOLD),
        ('Personality Archetype', archetype, NAVY),
        ('Brain Dominance', hem_dom, GOLD_DARK),
        ('Top Career Direction', top_career, GREEN_STRONG),
    ]

    tiles = []
    for tlabel, tvalue, tcolor in tile_rows:
        badge_style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), tcolor),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ])
        badge_t = Table([[Paragraph(tvalue, STYLES['table_header'])]],
                        colWidths=[CONTENT_W * 0.42])
        badge_t.setStyle(badge_style)
        tile_inner = Table([
            [Paragraph(tlabel, STYLES['label'])],
            [badge_t],
        ], colWidths=[CONTENT_W * 0.44])
        tile_inner.setStyle(TableStyle([
            ('BOX', (0, 0), (-1, -1), 1.2, GOLD),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 4),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('BACKGROUND', (0, 0), (-1, -1), GOLD_PALE),
        ]))
        tiles.append(tile_inner)
        tiles.append(Spacer(1, 6))

    # Gauge image (EQ / Creativity / MI dominant / Brain dominance)
    left_items = chart_image(gauge_b64, width=CONTENT_W * 0.98,
                             caption='Score Gauge Overview')
    block += left_items
    block.append(Spacer(1, 8))

    # MI snapshot gauge row (top-2 strengths + bottom-2 development areas)
    from ..charts import create_mi_gauge_grid
    if mi:
        mi_snap_b64 = create_mi_gauge_grid(mi)
        block += chart_image(mi_snap_b64, width=CONTENT_W * 0.98,
                             caption='Intelligence Snapshot: Strengths vs Development Areas')
        block.append(Spacer(1, 8))

    # Profile tiles
    block += tiles

    # End of the "visual dashboard" half (header + both gauge rows + tiles).
    # This alone already runs close to a full page, so the summary table and
    # strength/development pills that follow are built as a SECOND, separate
    # block below rather than appended here. Measurement showed the combined
    # content needs ~14in of vertical space against ~10in available on one
    # page — cramming both halves into a single shrink_block scaled every
    # font and image on the page down by ~30% to force-fit it. Splitting
    # into two independently-sized blocks lets each render at full, correct
    # scale; the second block simply flows onto a fresh page if the first
    # one filled the current page.
    block_2 = []
    block_2 += sub_heading('Key Profile at a Glance')

    summary_rows = [
        [Paragraph('Attribute', STYLES['table_header']),
         Paragraph('Value', STYLES['table_header']),
         Paragraph('Score', STYLES['table_header'])],
    ]
    if dom_mi is not None:
        summary_rows.append(['Dominant Intelligence', _label(dom_mi),
                              f'{dom_score*100:.0f}%' if dom_score is not None else 'N/A'])
    if weak_mi is not None:
        summary_rows.append(['Development Area', _label(weak_mi),
                              f'{weak_score*100:.0f}%' if weak_score is not None else 'N/A'])
    summary_rows.append(['Learning Style', dom_ls, ''])
    if hem_dom != 'N/A':
        summary_rows.append(['Brain Dominance', hem_dom, ''])
    summary_rows.append(['Personality Archetype', archetype, ''])
    if eq_score is not None:
        summary_rows.append(['Emotional Intelligence', 'EQ Profile', f'{eq_score*100:.0f}%'])
    for i in range(1, len(summary_rows)):
        summary_rows[i] = [Paragraph(str(c), STYLES['table_cell'])
                           for c in summary_rows[i]]

    cw = [CONTENT_W * 0.38, CONTENT_W * 0.40, CONTENT_W * 0.18]
    st = Table(summary_rows, colWidths=cw)
    st.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), NAVY),
        ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [GOLD_PALE, IVORY]),
        ('FONTNAME', (0, 0), (-1, 0), 'Times-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('ALIGN', (2, 0), (2, -1), 'CENTER'),
        ('ALIGN', (0, 0), (1, -1), 'LEFT'),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 7),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 7),
        ('GRID', (0, 0), (-1, -1), 0.4, GOLD_LIGHT),
    ]))
    block_2.append(st)
    block_2.append(Spacer(1, 10))

    # ---- Strengths and Development Areas ----
    strengths = []
    dev_areas = []
    if mi:
        sorted_mi = sorted(
            [(k, v) for k, v in mi.items() if isinstance(v, (int, float))],
            key=lambda x: x[1], reverse=True
        )
        strengths = [_label(k) for k, v in sorted_mi[:4] if v >= 0.55]
        dev_areas = [_label(k) for k, v in sorted_mi[-3:] if v < 0.55]

    block_2 += sub_heading('Core Strengths')
    if strengths:
        # pill row
        pill_cells = [Paragraph(s, STYLES['table_header']) for s in strengths]
        cws = [CONTENT_W / len(pill_cells)] * len(pill_cells)
        pt = Table([pill_cells], colWidths=cws)
        pt.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), GOLD),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ]))
        block_2.append(pt)
    block_2.append(Spacer(1, 8))

    block_2 += sub_heading('Development Areas')
    if dev_areas:
        pill_cells = [Paragraph(d, STYLES['table_header']) for d in dev_areas]
        cws = [CONTENT_W / len(pill_cells)] * len(pill_cells)
        pt = Table([pill_cells], colWidths=cws)
        pt.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), TERRACOTTA),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ]))
        block_2.append(pt)

    # Quotient summary panel (appended when quotient data is present)
    quotients = report_data.get('quotients', {})
    if quotients:
        block_2.append(Spacer(1, 8))
        block_2 += build_executive_summary_quotients(quotients)

    # Each half gets its own shrink_block sized to a full page. In practice
    # neither half is anywhere near a full page tall on its own, so
    # max_height is never actually invoked as a scale factor here — it only
    # guarantees each half can never split its own table/chart mid-way.
    # NOTE: CONTENT_H (PAGE_H - 1.35in) is ~12pt taller than the actual
    # SimpleDocTemplate frame height reported by ReportLab (topMargin +
    # bottomMargin leave slightly less usable space than that constant
    # assumes), so a max_height of exactly CONTENT_H overflowed the frame
    # ('too large on page' failure) even on a fully fresh page. Back off by
    # a small safety margin.
    from ..theme import CONTENT_H
    max_h = CONTENT_H - 0.3 * inch
    return [
        shrink_block(block, max_height=max_h, _label='executive_summary_dashboard'),
        shrink_block(block_2, max_height=max_h, _label='executive_summary_table'),
    ]
