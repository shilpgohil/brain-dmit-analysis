from __future__ import annotations

from typing import Any, Dict, List, Tuple

from reportlab.platypus import Paragraph, Spacer, Table, TableStyle, HRFlowable, PageBreak
from reportlab.lib.units import inch
from reportlab.lib import colors

from ..theme import (
    STYLES, NAVY, GOLD, GOLD_DARK, GOLD_LIGHT, GOLD_PALE,
    IVORY, WHITE, CONTENT_W,
)
from .helpers import shrink_block, SectionHeader, chart_image, institutional_table, institutional_card
from ..charts import generate_competency_comparison_radar


def build_pages_35_42_corporate_domains(report_data: Dict[str, Any], quotients: Dict[str, float]) -> list:
    pages: list = []
    bm = report_data.get('brain_mapping', {})
    lobe_hemi = bm.get('lobe_hemispheres', {})
    pb = report_data.get('personality_behavior', {})

    lp = float(lobe_hemi.get('left_prefrontal', 0.10)) * 10
    lf = float(lobe_hemi.get('left_frontal', 0.11)) * 10
    lpa = float(lobe_hemi.get('left_parietal', 0.10)) * 10
    lt = float(lobe_hemi.get('left_temporal', 0.10)) * 10
    lo = float(lobe_hemi.get('left_occipital', 0.09)) * 10

    rp = float(lobe_hemi.get('right_prefrontal', 0.11)) * 10
    rf = float(lobe_hemi.get('right_frontal', 0.10)) * 10
    rpa = float(lobe_hemi.get('right_parietal', 0.10)) * 10
    rt = float(lobe_hemi.get('right_temporal', 0.09)) * 10
    ro = float(lobe_hemi.get('right_occipital', 0.09)) * 10

    sq = float(quotients.get('SQ', 0.74))
    cq = float(quotients.get('CQ', 0.70))
    iq = float(quotients.get('IQ', 0.76))
    eq = float(quotients.get('EQ', 0.72))
    aq = float(quotients.get('AQ', 0.68))
    dq = float(quotients.get('DQ', 0.74))

    domains = [
        (
            35,
            'COMMERCIAL SALES CAPABILITIES',
            'Business Development, Client Negotiation & Account Acquisition',
            {'Right Prefrontal (Interpersonal)': rp, 'Left Temporal (Persuasion)': lt, 'Social Quotient (SQ)': sq, 'Goal Drive (Left Prefrontal)': lp},
            {'Right Prefrontal (Interpersonal)': 0.85, 'Left Temporal (Persuasion)': 0.80, 'Social Quotient (SQ)': 0.82, 'Goal Drive (Left Prefrontal)': 0.78},
            'High persuasive fluency, active listening, and commercial resilience. Position in enterprise B2B sales or strategic client partnership management.',
            'Refine objection-handling frameworks, practice consultative discovery questioning, and master CRM pipeline analytics.'
        ),
        (
            36,
            'STRATEGIC MARKETING CAPABILITIES',
            'Brand Architecture, Consumer Insights & Campaign Strategy',
            {'Right Frontal (Creativity)': rf, 'Right Prefrontal (Intuition)': rp, 'Creativity Quotient (CQ)': cq, 'Analytical Reasoning (Left Frontal)': lf},
            {'Right Frontal (Creativity)': 0.85, 'Right Prefrontal (Intuition)': 0.80, 'Creativity Quotient (CQ)': 0.82, 'Analytical Reasoning (Left Frontal)': 0.72},
            'Strong visual conceptualization and narrative empathy. Excels in campaign design, product messaging, and brand positioning.',
            'Deepen attribution modeling skills, master quantitative audience segmentation, and experiment with omnichannel growth hacking.'
        ),
        (
            37,
            'CLIENT SUCCESS & SERVICE DESK',
            'Relationship Retention, Empathic Support & Experience Operations',
            {'Right Prefrontal (Empathy)': rp, 'Left Temporal (Listening)': lt, 'Adaptability Quotient (AQ)': aq, 'Emotional Quotient (EQ)': eq},
            {'Right Prefrontal (Empathy)': 0.88, 'Left Temporal (Listening)': 0.82, 'Adaptability Quotient (AQ)': 0.80, 'Emotional Quotient (EQ)': 0.85},
            'Exceptional relational warmth, patient active listening, and conflict de-escalation skills. High customer lifetime value driver.',
            'Adopt structured customer journey mapping, master ticketing SLAs, and cultivate predictive churn-detection protocols.'
        ),
        (
            38,
            'INFORMATION TECHNOLOGY & SYSTEMS',
            'Software Architecture, Systems Engineering & Data Infrastructure',
            {'Left Frontal (Logic)': lf, 'Right Frontal (Spatial Architecture)': rf, 'Intelligence Quotient (IQ)': iq, 'Left Prefrontal (Systems)': lp},
            {'Left Frontal (Logic)': 0.90, 'Right Frontal (Spatial Architecture)': 0.82, 'Intelligence Quotient (IQ)': 0.85, 'Left Prefrontal (Systems)': 0.80},
            'High algorithmic problem-solving capacity, abstract mathematical reasoning, and structural spatial engineering.',
            'Pursue enterprise cloud certifications, master distributed system paradigms, and practice technical architecture design.'
        ),
        (
            39,
            'LEGAL, GOVERNANCE & COMPLIANCE',
            'Regulatory Risk, Contractual Precision & Corporate Policy',
            {'Left Frontal (Deduction)': lf, 'Left Temporal (Semantics)': lt, 'Decision Quotient (DQ)': dq, 'Left Occipital (Detail Reading)': lo},
            {'Left Frontal (Deduction)': 0.88, 'Left Temporal (Semantics)': 0.85, 'Decision Quotient (DQ)': 0.82, 'Left Occipital (Detail Reading)': 0.85},
            'Meticulous textual precision, rigorous deductive logic, and ethical risk evaluation. Thrives in corporate governance.',
            'Deepen regulatory compliance research, study cross-border dispute resolution, and practice precision statutory interpretation.'
        ),
        (
            40,
            'FINANCIAL ACCOUNTING & AUDIT',
            'Fiscal Control, Quantitative Audit & Risk Modeling',
            {'Left Frontal (Math)': lf, 'Left Occipital (Detail Accuracy)': lo, 'Left Prefrontal (Planning)': lp, 'Intelligence Quotient (IQ)': iq},
            {'Left Frontal (Math)': 0.90, 'Left Occipital (Detail Accuracy)': 0.88, 'Left Prefrontal (Planning)': 0.82, 'Intelligence Quotient (IQ)': 0.82},
            'High numerical precision, error-free auditing capacity, and disciplined financial modeling. Natural fit for controllership.',
            'Expand advanced financial econometrics, master corporate valuation modeling, and study algorithmic risk assessment.'
        ),
        (
            41,
            'OPERATIONS & PRODUCTION MANAGEMENT',
            'Process Engineering, Logistics & Operational Excellence',
            {'Left Prefrontal (Execution)': lp, 'Left Parietal (Process Agility)': lpa, 'Focus Quotient (FQ)': float(quotients.get('FQ', 0.72)), 'Adaptability (AQ)': aq},
            {'Left Prefrontal (Execution)': 0.88, 'Left Parietal (Process Agility)': 0.82, 'Focus Quotient (FQ)': 0.82, 'Adaptability (AQ)': 0.78},
            'High operational stamina, procedural efficiency, and milestone discipline. Excels in supply chain and agile production.',
            'Implement Lean Six Sigma methodologies, design bottleneck mitigation protocols, and master logistics management systems.'
        ),
        (
            42,
            'HUMAN RESOURCE MANAGEMENT',
            'Talent Development, Organizational Culture & People Strategy',
            {'Right Prefrontal (Interpersonal)': rp, 'Left Prefrontal (Organizational)': lp, 'Emotional Quotient (EQ)': eq, 'Social Quotient (SQ)': sq},
            {'Right Prefrontal (Interpersonal)': 0.88, 'Left Prefrontal (Organizational)': 0.80, 'Emotional Quotient (EQ)': 0.85, 'Social Quotient (SQ)': 0.82},
            'Inspirational consensus building, empathetic conflict mediation, and organizational culture stewardship.',
            'Develop workforce analytics frameworks, design performance review cycles, and study strategic talent acquisition.'
        ),
    ]

    for pnum, dname, dsub, cand_map, bench_map, strengths, dev_advice in domains:
        cand_norm = {k: max(0.40, min(0.98, float(v))) for k, v in cand_map.items()}
        bench_norm = {k: float(v) for k, v in bench_map.items()}

        match_score = (sum(cand_norm.values()) / sum(bench_norm.values())) * 100
        match_score = max(55.0, min(96.0, match_score))

        blk = []
        blk.append(SectionHeader(9, f"CORPORATE COMPETENCY: {dname}"))
        blk.append(HRFlowable(width=CONTENT_W, thickness=1.0, color=GOLD, spaceAfter=8, spaceBefore=4))

        head_html = (
            f'<font size="11" color="{NAVY.hexval()}"><b>SUITABILITY MATCH INDEX: {match_score:.1f}%</b></font><br/>'
            f'<font size="8" color="{GOLD_DARK.hexval()}">{dsub}</font>'
        )
        t_head = institutional_card([Paragraph(head_html, STYLES['body'])], width=CONTENT_W, border_color=GOLD, bg_color=GOLD_PALE)
        blk.append(t_head)
        blk.append(Spacer(1, 6))

        r_b64 = generate_competency_comparison_radar(dname, cand_norm, bench_norm)
        r_imgs = chart_image(r_b64, width=CONTENT_W * 0.72)
        if r_imgs:
            blk.extend(r_imgs)
            blk.append(Spacer(1, 6))

        comp_rows = [
            [
                Paragraph('<b>Competency Dimension</b>', STYLES['table_header']),
                Paragraph('<b>Candidate Score</b>', STYLES['table_header']),
                Paragraph('<b>Benchmark Target</b>', STYLES['table_header']),
                Paragraph('<b>Fit Status</b>', STYLES['table_header']),
            ]
        ]
        for k in cand_norm.keys():
            cv = cand_norm[k]
            bv = bench_norm[k]
            status = '<font color="#059669"><b>Aligned</b></font>' if cv >= bv * 0.9 else f'<font color="{GOLD_DARK.hexval()}"><b>Developing</b></font>'
            comp_rows.append([
                Paragraph(k, STYLES['table_cell']),
                Paragraph(f'{cv*100:.0f}%', STYLES['table_cell_bold']),
                Paragraph(f'{bv*100:.0f}%', STYLES['table_cell']),
                Paragraph(status, STYLES['table_cell']),
            ])

        t_comp = institutional_table(
            comp_rows,
            col_widths=[CONTENT_W * 0.44, CONTENT_W * 0.18, CONTENT_W * 0.18, CONTENT_W * 0.20],
            center_cols=[1, 2, 3],
        )
        blk.append(t_comp)
        blk.append(Spacer(1, 6))

        adv_html = (
            f'<font size="8" color="{NAVY.hexval()}"><b>Domain Strengths:</b> {strengths}</font><br/>'
            f'<font size="8" color="{GOLD_DARK.hexval()}"><b>Targeted Skill Development Directive:</b> {dev_advice}</font>'
        )
        t_adv = institutional_card([Paragraph(adv_html, STYLES['body'])], width=CONTENT_W, border_color=GOLD_LIGHT, bg_color=IVORY)
        blk.append(t_adv)

        pages.append(shrink_block(blk, max_height=9.2 * inch, _label=f'corp_page_{pnum}'))
        if pnum < 42:
            pages.append(PageBreak())

    return pages
