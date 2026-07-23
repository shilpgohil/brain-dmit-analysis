"""
Analysis pipeline routes.
"""
from __future__ import annotations

import asyncio
import logging
import re
import shutil
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import List, Optional

from fastapi import APIRouter, BackgroundTasks, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse

from api.helpers import (
    is_palm_position,
    palm_hand_label,
    parse_finger_position,
    parse_palm_position,
    slot_filename,
    thumbnail_url_for_path,
)
from api.schemas import (
    AnalyzeRequest,
    AnalysisResult,
    AnalysisStatus,
    AtdAnalysis,
    AtdHand,
    BrainLobeCapacity,
    CareerMatch,
    ExtensionResult,
    FingerBiometrics,
    LearningStyles,
    LobeHemispheres,
    MultipleIntelligences,
    PalmCapture,
    PatternType,
    PersonalityProfile,
    PipelineStage,
    SingularPoint,
)
from api.store import persist_session, session_store

sys.path.insert(0, str(Path(__file__).parents[2]))

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/analysis", tags=["analysis"])

OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)

CAREER_FIELD_LABELS = {
    "technical_career": ("Technology & Engineering", "Career"),
    "creative_career": ("Arts, Media & Design", "Career"),
    "analytical_career": ("Research & Analysis", "Career"),
    "leadership_career": ("Management & Leadership", "Career"),
    "social_career": ("People & Service", "Career"),
    "administrative_career": ("Operations & Administration", "Career"),
    "research_career": ("Science & Investigation", "Career"),
    "entrepreneurial_career": ("Entrepreneurship & Ventures", "Career"),
    "stem_careers": ("STEM Cluster", "Cluster"),
    "arts_media_careers": ("Arts & Media Cluster", "Cluster"),
    "business_careers": ("Business Cluster", "Cluster"),
    "service_careers": ("Service Cluster", "Cluster"),
    "innovation_careers": ("Innovation Cluster", "Cluster"),
}


def _humanize_extension_name(name: str) -> str:
    """LeftRightBrainExtension → Left Right Brain"""
    raw = name
    if raw.endswith("Extension"):
        raw = raw[: -len("Extension")]
    spaced = re.sub(r"([a-z])([A-Z])", r"\1 \2", raw)
    spaced = spaced.replace("_", " ")
    return " ".join(spaced.split()).title()


def _extension_lookup_key(name: str) -> str:
    raw = name
    if raw.endswith("Extension"):
        raw = raw[: -len("Extension")]
    return re.sub(r"([a-z])([A-Z])", r"\1_\2", raw).lower()


def _stage(id: str, label: str, status: str = "pending", detail: str = None) -> dict:
    return {"id": id, "label": label, "status": status, "duration_ms": None, "detail": detail}


def _normalize_finger_results(raw_results: list) -> list:
    fingers = []
    for r in raw_results:
        info = r.get("pipeline_info", {})
        fe = r.get("feature_extraction", {})
        feats = fe.get("consolidated_features", {})
        summary = fe.get("extraction_summary", {})

        image_path = info.get("image_path")
        finger_position = info.get("finger_position") or parse_finger_position(
            Path(image_path).name if image_path else ""
        )

        # Full classification detail (family string, subtype, singular points)
        # exposed by the extractor as 'pattern_classification'.
        cls_detail = fe.get("pattern_classification") or {}

        # FIX: consolidated_features carries the NUMERIC 'pattern_family'
        # (0=arch, 1=loop, 2=whorl, 3=accidental), not a 'pattern_type' string —
        # the old lookup made every finger render as "unknown" in the API.
        _family_map = {0: "arch", 1: "loop", 2: "whorl", 3: "accidental"}
        pattern_raw = feats.get("pattern_type") or cls_detail.get("family")
        if not pattern_raw:
            try:
                pattern_raw = _family_map.get(int(feats.get("pattern_family", -1)), "unknown")
            except (TypeError, ValueError):
                pattern_raw = "unknown"
        try:
            pt = PatternType(str(pattern_raw).lower())
        except (ValueError, AttributeError):
            pt = PatternType.UNKNOWN

        # Singular points (core/delta coordinates) from the Poincaré classifier.
        singular_points = None
        sp = cls_detail.get("singular_points") or {}
        points = [
            SingularPoint(x=p["x"], y=p["y"], type="core") for p in sp.get("cores", [])
        ] + [
            SingularPoint(x=p["x"], y=p["y"], type="delta") for p in sp.get("deltas", [])
        ]
        if points:
            singular_points = points

        finger = FingerBiometrics(
            finger_id=finger_position or info.get("finger_type", "unknown"),
            finger_type=info.get("finger_type", "unknown"),
            finger_position=finger_position,
            pattern_type=pt,
            # CADA subtype name (e.g. "Spiral Whorl") from the classifier.
            pattern_subtype=feats.get("pattern_subtype") or cls_detail.get("subtype_name"),
            ridge_count=int(feats["tfrc"]) if feats.get("tfrc") is not None else None,
            fractal_dimension=feats.get("box_counting_dimension"),
            # FIX: extractor emits 'overall_quality_score' in features and
            # 'image_quality_score' / 'quality_level' in the summary — the old
            # keys ('quality_score' / 'quality_tier') never existed, so quality
            # was always null in API results.
            quality_score=feats.get("quality_score")
            or feats.get("overall_quality_score")
            or summary.get("image_quality_score"),
            quality_tier=summary.get("quality_tier") or summary.get("quality_level"),
            singular_points=singular_points,
            minutiae_count=int(feats["minutiae_count"]) if feats.get("minutiae_count") is not None else None,
            entropy=feats.get("entropy"),
            image_path=image_path,
            thumbnail_url=thumbnail_url_for_path(image_path),
            raw_features={k: v for k, v in feats.items() if isinstance(v, (int, float, str, bool))},
        )
        fingers.append(finger)
    return fingers


def _extract_brain_lobes(agg: dict) -> Optional[BrainLobeCapacity]:
    bm = agg.get("brain_mapping", {})
    if not bm:
        return None
    lobe_hemis = None
    raw_hemis = bm.get("lobe_hemispheres")
    if isinstance(raw_hemis, dict):
        lobe_hemis = {
            lobe: LobeHemispheres(left=cells.get("left"), right=cells.get("right"))
            for lobe, cells in raw_hemis.items()
            if isinstance(cells, dict)
        }
    return BrainLobeCapacity(
        prefrontal_lobe=bm.get("prefrontal_lobe"),
        posterior_frontal=bm.get("posterior_frontal"),
        parietal_lobe=bm.get("parietal_lobe"),
        temporal_lobe=bm.get("temporal_lobe"),
        occipital_lobe=bm.get("occipital_lobe"),
        left_hemisphere=bm.get("left_hemisphere"),
        right_hemisphere=bm.get("right_hemisphere"),
        dominant_hemisphere=bm.get("dominant_hemisphere"),
        lobe_hemispheres=lobe_hemis,
    )


def _extract_atd(agg: dict) -> Optional[AtdAnalysis]:
    atd = agg.get("atd_analysis")
    if not isinstance(atd, dict):
        return None

    def hand(data):
        if not isinstance(data, dict):
            return None
        return AtdHand(
            angle_deg=data["angle_deg"],
            range_category=data["range_category"],
            learning_speed=data["learning_speed"],
            fine_motor_capacity=data["fine_motor_capacity"],
            sensory_sensitivity=data["sensory_sensitivity"],
            interpretation=data["interpretation"],
            method=data.get("method"),
            confidence=data.get("confidence"),
            source_note=data.get("source_note"),
        )

    left = hand(atd.get("left_hand"))
    right = hand(atd.get("right_hand"))
    if left is None and right is None:
        return None
    return AtdAnalysis(left_hand=left, right_hand=right, summary=atd.get("summary"))


def _extract_mi(agg: dict) -> Optional[MultipleIntelligences]:
    mi = agg.get("multiple_intelligences", {})
    if not mi:
        return None
    return MultipleIntelligences(
        linguistic=mi.get("linguistic"),
        logical_mathematical=mi.get("logical_mathematical"),
        spatial=mi.get("spatial"),
        musical=mi.get("musical"),
        bodily_kinesthetic=mi.get("bodily_kinesthetic"),
        interpersonal=mi.get("interpersonal"),
        intrapersonal=mi.get("intrapersonal"),
        naturalistic=mi.get("naturalistic"),
        existential=mi.get("existential"),
    )


def _extract_learning(agg: dict) -> Optional[LearningStyles]:
    ls = agg.get("learning_styles", {})
    if not ls:
        return None
    return LearningStyles(
        visual=ls.get("visual"),
        auditory=ls.get("auditory"),
        kinesthetic=ls.get("kinesthetic"),
    )


def _extract_personality(agg: dict) -> Optional[PersonalityProfile]:
    pb = agg.get("personality_behavior", {})
    if not pb:
        return None
    return PersonalityProfile(
        openness=pb.get("openness"),
        conscientiousness=pb.get("conscientiousness"),
        extraversion=pb.get("extraversion"),
        agreeableness=pb.get("agreeableness"),
        neuroticism=pb.get("neuroticism"),
    )


def _extract_extensions(ext_results: dict) -> list:
    extensions = []
    category_map = {
        "emotional_intelligence": "Emotional",
        "decision_making": "Cognitive",
        "attention_focus": "Cognitive",
        "creativity_index": "Creative",
        "stress_response": "Wellness",
        "left_right_brain": "Brain",
        "neurodivergence": "Neurological",
        "cognitive_load": "Cognitive",
        "executive_function": "Cognitive",
        "memory_processing": "Cognitive",
        "career_guidance": "Career",
        "learning_style": "Learning",
        "communication_style": "Social",
        "relationship_dynamics": "Social",
        "health_wellness": "Wellness",
        "leadership_potential": "Leadership",
        "entrepreneurial_aptitude": "Career",
        "motivation_drive": "Personality",
        "self_regulation": "Personality",
        "social_awareness": "Social",
        "linguistic_intelligence": "Intelligence",
        "logical_mathematical_intelligence": "Intelligence",
        "spatial_intelligence": "Intelligence",
        "bodily_kinesthetic_intelligence": "Intelligence",
        "musical_intelligence": "Intelligence",
        "interpersonal_intelligence": "Intelligence",
        "intrapersonal_intelligence": "Intelligence",
        "naturalistic_intelligence": "Intelligence",
        "risk_tolerance": "Personality",
        "curiosity_exploratory": "Personality",
        "persistence_grit": "Personality",
        "digital_intelligence": "Advanced",
        "cultural_intelligence": "Social",
        "financial_intelligence": "Career",
        "meta_cognition": "Cognitive",
        "innovation_intelligence": "Creative",
        "systems_thinking": "Cognitive",
        "pattern_recognition": "Cognitive",
        "problem_solving": "Cognitive",
        "adaptability_resilience": "Personality",
        "team_collaboration": "Social",
        "time_management": "Cognitive",
        "work_style": "Personality",
        "learning_agility": "Learning",
        "sustainability_intelligence": "Advanced",
        "wellness_intelligence": "Wellness",
    }

    for name, scores in ext_results.items():
        if not isinstance(scores, dict):
            continue
        numeric_scores = {k: float(v) for k, v in scores.items() if isinstance(v, (int, float))}
        if not numeric_scores:
            continue
        # Extensions name their primary aggregate '{domain}_score' or
        # '{domain}_index' (never 'overall'/'score'); the previous fallback to
        # "first numeric value" picked an arbitrary sub-dimension instead.
        primary = scores.get("overall", scores.get("score"))
        if primary is None:
            primary = next(
                (v for k, v in numeric_scores.items() if k.endswith(("_score", "_index"))),
                None,
            )
        if primary is None:
            primary = next(iter(numeric_scores.values()), 0)
        lookup = _extension_lookup_key(name) if name[0].isupper() else name
        display_name = _humanize_extension_name(name) if name[0].isupper() else name.replace("_", " ").title()
        extensions.append(
            ExtensionResult(
                name=display_name,
                category=category_map.get(lookup, "General"),
                scores=numeric_scores,
                primary_score=float(primary),
                recommendations=scores.get("recommendations", [])
                if isinstance(scores.get("recommendations"), list)
                else [],
            )
        )
    return sorted(extensions, key=lambda x: x.primary_score, reverse=True)


def _extract_careers(ext_results: dict) -> list:
    careers = []
    career_data = ext_results.get("career_guidance", {})
    if not isinstance(career_data, dict):
        career_data = {}

    for field_key, (title, category) in CAREER_FIELD_LABELS.items():
        score = career_data.get(field_key)
        if score is not None and isinstance(score, (int, float)) and score > 0:
            careers.append(
                CareerMatch(
                    title=title,
                    category=category,
                    match_score=float(score),
                    key_strengths=[],
                )
            )

    # Fallback: entrepreneurial extension
    if not careers:
        ent = ext_results.get("entrepreneurial_aptitude", {})
        if isinstance(ent, dict):
            for k, v in ent.items():
                if isinstance(v, (int, float)) and v > 0 and k not in ("overall", "score"):
                    careers.append(
                        CareerMatch(
                            title=k.replace("_", " ").title(),
                            category="Career",
                            match_score=float(v),
                            key_strengths=[],
                        )
                    )

    return sorted(careers, key=lambda x: x.match_score, reverse=True)[:12]


def _run_pipeline_sync(session_id: str, use_preprocessing: bool, generate_pdf: bool) -> None:
    session = session_store.get(session_id)
    if not session:
        return

    t_start = time.time()
    warnings: List[str] = []

    def update_stage(stage_id: str, status: str, duration: float = None, detail: str = None):
        for s in session["pipeline_stages"]:
            if s["id"] == stage_id:
                s["status"] = status
                if duration is not None:
                    s["duration_ms"] = round(duration * 1000, 1)
                if detail is not None:
                    s["detail"] = detail
                break

    stage_defs = [
        ("preprocessing", "Image Preprocessing"),
        ("extraction", "Feature Extraction"),
        ("mapping", "Intelligence Mapping"),
        ("extensions", "Extension Analysis"),
        ("report", "Report Generation"),
    ]
    session["pipeline_stages"] = [_stage(sid, label) for sid, label in stage_defs]

    image_paths = session.get("image_paths", [])
    if not image_paths:
        session["status"] = AnalysisStatus.FAILED
        session["error"] = "No images uploaded for this session"
        persist_session(session_id)
        return

    try:
        from integrated_dmit_pipeline import IntegratedDMITPipeline

        session["status"] = AnalysisStatus.PREPROCESSING
        update_stage("preprocessing", "running")
        t0 = time.time()
        pipeline = IntegratedDMITPipeline(use_preprocessing=use_preprocessing)
        update_stage("preprocessing", "completed", time.time() - t0)

        session["status"] = AnalysisStatus.EXTRACTING
        update_stage("extraction", "running", detail="85 biometric features per finger")
        t0 = time.time()

        palm_images = {
            slot.upper(): path
            for slot, path in (session.get("palm_slots") or {}).items()
        }
        full_result = pipeline.analyze_multiple_fingers(image_paths, palm_images=palm_images)
        individual_results = full_result.get("individual_results", [])
        session["completed_fingers"] = len(individual_results)

        if len(individual_results) < len(image_paths):
            warnings.append(
                f"{len(image_paths) - len(individual_results)} of {len(image_paths)} "
                "fingerprints could not be analyzed"
            )

        update_stage("extraction", "completed", time.time() - t0)

        session["status"] = AnalysisStatus.MAPPING
        update_stage("mapping", "running")
        t0 = time.time()
        agg_data = full_result.get("aggregated_analysis", {})
        agg = agg_data.get("dmit_profile", {})
        update_stage("mapping", "completed", time.time() - t0)

        session["status"] = AnalysisStatus.EXTENDING
        update_stage("extensions", "running", detail="40+ extension modules")
        t0 = time.time()
        ext_results = agg_data.get("extension_results", {})
        update_stage("extensions", "completed", time.time() - t0)

        fingers = _normalize_finger_results(individual_results)

        zero_ridges = sum(1 for f in fingers if f.ridge_count == 0)
        if fingers and zero_ridges == len(fingers):
            warnings.append(
                "All ridge counts are 0. Scanner BMP prints should be analyzed with "
                "preprocessing OFF — phone-photo preprocessing destroys ridge structure "
                "and misclassifies whorls as arches."
            )
        elif zero_ridges > len(fingers) // 2:
            warnings.append(
                f"{zero_ridges}/{len(fingers)} fingers have ridge count 0. "
                "Check image quality or disable preprocessing for scanner prints."
            )

        session["use_preprocessing"] = use_preprocessing
        result = AnalysisResult(
            session_id=session_id,
            status=AnalysisStatus.GENERATING_REPORT,
            subject_name=session.get("subject_name"),
            created_at=session["created_at"],
            fingers=fingers,
            brain_lobes=_extract_brain_lobes(agg),
            multiple_intelligences=_extract_mi(agg),
            learning_styles=_extract_learning(agg),
            personality=_extract_personality(agg),
            atd_analysis=_extract_atd(agg),
            extensions=_extract_extensions(ext_results),
            career_matches=_extract_careers(ext_results),
            pipeline_stages=[PipelineStage(**s) for s in session["pipeline_stages"]],
            total_features_extracted=sum(
                len(r.get("feature_extraction", {}).get("consolidated_features", {}))
                for r in individual_results
            ),
            warnings=warnings,
        )

        report_url = None
        if generate_pdf:
            session["status"] = AnalysisStatus.GENERATING_REPORT
            update_stage("report", "running")
            t0 = time.time()
            try:
                report_path = str(OUTPUT_DIR / f"dmit_report_{session_id}.pdf")
                from premium_pdf_report import PremiumReportGenerator

                session_meta = {
                    'subject_name':   session.get('subject_name', ''),
                    'subject_age':    session.get('subject_age', ''),
                    'subject_gender': session.get('subject_gender', ''),
                    'notes':          session.get('notes', ''),
                    'counsellor':     session.get('counsellor', ''),
                    'school':         session.get('school', ''),
                    'report_id':      f"RA-{session_id[:8].upper()}",
                }
                created_path = PremiumReportGenerator.create_report(
                    pipeline_data=full_result,
                    output_path=report_path,
                    session=session_meta,
                )
                session["report_path"] = created_path or report_path
                report_url = f"/api/analysis/{session_id}/report/download"
                update_stage("report", "completed", time.time() - t0)
            except Exception as e:
                logger.exception("PDF generation failed for session %s", session_id)
                warnings.append(f"Report generation failed: {e}")
                update_stage("report", "failed", time.time() - t0, detail=str(e))
        else:
            update_stage("report", "completed", detail="Skipped")

        result.warnings = warnings
        result.report_url = report_url
        result.processing_time_ms = round((time.time() - t_start) * 1000, 1)
        result.status = AnalysisStatus.COMPLETED
        result.pipeline_stages = [PipelineStage(**s) for s in session["pipeline_stages"]]

        session["result"] = result
        session["status"] = AnalysisStatus.COMPLETED
        session["updated_at"] = datetime.now()
        session.pop("error", None)

    except Exception as e:
        logger.exception("Pipeline failed for session %s", session_id)
        session["status"] = AnalysisStatus.FAILED
        session["error"] = str(e)
        for s in session.get("pipeline_stages", []):
            if s["status"] == "running":
                s["status"] = "failed"
                s["detail"] = str(e)

    persist_session(session_id)


async def _run_pipeline(session_id: str, use_preprocessing: bool, generate_pdf: bool):
    await asyncio.to_thread(_run_pipeline_sync, session_id, use_preprocessing, generate_pdf)


@router.post("/run")
async def run_analysis(body: AnalyzeRequest, background_tasks: BackgroundTasks):
    session_id = body.session_id
    if session_id not in session_store:
        raise HTTPException(status_code=404, detail="Session not found")

    session = session_store[session_id]
    if not session.get("image_paths"):
        raise HTTPException(status_code=400, detail="No images uploaded for this session")

    if session["status"] not in (AnalysisStatus.PENDING, AnalysisStatus.FAILED, AnalysisStatus.COMPLETED):
        raise HTTPException(status_code=409, detail=f"Session is already {session['status']}")

    session["status"] = AnalysisStatus.PREPROCESSING
    session.pop("result", None)
    session.pop("error", None)
    session.pop("report_path", None)
    persist_session(session_id)

    background_tasks.add_task(_run_pipeline, session_id, body.use_preprocessing, body.generate_pdf)
    return {"session_id": session_id, "status": "started"}


def _palm_captures(session: dict) -> list:
    palms = []
    for slot, path in (session.get("palm_slots") or {}).items():
        palms.append(
            PalmCapture(
                hand=palm_hand_label(slot),
                slot=slot.upper(),
                thumbnail_url=thumbnail_url_for_path(path),
                status="pending_analysis",
            )
        )
    return palms


@router.get("/{session_id}", response_model=AnalysisResult)
async def get_analysis(session_id: str):
    if session_id not in session_store:
        raise HTTPException(status_code=404, detail="Session not found")

    session = session_store[session_id]
    palms = _palm_captures(session)

    if "result" in session:
        r = session["result"]
        if isinstance(r, dict):
            r = AnalysisResult(**r)
            session["result"] = r
        r.pipeline_stages = [PipelineStage(**s) for s in session.get("pipeline_stages", [])]
        r.palms = palms
        if session.get("report_path") and not r.report_url:
            r.report_url = f"/api/analysis/{session_id}/report/download"
        return r

    if session.get("status") == AnalysisStatus.FAILED:
        return AnalysisResult(
            session_id=session_id,
            status=AnalysisStatus.FAILED,
            subject_name=session.get("subject_name"),
            created_at=session["created_at"],
            error_message=session.get("error", "Analysis failed"),
            pipeline_stages=[PipelineStage(**s) for s in session.get("pipeline_stages", [])],
            palms=palms,
            warnings=[],
        )

    return AnalysisResult(
        session_id=session_id,
        status=session["status"],
        subject_name=session.get("subject_name"),
        created_at=session["created_at"],
        pipeline_stages=[PipelineStage(**s) for s in session.get("pipeline_stages", [])],
        palms=palms,
        warnings=[],
    )


@router.get("/{session_id}/report/download")
async def download_report(session_id: str):
    if session_id not in session_store:
        raise HTTPException(status_code=404, detail="Session not found")
    session = session_store[session_id]
    report_path = session.get("report_path")
    if not report_path or not Path(report_path).exists():
        raise HTTPException(status_code=404, detail="Report not yet generated")
    return FileResponse(
        report_path,
        media_type="application/pdf",
        filename=f"DMIT_Report_{session.get('subject_name') or session_id}.pdf",
    )


@router.post("/{session_id}/upload")
async def upload_to_session(
    session_id: str,
    files: List[UploadFile] = File(...),
    finger_positions: Optional[str] = Form(None),
):
    """Upload fingerprint images. Use finger_positions=L1,R2,... aligned with files order."""
    if session_id not in session_store:
        raise HTTPException(status_code=404, detail="Session not found")

    session = session_store[session_id]
    upload_dir = Path("uploads") / session_id
    upload_dir.mkdir(parents=True, exist_ok=True)

    positions: List[str] = []
    if finger_positions:
        positions = [p.strip().upper() for p in finger_positions.split(",") if p.strip()]

    saved = []
    slot_map = session.get("finger_slots", {})
    palm_map = session.get("palm_slots", {})

    existing_paths = list(session.get("image_paths", []))
    for i, f in enumerate(files):
        explicit = positions[i] if i < len(positions) else None
        pos = explicit or parse_finger_position(f.filename or "") or parse_palm_position(f.filename or "")

        if is_palm_position(pos):
            # Palm prints are stored for the record but NOT added to image_paths:
            # the fingerprint pipeline must never try to extract ridges from a palm.
            dest = upload_dir / slot_filename(pos, f.filename)
            with dest.open("wb") as buf:
                shutil.copyfileobj(f.file, buf)
            palm_map[pos.upper()] = str(dest)
            saved.append(str(dest))
            continue

        dest_name = slot_filename(pos, f.filename) if pos else (f.filename or f"finger_{i}.bmp")
        dest = upload_dir / dest_name

        with dest.open("wb") as buf:
            shutil.copyfileobj(f.file, buf)

        path_str = str(dest)
        saved.append(path_str)
        if pos:
            # Re-uploading a slot replaces the previous image: drop the old
            # path so the same finger is never analyzed twice (and the canonical
            # {SLOT}.{ext} path is never duplicated in image_paths).
            old_path = slot_map.get(pos)
            if old_path and old_path in existing_paths:
                existing_paths.remove(old_path)
            slot_map[pos] = path_str
        if path_str not in existing_paths:
            existing_paths.append(path_str)

    session["image_paths"] = existing_paths
    session["finger_slots"] = slot_map
    session["palm_slots"] = palm_map
    session["finger_count"] = len(session["image_paths"])
    session["updated_at"] = datetime.now()
    persist_session(session_id)

    return {"uploaded": len(saved), "total": session["finger_count"], "paths": saved}
