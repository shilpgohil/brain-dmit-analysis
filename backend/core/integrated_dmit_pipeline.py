#!/usr/bin/env python3
"""
🚀 INTEGRATED DMIT PIPELINE WITH ADVANCED 3D PDF GENERATOR
=========================================================

Complete DMIT analysis pipeline using:
- Optimized Feature Extractor (real calculations only)
- DMIT Intelligence Mapper (Scientific 2.0 - Weighted Integration)
- Advanced 3D PDF Generator (stunning visuals, no dependencies)
- Real pipeline data only (no defaults, no fake values)

Author: DMIT Research Integration
Version: 3.1 - Scientific Mapping Support
"""

import os
import sys
import time
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
import json
import numpy as np
import cv2  # type: ignore

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Import core pipeline components
try:
    from optimized_feature_extractor_clean import OptimizedFeatureExtractor
    from dmit_intelligence_mapper import (
        map_features_to_dmit_profile,
        map_atd_angle,
        FingerType,
        BrainLobe,
        create_bulletproof_dmit_analysis
    )
    from advanced_3d_pdf_generator import create_3d_report
    from preprocessing_images import FingerToFingerprintPipeline
    from palm_processing import PalmAtdEstimator
    # Also load the extension engine
    from dmit_extensions.engine import DMITExtensionsEngine
    logger.info("✅ All core components imported successfully")
except ImportError as e:
    logger.exception(f"❌ Failed to import core components: {e}")
    logger.error("Please ensure all required modules are available")
    sys.exit(1)

class IntegratedDMITPipeline:
    """
    🎯 Integrated DMIT Pipeline with Scientific Mapping
    
    Features:
    - Automatic Finger Identification (filenames _00 to _04)
    - Weighted Slot Aggregation (Index -> Logic, Thumb -> Personality)
    - Real feature extraction
    - Advanced 3D PDF generation
    """
    
    def __init__(self, use_preprocessing: bool = True):
        self.feature_extractor = OptimizedFeatureExtractor()
        self.use_preprocessing = use_preprocessing
        if self.use_preprocessing:
            self.preprocessor = FingerToFingerprintPipeline()
        self.extension_engine = DMITExtensionsEngine()
        self.palm_atd = PalmAtdEstimator()
        self._palm_images: Dict[str, str] = {}
        self.session_atd: Optional[Dict[str, Any]] = None
        self.pipeline_version = "3.2-Scientific-Full"
        self.start_time = datetime.now()
        
        logger.info(f"🚀 Integrated DMIT Pipeline v{self.pipeline_version} initialized")
        logger.info(f"✅ Preprocessing (Finger to Fingerprint): {'Enabled' if use_preprocessing else 'Disabled'}")
        logger.info("✅ Scientific Mapping (Table 1.1) enabled")
    
    def _identify_finger_position(self, filename: str) -> Optional[str]:
        """Return L1–R5 slot id from filename when present."""
        name = Path(filename).stem.upper()
        for pos in ("R1", "R2", "R3", "R4", "R5", "L1", "L2", "L3", "L4", "L5"):
            if name.startswith(pos) or pos in name:
                return pos
        return None

    def _identify_finger_type(self, filename: str) -> FingerType:
        """
        Identify finger type from filename suffix.
        Convention:
        _00, _05, _L1, _R1 -> Thumb
        _01, _06, _L2, _R2 -> Index
        _02, _07, _L3, _R3 -> Middle
        _03, _08, _L4, _R4 -> Ring
        _04, _09, _L5, _R5 -> Little
        """
        stem = Path(filename).stem.lower()
        name = stem

        def _has(*tokens: str) -> bool:
            return any(t in name for t in tokens)

        # L1/R1 slot ids (with or without underscore) and numeric suffixes
        if _has("_00", "_05", "_l1", "_r1", "l1", "r1", "thumb"):
            return FingerType.THUMB
        elif _has("_01", "_06", "_l2", "_r2", "l2", "r2", "index"):
            return FingerType.INDEX
        elif _has("_02", "_07", "_l3", "_r3", "l3", "r3", "middle"):
            return FingerType.MIDDLE
        elif _has("_03", "_08", "_l4", "_r4", "l4", "r4", "ring"):
            return FingerType.RING
        elif _has("_04", "_09", "_l5", "_r5", "l5", "r5", "little"):
            return FingerType.LITTLE
            
        logger.warning(f"⚠️ Could not identify finger type for {filename}, defaulting to UNKNOWN")
        return FingerType.UNKNOWN

    def _singular_point_counts(self, gray: np.ndarray) -> Tuple[int, int]:
        """Return (core_count, delta_count) for choosing raw vs preprocessed image."""
        classifier = getattr(self.feature_extractor, "pattern_classifier", None)
        if classifier is None or gray is None:
            return 0, 0
        try:
            orientation = classifier._compute_orientation_field(gray)
            cores, deltas = classifier._detect_singular_points(gray, orientation)
            return len(cores or []), len(deltas or [])
        except Exception:
            return 0, 0

    def _is_likely_scanned_fingerprint(self, image_path: str) -> bool:
        """
        Detect ridge-ready scanner prints so we do not run the phone-photo
        preprocessing pipeline on them. Preprocessing on BMP scanner crops destroys
        singular-point structure and misclassifies whorls as arches (TFRC → 0).
        """
        ext = Path(image_path).suffix.lower()
        if ext in (".bmp", ".tif", ".tiff"):
            return True

        raw = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        if raw is None:
            return False

        classifier = getattr(self.feature_extractor, "pattern_classifier", None)
        if classifier is not None:
            try:
                orientation = classifier._compute_orientation_field(raw)
                cores, deltas = classifier._detect_singular_points(raw, orientation)
                if cores and deltas:
                    return True
            except Exception:
                pass

        h, w = raw.shape[:2]
        if h > 900 or w > 900:
            return False

        edges = cv2.Canny(raw, 40, 120)
        edge_density = float(np.mean(edges > 0))
        # Scanner ROI prints: compact frame, strong ridge edges, no finger silhouette crop.
        return edge_density >= 0.06 and min(h, w) >= 200

    def analyze_single_finger(self, image_path: str) -> Dict[str, Any]:
        """
        Analyze a single fingerprint image with real feature extraction and scientific mapping.
        """
        logger.info(f"🔍 Analyzing single finger: {image_path}")
        
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image not found: {image_path}")
        
        # 1. Identify Finger
        finger_type = self._identify_finger_type(os.path.basename(image_path))
        logger.info(f"🖐️ Identified Finger: {finger_type.value.upper()}")
        
        # 2. Preprocess only for phone photos — skip on scanner ridge prints.
        preprocessing_meta: Dict[str, Any] = {}
        raw_gray = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        if raw_gray is None:
            raise ValueError(f"Failed to load image: {image_path}")

        skip_prep = self._is_likely_scanned_fingerprint(image_path)
        image = raw_gray
        if self.use_preprocessing and not skip_prep:
            logger.info("🛠️ Running preprocessing pipeline...")
            prep_result = self.preprocessor.process(image_path)
            if prep_result['success'] and prep_result['fingerprint'] is not None:
                prepped = prep_result['fingerprint']
                preprocessing_meta = prep_result['metadata']
                raw_cores, raw_deltas = self._singular_point_counts(raw_gray)
                prep_cores, prep_deltas = self._singular_point_counts(prepped)
                if (raw_cores + raw_deltas) > (prep_cores + prep_deltas):
                    logger.warning(
                        "⚠️ Preprocessing reduced singular-point structure "
                        f"({raw_cores}+{raw_deltas} → {prep_cores}+{prep_deltas}); using raw image"
                    )
                    preprocessing_meta['reverted_to_raw'] = True
                    image = raw_gray
                else:
                    image = prepped
            else:
                logger.warning("⚠️ Preprocessing failed, falling back to direct load")
                image = raw_gray
        else:
            if self.use_preprocessing and skip_prep:
                logger.info("🔬 Scanner fingerprint detected — skipping phone-photo preprocessing")
                preprocessing_meta = {'skipped': True, 'reason': 'scanned_fingerprint_detected'}
            
        if image is None:
            raise ValueError(f"Failed to load or process image: {image_path}")
        
        # 3. Extract Features
        extractor_result = self.feature_extractor.extract_optimized_features(image)
        features = extractor_result['consolidated_features']
        
        if self.use_preprocessing and preprocessing_meta:
            extractor_result['preprocessing_metadata'] = preprocessing_meta
        
        # 4. Create DMIT Profile (Scientific Mapping)
        # Note: Validating strictly via Mapper
        dmit_profile = map_features_to_dmit_profile(features, finger_type_str=finger_type.value)
        
        # 5. Run Extensions
        # Combine features and mapped intelligences for the extensions
        combined_features = {**features, **dmit_profile.get('multiple_intelligences', {})}
        logger.info("🧩 Running DMIT Extensions...")
        extension_results = self.extension_engine.run_all_extensions(combined_features)
        
        # 6. Compile Results
        finger_position = self._identify_finger_position(os.path.basename(image_path))
        results = {
            'pipeline_info': {
                'image_path': image_path,
                'finger_type': finger_type.value,
                'finger_position': finger_position,
                'timestamp': datetime.now().isoformat()
            },
            'feature_extraction': extractor_result,
            'dmit_analysis': {
                'dmit_profile': dmit_profile,
                'extension_results': extension_results
            }
        }
        
        return results

    def analyze_multiple_fingers(self, image_paths: List[str],
                                 palm_images: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        Analyze multiple fingers and aggregate using Scientific Weighted Slots.
        palm_images: optional {'LPALM': path, 'RPALM': path} used for geometric atd estimation.
        """
        self._palm_images = palm_images or {}
        logger.info(f"🔍 Analyzing {len(image_paths)} fingers...")
        
        individual_results = []
        successful_analyses = 0
        
        for i, path in enumerate(image_paths, 1):
            try:
                res = self.analyze_single_finger(path)
                individual_results.append(res)
                successful_analyses += 1
            except Exception as e:
                logger.exception(f"❌ Failed to analyze {path}: {e}")
                
        if successful_analyses == 0:
            raise ValueError("No fingers successfully analyzed")
            
        # Aggregation
        aggregated_results = self._aggregate_results_scientifically(individual_results)
        
        logger.info(f"✅ Analysis Complete. Success: {successful_analyses}/{len(image_paths)}")
        return aggregated_results

    def _group_by_finger_type(self, individual_results: List[Dict[str, Any]]) -> Dict['FingerType', List[Dict[str, Any]]]:
        fingers_map = {
            FingerType.THUMB: [],
            FingerType.INDEX: [],
            FingerType.MIDDLE: [],
            FingerType.RING: [],
            FingerType.LITTLE: [],
            FingerType.UNKNOWN: []
        }
        for res in individual_results:
            f_type_str = res['pipeline_info'].get('finger_type', 'unknown')
            try:
                f_type = FingerType(f_type_str)
            except ValueError:
                f_type = FingerType.UNKNOWN
            
            fingers_map[f_type].append(res['dmit_analysis']['dmit_profile'])
        return fingers_map

    @staticmethod
    def _slot_hand_and_type(finger_position: Optional[str]) -> Tuple[Optional[str], Optional['FingerType']]:
        if not finger_position or len(finger_position) < 2:
            return None, None
        hand = finger_position[0].upper()
        if hand not in ('L', 'R'):
            return None, None
        digit_map = {
            '1': FingerType.THUMB,
            '2': FingerType.INDEX,
            '3': FingerType.MIDDLE,
            '4': FingerType.RING,
            '5': FingerType.LITTLE,
        }
        return hand, digit_map.get(finger_position[1])

    @staticmethod
    def _mean(values: List[float]) -> Optional[float]:
        present = [v for v in values if v is not None]
        if not present:
            return None
        return round(sum(present) / len(present), 4)

    def _hand_bilateral_features(self, individual_results: List[Dict[str, Any]]) -> Dict[str, float]:
        """
        Average biometric features separately for left-hand (L1–L5) and right-hand
        (R1–R5) slots. LeftRightBrainExtension compares these pairs; mirroring the
        same holistic average into both sides falsely yields 100% asymmetry balance.
        """
        left_sums: Dict[str, float] = {}
        left_counts: Dict[str, int] = {}
        right_sums: Dict[str, float] = {}
        right_counts: Dict[str, int] = {}

        for res in individual_results:
            pos = res.get('pipeline_info', {}).get('finger_position') or ''
            hand = pos[0].upper() if pos else ''
            if hand not in ('L', 'R'):
                continue
            consolidated = res['feature_extraction']['consolidated_features']
            sums = left_sums if hand == 'L' else right_sums
            counts = left_counts if hand == 'L' else right_counts
            for key, value in consolidated.items():
                if isinstance(value, bool) or not isinstance(value, (int, float)):
                    continue
                sums[key] = sums.get(key, 0.0) + float(value)
                counts[key] = counts.get(key, 0) + 1

        bilateral: Dict[str, float] = {}
        pairs = (
            ('tfrc', 'ridge_count_left', 'ridge_count_right'),
            ('ridge_density', 'ridge_density_left', 'ridge_density_right'),
            ('graph_density', 'graph_density_left', 'graph_density_right'),
            ('spectral_radius', 'spectral_radius_left', 'spectral_radius_right'),
            ('topological_complexity', 'topological_complexity_left', 'topological_complexity_right'),
            ('euler_characteristic', 'euler_characteristic_left', 'euler_characteristic_right'),
            ('box_counting_dimension', 'fractal_dimension_left', 'fractal_dimension_right'),
        )
        for feat, left_key, right_key in pairs:
            if left_counts.get(feat):
                bilateral[left_key] = left_sums[feat] / left_counts[feat]
            if right_counts.get(feat):
                bilateral[right_key] = right_sums[feat] / right_counts[feat]
        return bilateral

    @staticmethod
    def _blend_holistic_extensions(
        ext_results: Dict[str, Any],
        agg_mi: Dict[str, Any],
        agg_ls: Dict[str, Any],
        agg_pb: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Many extension modules share isomorphic biometric formulas and collapse to
        identical holistic scores. Re-anchor each module's primary score with the
        scientifically mapped profile trait it represents (MI / learning / personality).
        """
        mi = {k: v for k, v in (agg_mi or {}).items() if isinstance(v, (int, float))}
        ls = {k: v for k, v in (agg_ls or {}).items() if isinstance(v, (int, float))}
        pb = {k: v for k, v in (agg_pb or {}).items() if isinstance(v, (int, float))}

        def mix(*weighted: Tuple[Optional[float], float]) -> Optional[float]:
            """Weighted composite of several traits; None if any component is absent."""
            vals = []
            for val, weight in weighted:
                if val is None:
                    return None
                vals.append(float(val) * weight)
            return sum(vals)

        def blend(scores: Dict[str, Any], primary_key: str, anchor: Optional[float], weight: float = 0.38):
            if anchor is None or primary_key not in scores:
                return
            raw = scores[primary_key]
            if not isinstance(raw, (int, float)):
                return
            scores[primary_key] = max(0.0, min(1.0, (1.0 - weight) * float(raw) + weight * float(anchor)))

        lm = mi.get('logical_mathematical')
        l_ = mi.get('linguistic')
        s_ = mi.get('spatial')
        mu = mi.get('musical')
        bk = mi.get('bodily_kinesthetic')
        ip = mi.get('interpersonal')
        ia = mi.get('intrapersonal')
        n_ = mi.get('naturalistic')
        o_ = pb.get('openness')
        c_ = pb.get('conscientiousness')
        e_ = pb.get('extraversion')
        a_ = pb.get('agreeableness')
        ne = pb.get('neuroticism')
        ne_inv = (1.0 - ne) if ne is not None else None
        ls_k = ls.get('kinesthetic')

        # (extension class name, primary score key, anchor value). Each anchor below is a
        # unique trait or unique weighted composite so extensions that share a conceptual
        # neighborhood (e.g. all "conscientiousness-adjacent") still diverge after blending,
        # instead of every module in the group collapsing onto one identical value.
        anchors: List[Tuple[str, str, Optional[float]]] = [
            ('LinguisticIntelligenceExtension', 'linguistic_intelligence_score', l_),
            ('CommunicationStyleExtension', 'communication_effectiveness_score', mix((l_, 0.6), (e_, 0.4))),
            ('MemoryProcessingExtension', 'memory_processing_score', mix((l_, 0.6), (ia, 0.4))),

            ('LogicalMathematicalIntelligenceExtension', 'logical_mathematical_intelligence_score', lm),
            ('CareerGuidanceExtension', 'career_potential_score', mix((lm, 0.6), (o_, 0.4))),
            ('SystemsThinkingExtension', 'systems_thinking_score', mix((lm, 0.6), (ia, 0.4))),
            ('CognitiveLoadExtension', 'cognitive_load_management_score', mix((lm, 0.6), (c_, 0.4))),
            ('EntrepreneurialAptitudeExtension', 'entrepreneurial_aptitude_score',
             mix((lm, 0.5), (ip, 0.3), (o_, 0.2))),
            ('DigitalIntelligenceExtension', 'digital_intelligence_score', mix((lm, 0.6), (s_, 0.4))),
            ('FinancialIntelligenceExtension', 'financial_intelligence_score', mix((lm, 0.6), (ne_inv, 0.4))),
            ('ProblemSolvingExtension', 'problem_solving_score', mix((lm, 0.6), (ls_k, 0.4))),
            ('DecisionMakingExtension', 'decision_making_score', mix((lm, 0.6), (a_, 0.4))),

            ('SpatialIntelligenceExtension', 'spatial_intelligence_score', s_),
            ('InnovationIntelligenceExtension', 'innovation_intelligence_score', mix((s_, 0.6), (o_, 0.4))),
            ('PatternRecognitionExtension', 'pattern_recognition_index', mix((s_, 0.6), (lm, 0.4))),

            ('MusicalIntelligenceExtension', 'musical_intelligence_score', mu),
            ('BodilyKinestheticIntelligenceExtension', 'bodily_kinesthetic_intelligence_score', bk),

            ('InterpersonalIntelligenceExtension', 'interpersonal_intelligence_score', ip),
            ('EmotionalIntelligenceExtension', 'emotional_intelligence_score', mix((ip, 0.6), (ia, 0.4))),
            ('SocialAwarenessExtension', 'social_awareness_score', mix((ip, 0.6), (o_, 0.4))),
            ('RelationshipDynamicsExtension', 'relationship_dynamics_index', mix((ip, 0.6), (a_, 0.4))),
            ('CulturalIntelligenceExtension', 'cultural_intelligence_score', mix((ip, 0.6), (e_, 0.4))),
            ('TeamCollaborationExtension', 'team_collaboration_score', mix((ip, 0.6), (c_, 0.4))),
            ('LeadershipPotentialExtension', 'leadership_potential_score', mix((ip, 0.6), (lm, 0.4))),

            ('IntrapersonalIntelligenceExtension', 'intrapersonal_intelligence_score', ia),
            ('MetaCognitionExtension', 'meta_cognition_score', mix((ia, 0.6), (lm, 0.4))),
            ('AttentionFocusExtension', 'attention_focus_score', mix((ia, 0.6), (c_, 0.4))),

            ('NaturalisticIntelligenceExtension', 'naturalistic_intelligence_score', n_),
            ('SustainabilityIntelligenceExtension', 'sustainability_intelligence_score', mix((n_, 0.6), (o_, 0.4))),

            ('CreativityIndexExtension', 'creativity_index_score', mix((s_, 0.55), (mu, 0.45))),

            ('LearningStyleExtension', 'learning_effectiveness_score', max(ls.values()) if ls else None),
            ('LearningAgilityExtension', 'learning_agility_score', ls_k),

            ('MotivationDriveExtension', 'motivation_drive_score', c_),
            ('ExecutiveFunctionExtension', 'executive_function_score', mix((c_, 0.6), (lm, 0.4))),
            ('SelfRegulationExtension', 'self_regulation_score', mix((c_, 0.6), (ne_inv, 0.4))),
            ('PersistenceGritExtension', 'persistence_grit_score', mix((c_, 0.6), (o_, 0.4))),
            ('TimeManagementExtension', 'time_management_score', mix((c_, 0.6), (ia, 0.4))),
            ('WorkStyleExtension', 'work_style_score', mix((c_, 0.6), (e_, 0.4))),

            ('RiskToleranceExtension', 'risk_tolerance_index', o_),
            ('CuriosityExploratoryExtension', 'curiosity_exploratory_score', mix((o_, 0.6), (n_, 0.4))),
            ('AdaptabilityResilienceExtension', 'adaptability_resilience_score', mix((o_, 0.6), (ne_inv, 0.4))),

            ('HealthWellnessExtension', 'health_wellness_score', ne_inv),
            ('WellnessIntelligenceExtension', 'wellness_intelligence_score', mix((ne_inv, 0.6), (c_, 0.4))),
            ('StressResponseExtension', 'stress_response_score', mix((ne_inv, 0.6), (ia, 0.4))),
        ]

        for ext_name, primary_key, anchor in anchors:
            scores = ext_results.get(ext_name)
            if isinstance(scores, dict) and 'error' not in scores:
                blend(scores, primary_key, anchor)

        return ext_results

    def _aggregate_results_scientifically(self, individual_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Aggregate per-finger DMIT profiles into a cross-lateral brain model.

        Finger type selects the lobe (Table 1.1); hand side selects the hemisphere
        contralaterally (Sperry). A trait is aggregated only from the source fingers
        that were actually analyzed; with no source present the trait is absent.
        """
        fingers_map = self._group_by_finger_type(individual_results)

        def collect(category: str, key: str, source_fingers: List[FingerType]) -> Optional[float]:
            values: List[float] = []
            for ft in source_fingers:
                for prof in fingers_map[ft]:
                    val = prof.get(category, {}).get(key)
                    if isinstance(val, (int, float)) and not isinstance(val, bool):
                        values.append(float(val))
            return self._mean(values)

        agg_mi = {
            'logical_mathematical': collect('multiple_intelligences', 'logical_mathematical', [FingerType.INDEX]),
            'linguistic': collect('multiple_intelligences', 'linguistic', [FingerType.RING]),
            'musical': collect('multiple_intelligences', 'musical', [FingerType.RING]),
            'spatial': collect('multiple_intelligences', 'spatial', [FingerType.LITTLE, FingerType.INDEX]),
            'bodily_kinesthetic': collect('multiple_intelligences', 'bodily_kinesthetic', [FingerType.MIDDLE]),
            'interpersonal': collect('multiple_intelligences', 'interpersonal', [FingerType.THUMB]),
            'intrapersonal': collect('multiple_intelligences', 'intrapersonal', [FingerType.THUMB]),
            'naturalistic': collect('multiple_intelligences', 'naturalistic', [FingerType.RING, FingerType.LITTLE]),
        }

        lobe_for_type = {
            FingerType.THUMB: 'prefrontal_lobe',
            FingerType.INDEX: 'posterior_frontal',
            FingerType.MIDDLE: 'parietal_lobe',
            FingerType.RING: 'temporal_lobe',
            FingerType.LITTLE: 'occipital_lobe',
        }
        grid: Dict[str, Dict[str, List[float]]] = {
            lobe: {'left': [], 'right': []} for lobe in lobe_for_type.values()
        }
        for res in individual_results:
            position = res['pipeline_info'].get('finger_position')
            hand, ftype = self._slot_hand_and_type(position)
            if hand is None or ftype is None:
                continue
            lobe_key = lobe_for_type.get(ftype)
            if lobe_key is None:
                continue
            capacity = res['dmit_analysis']['dmit_profile'].get('brain_mapping', {}).get(lobe_key)
            if not isinstance(capacity, (int, float)) or isinstance(capacity, bool):
                continue
            hemisphere = 'left' if hand == 'R' else 'right'
            grid[lobe_key][hemisphere].append(float(capacity))

        lobe_hemispheres: Dict[str, Dict[str, Optional[float]]] = {}
        agg_brain: Dict[str, Any] = {}
        for lobe_key, cells in grid.items():
            left = self._mean(cells['left'])
            right = self._mean(cells['right'])
            overall = self._mean([v for v in (left, right) if v is not None])
            lobe_hemispheres[lobe_key] = {'left': left, 'right': right}
            agg_brain[lobe_key] = overall

        left_cells = [v for cells in grid.values() for v in cells['left']]
        right_cells = [v for cells in grid.values() for v in cells['right']]
        left_hemisphere = self._mean(left_cells)
        right_hemisphere = self._mean(right_cells)
        agg_brain['left_hemisphere'] = left_hemisphere
        agg_brain['right_hemisphere'] = right_hemisphere
        agg_brain['lobe_hemispheres'] = lobe_hemispheres
        if left_hemisphere is not None and right_hemisphere is not None:
            if abs(left_hemisphere - right_hemisphere) < 0.05:
                agg_brain['dominant_hemisphere'] = 'balanced'
            else:
                agg_brain['dominant_hemisphere'] = 'left' if left_hemisphere > right_hemisphere else 'right'
        else:
            agg_brain['dominant_hemisphere'] = None

        agg_ls = {
            'visual': collect('learning_styles', 'visual', [FingerType.LITTLE, FingerType.INDEX]),
            'auditory': collect('learning_styles', 'auditory', [FingerType.RING]),
            'kinesthetic': collect('learning_styles', 'kinesthetic', [FingerType.MIDDLE]),
        }

        agg_pb = {
            trait: collect('personality_behavior', trait, [FingerType.THUMB])
            for trait in ('openness', 'conscientiousness', 'extraversion', 'agreeableness', 'neuroticism')
        }

        atd_analysis = self._build_atd_analysis(individual_results)

        # --- Holistic extension pass ---
        # FIX: previously the holistic pass fed extensions ONLY the aggregated MI
        # scores plus a single TFRC value. Extensions read ~40 biometric features
        # (ridge, fractal, graph, spectral, ...) via features.get(key, default),
        # so every aggregate extension score collapsed to default-driven values.
        # Now each numeric biometric feature is averaged across all successfully
        # analyzed fingers so extensions score from REAL measurements.
        feature_sums: Dict[str, float] = {}
        feature_counts: Dict[str, int] = {}
        pattern_family_votes: Dict[int, int] = {}
        for res in individual_results:
            consolidated = res['feature_extraction']['consolidated_features']
            for key, value in consolidated.items():
                if isinstance(value, bool) or not isinstance(value, (int, float)):
                    continue
                feature_sums[key] = feature_sums.get(key, 0.0) + float(value)
                feature_counts[key] = feature_counts.get(key, 0) + 1
            fam = consolidated.get('pattern_family')
            if fam is not None:
                try:
                    fam_int = int(fam)
                    pattern_family_votes[fam_int] = pattern_family_votes.get(fam_int, 0) + 1
                except (TypeError, ValueError):
                    pass

        holistic_features: Dict[str, Any] = {
            key: feature_sums[key] / feature_counts[key] for key in feature_sums
        }
        # Categorical features must not be averaged: use the dominant (modal)
        # pattern family across fingers instead of a meaningless mean of codes.
        if pattern_family_votes:
            holistic_features['pattern_family'] = float(
                max(pattern_family_votes.items(), key=lambda kv: kv[1])[0]
            )
        for key, value in agg_mi.items():
            if value is not None:
                holistic_features[key] = value
        holistic_features.update(self._hand_bilateral_features(individual_results))
        if atd_analysis is not None:
            for hand_key, prefix in (('right_hand', 'left'), ('left_hand', 'right')):
                hand_data = atd_analysis.get(hand_key)
                if hand_data:
                    holistic_features['atd_average_angle'] = hand_data['angle_deg']
                    break

        holistic_extensions = self.extension_engine.run_all_extensions(holistic_features)
        holistic_extensions = self._blend_holistic_extensions(
            holistic_extensions, agg_mi, agg_ls, agg_pb
        )

        final_profile = {
            'multiple_intelligences': agg_mi,
            'brain_mapping': agg_brain,
            'learning_styles': agg_ls,
            'personality_behavior': agg_pb,
            'atd_analysis': atd_analysis,
        }

        return {
            'pipeline_info': {
                'pipeline_version': self.pipeline_version,
                'total_fingers_analyzed': len(individual_results),
                'fingers_found': {k.value: len(v) for k, v in fingers_map.items()},
                'aggregation_timestamp': datetime.now().isoformat()
            },
            'individual_results': individual_results,
            'aggregated_analysis': {
                'dmit_profile': final_profile,
                'extension_results': holistic_extensions
            }
        }

    def _atd_hand(self, slot: str, hand: str, manual_angle: Optional[float]) -> Optional[Dict[str, Any]]:
        image_path = self._palm_images.get(slot)
        if image_path:
            estimate = self.palm_atd.estimate(image_path, hand=hand)
            if estimate is not None:
                mapped = map_atd_angle(estimate['angle_deg'])
                if mapped is not None:
                    mapped['method'] = 'geometric_landmark_estimate'
                    mapped['confidence'] = estimate['confidence']
                    mapped['source_note'] = (
                        'Estimated from palm hand geometry (segmentation + landmark angle), '
                        'not from ridge triradii. Treat as an approximation.'
                    )
                    return mapped

        mapped = map_atd_angle(manual_angle)
        if mapped is not None:
            mapped['method'] = 'manual_measurement'
            mapped['confidence'] = 1.0
            mapped['source_note'] = 'Manually entered atd angle.'
            return mapped
        return None

    def _build_atd_analysis(self, individual_results: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        meta = self.session_atd or {}
        left = self._atd_hand('LPALM', 'left', meta.get('atd_left_deg'))
        right = self._atd_hand('RPALM', 'right', meta.get('atd_right_deg'))
        if left is None and right is None:
            return None

        analysis: Dict[str, Any] = {'left_hand': left, 'right_hand': right}
        summary_parts = []

        # ── Per-hand summary ──────────────────────────────────────────────────
        if right is not None:
            summary_parts.append(
                f"Right palm ATD {right['angle_deg']}° → left-hemisphere processing "
                f"speed: {right['range_category']} range ({right['learning_speed']:.0%})."
            )
        if left is not None:
            summary_parts.append(
                f"Left palm ATD {left['angle_deg']}° → right-hemisphere processing "
                f"speed: {left['range_category']} range ({left['learning_speed']:.0%})."
            )

        # ── Bilateral asymmetry check ─────────────────────────────────────────
        if left is not None and right is not None:
            diff = abs(left['angle_deg'] - right['angle_deg'])
            if diff >= 8.0:
                dominant = "left" if right['angle_deg'] < left['angle_deg'] else "right"
                summary_parts.append(
                    f"Notable bilateral asymmetry: {diff:.1f}° difference between hands. "
                    f"The {dominant} hemisphere processes new information more quickly."
                )

        # ── Method disclaimer ─────────────────────────────────────────────────
        if any(h and h.get('method') == 'geometric_landmark_estimate' for h in (left, right)):
            summary_parts.append(
                "Note: angles are geometric landmark estimates from palm photographs, "
                "not ridge-triradius measurements. A ridge-grade palm scan is required "
                "for a clinical-standard ATD reading."
            )

        analysis['summary'] = " ".join(summary_parts) if summary_parts else None
        return analysis

    def generate_advanced_3d_pdf(self, analysis_results: Dict[str, Any], output_path: Optional[str] = None) -> str:
        """Wrapper for 3D PDF generation."""
        logger.info("🎨 Generating Advanced 3D Report...")
        if output_path is None:
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = f"output/scientific_reports/dmit_scientific_{ts}.pdf"
            
        # Ensure dir
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        
        try:
            path = create_3d_report(analysis_results, output_path=output_path)
            logger.info(f"✅ PDF Generated: {path}")
            return path
        except Exception as e:
            logger.exception(f"❌ PDF Gen Failed: {e}")
            raise

    def run_complete_pipeline(self, image_paths: List[str], generate_pdf: bool = True) -> Dict[str, Any]:
        """Run the full flow."""
        logger.info("🚀 SCIENTIFIC DMIT BATCH PROCESS START")
        res = self.analyze_multiple_fingers(image_paths)
        
        if generate_pdf:
            self.generate_advanced_3d_pdf(res)
            
        return res

def main():
    print("🔬 SCIENTIFIC DMIT PIPELINE 3.1")
    pipeline = IntegratedDMITPipeline()
    
    sample_dir = Path("sample data")
    if sample_dir.exists():
        images = list(sample_dir.glob("*.bmp"))
        if images:
            pipeline.run_complete_pipeline([str(p) for p in images])
            print("✅ Batch Complete.")
    else:
        print("❌ 'sample data' not found.")

if __name__ == "__main__":
    main()