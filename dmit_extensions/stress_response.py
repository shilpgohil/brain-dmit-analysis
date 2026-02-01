from typing import Dict, Any
from .base import DMITExtensionBase

class StressResponseExtension(DMITExtensionBase):
    """
    Extension for analyzing Stress Response abilities from fingerprint features.
    Uses comprehensive DMIT scientific correlations between fingerprint patterns and stress response processes.
    """
    def analyze(self, features: Dict[str, Any]) -> Dict[str, Any]:
        # Extract comprehensive fingerprint features for stress response analysis
        # Ridge count and density features
        # tfrc already extracted above
        ridge_density = features.get('ridge_density', 0.0)
        tfrc = features.get('tfrc', 0)  # Total Fingerprint Ridge Count
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
        
        # Calculate stress response abilities using comprehensive DMIT scientific correlations
        
        # 1. Stress Tolerance Analysis (DMIT Principle: High pattern regularity + low lacunarity = stress tolerance)
        stress_tolerance = self._calculate_stress_tolerance(pattern_regularity, lacunarity, 
                                                          ridge_continuity, std_intensity)
        
        # 2. Stress Recovery Analysis (DMIT Principle: High correlation dimension + graph density = stress recovery)
        stress_recovery = self._calculate_stress_recovery(correlation_dimension, graph_density, 
                                                        betweenness_centrality, information_dimension)
        
        # 3. Stress Adaptability Analysis (DMIT Principle: High ridge uniformity + pattern type = stress adaptability)
        stress_adaptability = self._calculate_stress_adaptability(ridge_uniformity, pattern_type, 
                                                                ridge_curvature, community_cohesion)
        
        # 4. Stress Resilience Analysis (DMIT Principle: High ridge density + clustering coefficient = stress resilience)
        stress_resilience = self._calculate_stress_resilience(ridge_density, clustering_coefficient, 
                                                            modularity, ridge_thickness)
        
        # 5. Stress Management Analysis (DMIT Principle: High spectral radius + topological complexity = stress management)
        stress_management = self._calculate_stress_management(spectral_radius, topological_complexity, 
                                                            euler_characteristic, spectral_bandwidth)
        
        # 6. Stress Balance Analysis (DMIT Principle: High ridge count + fractal complexity = stress balance)
        stress_balance = self._calculate_stress_balance(tfrc, box_counting_dimension, 
                                                      h1_num_features, betti_1)
        
        # 7. Stress Monitoring Analysis (DMIT Principle: High information dimension + entropy = stress monitoring)
        stress_monitoring = self._calculate_stress_monitoring(information_dimension, entropy, 
                                                            pattern_symmetry, spectral_entropy)
        
        # 8. Stress Intelligence Analysis (DMIT Principle: High spectral features + graph complexity = stress intelligence)
        stress_intelligence = self._calculate_stress_intelligence(spectral_centroid, spectral_rolloff, 
                                                                graph_density, topological_complexity)
        
        # Overall stress response score (comprehensive weighted combination)
        stress_response_score = (
            stress_tolerance * 0.20 +             # Stress tolerance is fundamental
            stress_recovery * 0.18 +              # Stress recovery is crucial
            stress_resilience * 0.15 +            # Stress resilience is important
            stress_adaptability * 0.15 +          # Stress adaptability is essential
            stress_management * 0.12 +            # Stress management
            stress_balance * 0.10 +               # Stress balance
            stress_monitoring * 0.07 +            # Stress monitoring
            stress_intelligence * 0.03            # Stress intelligence
        )
        
        # Normalize to 0-1 range
        stress_response_score = max(0.0, min(1.0, stress_response_score))
        
        # Determine stress response style based on dominant features
        response_styles = {
            'tolerant': stress_tolerance + stress_balance,
            'recovery': stress_recovery + stress_management,
            'resilient': stress_resilience + stress_adaptability,
            'adaptive': stress_adaptability + stress_monitoring,
            'managed': stress_management + stress_intelligence,
            'balanced': stress_balance + stress_tolerance
        }
        primary_style = max(response_styles.items(), key=lambda x: x[1])[0]

        return {
            'stress_response_score': stress_response_score,
            'primary_response_style': primary_style,
            'stress_tolerance': stress_tolerance,
            'stress_recovery': stress_recovery,
            'stress_adaptability': stress_adaptability,
            'stress_resilience': stress_resilience,
            'stress_management': stress_management,
            'stress_balance': stress_balance,
            'stress_monitoring': stress_monitoring,
            'stress_intelligence': stress_intelligence,
            'coping_ability': stress_tolerance + stress_recovery,
            'adaptation_capacity': stress_adaptability + stress_resilience,
            'management_skills': stress_management + stress_intelligence,
            'emotional_stability': stress_balance + stress_monitoring,
            'stress_awareness': stress_monitoring + stress_intelligence,
            'response_profile': self.classify_response_level(stress_response_score)
        }

    def _calculate_stress_tolerance(self, pattern_regularity: float, lacunarity: float,
                                  ridge_continuity: float, std_intensity: float) -> float:
        """Calculate stress tolerance from fingerprint features (DMIT principle)"""
        # DMIT research shows: High pattern regularity + low lacunarity = stress tolerance
        
        # Pattern regularity contribution
        regularity_score = min(1.0, pattern_regularity)
        
        # Lacunarity contribution (lower lacunarity = more regular = better tolerance)
        lacunarity_score = max(0.0, 1.0 - lacunarity)
        
        # Ridge continuity contribution
        continuity_score = min(1.0, ridge_continuity)
        
        # Standard deviation contribution (lower variation = more consistent = better tolerance)
        if std_intensity > 0:
            std_score = max(0.0, 1.0 - (std_intensity / 100.0))
        else:
            std_score = 0.5
        
        # Combine scores
        stress_tolerance = (regularity_score * 0.3 + lacunarity_score * 0.25 + continuity_score * 0.25 + std_score * 0.2)
        return min(1.0, stress_tolerance)
    
    def _calculate_stress_recovery(self, correlation_dimension: float, graph_density: float,
                                 betweenness_centrality: float, information_dimension: float) -> float:
        """Calculate stress recovery from fingerprint features (DMIT principle)"""
        # DMIT research shows: High correlation dimension + graph density = stress recovery
        
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
        stress_recovery = (corr_score * 0.3 + density_score * 0.25 + centrality_score * 0.25 + info_score * 0.2)
        return min(1.0, stress_recovery)
    
    def _calculate_stress_adaptability(self, ridge_uniformity: float, pattern_type: str,
                                     ridge_curvature: float, community_cohesion: float) -> float:
        """Calculate stress adaptability from fingerprint features (DMIT principle)"""
        # DMIT research shows: High ridge uniformity + pattern type = stress adaptability
        
        # Ridge uniformity contribution
        uniformity_score = min(1.0, ridge_uniformity)
        
        # Pattern type contribution
        pattern_weights = {
            'whorl': 0.8,      # Complex patterns indicate good adaptability
            'loop': 0.7,       # Good adaptability
            'arch': 0.6,       # Moderate adaptability
            'tented_arch': 0.65, # Slightly better than plain arch
            'composite': 0.75   # Complex adaptability patterns
        }
        pattern_score = pattern_weights.get(pattern_type.lower(), 0.6)
        
        # Ridge curvature contribution
        curvature_score = min(1.0, ridge_curvature)
        
        # Community cohesion contribution
        cohesion_score = min(1.0, community_cohesion)
        
        # Combine scores
        stress_adaptability = (uniformity_score * 0.3 + pattern_score * 0.25 + curvature_score * 0.25 + cohesion_score * 0.2)
        return min(1.0, stress_adaptability)
    
    def _calculate_stress_resilience(self, ridge_density: float, clustering_coefficient: float,
                                   modularity: float, ridge_thickness: float) -> float:
        """Calculate stress resilience from fingerprint features (DMIT principle)"""
        # DMIT research shows: High ridge density + clustering coefficient = stress resilience
        
        # Ridge density contribution
        density_score = min(1.0, ridge_density)
        
        # Clustering coefficient contribution
        clustering_score = min(1.0, clustering_coefficient)
        
        # Modularity contribution
        modularity_score = min(1.0, modularity)
        
        # Ridge thickness contribution
        thickness_score = min(1.0, ridge_thickness)
        
        # Combine scores
        stress_resilience = (density_score * 0.3 + clustering_score * 0.25 + modularity_score * 0.25 + thickness_score * 0.2)
        return min(1.0, stress_resilience)
    
    def _calculate_stress_management(self, spectral_radius: float, topological_complexity: float,
                                   euler_characteristic: int, spectral_bandwidth: float) -> float:
        """Calculate stress management from fingerprint features (DMIT principle)"""
        # DMIT research shows: High spectral radius + topological complexity = stress management
        
        # Spectral radius contribution
        if spectral_radius > 0:
            spectral_score = min(1.0, spectral_radius / 10.0)
        else:
            spectral_score = 0.5
        
        # Topological complexity contribution
        complexity_score = min(1.0, topological_complexity)
        
        # Euler characteristic contribution
        if euler_characteristic > 0:
            euler_score = min(1.0, euler_characteristic / 10.0)
        else:
            euler_score = 0.5
        
        # Spectral bandwidth contribution
        bandwidth_score = min(1.0, spectral_bandwidth)
        
        # Combine scores
        stress_management = (spectral_score * 0.3 + complexity_score * 0.25 + euler_score * 0.25 + bandwidth_score * 0.2)
        return min(1.0, stress_management)
    
    def _calculate_stress_balance(self, tfrc: int, box_counting_dimension: float,
                                h1_num_features: int, betti_1: int) -> float:
        """Calculate stress balance from fingerprint features (DMIT principle)"""
        # DMIT research shows: High ridge count + fractal complexity = stress balance
        
        # Ridge count contribution
        if tfrc > 0:
            ridge_score = min(1.0, tfrc / 1500.0)
        else:
            ridge_score = min(1.0, tfrc / 1500.0) if tfrc > 0 else 0.0
        
        # Fractal dimension contribution
        if 1.5 <= box_counting_dimension <= 2.0:
            fractal_score = (box_counting_dimension - 1.5) / 0.5
        else:
            fractal_score = 0.5
        
        # H1 features contribution (loops/holes - complexity in balance)
        h1_score = min(1.0, h1_num_features / 10.0)
        
        # Betti-1 contribution (balance loops)
        betti_score = min(1.0, betti_1 / 10.0)
        
        # Combine scores
        stress_balance = (ridge_score * 0.35 + fractal_score * 0.25 + h1_score * 0.25 + betti_score * 0.15)
        return min(1.0, stress_balance)
    
    def _calculate_stress_monitoring(self, information_dimension: float, entropy: float,
                                   pattern_symmetry: float, spectral_entropy: float) -> float:
        """Calculate stress monitoring from fingerprint features (DMIT principle)"""
        # DMIT research shows: High information dimension + entropy = stress monitoring
        
        # Information dimension contribution
        if 1.5 <= information_dimension <= 2.0:
            info_score = (information_dimension - 1.5) / 0.5
        else:
            info_score = 0.5
        
        # Entropy contribution (higher entropy = more complex stress monitoring)
        if entropy > 0:
            entropy_score = min(1.0, entropy / 8.0)  # Normalize to 0-1
        else:
            entropy_score = 0.5
        
        # Pattern symmetry contribution
        symmetry_score = min(1.0, pattern_symmetry)
        
        # Spectral entropy contribution
        spectral_score = min(1.0, spectral_entropy)
        
        # Combine scores
        stress_monitoring = (info_score * 0.35 + entropy_score * 0.25 + symmetry_score * 0.25 + spectral_score * 0.15)
        return min(1.0, stress_monitoring)
    
    def _calculate_stress_intelligence(self, spectral_centroid: float, spectral_rolloff: float,
                                     graph_density: float, topological_complexity: float) -> float:
        """Calculate stress intelligence from fingerprint features (DMIT principle)"""
        # DMIT research shows: High spectral features + graph complexity = stress intelligence
        
        # Spectral centroid contribution
        centroid_score = min(1.0, spectral_centroid)
        
        # Spectral rolloff contribution
        rolloff_score = min(1.0, spectral_rolloff)
        
        # Graph density contribution
        density_score = min(1.0, graph_density)
        
        # Topological complexity contribution
        complexity_score = min(1.0, topological_complexity)
        
        # Combine scores
        stress_intelligence = (centroid_score * 0.3 + rolloff_score * 0.25 + density_score * 0.25 + complexity_score * 0.2)
        return min(1.0, stress_intelligence)

    @staticmethod
    def classify_response_level(score: float) -> str:
        """Classify stress response level based on score"""
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