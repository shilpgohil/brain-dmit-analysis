from __future__ import annotations

from typing import Any, Dict

from reportlab.platypus import Paragraph, Spacer, Table, TableStyle, HRFlowable, PageBreak
from reportlab.lib.units import inch
from reportlab.lib import colors

from ..theme import (
    STYLES, NAVY, GOLD, GOLD_DARK, GOLD_LIGHT, GOLD_PALE,
    IVORY, WHITE, CONTENT_W,
)
from .helpers import (
    shrink_block, SectionHeader, sub_heading, chart_image,
    institutional_table, institutional_card,
)
from ..charts import create_personality_radar
from ..assets.boho_vectors import draw_boho_swot_badge


def _build_quadrant_page(
    sec_num: int,
    sec_title: str,
    q_num: int,
    q_subtitle: str,
    letter: str,
    impact_pct: float,
    overview_text: str,
    mechanism_text: str,
    indicators: list[tuple[str, str, str]],
    directives: list[str],
    label_tag: str,
) -> list:
    block: list = []
    block.append(SectionHeader(sec_num, sec_title))
    block.append(HRFlowable(width=CONTENT_W, thickness=1.0, color=GOLD, spaceAfter=8, spaceBefore=4))

    block.extend(sub_heading(f"Quadrant {q_num}: {q_subtitle}"))
    block.append(Paragraph(overview_text, STYLES['body']))
    block.append(Spacer(1, 6))

    badge_art = draw_boho_swot_badge(letter, width=CONTENT_W * 0.20, height=48)
    left_badge = [
        badge_art,
        Paragraph(f'<font size="13" color="{NAVY.hexval()}"><b>{letter}</b></font> &bull; '
                  f'<font size="10" color="{GOLD_DARK.hexval()}"><b>{round(impact_pct * 100)}%</b></font><br/>'
                  f'<font size="6.5" color="{NAVY.hexval()}">IMPACT INDEX</font>', STYLES['body']),
    ]
    right_desc = [
        Paragraph(f'<b><font size="9.5" color="{NAVY.hexval()}">Executive Neuro-Cognitive Synthesis</font></b>', STYLES['body']),
        Spacer(1, 3),
        Paragraph(f'<font size="8" color="{NAVY.hexval()}">{mechanism_text}</font>', STYLES['body']),
    ]
    t_plaque = Table(
        [[Table([[c] for c in left_badge], colWidths=[CONTENT_W * 0.20]),
          Table([[c] for c in right_desc], colWidths=[CONTENT_W * 0.76])]],
        colWidths=[CONTENT_W * 0.22, CONTENT_W * 0.78]
    )
    t_plaque.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), GOLD_PALE),
        ('BOX', (0, 0), (-1, -1), 1.0, GOLD),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('ROUNDEDCORNERS', [4, 4, 4, 4]),
    ]))
    block.append(t_plaque)
    block.append(Spacer(1, 8))

    block.extend(sub_heading("Core Behavioral Manifestations & Observed Indicators"))

    rows = [
        [
            Paragraph('<b>Indicator Dimension</b>', STYLES['table_header']),
            Paragraph('<b>Behavioral Manifestation &amp; Operational Impact</b>', STYLES['table_header']),
            Paragraph('<b>Impact Tier</b>', STYLES['table_header']),
        ]
    ]
    for dim, desc, tier in indicators:
        rows.append([
            Paragraph(f'<b>{dim}</b>', STYLES['table_cell_bold']),
            Paragraph(desc, STYLES['table_cell']),
            Paragraph(f'<b>{tier}</b>', STYLES['table_cell_bold']),
        ])

    cw = [CONTENT_W * 0.26, CONTENT_W * 0.58, CONTENT_W * 0.16]
    t_ind = institutional_table(rows, col_widths=cw, center_cols=[2])
    block.append(t_ind)
    block.append(Spacer(1, 8))

    dir_flowables = [
        Paragraph(f'<b><font size="8.5" color="{NAVY.hexval()}">Tactical Action &amp; Optimization Directives</font></b>', STYLES['body']),
        Spacer(1, 4),
    ]
    for d in directives:
        dir_flowables.append(Paragraph(f'<font size="8" color="{NAVY.hexval()}">• {d}</font>', STYLES['body']))

    card_dir = institutional_card(dir_flowables, width=CONTENT_W, border_color=GOLD_DARK, bg_color=GOLD_PALE)
    block.append(card_dir)

    return [shrink_block(block, max_height=9.2 * inch, _label=label_tag)]


def build_pages_11_15_swot(report_data: Dict[str, Any]) -> list:
    pb = report_data.get('personality_behavior', {})
    openness = float(pb.get('openness', 0.72))
    consc = float(pb.get('conscientiousness', 0.68))
    extra = float(pb.get('extraversion', 0.65))
    agree = float(pb.get('agreeableness', 0.70))
    emot_stab = float(pb.get('emotional_stability', 0.64))

    score_s = max(0.50, min(0.95, (consc * 0.4 + openness * 0.3 + extra * 0.3)))
    score_w = max(0.20, min(0.65, (1.0 - consc) * 0.5 + (1.0 - emot_stab) * 0.5))
    score_o = max(0.50, min(0.95, (openness * 0.5 + extra * 0.5)))
    score_t = max(0.15, min(0.60, (1.0 - emot_stab) * 0.6 + (1.0 - agree) * 0.4))

    pages: list = []

    s_indicators = [
        ('Goal Persistence', 'Natural focus on closing open loops, maintaining multi-stage project milestones, and delivering definitive completion.', 'Primary Strength'),
        ('Cognitive Synthesis', 'Rapidly harmonizes disparate data inputs into structured operational blueprints with minimal processing delay.', 'High Fluency'),
        ('Intrinsic Drive', 'High self-starter motivation threshold; maintains sustained momentum without continuous external supervision.', 'Autonomous'),
        ('Composure under Load', 'Retains pragmatic judgment and structural composure during multi-variable crisis situations.', 'Resilient'),
    ]
    s_directives = [
        'Place candidate in high-ownership leadership tracks where independent strategic execution and accountability are rewarded.',
        'Pair rigorous intellectual execution stamina with formal delegation checklists to maximize systemic organizational leverage.',
        'Institutionalize quarterly stretch assignments to continuously challenge higher-order problem-solving faculties.',
    ]
    p11 = _build_quadrant_page(
        4, "SWOT BEHAVIORAL PROFILE: CORE STRENGTHS (S)",
        1, "Inherent Cognitive & Execution Assets", "S", score_s,
        'Innate strengths represent hardwired neuro-cognitive advantages where the candidate operates with natural fluency, '
        'requiring minimal metabolic friction to achieve high-performance outcomes.',
        'High synaptic transmission efficiency across the prefrontal and posterior frontal lobes generates spontaneous clarity '
        'in complex task decomposition and autonomous execution.',
        s_indicators, s_directives, 'swot_page_11'
    )
    pages.extend(p11)
    pages.append(PageBreak())

    w_indicators = [
        ('Pacing Impatience', 'Occasional frustration when collaborative peers or team members require extended conceptual onboarding.', 'Monitoring Area'),
        ('Delegation Friction', 'Inclination to self-execute detailed deliverables due to strict perfectionist standards rather than delegating.', 'Development Target'),
        ('Cognitive Over-Focus', 'Vulnerability to over-investing metabolic energy into secondary micro-details during prolonged sprints.', 'Restoration Need'),
        ('Direct Rhetoric', 'Tendency to communicate factual conclusions with unvarnished candor, requiring situational diplomacy calibration.', 'Communication Focus'),
    ]
    w_directives = [
        'Implement intentional 24-hour buffer windows before reacting to collaborative delays or operational bottlenecks.',
        'Adopt the 80/20 delegation matrix: assign execution ownership while preserving executive review milestones.',
        'Establish compulsory sensory recovery intervals following intense cognitive focus blocks to prevent fatigue.',
    ]
    p12 = _build_quadrant_page(
        4, "SWOT BEHAVIORAL PROFILE: AREAS FOR GROWTH (W)",
        2, "Developmental Vulnerabilities & Calibration Points", "W", score_w,
        'Weaknesses are not absolute deficiencies, but areas of relative neurological expenditure where high cognitive strain '
        'or behavioral friction may emerge if unmonitored.',
        'Heightened task accountability combined with intense analytical focus can induce operational rigidity if adaptive '
        'emotional buffers are not consciously cultivated.',
        w_indicators, w_directives, 'swot_page_12'
    )
    pages.extend(p12)
    pages.append(PageBreak())

    o_indicators = [
        ('Interdisciplinary Bridge', 'Unique capacity to link technical logic with creative strategy across emerging technological sectors.', 'High Horizon'),
        ('Strategic Mentorship', 'Transitioning personal technical mastery into scalable mentoring models for junior teams and cohorts.', 'Leadership Horizon'),
        ('Global Academic Tracks', 'Leveraging bilingual and spatial faculties to pursue specialized international credentials and publications.', 'Academic Horizon'),
        ('Enterprise Innovation', 'Commercializing analytical insights into viable institutional products and high-value workflows.', 'Commercial Horizon'),
    ]
    o_directives = [
        'Spearhead at least one cross-departmental initiative annually to practice multi-stakeholder consensus building.',
        'Form a strategic peer mastermind network to exchange frontier methodologies and test organizational hypotheses.',
        'Formalize specialized domain thought-leadership via structured executive presentations and whitepaper authoring.',
    ]
    p13 = _build_quadrant_page(
        4, "SWOT BEHAVIORAL PROFILE: DEVELOPMENTAL OPPORTUNITIES (O)",
        3, "High-Leverage Growth Horizons & Expansion", "O", score_o,
        'Opportunities identify external environments, academic intersections, and collaborative roles where the candidate’s '
        'unique profile can generate exponential developmental returns.',
        'The candidate’s balanced brain lobe profile positions them exceptionally well for frontier disciplines bridging '
        'empirical systems engineering and human-centric design.',
        o_indicators, o_directives, 'swot_page_13'
    )
    pages.extend(p13)
    pages.append(PageBreak())

    t_indicators = [
        ('Cognitive Burnout', 'Prolonged exposure to unstructured, high-friction tasks without adequate rest cycles creates exhaustion risks.', 'Systemic Threat'),
        ('Bureaucratic Stagnation', 'Hierarchical or low-velocity operational environments severely diminish motivation and creative output.', 'Environmental Threat'),
        ('Interpersonal Dissonance', 'Misinterpretation of objective candor by sensitive stakeholders during high-pressure deadlines.', 'Relational Threat'),
        ('Decision Over-Extension', 'Depleting finite executive willpower reserves by micro-evaluating trivial operational details.', 'Capacity Threat'),
    ]
    t_directives = [
        'Enforce protected 60-minute daily focus bubbles shielded from communication interruptions and ad-hoc task switching.',
        'Deploy the Eisenhower Decision Matrix to ruthlessly eliminate or automate trivial administrative tasks.',
        'Pre-brief collaborative teams on candidate’s objective communication style to maintain relational alignment.',
    ]
    p14 = _build_quadrant_page(
        4, "SWOT BEHAVIORAL PROFILE: RISK FACTORS & THREATS (T)",
        4, "Environmental Stressors & Boundary Preservation", "T", score_t,
        'Threats delineate external operational pressures or environmental misalignments that could deplete the candidate’s '
        'resilience reserves and precipitate burnout.',
        'High conscientiousness without explicit boundary architecture frequently invites involuntary task accumulation, '
        'demanding proactive protective strategies.',
        t_indicators, t_directives, 'swot_page_14'
    )
    pages.extend(p14)
    pages.append(PageBreak())

    p15_block = []
    p15_block.append(SectionHeader(4, "BEHAVIORAL BASELINE SUMMARY & PERSONALITY RADAR"))
    p15_block.append(HRFlowable(width=CONTENT_W, thickness=1.0, color=GOLD, spaceAfter=8, spaceBefore=4))

    radar_b64 = create_personality_radar(pb)
    r_imgs = chart_image(radar_b64, width=CONTENT_W * 0.70, caption="Big Five Personality & Behavioral Radar")
    if r_imgs:
        p15_block.extend(r_imgs)
        p15_block.append(Spacer(1, 6))

    baseline_rows = [
        [
            Paragraph('<b>Dimension</b>', STYLES['table_header']),
            Paragraph('<b>Innate Score</b>', STYLES['table_header']),
            Paragraph('<b>Behavioral Manifestation</b>', STYLES['table_header']),
            Paragraph('<b>Operational Recommendation</b>', STYLES['table_header']),
        ],
        [
            Paragraph('Openness', STYLES['table_cell_bold']),
            Paragraph(f'<b>{openness*100:.1f}%</b>', STYLES['table_cell_bold']),
            Paragraph('Intellectual curiosity; high receptive capacity for novel methodologies.', STYLES['table_cell']),
            Paragraph('Engage in exploratory problem solving and cross-disciplinary innovation.', STYLES['table_cell']),
        ],
        [
            Paragraph('Conscientiousness', STYLES['table_cell_bold']),
            Paragraph(f'<b>{consc*100:.1f}%</b>', STYLES['table_cell_bold']),
            Paragraph('High structural discipline; meticulous attention to execution milestones.', STYLES['table_cell']),
            Paragraph('Assign milestone ownership and complex logistical architecture tasks.', STYLES['table_cell']),
        ],
        [
            Paragraph('Extraversion', STYLES['table_cell_bold']),
            Paragraph(f'<b>{extra*100:.1f}%</b>', STYLES['table_cell_bold']),
            Paragraph('Balanced ambivert fluency; self-directed with selective group charisma.', STYLES['table_cell']),
            Paragraph('Blend solitary deep-work blocks with targeted collaborative presentations.', STYLES['table_cell']),
        ],
        [
            Paragraph('Agreeableness', STYLES['table_cell_bold']),
            Paragraph(f'<b>{agree*100:.1f}%</b>', STYLES['table_cell_bold']),
            Paragraph('Objective, equitable fairness; values integrity over superficial rapport.', STYLES['table_cell']),
            Paragraph('Leverage in negotiation and objective conflict resolution scenarios.', STYLES['table_cell']),
        ],
        [
            Paragraph('Emotional Stability', STYLES['table_cell_bold']),
            Paragraph(f'<b>{emot_stab*100:.1f}%</b>', STYLES['table_cell_bold']),
            Paragraph('Measured emotional baseline; analytical equilibrium under volatility.', STYLES['table_cell']),
            Paragraph('Place in mission-critical decision nodes during uncertain operational cycles.', STYLES['table_cell']),
        ],
    ]

    cw15 = [CONTENT_W * 0.22, CONTENT_W * 0.14, CONTENT_W * 0.32, CONTENT_W * 0.32]
    t_base = institutional_table(baseline_rows, colWidths=cw15, center_cols=[1])
    p15_block.append(t_base)

    pages.append(shrink_block(p15_block, max_height=9.2 * inch, _label='swot_page_15'))
    return pages
