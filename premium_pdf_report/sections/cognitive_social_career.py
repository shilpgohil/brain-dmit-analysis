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
                     AMBER_MID, CONTENT_W, score_color)
from .helpers import section_header, sub_heading, chart_image

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


# ---------------------------------------------------------------------------
# Section 13 : Cognitive Skills
# ---------------------------------------------------------------------------

def build_cognitive(ext_results: Dict[str, Any]) -> list:
    story = []
    story += section_header(13, 'Cognitive Skills Assessment')
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        'Cognitive skills assessment measures the efficiency and strength of core '
        'mental processes including memory, attention, creative thinking, analytical '
        'reasoning, and executive function.',
        STYLES['body']
    ))
    story.append(Spacer(1, 8))

    scores = _gather_scores(ext_results, COGNITIVE_KEYS)
    if scores:
        from ..charts import create_extension_bar
        bar_b64 = create_extension_bar(scores, 'Cognitive Skills Profile', SAGE)
        story += chart_image(bar_b64, caption='Cognitive Skills Scores')
        story.append(Spacer(1, 8))
    story += _build_score_table(scores, 'Cognitive Skill Scores', SAGE)
    return story


# ---------------------------------------------------------------------------
# Section 14 : Communication and Social Profile
# ---------------------------------------------------------------------------

def build_social(ext_results: Dict[str, Any]) -> list:
    story = []
    story += section_header(14, 'Communication and Social Profile')
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        'Social and communication intelligence reflects the ability to interact '
        'effectively with others, express ideas clearly, and collaborate in team '
        'environments. These skills are critical for leadership, relationships, and '
        'professional success.',
        STYLES['body']
    ))
    story.append(Spacer(1, 8))

    scores = _gather_scores(ext_results, SOCIAL_KEYS)
    if scores:
        from ..charts import create_extension_bar
        bar_b64 = create_extension_bar(scores, 'Communication and Social Scores', GOLD)
        story += chart_image(bar_b64, caption='Social Profile Scores')
        story.append(Spacer(1, 8))
    story += _build_score_table(scores, 'Social and Communication Scores')
    return story


# ---------------------------------------------------------------------------
# Section 15 : Leadership and Entrepreneurship
# ---------------------------------------------------------------------------

def build_leadership(ext_results: Dict[str, Any]) -> list:
    story = []
    story += section_header(15, 'Leadership and Entrepreneurship Profile')
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        'Leadership potential analysis evaluates innate capacity for vision, '
        'decision-making under pressure, team management, entrepreneurial risk-taking, '
        'and innovation. These traits are encoded in prefrontal and frontal lobe activity.',
        STYLES['body']
    ))
    story.append(Spacer(1, 8))

    scores = _gather_scores(ext_results, LEADERSHIP_KEYS)
    if scores:
        from ..charts import create_extension_bar
        bar_b64 = create_extension_bar(scores, 'Leadership and Entrepreneurship Scores', PLUM)
        story += chart_image(bar_b64, caption='Leadership Profile Scores')
        story.append(Spacer(1, 8))
    story += _build_score_table(scores, 'Leadership and Entrepreneurship Scores', PLUM)
    return story


# ---------------------------------------------------------------------------
# Section 16 : Career and Academic Analysis
# ---------------------------------------------------------------------------

def _derive_swot(mi: Dict[str, float], personality: Dict[str, float]) -> Dict[str, List[str]]:
    swot = {'strengths': [], 'weaknesses': [], 'opportunities': [], 'threats': []}
    if mi:
        sorted_mi = sorted(mi.items(), key=lambda x: x[1], reverse=True)
        for k, v in sorted_mi[:3]:
            if v >= 0.60:
                swot['strengths'].append(f'Strong {_label(k)}')
        for k, v in sorted_mi[-3:]:
            if v < 0.50:
                swot['weaknesses'].append(f'Developing {_label(k)}')
    if personality:
        if personality.get('openness', 0) >= 0.65:
            swot['strengths'].append('High Openness - adaptable to change')
        if personality.get('conscientiousness', 0) >= 0.65:
            swot['strengths'].append('Conscientious - disciplined work ethic')
        if personality.get('neuroticism', 0) >= 0.60:
            swot['threats'].append('Emotional sensitivity - stress management needed')
    swot['opportunities'] = [
        'Emerging careers in AI and technology sectors',
        'Growing demand for creative and design professionals',
        'Global remote work opportunities in specialised fields',
        'Entrepreneurship and startup ecosystem opportunities',
    ]
    if not swot['threats']:
        swot['threats'] = [
            'Rapidly changing skill requirements in the job market',
            'Competition in chosen career field',
        ]
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
                    career_scores[_label(f.replace('_career', ''))] = float(cg[f])

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

    # SWOT
    story += sub_heading('SWOT Analysis')
    swot = _derive_swot(mi, personality)
    from ..charts import create_swot_chart
    swot_b64 = create_swot_chart(swot)
    story += chart_image(swot_b64, caption='Personal SWOT Analysis')

    return story
