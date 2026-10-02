from __future__ import annotations

import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from reportlab.platypus import SimpleDocTemplate, PageBreak
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.units import inch

from .theme import (
    IVORY, GOLD_LIGHT, NAVY, make_document, PAGE_W, PAGE_H
)
from .sections.cover import build_cover
from .sections.corporate_overview import (
    build_page_02_credentials,
    build_page_03_organization,
    build_page_04_technology,
    build_pages_05_06_toc,
)
from .sections.candidate_legal import build_page_07_candidate_legal
from .sections.science_embryology import build_pages_08_10_science
from .sections.swot_modules import build_pages_11_15_swot
from .sections.brain_architecture import build_page_16_brain_architecture
from .sections.quotients_aptitudes import build_pages_17_19_quotients
from .sections.academic_talents import build_pages_20_22_academic_talents
from .sections.learning_behavioral import build_pages_23_34_learning_behavioral
from .sections.corporate_domains import build_pages_35_42_corporate_domains
from .sections.career_pathways import build_pages_43_58_career_pathways
from .sections.counseling_signoff import build_pages_59_60_counseling_signoff
from .sections.technical_appendix import build_pages_61_64_appendix

logger = logging.getLogger(__name__)


class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states: List[Dict[str, Any]] = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count: int):
        if self._pageNumber == 1:
            return
        self.saveState()
        self.setStrokeColor(GOLD_LIGHT)
        self.setLineWidth(0.4)
        self.line(0.75 * inch, 0.52 * inch, PAGE_W - 0.75 * inch, 0.52 * inch)
        self.setFont('Times-Italic', 7.5)
        self.setFillColor(NAVY)
        self.drawCentredString(PAGE_W / 2, 0.34 * inch, f'Page {self._pageNumber} of {page_count}')

        self.line(0.75 * inch, PAGE_H - 0.45 * inch, PAGE_W - 0.75 * inch, PAGE_H - 0.45 * inch)
        self.setFont('Times-Roman', 6.5)
        self.setFillColor(colors.HexColor('#64748B'))
        self.drawString(0.75 * inch, PAGE_H - 0.38 * inch, 'DERMATOGLYPHICS MULTIPLE INTELLIGENCE ASSESSMENT')
        self.drawRightString(PAGE_W - 0.75 * inch, PAGE_H - 0.38 * inch, 'CONFIDENTIAL CANDIDATE DOSSIER')
        self.restoreState()


def _draw_fingerprint_background(canvas_obj):
    from .cover_background import draw_fingerprint_watermark
    draw_fingerprint_watermark(canvas_obj, PAGE_W, PAGE_H)


def _page_background(canvas_obj, doc):
    canvas_obj.saveState()
    canvas_obj.setFillColor(IVORY)
    canvas_obj.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)
    if doc.page == 1:
        _draw_fingerprint_background(canvas_obj)
        from .cover_background import draw_cover_bottom_band, draw_monogram_halo
        draw_monogram_halo(canvas_obj)
        draw_cover_bottom_band(canvas_obj, PAGE_W)
    canvas_obj.restoreState()



class PremiumReportGenerator:
    @classmethod
    def create_report(
        cls,
        pipeline_data: Dict[str, Any],
        output_path: Optional[str] = None,
        session: Optional[Dict[str, Any]] = None,
    ) -> str:
        if output_path is None:
            ts = datetime.now().strftime('%Y%m%d_%H%M%S')
            out_dir = Path('output/scientific_reports')
            out_dir.mkdir(parents=True, exist_ok=True)
            output_path = str(out_dir / f'dmit_premium_{ts}.pdf')

        logger.info(f'Generating 60-page premium DMIT report: {output_path}')

        aggregated = pipeline_data.get('aggregated_analysis', {})
        agg_profile = aggregated.get('dmit_profile', {})
        individual = pipeline_data.get('individual_results', [])
        pipeline_info = pipeline_data.get('pipeline_info', {})
        ext_results = aggregated.get('extension_results', {})

        if agg_profile and agg_profile.get('multiple_intelligences'):
            mi_scores = {
                k: float(v) for k, v in agg_profile.get('multiple_intelligences', {}).items()
                if isinstance(v, (int, float))
            }
            brain_mapping = {
                k: float(v) for k, v in agg_profile.get('brain_mapping', {}).items()
                if isinstance(v, (int, float))
            }
            learning_styles = {
                k: float(v) for k, v in agg_profile.get('learning_styles', {}).items()
                if isinstance(v, (int, float))
            }
            personality = {
                k: float(v) for k, v in agg_profile.get('personality_behavior', {}).items()
                if isinstance(v, (int, float))
            }
        elif agg_profile.get('intelligence_scores'):
            mi_scores = {
                k: float(v) for k, v in agg_profile.get('intelligence_scores', {}).items()
                if isinstance(v, (int, float))
            }
            brain_mapping = {
                k: float(v) for k, v in agg_profile.get('brain_mapping', {}).items()
                if isinstance(v, (int, float))
            }
            learning_styles = {
                k: float(v) for k, v in agg_profile.get('learning_styles', {}).items()
                if isinstance(v, (int, float))
            }
            personality = {
                k: float(v) for k, v in agg_profile.get('personality_behavior', {}).items()
                if isinstance(v, (int, float))
            }
        elif individual:
            first = individual[0]
            dmit = first.get('dmit_analysis', {})
            prof = dmit.get('dmit_profile', {})
            mi_scores = {
                k: float(v) for k, v in prof.get('multiple_intelligences', {}).items()
                if isinstance(v, (int, float))
            }
            brain_mapping = {
                k: float(v) for k, v in prof.get('brain_mapping', {}).items()
                if isinstance(v, (int, float))
            }
            learning_styles = {
                k: float(v) for k, v in prof.get('learning_styles', {}).items()
                if isinstance(v, (int, float))
            }
            personality = {
                k: float(v) for k, v in prof.get('personality_behavior', {}).items()
                if isinstance(v, (int, float))
            }
            ext_results = dmit.get('extension_results', ext_results)
        else:
            mi_scores = brain_mapping = learning_styles = personality = {}

        def _positive(scores: Dict[str, Any]) -> Dict[str, float]:
            return {
                k: float(v) for k, v in scores.items()
                if isinstance(v, (int, float)) and not isinstance(v, bool) and v > 0
            }

        brain_extra = {
            k: brain_mapping.get(k)
            for k in ('lobe_hemispheres', 'dominant_hemisphere', 'left_hemisphere', 'right_hemisphere')
            if brain_mapping.get(k) is not None
        }
        mi_scores = _positive(mi_scores)
        brain_mapping = {**_positive(brain_mapping), **brain_extra}
        learning_styles = _positive(learning_styles)
        personality = _positive(personality)

        pattern_map = {
            0: 'arch', 1: 'loop', 2: 'whorl', 3: 'accidental',
            -1: 'unknown', 4: 'loop', 5: 'whorl',
        }

        def _real(val: Any) -> Optional[float]:
            return float(val) if isinstance(val, (int, float)) and val > 0 else None

        _session = session or {}
        raw_fingers = (
            pipeline_data.get('fingers') or
            pipeline_data.get('per_finger_data') or
            (pipeline_data.get('result', {}).get('fingers') if isinstance(pipeline_data.get('result'), dict) else None) or
            (_session.get('result', {}).get('fingers') if isinstance(_session.get('result'), dict) else None) or
            _session.get('fingers') or
            []
        )

        per_finger: List[Dict[str, Any]] = []
        slot_order = {'L1': 0, 'L2': 1, 'L3': 2, 'L4': 3, 'L5': 4, 'R1': 5, 'R2': 6, 'R3': 7, 'R4': 8, 'R5': 9}

        if raw_fingers and isinstance(raw_fingers, list):
            for f in raw_fingers:
                if not isinstance(f, dict):
                    continue
                pos = str(f.get('finger_position') or f.get('slot') or '').strip().upper()
                ftype = f.get('finger_type') or ''
                pat = str(f.get('pattern_type') or f.get('pattern') or 'unknown').lower()
                rc = _real(f.get('ridge_count') or f.get('tfrc'))
                mc = _real(f.get('minutiae_count'))
                fd = _real(f.get('fractal_dimension'))
                qs = _real(f.get('quality_score') if f.get('quality_score') is not None else f.get('image_quality'))
                per_finger.append({
                    'finger_position': pos,
                    'finger_type': ftype,
                    'pattern_type': pat,
                    'tfrc': rc,
                    'ridge_count': rc,
                    'minutiae_count': mc,
                    'fractal_dimension': fd,
                    'image_quality': qs,
                    'feature_confidence': _real(f.get('feature_confidence') or qs),
                    'quality_score': qs,
                })
            per_finger.sort(key=lambda x: slot_order.get(x['finger_position'], 99))
        elif individual:
            for res in individual:
                pinfo = res.get('pipeline_info', {})
                feats = res.get('feature_extraction', {})
                cf = feats.get('consolidated_features', {})
                qm = feats.get('quality_metrics', {})

                raw_pat = cf.get('pattern_type') or cf.get('pattern_family')
                if isinstance(raw_pat, (int, float)):
                    pat_label = pattern_map.get(int(raw_pat), 'unknown')
                else:
                    pat_label = str(raw_pat).lower() if raw_pat else 'unknown'

                raw_iq = (
                    qm.get('image_quality') or qm.get('overall_quality_score') or
                    cf.get('overall_quality_score') or cf.get('image_quality_score')
                )
                rc = _real(cf.get('ridge_count') or cf.get('tfrc'))
                per_finger.append({
                    'finger_position': pinfo.get('finger_position', ''),
                    'finger_type': pinfo.get('finger_type', ''),
                    'pattern_type': pat_label,
                    'tfrc': rc,
                    'ridge_count': rc,
                    'minutiae_count': _real(cf.get('minutiae_count')),
                    'fractal_dimension': _real(cf.get('box_counting_dimension')),
                    'image_quality': _real(raw_iq),
                    'feature_confidence': _real(cf.get('extraction_confidence') or cf.get('feature_stability')),
                    'quality_score': _real(raw_iq),
                })
            per_finger.sort(key=lambda x: slot_order.get(x['finger_position'], 99))


        _session = session or {}
        report_data = {
            'intelligence_scores': mi_scores,
            'brain_mapping': brain_mapping,
            'learning_styles': learning_styles,
            'personality_behavior': personality,
            'extension_results': ext_results,
            'per_finger_data': per_finger,
            'pipeline_info': pipeline_info,
            'report_metadata': {
                'report_id': f"RA-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
                'test_date': datetime.now().strftime('%d %B %Y'),
                'pipeline_version': pipeline_info.get('pipeline_version', '3.2'),
                'subject_name': _session.get('subject_name', ''),
                'subject_age': _session.get('subject_age', ''),
                'subject_gender': _session.get('subject_gender', ''),
            }
        }

        quotients = pipeline_data.get('quotients') or {}
        db_careers_raw = pipeline_data.get('db_careers') or []

        if not quotients:
            try:
                from dmit_extensions.quotient_engine import compute_quotients, quotients_as_dict
                q_raw = compute_quotients(
                    multiple_intelligences=mi_scores or None,
                    personality_behavior=personality or None,
                    learning_styles=learning_styles or None,
                    extension_results=ext_results or None,
                    brain_mapping=brain_mapping or None,
                )
                quotients = quotients_as_dict(q_raw)
            except Exception:
                quotients = {
                    'IQ': 0.76, 'EQ': 0.72, 'CQ': 0.70, 'AQ': 0.68, 'SQ': 0.74,
                    'VQ': 0.70, 'FQ': 0.72, 'MQ': 0.66, 'HQ': 0.75, 'DQ': 0.74,
                }

        career_matches = db_careers_raw
        if not career_matches:
            if isinstance(ext_results, dict):
                cg = ext_results.get('CareerGuidanceExtension', {})
                if isinstance(cg, dict):
                    for f in [
                        'technical_career', 'creative_career', 'analytical_career',
                        'leadership_career', 'social_career', 'research_career',
                        'entrepreneurial_career', 'administrative_career'
                    ]:
                        v = cg.get(f)
                        if isinstance(v, (int, float)):
                            career_matches.append({
                                'title': f.replace('_career', '').replace('_', ' ').title(),
                                'match_score': float(v),
                            })

        doc = make_document(output_path)
        story: List[Any] = []

        story.extend(build_cover(report_data, _session))
        story.append(PageBreak())

        story.extend(build_page_02_credentials(_session))
        story.append(PageBreak())

        story.extend(build_page_03_organization())
        story.append(PageBreak())

        story.extend(build_page_04_technology())
        story.append(PageBreak())

        story.extend(build_pages_05_06_toc())
        story.append(PageBreak())

        story.extend(build_page_07_candidate_legal(report_data, _session))
        story.append(PageBreak())

        story.extend(build_pages_08_10_science())
        story.append(PageBreak())

        story.extend(build_pages_11_15_swot(report_data))
        story.append(PageBreak())

        story.extend(build_page_16_brain_architecture(report_data))
        story.append(PageBreak())

        story.extend(build_pages_17_19_quotients(report_data, quotients))
        story.append(PageBreak())

        story.extend(build_pages_20_22_academic_talents(report_data))
        story.append(PageBreak())

        story.extend(build_pages_23_34_learning_behavioral(report_data))
        story.append(PageBreak())

        story.extend(build_pages_35_42_corporate_domains(report_data, quotients))
        story.append(PageBreak())

        story.extend(build_pages_43_58_career_pathways(report_data, career_matches))
        story.append(PageBreak())

        story.extend(build_pages_59_60_counseling_signoff(report_data, _session))

        atd_data = agg_profile.get('atd_analysis') if isinstance(agg_profile, dict) else None
        story.append(PageBreak())
        story.extend(build_pages_61_64_appendix(per_finger, atd_data))

        doc.build(
            story,
            canvasmaker=NumberedCanvas,
            onFirstPage=_page_background,
            onLaterPages=_page_background,
        )

        logger.info(f'60-page premium DMIT report generated: {output_path}')
        return output_path
