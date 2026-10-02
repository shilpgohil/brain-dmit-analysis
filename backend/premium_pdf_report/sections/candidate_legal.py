from __future__ import annotations

from typing import Any, Dict

from reportlab.platypus import Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.units import inch
from reportlab.lib import colors

from ..theme import (
    STYLES, NAVY, GOLD, GOLD_DARK, GOLD_LIGHT, GOLD_PALE,
    IVORY, WHITE, CONTENT_W,
)
from .helpers import shrink_block, SectionHeader, sub_heading, institutional_card


def build_page_07_candidate_legal(report_data: Dict[str, Any], session: Dict[str, Any]) -> list:
    block: list = []
    block.append(SectionHeader(2, "CANDIDATE INFORMATION & COMPREHENSIVE LEGAL DISCLAIMER"))
    block.append(HRFlowable(width=CONTENT_W, thickness=1.0, color=GOLD, spaceAfter=12, spaceBefore=4))

    meta = report_data.get('report_metadata', {})
    name = str(session.get('subject_name') or meta.get('subject_name') or 'Candidate Record').strip()
    age_raw = session.get('subject_age') or meta.get('subject_age') or 0
    try:
        age_int = int(age_raw)
    except Exception:
        age_int = 0

    guardian = str(session.get('guardian_name') or meta.get('guardian_name') or '').strip()
    if not guardian:
        guardian = 'N/A - Self (Adult Candidate)' if age_int >= 18 else 'Registered Legal Guardian'

    dob = str(session.get('subject_dob') or meta.get('subject_dob') or 'Unspecified').strip()
    gender = str(session.get('subject_gender') or meta.get('subject_gender') or 'Unspecified').capitalize().strip()
    phone = str(session.get('contact_phone') or meta.get('contact_phone') or '+91 • Confidential').strip()
    email = str(session.get('contact_email') or meta.get('contact_email') or 'confidential@client.portal').strip()
    test_date = str(meta.get('test_date') or 'Verified Assessment').strip()
    client_id = str(meta.get('report_id') or 'RA-2026-CONFIDENTIAL').strip()

    bio_cells = [
        [
            Paragraph(f'<font size="7.5" color="{GOLD_DARK.hexval()}">FULL CANDIDATE NAME</font><br/><b><font size="9.5" color="{NAVY.hexval()}">{name.upper()}</font></b>', STYLES['body']),
            Paragraph(f'<font size="7.5" color="{GOLD_DARK.hexval()}">GUARDIAN / PARENT NAME</font><br/><b><font size="9" color="{NAVY.hexval()}">{guardian}</font></b>', STYLES['body']),
        ],
        [
            Paragraph(f'<font size="7.5" color="{GOLD_DARK.hexval()}">DATE OF BIRTH / GENDER</font><br/><b><font size="9" color="{NAVY.hexval()}">{dob} • {gender}</font></b>', STYLES['body']),
            Paragraph(f'<font size="7.5" color="{GOLD_DARK.hexval()}">CONTACT NUMBER</font><br/><b><font size="9" color="{NAVY.hexval()}">{phone}</font></b>', STYLES['body']),
        ],
        [
            Paragraph(f'<font size="7.5" color="{GOLD_DARK.hexval()}">CANDIDATE / GUARDIAN EMAIL</font><br/><b><font size="9" color="{NAVY.hexval()}">{email}</font></b>', STYLES['body']),
            Paragraph(f'<font size="7.5" color="{GOLD_DARK.hexval()}">ASSESSMENT DATE &amp; REF ID</font><br/><b><font size="9" color="{GOLD_DARK.hexval()}">{test_date} • {client_id}</font></b>', STYLES['body']),
        ]
    ]

    t_bio = Table(bio_cells, colWidths=[CONTENT_W * 0.50, CONTENT_W * 0.50])
    t_bio.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), GOLD_PALE),
        ('BOX', (0, 0), (-1, -1), 1.0, GOLD),
        ('GRID', (0, 0), (-1, -1), 0.4, GOLD_LIGHT),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('ROUNDEDCORNERS', [4, 4, 4, 4]),
    ]))
    block.append(t_bio)
    block.append(Spacer(1, 10))

    block.extend(sub_heading("Comprehensive Terms of Use & Legal Framework"))

    clauses = [
        ('1. DATA OWNERSHIP & VOLUNTARY CONSENT',
         'The biometric data collected herein belongs exclusively to the evaluated candidate (or their appointed legal guardian if a minor). By participating in this assessment, the candidate or legal guardian confirms that the acquisition of epidermal ridge patterns was conducted voluntarily, transparently, and with informed authorization.'),
        ('2. BIOMETRIC PRIVACY & AUTOMATIC DATA ERASURE INVARIANT',
         'High-resolution epidermal ridge images captured during the intake process are processed strictly in volatile memory for mathematical feature extraction, minutiae mapping, and report synthesis. In strict accordance with international biometric privacy standards, all scanned image files are automatically purged from local and remote servers immediately following report compilation. Zero biometric image signatures are stored, retained, or distributed in any repository.'),
        ('3. OBSERVATIONAL NATURE OF THE ASSESSMENT',
         'This report constitutes an observational developmental analysis derived from established empirical correlations between epidermal ridge configurations (dermatoglyphs) and human cerebral neocortex lobe distributions. It serves exclusively as a self-awareness reference, pedagogical guide, and developmental blueprint. It does not constitute, and shall never be construed as, a clinical psychiatric evaluation, medical diagnostic tool, or genetic test.'),
        ('4. LIMITATION OF LIABILITY & INDICATIVE SCOPE',
         'Recommendations regarding academic streams, career trajectories, learning modalities, or behavioral tendencies are indicative and probabilistic in nature. Human potential is dynamically shaped by environment, deliberate effort, emotional resilience, and formal education. Neither the issuing organization, its affiliates, certified analysts, nor technology partners shall bear legal or financial liability for personal, educational, or professional decisions made based on this dossier.'),
        ('5. INDEPENDENT PROFESSIONAL CONSULTATION MANDATE',
         'Prior to executing significant academic track shifts, corporate career pivots, psychological interventions, or medical choices, candidates and guardians are strongly advised to consult qualified educational counselors, registered psychologists, or certified medical practitioners. This report is designed to complement, never supersede, professional human expertise.'),
    ]

    clause_rows = []
    for ctitle, cdesc in clauses:
        c_p = Paragraph(
            f'<font size="8" color="{NAVY.hexval()}"><b>{ctitle}</b></font><br/>'
            f'<font size="7.5" color="#2C2C2C">{cdesc}</font>',
            STYLES['body']
        )
        clause_rows.append([c_p])

    t_clauses = Table(clause_rows, colWidths=[CONTENT_W])
    t_clauses.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), GOLD_PALE),
        ('BOX', (0, 0), (-1, -1), 0.8, GOLD_LIGHT),
        ('LINEBELOW', (0, 0), (-1, -2), 0.4, GOLD_LIGHT),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('ROUNDEDCORNERS', [4, 4, 4, 4]),
    ]))
    block.append(t_clauses)
    block.append(Spacer(1, 8))

    ack_text = (
        '<b>CANDIDATE / GUARDIAN ELECTRONIC ACKNOWLEDGEMENT:</b> By reviewing this document, the recipient acknowledges receipt of the '
        'comprehensive legal disclaimer and agrees to its non-clinical developmental terms of use.'
    )
    p_ack = Paragraph(f'<font size="7" color="{NAVY.hexval()}">{ack_text}</font>', STYLES['body'])
    block.append(institutional_card([p_ack], width=CONTENT_W, border_color=GOLD_LIGHT, bg_color=GOLD_PALE))

    return [shrink_block(block, max_height=9.2 * inch, _label='candidate_legal_page_07')]
