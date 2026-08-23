#!/usr/bin/env python3
"""
🖐️ PREPROCESSING IMAGES MODULE
==============================
Converts any finger image (any color, any background) to a standardized 
fingerprint ready for DMIT feature extraction.

5-Stage Pipeline:
1. Color-Agnostic Finger Segmentation
2. Finger Shape Validation (geometry only)
3. Fingertip & Fingerprint ROI Detection
4. Nail Removal
5. Ridge Enhancement (classical, proven)

NO MACHINE LEARNING - Pure computer vision & geometry.

Author: DMIT Research Team
Version: 1.0
"""

from .pipeline import FingerToFingerprintPipeline
from .stage1_segmentation import FingerSegmenter
from .stage2_validation import ShapeValidator
from .stage3_roi_detection import FingertipROIDetector
from .stage4_nail_removal import NailRemover
from .stage5_ridge_enhancement import RidgeEnhancer

__all__ = [
    'FingerToFingerprintPipeline',
    'FingerSegmenter',
    'ShapeValidator', 
    'FingertipROIDetector',
    'NailRemover',
    'RidgeEnhancer',
    'convert_finger_to_fingerprint'
]

def convert_finger_to_fingerprint(image_path: str, output_path: str = None) -> dict:
    """
    Convenience function to convert any finger image to fingerprint.
    
    Args:
        image_path: Path to input finger image (any format, color, background)
        output_path: Optional path to save processed fingerprint
        
    Returns:
        dict with 'fingerprint' (processed image), 'confidence', 'metadata'
    """
    pipeline = FingerToFingerprintPipeline()
    return pipeline.process(image_path, output_path)
