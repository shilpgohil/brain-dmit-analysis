from typing import Dict, Any
from .base import DMITExtensionBase

class HealthWellnessExtension(DMITExtensionBase):
    """
    Extension for analyzing Health and Wellness awareness and management abilities from fingerprint features.
    Uses comprehensive DMIT scientific correlations between fingerprint patterns and health capabilities.
    """
    def analyze(self, features: Dict[str, Any]) -> Dict[str, Any]:
        # Extract comprehensive fingerprint features for health wellness analysis
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
        
        # Calculate health wellness abilities using comprehensive DMIT scientific correlations
        
        # 1. Health Awareness Analysis (DMIT Principle: High information dimension + entropy = health awareness)
        health_awareness = self._calculate_health_awareness(information_dimension, entropy, 
                                                          pattern_symmetry, spectral_entropy)
        
        # 2. Physical Wellness Analysis (DMIT Principle: High ridge density + clustering coefficient = physical wellness)
        physical_wellness = self._calculate_physical_wellness(ridge_density, clustering_coefficient, 
                                                            modularity, ridge_thickness)
        
        # 3. Mental Wellness Analysis (DMIT Principle: High correlation dimension + graph density = mental wellness)
        mental_wellness = self._calculate_mental_wellness(correlation_dimension, graph_density, 
                                                        betweenness_centrality, information_dimension)
        
        # 4. Lifestyle Management Analysis (DMIT Principle: High community cohesion + spectral radius = lifestyle management)
        lifestyle_management = self._calculate_lifestyle_management(community_cohesion, spectral_radius, 
                                                                  topological_complexity, euler_characteristic)
        
        # 5. Stress Management Analysis (DMIT Principle: High ridge count + fractal dimension = stress management)
        stress_management = self._calculate_stress_management(tfrc, box_counting_dimension, 
                                                            h1_num_features, betti_1)
        
        # 6. Nutrition Awareness Analysis (DMIT Principle: High pattern regularity + low lacunarity = nutrition awareness)
        nutrition_awareness = self._calculate_nutrition_awareness(pattern_regularity, lacunarity, 
                                                                ridge_continuity, std_intensity)
        
        # 7. Exercise Motivation Analysis (DMIT Principle: High ridge uniformity + pattern type = exercise motivation)
        exercise_motivation = self._calculate_exercise_motivation(ridge_uniformity, pattern_type, 
                                                                ridge_curvature, spectral_energy)
        
        # 8. Wellness Integration Analysis (DMIT Principle: High spectral features + graph complexity = wellness integration)
        wellness_integration = self._calculate_wellness_integration(spectral_centroid, spectral_rolloff, 
                                                                  graph_density, topological_complexity)
        
        # Calculate overall health wellness score
        health_wellness_score = (
            health_awareness * 0.20 +                # Health awareness is fundamental
            physical_wellness * 0.18 +               # Physical wellness is crucial
            mental_wellness * 0.15 +                 # Mental wellness is important
            lifestyle_management * 0.15 +            # Lifestyle management is essential
            stress_management * 0.12 +               # Stress management
            nutrition_awareness * 0.10 +             # Nutrition awareness
            exercise_motivation * 0.07 +             # Exercise motivation
            wellness_integration * 0.03              # Wellness integration
        )
        
        # Normalize to 0-1 range
        health_wellness_score = max(0.0, min(1.0, health_wellness_score))
        
        # Determine health wellness style based on dominant features
        health_styles = {
            'health_conscious': health_awareness + nutrition_awareness,
            'physically_active': physical_wellness + exercise_motivation,
            'mentally_balanced': mental_wellness + stress_management,
            'lifestyle_optimizer': lifestyle_management + wellness_integration,
            'wellness_integrator': wellness_integration + health_awareness,
            'balanced_wellness': (physical_wellness + mental_wellness) / 2
        }
        primary_style = max(health_styles.items(), key=lambda x: x[1])[0]
        
        return {
            'health_wellness_score': health_wellness_score,
            'primary_health_style': primary_style,
            'health_awareness': health_awareness,
            'physical_wellness': physical_wellness,
            'mental_wellness': mental_wellness,
            'lifestyle_management': lifestyle_management,
            'stress_management': stress_management,
            'nutrition_awareness': nutrition_awareness,
            'exercise_motivation': exercise_motivation,
            'wellness_integration': wellness_integration,
            'overall_wellness': physical_wellness + mental_wellness,
            'health_management': health_awareness + lifestyle_management,
            'stress_resilience': stress_management + mental_wellness,
            'fitness_orientation': physical_wellness + exercise_motivation,
            'nutrition_consciousness': nutrition_awareness + health_awareness,
            'health_wellness_profile': self.classify_health_wellness_level(health_wellness_score)
        }

    def _calculate_health_awareness(self, information_dimension: float, entropy: float,
                                  pattern_symmetry: float, spectral_entropy: float) -> float:
        """Calculate health awareness from fingerprint features (DMIT principle)"""
        # DMIT research shows: High information dimension + entropy = health awareness
        
        # Information dimension contribution
        if 1.5 <= information_dimension <= 2.0:
            info_score = (information_dimension - 1.5) / 0.5
        else:
            info_score = 0.5
        
        # Entropy contribution (higher entropy = more complex health awareness)
        if entropy > 0:
            entropy_score = min(1.0, entropy / 8.0)  # Normalize to 0-1
        else:
            entropy_score = 0.5
        
        # Pattern symmetry contribution
        symmetry_score = min(1.0, pattern_symmetry)
        
        # Spectral entropy contribution
        spectral_score = min(1.0, spectral_entropy)
        
        # Combine scores
        health_awareness = (info_score * 0.35 + entropy_score * 0.25 + symmetry_score * 0.25 + spectral_score * 0.15)
        return min(1.0, health_awareness)
    
    def _calculate_physical_wellness(self, ridge_density: float, clustering_coefficient: float,
                                   modularity: float, ridge_thickness: float) -> float:
        """Calculate physical wellness from fingerprint features (DMIT principle)"""
        # DMIT research shows: High ridge density + clustering coefficient = physical wellness
        
        # Ridge density contribution
        density_score = min(1.0, ridge_density)
        
        # Clustering coefficient contribution
        clustering_score = min(1.0, clustering_coefficient)
        
        # Modularity contribution
        modularity_score = min(1.0, modularity)
        
        # Ridge thickness contribution
        thickness_score = min(1.0, ridge_thickness)
        
        # Combine scores
        physical_wellness = (density_score * 0.3 + clustering_score * 0.25 + modularity_score * 0.25 + thickness_score * 0.2)
        return min(1.0, physical_wellness)
    
    def _calculate_mental_wellness(self, correlation_dimension: float, graph_density: float,
                                 betweenness_centrality: float, information_dimension: float) -> float:
        """Calculate mental wellness from fingerprint features (DMIT principle)"""
        # DMIT research shows: High correlation dimension + graph density = mental wellness
        
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
        mental_wellness = (corr_score * 0.3 + density_score * 0.25 + centrality_score * 0.25 + info_score * 0.2)
        return min(1.0, mental_wellness)
    
    def _calculate_lifestyle_management(self, community_cohesion: float, spectral_radius: float,
                                      topological_complexity: float, euler_characteristic: int) -> float:
        """Calculate lifestyle management from fingerprint features (DMIT principle)"""
        # DMIT research shows: High community cohesion + spectral radius = lifestyle management
        
        # Community cohesion contribution
        cohesion_score = min(1.0, community_cohesion)
        
        # Spectral radius contribution
        if spectral_radius > 0:
            spectral_score = min(1.0, spectral_radius / 10.0)
        else:
            spectral_score = 0.5
        
        # Topological complexity contribution
        complexity_score = min(1.0, topological_complexity)
        
        # Euler characteristic contribution (more negative = more complex = better lifestyle management)
        if euler_characteristic < 0:
            euler_score = min(1.0, abs(euler_characteristic) / 10.0)
        else:
            euler_score = 0.3
        
        # Combine scores
        lifestyle_management = (cohesion_score * 0.3 + spectral_score * 0.25 + complexity_score * 0.25 + euler_score * 0.2)
        return min(1.0, lifestyle_management)
    
    def _calculate_stress_management(self, tfrc: int, box_counting_dimension: float,
                                   h1_num_features: int, betti_1: int) -> float:
        """Calculate stress management from fingerprint features (DMIT principle)"""
        # DMIT research shows: High ridge count + fractal dimension = stress management
        
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
        
        # H1 features contribution (loops/holes - complexity in stress management)
        h1_score = min(1.0, h1_num_features / 10.0)
        
        # Betti-1 contribution (stress management loops)
        betti_score = min(1.0, betti_1 / 10.0)
        
        # Combine scores
        stress_management = (ridge_score * 0.35 + fractal_score * 0.25 + h1_score * 0.25 + betti_score * 0.15)
        return min(1.0, stress_management)
    
    def _calculate_nutrition_awareness(self, pattern_regularity: float, lacunarity: float,
                                     ridge_continuity: float, std_intensity: float) -> float:
        """Calculate nutrition awareness from fingerprint features (DMIT principle)"""
        # DMIT research shows: High pattern regularity + low lacunarity = nutrition awareness
        
        # Pattern regularity contribution
        regularity_score = min(1.0, pattern_regularity)
        
        # Lacunarity contribution (lower lacunarity = more regular = better nutrition awareness)
        lacunarity_score = max(0.0, 1.0 - lacunarity)
        
        # Ridge continuity contribution
        continuity_score = min(1.0, ridge_continuity)
        
        # Standard deviation contribution (lower variation = more consistent = better nutrition awareness)
        if std_intensity > 0:
            std_score = max(0.0, 1.0 - (std_intensity / 100.0))
        else:
            std_score = 0.5
        
        # Combine scores
        nutrition_awareness = (regularity_score * 0.3 + lacunarity_score * 0.25 + continuity_score * 0.25 + std_score * 0.2)
        return min(1.0, nutrition_awareness)
    
    def _calculate_exercise_motivation(self, ridge_uniformity: float, pattern_type: str,
                                     ridge_curvature: float, spectral_energy: float) -> float:
        """Calculate exercise motivation from fingerprint features (DMIT principle)"""
        # DMIT research shows: High ridge uniformity + pattern type = exercise motivation
        
        # Ridge uniformity contribution
        uniformity_score = min(1.0, ridge_uniformity)
        
        # Pattern type contribution
        pattern_weights = {
            'whorl': 0.8,      # Complex patterns indicate exercise motivation
            'loop': 0.7,       # Good exercise motivation
            'arch': 0.6,       # Moderate exercise motivation
            'tented_arch': 0.65, # Slightly better than plain arch
            'composite': 0.75   # Complex exercise motivation patterns
        }
        pattern_score = pattern_weights.get(pattern_type.lower(), 0.6)
        
        # Ridge curvature contribution
        curvature_score = min(1.0, ridge_curvature)
        
        # Spectral energy contribution
        energy_score = min(1.0, spectral_energy)
        
        # Combine scores
        exercise_motivation = (uniformity_score * 0.3 + pattern_score * 0.25 + curvature_score * 0.25 + energy_score * 0.2)
        return min(1.0, exercise_motivation)
    
    def _calculate_wellness_integration(self, spectral_centroid: float, spectral_rolloff: float,
                                      graph_density: float, topological_complexity: float) -> float:
        """Calculate wellness integration from fingerprint features (DMIT principle)"""
        # DMIT research shows: High spectral features + graph complexity = wellness integration
        
        # Spectral centroid contribution
        centroid_score = min(1.0, spectral_centroid)
        
        # Spectral rolloff contribution
        rolloff_score = min(1.0, spectral_rolloff)
        
        # Graph density contribution
        density_score = min(1.0, graph_density)
        
        # Topological complexity contribution
        complexity_score = min(1.0, topological_complexity)
        
        # Combine scores
        wellness_integration = (centroid_score * 0.3 + rolloff_score * 0.25 + density_score * 0.25 + complexity_score * 0.2)
        return min(1.0, wellness_integration)

    @staticmethod
    def classify_health_wellness_level(score: float) -> str:
        if score >= 0.85:
            return "Exceptional Health and Wellness"
        elif score >= 0.75:
            return "High Health and Wellness"
        elif score >= 0.65:
            return "Above Average Health and Wellness"
        elif score >= 0.55:
            return "Average Health and Wellness"
        else:
            return "Developing Health and Wellness" 