"""
Premium DMIT Report Generator
==============================
Orchestrates all 19 sections into a single A4 PDF.
Ivory/gold theme, Times New Roman throughout, no em dashes.
"""

import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional

from reportlab.platypus import SimpleDocTemplate, PageBreak, Spacer
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch

from .theme import IVORY, GOLD, NAVY, GOLD_LIGHT, make_document
from .sections.cover import build_cover
from .sections.intro import build_intro, build_candidate_profile
from .sections.executive_summary import build_executive_summary
from .sections.fingerprint import build_fingerprint_quality, build_finger_analysis
from .sections.brain import build_brain_hemisphere, build_brain_lobes
from .sections.intelligence import (build_intelligence, build_learning,
                                     build_personality, build_emotional)
from .sections.cognitive_social_career import (build_cognitive, build_social,
                                                build_leadership, build_career)
from .sections.development import (build_parenting, build_development,
                                    build_counsellor_note)

logger = logging.getLogger(__name__)

PAGE_W, PAGE_H = A4


def _draw_brain_neural_background(canvas):
    """Cover watermark from assets/cover_brain_watermark.png (approved mockup)."""
    from .cover_background import draw_brain_neural_watermark
    draw_brain_neural_watermark(canvas, PAGE_W, PAGE_H)


def _page_background(canvas, doc):
    """Draw ivory background and thin gold footer rule on every page.
    On page 1 (cover), draw the brain neural network watermark."""
    canvas.saveState()
    canvas.setFillColor(IVORY)
    canvas.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)

    # Brain neural pattern decorates only the cover page (page 1)
    if doc.page == 1:
        _draw_brain_neural_background(canvas)

    # Footer rule
    canvas.setStrokeColor(GOLD_LIGHT)
    canvas.setLineWidth(0.5)
    canvas.line(0.75 * inch, 0.55 * inch, PAGE_W - 0.75 * inch, 0.55 * inch)
    # Page number
    canvas.setFillColor(NAVY)
    canvas.setFont('Times-Italic', 8)
    canvas.drawCentredString(PAGE_W / 2, 0.35 * inch, f'Page {doc.page}')
    canvas.restoreState()


class PremiumReportGenerator:
    """
    Main entry point for generating the premium DMIT PDF report.

    Usage:
        PremiumReportGenerator.create_report(pipeline_data, output_path)
    """

    @classmethod
    def create_report(cls,
                      pipeline_data: Dict[str, Any],
                      output_path: Optional[str] = None,
                      session: Optional[Dict[str, Any]] = None) -> str:
        """
        Generate the premium PDF report from pipeline_data.

        Args:
            pipeline_data: Raw pipeline output dict
            output_path:   Where to save the PDF (auto-generated if None)
            session:       Optional session metadata dict with subject info

        Returns:
            Absolute path to the generated PDF.
        """
        if output_path is None:
            ts = datetime.now().strftime('%Y%m%d_%H%M%S')
            out_dir = Path('output/scientific_reports')
            out_dir.mkdir(parents=True, exist_ok=True)
            output_path = str(out_dir / f'dmit_premium_{ts}.pdf')

        logger.info(f'Generating premium DMIT report: {output_path}')

        # ---------------------------------------------------------------
        # Extract data from pipeline_data (same structure as existing gen)
        # ---------------------------------------------------------------
        aggregated = pipeline_data.get('aggregated_analysis', {})
        agg_profile = aggregated.get('dmit_profile', {})
        individual  = pipeline_data.get('individual_results', [])
        pipeline_info = pipeline_data.get('pipeline_info', {})

        # Try all known pipeline output structures in priority order
        ext_results = aggregated.get('extension_results', {})

        if agg_profile and agg_profile.get('multiple_intelligences'):
            # Real pipeline: aggregated_analysis.dmit_profile.multiple_intelligences
            mi_scores       = {k: float(v) for k, v in
                               agg_profile.get('multiple_intelligences', {}).items()
                               if isinstance(v, (int, float))}
            brain_mapping   = {k: float(v) for k, v in
                               agg_profile.get('brain_mapping', {}).items()
                               if isinstance(v, (int, float))}
            learning_styles = {k: float(v) for k, v in
                               agg_profile.get('learning_styles', {}).items()
                               if isinstance(v, (int, float))}
            personality     = {k: float(v) for k, v in
                               agg_profile.get('personality_behavior', {}).items()
                               if isinstance(v, (int, float))}
        elif agg_profile.get('intelligence_scores'):
            # Legacy / test structure: aggregated_analysis.dmit_analysis.intelligence_scores
            mi_scores       = {k: float(v) for k, v in
                               agg_profile.get('intelligence_scores', {}).items()
                               if isinstance(v, (int, float))}
            brain_mapping   = {k: float(v) for k, v in
                               agg_profile.get('brain_mapping', {}).items()
                               if isinstance(v, (int, float))}
            learning_styles = {k: float(v) for k, v in
                               agg_profile.get('learning_styles', {}).items()
                               if isinstance(v, (int, float))}
            personality     = {k: float(v) for k, v in
                               agg_profile.get('personality_behavior', {}).items()
                               if isinstance(v, (int, float))}
        elif individual:
            first = individual[0]
            dmit  = first.get('dmit_analysis', {})
            prof  = dmit.get('dmit_profile', {})
            mi_scores       = {k: float(v) for k, v in
                               prof.get('multiple_intelligences', {}).items()
                               if isinstance(v, (int, float))}
            brain_mapping   = {k: float(v) for k, v in
                               prof.get('brain_mapping', {}).items()
                               if isinstance(v, (int, float))}
            learning_styles = {k: float(v) for k, v in
                               prof.get('learning_styles', {}).items()
                               if isinstance(v, (int, float))}
            personality     = {k: float(v) for k, v in
                               prof.get('personality_behavior', {}).items()
                               if isinstance(v, (int, float))}
            ext_results     = dmit.get('extension_results', ext_results)
        else:
            mi_scores = brain_mapping = learning_styles = personality = {}

        def _positive(scores):
            return {
                k: v for k, v in scores.items()
                if isinstance(v, (int, float)) and not isinstance(v, bool) and v > 0
            }

        brain_extra = {
            k: brain_mapping.get(k)
            for k in ('lobe_hemispheres', 'dominant_hemisphere',
                      'left_hemisphere', 'right_hemisphere')
            if brain_mapping.get(k) is not None
        }
        mi_scores       = _positive(mi_scores)
        brain_mapping   = {**_positive(brain_mapping), **brain_extra}
        learning_styles = _positive(learning_styles)
        personality     = _positive(personality)

        # Per-finger data
        per_finger = []
        # Map numeric pattern_family codes to human-readable labels
        _PATTERN_MAP = {
            0: 'arch', 1: 'loop', 2: 'whorl', 3: 'accidental',
            -1: 'unknown', 4: 'loop', 5: 'whorl',
        }

        def _real(val):
            """Return val if it is a positive number; else None (prevents misleading 0)."""
            return val if isinstance(val, (int, float)) and val > 0 else None

        for res in individual:
            pinfo = res.get('pipeline_info', {})
            feats = res.get('feature_extraction', {})
            cf    = feats.get('consolidated_features', {})
            qm    = feats.get('quality_metrics', {})

            raw_pat = cf.get('pattern_type') or cf.get('pattern_family')
            if isinstance(raw_pat, (int, float)):
                pat_label = _PATTERN_MAP.get(int(raw_pat), 'unknown')
            else:
                pat_label = str(raw_pat).lower() if raw_pat else 'unknown'

            raw_iq = (qm.get('image_quality') or qm.get('overall_quality_score') or
                      cf.get('overall_quality_score') or cf.get('image_quality_score'))
            per_finger.append({
                'finger_position': pinfo.get('finger_position', ''),
                'finger_type':     pinfo.get('finger_type', ''),
                'pattern_type':    pat_label,
                'tfrc':            _real(cf.get('tfrc')),
                'ridge_count':     _real(cf.get('tfrc')),
                'minutiae_count':  _real(cf.get('minutiae_count')),
                'fractal_dimension': _real(cf.get('box_counting_dimension')),
                'image_quality':   _real(raw_iq),
                'feature_confidence': _real(cf.get('extraction_confidence') or
                                            cf.get('feature_stability')),
                'quality_score':   _real(raw_iq),
            })

        report_data = {
            'intelligence_scores': mi_scores,
            'brain_mapping':       brain_mapping,
            'learning_styles':     learning_styles,
            'personality_behavior': personality,
            'extension_results':   ext_results,
            'per_finger_data':     per_finger,
            'pipeline_info':       pipeline_info,
            'report_metadata':     {
                'report_id':     f"RA-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
                'test_date':     datetime.now().strftime('%d %B %Y'),
                'pipeline_version': pipeline_info.get('pipeline_version', '1.0'),
                'subject_name':  (session or {}).get('subject_name', ''),
                'subject_age':   (session or {}).get('subject_age', ''),
                'subject_gender': (session or {}).get('subject_gender', ''),
            }
        }

        # Career matches from ext_results
        career_matches = []
        if isinstance(ext_results, dict):
            cg = ext_results.get('CareerGuidanceExtension', {})
            if isinstance(cg, dict):
                for f in ['technical_career', 'creative_career', 'analytical_career',
                          'leadership_career', 'social_career', 'research_career',
                          'entrepreneurial_career', 'administrative_career']:
                    v = cg.get(f)
                    if isinstance(v, (int, float)):
                        career_matches.append({
                            'title': f.replace('_career', '').replace('_', ' ').title(),
                            'match_score': float(v),
                        })

        _session = session or {}

        # ---------------------------------------------------------------
        # Build PDF document
        # ---------------------------------------------------------------
        doc = make_document(output_path)
        story = []

        # Section 1 : Cover
        story += build_cover(report_data, _session)
        story.append(PageBreak())

        # Section 2 : Scientific Intro
        story += build_intro()
        story.append(PageBreak())

        # Section 3 : Candidate Profile
        story += build_candidate_profile(_session)
        story.append(PageBreak())

        # Section 4 : Executive Summary
        story += build_executive_summary(report_data, _session)
        story.append(PageBreak())

        # Section 5 : Fingerprint Quality
        if per_finger:
            story += build_fingerprint_quality(per_finger)
            story.append(PageBreak())

            # Section 6 : Finger-wise Analysis
            story += build_finger_analysis(per_finger)
            story.append(PageBreak())

        # Section 7 : Brain Hemisphere
        if brain_mapping:
            story += build_brain_hemisphere(brain_mapping)
            story.append(PageBreak())

            # Section 8 : Brain Lobes
            story += build_brain_lobes(brain_mapping)
            story.append(PageBreak())

        # Section 9 : Multiple Intelligence
        if mi_scores:
            story += build_intelligence(mi_scores)
            story.append(PageBreak())

        # Section 10 : Learning Style
        if learning_styles:
            story += build_learning(learning_styles)
            story.append(PageBreak())

        # Section 11 : Personality
        if personality:
            story += build_personality(personality)
            story.append(PageBreak())

        # Section 12 : Emotional Intelligence
        if ext_results:
            story += build_emotional(ext_results)
            story.append(PageBreak())

            # Section 13 : Cognitive Skills
            story += build_cognitive(ext_results)
            story.append(PageBreak())

            # Section 14 : Communication and Social
            story += build_social(ext_results)
            story.append(PageBreak())

            # Section 15 : Leadership
            story += build_leadership(ext_results)
            story.append(PageBreak())

        # Section 16 : Career Analysis
        story += build_career(ext_results, career_matches, mi_scores, personality)
        story.append(PageBreak())

        # Section 17 : Parenting Guidelines
        story += build_parenting(learning_styles, personality)
        story.append(PageBreak())

        # Section 18 : Development Roadmap
        story += build_development(mi_scores)
        story.append(PageBreak())

        # Section 19 : Counsellor Note
        story += build_counsellor_note(report_data, _session)

        # ---------------------------------------------------------------
        # Build
        # ---------------------------------------------------------------
        doc.build(story,
                  onFirstPage=_page_background,
                  onLaterPages=_page_background)

        logger.info(f'Premium DMIT report generated: {output_path}')
        return output_path
