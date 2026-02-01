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
import cv2

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Import core pipeline components
try:
    from optimized_feature_extractor_clean import OptimizedFeatureExtractor
    from dmit_intelligence_mapper import (
        map_features_to_dmit_profile, 
        FingerType, 
        BrainLobe,
        create_bulletproof_dmit_analysis
    )
    from advanced_3d_pdf_generator import create_3d_report
    logger.info("✅ All core components imported successfully")
except ImportError as e:
    logger.error(f"❌ Failed to import core components: {e}")
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
    
    def __init__(self):
        self.feature_extractor = OptimizedFeatureExtractor()
        self.pipeline_version = "3.1-Scientific"
        self.start_time = datetime.now()
        
        logger.info(f"🚀 Integrated DMIT Pipeline v{self.pipeline_version} initialized")
        logger.info("✅ Scientific Mapping (Table 1.1) enabled")
    
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
        name = filename.lower()
        
        # Check standard numeric suffixes
        if any(x in name for x in ['_00', '_05', '_l1', '_r1', 'thumb']):
            return FingerType.THUMB
        elif any(x in name for x in ['_01', '_06', '_l2', '_r2', 'index']):
            return FingerType.INDEX
        elif any(x in name for x in ['_02', '_07', '_l3', '_r3', 'middle']):
            return FingerType.MIDDLE
        elif any(x in name for x in ['_03', '_08', '_l4', '_r4', 'ring']):
            return FingerType.RING
        elif any(x in name for x in ['_04', '_09', '_l5', '_r5', 'little']):
            return FingerType.LITTLE
            
        logger.warning(f"⚠️ Could not identify finger type for {filename}, defaulting to UNKNOWN")
        return FingerType.UNKNOWN

    def analyze_single_finger(self, image_path: str) -> Dict[str, Any]:
        """
        Analyze a single fingerprint image with real feature extraction and scientific mapping.
        """
        logger.info(f"🔍 Analyzing single finger: {image_path}")
        
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image not found: {image_path}")
        
        image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        if image is None:
            raise ValueError(f"Failed to load image: {image_path}")
            
        # 1. Identify Finger
        finger_type = self._identify_finger_type(os.path.basename(image_path))
        logger.info(f"🖐️ Identified Finger: {finger_type.value.upper()}")
        
        # 2. Extract Features
        extractor_result = self.feature_extractor.extract_optimized_features(image)
        features = extractor_result['consolidated_features']
        
        # 3. Create DMIT Profile (Scientific Mapping)
        # Note: Validating strictly via Mapper
        dmit_profile = map_features_to_dmit_profile(features, finger_type_str=finger_type.value)
        
        # 4. Compile Results
        results = {
            'pipeline_info': {
                'image_path': image_path,
                'finger_type': finger_type.value,
                'timestamp': datetime.now().isoformat()
            },
            'feature_extraction': extractor_result,
            'dmit_analysis': {
                'dmit_profile': dmit_profile,
                # Add placeholders for compatibility if needed
            }
        }
        
        return results

    def analyze_multiple_fingers(self, image_paths: List[str]) -> Dict[str, Any]:
        """
        Analyze multiple fingers and aggregate using Scientific Weighted Slots.
        """
        logger.info(f"🔍 Analyzing {len(image_paths)} fingers...")
        
        individual_results = []
        successful_analyses = 0
        
        for i, path in enumerate(image_paths, 1):
            try:
                res = self.analyze_single_finger(path)
                individual_results.append(res)
                successful_analyses += 1
            except Exception as e:
                logger.error(f"❌ Failed to analyze {path}: {e}")
                
        if successful_analyses == 0:
            raise ValueError("No fingers successfully analyzed")
            
        # Aggregation
        aggregated_results = self._aggregate_results_scientifically(individual_results)
        
        logger.info(f"✅ Analysis Complete. Success: {successful_analyses}/{len(image_paths)}")
        return aggregated_results

    def _aggregate_results_scientifically(self, individual_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Aggregate results using strict Finger-Brain correlations.
        We group results by Finger Type and calculate specific traits from specific groups.
        """
        # Group by Finger Type
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
            except:
                f_type = FingerType.UNKNOWN
            
            fingers_map[f_type].append(res['dmit_analysis']['dmit_profile'])

        # --- Helper for Averaging ---
        def get_avg_score(category: str, key: str, source_fingers: List[FingerType]) -> float:
            total = 0.0
            count = 0
            
            # Collect valid profiles
            source_profiles = []
            for ft in source_fingers:
                source_profiles.extend(fingers_map[ft])
            
            # If no primary fingers found, fallback to ALL fingers (Average fallback)
            if not source_profiles:
                # Fallback: use all available profiles
                for vals in fingers_map.values():
                    source_profiles.extend(vals)
            
            if not source_profiles:
                return 0.0
                
            for prof in source_profiles:
                val = prof.get(category, {}).get(key, 0.0)
                total += val
                count += 1
            
            return total / count if count > 0 else 0.0

        # --- Aggregate: Multiple Intelligences ---
        agg_mi = {}
        
        # Scientific Table 1.1 Mappings for Aggregation:
        # Logical -> Index (Posterior Frontal)
        agg_mi['logical_mathematical'] = get_avg_score('multiple_intelligences', 'logical_mathematical', [FingerType.INDEX])
        
        # Linguistic -> Ring (Temporal)
        agg_mi['linguistic'] = get_avg_score('multiple_intelligences', 'linguistic', [FingerType.RING])
        
        # Musical -> Ring (Temporal)
        agg_mi['musical'] = get_avg_score('multiple_intelligences', 'musical', [FingerType.RING])
        
        # Spatial -> Little (Visual/Occipital) + Index (Spatial/Frontal)
        agg_mi['spatial'] = get_avg_score('multiple_intelligences', 'spatial', [FingerType.LITTLE, FingerType.INDEX])
        
        # Bodily-Kinesthetic -> Middle (Parietal)
        agg_mi['bodily_kinesthetic'] = get_avg_score('multiple_intelligences', 'bodily_kinesthetic', [FingerType.MIDDLE])
        
        # Inter/Intra Personal -> Thumb (Prefrontal)
        agg_mi['interpersonal'] = get_avg_score('multiple_intelligences', 'interpersonal', [FingerType.THUMB])
        agg_mi['intrapersonal'] = get_avg_score('multiple_intelligences', 'intrapersonal', [FingerType.THUMB])
        
        # Naturalistic -> Ring + Little (Pattern + Visual)
        agg_mi['naturalistic'] = get_avg_score('multiple_intelligences', 'naturalistic', [FingerType.RING, FingerType.LITTLE])
        
        # Existential (if present) -> Thumb
        agg_mi['existential'] = get_avg_score('multiple_intelligences', 'existential', [FingerType.THUMB])

        # --- Aggregate: Brain Lobes ---
        # The Mapper already applies penalties to non-primary lobes. 
        # So effectively, "Index" finger gives a HIGH Posterior Frontal score, and others give LOW (0.2x).
        # If we just averaged all 10 fingers, the 8 "low" fingers would drag down the 2 "high" fingers.
        # So we must ONLY take the score from the Primary Finger for that lobe.
        
        agg_brain = {}
        agg_brain['prefrontal_lobe'] = get_avg_score('brain_mapping', 'prefrontal_lobe', [FingerType.THUMB])
        agg_brain['posterior_frontal'] = get_avg_score('brain_mapping', 'posterior_frontal', [FingerType.INDEX])
        agg_brain['parietal_lobe'] = get_avg_score('brain_mapping', 'parietal_lobe', [FingerType.MIDDLE])
        agg_brain['temporal_lobe'] = get_avg_score('brain_mapping', 'temporal_lobe', [FingerType.RING])
        agg_brain['occipital_lobe'] = get_avg_score('brain_mapping', 'occipital_lobe', [FingerType.LITTLE])
        
        # Hemispheres (Left/Right) - Average of all
        agg_brain['left_hemisphere_bias'] = get_avg_score('brain_mapping', 'left_hemisphere_bias', [FingerType.THUMB, FingerType.INDEX, FingerType.MIDDLE, FingerType.RING, FingerType.LITTLE])
        agg_brain['right_hemisphere_bias'] = get_avg_score('brain_mapping', 'right_hemisphere_bias', [FingerType.THUMB, FingerType.INDEX, FingerType.MIDDLE, FingerType.RING, FingerType.LITTLE])

        # --- Aggregate: Learning Styles ---
        # Visual -> Little + Index
        # Auditory -> Ring
        # Kinesthetic -> Middle
        agg_ls = {}
        agg_ls['visual'] = get_avg_score('learning_styles', 'visual', [FingerType.LITTLE, FingerType.INDEX])
        agg_ls['auditory'] = get_avg_score('learning_styles', 'auditory', [FingerType.RING])
        agg_ls['kinesthetic'] = get_avg_score('learning_styles', 'kinesthetic', [FingerType.MIDDLE])

        # --- Aggregate: Personality ---
        # Almost entirely Prefrontal (Thumb)
        agg_pb = {}
        for trait in ['openness', 'conscientiousness', 'extraversion', 'agreeableness', 'neuroticism']:
            agg_pb[trait] = get_avg_score('personality_behavior', trait, [FingerType.THUMB])

        # Construct Final Profile
        final_profile = {
            'multiple_intelligences': agg_mi,
            'brain_mapping': agg_brain,
            'learning_styles': agg_ls,
            'personality_behavior': agg_pb
        }
        
        return {
            'pipeline_info': {
                'pipeline_version': self.pipeline_version,
                'total_fingers_analyzed': len(individual_results),
                'fingers_found': {k.value: len(v) for k,v in fingers_map.items()},
                'aggregation_timestamp': datetime.now().isoformat()
            },
            'individual_results': individual_results,
            'aggregated_analysis': {
                'dmit_profile': final_profile
            }
        }

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
            logger.error(f"❌ PDF Gen Failed: {e}")
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