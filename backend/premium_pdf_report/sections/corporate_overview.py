from __future__ import annotations

import os
from typing import Any, Dict

from reportlab.platypus import Paragraph, Spacer, Table, TableStyle, HRFlowable, PageBreak
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.units import inch
from reportlab.lib import colors

from ..theme import (
    STYLES, NAVY, GOLD, GOLD_DARK, GOLD_LIGHT, GOLD_PALE,
    IVORY, WHITE, CONTENT_W, GREY_TEXT,
)
from .helpers import (
    shrink_block, SectionHeader, sub_heading,
    institutional_table, institutional_card,
)
from ..assets.boho_vectors import draw_boho_wax_seal, draw_boho_organization_pillars


def build_page_02_credentials(session: Dict[str, Any]) -> list:
    block: list = []
    block.append(SectionHeader(1, "EXPERT CERTIFICATION & PROFILER CREDENTIALS"))
    block.append(HRFlowable(width=CONTENT_W, thickness=1.0, color=GOLD, spaceAfter=14, spaceBefore=4))

    analyst_name = str(session.get('analyst_name') or 'Prof. Shilp Gohil, Ph.D.').strip()
    analyst_title = str(session.get('analyst_title') or 'Senior Biometric Profiler & Cognitive Development Consultant').strip()
    cred_id = str(session.get('analyst_id') or 'IADP-89241-SR').strip()

    profile_html = (
        f'<font size="14" color="{NAVY.hexval()}" face="Times-Bold"><b>{analyst_name.upper()}</b></font><br/>'
        f'<font size="8.5" color="{GOLD_DARK.hexval()}"><b>{analyst_title}</b></font><br/><br/>'
        '<font size="8.5" color="#2C2C2C">'
        'Certified Dermatoglyphics Multiple Intelligence Analyst with specialized postgraduate qualifications '
        'in Developmental Neuropsychology, Cognitive Assessment, and Biometric Ridge Classification. Accredited by '
        'the International Association of Dermatoglyphics Professionals (IADP) and the Council for Neuro-Behavioral Testing.<br/><br/>'
        'Dedicated to unlocking innate human potential through evidence-based cognitive analysis, ethical pedagogical '
        'counseling, and personalized neuro-developmental roadmaps for academic, corporate, and personal life mastery.'
        '</font>'
    )
    p_profile = Paragraph(profile_html, STYLES['body'])

    seal_html = (
        f'<font size="9.5" color="{GOLD_DARK.hexval()}" face="Times-Bold"><b>ACCREDITATION</b></font><br/><br/>'
        f'<font size="11" color="{NAVY.hexval()}" face="Times-Bold"><b>{cred_id}</b></font><br/>'
        f'<font size="7.5" color="{GOLD_DARK.hexval()}">Board Certification ID</font>'
    )
    p_seal = Paragraph(seal_html, STYLES['body'])
    boho_wax = draw_boho_wax_seal(width=CONTENT_W * 0.28, height=44)

    t_seal = Table([[boho_wax], [p_seal]], colWidths=[CONTENT_W * 0.28])
    t_seal.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), GOLD_PALE),
        ('BOX', (0, 0), (-1, -1), 1.0, GOLD),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ('ROUNDEDCORNERS', [4, 4, 4, 4]),
    ]))

    t_top = Table([[p_profile, t_seal]], colWidths=[CONTENT_W * 0.68, CONTENT_W * 0.32])
    t_top.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (0, 0), 0),
        ('RIGHTPADDING', (0, 0), (0, 0), 22),
        ('LEFTPADDING', (1, 0), (1, 0), 0),
        ('RIGHTPADDING', (1, 0), (1, 0), 0),
        ('TOPPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
    ]))
    block.append(t_top)
    block.append(Spacer(1, 16))

    block.extend(sub_heading("Professional Accreditations & Affiliations"))

    creds_data = [
        [
            Paragraph('<b>Affiliation</b>', STYLES['table_header']),
            Paragraph('<b>Designation / Role</b>', STYLES['table_header']),
            Paragraph('<b>Accreditation Body</b>', STYLES['table_header']),
        ],
        [
            Paragraph('Intl. Dermatoglyphic Research Association', STYLES['table_cell_bold']),
            Paragraph('Chartered Senior Profiler (CSP)', STYLES['table_cell']),
            Paragraph('IADR Global Standards Council', STYLES['table_cell']),
        ],
        [
            Paragraph('Society for Applied Neuropsychology', STYLES['table_cell_bold']),
            Paragraph('Consultant Member', STYLES['table_cell']),
            Paragraph('Division of Cognitive Assessment', STYLES['table_cell']),
        ],
        [
            Paragraph('Board of Certified Career Counselors', STYLES['table_cell_bold']),
            Paragraph('Licensed Vocational Strategist', STYLES['table_cell']),
            Paragraph('National Career Council Accreditation', STYLES['table_cell']),
        ],
    ]
    t_creds = institutional_table(creds_data, col_widths=[CONTENT_W * 0.42, CONTENT_W * 0.28, CONTENT_W * 0.28])
    block.append(t_creds)
    block.append(Spacer(1, 16))

    oath_text = (
        '<b>ANALYST CODE OF ETHICS &amp; PRACTICE OATH:</b><br/>'
        '<i>"I solemnly affirm to uphold the highest standards of scientific integrity, strict confidentiality, '
        'and constructive developmental mentorship. Dermatoglyphics Multiple Intelligence Testing is applied '
        'exclusively as an educational guide to celebrate individuality and optimize self-actualization, '
        'never to limit, label, or define the boundless human spirit."</i>'
    )
    t_oath = institutional_card([Paragraph(oath_text, STYLES['body'])], width=CONTENT_W, border_color=GOLD_LIGHT, bg_color=GOLD_PALE)
    block.append(t_oath)

    return [shrink_block(block, max_height=9.2 * inch, _label='credentials_page_02')]


def build_page_03_organization() -> list:
    block: list = []
    block.append(SectionHeader(1, "ORGANIZATION MISSION & METHODOLOGY"))
    block.append(HRFlowable(width=CONTENT_W, thickness=1.0, color=GOLD, spaceAfter=14, spaceBefore=4))

    intro_p = Paragraph(
        f'<font size="10" color="{NAVY.hexval()}"><b>Empowering Human Potential Through Biometric Precision</b></font><br/>'
        '<font size="8.5" color="#2C2C2C">'
        'Our organization is founded upon the principle that every human brain possesses a unique neural architecture '
        'of innate strengths, cognitive processing rhythms, and creative capacities. By bridging the empirical science '
        'of dermatoglyphics with modern neuropsychological frameworks, we provide individuals, families, and academic '
        'institutions with actionable developmental clarity.</font>',
        STYLES['body']
    )
    block.append(intro_p)
    block.append(Spacer(1, 12))

    pillars = [
        (
            'COGNITIVE ASSESSMENTS',
            'Deep quantitative evaluation of multiple intelligences, brain hemisphere dominance, '
            'and sensory modality preferences (VAK) derived from high-fidelity epidermal ridge analysis.',
        ),
        (
            'ACADEMIC & CAREER MAPPING',
            'Algorithmic cross-matching of neurological capacities against 48 specialized career domains '
            'and 5 academic streams to identify high-flow vocational environments.',
        ),
        (
            'BEHAVIORAL COACHING',
            'Translating Big Five personality dimensions, adversity quotients, and emotional intelligence into '
            'practical habit formation, communication agility, and stress resilience.',
        ),
        (
            'SKILL ACCELERATION MODULES',
            'Targeted neuro-plasticity exercises, bilateral hemisphere bridging drills, and chronobiological '
            'routine architectures to transform latent genetic potential into applied excellence.',
        ),
    ]

    cards_data = []
    for title, desc in pillars:
        content = (
            f'<font size="10" color="{NAVY.hexval()}"><b>{title}</b></font><br/><br/>'
            f'<font size="8" color="#2C2C2C">{desc}</font>'
        )
        p = Paragraph(content, STYLES['body'])
        t_card = Table([[p]], colWidths=[CONTENT_W * 0.47])
        t_card.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), GOLD_PALE),
            ('BOX', (0, 0), (-1, -1), 1.0, GOLD),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
            ('ROUNDEDCORNERS', [4, 4, 4, 4]),
        ]))
        cards_data.append(t_card)

    t_grid = Table(
        [[cards_data[0], cards_data[1]], [cards_data[2], cards_data[3]]],
        colWidths=[CONTENT_W * 0.49, CONTENT_W * 0.49]
    )
    t_grid.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    block.append(t_grid)
    block.append(Spacer(1, 14))

    framework_html = (
        f'<font size="9.5" color="{NAVY.hexval()}" face="Times-Bold"><b>Methodological Standard: The CADA Biometric Invariant</b></font><br/>'
        '<font size="8" color="#2C2C2C">'
        'Our analysis conforms strictly to the Computer-Aided Dermatoglyphic Analysis (CADA) international standard. '
        'Biometric ridge patterns are captured via 500+ DPI optical sensors, preprocessed through five stages of contrast '
        'normalization and Gabor ridge filtering, and classified by automated Poincaré index topological delta/core detection. '
        'Zero synthetic data or arbitrary scores are generated.'
        '</font>'
    )
    t_frame = institutional_card([Paragraph(framework_html, STYLES['body'])], width=CONTENT_W, border_color=GOLD_LIGHT, bg_color=GOLD_PALE)
    block.append(t_frame)
    block.append(Spacer(1, 14))
    block.append(draw_boho_organization_pillars(width=CONTENT_W, height=75))

    return [shrink_block(block, max_height=9.2 * inch, _label='organization_page_03')]


def build_page_04_technology() -> list:
    block: list = []
    block.append(SectionHeader(1, "STRATEGIC TECHNOLOGY INTEGRATION & VALUES"))
    block.append(HRFlowable(width=CONTENT_W, thickness=1.0, color=GOLD, spaceAfter=14, spaceBefore=4))

    block.append(Paragraph(
        f'<font size="10.5" color="{NAVY.hexval()}"><b>4-Stage Automated Computer Vision &amp; Analytics Pipeline</b></font>',
        STYLES['body_left']
    ))
    block.append(Spacer(1, 6))

    step_title_style = ParagraphStyle(
        'FlowStepTitle',
        fontName='Times-Bold',
        fontSize=8.0,
        leading=10.0,
        textColor=NAVY,
        alignment=TA_LEFT,
    )
    step_body_style = ParagraphStyle(
        'FlowStepBody',
        fontName='Times-Roman',
        fontSize=7.2,
        leading=9.2,
        textColor=GREY_TEXT,
        alignment=TA_LEFT,
    )

    flow_steps = [
        ('1. DERMAL SCANNING', '500+ DPI optical acquisition of 10 digits & bilateral palm planar regions.'),
        ('2. PATTERN PROCESSING', 'Gabor filtering, minutiae extraction, Poincaré delta/core topology detection.'),
        ('3. ALGORITHMIC MAPPING', 'Table 1.1 Invariant cerebral lobe weighting, Gardner 9 MI & 10 Quotients.'),
        ('4. PERSONALIZED DOSSIER', 'Synthesis into 60-page executive blueprint with targeted developmental remedies.'),
    ]

    card_w = (CONTENT_W * 0.25) - 4
    step_tables = []
    for stitle, sdesc in flow_steps:
        st = Table(
            [
                [Paragraph(f'<b>{stitle}</b>', step_title_style)],
                [Paragraph(sdesc, step_body_style)],
            ],
            colWidths=[card_w],
            rowHeights=[22, 50],
        )
        st.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), GOLD_PALE),
            ('BOX', (0, 0), (-1, -1), 1.0, GOLD),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, 0), 6),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 2),
            ('TOPPADDING', (0, 1), (-1, 1), 2),
            ('BOTTOMPADDING', (0, 1), (-1, 1), 6),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('ROUNDEDCORNERS', [4, 4, 4, 4]),
        ]))
        step_tables.append(st)

    t_flow = Table([[step_tables[0], step_tables[1], step_tables[2], step_tables[3]]],
                   colWidths=[CONTENT_W * 0.25, CONTENT_W * 0.25, CONTENT_W * 0.25, CONTENT_W * 0.25])
    t_flow.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 2),
        ('RIGHTPADDING', (0, 0), (-1, -1), 2),
        ('TOPPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
    ]))
    block.append(t_flow)
    block.append(Spacer(1, 16))

    block.append(Paragraph(
        f'<font size="10.5" color="{NAVY.hexval()}"><b>Our Four Core Institutional Commitments</b></font>',
        STYLES['body_left']
    ))
    block.append(Spacer(1, 6))

    values = [
        ('SCIENTIFIC INTEGRITY', 'Zero data fabrication. Missing or degraded finger slots are honestly reported as uncollected rather than synthetically estimated. All calculations adhere to research-backed neurological correlations.'),
        ('DATA CONFIDENTIALITY', 'Complete privacy preservation. Raw fingerprint scans are processed in-memory for mathematical feature extraction and purged immediately following dossier generation.'),
        ('OBJECTIVE ANALYSIS', 'Neutral developmental metrics devoid of cultural, gender, or social bias. Results reflect innate biological baselines, providing a grounded foundation for deliberate practice.'),
        ('LIFE-LONG GROWTH', 'Viewing neuro-capacities through the lens of dynamic neuro-plasticity. Biometric indicators highlight natural inclinations while actionable strategies foster lifelong mastery.'),
    ]

    val_rows = []
    for vtitle, vdesc in values:
        v_p = Paragraph(
            f'<font size="9" color="{NAVY.hexval()}"><b>{vtitle}</b></font><br/>'
            f'<font size="8" color="#2C2C2C">{vdesc}</font>',
            STYLES['body']
        )
        val_rows.append([v_p])

    t_vals = Table(val_rows, colWidths=[CONTENT_W])
    t_vals.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), GOLD_PALE),
        ('BOX', (0, 0), (-1, -1), 0.8, GOLD_LIGHT),
        ('LINEBELOW', (0, 0), (-1, -2), 0.5, GOLD_LIGHT),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 7),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 7),
        ('ROUNDEDCORNERS', [4, 4, 4, 4]),
    ]))
    block.append(t_vals)

    return [shrink_block(block, max_height=9.2 * inch, _label='technology_page_04')]


def build_pages_05_06_toc() -> list:
    toc_modules = [
        ('01', 'Candidate Information & Comprehensive Legal Disclaimer', 'Page 07'),
        ('02', 'Science of Dermatoglyphics & Historical Context', 'Page 08'),
        ('03', 'Ridge Formation & Neurological Link', 'Page 09'),
        ('04', 'Literature & Research Foundations', 'Page 10'),
        ('05', 'SWOT Behavioral Profile: Core Strengths (S)', 'Page 11'),
        ('06', 'SWOT Behavioral Profile: Areas for Growth (W)', 'Page 12'),
        ('07', 'SWOT Behavioral Profile: Developmental Opportunities (O)', 'Page 13'),
        ('08', 'SWOT Behavioral Profile: Risk Factors & Threats (T)', 'Page 14'),
        ('09', 'Behavioral Baseline Summary & Personality Radar', 'Page 15'),
        ('10', 'Cerebral Lobe & Ridge Density Distribution (Left & Right)', 'Page 16'),
        ('11', 'Critical Academic Subject Orientations (STEM, Math, Linguistics)', 'Page 17'),
        ('12', 'Comprehensive 10-Quotient Profile: Cognitive & Physical (1–5)', 'Page 18'),
        ('13', 'Comprehensive 10-Quotient Profile: Operational & Strategic (6–10)', 'Page 19'),
        ('14', 'Core Performance Sectors (Academic vs. Physical)', 'Page 20'),
        ('15', 'Recommended Academic Stream Pathways', 'Page 21'),
        ('16', 'Co-Curricular & Talent Mapping (14 Activity Domains)', 'Page 22'),
        ('17', 'Primary Modality Learning Styles: Visual Learning Modality', 'Page 23'),
        ('18', 'Primary Modality Learning Styles: Auditory Learning Modality', 'Page 24'),
        ('19', 'Primary Modality Learning Styles: Kinesthetic Learning Modality', 'Page 25'),
        ('20', 'Efficacy & Self-Management Index (The 7 Habits Framework)', 'Pages 26–29'),
        ('21', 'Operational Leadership Alignment & Cognitive Processing', 'Pages 30–34'),
        ('22', 'Domain-Specific Corporate Competencies (8 Business Domains)', 'Pages 35–42'),
        ('23', 'High-Match Career Pathways (Top 10 & Emerging Tech Careers)', 'Pages 43–44'),
        ('24', 'Specialized Sector Career Compatibility Grids (14 Sectors)', 'Pages 45–58'),
        ('25', 'Counseling Action Plan, Strategy Notes & Mentorship Blueprint', 'Page 59'),
        ('26', 'Participant Acknowledgement, Feedback Scales & Official Sign-off', 'Page 60'),
    ]

    p1_items = toc_modules[:13]
    p2_items = toc_modules[13:]

    def _render_toc_table(items: list, part_title: str) -> list:
        page_block = []
        page_block.append(SectionHeader(1, f"INDEX OF ANALYSIS ({part_title})"))
        page_block.append(HRFlowable(width=CONTENT_W, thickness=1.0, color=GOLD, spaceAfter=14, spaceBefore=4))

        rows = [
            [
                Paragraph('<b>S.No.</b>', STYLES['table_header']),
                Paragraph('<b>Assessment Module &amp; Analytical Dimension</b>', STYLES['table_header']),
                Paragraph('<b>Page Anchor</b>', STYLES['table_header']),
            ]
        ]
        for sno, name, pg in items:
            rows.append([
                Paragraph(f'<b>{sno}</b>', STYLES['table_cell_bold']),
                Paragraph(name, STYLES['table_cell']),
                Paragraph(f'<b>{pg}</b>', STYLES['table_cell_bold']),
            ])

        cw = [CONTENT_W * 0.10, CONTENT_W * 0.72, CONTENT_W * 0.18]
        t = institutional_table(rows, col_widths=cw, center_cols=[0], right_cols=[2])
        page_block.append(t)
        return [shrink_block(page_block, max_height=9.2 * inch, _label=f'toc_{part_title}')]

    return _render_toc_table(p1_items, 'PART I: MODULES 01-13') + [PageBreak()] + _render_toc_table(p2_items, 'PART II: MODULES 14-26')
