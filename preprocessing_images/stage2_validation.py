#!/usr/bin/env python3
"""
🔹 STAGE 2: FINGER SHAPE VALIDATION
===================================
Validates that segmented region is actually a finger using geometry only.

Checks:
- Aspect ratio (length >> width)
- Convexity (finger is mostly convex)
- Skeleton continuity (single continuous axis)
- Low curvature variance along axis

Returns confidence score, never crashes.

NO ML - Pure geometry.

Author: DMIT Research Team
Version: 1.0
"""

import cv2
import numpy as np
from typing import Tuple, Dict, Any
import logging

logger = logging.getLogger(__name__)


class ShapeValidator:
    """
    Geometric validation that segmented region is a finger.
    
    Prevents false positives by checking:
    - Shape must be elongated
    - Shape must be mostly convex
    - Skeleton must be continuous
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        """
        Initialize validator with configuration.
        
        Args:
            config: Configuration dictionary with:
                - min_aspect_ratio: Minimum length/width ratio (default: 2.0)
                - max_aspect_ratio: Maximum length/width ratio (default: 6.0)
                - min_convexity: Minimum convexity score (default: 0.7)
                - min_confidence: Minimum overall confidence (default: 0.5)
        """
        self.config = config or {}
        self.min_aspect_ratio = self.config.get('min_aspect_ratio', 2.0)
        self.max_aspect_ratio = self.config.get('max_aspect_ratio', 6.0)
        self.min_convexity = self.config.get('min_convexity', 0.7)
        self.min_confidence = self.config.get('min_confidence', 0.5)
    
    def validate(self, segmented: np.ndarray, mask: np.ndarray) -> Tuple[bool, float, Dict[str, Any]]:
        """
        Validate that segmented region is a finger.
        
        Args:
            segmented: Segmented finger image (grayscale)
            mask: Binary mask of finger region
            
        Returns:
            Tuple of:
            - is_valid: Boolean indicating valid finger shape
            - confidence: Confidence score (0.0-1.0)
            - metadata: Validation details
        """
        metadata = {
            'input_shape': segmented.shape,
            'checks': {}
        }
        
        try:
            h, w = segmented.shape[:2]
            
            # ===== Check 1: Aspect Ratio =====
            aspect_ratio = h / w if w > 0 else 0
            aspect_valid = self.min_aspect_ratio <= aspect_ratio <= self.max_aspect_ratio
            
            # Score: 1.0 at ideal (3.0), lower otherwise
            ideal_aspect = 3.0
            aspect_score = 1.0 - min(1.0, abs(aspect_ratio - ideal_aspect) / 2.0)
            
            metadata['checks']['aspect_ratio'] = {
                'value': float(aspect_ratio),
                'valid': aspect_valid,
                'score': float(aspect_score)
            }
            
            # ===== Check 2: Convexity =====
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            if contours:
                largest_contour = max(contours, key=cv2.contourArea)
                area = cv2.contourArea(largest_contour)
                hull = cv2.convexHull(largest_contour)
                hull_area = cv2.contourArea(hull)
                
                convexity = area / hull_area if hull_area > 0 else 0
                convexity_valid = convexity >= self.min_convexity
                convexity_score = min(1.0, convexity / 0.9)  # Perfect at 0.9+
            else:
                convexity = 0
                convexity_valid = False
                convexity_score = 0
                largest_contour = None
            
            metadata['checks']['convexity'] = {
                'value': float(convexity),
                'valid': convexity_valid,
                'score': float(convexity_score)
            }
            
            # ===== Check 3: Skeleton Continuity =====
            skeleton = self._compute_skeleton(mask)
            skeleton_continuous, skeleton_score, skeleton_meta = self._check_skeleton_continuity(skeleton)
            
            metadata['checks']['skeleton_continuity'] = {
                'continuous': skeleton_continuous,
                'score': float(skeleton_score),
                **skeleton_meta
            }
            
            # ===== Check 4: Curvature Variance =====
            if largest_contour is not None:
                curvature_score, curvature_meta = self._check_curvature_variance(largest_contour)
            else:
                curvature_score = 0
                curvature_meta = {}
            
            metadata['checks']['curvature_variance'] = {
                'score': float(curvature_score),
                **curvature_meta
            }
            
            # ===== Calculate Overall Confidence =====
            # Weighted combination of all checks
            confidence = (
                aspect_score * 0.30 +
                convexity_score * 0.25 +
                skeleton_score * 0.25 +
                curvature_score * 0.20
            )
            
            is_valid = confidence >= self.min_confidence
            
            metadata['confidence'] = float(confidence)
            metadata['is_valid'] = is_valid
            
            if is_valid:
                logger.info(f"✓ Validation passed (confidence: {confidence:.2f})")
            else:
                logger.warning(f"✗ Validation failed (confidence: {confidence:.2f})")
            
            return is_valid, confidence, metadata
            
        except Exception as e:
            logger.error(f"Validation failed: {e}")
            metadata['error'] = str(e)
            return False, 0.0, metadata
    
    def _compute_skeleton(self, mask: np.ndarray) -> np.ndarray:
        """
        Compute morphological skeleton of the mask.
        
        Uses iterative thinning to get centerline.
        """
        # Ensure binary mask
        _, binary = cv2.threshold(mask, 127, 255, cv2.THRESH_BINARY)
        
        # Skeletonization using morphological operations
        skeleton = np.zeros_like(binary)
        temp = binary.copy()
        kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))
        
        while True:
            eroded = cv2.erode(temp, kernel)
            dilated = cv2.dilate(eroded, kernel)
            subset = cv2.subtract(temp, dilated)
            skeleton = cv2.bitwise_or(skeleton, subset)
            temp = eroded.copy()
            
            if cv2.countNonZero(temp) == 0:
                break
        
        return skeleton
    
    def _check_skeleton_continuity(self, skeleton: np.ndarray) -> Tuple[bool, float, Dict[str, Any]]:
        """
        Check if skeleton is a single continuous axis.
        
        Good finger: single skeleton with few branches
        Bad: fragmented or many branches
        """
        # Find skeleton contours
        contours, _ = cv2.findContours(skeleton, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        num_components = len(contours)
        
        if num_components == 0:
            return False, 0.0, {'num_components': 0}
        
        # Count skeleton endpoints and branch points
        skeleton_points = np.sum(skeleton > 0)
        
        # Good skeleton: mostly linear, few branches
        if num_components == 1 and skeleton_points > 50:
            score = 1.0
            continuous = True
        elif num_components <= 3:
            score = 0.7
            continuous = True
        else:
            score = max(0.2, 1.0 - num_components * 0.1)
            continuous = False
        
        return continuous, score, {
            'num_components': num_components,
            'skeleton_points': int(skeleton_points)
        }
    
    def _check_curvature_variance(self, contour: np.ndarray) -> Tuple[float, Dict[str, Any]]:
        """
        Check curvature variance along finger axis.
        
        Fingers have low, consistent curvature along sides.
        """
        if len(contour) < 10:
            return 0.0, {'contour_points': len(contour)}
        
        # Approximate contour to reduce noise
        epsilon = 0.01 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)
        
        if len(approx) < 5:
            return 0.5, {'contour_points': len(contour), 'approx_points': len(approx)}
        
        # Calculate curvature at each point
        curvatures = []
        points = approx.squeeze()
        
        for i in range(len(points)):
            p1 = points[i - 1]
            p2 = points[i]
            p3 = points[(i + 1) % len(points)]
            
            # Vectors
            v1 = p1 - p2
            v2 = p3 - p2
            
            # Angle between vectors (curvature proxy)
            dot = np.dot(v1, v2)
            mag1 = np.linalg.norm(v1)
            mag2 = np.linalg.norm(v2)
            
            if mag1 > 0 and mag2 > 0:
                cos_angle = dot / (mag1 * mag2)
                cos_angle = np.clip(cos_angle, -1, 1)
                angle = np.arccos(cos_angle)
                curvatures.append(angle)
        
        if not curvatures:
            return 0.5, {'contour_points': len(contour)}
        
        # Low variance = consistent curvature = good
        curvature_var = np.var(curvatures)
        curvature_mean = np.mean(curvatures)
        
        # Score: lower variance is better (fingers have smooth sides)
        score = 1.0 / (1.0 + curvature_var * 5)
        
        return score, {
            'curvature_variance': float(curvature_var),
            'curvature_mean': float(curvature_mean),
            'num_curvature_samples': len(curvatures)
        }
