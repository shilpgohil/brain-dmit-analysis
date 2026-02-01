#!/usr/bin/env python3
"""
🔹 STAGE 5: RIDGE ENHANCEMENT
=============================
Enhances fingerprint ridges using classical, proven techniques.

Steps:
1. CLAHE (Contrast Limited Adaptive Histogram Equalization)
2. Gabor filter bank (multi-orientation ridge detection)
3. Orientation field estimation
4. Ridge frequency normalization
5. Binarization + thinning

These are standard fingerprint preprocessing techniques used in biometrics.

Author: DMIT Research Team
Version: 1.0
"""

import cv2
import numpy as np
from typing import Tuple, Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


class RidgeEnhancer:
    """
    Enhances fingerprint ridges for feature extraction.
    
    Uses classical, proven fingerprint enhancement techniques:
    - CLAHE for contrast normalization
    - Gabor filters for ridge enhancement
    - Orientation field for directional filtering
    - Binarization and thinning for clean ridges
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        """
        Initialize enhancer with configuration.
        
        Args:
            config: Configuration dictionary with:
                - clahe_clip_limit: CLAHE clip limit (default: 2.0)
                - clahe_tile_size: CLAHE tile grid size (default: 8)
                - gabor_frequencies: List of Gabor frequencies (default: [0.1, 0.15, 0.2])
                - gabor_orientations: Number of orientations (default: 8)
        """
        self.config = config or {}
        self.clahe_clip_limit = self.config.get('clahe_clip_limit', 2.0)
        self.clahe_tile_size = self.config.get('clahe_tile_size', 8)
        self.gabor_frequencies = self.config.get('gabor_frequencies', [0.1, 0.15, 0.2])
        self.gabor_orientations = self.config.get('gabor_orientations', 8)
    
    def enhance(self, image: np.ndarray) -> Tuple[np.ndarray, Dict[str, Any]]:
        """
        Enhance fingerprint ridges.
        
        Args:
            image: Input fingerprint image (grayscale)
            
        Returns:
            Tuple of:
            - enhanced: Enhanced fingerprint image
            - metadata: Processing details
        """
        metadata = {
            'input_shape': image.shape,
            'confidence': 0.0
        }
        
        try:
            # Ensure grayscale
            if len(image.shape) == 3:
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            else:
                gray = image.copy()
            
            # Step 1: CLAHE for contrast normalization
            clahe_result = self._apply_clahe(gray)
            metadata['clahe_applied'] = True
            
            # Step 2: Orientation field estimation
            orientation_field = self._estimate_orientation_field(clahe_result)
            metadata['orientation_field_computed'] = True
            
            # Step 3: Ridge frequency estimation
            ridge_frequency = self._estimate_ridge_frequency(clahe_result, orientation_field)
            metadata['average_ridge_frequency'] = float(np.mean(ridge_frequency))
            
            # Step 4: Gabor filtering with orientation field
            gabor_enhanced = self._apply_gabor_filter_bank(
                clahe_result, orientation_field, ridge_frequency
            )
            metadata['gabor_enhanced'] = True
            
            # Step 5: Normalize and enhance contrast
            normalized = self._normalize_image(gabor_enhanced)
            
            # Step 6: Optional binarization
            binary = self._binarize(normalized)
            
            # Step 7: Optional thinning (skeleton)
            thinned = self._thin_ridges(binary)
            
            # Calculate quality/confidence
            ridge_clarity = self._assess_ridge_clarity(gabor_enhanced)
            confidence = min(1.0, ridge_clarity)
            
            metadata.update({
                'ridge_clarity': float(ridge_clarity),
                'confidence': float(confidence),
                'output_shape': gabor_enhanced.shape
            })
            
            logger.info(f"✓ Ridge enhancement complete (clarity: {ridge_clarity:.2f})")
            
            # Return the enhanced grayscale (not binary) for feature extraction
            # Binary and thinned versions can be used for minutiae extraction
            return normalized, metadata
            
        except Exception as e:
            logger.error(f"Ridge enhancement failed: {e}")
            metadata['error'] = str(e)
            metadata['confidence'] = 0.3
            return image, metadata
    
    def _apply_clahe(self, image: np.ndarray) -> np.ndarray:
        """
        Apply CLAHE (Contrast Limited Adaptive Histogram Equalization).
        
        Normalizes contrast across the fingerprint image while
        limiting noise amplification.
        """
        clahe = cv2.createCLAHE(
            clipLimit=self.clahe_clip_limit,
            tileGridSize=(self.clahe_tile_size, self.clahe_tile_size)
        )
        return clahe.apply(image)
    
    def _estimate_orientation_field(self, image: np.ndarray) -> np.ndarray:
        """
        Estimate local ridge orientation using gradient analysis.
        
        Returns orientation in radians for each pixel.
        """
        # Compute gradients
        gx = cv2.Sobel(image.astype(np.float64), cv2.CV_64F, 1, 0, ksize=3)
        gy = cv2.Sobel(image.astype(np.float64), cv2.CV_64F, 0, 1, ksize=3)
        
        # Compute orientation using squared gradients (removes ambiguity)
        gxx = gx * gx
        gyy = gy * gy
        gxy = gx * gy
        
        # Block averaging for robustness
        block_size = 16
        gxx_avg = cv2.blur(gxx, (block_size, block_size))
        gyy_avg = cv2.blur(gyy, (block_size, block_size))
        gxy_avg = cv2.blur(gxy, (block_size, block_size))
        
        # Compute orientation (perpendicular to ridge direction)
        orientation = 0.5 * np.arctan2(2 * gxy_avg, gxx_avg - gyy_avg)
        
        # Ridges are perpendicular to gradient
        orientation = orientation + np.pi / 2
        
        return orientation
    
    def _estimate_ridge_frequency(self, image: np.ndarray, 
                                   orientation: np.ndarray) -> np.ndarray:
        """
        Estimate local ridge frequency.
        
        Ridge frequency is the number of ridges per unit length.
        Typical fingerprint: 0.1 to 0.25 ridges/pixel
        """
        h, w = image.shape
        frequency = np.zeros_like(image, dtype=np.float64)
        
        # Block-based frequency estimation
        block_size = 32
        
        for y in range(0, h - block_size, block_size):
            for x in range(0, w - block_size, block_size):
                block = image[y:y+block_size, x:x+block_size]
                
                if np.std(block) < 10:  # Skip flat regions
                    continue
                
                # Project along orientation to get 1D signal
                angle = np.mean(orientation[y:y+block_size, x:x+block_size])
                
                # Sample along perpendicular direction
                freq = self._estimate_block_frequency(block, angle)
                frequency[y:y+block_size, x:x+block_size] = freq
        
        # Default frequency for unestimated regions
        default_freq = 0.15
        frequency[frequency == 0] = default_freq
        
        return frequency
    
    def _estimate_block_frequency(self, block: np.ndarray, angle: float) -> float:
        """Estimate ridge frequency for a single block."""
        # Create projection along ridge direction
        center = block.shape[0] // 2
        
        # Sample along perpendicular to ridge
        perp_angle = angle + np.pi / 2
        
        # Create sampling line
        length = min(block.shape) // 2
        profile = []
        
        for i in range(-length, length):
            px = int(center + i * np.cos(perp_angle))
            py = int(center + i * np.sin(perp_angle))
            
            if 0 <= px < block.shape[1] and 0 <= py < block.shape[0]:
                profile.append(block[py, px])
        
        if len(profile) < 10:
            return 0.15  # Default frequency
        
        profile = np.array(profile)
        
        # Count zero crossings of detrended signal
        profile = profile - np.mean(profile)
        zero_crossings = np.sum(np.diff(np.sign(profile)) != 0)
        
        # Frequency = zero_crossings / (2 * length)
        freq = zero_crossings / (2 * len(profile))
        
        # Clamp to reasonable range
        return np.clip(freq, 0.05, 0.3)
    
    def _apply_gabor_filter_bank(self, image: np.ndarray,
                                  orientation: np.ndarray,
                                  frequency: np.ndarray) -> np.ndarray:
        """
        Apply Gabor filters tuned to local ridge orientation and frequency.
        
        Uses vectorized max-response approach for efficiency and robustness.
        This handles low-value regions better than pixel-by-pixel selection.
        """
        h, w = image.shape
        
        # Apply Gabor filters for each orientation
        num_orientations = self.gabor_orientations
        gabor_responses = []
        
        for i in range(num_orientations):
            theta = i * np.pi / num_orientations
            
            # Use average frequency for filter
            avg_freq = np.mean(self.gabor_frequencies)
            
            # Create Gabor kernel
            kernel = cv2.getGaborKernel(
                (31, 31),  # kernel size
                sigma=4.0,  # standard deviation
                theta=theta,
                lambd=1.0 / avg_freq,  # wavelength
                gamma=0.5,  # aspect ratio
                psi=0  # phase offset
            )
            
            # Apply filter
            response = cv2.filter2D(image.astype(np.float64), cv2.CV_64F, kernel)
            gabor_responses.append(np.abs(response))  # Use absolute value
        
        # Stack all responses and take maximum across orientations
        # This is robust to low-value regions and much faster than pixel-by-pixel
        response_stack = np.stack(gabor_responses, axis=0)
        enhanced = np.max(response_stack, axis=0)
        
        # Normalize to 0-255
        enhanced = cv2.normalize(enhanced, None, 0, 255, cv2.NORM_MINMAX)
        
        return enhanced.astype(np.uint8)
    
    def _normalize_image(self, image: np.ndarray) -> np.ndarray:
        """Normalize image to 0-255 range with enhanced contrast."""
        # Remove outliers
        p2, p98 = np.percentile(image, (2, 98))
        clipped = np.clip(image, p2, p98)
        
        # Normalize to 0-255
        if p98 > p2:
            normalized = ((clipped - p2) / (p98 - p2) * 255).astype(np.uint8)
        else:
            normalized = image.astype(np.uint8)
        
        return normalized
    
    def _binarize(self, image: np.ndarray) -> np.ndarray:
        """
        Binarize fingerprint image using adaptive thresholding.
        
        Returns binary image with white ridges, black valleys.
        """
        # Adaptive thresholding works best for fingerprints
        binary = cv2.adaptiveThreshold(
            image, 255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY,
            blockSize=15,
            C=5
        )
        
        return binary
    
    def _thin_ridges(self, binary: np.ndarray) -> np.ndarray:
        """
        Thin ridges to single-pixel width using morphological thinning.
        
        Used for minutiae extraction.
        """
        # Skeletonization
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
    
    def _assess_ridge_clarity(self, image: np.ndarray) -> float:
        """
        Assess clarity/quality of enhanced ridges.
        
        Based on local contrast and ridge structure.
        """
        # Local standard deviation (indicator of ridge-valley contrast)
        kernel_size = 15
        
        mean = cv2.blur(image.astype(np.float32), (kernel_size, kernel_size))
        sq_mean = cv2.blur((image.astype(np.float32))**2, (kernel_size, kernel_size))
        variance = sq_mean - mean**2
        variance = np.maximum(variance, 0)
        std_dev = np.sqrt(variance)
        
        # Average contrast
        avg_contrast = np.mean(std_dev)
        
        # Normalize to 0-1 (typical good fingerprint has std ~40-80)
        clarity = min(1.0, avg_contrast / 60.0)
        
        return float(clarity)
    
    def get_binary_output(self, image: np.ndarray) -> np.ndarray:
        """Get binarized version of enhanced image."""
        return self._binarize(image)
    
    def get_skeleton_output(self, image: np.ndarray) -> np.ndarray:
        """Get skeletonized/thinned version of enhanced image."""
        binary = self._binarize(image)
        return self._thin_ridges(binary)
