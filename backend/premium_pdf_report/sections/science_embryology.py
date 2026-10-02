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
    shrink_block, SectionHeader, sub_heading,
    institutional_table, institutional_card,
)
from ..assets.boho_vectors import draw_boho_embryo_seedling


def build_pages_08_10_science() -> list:
    pages: list = []

    p8_block = []
    p8_block.append(SectionHeader(3, "FOUNDATIONS & HISTORICAL SCIENCE OF DERMATOGLYPHICS"))
    p8_block.append(HRFlowable(width=CONTENT_W, thickness=1.0, color=GOLD, spaceAfter=12, spaceBefore=4))

    block_intro = (
        'Derived from the ancient Greek words <i>derma</i> (skin) and <i>glyph</i> (carving), Dermatoglyphics is the '
        'formal scientific study of the epidermal ridge patterns formed on the palmar and plantar surfaces of the human body. '
        'Unlike transient physical features, epidermal ridge formations are immutable from birth until post-mortem decomposition, '
        'providing an invariant biological baseline of developmental synaptogenesis.'
    )
    p8_block.extend(sub_heading("The Scientific Discipline of Dermatoglyphics"))
    p8_block.append(Paragraph(block_intro, STYLES['body']))
    p8_block.append(Spacer(1, 8))

    timeline_milestones = [
        ('1823: JAN EVANGELISTA PURKINJE', 'Czech anatomist and physiologist who published the first systematic scientific classification of fingerprint ridge patterns, identifying nine fundamental configurations.'),
        ('1892: SIR FRANCIS GALTON', 'British polymath who established the mathematical uniqueness and permanence of fingerprints, proving the probability of two identical patterns is less than 1 in 64 billion.'),
        ('1926: DR. HAROLD CUMMINS & CHARLES MIDLO', 'Regarded as the fathers of modern dermatoglyphics, Cummins and Midlo demonstrated that epidermal ridge patterns develop simultaneously with the cerebral neocortex from the embryonic ectoderm.'),
        ('MODERN: COMPUTER-AIDED DERMAL ANALYSIS (CADA)', 'Integration of high-definition 500+ DPI optical sensors, Poincaré topological index delta/core detection, and validated algorithmic multiple intelligence mapping.'),
    ]

    t_cards = []
    for mtitle, mdesc in timeline_milestones:
        m_p = Paragraph(
            f'<font size="8.5" color="{NAVY.hexval()}"><b>{mtitle}</b></font><br/>'
            f'<font size="8" color="#2C2C2C">{mdesc}</font>',
            STYLES['body']
        )
        tc = Table([[m_p]], colWidths=[CONTENT_W])
        tc.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), GOLD_PALE),
            ('BOX', (0, 0), (-1, -1), 0.8, GOLD),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('ROUNDEDCORNERS', [4, 4, 4, 4]),
        ]))
        t_cards.append(tc)

    for tc in t_cards:
        p8_block.append(tc)
        p8_block.append(Spacer(1, 5))

    gest_text = (
        f'<b><font color="{NAVY.hexval()}">Embryological Development Invariant (13th to 21st Gestational Weeks):</font></b> '
        'Human epidermal ridges begin differentiation during the 13th week of intrauterine gestation, mirroring the rapid '
        'cellular proliferation and furrowing of the human cerebral neocortex. Both organ systems originate from the exact same '
        'embryonic germ layer—the <b>ectoderm</b>. By the 21st week, volar pad formations regress and primary ridge paths are '
        'permanently locked in place, reflecting genetic and epigenetic developmental influences.'
    )
    t_gest = institutional_card([Paragraph(gest_text, STYLES['body'])], width=CONTENT_W, border_color=GOLD_LIGHT, bg_color=GOLD_PALE)
    p8_block.append(t_gest)
    p8_block.append(Spacer(1, 8))
    p8_block.append(draw_boho_embryo_seedling(width=CONTENT_W, height=50))

    pages.append(shrink_block(p8_block, max_height=9.2 * inch, _label='science_page_08'))
    pages.append(PageBreak())

    p9_block = []
    p9_block.append(SectionHeader(3, "RIDGE-NEURAL LINK & TABLE 1.1 INVARIANT"))
    p9_block.append(HRFlowable(width=CONTENT_W, thickness=1.0, color=GOLD, spaceAfter=12, spaceBefore=4))

    p9_intro = (
        'Due to the decussation of neurological tracts in the brainstem, contralateral wiring maps the right hand '
        'primarily to the left cerebral hemisphere (operational execution, sequential logic) and the left hand to the '
        'right cerebral hemisphere (holistic conceptualization, visionary intuition). Table 1.1 defines the strict '
        'correlation between individual finger slots and specific human cerebral lobes.'
    )
    p9_block.extend(sub_heading("Neurological Pathway: The 10 Digits to 5 Cerebral Lobes"))
    p9_block.append(Paragraph(p9_intro, STYLES['body']))
    p9_block.append(Spacer(1, 6))

    t11_rows = [
        [
            Paragraph('<b>Digit Slot</b>', STYLES['table_header']),
            Paragraph('<b>Target Cerebral Lobe</b>', STYLES['table_header']),
            Paragraph('<b>Primary Cognitive Domain</b>', STYLES['table_header']),
            Paragraph('<b>Weighting Rule</b>', STYLES['table_header']),
        ],
        [
            Paragraph('Thumb (L1 / R1)', STYLES['table_cell_bold']),
            Paragraph('Prefrontal Lobe', STYLES['table_cell']),
            Paragraph('Executive Command, Planning, Inter/Intrapersonal MI', STYLES['table_cell']),
            Paragraph('Primary: 1.0 (Direct)', STYLES['table_cell']),
        ],
        [
            Paragraph('Index (L2 / R2)', STYLES['table_cell_bold']),
            Paragraph('Posterior Frontal Lobe', STYLES['table_cell']),
            Paragraph('Logical-Mathematical Deduction, Spatial Conception', STYLES['table_cell']),
            Paragraph('Primary: 1.0 (Direct)', STYLES['table_cell']),
        ],
        [
            Paragraph('Middle (L3 / R3)', STYLES['table_cell_bold']),
            Paragraph('Parietal Lobe', STYLES['table_cell']),
            Paragraph('Bodily-Kinesthetic Agility, Fine/Gross Motor Control', STYLES['table_cell']),
            Paragraph('Primary: 1.0 (Direct)', STYLES['table_cell']),
        ],
        [
            Paragraph('Ring (L4 / R4)', STYLES['table_cell_bold']),
            Paragraph('Temporal Lobe', STYLES['table_cell']),
            Paragraph('Linguistic Memory, Auditory Processing, Music', STYLES['table_cell']),
            Paragraph('Primary: 1.0 (Direct)', STYLES['table_cell']),
        ],
        [
            Paragraph('Little (L5 / R5)', STYLES['table_cell_bold']),
            Paragraph('Occipital Lobe', STYLES['table_cell']),
            Paragraph('Visual Identification, Reading, Spatial Observation', STYLES['table_cell']),
            Paragraph('Primary: 1.0 (Direct)', STYLES['table_cell']),
        ],
    ]
    t_t11 = institutional_table(t11_rows, col_widths=[CONTENT_W * 0.22, CONTENT_W * 0.26, CONTENT_W * 0.34, CONTENT_W * 0.18])
    p9_block.append(t_t11)
    p9_block.append(Spacer(1, 8))

    p9_block.extend(sub_heading("The 3 Principal CADA Ridge Pattern Families"))

    cada_families = [
        ('WHORL PATTERNS (W)', 'Concentric circles, spirals, and composite configurations. Possesses 2 deltas and 1 core. Associated with independent cognitive drive, high focus, and goal persistence.'),
        ('LOOP PATTERNS (L)', 'Flowing ridge lines entering and exiting on the same side. Possesses 1 delta and 1 core. Associated with adaptive social learning, observational modeling, and collaborative empathy.'),
        ('ARCH PATTERNS (A)', 'Wave-like ridges flowing from side to side without recurving. Possesses 0 deltas and 0 cores. Associated with grounded pragmatic execution, methodical absorption, and foundational stability.'),
    ]
    cada_rows = []
    for ftitle, fdesc in cada_families:
        cp = Paragraph(
            f'<font size="8.5" color="{NAVY.hexval()}"><b>{ftitle}</b></font><br/>'
            f'<font size="7.5" color="#2C2C2C">{fdesc}</font>',
            STYLES['body']
        )
        cada_rows.append([cp])

    t_cada = Table(cada_rows, colWidths=[CONTENT_W])
    t_cada.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), GOLD_PALE),
        ('BOX', (0, 0), (-1, -1), 0.8, GOLD_LIGHT),
        ('LINEBELOW', (0, 0), (-1, -2), 0.4, GOLD_LIGHT),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('ROUNDEDCORNERS', [4, 4, 4, 4]),
    ]))
    p9_block.append(t_cada)

    pages.append(shrink_block(p9_block, max_height=9.2 * inch, _label='science_page_09'))
    pages.append(PageBreak())

    p10_block = []
    p10_block.append(SectionHeader(3, "LITERATURE FOUNDATIONS & RESEARCH REFERENCES"))
    p10_block.append(HRFlowable(width=CONTENT_W, thickness=1.0, color=GOLD, spaceAfter=12, spaceBefore=4))

    p10_intro = (
        'The algorithmic scoring models within this dossier are synthesized from over a century of peer-reviewed '
        'dermatoglyphic, genetic, and neuro-anatomical publications across accredited medical and psychological journals.'
    )
    p10_block.extend(sub_heading("Academic Citations & Neuropsychological Frameworks"))
    p10_block.append(Paragraph(p10_intro, STYLES['body']))
    p10_block.append(Spacer(1, 8))

    citations = [
        ('1. Cummins, H., & Midlo, C. (1943)', 'Finger Prints, Palms and Soles: An Introduction to Dermatoglyphics. Blakiston Co., Philadelphia.', 'Established foundational anatomical taxonomy and statistical distributions of human palmar and plantar ridges.'),
        ('2. Penrose, L. S., & Loesch, D. (1970)', 'Topological Classification of Diversity of Dermatoglyphic Patterns. Journal of Medical Genetics, 7(2), 111-121.', 'Introduced topological graph invariants and quantitative core-delta coordinate mathematics for minutiae mapping.'),
        ('3. Babler, W. J. (1991)', 'Embryologic Development of Epidermal Ridges and Their Association with Normal and Abnormal Development. Birth Defects Original Article Series, 27(2), 67-86.', 'Demonstrated strict synchronization between ectodermal ridgeogenesis and neuro-cortical proliferation during weeks 13–21.'),
        ('4. Gardner, H. (1983)', 'Frames of Mind: The Theory of Multiple Intelligences. Basic Books, New York.', 'Dismantled singular IQ metric, establishing the 9 autonomous cognitive faculties mapped in this report.'),
        ('5. Schaumann, B., & Alter, M. (1976)', 'Dermatoglyphics in Medical Disorders. Springer-Verlag, New York.', 'Comprehensive clinical synthesis correlating volar ridge patterns with chromosomal and neurological baselines.'),
        ('6. Goleman, D. (1995)', 'Emotional Intelligence: Why It Can Matter More Than IQ. Bantam Books, New York.', 'Theoretical foundation for the 4-quadrant emotional intelligence and interpersonal competency scoring layer.'),
    ]

    cite_rows = []
    for author, pub, annot in citations:
        cp = Paragraph(
            f'<font size="8.5" color="{NAVY.hexval()}"><b>{author}</b></font> &mdash; '
            f'<font size="8" color="{GOLD_DARK.hexval()}"><i>{pub}</i></font><br/>'
            f'<font size="7.5" color="#2C2C2C">{annot}</font>',
            STYLES['body']
        )
        cite_rows.append([cp])

    t_cites = Table(cite_rows, colWidths=[CONTENT_W])
    t_cites.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), GOLD_PALE),
        ('BOX', (0, 0), (-1, -1), 0.8, GOLD_LIGHT),
        ('LINEBELOW', (0, 0), (-1, -2), 0.4, GOLD_LIGHT),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 6.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6.5),
        ('ROUNDEDCORNERS', [4, 4, 4, 4]),
    ]))
    p10_block.append(t_cites)

    pages.append(shrink_block(p10_block, max_height=9.2 * inch, _label='science_page_10'))
    return pages
