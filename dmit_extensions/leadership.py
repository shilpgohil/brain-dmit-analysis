from typing import Dict, Any
from .base import DMITExtensionBase

class LeadershipExtension(DMITExtensionBase):
    """
    Extension for analyzing Leadership abilities from fingerprint features.
    Uses comprehensive DMIT scientific correlations between fingerprint patterns and leadership processes.
    """
    def analyze(self, features: Dict[str, Any]) -> Dict[str, Any]:
        # Extract comprehensive fingerprint features for leadership analysis
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
        # Leadership sub-abilities
        strategic_vision = self._calculate_strategic_vision(information_dimension, entropy, pattern_symmetry, spectral_entropy)
        influence = self._calculate_influence(correlation_dimension, graph_density, betweenness_centrality, information_dimension)
        decision_making = self._calculate_decision_making(tfrc, box_counting_dimension, h1_num_features, betti_1)
        team_building = self._calculate_team_building(spectral_radius, topological_complexity, euler_characteristic, spectral_bandwidth)
        adaptability = self._calculate_adaptability(ridge_density, clustering_coefficient, modularity, ridge_thickness)
        communication = self._calculate_communication(ridge_uniformity, pattern_type, ridge_curvature, community_cohesion)
        resilience = self._calculate_resilience(pattern_regularity, lacunarity, ridge_continuity, std_intensity)
        innovation = self._calculate_innovation(spectral_centroid, spectral_rolloff, graph_density, topological_complexity)
        # Overall leadership score
        leadership_score = (
            strategic_vision * 0.18 +
            influence * 0.16 +
            decision_making * 0.15 +
            team_building * 0.15 +
            adaptability * 0.12 +
            communication * 0.10 +
            resilience * 0.08 +
            innovation * 0.06
        )
        leadership_score = max(0.0, min(1.0, leadership_score))
        leadership_styles = {
            'visionary': (strategic_vision + innovation) / 2,
            'influential': (influence + communication) / 2,
            'decisive': (decision_making + resilience) / 2,
            'team_builder': (team_building + adaptability) / 2,
            'adaptive': (adaptability + resilience) / 2,
            'innovative': (innovation + strategic_vision) / 2
        }
        primary_style = max(leadership_styles.items(), key=lambda x: x[1])[0]
        return {
            'leadership_score': leadership_score,
            'primary_leadership_style': primary_style,
            'strategic_vision': strategic_vision,
            'influence': influence,
            'decision_making': decision_making,
            'team_building': team_building,
            'adaptability': adaptability,
            'communication': communication,
            'resilience': resilience,
            'innovation': innovation,
            'leadership_profile': self.classify_leadership_level(leadership_score)
        }
    def _calculate_strategic_vision(self, information_dimension: float, entropy: float, pattern_symmetry: float, spectral_entropy: float) -> float:
        if 1.5 <= information_dimension <= 2.0:
            info_score = (information_dimension - 1.5) / 0.5
        else:
            info_score = 0.5
        entropy_score = min(1.0, entropy / 8.0) if entropy > 0 else 0.5
        symmetry_score = min(1.0, pattern_symmetry)
        spectral_score = min(1.0, spectral_entropy)
        return min(1.0, info_score * 0.35 + entropy_score * 0.25 + symmetry_score * 0.25 + spectral_score * 0.15)
    def _calculate_influence(self, correlation_dimension: float, graph_density: float, betweenness_centrality: float, information_dimension: float) -> float:
        if 1.5 <= correlation_dimension <= 2.0:
            corr_score = (correlation_dimension - 1.5) / 0.5
        else:
            corr_score = 0.5
        density_score = min(1.0, graph_density)
        centrality_score = min(1.0, betweenness_centrality)
        info_score = (information_dimension - 1.5) / 0.5 if 1.5 <= information_dimension <= 2.0 else 0.5
        return min(1.0, corr_score * 0.3 + density_score * 0.25 + centrality_score * 0.25 + info_score * 0.2)
    def _calculate_decision_making(self, tfrc: int, box_counting_dimension: float, h1_num_features: int, betti_1: int) -> float:
        ridge_score = min(1.0, float(tfrc or 0))  # FIX: per-finger TFRC 0-30, not 0-1500 if tfrc > 0 else 0.0
        fractal_score = (box_counting_dimension - 1.5) / 0.5 if 1.5 <= box_counting_dimension <= 2.0 else 0.5
        h1_score = min(1.0, h1_num_features / 10.0)
        betti_score = min(1.0, betti_1 / 10.0)
        return min(1.0, ridge_score * 0.35 + fractal_score * 0.25 + h1_score * 0.25 + betti_score * 0.15)
    def _calculate_team_building(self, spectral_radius: float, topological_complexity: float, euler_characteristic: int, spectral_bandwidth: float) -> float:
        spectral_score = min(1.0, spectral_radius / 10.0) if spectral_radius > 0 else 0.5
        complexity_score = min(1.0, topological_complexity)
        euler_score = min(1.0, euler_characteristic / 10.0) if euler_characteristic > 0 else 0.5
        bandwidth_score = min(1.0, spectral_bandwidth)
        return min(1.0, spectral_score * 0.3 + complexity_score * 0.25 + euler_score * 0.25 + bandwidth_score * 0.2)
    def _calculate_adaptability(self, ridge_density: float, clustering_coefficient: float, modularity: float, ridge_thickness: float) -> float:
        density_score = min(1.0, ridge_density)
        clustering_score = min(1.0, clustering_coefficient)
        modularity_score = min(1.0, modularity)
        thickness_score = min(1.0, ridge_thickness)
        return min(1.0, density_score * 0.3 + clustering_score * 0.25 + modularity_score * 0.25 + thickness_score * 0.2)
    def _calculate_communication(self, ridge_uniformity: float, pattern_type: str, ridge_curvature: float, community_cohesion: float) -> float:
        uniformity_score = min(1.0, ridge_uniformity)
        pattern_weights = {'whorl': 0.8, 'loop': 0.7, 'arch': 0.6, 'tented_arch': 0.65, 'composite': 0.75}
        pattern_score = pattern_weights.get(pattern_type.lower(), 0.6)
        curvature_score = min(1.0, ridge_curvature)
        cohesion_score = min(1.0, community_cohesion)
        return min(1.0, uniformity_score * 0.3 + pattern_score * 0.25 + curvature_score * 0.25 + cohesion_score * 0.2)
    def _calculate_resilience(self, pattern_regularity: float, lacunarity: float, ridge_continuity: float, std_intensity: float) -> float:
        regularity_score = min(1.0, pattern_regularity)
        lacunarity_score = max(0.0, 1.0 - lacunarity)
        continuity_score = min(1.0, ridge_continuity)
        std_score = max(0.0, 1.0 - (std_intensity / 100.0)) if std_intensity > 0 else 0.5
        return min(1.0, regularity_score * 0.3 + lacunarity_score * 0.25 + continuity_score * 0.25 + std_score * 0.2)
    def _calculate_innovation(self, spectral_centroid: float, spectral_rolloff: float, graph_density: float, topological_complexity: float) -> float:
        centroid_score = min(1.0, spectral_centroid)
        rolloff_score = min(1.0, spectral_rolloff)
        density_score = min(1.0, graph_density)
        complexity_score = min(1.0, topological_complexity)
        return min(1.0, centroid_score * 0.3 + rolloff_score * 0.25 + density_score * 0.25 + complexity_score * 0.2)
    @staticmethod
    def classify_leadership_level(score: float) -> str:
        if score >= 0.8:
            return "Excellent"
        elif score >= 0.7:
            return "Very Good"
        elif score >= 0.6:
            return "Good"
        elif score >= 0.5:
            return "Average"
        elif score >= 0.4:
            return "Below Average"
        else:
            return "Needs Development" 