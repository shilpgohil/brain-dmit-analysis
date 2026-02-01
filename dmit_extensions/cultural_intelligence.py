from typing import Dict, Any
from .base import DMITExtensionBase

class CulturalIntelligenceExtension(DMITExtensionBase):
    """
    Extension for analyzing Cultural Intelligence and cross-cultural abilities from fingerprint features.
    Uses comprehensive DMIT scientific correlations between fingerprint patterns and cultural awareness.
    """
    def analyze(self, features: Dict[str, Any]) -> Dict[str, Any]:
        # Extract comprehensive fingerprint features for cultural intelligence analysis
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
        
        # Calculate cultural intelligence abilities using comprehensive DMIT scientific correlations
        
        # 1. Cultural Awareness Analysis (DMIT Principle: High information dimension + entropy = cultural awareness)
        cultural_awareness = self._calculate_cultural_awareness(information_dimension, entropy, 
                                                              pattern_symmetry, spectral_entropy)
        
        # 2. Cultural Sensitivity Analysis (DMIT Principle: High ridge density + clustering coefficient = sensitivity)
        cultural_sensitivity = self._calculate_cultural_sensitivity(ridge_density, clustering_coefficient, 
                                                                  modularity, ridge_thickness)
        
        # 3. Cross-cultural Communication Analysis (DMIT Principle: High correlation dimension + graph density = communication)
        cross_cultural_communication = self._calculate_cross_cultural_communication(correlation_dimension, graph_density, 
                                                                                  betweenness_centrality, information_dimension)
        
        # 4. Cultural Adaptability Analysis (DMIT Principle: High community cohesion + spectral radius = adaptability)
        cultural_adaptability = self._calculate_cultural_adaptability(community_cohesion, spectral_radius, 
                                                                    topological_complexity, euler_characteristic)
        
        # 5. Cultural Knowledge Analysis (DMIT Principle: High ridge count + fractal dimension = knowledge)
        cultural_knowledge = self._calculate_cultural_knowledge(tfrc, box_counting_dimension, 
                                                              h1_num_features, betti_1)
        
        # 6. Cultural Empathy Analysis (DMIT Principle: High pattern regularity + low lacunarity = empathy)
        cultural_empathy = self._calculate_cultural_empathy(pattern_regularity, lacunarity, 
                                                          ridge_continuity, std_intensity)
        
        # 7. Cultural Flexibility Analysis (DMIT Principle: High ridge uniformity + pattern type = flexibility)
        cultural_flexibility = self._calculate_cultural_flexibility(ridge_uniformity, pattern_type, 
                                                                  ridge_curvature, spectral_energy)
        
        # 8. Cultural Intelligence Integration Analysis (DMIT Principle: High spectral features + graph complexity = integration)
        cultural_integration = self._calculate_cultural_integration(spectral_centroid, spectral_rolloff, 
                                                                  graph_density, topological_complexity)
        
        # Calculate overall cultural intelligence score
        cultural_intelligence_score = (
            cultural_awareness * 0.20 +              # Cultural awareness is fundamental
            cultural_sensitivity * 0.18 +            # Cultural sensitivity is crucial
            cross_cultural_communication * 0.15 +    # Cross-cultural communication is important
            cultural_adaptability * 0.15 +           # Cultural adaptability is essential
            cultural_knowledge * 0.12 +              # Cultural knowledge
            cultural_empathy * 0.10 +                # Cultural empathy
            cultural_flexibility * 0.07 +            # Cultural flexibility
            cultural_integration * 0.03              # Cultural integration
        )
        
        # Normalize to 0-1 range
        cultural_intelligence_score = max(0.0, min(1.0, cultural_intelligence_score))
        
        # Determine cultural intelligence style based on dominant features
        cultural_styles = {
            'awareness_focused': cultural_awareness + cultural_knowledge,
            'sensitivity_focused': cultural_sensitivity + cultural_empathy,
            'communication_focused': cross_cultural_communication + cultural_flexibility,
            'adaptability_focused': cultural_adaptability + cultural_integration,
            'empathy_focused': cultural_empathy + cultural_sensitivity,
            'balanced_cultural': (cultural_awareness + cultural_adaptability) / 2
        }
        primary_style = max(cultural_styles.items(), key=lambda x: x[1])[0]
        
        return {
            'cultural_intelligence_score': cultural_intelligence_score,
            'primary_cultural_style': primary_style,
            'cultural_awareness': cultural_awareness,
            'cultural_sensitivity': cultural_sensitivity,
            'cross_cultural_communication': cross_cultural_communication,
            'cultural_adaptability': cultural_adaptability,
            'cultural_knowledge': cultural_knowledge,
            'cultural_empathy': cultural_empathy,
            'cultural_flexibility': cultural_flexibility,
            'cultural_integration': cultural_integration,
            'cultural_perception': cultural_awareness + cultural_sensitivity,
            'cultural_interaction': cross_cultural_communication + cultural_adaptability,
            'cultural_understanding': cultural_knowledge + cultural_empathy,
            'cultural_adaptation': cultural_flexibility + cultural_integration,
            'cultural_competence': cultural_awareness + cross_cultural_communication,
            'cultural_intelligence_profile': self.classify_cultural_intelligence_level(cultural_intelligence_score)
        }

    def _calculate_cultural_awareness(self, information_dimension: float, entropy: float,
                                    pattern_symmetry: float, spectral_entropy: float) -> float:
        """Calculate cultural awareness from fingerprint features (DMIT principle)"""
        # DMIT research shows: High information dimension + entropy = cultural awareness
        
        # Information dimension contribution
        if 1.5 <= information_dimension <= 2.0:
            info_score = (information_dimension - 1.5) / 0.5
        else:
            info_score = 0.5
        
        # Entropy contribution (higher entropy = more complex cultural awareness)
        if entropy > 0:
            entropy_score = min(1.0, entropy / 8.0)  # Normalize to 0-1
        else:
            entropy_score = 0.5
        
        # Pattern symmetry contribution
        symmetry_score = min(1.0, pattern_symmetry)
        
        # Spectral entropy contribution
        spectral_score = min(1.0, spectral_entropy)
        
        # Combine scores
        cultural_awareness = (info_score * 0.35 + entropy_score * 0.25 + symmetry_score * 0.25 + spectral_score * 0.15)
        return min(1.0, cultural_awareness)
    
    def _calculate_cultural_sensitivity(self, ridge_density: float, clustering_coefficient: float,
                                      modularity: float, ridge_thickness: float) -> float:
        """Calculate cultural sensitivity from fingerprint features (DMIT principle)"""
        # DMIT research shows: High ridge density + clustering coefficient = cultural sensitivity
        
        # Ridge density contribution
        density_score = min(1.0, ridge_density)
        
        # Clustering coefficient contribution
        clustering_score = min(1.0, clustering_coefficient)
        
        # Modularity contribution
        modularity_score = min(1.0, modularity)
        
        # Ridge thickness contribution
        thickness_score = min(1.0, ridge_thickness)
        
        # Combine scores
        cultural_sensitivity = (density_score * 0.3 + clustering_score * 0.25 + modularity_score * 0.25 + thickness_score * 0.2)
        return min(1.0, cultural_sensitivity)
    
    def _calculate_cross_cultural_communication(self, correlation_dimension: float, graph_density: float,
                                              betweenness_centrality: float, information_dimension: float) -> float:
        """Calculate cross-cultural communication from fingerprint features (DMIT principle)"""
        # DMIT research shows: High correlation dimension + graph density = cross-cultural communication
        
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
        cross_cultural_communication = (corr_score * 0.3 + density_score * 0.25 + centrality_score * 0.25 + info_score * 0.2)
        return min(1.0, cross_cultural_communication)
    
    def _calculate_cultural_adaptability(self, community_cohesion: float, spectral_radius: float,
                                       topological_complexity: float, euler_characteristic: int) -> float:
        """Calculate cultural adaptability from fingerprint features (DMIT principle)"""
        # DMIT research shows: High community cohesion + spectral radius = cultural adaptability
        
        # Community cohesion contribution
        cohesion_score = min(1.0, community_cohesion)
        
        # Spectral radius contribution
        if spectral_radius > 0:
            spectral_score = min(1.0, spectral_radius / 10.0)
        else:
            spectral_score = 0.5
        
        # Topological complexity contribution
        complexity_score = min(1.0, topological_complexity)
        
        # Euler characteristic contribution (more negative = more complex = better adaptability)
        if euler_characteristic < 0:
            euler_score = min(1.0, abs(euler_characteristic) / 10.0)
        else:
            euler_score = 0.3
        
        # Combine scores
        cultural_adaptability = (cohesion_score * 0.3 + spectral_score * 0.25 + complexity_score * 0.25 + euler_score * 0.2)
        return min(1.0, cultural_adaptability)
    
    def _calculate_cultural_knowledge(self, tfrc: int, box_counting_dimension: float,
                                    h1_num_features: int, betti_1: int) -> float:
        """Calculate cultural knowledge from fingerprint features (DMIT principle)"""
        # DMIT research shows: High ridge count + fractal dimension = cultural knowledge
        
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
        
        # H1 features contribution (loops/holes - complexity in knowledge)
        h1_score = min(1.0, h1_num_features / 10.0)
        
        # Betti-1 contribution (knowledge loops)
        betti_score = min(1.0, betti_1 / 10.0)
        
        # Combine scores
        cultural_knowledge = (ridge_score * 0.35 + fractal_score * 0.25 + h1_score * 0.25 + betti_score * 0.15)
        return min(1.0, cultural_knowledge)
    
    def _calculate_cultural_empathy(self, pattern_regularity: float, lacunarity: float,
                                  ridge_continuity: float, std_intensity: float) -> float:
        """Calculate cultural empathy from fingerprint features (DMIT principle)"""
        # DMIT research shows: High pattern regularity + low lacunarity = cultural empathy
        
        # Pattern regularity contribution
        regularity_score = min(1.0, pattern_regularity)
        
        # Lacunarity contribution (lower lacunarity = more regular = better empathy)
        lacunarity_score = max(0.0, 1.0 - lacunarity)
        
        # Ridge continuity contribution
        continuity_score = min(1.0, ridge_continuity)
        
        # Standard deviation contribution (lower variation = more consistent = better empathy)
        if std_intensity > 0:
            std_score = max(0.0, 1.0 - (std_intensity / 100.0))
        else:
            std_score = 0.5
        
        # Combine scores
        cultural_empathy = (regularity_score * 0.3 + lacunarity_score * 0.25 + continuity_score * 0.25 + std_score * 0.2)
        return min(1.0, cultural_empathy)
    
    def _calculate_cultural_flexibility(self, ridge_uniformity: float, pattern_type: str,
                                      ridge_curvature: float, spectral_energy: float) -> float:
        """Calculate cultural flexibility from fingerprint features (DMIT principle)"""
        # DMIT research shows: High ridge uniformity + pattern type = cultural flexibility
        
        # Ridge uniformity contribution
        uniformity_score = min(1.0, ridge_uniformity)
        
        # Pattern type contribution
        pattern_weights = {
            'whorl': 0.8,      # Complex patterns indicate cultural flexibility
            'loop': 0.7,       # Good cultural flexibility
            'arch': 0.6,       # Moderate cultural flexibility
            'tented_arch': 0.65, # Slightly better than plain arch
            'composite': 0.75   # Complex cultural flexibility patterns
        }
        pattern_score = pattern_weights.get(pattern_type.lower(), 0.6)
        
        # Ridge curvature contribution
        curvature_score = min(1.0, ridge_curvature)
        
        # Spectral energy contribution
        energy_score = min(1.0, spectral_energy)
        
        # Combine scores
        cultural_flexibility = (uniformity_score * 0.3 + pattern_score * 0.25 + curvature_score * 0.25 + energy_score * 0.2)
        return min(1.0, cultural_flexibility)
    
    def _calculate_cultural_integration(self, spectral_centroid: float, spectral_rolloff: float,
                                      graph_density: float, topological_complexity: float) -> float:
        """Calculate cultural integration from fingerprint features (DMIT principle)"""
        # DMIT research shows: High spectral features + graph complexity = cultural integration
        
        # Spectral centroid contribution
        centroid_score = min(1.0, spectral_centroid)
        
        # Spectral rolloff contribution
        rolloff_score = min(1.0, spectral_rolloff)
        
        # Graph density contribution
        density_score = min(1.0, graph_density)
        
        # Topological complexity contribution
        complexity_score = min(1.0, topological_complexity)
        
        # Combine scores
        cultural_integration = (centroid_score * 0.3 + rolloff_score * 0.25 + density_score * 0.25 + complexity_score * 0.2)
        return min(1.0, cultural_integration)

    @staticmethod
    def classify_cultural_intelligence_level(score: float) -> str:
        if score >= 0.85:
            return "Exceptional Cultural Intelligence"
        elif score >= 0.75:
            return "High Cultural Intelligence"
        elif score >= 0.65:
            return "Above Average Cultural Intelligence"
        elif score >= 0.55:
            return "Average Cultural Intelligence"
        else:
            return "Developing Cultural Intelligence" 