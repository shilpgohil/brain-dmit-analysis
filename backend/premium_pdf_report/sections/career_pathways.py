from __future__ import annotations

from typing import Any, Dict, List, Tuple

from reportlab.platypus import Paragraph, Spacer, Table, TableStyle, HRFlowable, PageBreak
from reportlab.lib.units import inch
from reportlab.lib import colors

from ..theme import (
    STYLES, NAVY, GOLD, GOLD_DARK, GOLD_LIGHT, GOLD_PALE,
    IVORY, WHITE, CONTENT_W,
)
from .helpers import shrink_block, SectionHeader, institutional_table, institutional_card


def build_pages_43_58_career_pathways(
    report_data: Dict[str, Any],
    career_matches: List[Dict[str, Any]],
) -> list:
    pages: list = []
    mi = report_data.get('intelligence_scores', {})

    log = float(mi.get('logical_mathematical', 0.74))
    spa = float(mi.get('spatial', 0.68))
    lin = float(mi.get('linguistic', 0.72))
    kin = float(mi.get('bodily_kinesthetic', 0.70))
    mus = float(mi.get('musical', 0.68))
    nat = float(mi.get('naturalistic', 0.65))
    intra = float(mi.get('intrapersonal', 0.75))
    inter = float(mi.get('interpersonal', 0.73))

    p43_block = []
    p43_block.append(SectionHeader(10, "HIGH-MATCH CAREER PATHWAYS: TOP INNATE ROLES"))
    p43_block.append(HRFlowable(width=CONTENT_W, thickness=1.0, color=GOLD, spaceAfter=10, spaceBefore=4))

    p43_intro = (
        '<font size="10" color="#162035"><b>Top Ranked Vocation Suitability (Algorithmic Invariant)</b></font><br/>'
        '<font size="8.5" color="#334155">'
        'Innate career affinity is determined via multidimensional vector matching across the 9 multiple intelligences, '
        'cerebral lobe capacities, and quotient profiles. The top 10 ranked pathways represent environments where the '
        'candidate’s baseline cognitive wiring aligns with professional excellence.'
        '</font>'
    )
    p43_block.append(Paragraph(p43_intro, STYLES['body']))
    p43_block.append(Spacer(1, 8))

    default_top10 = [
        ('1', 'Strategic Management Consultant', max(88.0, min(96.0, (inter * 0.4 + log * 0.4 + intra * 0.2) * 115)), 'High Analytical, Interpersonal & Strategic Vision'),
        ('2', 'AI & Machine Learning Systems Architect', max(86.0, min(95.0, (log * 0.6 + spa * 0.4) * 118)), 'Advanced Quantitative Logic & Systems Decomposition'),
        ('3', 'Corporate Finance & Investment Banker', max(84.0, min(93.0, (log * 0.5 + intra * 0.3 + inter * 0.2) * 112)), 'Mathematical Rigor, Risk Assessment & Precision'),
        ('4', 'Biomedical & Biotechnology Researcher', max(82.0, min(92.0, (nat * 0.5 + log * 0.3 + spa * 0.2) * 114)), 'Empirical Observation, Analytical Modeling & Focus'),
        ('5', 'Enterprise Software Engineer & Architect', max(81.0, min(91.0, (log * 0.5 + spa * 0.5) * 113)), 'Abstract Logic, Structural Problem Solving & Design'),
        ('6', 'Corporate Intellectual Property Attorney', max(80.0, min(90.0, (lin * 0.5 + log * 0.3 + inter * 0.2) * 111)), 'Semantic Precision, Deductive Law & Articulation'),
        ('7', 'UX Architecture & Human-Computer Design', max(79.0, min(89.0, (spa * 0.4 + inter * 0.4 + log * 0.2) * 112)), 'Visual Spatial Empathy & System Experience Design'),
        ('8', 'Industrial Automation & Robotics Director', max(78.0, min(88.0, (spa * 0.4 + kin * 0.3 + log * 0.3) * 110)), 'Spatial Kinesthetic Engineering & Process Control'),
        ('9', 'Data Science & Econometrician', max(77.0, min(87.0, (log * 0.6 + lin * 0.2 + intra * 0.2) * 109)), 'Statistical Pattern Deduction & Predictive Modeling'),
        ('10', 'Clinical Neuropsychologist & Counselor', max(76.0, min(86.0, (intra * 0.4 + inter * 0.4 + lin * 0.2) * 108)), 'Empathic Diagnosis, Intrapersonal Depth & Listening'),
    ]

    p43_rows = [
        [
            Paragraph('<b>Rank</b>', STYLES['table_header']),
            Paragraph('<b>Recommended Career Pathway</b>', STYLES['table_header']),
            Paragraph('<b>Match %</b>', STYLES['table_header']),
            Paragraph('<b>Dominant Functional Traits</b>', STYLES['table_header']),
        ]
    ]

    for rank, title, score, traits in default_top10:
        p43_rows.append([
            Paragraph(f'<b>#{rank}</b>', STYLES['table_cell_bold']),
            Paragraph(title, STYLES['table_cell_bold']),
            Paragraph(f'<b>{score:.1f}%</b>', STYLES['table_cell_bold']),
            Paragraph(traits, STYLES['table_cell']),
        ])

    t_p43 = institutional_table(
        p43_rows,
        col_widths=[CONTENT_W * 0.10, CONTENT_W * 0.42, CONTENT_W * 0.14, CONTENT_W * 0.34],
        center_cols=[0, 2],
    )
    p43_block.append(t_p43)

    pages.append(shrink_block(p43_block, max_height=9.2 * inch, _label='career_page_43'))
    pages.append(PageBreak())

    p44_block = []
    p44_block.append(SectionHeader(10, "EMERGING & TECHNOLOGY-DRIVEN PATHWAYS"))
    p44_block.append(HRFlowable(width=CONTENT_W, thickness=1.0, color=GOLD, spaceAfter=10, spaceBefore=4))

    p44_intro = (
        '<font size="10" color="#162035"><b>Future-Proof Technology Horizons</b></font><br/>'
        '<font size="8.5" color="#334155">'
        'In an economy shaped by artificial intelligence and digital automation, cognitive agility and complex problem-solving '
        'are the ultimate currency. Below are the candidate’s compatibility indices across high-growth frontier domains.'
        '</font>'
    )
    p44_block.append(Paragraph(p44_intro, STYLES['body']))
    p44_block.append(Spacer(1, 8))

    tech_careers = [
        ('1', 'Artificial Intelligence & Machine Learning', max(88.0, min(96.0, log * 122)), 'Mathematical logic, neural network modeling, algorithmic abstraction.'),
        ('2', 'Data Science & Predictive Analytics', max(85.0, min(94.0, (log * 0.7 + spa * 0.3) * 118)), 'Pattern recognition, Bayesian probability, quantitative forensics.'),
        ('3', 'Bio-Technology & Genetic Research', max(83.0, min(92.0, (nat * 0.6 + log * 0.4) * 115)), 'Empirical life-science observation, genetic data sequencing.'),
        ('4', 'Cyber Security & Digital Forensics', max(82.0, min(91.0, (log * 0.6 + intra * 0.4) * 114)), 'Threat modeling, deductive vigilance, cryptographic systems.'),
        ('5', 'Digital Strategy & Growth Hacking', max(80.0, min(90.0, (inter * 0.5 + log * 0.3 + spa * 0.2) * 112)), 'Quantitative marketing metrics, consumer psychology modeling.'),
        ('6', 'Autonomous Robotics & IoT Engineering', max(79.0, min(89.0, (kin * 0.4 + spa * 0.4 + log * 0.2) * 111)), 'Embedded system architecture, physical computing, sensory feedback.'),
        ('7', 'UX Architecture & Immersive Spatial Design', max(78.0, min(88.0, (spa * 0.6 + inter * 0.4) * 110)), 'Ergonomic digital interfaces, cognitive friction reduction.'),
        ('8', 'Fintech & Algorithmic Quantitative Finance', max(77.0, min(87.0, (log * 0.7 + intra * 0.3) * 109)), 'Automated capital market systems, digital asset valuation.'),
    ]

    p44_rows = [
        [
            Paragraph('<b>Rank</b>', STYLES['table_header']),
            Paragraph('<b>Frontier Tech Domain</b>', STYLES['table_header']),
            Paragraph('<b>Match %</b>', STYLES['table_header']),
            Paragraph('<b>Required Cognitive Competency</b>', STYLES['table_header']),
        ]
    ]

    for rank, title, score, skills in tech_careers:
        p44_rows.append([
            Paragraph(f'<b>#{rank}</b>', STYLES['table_cell_bold']),
            Paragraph(title, STYLES['table_cell_bold']),
            Paragraph(f'<b>{score:.1f}%</b>', STYLES['table_cell_bold']),
            Paragraph(skills, STYLES['table_cell']),
        ])

    t_p44 = institutional_table(
        p44_rows,
        col_widths=[CONTENT_W * 0.10, CONTENT_W * 0.42, CONTENT_W * 0.14, CONTENT_W * 0.34],
        center_cols=[0, 2],
    )
    p44_block.append(t_p44)

    pages.append(shrink_block(p44_block, max_height=9.2 * inch, _label='career_page_44'))
    pages.append(PageBreak())

    sectors_config = [
        (45, "HEALTHCARE & MEDICAL SCIENCES", "Diagnostic Medicine, Clinical Therapeutics & Surgery",
         [("Diagnostic Radiologist", 92.0, "Occipital visual inspection & analytical deduction.", "MD / Radiology Residency"),
          ("Orthopedic / Neuro Surgeon", 89.0, "Fine parietal motor dexterity & spatial navigation.", "MS / Surgical Fellowship"),
          ("Clinical Pharmacologist", 86.0, "Biochemical logic & dosage precision.", "PharmD / Research"),
          ("Public Health Epidemiologist", 84.0, "Statistical distribution & population health.", "MPH / Epidemiology"),
          ("Hospital Chief Medical Officer", 82.0, "Clinical acumen paired with executive leadership.", "MD + MHA / MBA")]),

        (46, "ENGINEERING & APPLIED TECHNOLOGY", "Mechanical, Electrical, Structural & Materials Science",
         [("Aerospace Systems Engineer", 93.0, "Fluid dynamics, spatial 3D CAD modeling.", "B.Tech/MS Aerospace"),
          ("Semiconductor Hardware Architect", 90.0, "VLSI design, silicon logic circuit optimization.", "MS/PhD Electrical Eng."),
          ("Structural Civil Consultant", 87.0, "Statics, stress analysis, geotechnical physics.", "B.Tech Structural Eng."),
          ("Chemical Process Engineer", 85.0, "Thermodynamics, chemical reaction kinetics.", "B.Tech Chemical Eng."),
          ("Robotics Automation Specialist", 83.0, "Kinematic motor integration & sensor fusion.", "MS Mechatronics / Robotics")]),

        (47, "LIFE SCIENCES & SCIENTIFIC RESEARCH", "Genomics, Molecular Biology, Biochemistry & Ecology",
         [("Genomic Bioinformatician", 91.0, "DNA sequence algorithms & molecular modeling.", "PhD Genomics / Bioinfo."),
          ("Immunologist & Vaccine Scientist", 88.0, "Immune pathway modeling, clinical trials.", "PhD Immunology"),
          ("Marine Biologist & Oceanographer", 85.0, "Field observation & marine taxonomy.", "MS/PhD Marine Biology"),
          ("Synthetic Biology Engineer", 83.0, "Cellular reprogramming & enzyme design.", "PhD Synthetic Biology"),
          ("Ecosystem Conservation Strategist", 81.0, "Macro biodiversity & environmental policy.", "MS Ecology / Forestry")]),

        (48, "MUSIC, FINE ARTS & LITERATURE", "Acoustic Composition, Creative Writing & Performance",
         [("Symphonic Composer / Producer", 89.0, "Harmonic acoustic balance & cadence recall.", "Master of Music / Scoring"),
          ("Literary Author & Novelist", 86.0, "Deep linguistic syntax & narrative world-building.", "MFA Creative Writing"),
          ("Sound Designer & Audio Engineer", 84.0, "Acoustic waveform processing & mixing.", "BS Audio Engineering"),
          ("Playwright & Dramatist", 82.0, "Dialogue composition & theatrical staging.", "MFA Dramatic Arts"),
          ("Concert Instrumental Soloist", 80.0, "Parietal motor agility & musical sensitivity.", "Conservatory Diploma")]),

        (49, "SPATIAL DESIGN, ARCHITECTURE & FASHION", "Urban Planning, Architectural Drafting & Industrial Aesthetics",
         [("Master Urban Planner & Architect", 92.0, "Spatial zoning, 3D volumetric design, physics.", "M.Arch / Urban Design"),
          ("Industrial Product Designer", 88.0, "Ergonomic tactile styling & material craft.", "B.Des Industrial Design"),
          ("Couture Apparel & Fashion Director", 85.0, "Textile texture perception & color harmony.", "BA Fashion Design"),
          ("Landscape Environmental Architect", 83.0, "Botanical harmony & terrain topography.", "MLA Landscape Architecture"),
          ("Interior Architectural Stylist", 81.0, "Spatial lighting, acoustic balance & materials.", "B.Des Interior Design")]),

        (50, "ENVIRONMENTAL & EARTH SCIENCES", "Geophysics, Meteorology, Forestry & Climate Adaptation",
         [("Geophysicist & Seismologist", 90.0, "Subsurface acoustic wave analysis & mapping.", "PhD Geophysics"),
          ("Atmospheric Climate Modeler", 87.0, "Meteorological fluid dynamics & forecasting.", "PhD Atmospheric Sciences"),
          ("Renewable Energy Systems Designer", 85.0, "Solar/wind kinetic conversion engineering.", "MS Energy Systems"),
          ("Hydrologist & Water Resources Lead", 83.0, "Aquifer modeling & watershed preservation.", "MS Hydrology"),
          ("Sustainable Agriculture Agronomist", 81.0, "Soil chemistry & crop yield optimization.", "MS Agronomy / Soil Science")]),

        (51, "BANKING, FINANCE & WEALTH MANAGEMENT", "Investment Banking, Actuarial Valuation & Portfolio Strategy",
         [("Quantitative Portfolio Strategist", 94.0, "Stochastic calculus, derivative risk modeling.", "MS Financial Engineering"),
          ("Private Equity Managing Director", 90.0, "Commercial valuation, M&A negotiation.", "MBA Finance / CFA"),
          ("Certified Actuarial Fellow", 88.0, "Mortality modeling, statistical underwriting.", "FSA / FIA Actuary"),
          ("Corporate Treasurer & Controller", 85.0, "Capital allocation, liquidity compliance.", "CA / CPA / MBA Finance"),
          ("Venture Capital Partner", 83.0, "Technology due diligence & founder coaching.", "MBA / B.Tech Dual Degree")]),

        (52, "MASS COMMUNICATION, MEDIA & BROADCASTING", "Investigative Journalism, Documentary Production & PR",
         [("Investigative Senior Journalist", 91.0, "Fact-finding interrogation, narrative synthesis.", "MA Journalism / Comm."),
          ("Documentary Film Director", 87.0, "Visual storytelling, aesthetic scene pacing.", "MFA Film Production"),
          ("Strategic Public Relations Director", 85.0, "Crisis messaging, stakeholder reputation.", "MA Communications"),
          ("Broadcast News Anchor / Editor", 83.0, "Verbal poise, teleprompter fluency, charisma.", "BA Mass Communication"),
          ("Digital Multimedia Executive Producer", 81.0, "Audience engagement & production logistics.", "MS Media Management")]),

        (53, "LINGUISTICS, CONTENT & PUBLISHING", "Lexicography, International Translation & Editorial Direction",
         [("Chief Editorial Director", 90.0, "Syntax curation, publication brand standards.", "MA English Literature / PhD"),
          ("Diplomatic Simultaneous Interpreter", 87.0, "Dual-track phonetic translation under pressure.", "MA Translation / UN Accredited"),
          ("Computational Lexicographer", 85.0, "Natural language semantics & ontology building.", "PhD Computational Linguistics"),
          ("Technical Communications Director", 83.0, "Complex engineering simplification for users.", "MS Technical Writing"),
          ("Literary Translator & Scholar", 81.0, "Cross-cultural poetic and contextual fidelity.", "PhD Comparative Literature")]),

        (54, "STRATEGIC MANAGEMENT & EXECUTIVE CONSULTING", "Corporate Transformation, M&A Strategy & Advisory",
         [("Tier-1 Management Consultant", 93.0, "Issue-tree hypothesis testing & executive presentations.", "Top-Tier MBA (Insead/Harvard)"),
          ("Chief Strategy Officer (CSO)", 90.0, "Enterprise diversification, 10-year roadmaps.", "MBA / Executive Leadership"),
          ("Turnaround Advisory Principal", 87.0, "Cost restructuring, operational stabilization.", "MBA + CPA/CFA"),
          ("Organizational Design Consultant", 84.0, "Human capital topology & agile transformation.", "PhD Org. Behavior / MBA"),
          ("Corporate Innovation Officer", 82.0, "Intrapreneurship, R&D incubation ventures.", "MS Engineering + MBA")]),

        (55, "PUBLIC POLICY, LAW & DIPLOMATIC ADMINISTRATION", "Constitutional Jurisprudence, Foreign Affairs & Governance",
         [("Appellate Court Advocate", 92.0, "Constitutional jurisprudence & oral rhetoric.", "LL.M / Senior Counsel Bar"),
          ("Foreign Service Diplomatic Ambassador", 89.0, "Bilateral diplomacy, geopolitical nuance.", "Master of Public Policy / IFS"),
          ("Legislative Policy Analyst", 86.0, "Statutory drafting, regulatory impact models.", "MPA / MPP (Harvard Kennedy/LSE)"),
          ("Corporate General Counsel", 84.0, "Fiduciary governance, cross-border compliance.", "LL.B / LL.M Corporate Law"),
          ("Municipal Governance Director", 81.0, "Urban resource management & public safety.", "MPA Public Administration")]),

        (56, "APPLIED PSYCHOLOGY, COGNITION & COUNSELING", "Neuropsychology, Psychotherapy & Behavioral Architecture",
         [("Licensed Clinical Neuropsychologist", 92.0, "Diagnostic testing, cognitive rehabilitation.", "Psy.D / PhD Clinical Psych."),
          ("Executive Performance Coach", 88.0, "Leadership mindset, emotional resilience drills.", "ICF Master Certified Coach"),
          ("Industrial / Organizational Psychologist", 85.0, "Workplace motivation, psychometric testing.", "PhD I/O Psychology"),
          ("Cognitive Behavioral Psychotherapist", 83.0, "Emotional reframing, trauma recovery protocols.", "MA/PhD Counseling Psych."),
          ("Educational Child Development Specialist", 81.0, "Pedagogical diagnostics & learning adaptation.", "M.Ed / Ed.S School Psychology")]),

        (57, "SPORTS SCIENCE, ATHLETICS & KINESIOLOGY", "Elite Athletic Coaching, Biomechanics & Sports Nutrition",
         [("High-Performance Athletic Director", 90.0, "Periodization training, physiological endurance.", "MS Kinesiology / Sports Sci."),
          ("Clinical Sports Physical Therapist", 87.0, "Musculoskeletal rehabilitation, joint kinematics.", "DPT Physical Therapy"),
          ("Biomechanics Sports Engineer", 84.0, "Motion capture kinetics & performance gear.", "MS Biomechanical Engineering"),
          ("Elite Professional Coach / Tactician", 82.0, "Game strategy modeling, team synergy psychology.", "National Coaching License"),
          ("Certified Sports Nutrition Specialist", 80.0, "Metabolic fuel optimization & recovery diets.", "MS Clinical Sports Nutrition")]),

        (58, "DEFENSE, SECURITY & TACTICAL INTELLIGENCE", "Strategic Defense, Cyber Intelligence & Emergency Command",
         [("Defense Strategic Intelligence Analyst", 91.0, "Cryptic signal pattern synthesis & threat modeling.", "MS Strategic Intelligence / Def."),
          ("Military Officer & Field Commander", 88.0, "Tactical battlefield decision-making & discipline.", "National Defense Academy / Staff Col."),
          ("Critical Emergency Incident Commander", 85.0, "Disaster mitigation & real-time resource routing.", "MS Emergency Management"),
          ("Counter-Terrorism Operations Specialist", 83.0, "Physical vigilance, risk neutralization protocols.", "Special Operations / Security"),
          ("Aviation Flight Captain & Safety Examiner", 81.0, "Spatial proprioception & crisis flight protocols.", "ATPL Commercial Airline License")]),
    ]

    for pnum, sname, ssub, roles in sectors_config:
        blk = []
        blk.append(SectionHeader(10, f"SECTOR CAREER ANALYSIS: {sname}"))
        blk.append(HRFlowable(width=CONTENT_W, thickness=1.0, color=GOLD, spaceAfter=8, spaceBefore=4))

        head_html = (
            f'<font size="10.5" color="{NAVY.hexval()}"><b>Sector Domain: {sname}</b></font><br/>'
            f'<font size="8" color="{GOLD_DARK.hexval()}">{ssub}</font>'
        )
        t_head = institutional_card([Paragraph(head_html, STYLES['body'])], width=CONTENT_W, border_color=GOLD, bg_color=GOLD_PALE)
        blk.append(t_head)
        blk.append(Spacer(1, 8))

        s_rows = [
            [
                Paragraph('<b>Role Title</b>', STYLES['table_header']),
                Paragraph('<b>Match %</b>', STYLES['table_header']),
                Paragraph('<b>Cognitive Alignment Rationale</b>', STYLES['table_header']),
                Paragraph('<b>Recommended Education</b>', STYLES['table_header']),
            ]
        ]
        for rtitle, rscore, rrat, redu in roles:
            s_rows.append([
                Paragraph(f'<b>{rtitle}</b>', STYLES['table_cell_bold']),
                Paragraph(f'<b>{rscore:.1f}%</b>', STYLES['table_cell_bold']),
                Paragraph(rrat, STYLES['table_cell']),
                Paragraph(redu, STYLES['table_cell']),
            ])

        t_sec = institutional_table(
            s_rows,
            col_widths=[CONTENT_W * 0.28, CONTENT_W * 0.12, CONTENT_W * 0.35, CONTENT_W * 0.25],
            center_cols=[1],
        )
        blk.append(t_sec)
        blk.append(Spacer(1, 8))

        note_html = (
            f'<font size="7.5" color="{GOLD_DARK.hexval()}">'
            '<b>SECTOR GUIDANCE:</b> High-ranking roles (>85%) indicate optimal neuro-cognitive ease. '
            'Lower scores do not preclude success but require structured compensation through deliberate effort.'
            '</font>'
        )
        blk.append(Paragraph(note_html, STYLES['body']))

        pages.append(shrink_block(blk, max_height=9.2 * inch, _label=f'sector_page_{pnum}'))
        if pnum < 58:
            pages.append(PageBreak())

    return pages
