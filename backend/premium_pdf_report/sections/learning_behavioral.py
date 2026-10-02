from __future__ import annotations

from typing import Any, Dict, List

from reportlab.platypus import Paragraph, Spacer, Table, TableStyle, HRFlowable, PageBreak
from reportlab.lib.units import inch
from reportlab.lib import colors

from ..theme import (
    STYLES, NAVY, GOLD, GOLD_DARK, GOLD_LIGHT, GOLD_PALE,
    IVORY, WHITE, CONTENT_W,
)
from .helpers import shrink_block, SectionHeader, chart_image, institutional_table, institutional_card
from ..charts import (
    generate_task_people_donut,
    generate_analysis_action_divergence,
)
from ..assets.boho_vectors import (
    draw_boho_learning_visual,
    draw_boho_learning_auditory,
    draw_boho_learning_kinesthetic,
    draw_boho_habits_vision,
    draw_boho_habits_synergy,
    draw_boho_habits_empathy,
    draw_boho_habits_renewal,
    draw_boho_leadership_alignment,
    draw_boho_cognitive_processing,
    draw_boho_collaboration_dynamics,
    draw_boho_behavioral_ambition,
    draw_boho_behavioral_equilibrium,
)


def build_pages_23_34_learning_behavioral(report_data: Dict[str, Any]) -> list:
    pages: list = []
    ls = report_data.get('learning_styles', {})
    pb = report_data.get('personality_behavior', {})
    ext = report_data.get('extension_results', {})

    v_val = float(ls.get('visual', 0.42))
    a_val = float(ls.get('auditory', 0.32))
    k_val = float(ls.get('kinesthetic', 0.26))
    total_vak = v_val + a_val + k_val or 1.0
    v_pct = (v_val / total_vak) * 100
    a_pct = (a_val / total_vak) * 100
    k_pct = (k_val / total_vak) * 100

    def _make_vak_page(mod_num: int, title: str, pct: float, icon_col: str,
                       chars: list[str], tips: list[str], neuro: str, art_flowable=None) -> list:
        blk = []
        blk.append(SectionHeader(8, f"PRIMARY MODALITY LEARNING STYLES: {title.upper()}"))
        blk.append(HRFlowable(width=CONTENT_W, thickness=1.0, color=GOLD, spaceAfter=12, spaceBefore=4))

        score_html = (
            f'<font size="12" color="{NAVY.hexval()}"><b>MODALITY SHARE: {pct:.1f}%</b></font><br/>'
            f'<font size="8" color="{GOLD_DARK.hexval()}">{neuro}</font>'
        )
        t_sc = institutional_card([Paragraph(score_html, STYLES['body'])], width=CONTENT_W, border_color=GOLD, bg_color=GOLD_PALE)
        blk.append(t_sc)
        blk.append(Spacer(1, 12))

        blk.append(Paragraph(f'<font size="10.5" color="{NAVY.hexval()}"><b>Cognitive Characteristics of {title} Learners</b></font>', STYLES['body']))
        blk.append(Spacer(1, 6))

        c_html = ''.join([f'&bull; {c}<br/>' for c in chars])
        t_c = institutional_card([Paragraph(f'<font size="8.5" color="#1F2937">{c_html}</font>', STYLES['body'])], width=CONTENT_W, border_color=GOLD_LIGHT, bg_color=IVORY)
        blk.append(t_c)
        blk.append(Spacer(1, 14))

        blk.append(Paragraph(f'<font size="10.5" color="{NAVY.hexval()}"><b>Tailored Actionable Study Strategies</b></font>', STYLES['body']))
        blk.append(Spacer(1, 6))

        t_html = ''.join([f'&bull; {t}<br/>' for t in tips])
        t_t = institutional_card([Paragraph(f'<font size="8.5" color="#1F2937">{t_html}</font>', STYLES['body'])], width=CONTENT_W, border_color=GOLD, bg_color=GOLD_PALE)
        blk.append(t_t)

        if art_flowable:
            blk.append(Spacer(1, 14))
            blk.append(art_flowable)

        return [shrink_block(blk, max_height=9.2 * inch, _label=f'vak_page_{mod_num}')]

    v_chars = [
        'Rapidly assimilates information presented in pictorial, diagrammatic, and infographic formats.',
        'Relies on spatial mental mapping and mental photography to retrieve archived data during examinations.',
        'High sensitivity to environmental visual clutter; requires an organized, clean physical workspace.',
        'Benefits from color-coding concepts, flowcharts, and hierarchical mind-map summaries.',
    ]
    v_tips = [
        '<b>Mind Mapping &amp; Concept Flowcharts:</b> Convert text chapters into spatial visual trees before exams.',
        '<b>Chromatic Highlighter System:</b> Standardize highlighters (e.g., Gold for core theories, Terracotta for dates, Sage for definitions).',
        '<b>Spatial Flashcards:</b> Utilize visual digital flashcards with integrated diagrams and high-contrast cues.',
        '<b>Quiet Visual Sanctuary:</b> Ensure study desk faces a blank neutral wall rather than active doorways or windows.',
    ]
    pages.append(_make_vak_page(23, "Visual Learning Modality", v_pct, "#1E3A8A", v_chars, v_tips, "Primary Occipital Lobe Sensory Pathway (Little Fingers L5/R5)", draw_boho_learning_visual(width=CONTENT_W, height=110))[0])
    pages.append(PageBreak())

    a_chars = [
        'Absorbs concepts seamlessly through oral lectures, classroom discussions, and audiobooks.',
        'Demonstrates heightened tone and cadence recall; remembers spoken explanations word-for-word.',
        'Internal vocalizer who often sub-vocalizes or reads aloud when encountering complex syntax.',
        'Vulnerable to auditory distractions; background music with lyrics hampers cognitive retention.',
    ]
    a_tips = [
        '<b>Audio Memo Summaries:</b> Record 3-minute spoken summaries of key chapters and review while commuting.',
        '<b>Verbal Recitation:</b> Teach complex concepts to a peer or recite formulas aloud to solidify phonetic memory.',
        '<b>Socratic Study Groups:</b> Engage in structured group debates to process contrasting perspectives.',
        '<b>Acoustic Calibration:</b> Utilize 40Hz binaural beats or brown noise to shield against irregular environmental noise.',
    ]
    pages.append(_make_vak_page(24, "Auditory Learning Modality", a_pct, "#C46849", a_chars, a_tips, "Primary Temporal Lobe Auditory Pathway (Ring Fingers L4/R4)", draw_boho_learning_auditory(width=CONTENT_W, height=110))[0])
    pages.append(PageBreak())

    k_chars = [
        'Learns by physical experimentation, touch, tactile manipulation, and bodily movement.',
        'High motor restlessness during sedentary lectures; thrives when allowed to pace or gesture.',
        'Possesses muscle memory; retains processes best after hands-on physical rehearsal.',
        'Prefers real-world case studies and tangible laboratory models over theoretical treatises.',
    ]
    k_tips = [
        '<b>Tactile Note-Taking &amp; Modeling:</b> Build physical models, write notes by hand with textured pens.',
        '<b>Kinetic Study Intervals:</b> Pace while reciting concepts; utilize standing desks or balance boards.',
        '<b>Role-Play Simulations:</b> Re-enact historical events or scientific interactions physically.',
        '<b>Pomodoro Movement Rest:</b> 25-minute study sprints punctuated by 5-minute physical stretching intervals.',
    ]
    pages.append(_make_vak_page(25, "Kinesthetic Learning Modality", k_pct, "#5A7865", k_chars, k_tips, "Primary Parietal Lobe Somatosensory Pathway (Middle Fingers L3/R3)", draw_boho_learning_kinesthetic(width=CONTENT_W, height=110))[0])
    pages.append(PageBreak())

    def _make_habit_card(h_num: str, h_title: str, h_sub: str, h_score: float, h_guidance: str, col: str) -> Table:
        c_html = (
            f'<font size="9.5" color="{NAVY.hexval()}"><b>HABIT {h_num}: {h_title.upper()}</b></font><br/>'
            f'<font size="8" color="{GOLD_DARK.hexval()}"><i>{h_sub}</i></font><br/><br/>'
            f'<font size="8.5" color="#1F2937">{h_guidance}</font><br/><br/>'
            f'<font size="7.5" color="#4B5563">Innate Efficacy Index:</font> '
            f'<font size="10.5" color="{GOLD_DARK.hexval()}"><b>{h_score*100:.0f}%</b></font>'
        )
        return institutional_card([Paragraph(c_html, STYLES['body'])], width=CONTENT_W, border_color=GOLD, bg_color=GOLD_PALE)

    p26_blk = []
    p26_blk.append(SectionHeader(8, "EFFICACY & SELF-MANAGEMENT: HABITS 1 & 2"))
    p26_blk.append(HRFlowable(width=CONTENT_W, thickness=1.0, color=GOLD, spaceAfter=12, spaceBefore=4))
    p26_blk.append(_make_habit_card('1', 'Be Proactive', 'Personal Vision & Responsibility', 0.78,
                                   'Take the initiative to create positive outcomes rather than merely reacting to external stimuli. Cultivate an internal locus of control.', '#1E3A8A'))
    p26_blk.append(Spacer(1, 10))
    p26_blk.append(_make_habit_card('2', 'Begin with the End in Mind', 'Mental Creation & Long-Term Purpose', 0.82,
                                   'Envision desired future achievements prior to commencing execution. Formulate clear criteria for long-term projects.', '#C46849'))
    p26_blk.append(Spacer(1, 14))
    p26_blk.append(draw_boho_habits_vision(width=CONTENT_W, height=120))
    pages.append(shrink_block(p26_blk, max_height=9.2 * inch, _label='habits_page_26'))
    pages.append(PageBreak())

    p27_blk = []
    p27_blk.append(SectionHeader(8, "EFFICACY & SELF-MANAGEMENT: HABITS 3 & 4"))
    p27_blk.append(HRFlowable(width=CONTENT_W, thickness=1.0, color=GOLD, spaceAfter=12, spaceBefore=4))
    p27_blk.append(_make_habit_card('3', 'Put First Things First', 'Prioritization & Time Matrix', 0.74,
                                   'Organize and execute around non-urgent, highly important priorities (Quadrant II). Eliminate trivial distractions.', '#5A7865'))
    p27_blk.append(Spacer(1, 10))
    p27_blk.append(_make_habit_card('4', 'Think Win-Win', 'Mutual Benefit & Interpersonal EQ', 0.76,
                                   'Approach negotiations and collaborative projects seeking agreements that satisfy all parties, establishing psychological safety.', '#D99B38'))
    p27_blk.append(Spacer(1, 14))
    p27_blk.append(draw_boho_habits_synergy(width=CONTENT_W, height=120))
    pages.append(shrink_block(p27_blk, max_height=9.2 * inch, _label='habits_page_27'))
    pages.append(PageBreak())

    p28_blk = []
    p28_blk.append(SectionHeader(8, "EFFICACY & SELF-MANAGEMENT: HABITS 5 & 6"))
    p28_blk.append(HRFlowable(width=CONTENT_W, thickness=1.0, color=GOLD, spaceAfter=12, spaceBefore=4))
    p28_blk.append(_make_habit_card('5', 'Seek First to Understand', 'Empathy & Active Listening', 0.72,
                                   'Listen with the intent to genuinely comprehend emotional and logical perspectives before formulating advisory responses.', '#1E3A8A'))
    p28_blk.append(Spacer(1, 10))
    p28_blk.append(_make_habit_card('6', 'Synergize', 'Creative Cooperation & Synthesis', 0.75,
                                   'Combine individual strengths through collaborative teamwork, producing outcomes superior to solitary efforts.', '#C46849'))
    p28_blk.append(Spacer(1, 14))
    p28_blk.append(draw_boho_habits_empathy(width=CONTENT_W, height=120))
    pages.append(shrink_block(p28_blk, max_height=9.2 * inch, _label='habits_page_28'))
    pages.append(PageBreak())

    p29_blk = []
    p29_blk.append(SectionHeader(8, "EFFICACY & SELF-MANAGEMENT: HABIT 7 & SUMMARY"))
    p29_blk.append(HRFlowable(width=CONTENT_W, thickness=1.0, color=GOLD, spaceAfter=12, spaceBefore=4))
    p29_blk.append(_make_habit_card('7', 'Sharpen the Saw', 'Continuous Renewal & Equilibrium', 0.70,
                                   'Regularly renew physical, mental, social-emotional, and spiritual dimensions to sustain peak long-term executive capacity.', '#5A7865'))
    p29_blk.append(Spacer(1, 12))
    summary_html = (
        f'<font size="9.5" color="{NAVY.hexval()}"><b>Efficacy Synthesis: Habit Mastery Index</b></font><br/>'
        '<font size="8.5" color="#1F2937">'
        'The candidate demonstrates exceptional fluency in proactive vision (Habit 1 &amp; 2) and mutual collaboration (Habit 4). '
        'Long-term leverage will be maximized by continuing to reinforce structured Quadrant II prioritization (Habit 3) '
        'and institutionalizing scheduled rest intervals (Habit 7).'
        '</font>'
    )
    t_sum = institutional_card([Paragraph(summary_html, STYLES['body'])], width=CONTENT_W, border_color=GOLD_LIGHT, bg_color=IVORY)
    p29_blk.append(t_sum)
    p29_blk.append(Spacer(1, 14))
    p29_blk.append(draw_boho_habits_renewal(width=CONTENT_W, height=120))
    pages.append(shrink_block(p29_blk, max_height=9.2 * inch, _label='habits_page_29'))
    pages.append(PageBreak())

    p30_blk = []
    p30_blk.append(SectionHeader(8, "OPERATIONAL LEADERSHIP ALIGNMENT: TASK VS. PEOPLE"))
    p30_blk.append(HRFlowable(width=CONTENT_W, thickness=1.0, color=GOLD, spaceAfter=10, spaceBefore=4))

    task_score = float(pb.get('conscientiousness', 0.68) * 0.6 + ls.get('visual', 0.42) * 0.4)
    people_score = float(pb.get('agreeableness', 0.70) * 0.5 + pb.get('extraversion', 0.65) * 0.5)

    d_b64 = generate_task_people_donut(task_score, people_score)
    d_imgs = chart_image(d_b64, width=CONTENT_W * 0.72)
    if d_imgs:
        p30_blk.extend(d_imgs)
        p30_blk.append(Spacer(1, 8))

    lead_text = (
        f'<font size="10" color="{NAVY.hexval()}"><b>Leadership Style Interpretation</b></font><br/>'
        f'<font size="8.5" color="#1F2937">'
        f'The candidate exhibits a balanced leadership orientation ({task_score*100/(task_score+people_score):.1f}% Task vs. '
        f'{people_score*100/(task_score+people_score):.1f}% People). This enables them to drive projects to completion '
        f'under strict timelines while maintaining psychological safety and collaborative morale among team members.'
        f'</font>'
    )
    t_lead = institutional_card([Paragraph(lead_text, STYLES['body'])], width=CONTENT_W, border_color=GOLD, bg_color=GOLD_PALE)
    p30_blk.append(t_lead)
    p30_blk.append(Spacer(1, 12))
    p30_blk.append(draw_boho_leadership_alignment(width=CONTENT_W, height=105))
    pages.append(shrink_block(p30_blk, max_height=9.2 * inch, _label='leadership_page_30'))
    pages.append(PageBreak())

    p31_blk = []
    p31_blk.append(SectionHeader(8, "COGNITIVE PROCESSING: ANALYSIS VS. ACTION RATIO"))
    p31_blk.append(HRFlowable(width=CONTENT_W, thickness=1.0, color=GOLD, spaceAfter=10, spaceBefore=4))

    anal_val = float(pb.get('conscientiousness', 0.70))
    act_val = float(pb.get('extraversion', 0.65))

    bar_b64 = generate_analysis_action_divergence(anal_val, act_val)
    b_imgs = chart_image(bar_b64, width=CONTENT_W * 0.88)
    if b_imgs:
        p31_blk.extend(b_imgs)
        p31_blk.append(Spacer(1, 12))

    anal_text = (
        f'<font size="10" color="{NAVY.hexval()}"><b>Ideation vs. Execution Dynamics</b></font><br/>'
        '<font size="8.5" color="#1F2937">'
        '<b>Reflective Thought (Analytical Tank):</b> Measures the tendency to perform deep pre-computation, '
        'scenario modeling, and risk identification before taking action.<br/><br/>'
        '<b>Direct Execution (Action Taker):</b> Measures the speed of moving from decision to real-world implementation, '
        'rapid prototyping, and iterating on live feedback.'
        '</font>'
    )
    t_anal = institutional_card([Paragraph(anal_text, STYLES['body'])], width=CONTENT_W, border_color=GOLD_LIGHT, bg_color=IVORY)
    p31_blk.append(t_anal)
    p31_blk.append(Spacer(1, 12))
    p31_blk.append(draw_boho_cognitive_processing(width=CONTENT_W, height=105))
    pages.append(shrink_block(p31_blk, max_height=9.2 * inch, _label='processing_page_31'))
    pages.append(PageBreak())

    p32_blk = []
    p32_blk.append(SectionHeader(8, "COLLABORATION DYNAMICS: LEADERSHIP VS. SUPPORT"))
    p32_blk.append(HRFlowable(width=CONTENT_W, thickness=1.0, color=GOLD, spaceAfter=12, spaceBefore=4))

    lead_cap = float(pb.get('extraversion', 0.65) * 0.5 + pb.get('conscientiousness', 0.68) * 0.5)
    supp_cap = float(pb.get('agreeableness', 0.70) * 0.6 + pb.get('emotional_stability', 0.64) * 0.4)

    collab_rows = [
        [
            Paragraph('<b>Role Dimension</b>', STYLES['table_header']),
            Paragraph('<b>Capacity Index</b>', STYLES['table_header']),
            Paragraph('<b>Behavioral Tendencies</b>', STYLES['table_header']),
            Paragraph('<b>Ideal Team Environment</b>', STYLES['table_header']),
        ],
        [
            Paragraph('Team Leadership Capacity', STYLES['table_cell_bold']),
            Paragraph(f'<b>{lead_cap*100:.1f}%</b>', STYLES['table_cell_bold']),
            Paragraph('Directs strategy, enforces accountability, motivates peers.', STYLES['table_cell']),
            Paragraph('Autonomous squads, project management oversight.', STYLES['table_cell']),
        ],
        [
            Paragraph('Team Contributor / Player', STYLES['table_cell_bold']),
            Paragraph(f'<b>{supp_cap*100:.1f}%</b>', STYLES['table_cell_bold']),
            Paragraph('Harmonizes differences, executes shared assignments, supports team consensus.', STYLES['table_cell']),
            Paragraph('Cross-functional collaborative forums, peer review teams.', STYLES['table_cell']),
        ],
    ]
    t_collab = institutional_table(
        collab_rows,
        col_widths=[CONTENT_W * 0.25, CONTENT_W * 0.16, CONTENT_W * 0.32, CONTENT_W * 0.27],
        center_cols=[1],
    )
    p32_blk.append(t_collab)
    p32_blk.append(Spacer(1, 14))
    p32_blk.append(draw_boho_collaboration_dynamics(width=CONTENT_W, height=115))
    pages.append(shrink_block(p32_blk, max_height=9.2 * inch, _label='collab_page_32'))
    pages.append(PageBreak())

    p33_blk = []
    p33_blk.append(SectionHeader(8, "KEY BEHAVIORAL DRIVERS: PILLARS 1 & 2"))
    p33_blk.append(HRFlowable(width=CONTENT_W, thickness=1.0, color=GOLD, spaceAfter=12, spaceBefore=4))

    drive_score = float(pb.get('conscientiousness', 0.68) * 0.7 + pb.get('openness', 0.72) * 0.3)
    comp_score = float(pb.get('extraversion', 0.65) * 0.6 + pb.get('conscientiousness', 0.68) * 0.4)

    p33_blk.append(_make_habit_card('I', 'Drive & Inherent Ambition', 'Aspirational Standard & Goal Motivation', drive_score,
                                   'High intrinsic need for achievement. Measures the internal standard of excellence that drives the candidate to pursue mastery.', '#1E3A8A'))
    p33_blk.append(Spacer(1, 12))
    p33_blk.append(_make_habit_card('II', 'Competitive Spirit', 'External Benchmarking & Victory Orientation', comp_score,
                                   'Energized by comparative performance metrics and competitive arenas. Thrives when benchmarked against high-performing cohorts.', '#C46849'))
    p33_blk.append(Spacer(1, 14))
    p33_blk.append(draw_boho_behavioral_ambition(width=CONTENT_W, height=120))
    pages.append(shrink_block(p33_blk, max_height=9.2 * inch, _label='drivers_page_33'))
    pages.append(PageBreak())

    p34_blk = []
    p34_blk.append(SectionHeader(8, "KEY BEHAVIORAL DRIVERS: PILLARS 3 & 4"))
    p34_blk.append(HRFlowable(width=CONTENT_W, thickness=1.0, color=GOLD, spaceAfter=12, spaceBefore=4))

    comp_ctrl = float(pb.get('emotional_stability', 0.64))
    risk_app = float(pb.get('openness', 0.72) * 0.6 + (1.0 - pb.get('emotional_stability', 0.64)) * 0.4)

    p34_blk.append(_make_habit_card('III', 'Composure & Emotional Control', 'Equilibrium under High Pressure', comp_ctrl,
                                   'Ability to maintain rational, deliberate thought processes during crises without succumbing to emotional panic or impulsivity.', '#5A7865'))
    p34_blk.append(Spacer(1, 12))
    p34_blk.append(_make_habit_card('IV', 'Risk Appetite & Innovation', 'Comfort with Strategic Uncertainty', risk_app,
                                   'Willingness to explore novel pathways with uncertain outcomes. Balances calculated downside risk with transformative upside potential.', '#D99B38'))
    p34_blk.append(Spacer(1, 14))
    p34_blk.append(draw_boho_behavioral_equilibrium(width=CONTENT_W, height=120))
    pages.append(shrink_block(p34_blk, max_height=9.2 * inch, _label='drivers_page_34'))

    return pages
