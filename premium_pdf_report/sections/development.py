"""
Section 17 : Parenting and Teacher Guidelines
Section 18 : Development Roadmap and Remedies
Section 19 : Counsellor's Professional Note
"""

from typing import Dict, Any, List
from reportlab.platypus import Paragraph, Spacer, Table, TableStyle
from reportlab.lib.units import inch

from ..theme import (STYLES, NAVY, GOLD, GOLD_DARK, GOLD_LIGHT, GOLD_PALE,
                     IVORY, WHITE, SAGE, PLUM, GREEN_STRONG, TERRACOTTA,
                     CONTENT_W, score_color)
from .helpers import section_header, sub_heading

REMEDIES = {
    'linguistic': [
        'Read aloud daily for 15 minutes.',
        'Keep a vocabulary journal and learn 5 new words per day.',
        'Practise storytelling and narrative writing.',
        'Join a debate or public speaking club.',
    ],
    'logical_mathematical': [
        'Solve Sudoku or logic puzzles daily.',
        'Explore coding games and programming basics.',
        'Practise mental arithmetic and estimation.',
        'Play strategy board games (chess, Rubik\'s cube).',
    ],
    'spatial': [
        'Draw, sketch, or practise mind mapping regularly.',
        'Build LEGO or 3D models from instructions.',
        'Play spatial reasoning video games.',
        'Study maps and practise orienteering.',
    ],
    'musical': [
        'Learn to play a musical instrument.',
        'Study basic music theory and rhythm patterns.',
        'Listen analytically to different music genres.',
        'Compose simple melodies or rhythms.',
    ],
    'bodily_kinesthetic': [
        'Practise yoga, martial arts, or dance.',
        'Engage in a regular sport or physical activity.',
        'Take movement breaks during study sessions.',
        'Learn through hands-on experiments and models.',
    ],
    'interpersonal': [
        'Join team projects, clubs, or community groups.',
        'Practise active listening in conversations.',
        'Volunteer in social or community roles.',
        'Engage in cooperative group activities.',
    ],
    'intrapersonal': [
        'Keep a daily reflective journal.',
        'Practise mindfulness or meditation for 10 minutes daily.',
        'Set personal goals and review weekly.',
        'Explore self-assessment personality tools.',
    ],
    'naturalistic': [
        'Maintain a plant garden or nature journal.',
        'Observe birds, insects, or local ecosystems.',
        'Study biology and environmental science.',
        'Take regular walks in natural settings.',
    ],
}

DAILY_ROUTINE = [
    ('6:00 - 6:30 am', 'Morning meditation and breathing exercises'),
    ('6:30 - 7:00 am', 'Physical exercise or yoga'),
    ('7:00 - 7:30 am', 'Healthy breakfast and hydration'),
    ('8:00 am - 12:00 pm', 'Primary study block (peak focus hours)'),
    ('12:00 - 1:00 pm', 'Lunch and outdoor break'),
    ('1:00 - 3:00 pm', 'Secondary study or creative activity'),
    ('3:00 - 4:00 pm', 'Extracurricular or skill development'),
    ('4:00 - 5:30 pm', 'Sport, physical activity, or nature time'),
    ('6:00 - 7:00 pm', 'Reading or independent learning'),
    ('7:00 - 8:00 pm', 'Family time and social interaction'),
    ('8:00 - 9:00 pm', 'Light revision or creative hobby'),
    ('9:30 pm', 'Screen-free wind-down, journaling, sleep preparation'),
]


def _label(key: str) -> str:
    return key.replace('_', ' ').title()


# ---------------------------------------------------------------------------
# Section 17 : Parenting and Teacher Guidelines
# ---------------------------------------------------------------------------

def build_parenting(learning_styles: Dict[str, float],
                    personality: Dict[str, float]) -> list:
    story = []
    story += section_header(17, 'Parenting and Teacher Guidelines')
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        'The following guidelines are tailored to the candidate\'s learning style '
        'and personality profile. Applying these strategies at home and in the '
        'classroom will support holistic development and maximise potential.',
        STYLES['body']
    ))
    story.append(Spacer(1, 8))

    dom_ls = max(learning_styles.items(), key=lambda x: x[1])[0] \
             if learning_styles else None
    openness = personality.get('openness') if personality else None
    conscientiousness = personality.get('conscientiousness') if personality else None

    story += sub_heading('Parenting Guidelines')

    parenting_dos = [
        f'Provide {(dom_ls or "multi-modal")} learning materials and '
        f'{"diverse" if (openness or 0) >= 0.6 else "structured"} activities.',
        'Celebrate effort and process, not just outcomes.',
        'Encourage strengths while gently developing weaker areas.',
        'Create a consistent, structured daily routine.'
        if (conscientiousness or 0.5) < 0.55
        else 'Allow creative freedom within a flexible structure.',
        'Engage in open, supportive conversations about emotions.',
        'Expose the child to diverse experiences and environments.',
    ]

    parenting_donts = [
        'Avoid comparison with siblings or peers.',
        'Do not force activities that conflict with natural strengths.',
        'Avoid over-scheduling - allow free play and exploration time.',
        'Do not use criticism without constructive alternatives.',
        'Avoid excessive screen time, especially before sleep.',
    ]

    dos_rows = [[Paragraph(h, STYLES['table_header'])
                 for h in ['Parenting Dos', 'Parenting Avoid']]]
    max_r = max(len(parenting_dos), len(parenting_donts))
    for i in range(max_r):
        d = parenting_dos[i] if i < len(parenting_dos) else ''
        a = parenting_donts[i] if i < len(parenting_donts) else ''
        dos_rows.append([
            Paragraph(f'    {d}', STYLES['table_cell']),
            Paragraph(f'    {a}', STYLES['table_cell']),
        ])
    cw = [CONTENT_W * 0.50, CONTENT_W * 0.46]
    pt = Table(dos_rows, colWidths=cw)
    pt.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, 0), GREEN_STRONG),
        ('BACKGROUND', (1, 0), (1, 0), TERRACOTTA),
        ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [GOLD_PALE, IVORY]),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 0.4, GOLD_LIGHT),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(pt)
    story.append(Spacer(1, 10))

    story += sub_heading('Teacher and Classroom Strategy Guidelines')
    teacher_rows = [[Paragraph(h, STYLES['table_header'])
                     for h in ['Strategy Area', 'Recommendation']]]
    teacher_strategies = [
        ('Teaching Method', f'Use {(dom_ls or "multi-modal")} demonstrations, real-world examples, and multi-modal instruction.'),
        ('Classroom Seating', 'Front-centre positioning for optimal engagement and board visibility.'),
        ('Assessment Style', 'Offer project-based, portfolio, or oral assessment options alongside written tests.'),
        ('Motivation Technique', 'Set achievable short-term milestones with visible progress tracking.'),
        ('Attention Strategy', 'Use the Pomodoro technique (25-minute focused blocks with 5-minute breaks).'),
        ('Group Work', 'Assign team roles that align with interpersonal strengths.'),
        ('Remediation', 'Provide extra time and alternative formats for areas of development.'),
    ]
    for area, rec in teacher_strategies:
        teacher_rows.append([
            Paragraph(area, STYLES['table_cell_bold']),
            Paragraph(rec, STYLES['table_cell']),
        ])
    cw2 = [CONTENT_W * 0.26, CONTENT_W * 0.70]
    tt = Table(teacher_rows, colWidths=cw2)
    tt.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), NAVY),
        ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [GOLD_PALE, IVORY]),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 0.4, GOLD_LIGHT),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(tt)
    return story


# ---------------------------------------------------------------------------
# Section 18 : Development Roadmap and Remedies
# ---------------------------------------------------------------------------

def build_development(mi: Dict[str, float]) -> list:
    story = []
    story += section_header(18, 'Development Roadmap and Remedies')
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        'This section provides a personalised 30-day development plan and specific '
        'activity-based remedies for intelligence areas that benefit from targeted '
        'practice. Consistent daily effort in these activities will progressively '
        'strengthen identified development areas.',
        STYLES['body']
    ))
    story.append(Spacer(1, 8))

    # Remedies for weak MI areas
    story += sub_heading('Targeted Remedial Activities')
    if mi:
        weak_areas = [(k, v) for k, v in mi.items() if v < 0.55]
        weak_areas.sort(key=lambda x: x[1])
        if weak_areas:
            for k, v in weak_areas[:5]:
                rem_list = REMEDIES.get(k, ['Practise relevant activities daily.'])
                story.append(Paragraph(
                    f'For {_label(k)} (Score: {v*100:.0f}%)',
                    STYLES['sub_heading']
                ))
                for r in rem_list:
                    story.append(Paragraph(f'    {r}', STYLES['bullet']))
                story.append(Spacer(1, 4))
        else:
            story.append(Paragraph(
                'All intelligence areas are at a strong level. Focus on maintaining and '
                'advancing dominant intelligences through advanced activities.',
                STYLES['body']
            ))
    story.append(Spacer(1, 8))

    # 30-day plan table
    story += sub_heading('30-Day Personalised Development Plan')
    plan_rows = [[Paragraph(h, STYLES['table_header'])
                  for h in ['Week', 'Focus Area', 'Daily Activity', 'Goal']]]
    plan_items = []
    if mi:
        sorted_weak = sorted(
            [(k, v) for k, v in mi.items() if isinstance(v, (int, float))],
            key=lambda x: x[1]
        )
        for i, (k, v) in enumerate(sorted_weak[:4]):
            week = f'Week {i + 1}'
            acts = REMEDIES.get(k, ['Practise relevant activities.'])
            # Express the goal in terms of relative progress from the actual score
            current_pct = int(v * 100)
            target_pct = min(100, current_pct + 15)
            plan_items.append((week, _label(k), acts[0],
                                f'Raise {_label(k)} from {current_pct}% to {target_pct}%'))
    if not plan_items:
        plan_items = [('Week 1-4', 'All Intelligences',
                       'Balanced daily practice', 'Maintain peak performance')]
    for row in plan_items:
        plan_rows.append([Paragraph(str(c), STYLES['table_cell'])
                          for c in row])
    cw = [CONTENT_W*0.14, CONTENT_W*0.24, CONTENT_W*0.38, CONTENT_W*0.20]
    plt_t = Table(plan_rows, colWidths=cw)
    plt_t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), NAVY),
        ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [GOLD_PALE, IVORY]),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 0.4, GOLD_LIGHT),
        ('LEFTPADDING', (0, 0), (-1, -1), 7),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(plt_t)
    story.append(Spacer(1, 10))

    # Daily routine
    story += sub_heading('Recommended Daily Development Routine')
    routine_rows = [[Paragraph(h, STYLES['table_header'])
                     for h in ['Time', 'Activity']]]
    for time_slot, activity in DAILY_ROUTINE:
        routine_rows.append([
            Paragraph(time_slot, STYLES['table_cell_bold']),
            Paragraph(activity, STYLES['table_cell']),
        ])
    cw2 = [CONTENT_W * 0.28, CONTENT_W * 0.68]
    rt = Table(routine_rows, colWidths=cw2)
    rt.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), GOLD_DARK),
        ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [GOLD_PALE, IVORY]),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 0.4, GOLD_LIGHT),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(rt)
    return story


# ---------------------------------------------------------------------------
# Section 19 : Counsellor's Professional Note
# ---------------------------------------------------------------------------

def build_counsellor_note(report_data: Dict[str, Any],
                           session: Dict[str, Any]) -> list:
    story = []
    story += section_header(19, "Counsellor's Professional Note")
    story.append(Spacer(1, 8))

    mi = report_data.get('intelligence_scores', {})
    learning = report_data.get('learning_styles', {})
    subject = session.get('subject_name', 'the candidate')
    counsellor = session.get('counsellor', 'Certified DMIT Counsellor')

    dom_mi_key = max(mi.items(), key=lambda x: x[1])[0] if mi else None
    weak_mi_key = min(mi.items(), key=lambda x: x[1])[0] if mi else None
    dom_ls = max(learning.items(), key=lambda x: x[1])[0].title() if learning else None

    if dom_mi_key is None or weak_mi_key is None:
        story.append(Paragraph(
            'Insufficient intelligence profile data to generate a personalised counsellor note. '
            'Please ensure fingerprint images were captured with sufficient clarity for full analysis.',
            STYLES['body']
        ))
        return story

    ls_phrase = f'As a primary {dom_ls} learner, {subject} will benefit most from study ' \
                f'environments and teaching methodologies that align with this learning orientation. ' \
                if dom_ls else f'{subject} will benefit from multi-modal learning environments. '

    note_text = (
        f'Based on the comprehensive biometric analysis conducted for {subject}, '
        f'the following professional observations are noted. The candidate demonstrates '
        f'a naturally strong aptitude in {_label(dom_mi_key)}, which represents a '
        f'significant innate strength that should be actively nurtured and developed. '
        f'{ls_phrase}'
        f'\n\n'
        f'The area of {_label(weak_mi_key)} presents the most significant opportunity '
        f'for growth. With consistent, targeted practice using the remedial activities '
        f'outlined in Section 18, meaningful improvement in this dimension is achievable '
        f'over a 3 to 6 month period. '
        f'\n\n'
        f'It is recommended that parents and educators focus on creating a supportive, '
        f'strength-based environment that celebrates natural abilities while providing '
        f'gentle, consistent encouragement in developmental areas. The candidate\'s innate '
        f'potential is substantial, and with appropriate guidance and environment, '
        f'meaningful academic, personal, and professional achievement is well within reach.'
    )

    story.append(Paragraph(note_text, STYLES['counsellor']))
    story.append(Spacer(1, 16))

    story += sub_heading('Key Recommendations')
    recs = [
        f'Prioritise {_label(dom_mi_key)}-oriented activities and career exploration.',
        f'Implement daily {dom_ls.lower() if dom_ls else "multi-modal"} learning strategies for all subjects.',
        f'Dedicate 15-20 minutes daily to {_label(weak_mi_key)} development exercises.',
        'Maintain a consistent daily routine aligned with the recommended schedule.',
        'Review progress quarterly and update development activities accordingly.',
        'Seek enrichment opportunities that combine natural strengths with new challenges.',
    ]
    for rec in recs:
        story.append(Paragraph(f'    {rec}', STYLES['bullet']))
    story.append(Spacer(1, 20))

    # Signature section
    from reportlab.platypus import HRFlowable
    sig_rows = [
        [Paragraph('Counsellor Name', STYLES['table_cell_bold']),
         Paragraph(counsellor, STYLES['table_cell']),
         Paragraph('Signature', STYLES['table_cell_bold']),
         Paragraph('_______________________', STYLES['table_cell'])],
        [Paragraph('Qualification', STYLES['table_cell_bold']),
         Paragraph('Certified DMIT Analyst', STYLES['table_cell']),
         Paragraph('Date', STYLES['table_cell_bold']),
         Paragraph('_______________________', STYLES['table_cell'])],
        [Paragraph('Organisation', STYLES['table_cell_bold']),
         Paragraph('Ridge Analysis', STYLES['table_cell']),
         Paragraph('Report ID', STYLES['table_cell_bold']),
         Paragraph(session.get('report_id', 'RA-2026'), STYLES['table_cell'])],
    ]
    cw = [CONTENT_W*0.22, CONTENT_W*0.26, CONTENT_W*0.22, CONTENT_W*0.26]
    sig_t = Table(sig_rows, colWidths=cw)
    sig_t.setStyle(TableStyle([
        ('BOX', (0, 0), (-1, -1), 1.2, GOLD),
        ('LINEBELOW', (0, 0), (-1, -2), 0.4, GOLD_LIGHT),
        ('BACKGROUND', (0, 0), (-1, -1), GOLD_PALE),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
    ]))
    story.append(sig_t)
    story.append(Spacer(1, 16))

    story.append(Paragraph(
        'This report is generated by the Ridge Analysis DMIT System. '
        'All data is derived from biometric fingerprint analysis. '
        'For counselling appointments and follow-up sessions, contact your '
        'certified DMIT counsellor.',
        STYLES['caption']
    ))

    return story
