"""
Section 2 : Scientific Introduction and Disclaimer
Section 3 : Candidate Profile
"""

from typing import Dict, Any
from reportlab.platypus import Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.units import inch

from ..theme import (STYLES, NAVY, GOLD, GOLD_DARK, GOLD_LIGHT, GOLD_PALE,
                     IVORY, CREAM_ROW, WHITE, GREY_TEXT, CONTENT_W)
from .helpers import section_header, sub_heading, info_card


# ---------------------------------------------------------------------------
# Section 2 : Scientific Introduction and Disclaimer
# ---------------------------------------------------------------------------

DISCLAIMER_TEXT = (
    'This report is an assessment and counselling tool based on Dermatoglyphics '
    'Multiple Intelligence Test (DMIT) methodology. It identifies natural tendencies '
    'and innate potential. Results should be used exclusively for educational and '
    'developmental guidance. Intelligence and success depend on environment, practice, '
    'discipline, and opportunities. Dermatoglyphic ridge patterns are formed between '
    'the 13th and 21st weeks of fetal development and remain unchanged throughout life. '
    'This report does not constitute a medical diagnosis.'
)

DMIT_HISTORY = (
    'Dermatoglyphics is the scientific study of fingerprint ridge patterns and their '
    'relationship to human traits and abilities. The field was pioneered by Jan Evangelista '
    'Purkinje (1823), who first classified fingerprint patterns. Sir Francis Galton further '
    'advanced the science in 1892, establishing the classification system still used today. '
    'Harold Cummins coined the term "dermatoglyphics" in 1926 and established the '
    'brain-finger correlation framework. Wilder Penfield\'s motor cortex mapping (1937) '
    'confirmed that each finger corresponds to specific brain lobe areas. Roger Sperry\'s '
    'split-brain research demonstrated hemispheric specialisation, and Dr. Howard Gardner '
    'introduced Multiple Intelligence Theory in 1983, providing the cognitive framework '
    'that DMIT analysis is built upon.'
)

BRAIN_FINGER_TEXT = (
    'Each finger connects directly to a distinct region of the cerebral cortex through '
    'dedicated neural pathways. The thumbs (L1, R1) are linked to the prefrontal cortex, '
    'governing executive function and leadership. Index fingers (L2, R2) correspond to '
    'the frontal lobe, responsible for logic and analysis. Middle fingers (L3, R3) '
    'connect to the parietal lobe, associated with spatial and sensory processing. '
    'Ring fingers (L4, R4) link to the temporal lobe, governing language and musical '
    'intelligence. Little fingers (L5, R5) connect to the occipital lobe, responsible '
    'for visual processing and creativity. Ridge count and pattern complexity on each '
    'finger reflect the developmental density of corresponding brain regions.'
)

GARDNER_TEXT = (
    'Dr. Howard Gardner\'s Theory of Multiple Intelligences (1983) proposes that human '
    'intelligence is not a single general ability but a collection of distinct cognitive '
    'capacities. Gardner identified nine core intelligences: Linguistic, Logical-Mathematical, '
    'Spatial, Musical, Bodily-Kinesthetic, Interpersonal, Intrapersonal, Naturalistic, '
    'and Existential. DMIT analysis maps fingerprint biometric data to these intelligence '
    'dimensions through validated neuroscientific correlation models, providing an objective '
    'baseline profile of innate cognitive strengths.'
)


def build_intro() -> list:
    story = []
    story += section_header(2, 'Scientific Introduction and Disclaimer')
    story.append(Spacer(1, 6))

    story += sub_heading('Disclaimer')
    story.append(Paragraph(DISCLAIMER_TEXT, STYLES['body']))
    story.append(Spacer(1, 8))

    story += sub_heading('What is Dermatoglyphics?')
    story.append(Paragraph(DMIT_HISTORY, STYLES['intro_body']))
    story.append(Spacer(1, 8))

    story += sub_heading('Brain-Finger Correlation')
    story.append(Paragraph(BRAIN_FINGER_TEXT, STYLES['intro_body']))
    story.append(Spacer(1, 8))

    # Finger-to-lobe mapping table
    story += sub_heading('Finger to Brain Lobe Mapping Reference')
    mapping_rows = [
        [Paragraph('Finger', STYLES['table_header']),
         Paragraph('Slot', STYLES['table_header']),
         Paragraph('Brain Lobe', STYLES['table_header']),
         Paragraph('Primary Function', STYLES['table_header'])],
        ['Thumb', 'R1 / L1', 'Prefrontal Cortex', 'Leadership, Executive Function'],
        ['Index', 'R2 / L2', 'Frontal Lobe', 'Logic, Analysis, Planning'],
        ['Middle', 'R3 / L3', 'Parietal Lobe', 'Spatial, Sensory Processing'],
        ['Ring', 'R4 / L4', 'Temporal Lobe', 'Language, Music, Memory'],
        ['Little', 'R5 / L5', 'Occipital Lobe', 'Visual Processing, Creativity'],
    ]
    for i in range(1, len(mapping_rows)):
        mapping_rows[i] = [Paragraph(str(c), STYLES['table_cell'])
                           for c in mapping_rows[i]]
    col_w = [CONTENT_W * 0.18, CONTENT_W * 0.16, CONTENT_W * 0.28, CONTENT_W * 0.34]
    mt = Table(mapping_rows, colWidths=col_w)
    mt.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), NAVY),
        ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [GOLD_PALE, IVORY]),
        ('FONTNAME', (0, 1), (-1, -1), 'Times-Roman'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 0.4, GOLD_LIGHT),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(mt)
    story.append(Spacer(1, 10))

    story += sub_heading('Howard Gardner\'s Multiple Intelligence Theory')
    story.append(Paragraph(GARDNER_TEXT, STYLES['intro_body']))

    return story


# ---------------------------------------------------------------------------
# Section 3 : Candidate Profile
# ---------------------------------------------------------------------------

def build_candidate_profile(session: Dict[str, Any]) -> list:
    story = []
    story += section_header(3, 'Candidate Profile')
    story.append(Spacer(1, 8))

    from datetime import datetime
    fields = [
        ('Full Name', session.get('subject_name', '')),
        ('Age', str(session.get('subject_age', '')) if session.get('subject_age') else ''),
        ('Gender', session.get('subject_gender', '')),
        ('School / Institution', session.get('school', '')),
        ('Parent / Guardian', session.get('parent_name', '')),
        ('Occupation', session.get('occupation', '')),
        ('Notes', session.get('notes', '')),
        ('Report ID', session.get('report_id', '')),
        ('Test Date', session.get('test_date', datetime.now().strftime('%d %B %Y'))),
        ('Counsellor', session.get('counsellor', '')),
    ]
    rows = []
    for label, value in fields:
        if value:
            rows.append([
                Paragraph(label, STYLES['table_cell_bold']),
                Paragraph(str(value), STYLES['table_cell']),
            ])
    if not rows:
        rows = [[Paragraph('No candidate details provided.', STYLES['body']),
                 Paragraph('', STYLES['body'])]]

    cw = [2.2 * inch, CONTENT_W - 2.4 * inch]
    t = Table(rows, colWidths=cw)
    t.setStyle(TableStyle([
        ('ROWBACKGROUNDS', (0, 0), (-1, -1), [GOLD_PALE, IVORY]),
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('BOX', (0, 0), (-1, -1), 1.5, GOLD),
        ('LINEBELOW', (0, 0), (-1, -2), 0.4, GOLD_LIGHT),
    ]))
    story.append(t)
    story.append(Spacer(1, 10))

    return story
