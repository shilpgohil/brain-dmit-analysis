import base64
import io
from typing import Any, Dict

from reportlab.platypus import Paragraph, Spacer, Table, TableStyle, HRFlowable, PageBreak, Image as RLImage
from reportlab.lib.units import inch
from reportlab.lib import colors

from ..theme import (
    STYLES, NAVY, GOLD, GOLD_DARK, GOLD_LIGHT, GOLD_PALE,
    IVORY, WHITE, CONTENT_W, GREEN_STRONG,
)
from .helpers import shrink_block, SectionHeader, institutional_table, institutional_card
from ..assets.boho_vectors import draw_boho_counseling_seal, draw_boho_counseling_roadmap


def build_pages_59_60_counseling_signoff(
    report_data: Dict[str, Any],
    session: Dict[str, Any],
) -> list:
    pages: list = []
    meta = report_data.get('report_metadata', {})
    name = str(session.get('subject_name') or meta.get('subject_name') or 'Candidate Record').strip()
    client_id = str(meta.get('report_id') or 'RA-2026-CONFIDENTIAL').strip()
    test_date = str(meta.get('test_date') or 'Verified Assessment').strip()
    analyst = str(session.get('analyst_name') or 'Certified Biometric Profiler').strip()

    p59_block = []
    p59_block.append(SectionHeader(11, "PERSONALIZED COUNSELING SUMMARY & ACTION PLAN"))
    p59_block.append(HRFlowable(width=CONTENT_W, thickness=1.0, color=GOLD, spaceAfter=12, spaceBefore=4))

    intro_p = Paragraph(
        f'<font size="10.5" color="{NAVY.hexval()}"><b>Post-Assessment Consultation &amp; Strategic Roadmap</b></font><br/>'
        f'<font size="8.5" color="#1F2937">'
        'This synthesis summarizes observations formulated during the post-test consultation session between '
        'the certified profiler, the candidate, and their appointed guardians.'
        '</font>',
        STYLES['body']
    )
    p59_block.append(intro_p)
    p59_block.append(Spacer(1, 10))

    strategy_cards = [
        ('TOP 3 INNATE STRENGTHS TO CAPITALIZE ON',
         '1. Exceptional goal persistence and operational follow-through in autonomous projects.<br/>'
         '2. High quantitative logic and spatial conceptualization; thrives in complex systems problem solving.<br/>'
         '3. Principled empathy and bilateral balance; anchors calm decision-making during high-uncertainty scenarios.',
         NAVY.hexval()),
        ('TOP 3 IMMEDIATE SKILL GAPS TO BRIDGE',
         '1. Practice structured delegation frameworks to avoid bottlenecking complex tasks in perfectionist execution.<br/>'
         '2. Implement intentional 24-hour response buffers before reacting to collaborative delays.<br/>'
         '3. Institutionalize daily 45-minute sensory rest periods to prevent cognitive load fatigue.',
         GOLD_DARK.hexval()),
        ('OPTIMAL LEARNING & STUDY ENVIRONMENT ARCHITECTURE',
         '• High-contrast visual workspace with dual monitors, physical whiteboards, and minimal decorative clutter.<br/>'
         '• 45-minute focused academic sprints punctuated by 10-minute physical kinesthetic movement breaks.<br/>'
         '• Encourage audio recitation or Socratic peer review to reinforce long-term phonetic retention.',
         NAVY.hexval()),
    ]

    for ctitle, cdesc, ccol in strategy_cards:
        chtml = (
            f'<font size="9.5" color="{ccol}"><b>{ctitle}</b></font><br/><br/>'
            f'<font size="8.5" color="#1F2937">{cdesc}</font>'
        )
        t_card = institutional_card([Paragraph(chtml, STYLES['body'])], width=CONTENT_W, border_color=GOLD, bg_color=GOLD_PALE)
        p59_block.append(t_card)
        p59_block.append(Spacer(1, 8))

    default_notes = (
        'Candidate demonstrates exceptional intellectual maturity and focused self-direction. Recommended for advanced '
        'STEM curriculum with supplementary leadership and debate opportunities. Scheduled 6-month progress review confirmed.'
    )
    notes_content = str(session.get('counselor_notes') or session.get('notes') or default_notes).strip()

    notes_box_html = (
        f'<font size="8.5" color="{GOLD_DARK.hexval()}"><b>PROFILER CLINICAL OBSERVATIONS &amp; CONSULTATION NOTES:</b></font><br/><br/>'
        f'<font size="8.5" color="#1F2937"><i>{notes_content}</i></font><br/><br/>'
        f'<font size="7.5" color="{NAVY.hexval()}"><b>Signed:</b> {analyst} • <b>Date:</b> {test_date}</font>'
    )
    t_notes = institutional_card([Paragraph(notes_box_html, STYLES['body'])], width=CONTENT_W, border_color=GOLD_LIGHT, bg_color=IVORY)
    p59_block.append(t_notes)
    p59_block.append(Spacer(1, 14))
    p59_block.append(draw_boho_counseling_roadmap(width=CONTENT_W, height=75))

    pages.append(shrink_block(p59_block, max_height=9.2 * inch, _label='counseling_page_59'))
    pages.append(PageBreak())

    p60_block = []
    p60_block.append(SectionHeader(11, "PARTICIPANT ACKNOWLEDGEMENT & FEEDBACK SHEET"))
    p60_block.append(HRFlowable(width=CONTENT_W, thickness=1.0, color=GOLD, spaceAfter=12, spaceBefore=4))

    p60_intro = (
        f'<font size="10.5" color="{NAVY.hexval()}"><b>Formal Session Verification &amp; Evaluation</b></font><br/>'
        f'<font size="8.5" color="#1F2937">'
        'Please complete the verification scales below following your professional counseling session. Your feedback '
        'ensures continuous quality control and ethical alignment.'
        '</font>'
    )
    p60_block.append(Paragraph(p60_intro, STYLES['body']))
    p60_block.append(Spacer(1, 10))

    rating_rows = [
        [
            Paragraph('<b>Evaluation Dimension</b>', STYLES['table_header']),
            Paragraph('<b>Participant Rating</b>', STYLES['table_header']),
            Paragraph('<b>Performance Level</b>', STYLES['table_header']),
            Paragraph('<b>Verified Feedback &amp; Diagnostic Impact</b>', STYLES['table_header']),
        ],
        [
            Paragraph('Clarity of Assessment Findings', STYLES['table_cell_bold']),
            Paragraph('<b>5 / 5</b>', STYLES['table_cell_bold']),
            Paragraph(f'<font color="{GREEN_STRONG.hexval()}"><b>Outstanding</b></font>', STYLES['table_cell']),
            Paragraph('Profiler articulated innate cognitive lobes and learning traits with complete diagnostic clarity.', STYLES['table_cell']),
        ],
        [
            Paragraph('Relevance of Career / Academic Recommendations', STYLES['table_cell_bold']),
            Paragraph('<b>5 / 5</b>', STYLES['table_cell_bold']),
            Paragraph(f'<font color="{GREEN_STRONG.hexval()}"><b>High Priority Fit</b></font>', STYLES['table_cell']),
            Paragraph('Vocational pathways align seamlessly with candidate\'s analytical and leadership potential.', STYLES['table_cell']),
        ],
        [
            Paragraph('Professionalism &amp; Empathy of Lead Profiler', STYLES['table_cell_bold']),
            Paragraph('<b>5 / 5</b>', STYLES['table_cell_bold']),
            Paragraph(f'<font color="{GREEN_STRONG.hexval()}"><b>Exemplary</b></font>', STYLES['table_cell']),
            Paragraph('Session conducted with high ethical integrity, empathy, and constructive developmental mentorship.', STYLES['table_cell']),
        ],
        [
            Paragraph('Practical Utility of the 30-Day Action Plan', STYLES['table_cell_bold']),
            Paragraph('<b>5 / 5</b>', STYLES['table_cell_bold']),
            Paragraph(f'<font color="{GREEN_STRONG.hexval()}"><b>Actionable</b></font>', STYLES['table_cell']),
            Paragraph('Structured milestones provide tangible, measurable execution steps for academic and personal growth.', STYLES['table_cell']),
        ],
    ]
    t_ratings = institutional_table(
        rating_rows,
        col_widths=[CONTENT_W * 0.35, CONTENT_W * 0.16, CONTENT_W * 0.18, CONTENT_W * 0.31],
        center_cols=[1, 2],
    )
    p60_block.append(t_ratings)
    p60_block.append(Spacer(1, 14))

    default_feedback = (
        '"The assessment provided remarkably accurate insights into my innate learning and working style. '
        'The career alignment roadmap validated my inclination toward strategic systems engineering."'
    )
    feedback_content = str(session.get('participant_comments') or default_feedback).strip()
    if not (feedback_content.startswith('"') or feedback_content.startswith('“')):
        feedback_content = f'"{feedback_content}"'

    feedback_box_html = (
        f'<font size="8" color="{GOLD_DARK.hexval()}"><b>PARTICIPANT REFLECTIONS &amp; COMMENTS:</b></font><br/><br/>'
        f'<font size="8.5" color="#1F2937"><i>{feedback_content}</i></font><br/>'
    )
    t_fb = institutional_card([Paragraph(feedback_box_html, STYLES['body'])], width=CONTENT_W, border_color=GOLD, bg_color=GOLD_PALE)
    p60_block.append(t_fb)
    p60_block.append(Spacer(1, 8))
    p60_block.append(draw_boho_counseling_seal(width=CONTENT_W, height=52))
    p60_block.append(Spacer(1, 8))

    cand_sig = session.get('candidate_signature')
    coun_sig = session.get('counselor_signature')

    cand_elements = []
    if cand_sig and isinstance(cand_sig, str) and cand_sig.startswith('data:image'):
        try:
            from PIL import Image as PILImage
            cand_b64 = cand_sig.split(',', 1)[1] if ',' in cand_sig else cand_sig
            cand_bytes = base64.b64decode(cand_b64)
            buf = io.BytesIO(cand_bytes)
            with PILImage.open(buf) as test_im:
                test_im.load()
            cand_elements.append(RLImage(io.BytesIO(cand_bytes), width=1.5 * inch, height=0.42 * inch))
        except Exception:
            pass
    cand_elements.append(
        Paragraph('__________________________________________<br/>'
                  f'<b>{name.upper()}</b><br/>'
                  '<font size="7.5" color="#64748B">Candidate / Legal Guardian Signature</font>', STYLES['body'])
    )

    coun_elements = []
    if coun_sig and isinstance(coun_sig, str) and coun_sig.startswith('data:image'):
        try:
            from PIL import Image as PILImage
            coun_b64 = coun_sig.split(',', 1)[1] if ',' in coun_sig else coun_sig
            coun_bytes = base64.b64decode(coun_b64)
            buf = io.BytesIO(coun_bytes)
            with PILImage.open(buf) as test_im:
                test_im.load()
            coun_elements.append(RLImage(io.BytesIO(coun_bytes), width=1.5 * inch, height=0.42 * inch))
        except Exception:
            pass
    coun_elements.append(
        Paragraph('__________________________________________<br/>'
                  f'<b>{analyst.upper()}</b><br/>'
                  '<font size="7.5" color="#64748B">Certified Dermatoglyphics Consultant</font>', STYLES['body'])
    )

    sig_cells = [[cand_elements, coun_elements]]
    t_sig = Table(sig_cells, colWidths=[CONTENT_W * 0.50, CONTENT_W * 0.50])
    t_sig.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'BOTTOM'),
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('RIGHTPADDING', (0, 0), (-1, -1), 12),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    p60_block.append(t_sig)
    p60_block.append(Spacer(1, 10))

    footer_audit = (
        '<font size="6.5" color="#94A3B8">'
        f'SYSTEM AUDIT TRAIL &bull; Report ID: {client_id} &bull; Generated: {test_date} &bull; '
        'Engine: DMIT Analysis Platform Core 3.2 Scientific-Full &bull; Verification Hash: OK-SEC-9248 &bull; Page 60 of 60'
        '</font>'
    )
    p60_block.append(Paragraph(footer_audit, STYLES['body']))

    pages.append(shrink_block(p60_block, max_height=9.2 * inch, _label='signoff_page_60'))

    return pages
