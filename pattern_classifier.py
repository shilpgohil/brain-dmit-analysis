#!/usr/bin/env python3
"""
🎯 FINGERPRINT PATTERN CLASSIFIER
=================================
Classifies fingerprint patterns into Whorl/Loop/Arch families and subtypes.
Based on CADA (China Association of Dermatoglyphics Analyst) standards.

Author: DMIT Research Team
Version: 1.0
"""

import cv2
import numpy as np
import logging
from typing import Dict, Any, Tuple, List, Optional
from enum import Enum

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PatternFamily(Enum):
    """Main fingerprint pattern families."""
    WHORL = "whorl"
    LOOP = "loop"
    ARCH = "arch"
    ACCIDENTAL = "accidental"
    UNKNOWN = "unknown"


class PatternSubtype(Enum):
    """All pattern subtypes from CADA standards."""
    # Whorl Family (10 types)
    TARGET_WHORL = "Wt"
    SPIRAL_WHORL = "Ws"
    ELONGATED_WHORL = "We"
    WHORL_COMPOSITE = "Wc"
    DOUBLE_WHORL = "Wd"
    IMPLODING_WHORL = "Wi"
    PEACOCKS_EYE = "Wp"
    RADIAL_PEACOCK = "Rp"
    LATERAL_POCKET = "Wl"
    RADIAL_LATERAL = "Rl"
    
    # Loop Family (4 types)
    ULNAR_LOOP = "U"
    RADIAL_LOOP = "R"
    FALLING_LOOP = "Lf"
    RADIAL_FALLING = "Rf"
    
    # Arch Family (5 types)
    SIMPLE_ARCH = "As"
    TENTED_ARCH = "At"
    ENCLOSED_ARCH = "Ae"
    ARCH_ULNAR_LOOP = "Au"
    ARCH_RADIAL_LOOP = "Ar"
    
    # Accidental (4 types)
    ACCIDENTAL_LOOP = "Xu"
    ACCIDENTAL_WHORL = "Xw"
    ACCIDENTAL_ARCH = "Xa"
    MALFORMATION = "Mf"
    
    UNKNOWN = "?"


class PatternClassifier:
    """
    Fingerprint pattern classifier using orientation field analysis.
    
    Detection methods:
    1. Compute orientation field using gradient analysis
    2. Detect singular points (cores and deltas/triradii)
    3. Classify based on singular point count
    4. Determine subtype based on ridge flow analysis
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        """Initialize classifier with optional configuration."""
        self.config = config or self._default_config()
        logger.info("🔍 Pattern Classifier initialized")
    
    def _default_config(self) -> Dict[str, Any]:
        """Default configuration for pattern classification."""
        return {
            'block_size': 8,            # Smaller block for small images
            'gaussian_sigma': 2.0,      # More smoothing
            'poincare_threshold': 0.40, # Higher threshold for detection
            'min_confidence': 0.5,      # Minimum confidence for classification
            'max_cores': 2,             # Maximum cores to keep
            'max_deltas': 2             # Maximum deltas to keep
        }
    
    def classify(self, image: np.ndarray) -> Dict[str, Any]:
        """
        Classify fingerprint pattern.
        
        Args:
            image: Grayscale fingerprint image
            
        Returns:
            Dictionary containing:
            - family: PatternFamily
            - subtype: PatternSubtype
            - triradii_count: Number of triradii (delta) points
            - core_count: Number of core points
            - confidence: Classification confidence (0-1)
            - singular_points: List of detected singular points
        """
        # Ensure grayscale
        if len(image.shape) == 3:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Step 1: Compute orientation field
        orientation_field = self._compute_orientation_field(image)
        
        # Step 2: Detect singular points (cores and deltas)
        cores, deltas = self._detect_singular_points(image, orientation_field)
        
        # Step 3: Classify based on singular points
        family, confidence = self._classify_family(len(cores), len(deltas))
        
        # Step 4: Determine subtype
        subtype = self._determine_subtype(image, orientation_field, family, cores, deltas)
        
        # Step 5: Calculate ridge count from core to delta (TFRC method)
        tfrc_result = self.calculate_tfrc(image, cores, deltas)
        
        result = {
            'family': family.value,
            'family_enum': family,
            'subtype': subtype.value,
            'subtype_enum': subtype,
            'subtype_name': self._get_subtype_name(subtype),
            'triradii_count': len(deltas),
            'core_count': len(cores),
            'confidence': confidence,
            'singular_points': {
                'cores': cores,
                'deltas': deltas
            },
            # Ridge count features
            'ridge_count': tfrc_result['ridge_count'],
            'ridge_counts_all': tfrc_result['ridge_counts_all']
        }
        
        logger.info(f"📊 Pattern: {family.value} ({subtype.value}) - "
                   f"Cores: {len(cores)}, Deltas: {len(deltas)}, "
                   f"Ridge Count: {tfrc_result['ridge_count']}, "
                   f"Confidence: {confidence:.2f}")
        
        return result
    
    def _compute_orientation_field(self, image: np.ndarray) -> np.ndarray:
        """
        Compute orientation field using gradient-based method with doubled angles.
        
        Returns orientation in radians for each block (range: -pi/2 to pi/2).
        """
        block_size = self.config['block_size']
        h, w = image.shape
        
        # Apply Gaussian blur to reduce noise
        blurred = cv2.GaussianBlur(image, (5, 5), 1.0)
        
        # Compute gradients using Sobel
        gx = cv2.Sobel(blurred.astype(np.float64), cv2.CV_64F, 1, 0, ksize=3)
        gy = cv2.Sobel(blurred.astype(np.float64), cv2.CV_64F, 0, 1, ksize=3)
        
        # Block-based orientation estimation
        rows = h // block_size
        cols = w // block_size
        
        # Store cos(2*theta) and sin(2*theta) for proper averaging
        cos2theta = np.zeros((rows, cols))
        sin2theta = np.zeros((rows, cols))
        
        for i in range(rows):
            for j in range(cols):
                y1, y2 = i * block_size, (i + 1) * block_size
                x1, x2 = j * block_size, (j + 1) * block_size
                
                gx_block = gx[y1:y2, x1:x2].flatten()
                gy_block = gy[y1:y2, x1:x2].flatten()
                
                # Use gradient squared method (doubled angle)
                # cos(2*theta) = Gx^2 - Gy^2
                # sin(2*theta) = 2*Gx*Gy
                gxx = np.sum(gx_block * gx_block)
                gyy = np.sum(gy_block * gy_block)
                gxy = np.sum(gx_block * gy_block)
                
                cos2theta[i, j] = gxx - gyy
                sin2theta[i, j] = 2 * gxy
        
        # Smooth the doubled angle components separately
        sigma = self.config['gaussian_sigma']
        cos2theta = cv2.GaussianBlur(cos2theta, (5, 5), sigma)
        sin2theta = cv2.GaussianBlur(sin2theta, (5, 5), sigma)
        
        # Compute orientation as half the doubled angle
        orientation = 0.5 * np.arctan2(sin2theta, cos2theta)
        
        return orientation
    
    def _detect_singular_points(self, image: np.ndarray, 
                                orientation: np.ndarray) -> Tuple[List, List]:
        """
        Detect singular points using Poincaré index.
        
        Core points have Poincaré index = +1/2 (or +180°)
        Delta/triradii points have Poincaré index = -1/2 (or -180°)
        """
        rows, cols = orientation.shape
        cores = []
        deltas = []
        
        block_size = self.config['block_size']
        threshold = self.config['poincare_threshold']
        
        # Compute Poincaré index for each block
        for i in range(1, rows - 1):
            for j in range(1, cols - 1):
                poincare_sum = self._compute_poincare_index(orientation, i, j)
                
                # Normalize to turns (0 to 1 scale)
                poincare_normalized = poincare_sum / (2 * np.pi)
                
                # Core detection (positive Poincaré)
                if poincare_normalized > threshold:
                    x = (j + 0.5) * block_size
                    y = (i + 0.5) * block_size
                    cores.append({'x': int(x), 'y': int(y), 
                                 'poincare': float(poincare_normalized)})
                
                # Delta/triradii detection (negative Poincaré)
                elif poincare_normalized < -threshold:
                    x = (j + 0.5) * block_size
                    y = (i + 0.5) * block_size
                    deltas.append({'x': int(x), 'y': int(y), 
                                  'poincare': float(poincare_normalized)})
        
        # Filter duplicates and keep strongest, then limit to max
        cores = self._filter_singular_points(cores)
        deltas = self._filter_singular_points(deltas)
        
        # Apply max limits
        max_cores = self.config.get('max_cores', 2)
        max_deltas = self.config.get('max_deltas', 2)
        cores = cores[:max_cores]
        deltas = deltas[:max_deltas]
        
        return cores, deltas
    
    def _compute_poincare_index(self, orientation: np.ndarray, 
                                row: int, col: int) -> float:
        """
        Compute Poincaré index at a given position.
        
        The Poincaré index is the sum of orientation changes around a closed path.
        For fingerprints (half-angle representation):
        - Core: Poincaré index = +π (or +180°)
        - Delta: Poincaré index = -π (or -180°)
        """
        # Get 8-connected neighborhood positions (clockwise)
        neighbors = [
            (row - 1, col - 1), (row - 1, col), (row - 1, col + 1),
            (row, col + 1), (row + 1, col + 1), (row + 1, col),
            (row + 1, col - 1), (row, col - 1)
        ]
        
        poincare_sum = 0.0
        
        for k in range(8):
            i1, j1 = neighbors[k]
            i2, j2 = neighbors[(k + 1) % 8]
            
            # Compute orientation difference
            # Orientations are in range [-pi/2, pi/2] from doubled-angle method
            theta1 = orientation[i1, j1]
            theta2 = orientation[i2, j2]
            
            # Compute the smallest signed angle difference
            diff = theta2 - theta1
            
            # Handle wrap-around for orientation (period = pi, not 2*pi)
            # Orientation angles have 180° ambiguity
            if diff > np.pi / 2:
                diff -= np.pi
            elif diff < -np.pi / 2:
                diff += np.pi
            
            poincare_sum += diff
        
        return poincare_sum
    
    def _filter_singular_points(self, points: List[Dict], 
                                min_distance: int = 20) -> List[Dict]:
        """Filter singular points to remove duplicates and noise."""
        if not points:
            return []
        
        # Sort by absolute Poincaré value (strongest first)
        points_sorted = sorted(points, key=lambda p: abs(p['poincare']), reverse=True)
        
        filtered = []
        for point in points_sorted:
            is_duplicate = False
            for existing in filtered:
                dist = np.sqrt((point['x'] - existing['x'])**2 + 
                              (point['y'] - existing['y'])**2)
                if dist < min_distance:
                    is_duplicate = True
                    break
            
            if not is_duplicate:
                filtered.append(point)
        
        return filtered
    
    def count_ridges_core_to_delta(self, image: np.ndarray, 
                                    core: Dict, delta: Dict) -> int:
        """
        Count ridges along the line from core to delta.
        
        This is the standard TFRC (Total Fingerprint Ridge Count) method.
        Uses line profile and zero-crossing detection.
        
        Args:
            image: Grayscale fingerprint image
            core: Core point dict with 'x', 'y' keys
            delta: Delta point dict with 'x', 'y' keys
            
        Returns:
            Number of ridge crossings (integer)
        """
        # Get line coordinates from core to delta
        x1, y1 = core['x'], core['y']
        x2, y2 = delta['x'], delta['y']
        
        # Calculate line length and number of samples
        length = int(np.sqrt((x2 - x1)**2 + (y2 - y1)**2))
        if length < 5:
            return 0
        
        # Sample points along the line
        num_samples = length * 2  # Oversample for better accuracy
        x_coords = np.linspace(x1, x2, num_samples).astype(int)
        y_coords = np.linspace(y1, y2, num_samples).astype(int)
        
        # Clip to image bounds
        h, w = image.shape
        x_coords = np.clip(x_coords, 0, w - 1)
        y_coords = np.clip(y_coords, 0, h - 1)
        
        # Extract intensity profile along the line
        profile = image[y_coords, x_coords].astype(float)
        
        # Smooth the profile to reduce noise
        kernel_size = max(3, num_samples // 20)
        if kernel_size % 2 == 0:
            kernel_size += 1
        smoothed = cv2.GaussianBlur(profile.reshape(1, -1), (kernel_size, 1), 0).flatten()
        
        # Compute derivative to find crossings
        derivative = np.diff(smoothed)
        
        # Find zero crossings in derivative (peaks/valleys)
        # Each ridge-valley pair = 1 ridge crossing
        zero_crossings = np.where(np.diff(np.sign(derivative)))[0]
        
        # Count ridge crossings (divide by 2 since we count both rising and falling)
        ridge_count = len(zero_crossings) // 2
        
        return ridge_count
    
    def calculate_tfrc(self, image: np.ndarray, 
                       cores: List[Dict], deltas: List[Dict]) -> Dict[str, Any]:
        """
        Calculate Total Fingerprint Ridge Count for a single finger.
        
        Returns ridge counts for each core-delta pair and the maximum.
        
        Args:
            image: Grayscale fingerprint image
            cores: List of core points
            deltas: List of delta points
            
        Returns:
            Dictionary with ridge count information
        """
        ridge_counts = []
        
        for core in cores:
            for delta in deltas:
                count = self.count_ridges_core_to_delta(image, core, delta)
                ridge_counts.append({
                    'core': core,
                    'delta': delta,
                    'count': count
                })
        
        if not ridge_counts:
            return {
                'ridge_count': 0,
                'ridge_counts_all': [],
                'max_ridge_count': 0
            }
        
        max_count = max(rc['count'] for rc in ridge_counts)
        
        return {
            'ridge_count': max_count,  # Use max for single finger
            'ridge_counts_all': ridge_counts,
            'max_ridge_count': max_count
        }
    
    def _classify_family(self, core_count: int, 
                        delta_count: int) -> Tuple[PatternFamily, float]:
        """
        Classify pattern family based on singular point counts.
        
        Standard classification:
        - Arch: 0 cores, 0 deltas
        - Loop: 1 core, 1 delta
        - Whorl: 1-2 cores, 2 deltas
        """
        # Calculate confidence based on match to expected counts
        confidence = 0.5  # Base confidence
        
        if core_count == 0 and delta_count == 0:
            return PatternFamily.ARCH, 0.9
        
        elif core_count == 1 and delta_count == 1:
            return PatternFamily.LOOP, 0.9
        
        elif delta_count == 2 and core_count >= 1:
            return PatternFamily.WHORL, 0.9
        
        # Fuzzy matching for non-standard cases
        elif delta_count == 0:
            return PatternFamily.ARCH, 0.6
        
        elif delta_count == 1:
            return PatternFamily.LOOP, 0.7
        
        elif delta_count >= 2:
            return PatternFamily.WHORL, 0.7
        
        else:
            return PatternFamily.ACCIDENTAL, 0.4
    
    def _determine_subtype(self, image: np.ndarray,
                          orientation: np.ndarray,
                          family: PatternFamily,
                          cores: List[Dict],
                          deltas: List[Dict]) -> PatternSubtype:
        """
        Determine pattern subtype based on detailed analysis.
        """
        if family == PatternFamily.ARCH:
            return self._classify_arch_subtype(image, orientation, cores)
        
        elif family == PatternFamily.LOOP:
            return self._classify_loop_subtype(image, orientation, cores, deltas)
        
        elif family == PatternFamily.WHORL:
            return self._classify_whorl_subtype(image, orientation, cores, deltas)
        
        elif family == PatternFamily.ACCIDENTAL:
            return self._classify_accidental_subtype(image, orientation, cores, deltas)
        
        return PatternSubtype.UNKNOWN
    
    def _classify_arch_subtype(self, image: np.ndarray,
                               orientation: np.ndarray,
                               cores: List[Dict]) -> PatternSubtype:
        """Classify arch subtypes."""
        h, w = image.shape
        
        # Check for tented arch (sharp peak)
        center_region = orientation[orientation.shape[0]//3:2*orientation.shape[0]//3,
                                   orientation.shape[1]//3:2*orientation.shape[1]//3]
        
        # Measure orientation variance in center (tented has more variation)
        orientation_variance = np.var(center_region)
        
        if orientation_variance > 0.3:
            return PatternSubtype.TENTED_ARCH
        
        # Check for enclosed arch (has a small loop-like structure)
        if len(cores) > 0:
            return PatternSubtype.ENCLOSED_ARCH
        
        return PatternSubtype.SIMPLE_ARCH
    
    def _classify_loop_subtype(self, image: np.ndarray,
                               orientation: np.ndarray,
                               cores: List[Dict],
                               deltas: List[Dict]) -> PatternSubtype:
        """Classify loop subtypes based on ridge flow direction."""
        h, w = image.shape
        
        if not cores or not deltas:
            return PatternSubtype.ULNAR_LOOP  # Default
        
        core = cores[0]
        delta = deltas[0]
        
        # Determine loop direction based on delta position relative to core
        # Ulnar: delta is on the thumb side (for right hand analysis)
        # Radial: delta is on the little finger side
        
        if delta['x'] < core['x']:
            # Delta is to the left of core
            return PatternSubtype.RADIAL_LOOP
        else:
            # Delta is to the right of core
            return PatternSubtype.ULNAR_LOOP
    
    def _classify_whorl_subtype(self, image: np.ndarray,
                                orientation: np.ndarray,
                                cores: List[Dict],
                                deltas: List[Dict]) -> PatternSubtype:
        """Classify whorl subtypes based on pattern shape analysis."""
        h, w = image.shape
        
        if len(cores) >= 2:
            # Double core patterns
            core1, core2 = cores[0], cores[1]
            distance = np.sqrt((core1['x'] - core2['x'])**2 + 
                              (core1['y'] - core2['y'])**2)
            
            if distance < w * 0.2:
                return PatternSubtype.IMPLODING_WHORL
            else:
                return PatternSubtype.DOUBLE_WHORL
        
        elif len(cores) == 1:
            core = cores[0]
            
            # Analyze pattern around core
            # Check for spiral vs concentric vs elongated
            block_size = self.config['block_size']
            core_row = min(core['y'] // block_size, orientation.shape[0] - 1)
            core_col = min(core['x'] // block_size, orientation.shape[1] - 1)
            
            # Get orientation changes around core
            if core_row > 1 and core_col > 1:
                local_region = orientation[max(0, core_row-2):min(orientation.shape[0], core_row+3),
                                          max(0, core_col-2):min(orientation.shape[1], core_col+3)]
                
                # Check for concentric pattern (low variance in magnitude)
                if np.var(local_region) < 0.1:
                    return PatternSubtype.TARGET_WHORL
                
                # Check for elongated pattern (high variance in one direction)
                row_var = np.var(np.mean(local_region, axis=1))
                col_var = np.var(np.mean(local_region, axis=0))
                
                if abs(row_var - col_var) > 0.1:
                    return PatternSubtype.ELONGATED_WHORL
            
            # Default to spiral whorl
            return PatternSubtype.SPIRAL_WHORL
        
        return PatternSubtype.SPIRAL_WHORL
    
    def _classify_accidental_subtype(self, image: np.ndarray,
                                     orientation: np.ndarray,
                                     cores: List[Dict],
                                     deltas: List[Dict]) -> PatternSubtype:
        """Classify accidental/mixed patterns."""
        if len(deltas) >= 3:
            return PatternSubtype.ACCIDENTAL_WHORL
        elif len(cores) >= 2:
            return PatternSubtype.ACCIDENTAL_LOOP
        else:
            return PatternSubtype.ACCIDENTAL_ARCH
    
    def _get_subtype_name(self, subtype: PatternSubtype) -> str:
        """Get human-readable name for subtype."""
        names = {
            PatternSubtype.TARGET_WHORL: "Target Whorl",
            PatternSubtype.SPIRAL_WHORL: "Spiral Whorl",
            PatternSubtype.ELONGATED_WHORL: "Elongated Whorl",
            PatternSubtype.WHORL_COMPOSITE: "Whorl Composite",
            PatternSubtype.DOUBLE_WHORL: "Double Whorl",
            PatternSubtype.IMPLODING_WHORL: "Imploding Whorl",
            PatternSubtype.PEACOCKS_EYE: "Peacock's Eye",
            PatternSubtype.RADIAL_PEACOCK: "Radial Peacock",
            PatternSubtype.LATERAL_POCKET: "Lateral Pocket",
            PatternSubtype.RADIAL_LATERAL: "Radial Lateral",
            PatternSubtype.ULNAR_LOOP: "Ulnar Loop",
            PatternSubtype.RADIAL_LOOP: "Radial Loop",
            PatternSubtype.FALLING_LOOP: "Falling Loop",
            PatternSubtype.RADIAL_FALLING: "Radial Falling",
            PatternSubtype.SIMPLE_ARCH: "Simple Arch",
            PatternSubtype.TENTED_ARCH: "Tented Arch",
            PatternSubtype.ENCLOSED_ARCH: "Enclosed Arch",
            PatternSubtype.ARCH_ULNAR_LOOP: "Arch with Ulnar Loop",
            PatternSubtype.ARCH_RADIAL_LOOP: "Arch with Radial Loop",
            PatternSubtype.ACCIDENTAL_LOOP: "Accidental Loop",
            PatternSubtype.ACCIDENTAL_WHORL: "Accidental Whorl",
            PatternSubtype.ACCIDENTAL_ARCH: "Accidental Arch",
            PatternSubtype.MALFORMATION: "Malformation",
            PatternSubtype.UNKNOWN: "Unknown"
        }
        return names.get(subtype, "Unknown")
    
    def visualize(self, image: np.ndarray, 
                 classification: Dict[str, Any],
                 output_path: str = None) -> np.ndarray:
        """
        Visualize classification results on the image.
        
        Args:
            image: Original fingerprint image
            classification: Result from classify()
            output_path: Optional path to save visualization
            
        Returns:
            Annotated image with singular points marked
        """
        # Convert to color for visualization
        if len(image.shape) == 2:
            vis_image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
        else:
            vis_image = image.copy()
        
        # Draw core points (red circles)
        for core in classification['singular_points']['cores']:
            cv2.circle(vis_image, (core['x'], core['y']), 10, (0, 0, 255), 2)
            cv2.circle(vis_image, (core['x'], core['y']), 3, (0, 0, 255), -1)
        
        # Draw delta/triradii points (blue triangles)
        for delta in classification['singular_points']['deltas']:
            pts = np.array([
                [delta['x'], delta['y'] - 10],
                [delta['x'] - 8, delta['y'] + 6],
                [delta['x'] + 8, delta['y'] + 6]
            ], np.int32)
            cv2.polylines(vis_image, [pts], True, (255, 0, 0), 2)
        
        # Add text label
        label = f"{classification['family'].upper()}: {classification['subtype_name']}"
        cv2.putText(vis_image, label, (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        conf_label = f"Confidence: {classification['confidence']:.2f}"
        cv2.putText(vis_image, conf_label, (10, 60),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
        
        if output_path:
            cv2.imwrite(output_path, vis_image)
            logger.info(f"💾 Visualization saved to: {output_path}")
        
        return vis_image


# Convenience function
def classify_fingerprint(image: np.ndarray) -> Dict[str, Any]:
    """
    Convenience function to classify a fingerprint pattern.
    
    Args:
        image: Grayscale fingerprint image
        
    Returns:
        Classification result dictionary
    """
    classifier = PatternClassifier()
    return classifier.classify(image)


if __name__ == "__main__":
    # Test with sample image
    import os
    
    test_image_path = "sample data/00000_00.bmp"
    
    if os.path.exists(test_image_path):
        image = cv2.imread(test_image_path, cv2.IMREAD_GRAYSCALE)
        
        classifier = PatternClassifier()
        result = classifier.classify(image)
        
        print("\n" + "="*50)
        print("PATTERN CLASSIFICATION RESULT")
        print("="*50)
        print(f"Family: {result['family']}")
        print(f"Subtype: {result['subtype']} ({result['subtype_name']})")
        print(f"Cores: {result['core_count']}")
        print(f"Triradii: {result['triradii_count']}")
        print(f"Confidence: {result['confidence']:.2f}")
        
        # Save visualization
        os.makedirs("test_output", exist_ok=True)
        classifier.visualize(image, result, "test_output/pattern_classification.png")
    else:
        print(f"Test image not found: {test_image_path}")
