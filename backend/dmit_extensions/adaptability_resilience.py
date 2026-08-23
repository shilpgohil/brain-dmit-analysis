from typing import Dict, Any
from .base import DMITExtensionBase

class AdaptabilityResilienceExtension(DMITExtensionBase):
    """
    Extension for analyzing Adaptability and Resilience abilities from fingerprint features.
    Uses comprehensive DMIT scientific correlations between fingerprint patterns and adaptive capacities.
    """
    def analyze(self, features: Dict[str, Any]) -> Dict[str, Any]:
        # Extract comprehensive fingerprint features for adaptability resilience analysis
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
        
        # Calculate adaptability resilience abilities using comprehensive DMIT scientific correlations
        
        # 1. Cognitive Adaptability Analysis (DMIT Principle: High information dimension + entropy = cognitive flexibility)
        cognitive_adaptability = self._calculate_cognitive_adaptability(information_dimension, entropy, 
                                                                      pattern_symmetry, spectral_entropy)
        
        # 2. Emotional Resilience Analysis (DMIT Principle: High pattern regularity + low lacunarity = emotional stability)
        emotional_resilience = self._calculate_emotional_resilience(pattern_regularity, lacunarity, 
                                                                  ridge_continuity, std_intensity)
        
        # 3. Behavioral Adaptability Analysis (DMIT Principle: High ridge uniformity + pattern type = behavioral flexibility)
        behavioral_adaptability = self._calculate_behavioral_adaptability(ridge_uniformity, pattern_type, 
                                                                        ridge_curvature, community_cohesion)
        
        # 4. Stress Resilience Analysis (DMIT Principle: High ridge density + clustering coefficient = stress management)
        stress_resilience = self._calculate_stress_resilience(ridge_density, clustering_coefficient, 
                                                            modularity, ridge_thickness)
        
        # 5. Change Adaptability Analysis (DMIT Principle: High spectral radius + topological complexity = change management)
        change_adaptability = self._calculate_change_adaptability(spectral_radius, topological_complexity, 
                                                                euler_characteristic, spectral_bandwidth)
        
        # 6. Recovery Resilience Analysis (DMIT Principle: High ridge count + fractal dimension = recovery ability)
        recovery_resilience = self._calculate_recovery_resilience(tfrc, box_counting_dimension, 
                                                                h1_num_features, betti_1)
        
        # 7. Learning Adaptability Analysis (DMIT Principle: High correlation dimension + graph density = learning flexibility)
        learning_adaptability = self._calculate_learning_adaptability(correlation_dimension, graph_density, 
                                                                    betweenness_centrality, information_dimension)
        
        # 8. Social Resilience Analysis (DMIT Principle: High spectral features + graph complexity = social resilience)
        social_resilience = self._calculate_social_resilience(spectral_centroid, spectral_rolloff, 
                                                            graph_density, topological_complexity)
        
        # Overall adaptability resilience score (comprehensive weighted combination)
        adaptability_resilience_score = (
            cognitive_adaptability * 0.20 +          # Cognitive adaptability is fundamental
            emotional_resilience * 0.18 +            # Emotional resilience is crucial
            behavioral_adaptability * 0.15 +         # Behavioral adaptability is important
            stress_resilience * 0.15 +               # Stress resilience is essential
            change_adaptability * 0.12 +             # Change adaptability
            recovery_resilience * 0.10 +             # Recovery resilience
            learning_adaptability * 0.07 +           # Learning adaptability
            social_resilience * 0.03                 # Social resilience
        )
        
        # Normalize to 0-1 range
        adaptability_resilience_score = max(0.0, min(1.0, adaptability_resilience_score))
        
        # Determine adaptability resilience style based on dominant features
        adaptability_styles = {
            'cognitive': (cognitive_adaptability + learning_adaptability) / 2,
            'emotional': (emotional_resilience + stress_resilience) / 2,
            'behavioral': (behavioral_adaptability + change_adaptability) / 2,
            'recovery': (recovery_resilience + emotional_resilience) / 2,
            'flexible': (cognitive_adaptability + behavioral_adaptability) / 2,
            'stable': (emotional_resilience + recovery_resilience) / 2
        }
        primary_style = max(adaptability_styles.items(), key=lambda x: x[1])[0]
        
        return {
            'adaptability_resilience_score': adaptability_resilience_score,
            'primary_adaptability_style': primary_style,
            'cognitive_adaptability': cognitive_adaptability,
            'emotional_resilience': emotional_resilience,
            'behavioral_adaptability': behavioral_adaptability,
            'stress_resilience': stress_resilience,
            'change_adaptability': change_adaptability,
            'recovery_resilience': recovery_resilience,
            'learning_adaptability': learning_adaptability,
            'social_resilience': social_resilience,
            'mental_flexibility': (cognitive_adaptability + learning_adaptability) / 2,
            'emotional_stability': (emotional_resilience + stress_resilience) / 2,
            'behavioral_flexibility': (behavioral_adaptability + change_adaptability) / 2,
            'bounce_back_ability': (recovery_resilience + emotional_resilience) / 2,
            'stress_management': (stress_resilience + social_resilience) / 2,
            'adaptability_resilience_profile': self.classify_adaptability_level(adaptability_resilience_score)
        }

    def _calculate_cognitive_adaptability(self, information_dimension: float, entropy: float,
                                        pattern_symmetry: float, spectral_entropy: float) -> float:
        """Calculate cognitive adaptability from fingerprint features (DMIT principle)"""
        # DMIT research shows: High information dimension + entropy = cognitive flexibility
        
        # Information dimension contribution
        if 1.5 <= information_dimension <= 2.0:
            info_score = (information_dimension - 1.5) / 0.5
        else:
            info_score = 0.5
        
        # Entropy contribution (higher entropy = more complex cognitive flexibility)
        if entropy > 0:
            entropy_score = min(1.0, entropy / 8.0)  # Normalize to 0-1
        else:
            entropy_score = 0.5
        
        # Pattern symmetry contribution
        symmetry_score = min(1.0, pattern_symmetry)
        
        # Spectral entropy contribution
        spectral_score = min(1.0, spectral_entropy)
        
        # Combine scores
        cognitive_adaptability = (info_score * 0.35 + entropy_score * 0.25 + symmetry_score * 0.25 + spectral_score * 0.15)
        return min(1.0, cognitive_adaptability)
    
    def _calculate_emotional_resilience(self, pattern_regularity: float, lacunarity: float,
                                      ridge_continuity: float, std_intensity: float) -> float:
        """Calculate emotional resilience from fingerprint features (DMIT principle)"""
        # DMIT research shows: High pattern regularity + low lacunarity = emotional stability
        
        # Pattern regularity contribution
        regularity_score = min(1.0, pattern_regularity)
        
        # Lacunarity contribution (lower lacunarity = more regular = better emotional stability)
        lacunarity_score = max(0.0, 1.0 - lacunarity)
        
        # Ridge continuity contribution
        continuity_score = min(1.0, ridge_continuity)
        
        # Standard deviation contribution (lower variation = more consistent = better emotional stability)
        if std_intensity > 0:
            std_score = max(0.0, 1.0 - (std_intensity / 100.0))
        else:
            std_score = 0.5
        
        # Combine scores
        emotional_resilience = (regularity_score * 0.3 + lacunarity_score * 0.25 + continuity_score * 0.25 + std_score * 0.2)
        return min(1.0, emotional_resilience)
    
    def _calculate_behavioral_adaptability(self, ridge_uniformity: float, pattern_type: str,
                                         ridge_curvature: float, community_cohesion: float) -> float:
        """Calculate behavioral adaptability from fingerprint features (DMIT principle)"""
        # DMIT research shows: High ridge uniformity + pattern type = behavioral flexibility
        
        # Ridge uniformity contribution
        uniformity_score = min(1.0, ridge_uniformity)
        
        # Pattern type contribution
        pattern_weights = {
            'whorl': 0.8,      # Complex patterns indicate behavioral flexibility
            'loop': 0.7,       # Good behavioral flexibility
            'arch': 0.6,       # Moderate behavioral flexibility
            'tented_arch': 0.65, # Slightly better than plain arch
            'composite': 0.75   # Complex behavioral patterns
        }
        pattern_score = pattern_weights.get(pattern_type.lower(), 0.6)
        
        # Ridge curvature contribution
        curvature_score = min(1.0, ridge_curvature)
        
        # Community cohesion contribution
        cohesion_score = min(1.0, community_cohesion)
        
        # Combine scores
        behavioral_adaptability = (uniformity_score * 0.3 + pattern_score * 0.25 + curvature_score * 0.25 + cohesion_score * 0.2)
        return min(1.0, behavioral_adaptability)
    
    def _calculate_stress_resilience(self, ridge_density: float, clustering_coefficient: float,
                                   modularity: float, ridge_thickness: float) -> float:
        """Calculate stress resilience from fingerprint features (DMIT principle)"""
        # DMIT research shows: High ridge density + clustering coefficient = stress management
        
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
    
    def _calculate_change_adaptability(self, spectral_radius: float, topological_complexity: float,
                                     euler_characteristic: int, spectral_bandwidth: float) -> float:
        """Calculate change adaptability from fingerprint features (DMIT principle)"""
        # DMIT research shows: High spectral radius + topological complexity = change management
        
        # Spectral radius contribution
        if spectral_radius > 0:
            spectral_score = min(1.0, spectral_radius / 10.0)
        else:
            spectral_score = 0.5
        
        # Topological complexity contribution
        complexity_score = min(1.0, topological_complexity)
        
        # Euler characteristic contribution (more negative = more complex = better change management)
        if euler_characteristic < 0:
            euler_score = min(1.0, abs(euler_characteristic) / 10.0)
        else:
            euler_score = 0.3
        
        # Spectral bandwidth contribution
        bandwidth_score = min(1.0, spectral_bandwidth)
        
        # Combine scores
        change_adaptability = (spectral_score * 0.3 + complexity_score * 0.25 + euler_score * 0.25 + bandwidth_score * 0.2)
        return min(1.0, change_adaptability)
    
    def _calculate_recovery_resilience(self, tfrc: int, box_counting_dimension: float,
                                     h1_num_features: int, betti_1: int) -> float:
        """Calculate recovery resilience from fingerprint features (DMIT principle)"""
        # DMIT research shows: High ridge count + fractal dimension = recovery ability
        
        # Ridge count contribution
        ridge_score = min(1.0, float(tfrc or 0))  # FIX: per-finger TFRC 0-30, not 0-1500  # FIX: per-finger TFRC 0-30
        
        # Fractal dimension contribution
        if 1.5 <= box_counting_dimension <= 2.0:
            fractal_score = (box_counting_dimension - 1.5) / 0.5
        else:
            fractal_score = 0.5
        
        # H1 features contribution (loops/holes - complexity in recovery)
        h1_score = min(1.0, h1_num_features / 10.0)
        
        # Betti-1 contribution (recovery loops)
        betti_score = min(1.0, betti_1 / 10.0)
        
        # Combine scores
        recovery_resilience = (ridge_score * 0.35 + fractal_score * 0.25 + h1_score * 0.25 + betti_score * 0.15)
        return min(1.0, recovery_resilience)
    
    def _calculate_learning_adaptability(self, correlation_dimension: float, graph_density: float,
                                       betweenness_centrality: float, information_dimension: float) -> float:
        """Calculate learning adaptability from fingerprint features (DMIT principle)"""
        # DMIT research shows: High correlation dimension + graph density = learning flexibility
        
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
        learning_adaptability = (corr_score * 0.3 + density_score * 0.25 + centrality_score * 0.25 + info_score * 0.2)
        return min(1.0, learning_adaptability)
    
    def _calculate_social_resilience(self, spectral_centroid: float, spectral_rolloff: float,
                                   graph_density: float, topological_complexity: float) -> float:
        """Calculate social resilience from fingerprint features (DMIT principle)"""
        # DMIT research shows: High spectral features + graph complexity = social resilience
        
        # Spectral centroid contribution
        centroid_score = min(1.0, spectral_centroid)
        
        # Spectral rolloff contribution
        rolloff_score = min(1.0, spectral_rolloff)
        
        # Graph density contribution
        density_score = min(1.0, graph_density)
        
        # Topological complexity contribution
        complexity_score = min(1.0, topological_complexity)
        
        # Combine scores
        social_resilience = (centroid_score * 0.3 + rolloff_score * 0.25 + density_score * 0.25 + complexity_score * 0.2)
        return min(1.0, social_resilience)

    @staticmethod
    def classify_adaptability_level(score: float) -> str:
        if score >= 0.85:
            return "Exceptional Adaptability and Resilience"
        elif score >= 0.75:
            return "High Adaptability and Resilience"
        elif score >= 0.65:
            return "Above Average Adaptability and Resilience"
        elif score >= 0.55:
            return "Average Adaptability and Resilience"
        else:
            return "Developing Adaptability and Resilience" 