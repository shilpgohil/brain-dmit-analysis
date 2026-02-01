#!/usr/bin/env python3
"""
🎯 FINGER TO FINGERPRINT PIPELINE
=================================
Main orchestrator for the 5-stage preprocessing pipeline.

Author: DMIT Research Team
Version: 1.0
"""

import cv2
import numpy as np
import logging
from pathlib import Path
from typing import Dict, Any, Optional, Tuple
from datetime import datetime

from .stage1_segmentation import FingerSegmenter
from .stage2_validation import ShapeValidator
from .stage3_roi_detection import FingertipROIDetector
from .stage4_nail_removal import NailRemover
from .stage5_ridge_enhancement import RidgeEnhancer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FingerToFingerprintPipeline:
    """
    Complete pipeline to convert any finger image to standardized fingerprint.
    
    Stages:
    1. Color-agnostic finger segmentation
    2. Shape-based finger validation
    3. Fingertip & ROI detection
    4. Nail removal
    5. Ridge enhancement
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        """
        Initialize pipeline with optional configuration.
        
        Args:
            config: Optional configuration dictionary
        """
        self.config = config or self._default_config()
        
        # Initialize all stages
        self.segmenter = FingerSegmenter(self.config.get('segmentation', {}))
        self.validator = ShapeValidator(self.config.get('validation', {}))
        self.roi_detector = FingertipROIDetector(self.config.get('roi_detection', {}))
        self.nail_remover = NailRemover(self.config.get('nail_removal', {}))
        self.ridge_enhancer = RidgeEnhancer(self.config.get('ridge_enhancement', {}))
        
        logger.info("🖐️ Finger-to-Fingerprint Pipeline initialized")
    
    def _default_config(self) -> Dict[str, Any]:
        """Default configuration for all stages."""
        return {
            'segmentation': {
                'canny_low': 50,
                'canny_high': 150,
                'morph_kernel_size': 5,
                'min_finger_area_ratio': 0.05
            },
            'validation': {
                'min_aspect_ratio': 2.0,
                'max_aspect_ratio': 6.0,
                'min_convexity': 0.7,
                'min_confidence': 0.5
            },
            'roi_detection': {
                'fingerprint_region_ratio': 0.25,  # Top 25% of finger
                'roi_width_ratio': 0.8
            },
            'nail_removal': {
                'smoothness_threshold': 0.3,
                'nail_region_ratio': 0.15
            },
            'ridge_enhancement': {
                'clahe_clip_limit': 2.0,
                'clahe_tile_size': 8,
                'gabor_frequencies': [0.1, 0.15, 0.2],
                'gabor_orientations': 8
            }
        }
    
    def process(self, input_path: str, output_path: str = None) -> Dict[str, Any]:
        """
        Process a finger image through all 5 stages.
        
        Args:
            input_path: Path to input finger image
            output_path: Optional path to save output
            
        Returns:
            Dictionary containing:
            - 'fingerprint': Processed fingerprint image (grayscale)
            - 'confidence': Overall confidence score (0.0-1.0)
            - 'metadata': Processing details from each stage
            - 'success': Boolean indicating success
        """
        start_time = datetime.now()
        logger.info(f"📸 Processing: {input_path}")
        
        result = {
            'fingerprint': None,
            'confidence': 0.0,
            'metadata': {},
            'success': False,
            'stages_completed': []
        }
        
        try:
            # Load image
            image = cv2.imread(str(input_path))
            if image is None:
                raise ValueError(f"Failed to load image: {input_path}")
            
            result['metadata']['input_shape'] = image.shape
            result['metadata']['input_path'] = str(input_path)
            
            # ===== STAGE 1: Finger Segmentation =====
            logger.info("🔹 Stage 1: Finger Segmentation")
            segmented, seg_mask, seg_meta = self.segmenter.segment(image)
            result['metadata']['stage1_segmentation'] = seg_meta
            result['stages_completed'].append('segmentation')
            
            if segmented is None:
                logger.warning("⚠️ Segmentation failed - no finger detected")
                result['metadata']['failure_stage'] = 'segmentation'
                return result
            
            # ===== STAGE 2: Shape Validation =====
            logger.info("🔹 Stage 2: Shape Validation")
            is_valid, validation_confidence, val_meta = self.validator.validate(
                segmented, seg_mask
            )
            result['metadata']['stage2_validation'] = val_meta
            result['stages_completed'].append('validation')
            
            if not is_valid:
                logger.warning(f"⚠️ Shape validation failed (confidence: {validation_confidence:.2f})")
                result['confidence'] = validation_confidence
                result['metadata']['failure_stage'] = 'validation'
                # Continue anyway with low confidence rather than failing completely
            
            # ===== STAGE 3: Fingertip & ROI Detection =====
            logger.info("🔹 Stage 3: Fingertip & ROI Detection")
            roi, roi_meta = self.roi_detector.detect(segmented, seg_mask)
            result['metadata']['stage3_roi_detection'] = roi_meta
            result['stages_completed'].append('roi_detection')
            
            if roi is None:
                logger.warning("⚠️ ROI detection failed - using full segmented region")
                roi = segmented
            
            # ===== STAGE 4: Nail Removal =====
            logger.info("🔹 Stage 4: Nail Removal")
            cleaned, nail_meta = self.nail_remover.remove(roi)
            result['metadata']['stage4_nail_removal'] = nail_meta
            result['stages_completed'].append('nail_removal')
            
            # ===== STAGE 5: Ridge Enhancement =====
            logger.info("🔹 Stage 5: Ridge Enhancement")
            enhanced, enhance_meta = self.ridge_enhancer.enhance(cleaned)
            result['metadata']['stage5_ridge_enhancement'] = enhance_meta
            result['stages_completed'].append('ridge_enhancement')
            
            # Final result
            result['fingerprint'] = enhanced
            result['success'] = True
            
            # Calculate overall confidence
            confidences = [
                seg_meta.get('confidence', 0.5),
                val_meta.get('confidence', validation_confidence),
                roi_meta.get('confidence', 0.5),
                nail_meta.get('confidence', 0.8),
                enhance_meta.get('confidence', 0.8)
            ]
            result['confidence'] = np.mean(confidences)
            
            # Save output if requested
            if output_path:
                cv2.imwrite(str(output_path), enhanced)
                result['metadata']['output_path'] = str(output_path)
                logger.info(f"💾 Saved to: {output_path}")
            
            # Processing time
            elapsed = (datetime.now() - start_time).total_seconds()
            result['metadata']['processing_time_seconds'] = elapsed
            
            logger.info(f"✅ Processing complete (confidence: {result['confidence']:.2f}, time: {elapsed:.2f}s)")
            
        except Exception as e:
            logger.error(f"❌ Pipeline failed: {e}")
            result['metadata']['error'] = str(e)
            result['success'] = False
        
        return result
    
    def process_image(self, image: np.ndarray) -> Dict[str, Any]:
        """
        Process a numpy image directly (no file I/O).
        
        Args:
            image: Input image as numpy array (BGR or grayscale)
            
        Returns:
            Same structure as process()
        """
        # Create a temporary result structure
        result = {
            'fingerprint': None,
            'confidence': 0.0,
            'metadata': {'input_shape': image.shape},
            'success': False,
            'stages_completed': []
        }
        
        try:
            # Stage 1
            segmented, seg_mask, seg_meta = self.segmenter.segment(image)
            result['metadata']['stage1_segmentation'] = seg_meta
            result['stages_completed'].append('segmentation')
            
            if segmented is None:
                return result
            
            # Stage 2
            is_valid, validation_confidence, val_meta = self.validator.validate(
                segmented, seg_mask
            )
            result['metadata']['stage2_validation'] = val_meta
            result['stages_completed'].append('validation')
            
            # Stage 3
            roi, roi_meta = self.roi_detector.detect(segmented, seg_mask)
            result['metadata']['stage3_roi_detection'] = roi_meta
            result['stages_completed'].append('roi_detection')
            
            if roi is None:
                roi = segmented
            
            # Stage 4
            cleaned, nail_meta = self.nail_remover.remove(roi)
            result['metadata']['stage4_nail_removal'] = nail_meta
            result['stages_completed'].append('nail_removal')
            
            # Stage 5
            enhanced, enhance_meta = self.ridge_enhancer.enhance(cleaned)
            result['metadata']['stage5_ridge_enhancement'] = enhance_meta
            result['stages_completed'].append('ridge_enhancement')
            
            result['fingerprint'] = enhanced
            result['success'] = True
            result['confidence'] = np.mean([
                seg_meta.get('confidence', 0.5),
                val_meta.get('confidence', 0.5),
                roi_meta.get('confidence', 0.5),
                nail_meta.get('confidence', 0.8),
                enhance_meta.get('confidence', 0.8)
            ])
            
        except Exception as e:
            result['metadata']['error'] = str(e)
        
        return result
