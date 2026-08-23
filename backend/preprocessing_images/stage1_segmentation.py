#!/usr/bin/env python3
"""
🔹 STAGE 1: COLOR-AGNOSTIC FINGER SEGMENTATION
==============================================
Segments finger from any background, any color.

Steps:
1. Convert to grayscale (discard color)
2. Edge & gradient detection (Sobel + Canny)
3. Morphological reconstruction (close gaps, fill regions)
4. Select largest elongated connected component

NO ML - Pure computer vision.

Author: DMIT Research Team
Version: 1.0
"""

import cv2
import numpy as np
from typing import Tuple, Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


class FingerSegmenter:
    """
    Color-agnostic finger segmentation using gradient and morphology.
    
    Works because:
    - Finger ≈ long convex object with strong edges
    - Background ≈ fragmented or flat regions
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        """
        Initialize segmenter with configuration.
        
        Args:
            config: Configuration dictionary with:
                - canny_low: Lower Canny threshold (default: 50)
                - canny_high: Upper Canny threshold (default: 150)
                - morph_kernel_size: Morphological kernel size (default: 5)
                - min_finger_area_ratio: Minimum finger area as ratio of image (default: 0.05)
        """
        self.config = config or {}
        self.canny_low = self.config.get('canny_low', 50)
        self.canny_high = self.config.get('canny_high', 150)
        self.morph_kernel_size = self.config.get('morph_kernel_size', 5)
        self.min_finger_area_ratio = self.config.get('min_finger_area_ratio', 0.05)
    
    def segment(self, image: np.ndarray) -> Tuple[Optional[np.ndarray], Optional[np.ndarray], Dict[str, Any]]:
        """
        Segment finger from background.
        
        Args:
            image: Input image (BGR or grayscale)
            
        Returns:
            Tuple of:
            - segmented: Cropped finger region (grayscale)
            - mask: Binary mask of finger region
            - metadata: Processing details
        """
        metadata = {
            'input_shape': image.shape,
            'confidence': 0.0
        }
        
        try:
            # Step 1: Convert to grayscale
            if len(image.shape) == 3:
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            else:
                gray = image.copy()
            
            metadata['grayscale_mean'] = float(np.mean(gray))
            
            # Step 2: Edge & gradient detection
            edges = self._detect_edges(gray)
            
            # Step 3: Morphological reconstruction
            filled_mask = self._morphological_reconstruction(edges, gray)
            
            # Step 4: Select largest elongated connected component
            finger_mask, contour = self._select_finger_region(filled_mask, gray)
            
            if finger_mask is None:
                logger.warning("No valid finger region found")
                return None, None, metadata
            
            # Calculate bounding box and crop
            x, y, w, h = cv2.boundingRect(contour)
            
            # Add padding
            pad = 10
            x = max(0, x - pad)
            y = max(0, y - pad)
            w = min(gray.shape[1] - x, w + 2 * pad)
            h = min(gray.shape[0] - y, h + 2 * pad)
            
            # Crop finger region
            segmented = gray[y:y+h, x:x+w].copy()
            cropped_mask = finger_mask[y:y+h, x:x+w]
            
            # NOTE: Do NOT apply destructive masking here!
            # Previously this zeroed out background pixels, causing black regions
            # that propagate through the entire pipeline.
            # The mask is returned for reference but pixel values are preserved.
            
            # Calculate confidence
            area_ratio = np.sum(finger_mask > 0) / (gray.shape[0] * gray.shape[1])
            aspect_ratio = h / w if w > 0 else 0
            
            # Good finger: reasonable area, elongated shape
            if area_ratio > self.min_finger_area_ratio and aspect_ratio > 1.5:
                confidence = min(1.0, 0.5 + area_ratio * 2 + (aspect_ratio - 1.5) * 0.2)
            else:
                confidence = 0.3
            
            metadata.update({
                'bounding_box': (x, y, w, h),
                'area_ratio': float(area_ratio),
                'aspect_ratio': float(aspect_ratio),
                'segmented_shape': segmented.shape,
                'confidence': float(confidence)
            })
            
            logger.info(f"✓ Segmentation: {segmented.shape}, confidence: {confidence:.2f}")
            
            return segmented, cropped_mask, metadata
            
        except Exception as e:
            logger.error(f"Segmentation failed: {e}")
            metadata['error'] = str(e)
            return None, None, metadata
    
    def _detect_edges(self, gray: np.ndarray) -> np.ndarray:
        """
        Detect edges using Sobel gradients and Canny.
        
        Finger edges are strong, continuous curves.
        """
        # Gaussian blur to reduce noise
        blurred = cv2.GaussianBlur(gray, (5, 5), 1.0)
        
        # Sobel gradients (stronger edge detection)
        sobel_x = cv2.Sobel(blurred, cv2.CV_64F, 1, 0, ksize=3)
        sobel_y = cv2.Sobel(blurred, cv2.CV_64F, 0, 1, ksize=3)
        sobel_mag = np.sqrt(sobel_x**2 + sobel_y**2)
        sobel_mag = np.uint8(255 * sobel_mag / sobel_mag.max())
        
        # Canny edge detection
        canny = cv2.Canny(blurred, self.canny_low, self.canny_high)
        
        # Combine Sobel and Canny
        sobel_binary = (sobel_mag > 50).astype(np.uint8) * 255
        edges = cv2.bitwise_or(canny, sobel_binary)
        
        return edges
    
    def _morphological_reconstruction(self, edges: np.ndarray, gray: np.ndarray) -> np.ndarray:
        """
        Morphological operations to reconstruct finger region.
        
        Steps:
        - Close gaps in edges
        - Dilate to connect nearby edges
        - Fill enclosed regions
        - Remove small components
        """
        # Create morphological kernel
        kernel = cv2.getStructuringElement(
            cv2.MORPH_ELLIPSE, 
            (self.morph_kernel_size, self.morph_kernel_size)
        )
        
        # Close gaps
        closed = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel, iterations=3)
        
        # Dilate to connect nearby edges
        dilated = cv2.dilate(closed, kernel, iterations=2)
        
        # Fill enclosed regions using flood fill
        h, w = dilated.shape
        mask = np.zeros((h + 2, w + 2), np.uint8)
        flood_fill = dilated.copy()
        cv2.floodFill(flood_fill, mask, (0, 0), 255)
        flood_fill_inv = cv2.bitwise_not(flood_fill)
        
        # Combine with original edges
        filled = cv2.bitwise_or(dilated, flood_fill_inv)
        
        # Also try Otsu thresholding as backup
        _, otsu = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        # Combine methods
        combined = cv2.bitwise_or(filled, otsu)
        
        # Clean up with morphological opening
        cleaned = cv2.morphologyEx(combined, cv2.MORPH_OPEN, kernel, iterations=2)
        
        return cleaned
    
    def _select_finger_region(self, mask: np.ndarray, gray: np.ndarray) -> Tuple[Optional[np.ndarray], Optional[np.ndarray]]:
        """
        Select the largest elongated connected component as finger.
        
        Finger characteristics:
        - Largest or near-largest region
        - Elongated (aspect ratio > 1.5)
        - Convex hull similar to original shape
        """
        # Find contours
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if not contours:
            return None, None
        
        # Score each contour
        best_score = 0
        best_contour = None
        image_area = gray.shape[0] * gray.shape[1]
        
        for contour in contours:
            area = cv2.contourArea(contour)
            if area < image_area * self.min_finger_area_ratio:
                continue
            
            # Get bounding rect
            x, y, w, h = cv2.boundingRect(contour)
            aspect_ratio = max(h, w) / min(h, w) if min(h, w) > 0 else 0
            
            # Prefer elongated shapes (finger-like)
            elongation_score = min(1.0, aspect_ratio / 3.0)  # Max at 3:1
            
            # Prefer larger regions
            size_score = area / image_area
            
            # Convexity score
            hull = cv2.convexHull(contour)
            hull_area = cv2.contourArea(hull)
            convexity = area / hull_area if hull_area > 0 else 0
            
            # Combined score
            score = elongation_score * 0.4 + size_score * 0.3 + convexity * 0.3
            
            if score > best_score:
                best_score = score
                best_contour = contour
        
        if best_contour is None:
            return None, None
        
        # Create mask from best contour
        finger_mask = np.zeros(mask.shape, dtype=np.uint8)
        cv2.drawContours(finger_mask, [best_contour], -1, 255, -1)
        
        return finger_mask, best_contour
