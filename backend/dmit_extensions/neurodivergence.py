from typing import Dict, Any
from .base import DMITExtensionBase

class NeurodivergenceExtension(DMITExtensionBase):
    """
    Extension for analyzing Neurodivergence tendencies from fingerprint features.
    Uses comprehensive DMIT scientific correlations between fingerprint patterns and neurodivergence markers.
    """
    def analyze(self, features: Dict[str, Any]) -> Dict[str, Any]:
        # Extract comprehensive fingerprint features for neurodivergence analysis
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

        # DMIT research: Neurodivergence is often associated with high entropy, high fractal complexity, unusual pattern types, and high/low TFRC
        entropy_score = min(1.0, entropy / 8.0)
        fractal_score = min(1.0, fractal_complexity)
        pattern_score = 1.0 if pattern_type.lower() in ['composite', 'tented_arch'] else 0.5
        # Flag only genuinely atypical ridge counts when TFRC was measured.
        tfrc_score = 0.5
        if isinstance(tfrc, (int, float)) and tfrc > 0:
            tfrc_score = 1.0 if (tfrc < 0.2 or tfrc > 0.9) else 0.5
        lacunarity_score = min(1.0, lacunarity)
        box_dim_score = (box_counting_dimension - 1.5) / 0.5 if 1.5 <= box_counting_dimension <= 2.0 else 0.5
        spectral_score = min(1.0, spectral_entropy)
        # FIX: the old binary threshold (> 0.15) was always true for any real
        # print, making this component a constant 1.0. Minutiae density now
        # arrives normalized to [0,1] (typical ~0.3-0.45); score it proportionally
        # so atypically dense ridge-event fields raise the index gradually.
        minutiae_score = 0.5 + 0.5 * max(0.0, min(1.0, (minutiae_density - 0.15) / 0.45))
        topological_score = min(1.0, topological_complexity)

        # Weighted sum for neurodivergence index
        neurodivergence_index = (
            entropy_score * 0.20 +
            fractal_score * 0.15 +
            pattern_score * 0.13 +
            tfrc_score * 0.12 +
            lacunarity_score * 0.10 +
            box_dim_score * 0.10 +
            spectral_score * 0.08 +
            minutiae_score * 0.06 +
            topological_score * 0.06
        )
        neurodivergence_index = max(0.0, min(1.0, neurodivergence_index))

        # Classification
        if neurodivergence_index >= 0.8:
            level = "Highly Neurodivergent"
        elif neurodivergence_index >= 0.6:
            level = "Moderately Neurodivergent"
        elif neurodivergence_index >= 0.4:
            level = "Mildly Neurodivergent"
        else:
            level = "Neurotypical"

        return {
            'neurodivergence_index': neurodivergence_index,
            'neurodivergence_level': level,
            'entropy_score': entropy_score,
            'fractal_score': fractal_score,
            'pattern_score': pattern_score,
            'tfrc_score': tfrc_score,
            'lacunarity_score': lacunarity_score,
            'box_dim_score': box_dim_score,
            'spectral_score': spectral_score,
            'minutiae_score': minutiae_score,
            'topological_score': topological_score
        } 