from typing import Dict, Any
from .base import DMITExtensionBase

class PatternRecognitionExtension(DMITExtensionBase):
    """
    Extension for analyzing Pattern Recognition abilities from fingerprint features.
    Uses comprehensive DMIT scientific correlations between fingerprint patterns and pattern recognition processes.
    """
    def analyze(self, features: Dict[str, Any]) -> Dict[str, Any]:
        # Extract comprehensive fingerprint features for pattern recognition analysis
        # tfrc already extracted above
        ridge_density = features.get('ridge_density', 0.0)
        tfrc = features.get('tfrc_normalized', min(1.0, float(features.get('tfrc', 0) or 0) / 25.0))  # FIX: normalized 0-1
        ridge_continuity = features.get('ridge_continuity', 0.0)
        ridge_uniformity = features.get('ridge_uniformity', 0.0)
        ridge_thickness = features.get('mean_ridge_thickness', 0.0)
        ridge_orientation = features.get('mean_ridge_orientation', 0.0)
        ridge_curvature = features.get('mean_ridge_curvature', 0.0)
        pattern_type = features.get('pattern_type', 'loop')
        pattern_symmetry = features.get('pattern_symmetry', 0.0)
        pattern_regularity = features.get('pattern_regularity', 0.0)
        whorl_complexity = features.get('whorl_complexity', 0.0)
        box_counting_dimension = features.get('box_counting_dimension', 1.5)
        correlation_dimension = features.get('correlation_dimension', 1.5)
        information_dimension = features.get('information_dimension', 1.5)
        lacunarity = features.get('lacunarity', 0.0)
        fractal_complexity = features.get('fractal_complexity', 0.0)
        graph_density = features.get('graph_density', 0.0)
        clustering_coefficient = features.get('clustering_coefficient', 0.0)
        spectral_radius = features.get('spectral_radius', 0.0)
        betweenness_centrality = features.get('betweenness_centrality', 0.0)
        modularity = features.get('modularity', 0.0)
        community_cohesion = features.get('community_cohesion', 0.0)
        euler_characteristic = features.get('euler_characteristic', 0)
        topological_complexity = features.get('topological_complexity', 0.0)
        h1_num_features = features.get('h1_num_features', 0)
        betti_0 = features.get('betti_0', 0)
        betti_1 = features.get('betti_1', 0)
        entropy = features.get('entropy', 0.0)
        std_intensity = features.get('std_intensity', 0.0)
        minutiae_density = features.get('minutiae_density', 0.0)
        minutiae_count = features.get('minutiae_count', 0)
        spectral_energy = features.get('spectral_energy', 0.0)
        spectral_entropy = features.get('spectral_entropy', 0.0)
        spectral_centroid = features.get('spectral_centroid', 0.0)
        spectral_bandwidth = features.get('spectral_bandwidth', 0.0)
        spectral_rolloff = features.get('spectral_rolloff', 0.0)
        pore_density = features.get('pore_density', 0.0)
        pore_count = features.get('pore_count', 0)

        # DMIT research: Pattern recognition is associated with high pattern regularity, symmetry, ridge continuity, and fractal complexity
        regularity_score = min(1.0, pattern_regularity)
        symmetry_score = min(1.0, pattern_symmetry)
        continuity_score = min(1.0, ridge_continuity)
        fractal_score = min(1.0, fractal_complexity)
        box_dim_score = (box_counting_dimension - 1.5) / 0.5 if 1.5 <= box_counting_dimension <= 2.0 else 0.5
        entropy_score = min(1.0, entropy / 8.0)
        spectral_score = min(1.0, spectral_entropy)
        # FIX: the old binary threshold (> 0.12) was always true for any real
        # print, making this component a constant 1.0. Score proportionally on
        # the normalized [0,1] density instead.
        minutiae_score = 0.5 + 0.5 * max(0.0, min(1.0, (minutiae_density - 0.12) / 0.48))
        ridge_score = min(1.0, ridge_density)
        tfrc_score = min(1.0, float(tfrc or 0))  # FIX: per-finger TFRC 0-30, not 0-1500 if tfrc > 0 else 0.0

        # Weighted sum for pattern recognition index
        pattern_recognition_index = (
            regularity_score * 0.18 +
            symmetry_score * 0.16 +
            continuity_score * 0.14 +
            fractal_score * 0.13 +
            box_dim_score * 0.10 +
            entropy_score * 0.09 +
            spectral_score * 0.08 +
            minutiae_score * 0.06 +
            ridge_score * 0.04 +
            tfrc_score * 0.02
        )
        pattern_recognition_index = max(0.0, min(1.0, pattern_recognition_index))

        # Classification
        if pattern_recognition_index >= 0.8:
            level = "Exceptional"
        elif pattern_recognition_index >= 0.7:
            level = "Excellent"
        elif pattern_recognition_index >= 0.6:
            level = "Very Good"
        elif pattern_recognition_index >= 0.5:
            level = "Good"
        elif pattern_recognition_index >= 0.4:
            level = "Average"
        else:
            level = "Needs Development"

        return {
            'pattern_recognition_index': pattern_recognition_index,
            'pattern_recognition_level': level,
            'regularity_score': regularity_score,
            'symmetry_score': symmetry_score,
            'continuity_score': continuity_score,
            'fractal_score': fractal_score,
            'box_dim_score': box_dim_score,
            'entropy_score': entropy_score,
            'spectral_score': spectral_score,
            'minutiae_score': minutiae_score,
            'ridge_score': ridge_score,
            'tfrc_score': tfrc_score
        } 