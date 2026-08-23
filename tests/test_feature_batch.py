#!/usr/bin/env python3
"""
TEST: FEATURE EXTRACTION BATCH
==============================
Processes the 10 finger prints in the 'sample data' directory
specifically for the feature extraction part of the pipeline.
"""

import os
import sys
import logging
from pathlib import Path
from typing import Dict, List, Any
import json
import cv2
import numpy as np
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Import required components
try:
    from optimized_feature_extractor_clean import OptimizedFeatureExtractor
    from dmit_intelligence_mapper import FingerType
    logger.info("✅ Core components imported successfully")
except ImportError as e:
    logger.error(f"❌ Failed to import core components: {e}")
    sys.exit(1)

class FeatureExtractionTester:
    def __init__(self):
        self.extractor = OptimizedFeatureExtractor()
        logger.info("🚀 Optimized Feature Extractor initialized")

    def _identify_finger_type(self, filename: str) -> FingerType:
        """Identify finger type from filename suffix (copying pipeline logic)."""
        name = filename.lower()
        if any(x in name for x in ['_00', '_05', 'l1', 'r1', 'thumb']):
            return FingerType.THUMB
        elif any(x in name for x in ['_01', '_06', 'l2', 'r2', 'index']):
            return FingerType.INDEX
        elif any(x in name for x in ['_02', '_07', 'l3', 'r3', 'middle']):
            return FingerType.MIDDLE
        elif any(x in name for x in ['_03', '_08', 'l4', 'r4', 'ring']):
            return FingerType.RING
        elif any(x in name for x in ['_04', '_09', 'l5', 'r5', 'little']):
            return FingerType.LITTLE
        return FingerType.UNKNOWN

    def test_batch(self, sample_dir: str):
        path = Path(sample_dir)
        if not path.exists():
            logger.error(f"❌ Sample directory not found: {sample_dir}")
            return

        image_files = sorted(list(path.glob("*.bmp")))
        if not image_files:
            logger.info(f"❓ No .bmp files found in {sample_dir}")
            return

        logger.info(f"🔍 Found {len(image_files)} images to process")
        
        results = []
        for img_path in image_files:
            try:
                logger.info(f"--- Processing: {img_path.name} ---")
                
                # 1. Load Image
                image = cv2.imread(str(img_path), cv2.IMREAD_GRAYSCALE)
                if image is None:
                    logger.error(f"❌ Failed to load image: {img_path}")
                    continue

                # 2. Identify Finger
                finger_type = self._identify_finger_type(img_path.name)
                logger.info(f"🖐️ Identified Finger: {finger_type.value.upper()}")

                # 3. Extract Features
                extraction_result = self.extractor.extract_optimized_features(image)
                
                # 4. Summarize
                features = extraction_result.get('consolidated_features', {})
                summary = {
                    'filename': img_path.name,
                    'finger_type': finger_type.value,
                    'quality_score': extraction_result.get('extraction_summary', {}).get('image_quality_score', 0),
                    'pattern_family': features.get('pattern_family', 'N/A'),
                    'entropy': round(features.get('entropy', 0), 4),
                    'whorl_score': round(features.get('whorl_logical_layering_score', 0), 4),
                    'ridge_density': round(features.get('ridge_density', 0), 4),
                    'extracted_at': datetime.now().isoformat()
                }
                
                results.append({
                    'summary': summary,
                    'all_features': features
                })
                
                logger.info(f"✅ Success: Quality={summary['quality_score']:.2f}, Pattern={summary['pattern_family']}")

            except Exception as e:
                logger.error(f"❌ Error processing {img_path.name}: {e}")

        # Save results
        output_file = "feature_extraction_results.json"
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=4)
        
        logger.info(f"\n📊 Batch complete. Results saved to {output_file}")
        return results

def main():
    tester = FeatureExtractionTester()
    tester.test_batch("sample data")

if __name__ == "__main__":
    main()
