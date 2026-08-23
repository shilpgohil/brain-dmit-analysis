"""
Section 9  : Multiple Intelligence Profile
Section 10 : Learning Style Analysis
Section 11 : Personality and Behavioral Profile
Section 12 : Emotional Intelligence
"""

from typing import Dict, Any, List
from reportlab.platypus import Paragraph, Spacer, Table, TableStyle
from reportlab.lib.units import inch

from ..theme import (STYLES, NAVY, GOLD, GOLD_DARK, GOLD_LIGHT, GOLD_PALE,
                     IVORY, WHITE, SAGE, PLUM, CONTENT_W, CONTENT_H, score_color)
from .helpers import section_header, section_header_plain, sub_heading, chart_image, shrink_block

# Section 12 always starts on a fresh page (follows a forced PageBreak after
# Section 11 in generator.py), so the fuller page height is available rather
# than shrink_block()'s conservative 8.7in default.
_FULL_PAGE_MAX_H = CONTENT_H - 0.3 * inch

MI_INFO = {
    'linguistic': (
        'Linguistic Intelligence',
        'The ability to use language effectively for communication, expression, and learning.',
        'Writing, Reading, Public Speaking, Journalism, Teaching, Law',
        'Read daily, write journals, learn a new language, participate in debates.'
    ),
    'logical_mathematical': (
        'Logical-Mathematical Intelligence',
        'Capacity for logical reasoning, problem-solving, and numerical analysis.',
        'Engineering, Research, Data Science, Finance, Medicine, Programming',
        'Solve puzzles, learn coding, practise mental arithmetic, explore logic games.'
    ),
    'spatial': (
        'Spatial Intelligence',
        'Ability to think in three dimensions, visualise and manipulate spatial relationships.',
        'Architecture, Design, Fine Arts, Surgery, Navigation, Film Direction',
        'Draw, sketch, build models, play strategy games, practise mind mapping.'
    ),
    'musical': (
        'Musical Intelligence',
        'Sensitivity to rhythm, pitch, melody, and musical patterns.',
        'Music, Composition, Sound Engineering, Music Therapy, Performance',
        'Learn an instrument, study music theory, listen analytically, compose.'
    ),
    'bodily_kinesthetic': (
        'Bodily-Kinesthetic Intelligence',
        'Skill in using the body expressively and handling objects skillfully.',
        'Sports, Dance, Surgery, Physiotherapy, Crafts, Drama',
        'Practise yoga, learn martial arts, dance, engage in sports, build things.'
    ),
    'interpersonal': (
        'Interpersonal Intelligence',
        'Understanding and interacting effectively with others, empathy and social awareness.',
        'Counselling, Leadership, Teaching, Sales, Diplomacy, HR Management',
        'Join clubs, practice active listening, volunteer, engage in team projects.'
    ),
    'intrapersonal': (
        'Intrapersonal Intelligence',
        'Deep understanding of one\'s own emotions, motivations, and inner life.',
        'Psychology, Counselling, Philosophy, Entrepreneurship, Creative Writing',
        'Keep a reflective journal, meditate, set personal goals, practise mindfulness.'
    ),
    'naturalistic': (
        'Naturalistic Intelligence',
        'Ability to recognise and categorise natural objects and patterns in nature.',
        'Biology, Ecology, Veterinary Science, Agriculture, Environmental Science',
        'Observe nature, maintain a plant garden, study biology, go bird-watching.'
    ),
    'existential': (
        'Existential Intelligence',
        'Capacity to ponder deep questions about existence, meaning, and the cosmos.',
        'Philosophy, Theology, Counselling, Literature, Social Research',
        'Explore philosophy texts, engage in reflective discussions, study ethics.'
    ),
}

LEARNING_INFO = {
    'visual': (
        'Visual Learner',
        'Learns best through diagrams, charts, colour-coded notes, and visual demonstrations.',
        [
            'Use mind maps, flowcharts, and colour-coded notes.',
            'Watch educational videos and documentaries.',
            'Sit at the front of the class for clear board visibility.',
            'Use highlighters and visual organisers while studying.',
        ]
    ),
    'auditory': (
        'Auditory Learner',
        'Learns best through listening, discussion, and verbal instruction.',
        [
            'Record lectures and replay for revision.',
            'Participate actively in group discussions and debates.',
            'Use rhythmic mnemonics and read notes aloud.',
            'Listen to educational podcasts and audio books.',
        ]
    ),
    'kinesthetic': (
        'Kinesthetic Learner',
        'Learns best through hands-on activity, movement, and physical engagement.',
        [
            'Use role-play, demonstrations, and practical experiments.',
            'Take movement breaks between study sessions.',
            'Build models or use manipulatives to understand concepts.',
            'Study while walking or using fidget tools.',
        ]
    ),
}

BIG5_INFO = {
    'openness': ('Openness', 'Curiosity, creativity, willingness to explore new ideas.'),
    'conscientiousness': ('Conscientiousness', 'Organisation, dependability, goal-directed behaviour.'),
    'extraversion': ('Extraversion', 'Sociability, assertiveness, and preference for social interaction.'),
    'agreeableness': ('Agreeableness', 'Cooperativeness, empathy, and trust in others.'),
    'neuroticism': ('Emotional Stability', 'Degree of emotional resilience vs anxiety (inverted score).'),
}


def _label(key: str) -> str:
    return key.replace('_', ' ').title()


# ---------------------------------------------------------------------------
# Personality style derivation helpers
# ---------------------------------------------------------------------------

def _build_personality_styles(personality: Dict[str, float]) -> list:
    """Derive and render a 2x2 styled table: Communication, Decision, Leadership, Stress."""
    if not personality:
        return []

    e = personality.get('extraversion', 0)
    a = personality.get('agreeableness', 0)
    c = personality.get('conscientiousness', 0)
    o = personality.get('openness', 0)
    n = personality.get('neuroticism', 0)

    # Communication Style
    if e >= 0.65 and a >= 0.65:
        comm_style = 'Expressive & Collaborative'
        comm_desc = ('You communicate openly and thrive in team environments '
                     'where ideas are shared freely and enthusiastically.')
    elif e < 0.40 and a >= 0.65:
        comm_style = 'Empathetic & Supportive'
        comm_desc = ('You listen deeply and offer thoughtful, caring responses '
                     'that make others feel understood and valued.')
    elif e >= 0.65 and a < 0.40:
        comm_style = 'Direct & Assertive'
        comm_desc = ('You communicate with clarity and confidence, preferring '
                     'direct and efficient exchanges without ambiguity.')
    else:
        comm_style = 'Reserved & Analytical'
        comm_desc = ('You reflect carefully before speaking, offering well-considered '
                     'and precise input rather than impulsive responses.')

    # Decision Style
    if c >= 0.65 and o >= 0.65:
        dec_style = 'Systematic & Methodical'
        dec_desc = ('You plan thoroughly and use structured approaches, '
                    'balancing creativity with discipline to reach sound decisions.')
    elif c < 0.40 and o >= 0.65:
        dec_style = 'Intuitive & Flexible'
        dec_desc = ('You rely on instinct and adapt your decision-making rapidly '
                    'as new information and opportunities emerge.')
    elif c >= 0.65 and o < 0.40:
        dec_style = 'Cautious & Data-Driven'
        dec_desc = ('You gather evidence carefully and prefer proven methods, '
                    'ensuring reliability before committing to a course of action.')
    else:
        dec_style = 'Visionary & Risk-Taking'
        dec_desc = ('You embrace bold ideas and feel comfortable making decisions '
                    'in uncertain or ambiguous situations.')

    # Leadership Style
    if e >= 0.65 and c >= 0.65:
        lead_style = 'Transformational'
        lead_desc = ('You inspire and energise teams through a compelling vision '
                     'combined with high personal standards and drive.')
    elif e < 0.40 and c >= 0.65:
        lead_style = 'Analytical & Strategic'
        lead_desc = ('You lead through careful planning and structured execution, '
                     'earning trust through expertise rather than authority.')
    elif e >= 0.65 and c < 0.40:
        lead_style = 'Democratic & Inspiring'
        lead_desc = ('You lead by involving others, drawing on the group\'s '
                     'collective energy and making people feel heard.')
    else:
        lead_style = 'Servant Leader'
        lead_desc = ('You prioritise the growth and well-being of your team '
                     'above personal recognition, leading through example.')

    # Stress Behaviour
    if n < 0.40:
        stress_style = 'Resilient Under Pressure'
        stress_desc = ('You remain calm and composed during challenging situations, '
                       'recovering quickly and maintaining performance under stress.')
    elif n <= 0.64:
        stress_style = 'Manages Stress Actively'
        stress_desc = ('You are aware of your stress triggers and employ coping '
                       'strategies to maintain focus and balance under pressure.')
    else:
        stress_style = 'Sensitive to Stressors'
        stress_desc = ('You experience stress more acutely; building consistent '
                       'coping routines and mindfulness practices can build resilience.')

    items: list = []
    items += sub_heading('Personality Style Analysis')

    cells = [
        ('Communication Style', comm_style, comm_desc),
        ('Decision Style',      dec_style,  dec_desc),
        ('Leadership Style',    lead_style, lead_desc),
        ('Stress Behaviour',    stress_style, stress_desc),
    ]

    cell_w = (CONTENT_W - 0.05 * inch) / 2
    inner_w = cell_w - 0.20 * inch

    grid_rows = []
    for i in range(0, 4, 2):
        row = []
        for j in range(2):
            cat_label, style_name, style_desc = cells[i + j]
            inner = Table([
                [Paragraph(cat_label, STYLES['label'])],
                [Paragraph(f'<b>{style_name}</b>', STYLES['table_cell_bold'])],
                [Paragraph(style_desc, STYLES['table_cell'])],
            ], colWidths=[inner_w])
            inner.setStyle(TableStyle([
                ('BOX', (0, 0), (-1, -1), 1.0, GOLD),
                ('BACKGROUND', (0, 0), (-1, -1), GOLD_PALE),
                ('BACKGROUND', (0, 0), (-1, 0), NAVY),
                ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
                ('LEFTPADDING', (0, 0), (-1, -1), 8),
                ('RIGHTPADDING', (0, 0), (-1, -1), 8),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ]))
            row.append(inner)
        grid_rows.append(row)

    grid = Table(grid_rows, colWidths=[cell_w, cell_w])
    grid.setStyle(TableStyle([
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 2),
        ('RIGHTPADDING', (0, 0), (-1, -1), 2),
    ]))
    items.append(grid)
    return items


# ---------------------------------------------------------------------------
# Section 9 : Multiple Intelligence Profile
# ---------------------------------------------------------------------------

def build_intelligence(mi_scores: Dict[str, float]) -> list:
    story = []
    story += section_header(9, 'Multiple Intelligence Profile')
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        'Your Multiple Intelligence profile is derived from the biometric analysis of '
        'all ten fingerprints. Each intelligence dimension corresponds to specific brain '
        'lobe activity patterns encoded in dermatoglyphic features.',
        STYLES['body']
    ))
    story.append(Spacer(1, 6))

    from ..charts import (create_intelligence_radar, create_intelligence_bar,
                          create_mi_full_bar)
    radar_b64    = create_intelligence_radar(mi_scores)
    bar_b64      = create_intelligence_bar(mi_scores)
    full_bar_b64 = create_mi_full_bar(mi_scores)

    from .helpers import two_col
    left_items = chart_image(radar_b64, width=CONTENT_W * 0.48,
                             caption='Intelligence Radar Chart')
    right_items = chart_image(bar_b64, width=CONTENT_W * 0.48,
                              caption='Ranked Intelligence Scores')
    story.append(two_col(left_items, right_items,
                         left_w=CONTENT_W * 0.50, right_w=CONTENT_W * 0.46))
    story.append(Spacer(1, 8))

    # Full ranked bar chart (detailed view)
    story += chart_image(full_bar_b64, width=CONTENT_W * 0.96,
                         caption='Full Multiple Intelligence Ranking with Score Levels')
    story.append(Spacer(1, 10))

    # Detailed interpretation table
    story += sub_heading('Intelligence Profile - Detailed Interpretation')
    header = [Paragraph(h, STYLES['table_header']) for h in
              ['Intelligence', 'Score', 'Level', 'Career Linkage', 'Development Activity']]
    rows = [header]
    sorted_mi = sorted(mi_scores.items(), key=lambda x: x[1], reverse=True)
    for k, v in sorted_mi:
        info = MI_INFO.get(k, (_label(k), '', '', ''))
        _, _, careers, activity = info
        _, level = score_color(v)
        rows.append([
            Paragraph(_label(k), STYLES['table_cell_bold']),
            Paragraph(f'{v*100:.0f}%', STYLES['table_cell_bold']),
            Paragraph(level, STYLES['table_cell']),
            Paragraph(careers, STYLES['table_cell']),
            Paragraph(activity, STYLES['table_cell']),
        ])
    cw = [CONTENT_W*0.19, CONTENT_W*0.09, CONTENT_W*0.13,
          CONTENT_W*0.31, CONTENT_W*0.24]
    t = Table(rows, colWidths=cw, repeatRows=1, splitByRow=1)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), NAVY),
        ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [GOLD_PALE, IVORY]),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('ALIGN', (1, 0), (2, -1), 'CENTER'),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('GRID', (0, 0), (-1, -1), 0.4, GOLD_LIGHT),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(t)
    return story


# ---------------------------------------------------------------------------
# Section 10 : Learning Style
# ---------------------------------------------------------------------------

def build_learning(learning_styles: Dict[str, float]) -> list:
    story = []
    story += section_header(10, 'Learning Style Analysis')
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        'Learning style analysis identifies how you most effectively receive, process, '
        'and retain new information. Understanding your learning style enables targeted '
        'study strategies that maximise retention and comprehension.',
        STYLES['body']
    ))
    story.append(Spacer(1, 6))

    from ..charts import create_learning_pie, create_learning_bar
    from .helpers import two_col
    pie_b64 = create_learning_pie(learning_styles)
    bar_b64 = create_learning_bar(learning_styles)
    left_items  = chart_image(pie_b64, width=CONTENT_W * 0.46,
                               caption='Learning Style Distribution')
    right_items = chart_image(bar_b64, width=CONTENT_W * 0.50,
                               caption='Style Strength Comparison')
    story.append(two_col(left_items, right_items,
                         left_w=CONTENT_W * 0.48, right_w=CONTENT_W * 0.48))
    story.append(Spacer(1, 8))

    dom_style = max(learning_styles.items(), key=lambda x: x[1])[0] \
                if learning_styles else None
    if dom_style is None:
        story.append(Paragraph(
            'Dominant learning style data not available from pipeline for this session.',
            STYLES['body']
        ))
        return story
    info = LEARNING_INFO.get(dom_style, LEARNING_INFO.get('visual', ('Unknown', '', [])))
    ls_name, ls_desc, strategies = info

    story += sub_heading(f'Primary Learning Style : {ls_name}')
    story.append(Paragraph(ls_desc, STYLES['body']))
    story.append(Spacer(1, 6))

    story += sub_heading('Recommended Study Strategies')
    for s in strategies:
        story.append(Paragraph(f'    {s}', STYLES['bullet']))
    story.append(Spacer(1, 8))

    # All styles score table
    story += sub_heading('Learning Style Scores')
    rows = [[Paragraph(h, STYLES['table_header'])
             for h in ['Learning Style', 'Score', 'Strength Level']]]
    for k, v in sorted(learning_styles.items(), key=lambda x: x[1], reverse=True):
        _, level = score_color(v)
        rows.append([Paragraph(_label(k), STYLES['table_cell']),
                     Paragraph(f'{v*100:.0f}%', STYLES['table_cell_bold']),
                     Paragraph(level, STYLES['table_cell'])])
    cw = [CONTENT_W * 0.45, CONTENT_W * 0.20, CONTENT_W * 0.30]
    lt = Table(rows, colWidths=cw)
    lt.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), NAVY),
        ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [GOLD_PALE, IVORY]),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('ALIGN', (1, 0), (2, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 0.4, GOLD_LIGHT),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(lt)
    return story


# ---------------------------------------------------------------------------
# Section 11 : Personality and Behavioral Profile
# ---------------------------------------------------------------------------

def build_personality(personality: Dict[str, float]) -> list:
    story = []
    story += section_header(11, 'Personality and Behavioral Profile')
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        'Personality analysis is based on the Five-Factor Model (Big Five), mapping '
        'openness, conscientiousness, extraversion, agreeableness, and emotional '
        'stability. These traits emerge from neurological patterns encoded in '
        'dermatoglyphic features.',
        STYLES['body']
    ))
    story.append(Spacer(1, 6))

    from ..charts import create_personality_radar, create_personality_bars
    from .helpers import two_col
    radar_b64 = create_personality_radar(personality)
    bars_b64  = create_personality_bars(personality)
    left_items  = chart_image(radar_b64, width=CONTENT_W * 0.46,
                               caption='Big Five Radar')
    right_items = chart_image(bars_b64, width=CONTENT_W * 0.50,
                               caption='Trait Score Breakdown')
    story.append(two_col(left_items, right_items,
                         left_w=CONTENT_W * 0.48, right_w=CONTENT_W * 0.48))
    story.append(Spacer(1, 8))

    # Trait table
    story += sub_heading('Big Five Trait Scores and Interpretation')
    rows = [[Paragraph(h, STYLES['table_header'])
             for h in ['Trait', 'Score', 'Level', 'Meaning']]]
    for k, v in personality.items():
        display_v = (1 - v) if k == 'neuroticism' else v
        _, level = score_color(display_v)
        name, meaning = BIG5_INFO.get(k, (_label(k), ''))
        rows.append([
            Paragraph(name, STYLES['table_cell_bold']),
            Paragraph(f'{display_v*100:.0f}%', STYLES['table_cell_bold']),
            Paragraph(level, STYLES['table_cell']),
            Paragraph(meaning, STYLES['table_cell']),
        ])
    cw = [CONTENT_W*0.24, CONTENT_W*0.10, CONTENT_W*0.16, CONTENT_W*0.46]
    pt = Table(rows, colWidths=cw)
    pt.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), NAVY),
        ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [GOLD_PALE, IVORY]),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('ALIGN', (1, 0), (2, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 0.4, GOLD_LIGHT),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(pt)

    # Introvert / Extrovert scale note (only when extraversion data exists)
    extraversion = personality.get('extraversion')
    if isinstance(extraversion, (int, float)):
        ie_label = 'Extroverted' if extraversion >= 0.55 else \
                   'Introverted' if extraversion <= 0.45 else 'Ambivert'
        story.append(Spacer(1, 8))
        story.append(Paragraph(
            f'Social Orientation: {ie_label}  (Extraversion score: {extraversion*100:.0f}%)',
            STYLES['label']
        ))

    # Derived style analysis (Communication / Decision / Leadership / Stress)
    style_items = _build_personality_styles(personality)
    if style_items:
        story.append(Spacer(1, 10))
        story += style_items

    return story


# ---------------------------------------------------------------------------
# Section 12 : Emotional Intelligence
# ---------------------------------------------------------------------------

def build_emotional(ext_results: Dict[str, Any]) -> list:
    # Header + intro live inside the first shrink_block (not in story
    # ahead of it) for the same reason as Sections 13/14/15: if the block
    # after them doesn't fit in whatever page space remains, ReportLab
    # defers the whole block to a fresh page and would strand the header
    # alone above a near-empty page otherwise.
    story = []
    block = []
    block += section_header_plain(12, 'Emotional Intelligence Profile')
    block.append(Spacer(1, 6))
    block.append(Paragraph(
        'Emotional Intelligence (EQ) reflects the ability to recognise, understand, '
        'manage, and express emotions effectively. High EQ is strongly correlated with '
        'relationship quality, leadership effectiveness, and overall well-being.',
        STYLES['body']
    ))
    block.append(Spacer(1, 6))

    eq_data = {}
    if isinstance(ext_results, dict):
        eq_data = ext_results.get('EmotionalIntelligenceExtension', {})
    if not eq_data:
        block.append(Paragraph('Emotional intelligence data not available.', STYLES['body']))
        story.append(shrink_block(block, max_height=_FULL_PAGE_MAX_H, _label='emotional_empty'))
        return story

    # Extract sub-scores for radar
    eq_sub = {k: float(v) for k, v in eq_data.items()
              if isinstance(v, (int, float)) and k not in
              ('emotional_intelligence_score', 'overall', 'score')}
    eq_overall = eq_data.get('emotional_intelligence_score',
                             eq_data.get('overall', None))
    eq_overall_str = f'{eq_overall*100:.0f}%' if isinstance(eq_overall, (int, float)) else 'N/A'

    from ..charts import create_eq_radar, create_extension_bar
    if eq_sub:
        # Radar is roughly square (5.5x5in native); embedding it at the
        # default ~88% content width blew it up to ~5.4in tall on its own —
        # more than half the combined radar+table block's total height.
        # It doesn't need full page width to stay legible, so cap it at
        # ~60% width, which proportionally shrinks its height too.
        radar_b64 = create_eq_radar(eq_sub)
        block += chart_image(radar_b64, width=CONTENT_W * 0.60,
                             caption='Emotional Intelligence Sub-Dimensions')
        block.append(Spacer(1, 6))

    block += sub_heading(f'Overall EQ Score : {eq_overall_str}')

    # EQ score table is built as a SEPARATE block below (see block_2): the
    # radar chart + 12-row table combined measured ~11.8in tall against
    # ~8.7-10in available on one page, so a single shrink_block scaled every
    # font in this section down ~25%. Splitting lets the radar (which fits
    # comfortably alone) render at full scale, and the table flows onto a
    # fresh page at full scale too if it doesn't fit the remaining space.
    block_2 = []
    if eq_sub:
        block_2 += sub_heading('EQ Sub-Dimension Scores')
        rows = [[Paragraph(h, STYLES['table_header'])
                 for h in ['Dimension', 'Score', 'Level']]]
        for k, v in sorted(eq_sub.items(), key=lambda x: x[1], reverse=True):
            _, level = score_color(v)
            rows.append([
                Paragraph(_label(k), STYLES['table_cell']),
                Paragraph(f'{v*100:.0f}%', STYLES['table_cell_bold']),
                Paragraph(level, STYLES['table_cell']),
            ])
        cw = [CONTENT_W * 0.56, CONTENT_W * 0.20, CONTENT_W * 0.20]
        t = Table(rows, colWidths=cw)
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), NAVY),
            ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [GOLD_PALE, IVORY]),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('ALIGN', (1, 0), (2, -1), 'CENTER'),
            ('GRID', (0, 0), (-1, -1), 0.4, GOLD_LIGHT),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        block_2.append(t)

    story.append(shrink_block(block, max_height=_FULL_PAGE_MAX_H, _label='emotional_radar'))
    if block_2:
        story.append(shrink_block(block_2, max_height=_FULL_PAGE_MAX_H, _label='emotional_table'))
    return story
