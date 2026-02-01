from typing import Dict, Any
from .base import DMITExtensionBase

class RiskToleranceExtension(DMITExtensionBase):
    """
    Extension for analyzing Risk Tolerance from fingerprint features.
    Uses comprehensive DMIT scientific correlations between fingerprint patterns and risk tolerance.
    """
    def analyze(self, features: Dict[str, Any]) -> Dict[str, Any]:
        # Extract comprehensive fingerprint features for risk tolerance analysis
        # tfrc already extracted above
        ridge_density = features.get('ridge_density', 0.0)
        tfrc = features.get('tfrc', 0)
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

        # DMIT research: Risk tolerance is associated with high ridge density, high entropy, high graph density, and certain pattern types
        density_score = min(1.0, ridge_density)
        entropy_score = min(1.0, entropy / 8.0)
        graph_score = min(1.0, graph_density)
        pattern_score = 1.0 if pattern_type.lower() in ['whorl', 'composite'] else 0.5
        continuity_score = min(1.0, ridge_continuity)
        modularity_score = min(1.0, modularity)
        spectral_score = min(1.0, spectral_entropy)
        tfrc_score = min(1.0, tfrc / 1500.0) if tfrc > 0 else 0.0
        fractal_score = min(1.0, fractal_complexity)
        regularity_score = min(1.0, pattern_regularity)

        # Weighted sum for risk tolerance index
        risk_tolerance_index = (
            density_score * 0.18 +
            entropy_score * 0.16 +
            graph_score * 0.14 +
            pattern_score * 0.13 +
            continuity_score * 0.10 +
            modularity_score * 0.08 +
            spectral_score * 0.08 +
            tfrc_score * 0.07 +
            fractal_score * 0.04 +
            regularity_score * 0.02
        )
        risk_tolerance_index = max(0.0, min(1.0, risk_tolerance_index))

        # Classification
        if risk_tolerance_index >= 0.8:
            level = "Very High"
        elif risk_tolerance_index >= 0.7:
            level = "High"
        elif risk_tolerance_index >= 0.6:
            level = "Above Average"
        elif risk_tolerance_index >= 0.5:
            level = "Average"
        elif risk_tolerance_index >= 0.4:
            level = "Below Average"
        else:
            level = "Low"

        return {
            'risk_tolerance_index': risk_tolerance_index,
            'risk_tolerance_level': level,
            'density_score': density_score,
            'entropy_score': entropy_score,
            'graph_score': graph_score,
            'pattern_score': pattern_score,
            'continuity_score': continuity_score,
            'modularity_score': modularity_score,
            'spectral_score': spectral_score,
            'tfrc_score': tfrc_score,
            'fractal_score': fractal_score,
            'regularity_score': regularity_score
        } 