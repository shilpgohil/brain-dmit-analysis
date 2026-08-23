#!/usr/bin/env python3
"""
🔹 STAGE 3: FINGERTIP & FINGERPRINT ROI DETECTION
=================================================
Locates the fingertip and extracts the fingerprint-bearing region.

Steps:
1. Compute finger skeleton
2. Find fingertip endpoint (max distance from centroid + highest curvature)
3. Compute finger axis
4. Crop top 20-30% of finger length (fingerprint pad region)

Geometry-only, extremely robust.

Author: DMIT Research Team
Version: 1.0
"""

import cv2
import numpy as np
from typing import Tuple, Dict, Any, Optional, List
import logging

logger = logging.getLogger(__name__)


class FingertipROIDetector:
    """
    Detects fingertip and extracts fingerprint ROI using pure geometry.
    
    The fingerprint is located on the palmar surface of the fingertip,
    approximately the top 20-30% of the finger length.
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        """
        Initialize detector with configuration.
        
        Args:
            config: Configuration dictionary with:
                - fingerprint_region_ratio: Top portion of finger (default: 0.25)
                - roi_width_ratio: Width ratio of ROI (default: 0.8)
        """
        self.config = config or {}
        self.fingerprint_region_ratio = self.config.get('fingerprint_region_ratio', 0.25)
        self.roi_width_ratio = self.config.get('roi_width_ratio', 0.8)
    
    def detect(self, segmented: np.ndarray, mask: np.ndarray) -> Tuple[Optional[np.ndarray], Dict[str, Any]]:
        """
        Detect fingertip and extract fingerprint ROI.
        
        Args:
            segmented: Segmented finger image (grayscale)
            mask: Binary mask of finger region
            
        Returns:
            Tuple of:
            - roi: Extracted fingerprint region (grayscale)
            - metadata: Detection details
        """
        metadata = {
            'input_shape': segmented.shape,
            'confidence': 0.0
        }
        
        try:
            h, w = segmented.shape[:2]
            
            # Step 1: Compute skeleton
            skeleton = self._compute_skeleton(mask)
            
            # Step 2: Find skeleton endpoints
            endpoints = self._find_skeleton_endpoints(skeleton)
            
            if len(endpoints) < 1:
                logger.warning("No skeleton endpoints found, using top region")
                return self._fallback_roi(segmented, mask, metadata)
            
            # Step 3: Find fingertip (endpoint closest to top of image)
            # Assume finger is roughly vertical with tip at top
            fingertip = min(endpoints, key=lambda p: p[1])  # Smallest y = topmost
            
            metadata['fingertip_location'] = (int(fingertip[0]), int(fingertip[1]))
            
            # Step 4: Compute finger axis
            centroid = self._compute_centroid(mask)
            if centroid is None:
                return self._fallback_roi(segmented, mask, metadata)
            
            metadata['centroid'] = (int(centroid[0]), int(centroid[1]))
            
            # Finger axis: from centroid towards fingertip
            axis_vector = fingertip - centroid
            axis_length = np.linalg.norm(axis_vector)
            
            if axis_length < 10:
                return self._fallback_roi(segmented, mask, metadata)
            
            axis_unit = axis_vector / axis_length
            
            # Step 5: Calculate ROI boundaries
            # Fingerprint region: from fingertip, going down 25-30% of finger
            roi_length = int(h * self.fingerprint_region_ratio)
            roi_width = int(w * self.roi_width_ratio)
            
            # Center ROI on fingertip
            roi_top = max(0, int(fingertip[1]))
            roi_bottom = min(h, roi_top + roi_length)
            roi_left = max(0, int(fingertip[0] - roi_width // 2))
            roi_right = min(w, roi_left + roi_width)
            
            # Ensure minimum size
            if (roi_bottom - roi_top) < 50 or (roi_right - roi_left) < 30:
                return self._fallback_roi(segmented, mask, metadata)
            
            # Extract ROI
            roi = segmented[roi_top:roi_bottom, roi_left:roi_right].copy()
            roi_mask = mask[roi_top:roi_bottom, roi_left:roi_right]
            
            # NOTE: Do NOT apply destructive masking!
            # Pixel values are preserved; mask is for reference only.
            
            # Calculate confidence
            roi_area = np.sum(roi_mask > 0)
            total_roi_area = roi.shape[0] * roi.shape[1]
            fill_ratio = roi_area / total_roi_area if total_roi_area > 0 else 0
            
            confidence = min(1.0, fill_ratio * 1.5)  # 66% fill = full confidence
            
            metadata.update({
                'roi_bounds': (roi_top, roi_bottom, roi_left, roi_right),
                'roi_shape': roi.shape,
                'fill_ratio': float(fill_ratio),
                'confidence': float(confidence),
                'method': 'skeleton_based'
            })
            
            logger.info(f"✓ ROI detected: {roi.shape}, confidence: {confidence:.2f}")
            
            return roi, metadata
            
        except Exception as e:
            logger.error(f"ROI detection failed: {e}")
            metadata['error'] = str(e)
            return self._fallback_roi(segmented, mask, metadata)
    
    def _compute_skeleton(self, mask: np.ndarray) -> np.ndarray:
        """Compute morphological skeleton using iterative thinning."""
        _, binary = cv2.threshold(mask, 127, 255, cv2.THRESH_BINARY)
        
        skeleton = np.zeros_like(binary)
        temp = binary.copy()
        kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))
        
        iterations = 0
        max_iterations = 1000
        
        while True:
            eroded = cv2.erode(temp, kernel)
            dilated = cv2.dilate(eroded, kernel)
            subset = cv2.subtract(temp, dilated)
            skeleton = cv2.bitwise_or(skeleton, subset)
            temp = eroded.copy()
            
            iterations += 1
            if cv2.countNonZero(temp) == 0 or iterations >= max_iterations:
                break
        
        return skeleton
    
    def _find_skeleton_endpoints(self, skeleton: np.ndarray) -> List[np.ndarray]:
        """
        Find endpoints of skeleton using hit-or-miss transform.
        
        Endpoints have exactly 1 neighbor in skeletal connectivity.
        """
        endpoints = []
        
        # Endpoint kernels (8 orientations)
        endpoint_kernels = [
            np.array([[0, 0, 0], [0, 1, 0], [0, 1, 0]], dtype=np.uint8),
            np.array([[0, 0, 0], [0, 1, 1], [0, 0, 0]], dtype=np.uint8),
            np.array([[0, 0, 0], [0, 1, 0], [0, 0, 1]], dtype=np.uint8),
            np.array([[0, 0, 0], [1, 1, 0], [0, 0, 0]], dtype=np.uint8),
            np.array([[0, 1, 0], [0, 1, 0], [0, 0, 0]], dtype=np.uint8),
            np.array([[1, 0, 0], [0, 1, 0], [0, 0, 0]], dtype=np.uint8),
            np.array([[0, 0, 1], [0, 1, 0], [0, 0, 0]], dtype=np.uint8),
            np.array([[0, 0, 0], [0, 1, 0], [1, 0, 0]], dtype=np.uint8),
        ]
        
        # Find all skeleton points
        skeleton_points = np.where(skeleton > 0)
        
        if len(skeleton_points[0]) == 0:
            return endpoints
        
        # Check each skeleton point for endpoint pattern
        for y, x in zip(skeleton_points[0], skeleton_points[1]):
            if y < 1 or y >= skeleton.shape[0] - 1:
                continue
            if x < 1 or x >= skeleton.shape[1] - 1:
                continue
            
            # Extract 3x3 neighborhood
            neighborhood = skeleton[y-1:y+2, x-1:x+2]
            
            # Count neighbors (excluding center)
            neighbor_count = np.sum(neighborhood > 0) - 1
            
            # Endpoint has exactly 1 neighbor
            if neighbor_count == 1:
                endpoints.append(np.array([x, y]))
        
        return endpoints
    
    def _compute_centroid(self, mask: np.ndarray) -> Optional[np.ndarray]:
        """Compute centroid of mask region."""
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if not contours:
            return None
        
        largest = max(contours, key=cv2.contourArea)
        M = cv2.moments(largest)
        
        if M['m00'] == 0:
            return None
        
        cx = M['m10'] / M['m00']
        cy = M['m01'] / M['m00']
        
        return np.array([cx, cy])
    
    def _fallback_roi(self, segmented: np.ndarray, mask: np.ndarray, 
                      metadata: Dict[str, Any]) -> Tuple[np.ndarray, Dict[str, Any]]:
        """
        Fallback ROI extraction: take top portion of segmented region.
        
        Used when skeleton-based detection fails.
        """
        h, w = segmented.shape[:2]
        
        # Simple approach: top 30% of image
        roi_height = int(h * 0.30)
        roi = segmented[:roi_height, :].copy()
        roi_mask = mask[:roi_height, :]
        
        # NOTE: Do NOT apply destructive masking!
        # Pixel values are preserved; mask is for reference only.
        
        metadata.update({
            'roi_shape': roi.shape,
            'confidence': 0.4,
            'method': 'fallback_top_region'
        })
        
        logger.info(f"✓ Fallback ROI: {roi.shape}")
        
        return roi, metadata
