from typing import Dict, Any
from .base import DMITExtensionBase

class StressManagementExtension(DMITExtensionBase):
    """
    Extension for analyzing Stress Management and resilience abilities from fingerprint features.
    Uses comprehensive DMIT scientific correlations between fingerprint patterns and stress management capabilities.
    """
    def analyze(self, features: Dict[str, Any]) -> Dict[str, Any]:
        # Extract comprehensive fingerprint features for stress management analysis
        # Ridge count and density features
        # tfrc already extracted above
        ridge_density = features.get('ridge_density', 0.0)
        tfrc = features.get('tfrc_normalized', min(1.0, float(features.get('tfrc', 0) or 0) / 25.0))  # FIX: normalized 0-1
        ridge_continuity = features.get('ridge_continuity', 0.0)
        ridge_uniformity = features.get('ridge_uniformity', 0.0)
        ridge_thickness = features.get('mean_ridge_thickness', 0.0)
        ridge_orientation = features.get('mean_ridge_orientation', 0.0)
        ridge_curvature = features.get('mean_ridge_curvature', 0.0)
        
        # Pattern analysis features
        pattern_type = features.get('pattern_type', 'loop')
        pattern_symmetry = features.get('pattern_symmetry', 0.0)
        pattern_regularity = features.get('pattern_regularity', 0.0)
        whorl_complexity = features.get('whorl_complexity', 0.0)
        
        # Fractal and complexity features
        box_counting_dimension = features.get('box_counting_dimension', 1.5)
        correlation_dimension = features.get('correlation_dimension', 1.5)
        information_dimension = features.get('information_dimension', 1.5)
        lacunarity = features.get('lacunarity', 0.0)
        fractal_complexity = features.get('fractal_complexity', 0.0)
        
        # Graph and network features
        graph_density = features.get('graph_density', 0.0)
        clustering_coefficient = features.get('clustering_coefficient', 0.0)
        spectral_radius = features.get('spectral_radius', 0.0)
        betweenness_centrality = features.get('betweenness_centrality', 0.0)
        modularity = features.get('modularity', 0.0)
        community_cohesion = features.get('community_cohesion', 0.0)
        
        # Topological features
        euler_characteristic = features.get('euler_characteristic', 0)
        topological_complexity = features.get('topological_complexity', 0.0)
        h1_num_features = features.get('h1_num_features', 0)  # Loop/hole count
        betti_0 = features.get('betti_0', 0)  # Connected components
        betti_1 = features.get('betti_1', 0)  # Loops/holes
        
        # Statistical features
        entropy = features.get('entropy', 0.0)
        std_intensity = features.get('std_intensity', 0.0)
        minutiae_density = features.get('minutiae_density', 0.0)
        minutiae_count = features.get('minutiae_count', 0)
        
        # Spectral features
        spectral_energy = features.get('spectral_energy', 0.0)
        spectral_entropy = features.get('spectral_entropy', 0.0)
        spectral_centroid = features.get('spectral_centroid', 0.0)
        spectral_bandwidth = features.get('spectral_bandwidth', 0.0)
        spectral_rolloff = features.get('spectral_rolloff', 0.0)
        
        # Micro-features
        pore_density = features.get('pore_density', 0.0)
        pore_count = features.get('pore_count', 0)
        
        # Calculate stress management abilities using comprehensive DMIT scientific correlations
        
        # 1. Stress Resilience Analysis (DMIT Principle: High information dimension + entropy = stress resilience)
        stress_resilience = self._calculate_stress_resilience(information_dimension, entropy, 
                                                            pattern_symmetry, spectral_entropy)
        
        # 2. Emotional Regulation Analysis (DMIT Principle: High ridge density + clustering coefficient = emotional regulation)
        emotional_regulation = self._calculate_emotional_regulation(ridge_density, clustering_coefficient, 
                                                                  modularity, ridge_thickness)
        
        # 3. Coping Mechanisms Analysis (DMIT Principle: High correlation dimension + graph density = coping mechanisms)
        coping_mechanisms = self._calculate_coping_mechanisms(correlation_dimension, graph_density, 
                                                            betweenness_centrality, information_dimension)
        
        # 4. Stress Adaptation Analysis (DMIT Principle: High community cohesion + spectral radius = stress adaptation)
        stress_adaptation = self._calculate_stress_adaptation(community_cohesion, spectral_radius, 
                                                            topological_complexity, euler_characteristic)
        
        # 5. Mental Stability Analysis (DMIT Principle: High ridge count + fractal dimension = mental stability)
        mental_stability = self._calculate_result(tfrc, box_counting_dimension, 
                                                          h1_num_features, betti_1)
        
        # 6. Stress Tolerance Analysis (DMIT Principle: High pattern regularity + low lacunarity = stress tolerance)
        stress_tolerance = self._calculate_stress_tolerance(pattern_regularity, lacunarity, 
                                                          ridge_continuity, std_intensity)
        
        # 7. Recovery Ability Analysis (DMIT Principle: High ridge uniformity + pattern type = recovery ability)
        recovery_ability = self._calculate_recovery_ability(ridge_uniformity, pattern_type, 
                                                          ridge_curvature, spectral_energy)
        
        # 8. Adaptive Response Analysis (DMIT Principle: High spectral features + graph complexity = adaptive response)
        adaptive_response = self._calculate_adaptive_response(spectral_centroid, spectral_rolloff, 
                                                            graph_density, topological_complexity)
        
        # Calculate overall stress management score
        stress_management_score = (
            stress_resilience * 0.20 +               # Stress resilience is fundamental
            emotional_regulation * 0.18 +            # Emotional regulation is crucial
            coping_mechanisms * 0.15 +               # Coping mechanisms is important
            stress_adaptation * 0.15 +               # Stress adaptation is essential
            mental_stability * 0.12 +                # Mental stability
            stress_tolerance * 0.10 +                # Stress tolerance
            recovery_ability * 0.07 +                # Recovery ability
            adaptive_response * 0.03                 # Adaptive response
        )
        
        # Normalize to 0-1 range
        stress_management_score = max(0.0, min(1.0, stress_management_score))
        
        # Determine stress management style based on dominant features
        stress_styles = {
            'resilient_handler': (stress_resilience + stress_tolerance) / 2,
            'emotional_regulator': (emotional_regulation + recovery_ability) / 2,
            'adaptive_coper': (coping_mechanisms + adaptive_response) / 2,
            'stable_processor': (mental_stability + stress_adaptation) / 2,
            'balanced_manager': (stress_resilience + emotional_regulation) / 2,
            'recovery_focused': (recovery_ability + adaptive_response) / 2
        }
        primary_style = max(stress_styles.items(), key=lambda x: x[1])[0]
        
        return {
            'stress_management_score': stress_management_score,
            'primary_stress_style': primary_style,
            'stress_resilience': stress_resilience,
            'emotional_regulation': emotional_regulation,
            'coping_mechanisms': coping_mechanisms,
            'stress_adaptation': stress_adaptation,
            'mental_stability': mental_stability,
            'stress_tolerance': stress_tolerance,
            'recovery_ability': recovery_ability,
            'adaptive_response': adaptive_response,
            'resilience_capacity': (stress_resilience + stress_tolerance) / 2,
            'emotional_capacity': (emotional_regulation + recovery_ability) / 2,
            'coping_capacity': (coping_mechanisms + adaptive_response) / 2,
            'stability_capacity': (mental_stability + stress_adaptation) / 2,
            'stress_handling': (stress_resilience + emotional_regulation) / 2,
            'stress_management_profile': self.classify_stress_management_level(stress_management_score)
        }

    def _calculate_stress_resilience(self, information_dimension: float, entropy: float,
                                   pattern_symmetry: float, spectral_entropy: float) -> float:
        """Calculate stress resilience from fingerprint features (DMIT principle)"""
        # DMIT research shows: High information dimension + entropy = stress resilience
        
        # Information dimension contribution
        if 1.5 <= information_dimension <= 2.0:
            info_score = (information_dimension - 1.5) / 0.5
        else:
            info_score = 0.5
        
        # Entropy contribution (higher entropy = more complex stress resilience)
        if entropy > 0:
            entropy_score = min(1.0, entropy / 8.0)  # Normalize to 0-1
        else:
            entropy_score = 0.5
        
        # Pattern symmetry contribution
        symmetry_score = min(1.0, pattern_symmetry)
        
        # Spectral entropy contribution
        spectral_score = min(1.0, spectral_entropy)
        
        # Combine scores
        stress_resilience = (info_score * 0.35 + entropy_score * 0.25 + symmetry_score * 0.25 + spectral_score * 0.15)
        return min(1.0, stress_resilience)
    
    def _calculate_emotional_regulation(self, ridge_density: float, clustering_coefficient: float,
                                      modularity: float, ridge_thickness: float) -> float:
        """Calculate emotional regulation from fingerprint features (DMIT principle)"""
        # DMIT research shows: High ridge density + clustering coefficient = emotional regulation
        
        # Ridge density contribution
        density_score = min(1.0, ridge_density)
        
        # Clustering coefficient contribution
        clustering_score = min(1.0, clustering_coefficient)
        
        # Modularity contribution
        modularity_score = min(1.0, modularity)
        
        # Ridge thickness contribution
        thickness_score = min(1.0, ridge_thickness)
        
        # Combine scores
        emotional_regulation = (density_score * 0.3 + clustering_score * 0.25 + modularity_score * 0.25 + thickness_score * 0.2)
        return min(1.0, emotional_regulation)
    
    def _calculate_coping_mechanisms(self, correlation_dimension: float, graph_density: float,
                                   betweenness_centrality: float, information_dimension: float) -> float:
        """Calculate coping mechanisms from fingerprint features (DMIT principle)"""
        # DMIT research shows: High correlation dimension + graph density = coping mechanisms
        
        # Correlation dimension contribution
        if 1.5 <= correlation_dimension <= 2.0:
            corr_score = (correlation_dimension - 1.5) / 0.5
        else:
            corr_score = 0.5
        
        # Graph density contribution
        density_score = min(1.0, graph_density)
        
        # Betweenness centrality contribution
        centrality_score = min(1.0, betweenness_centrality)
        
        # Information dimension contribution
        if 1.5 <= information_dimension <= 2.0:
            info_score = (information_dimension - 1.5) / 0.5
        else:
            info_score = 0.5
        
        # Combine scores
        coping_mechanisms = (corr_score * 0.3 + density_score * 0.25 + centrality_score * 0.25 + info_score * 0.2)
        return min(1.0, coping_mechanisms)
    
    def _calculate_stress_adaptation(self, community_cohesion: float, spectral_radius: float,
                                   topological_complexity: float, euler_characteristic: int) -> float:
        """Calculate stress adaptation from fingerprint features (DMIT principle)"""
        # DMIT research shows: High community cohesion + spectral radius = stress adaptation
        
        # Community cohesion contribution
        cohesion_score = min(1.0, community_cohesion)
        
        # Spectral radius contribution
        if spectral_radius > 0:
            spectral_score = min(1.0, spectral_radius / 10.0)
        else:
            spectral_score = 0.5
        
        # Topological complexity contribution
        complexity_score = min(1.0, topological_complexity)
        
        # Euler characteristic contribution (more negative = more complex = better stress adaptation)
        if euler_characteristic < 0:
            euler_score = min(1.0, abs(euler_characteristic) / 10.0)
        else:
            euler_score = 0.3
        
        # Combine scores
        stress_adaptation = (cohesion_score * 0.3 + spectral_score * 0.25 + complexity_score * 0.25 + euler_score * 0.2)
        return min(1.0, stress_adaptation)
    
    def _calculate_result(self, tfrc: int, box_counting_dimension: float,
                         h1_num_features: int, betti_1: int) -> float:
        """Calculate mental stability from fingerprint features (DMIT principle)"""
        # DMIT research shows: High ridge count + fractal dimension = mental stability
        # Ridge count contribution
        if tfrc > 0:
            ridge_score = min(1.0, float(tfrc or 0))  # FIX: per-finger TFRC 0-30, not 0-1500
        else:
            ridge_score = 0.0
        # Fractal dimension contribution
        if 1.5 <= box_counting_dimension <= 2.0:
            fractal_score = (box_counting_dimension - 1.5) / 0.5
        else:
            fractal_score = 0.5
        # H1 features contribution (loops/holes - complexity in mental stability)
        h1_score = min(1.0, h1_num_features / 10.0)
        # Betti-1 contribution (loops)
        betti_score = min(1.0, betti_1 / 10.0)
        # Combine scores
        mental_stability = (ridge_score * 0.35 + fractal_score * 0.25 + h1_score * 0.25 + betti_score * 0.15)
        return min(1.0, mental_stability)

    def _calculate_stress_tolerance(self, pattern_regularity: float, lacunarity: float,
                                    ridge_continuity: float, std_intensity: float) -> float:
        """Calculate stress tolerance from fingerprint features (DMIT principle)"""
        # Pattern regularity contribution
        regularity_score = min(1.0, pattern_regularity)
        # Lacunarity (lower is better)
        lacunarity_score = 1.0 - min(1.0, lacunarity)
        # Ridge continuity contribution
        continuity_score = min(1.0, ridge_continuity)
        # Intensity std contribution
        intensity_score = min(1.0, std_intensity)
        # Combine scores
        stress_tolerance = (regularity_score * 0.35 + lacunarity_score * 0.25 +
                            continuity_score * 0.25 + intensity_score * 0.15)
        return min(1.0, stress_tolerance)

    def _calculate_recovery_ability(self, ridge_uniformity: float, pattern_type: str,
                                    ridge_curvature: float, spectral_energy: float) -> float:
        """Calculate recovery ability from fingerprint features (DMIT principle)"""
        # Ridge uniformity contribution
        uniformity_score = min(1.0, ridge_uniformity)
        # Pattern type contribution (assign a score based on type)
        pattern_score = 1.0 if pattern_type == 'whorl' else 0.7 if pattern_type == 'loop' else 0.5
        # Ridge curvature contribution
        curvature_score = min(1.0, ridge_curvature)
        # Spectral energy contribution
        spectral_score = min(1.0, spectral_energy)
        # Combine scores
        recovery_ability = (uniformity_score * 0.35 + pattern_score * 0.25 +
                            curvature_score * 0.25 + spectral_score * 0.15)
        return min(1.0, recovery_ability)

    def _calculate_adaptive_response(self, spectral_centroid: float, spectral_rolloff: float,
                                    graph_density: float, topological_complexity: float) -> float:
        """Calculate adaptive response from fingerprint features (DMIT principle)"""
        # Spectral centroid contribution
        centroid_score = min(1.0, spectral_centroid)
        # Spectral rolloff contribution
        rolloff_score = min(1.0, spectral_rolloff)
        # Graph density contribution
        density_score = min(1.0, graph_density)
        # Topological complexity contribution
        complexity_score = min(1.0, topological_complexity)
        # Combine scores
        adaptive_response = (centroid_score * 0.3 + rolloff_score * 0.25 +
                             density_score * 0.25 + complexity_score * 0.2)
        return min(1.0, adaptive_response)

    @staticmethod
    def classify_stress_management_level(score: float) -> str:
        if score >= 0.85:
            return "Exceptional Stress Management"
        elif score >= 0.75:
            return "High Stress Management"
        elif score >= 0.65:
            return "Above Average Stress Management"
        elif score >= 0.55:
            return "Average Stress Management"
        else:
            return "Developing Stress Management" 