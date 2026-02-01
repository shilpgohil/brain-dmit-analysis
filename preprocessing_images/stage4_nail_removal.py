#!/usr/bin/env python3
"""
🔹 STAGE 4: NAIL REMOVAL
========================
Removes nail region from fingerprint ROI to prevent false ridges.

Detection criteria (rule-based, no ML):
- Local intensity smoothness (nails are smoother than ridges)
- Low ridge frequency in nail region
- Sharp curvature boundary at nail edge

Author: DMIT Research Team
Version: 1.0
"""

import cv2
import numpy as np
from typing import Tuple, Dict, Any
import logging

logger = logging.getLogger(__name__)


class NailRemover:
    """
    Removes nail region from fingerprint ROI.
    
    Nail causes false ridges and must be removed. Detection is based on:
    - Nail surface is smoother than fingerprint ridges
    - Nail has low ridge frequency (near zero)
    - Sharp curvature boundary at nail edge
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        """
        Initialize remover with configuration.
        
        Args:
            config: Configuration dictionary with:
                - smoothness_threshold: Threshold for smooth region detection (default: 0.3)
                - nail_region_ratio: Maximum nail region as ratio of ROI (default: 0.15)
        """
        self.config = config or {}
        self.smoothness_threshold = self.config.get('smoothness_threshold', 0.3)
        self.nail_region_ratio = self.config.get('nail_region_ratio', 0.15)
    
    def remove(self, roi: np.ndarray) -> Tuple[np.ndarray, Dict[str, Any]]:
        """
        Remove nail region from fingerprint ROI.
        
        Args:
            roi: Fingerprint ROI image (grayscale)
            
        Returns:
            Tuple of:
            - cleaned: ROI with nail region removed/masked
            - metadata: Processing details
        """
        metadata = {
            'input_shape': roi.shape,
            'nail_detected': False,
            'nail_removed': False,
            'confidence': 0.8
        }
        
        try:
            h, w = roi.shape[:2]
            
            if h < 20 or w < 20:
                logger.info("ROI too small for nail detection")
                return roi, metadata
            
            # Step 1: Detect smooth regions (potential nail)
            smoothness_map = self._compute_smoothness_map(roi)
            
            # Step 2: Detect low ridge frequency regions
            ridge_freq_map = self._compute_ridge_frequency_map(roi)
            
            # Step 3: Detect sharp curvature boundaries
            boundary_map = self._detect_nail_boundary(roi)
            
            # Step 4: Combine evidence for nail region
            nail_mask = self._combine_nail_evidence(
                smoothness_map, ridge_freq_map, boundary_map, roi
            )
            
            nail_area = np.sum(nail_mask > 0)
            total_area = h * w
            nail_ratio = nail_area / total_area
            
            metadata['nail_ratio'] = float(nail_ratio)
            
            # Only remove if nail region is reasonably sized
            if 0.01 < nail_ratio < self.nail_region_ratio:
                metadata['nail_detected'] = True
                
                # Create cleaned ROI by masking nail region
                cleaned = roi.copy()
                
                # Option 1: Black out nail region
                # cleaned[nail_mask > 0] = 0
                
                # Option 2: Inpaint nail region (better for downstream processing)
                if nail_area > 100:
                    cleaned = cv2.inpaint(roi, nail_mask, 3, cv2.INPAINT_TELEA)
                    metadata['nail_removed'] = True
                
                metadata['confidence'] = 0.85
                logger.info(f"✓ Nail removed: {nail_ratio:.1%} of ROI")
                
                return cleaned, metadata
            else:
                # No significant nail detected or too large (probably false positive)
                if nail_ratio >= self.nail_region_ratio:
                    logger.info(f"Nail region too large ({nail_ratio:.1%}), skipping removal")
                else:
                    logger.info("No significant nail region detected")
                
                return roi, metadata
            
        except Exception as e:
            logger.error(f"Nail removal failed: {e}")
            metadata['error'] = str(e)
            return roi, metadata
    
    def _compute_smoothness_map(self, image: np.ndarray) -> np.ndarray:
        """
        Compute local smoothness map.
        
        Nail regions have low local variance (smooth surface).
        """
        # Use local standard deviation as smoothness measure
        kernel_size = 15
        
        # Compute local mean and variance
        mean = cv2.blur(image.astype(np.float32), (kernel_size, kernel_size))
        sq_mean = cv2.blur((image.astype(np.float32))**2, (kernel_size, kernel_size))
        variance = sq_mean - mean**2
        variance = np.maximum(variance, 0)  # Ensure non-negative
        std_dev = np.sqrt(variance)
        
        # Normalize to 0-1 range
        max_std = np.max(std_dev)
        if max_std > 0:
            std_dev_norm = std_dev / max_std
        else:
            std_dev_norm = std_dev
        
        # Invert: low variance (smooth) = high smoothness
        smoothness = 1.0 - std_dev_norm
        
        return smoothness.astype(np.float32)
    
    def _compute_ridge_frequency_map(self, image: np.ndarray) -> np.ndarray:
        """
        Compute local ridge frequency map.
        
        Nail regions have very low ridge frequency compared to fingerprint.
        """
        # Apply Gabor filter bank to detect ridge frequency
        frequencies = []
        
        for freq in [0.1, 0.15, 0.2, 0.25]:
            for theta in np.linspace(0, np.pi, 8):
                kernel = cv2.getGaborKernel(
                    (21, 21), sigma=4.0, theta=theta, 
                    lambd=1.0/freq, gamma=0.5, psi=0
                )
                filtered = cv2.filter2D(image, cv2.CV_32F, kernel)
                frequencies.append(np.abs(filtered))
        
        # Max response across all orientations and frequencies
        freq_response = np.max(np.stack(frequencies), axis=0)
        
        # Normalize
        max_response = np.max(freq_response)
        if max_response > 0:
            freq_response = freq_response / max_response
        
        # Low frequency = potential nail
        low_freq_map = 1.0 - freq_response
        
        return low_freq_map.astype(np.float32)
    
    def _detect_nail_boundary(self, image: np.ndarray) -> np.ndarray:
        """
        Detect sharp intensity boundaries that indicate nail edge.
        
        Nail-skin boundary has distinct intensity gradient.
        """
        # Edge detection with high sensitivity
        edges = cv2.Canny(image, 30, 100)
        
        # Dilate to connect edges
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        edges_dilated = cv2.dilate(edges, kernel, iterations=1)
        
        # Look for horizontal-ish edges (nail boundary typically horizontal)
        sobel_x = cv2.Sobel(image, cv2.CV_64F, 1, 0, ksize=3)
        sobel_y = cv2.Sobel(image, cv2.CV_64F, 0, 1, ksize=3)
        
        # Compute gradient direction
        gradient_direction = np.arctan2(sobel_y, sobel_x)
        
        # Find roughly horizontal edges (direction near 0 or pi)
        horizontal_edge = np.logical_or(
            np.abs(gradient_direction) < np.pi/6,
            np.abs(gradient_direction) > 5*np.pi/6
        )
        
        boundary_map = np.logical_and(edges_dilated > 0, horizontal_edge)
        
        return boundary_map.astype(np.uint8) * 255
    
    def _combine_nail_evidence(self, smoothness: np.ndarray, 
                                ridge_freq: np.ndarray,
                                boundary: np.ndarray,
                                image: np.ndarray) -> np.ndarray:
        """
        Combine evidence maps to detect nail region.
        
        Nail region: smooth + low ridge frequency + near top of ROI.
        """
        h, w = image.shape[:2]
        
        # Weight towards top of image (nail typically at fingertip top)
        vertical_weight = np.zeros((h, w), dtype=np.float32)
        for i in range(h):
            vertical_weight[i, :] = 1.0 - (i / h)  # Higher weight at top
        
        # Combine evidence
        combined = (
            smoothness * 0.35 +
            ridge_freq * 0.35 +
            vertical_weight * 0.30
        )
        
        # Threshold to get binary nail mask
        threshold = self.smoothness_threshold + 0.3  # ~0.6 combined score
        nail_mask = (combined > threshold).astype(np.uint8) * 255
        
        # Clean up mask with morphological operations
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        nail_mask = cv2.morphologyEx(nail_mask, cv2.MORPH_OPEN, kernel)
        nail_mask = cv2.morphologyEx(nail_mask, cv2.MORPH_CLOSE, kernel)
        
        # Only keep regions connected to top of image
        # Find contours
        contours, _ = cv2.findContours(nail_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Keep only contours touching top edge
        final_mask = np.zeros_like(nail_mask)
        for contour in contours:
            x, y, cw, ch = cv2.boundingRect(contour)
            if y < h * 0.3:  # Must start in top 30%
                cv2.drawContours(final_mask, [contour], -1, 255, -1)
        
        return final_mask
