"""
Section 13 : Cognitive Skills Assessment
Section 14 : Communication and Social Profile
Section 15 : Leadership and Entrepreneurship
Section 16 : Career and Academic Analysis (with SWOT)
"""

from typing import Dict, Any, List
from reportlab.platypus import Paragraph, Spacer, Table, TableStyle
from reportlab.lib.units import inch

from ..theme import (STYLES, NAVY, GOLD, GOLD_DARK, GOLD_LIGHT, GOLD_PALE,
                     IVORY, WHITE, SAGE, PLUM, GREEN_STRONG, TERRACOTTA,
                     AMBER_MID, CONTENT_W, CONTENT_H, score_color)
from .helpers import section_header, section_header_plain, sub_heading, chart_image, shrink_block

# Sections 13/14/15 always start on a fresh page (each follows a forced
# PageBreak in generator.py), so the full page height is available rather
# than shrink_block()'s conservative default of 8.7in (sized for sections
# that may start partway down an already-occupied page). Using the fuller
# height here means their chart+table content (~9.6in measured) renders at
# full, undistorted scale instead of being scaled down ~9% to force-fit
# the smaller default cap.
_FULL_PAGE_MAX_H = CONTENT_H - 0.3 * inch

# Keys match actual extension analyze() output — verified against engine
COGNITIVE_KEYS = [
    'memory_processing_score',        # MemoryProcessingExtension
    'attention_focus_score',           # AttentionFocusExtension
    'focus_quality',                   # AttentionFocusExtension
    'processing_speed',                # CognitiveLoadExtension
    'cognitive_load_management_score', # CognitiveLoadExtension
    'working_memory_capacity',         # CognitiveLoadExtension
    'executive_function_score',        # ExecutiveFunctionExtension
    'decision_making_score',           # DecisionMakingExtension
    'problem_solving_score',           # ProblemSolvingExtension
    'analytical_thinking',             # ProblemSolvingExtension
    'creativity_index_score',          # CreativityIndexExtension
]

SOCIAL_KEYS = [
    'communication_effectiveness_score',  # CommunicationStyleExtension
    'verbal_communication',               # CommunicationStyleExtension
    'active_listening',                   # CommunicationStyleExtension
    'persuasive_communication',           # CommunicationStyleExtension
    'social_awareness_score',             # SocialAwarenessExtension
    'empathy_skills',                     # SocialAwarenessExtension
    'social_communication',               # SocialAwarenessExtension
    'relationship_awareness',             # SocialAwarenessExtension
]

LEADERSHIP_KEYS = [
    'leadership_potential_score',         # LeadershipPotentialExtension
    'vision_leadership',                  # LeadershipPotentialExtension
    'strategic_thinking',                 # LeadershipPotentialExtension
    'influence_ability',                  # LeadershipPotentialExtension
    'team_building',                      # LeadershipPotentialExtension
    'entrepreneurial_aptitude_score',     # EntrepreneurialAptitudeExtension
    'business_vision',                    # EntrepreneurialAptitudeExtension
    'innovation_intelligence_score',      # InnovationIntelligenceExtension
    'risk_tolerance_index',               # RiskToleranceExtension
    'motivation_drive_score',             # MotivationDriveExtension
    'achievement_drive',                  # MotivationDriveExtension
]

# Must stay in sync with CAREER_FIELD_LABELS in api/routes/analysis.py so the
# same CareerGuidanceExtension score displays the same title in the PDF and
# the dashboard/API response.
CAREER_FIELD_TITLES = {
    'technical_career': 'Technology & Engineering',
    'creative_career': 'Arts, Media & Design',
    'analytical_career': 'Research & Analysis',
    'leadership_career': 'Management & Leadership',
    'social_career': 'People & Service',
    'administrative_career': 'Operations & Administration',
    'research_career': 'Science & Investigation',
    'entrepreneurial_career': 'Entrepreneurship & Ventures',
}

STREAM_SUITABILITY = {
    'Science': ['logical_mathematical', 'spatial', 'naturalistic'],
    'Commerce': ['logical_mathematical', 'interpersonal', 'linguistic'],
    'Arts and Humanities': ['linguistic', 'interpersonal', 'intrapersonal'],
    'Design and Technology': ['spatial', 'bodily_kinesthetic', 'musical'],
    'Sports and Fitness': ['bodily_kinesthetic', 'naturalistic', 'interpersonal'],
}


def _label(key: str) -> str:
    return key.replace('_', ' ').title()


def _gather_scores(ext_results: Dict[str, Any], keys: List[str]) -> Dict[str, float]:
    """Search all extension dicts for given score keys."""
    found = {}
    if not isinstance(ext_results, dict):
        return found
    for ext_name, ext_dict in ext_results.items():
        if not isinstance(ext_dict, dict):
            continue
        for k in keys:
            if k in ext_dict and k not in found:
                v = ext_dict[k]
                if isinstance(v, (int, float)) and 0 <= v <= 1:
                    found[k] = float(v)
    return found


def _gather_recommendations(ext_results: Dict[str, Any],
                            keys: List[str]) -> List[str]:
    """Collect up to 5 unique recommendation strings from extensions that
    contain at least one of the given score keys."""
    if not ext_results or not isinstance(ext_results, dict):
        return []
    recommendations: List[str] = []
    seen: set = set()
    for ext_dict in ext_results.values():
        if not isinstance(ext_dict, dict):
            continue
        if not any(k in ext_dict for k in keys):
            continue
        recs = ext_dict.get('recommendations', [])
        if not isinstance(recs, list):
            continue
        for r in recs:
            r_str = str(r).strip()
            if r_str and r_str not in seen:
                seen.add(r_str)
                recommendations.append(r_str)
                if len(recommendations) >= 5:
                    return recommendations
    return recommendations


def _build_score_table(scores: Dict[str, float], title: str, color=None) -> list:
    color = color or NAVY
    items = []
    items += sub_heading(title)
    if not scores:
        items.append(Paragraph('Data not available.', STYLES['body']))
        return items

    rows = [[Paragraph(h, STYLES['table_header'])
             for h in ['Skill / Attribute', 'Score', 'Level']]]
    for k, v in sorted(scores.items(), key=lambda x: x[1], reverse=True):
        _, level = score_color(v)
        rows.append([
            Paragraph(_label(k), STYLES['table_cell']),
            Paragraph(f'{v*100:.0f}%', STYLES['table_cell_bold']),
            Paragraph(level, STYLES['table_cell']),
        ])
    cw = [CONTENT_W * 0.56, CONTENT_W * 0.18, CONTENT_W * 0.22]
    t = Table(rows, colWidths=cw, repeatRows=1, splitByRow=1)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), color),
        ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [GOLD_PALE, IVORY]),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('ALIGN', (1, 0), (2, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 0.4, GOLD_LIGHT),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    items.append(t)
    return items


def _build_career_match_table(career_matches: List[Dict[str, Any]]) -> list:
    """Render up to 15 career matches with rank, title, family, suitability %, key strengths."""
    if not career_matches:
        return []

    items: list = []
    items += sub_heading('Top Career Matches — Detailed View')

    headers = ['#', 'Career Title', 'Family', 'Suitability', 'Key Strengths']
    rows = [[Paragraph(h, STYLES['table_header']) for h in headers]]

    for i, cm in enumerate(career_matches[:15], 1):
        title = str(cm.get('title', ''))
        family = str(cm.get('family', cm.get('category', '')))
        score = cm.get('match_score', 0)
        strengths = cm.get('key_strengths', [])
        if isinstance(strengths, list):
            strengths_str = ', '.join(str(s) for s in strengths[:4])
        else:
            strengths_str = str(strengths)
        score_str = (f'{score * 100:.0f}%'
                     if isinstance(score, (int, float)) else str(score))
        rows.append([
            Paragraph(str(i), STYLES['table_cell']),
            Paragraph(title, STYLES['table_cell_bold']),
            Paragraph(family, STYLES['table_cell']),
            Paragraph(score_str, STYLES['table_cell_bold']),
            Paragraph(strengths_str, STYLES['table_cell']),
        ])

    cw = [
        CONTENT_W * 0.05,
        CONTENT_W * 0.27,
        CONTENT_W * 0.18,
        CONTENT_W * 0.10,
        CONTENT_W * 0.36,
    ]
    t = Table(rows, colWidths=cw, repeatRows=1, splitByRow=1)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), NAVY),
        ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [GOLD_PALE, IVORY]),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('ALIGN', (0, 0), (0, -1), 'CENTER'),
        ('ALIGN', (3, 0), (3, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 0.4, GOLD_LIGHT),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    items.append(t)
    return items


# ---------------------------------------------------------------------------
# Section 13 : Cognitive Skills
# ---------------------------------------------------------------------------

def build_cognitive(ext_results: Dict[str, Any]) -> list:
    # Header + intro go INSIDE the shrink_block too (not left in story
    # before it): if only the chart+table were wrapped, a large-enough
    # shrink_block could fail to fit in whatever page space remains after
    # the header+intro render, deferring the whole block to a fresh page
    # and stranding the header and intro paragraph alone above a
    # near-empty page — the exact "heading on one page, content on the
    # next" defect this pattern exists to prevent (observed here once the
    # max_height was raised to a full page).
    story = []
    block = []
    block += section_header_plain(13, 'Cognitive Skills Assessment')
    block.append(Spacer(1, 6))
    block.append(Paragraph(
        'Cognitive skills assessment measures the efficiency and strength of core '
        'mental processes including memory, attention, creative thinking, analytical '
        'reasoning, and executive function.',
        STYLES['body']
    ))
    block.append(Spacer(1, 8))

    scores = _gather_scores(ext_results, COGNITIVE_KEYS)
    if scores:
        from ..charts import create_extension_bar
        bar_b64 = create_extension_bar(scores, 'Cognitive Skills Profile', SAGE)
        block += chart_image(bar_b64, caption='Cognitive Skills Scores')
        block.append(Spacer(1, 8))
    block += _build_score_table(scores, 'Cognitive Skill Scores', SAGE)

    cog_recs = _gather_recommendations(ext_results, COGNITIVE_KEYS)
    if cog_recs:
        block.append(Spacer(1, 6))
        block += sub_heading('Development Tips')
        for r in cog_recs:
            block.append(Paragraph(f'\u2022  {r}', STYLES['bullet']))
        block.append(Spacer(1, 4))

    story.append(shrink_block(block, max_height=_FULL_PAGE_MAX_H, _label='cognitive'))
    return story


# ---------------------------------------------------------------------------
# Section 14 : Communication and Social Profile
# ---------------------------------------------------------------------------

def build_social(ext_results: Dict[str, Any]) -> list:
    story = []
    block = []
    block += section_header_plain(14, 'Communication and Social Profile')
    block.append(Spacer(1, 6))
    block.append(Paragraph(
        'Social and communication intelligence reflects the ability to interact '
        'effectively with others, express ideas clearly, and collaborate in team '
        'environments. These skills are critical for leadership, relationships, and '
        'professional success.',
        STYLES['body']
    ))
    block.append(Spacer(1, 8))

    scores = _gather_scores(ext_results, SOCIAL_KEYS)
    if scores:
        from ..charts import create_extension_bar
        bar_b64 = create_extension_bar(scores, 'Communication and Social Scores', GOLD)
        block += chart_image(bar_b64, caption='Social Profile Scores')
        block.append(Spacer(1, 8))
    block += _build_score_table(scores, 'Social and Communication Scores')

    soc_recs = _gather_recommendations(ext_results, SOCIAL_KEYS)
    if soc_recs:
        block.append(Spacer(1, 6))
        block += sub_heading('Development Tips')
        for r in soc_recs:
            block.append(Paragraph(f'\u2022  {r}', STYLES['bullet']))
        block.append(Spacer(1, 4))

    story.append(shrink_block(block, max_height=_FULL_PAGE_MAX_H, _label='social'))
    return story


# ---------------------------------------------------------------------------
# Section 15 : Leadership and Entrepreneurship
# ---------------------------------------------------------------------------

def build_leadership(ext_results: Dict[str, Any]) -> list:
    story = []
    block = []
    block += section_header_plain(15, 'Leadership and Entrepreneurship Profile')
    block.append(Spacer(1, 6))
    block.append(Paragraph(
        'Leadership potential analysis evaluates innate capacity for vision, '
        'decision-making under pressure, team management, entrepreneurial risk-taking, '
        'and innovation. These traits are encoded in prefrontal and frontal lobe activity.',
        STYLES['body']
    ))
    block.append(Spacer(1, 8))

    scores = _gather_scores(ext_results, LEADERSHIP_KEYS)
    if scores:
        from ..charts import create_extension_bar
        bar_b64 = create_extension_bar(scores, 'Leadership and Entrepreneurship Scores', PLUM)
        block += chart_image(bar_b64, caption='Leadership Profile Scores')
        block.append(Spacer(1, 8))
    block += _build_score_table(scores, 'Leadership and Entrepreneurship Scores', PLUM)

    lead_recs = _gather_recommendations(ext_results, LEADERSHIP_KEYS)
    if lead_recs:
        block.append(Spacer(1, 6))
        block += sub_heading('Development Tips')
        for r in lead_recs:
            block.append(Paragraph(f'\u2022  {r}', STYLES['bullet']))
        block.append(Spacer(1, 4))

    story.append(shrink_block(block, max_height=_FULL_PAGE_MAX_H, _label='leadership'))
    return story


# ---------------------------------------------------------------------------
# Section 16 : Career and Academic Analysis
# ---------------------------------------------------------------------------

def _derive_swot(mi: Dict[str, float], personality: Dict[str, float]) -> Dict[str, List[str]]:
    swot: Dict[str, List[str]] = {
        'strengths': [], 'weaknesses': [], 'opportunities': [], 'threats': [],
    }

    # --- Strengths from MI (top 3 above threshold) ---
    if mi:
        sorted_mi = sorted(mi.items(), key=lambda x: x[1], reverse=True)
        for k, v in sorted_mi[:4]:
            if v >= 0.65:
                swot['strengths'].append(f'Strong {_label(k)} ({round(v*100)}%)')

    if personality:
        p = personality
        if p.get('openness', 0) >= 0.65:
            swot['strengths'].append('High Openness — adaptable and creative thinker')
        if p.get('conscientiousness', 0) >= 0.65:
            swot['strengths'].append('High Conscientiousness — disciplined, goal-oriented')
        if p.get('extraversion', 0) >= 0.65:
            swot['strengths'].append('Extraverted — energised by people and collaboration')
        if p.get('agreeableness', 0) >= 0.65:
            swot['strengths'].append('High Agreeableness — cooperative team player')

    # --- Weaknesses from MI (bottom 3 below threshold) ---
    if mi:
        sorted_mi = sorted(mi.items(), key=lambda x: x[1], reverse=True)
        for k, v in sorted_mi[-3:]:
            if v < 0.45:
                swot['weaknesses'].append(f'{_label(k)} is a development area ({round(v*100)}%)')

    if personality:
        p = personality
        if p.get('neuroticism', 0) >= 0.65:
            swot['weaknesses'].append('High Neuroticism — emotional reactions may affect decisions')
        if p.get('conscientiousness', 0) < 0.40:
            swot['weaknesses'].append('Lower Conscientiousness — structured planning may help')
        if p.get('extraversion', 0) < 0.35:
            swot['weaknesses'].append('Introversion tendency — networking may need deliberate effort')

    if not swot['weaknesses']:
        swot['weaknesses'] = ['No strong weaknesses identified from available data']

    # --- Opportunities (general, fact-based) ---
    opps = [
        'Emerging careers in AI, data science, and technology',
        'Growing demand for creative and design professionals globally',
        'Remote and hybrid work models expanding career geography',
        'Entrepreneurship and startup ecosystem opportunities',
        'Interdisciplinary roles bridging technical and social skills',
    ]
    if mi:
        sorted_mi = sorted(mi.items(), key=lambda x: x[1], reverse=True)
        top_k, top_v = sorted_mi[0]
        if top_k in ('linguistic', 'interpersonal') and top_v >= 0.6:
            opps.insert(0, 'Strong communication skills open leadership and teaching roles')
        elif top_k in ('spatial', 'bodily_kinesthetic') and top_v >= 0.6:
            opps.insert(0, 'Spatial-kinesthetic strength suits design, sports, and engineering paths')
        elif top_k == 'logical_mathematical' and top_v >= 0.6:
            opps.insert(0, 'High logical ability aligns with finance, research, and STEM fields')

    swot['opportunities'] = opps[:4]

    # --- Threats ---
    threats = ['Rapidly changing skill requirements in the job market']
    if personality:
        if personality.get('neuroticism', 0) >= 0.60:
            threats.append('Stress sensitivity may impact performance under pressure')
    if mi:
        sorted_mi = sorted(mi.items(), key=lambda x: x[1], reverse=True)
        low_q = [k for k, v in sorted_mi if v < 0.40]
        if low_q:
            threats.append(f'Developing {_label(low_q[0])} may limit some career paths')

    swot['threats'] = threats[:3]
    return swot


def build_career(ext_results: Dict[str, Any], career_matches: List[Dict[str, Any]],
                 mi: Dict[str, float], personality: Dict[str, float]) -> list:
    story = []
    story += section_header(16, 'Career and Academic Analysis')
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        'Career aptitude analysis identifies the professional domains where natural '
        'intelligence patterns, personality traits, and cognitive strengths align for '
        'the greatest potential for success and fulfillment.',
        STYLES['body']
    ))
    story.append(Spacer(1, 8))

    # Career scores from ext_results
    career_scores = {}
    if isinstance(ext_results, dict):
        cg = ext_results.get('CareerGuidanceExtension', {})
        if isinstance(cg, dict):
            career_fields = [
                'technical_career', 'creative_career', 'analytical_career',
                'leadership_career', 'social_career', 'administrative_career',
                'research_career', 'entrepreneurial_career',
            ]
            for f in career_fields:
                if f in cg and isinstance(cg[f], (int, float)):
                    career_scores[CAREER_FIELD_TITLES[f]] = float(cg[f])

    if not career_scores and career_matches:
        career_scores = {c.get('title', ''): c.get('match_score', 0)
                         for c in career_matches if c.get('match_score', 0) > 0}

    if career_scores:
        from ..charts import create_career_bar
        bar_b64 = create_career_bar(career_scores)
        story += chart_image(bar_b64, caption='Career Aptitude Scores')
        story.append(Spacer(1, 8))

    # Stream suitability matrix
    story += sub_heading('Academic Stream Suitability')
    if mi:
        stream_rows = [[Paragraph(h, STYLES['table_header'])
                        for h in ['Stream', 'Suitability Score', 'Key Intelligences', 'Level']]]
        for stream, mi_keys in STREAM_SUITABILITY.items():
            # Only average MI keys that are actually present in the pipeline data
            present = [(k, mi[k]) for k in mi_keys
                       if k in mi and isinstance(mi[k], (int, float))]
            if not present:
                continue  # skip stream if no relevant MI scores available
            avg = sum(v for _, v in present) / len(present)
            ki_labels = ', '.join(_label(k) for k in mi_keys)
            _, level = score_color(avg)
            stream_rows.append([
                Paragraph(stream, STYLES['table_cell_bold']),
                Paragraph(f'{avg*100:.0f}%', STYLES['table_cell_bold']),
                Paragraph(ki_labels, STYLES['table_cell']),
                Paragraph(level, STYLES['table_cell']),
            ])
        cw = [CONTENT_W*0.28, CONTENT_W*0.16, CONTENT_W*0.38, CONTENT_W*0.14]
        st = Table(stream_rows, colWidths=cw, repeatRows=1, splitByRow=1)
        st.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), NAVY),
            ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [GOLD_PALE, IVORY]),
            ('FONTSIZE', (0, 0), (-1, -1), 8.5),
            ('ALIGN', (1, 0), (1, -1), 'CENTER'),
            ('ALIGN', (3, 0), (3, -1), 'CENTER'),
            ('GRID', (0, 0), (-1, -1), 0.4, GOLD_LIGHT),
            ('LEFTPADDING', (0, 0), (-1, -1), 7),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ]))
        story.append(st)
        story.append(Spacer(1, 10))

    # Top career match cards
    if career_scores:
        story += sub_heading('Top Career Match Scores')
        sorted_careers = sorted(career_scores.items(), key=lambda x: x[1], reverse=True)
        card_rows = []
        for i in range(0, min(8, len(sorted_careers)), 2):
            row = []
            for j in range(2):
                if i + j < len(sorted_careers):
                    title, pct = sorted_careers[i + j]
                    _, level = score_color(pct)
                    card_inner = Table([
                        [Paragraph(title, STYLES['sub_heading'])],
                        [Paragraph(f'{pct*100:.0f}%  -  {level}', STYLES['table_cell_bold'])],
                    ], colWidths=[(CONTENT_W - 0.1 * inch) / 2])
                    card_inner.setStyle(TableStyle([
                        ('BOX', (0, 0), (-1, -1), 1.0, GOLD),
                        ('BACKGROUND', (0, 0), (-1, -1), GOLD_PALE),
                        ('LEFTPADDING', (0, 0), (-1, -1), 10),
                        ('TOPPADDING', (0, 0), (-1, -1), 7),
                        ('BOTTOMPADDING', (0, 0), (-1, -1), 7),
                    ]))
                    row.append(card_inner)
                else:
                    row.append(Paragraph('', STYLES['body']))
            card_rows.append(row)
        if card_rows:
            ct = Table(card_rows,
                       colWidths=[(CONTENT_W - 0.1 * inch) / 2] * 2)
            ct.setStyle(TableStyle([
                ('TOPPADDING', (0, 0), (-1, -1), 4),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
                ('LEFTPADDING', (0, 0), (-1, -1), 2),
                ('RIGHTPADDING', (0, 0), (-1, -1), 2),
            ]))
            story.append(ct)
        story.append(Spacer(1, 10))

    # Detailed career match table (when db_careers list with key_strengths is available)
    if career_matches:
        story += _build_career_match_table(career_matches)
        story.append(Spacer(1, 10))

    # SWOT
    story += sub_heading('SWOT Analysis')
    swot = _derive_swot(mi, personality)
    from ..charts import create_swot_chart
    swot_b64 = create_swot_chart(swot)
    story += chart_image(swot_b64, caption='Personal SWOT Analysis')

    return story
