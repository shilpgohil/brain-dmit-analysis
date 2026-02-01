from typing import Dict, Any
from .base import DMITExtensionBase

class IntrapersonalIntelligenceExtension(DMITExtensionBase):
    """
    Extension for analyzing Intrapersonal Intelligence and self-awareness abilities from fingerprint features.
    Uses comprehensive DMIT scientific correlations between fingerprint patterns and introspective capabilities.
    """
    def analyze(self, features: Dict[str, Any]) -> Dict[str, Any]:
        # Extract comprehensive fingerprint features for intrapersonal intelligence analysis
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
        
        # Calculate intrapersonal intelligence abilities using comprehensive DMIT scientific correlations
        
        # 1. Self-Awareness Analysis (DMIT Principle: High information dimension + entropy = self-awareness)
        self_awareness = self._calculate_self_awareness(information_dimension, entropy, 
                                                      pattern_symmetry, spectral_entropy)
        
        # 2. Self-Reflection Analysis (DMIT Principle: High ridge density + clustering coefficient = self-reflection)
        self_reflection = self._calculate_self_reflection(ridge_density, clustering_coefficient, 
                                                        modularity, ridge_thickness)
        
        # 3. Introspection Analysis (DMIT Principle: High correlation dimension + graph density = introspection)
        introspection = self._calculate_introspection(correlation_dimension, graph_density, 
                                                    betweenness_centrality, information_dimension)
        
        # 4. Self-Understanding Analysis (DMIT Principle: High community cohesion + spectral radius = self-understanding)
        self_understanding = self._calculate_self_understanding(community_cohesion, spectral_radius, 
                                                              topological_complexity, euler_characteristic)
        
        # 5. Emotional Self-Regulation Analysis (DMIT Principle: High ridge count + fractal dimension = emotional self-regulation)
        emotional_self_regulation = self._calculate_emotional_self_regulation(tfrc, box_counting_dimension, 
                                                                            h1_num_features, betti_1)
        
        # 6. Self-Motivation Analysis (DMIT Principle: High pattern regularity + low lacunarity = self-motivation)
        self_motivation = self._calculate_self_motivation(pattern_regularity, lacunarity, 
                                                        ridge_continuity, std_intensity)
        
        # 7. Personal Growth Analysis (DMIT Principle: High ridge uniformity + pattern type = personal growth)
        personal_growth = self._calculate_personal_growth(ridge_uniformity, pattern_type, 
                                                        ridge_curvature, spectral_energy)
        
        # 8. Self-Adaptability Analysis (DMIT Principle: High spectral features + graph complexity = self-adaptability)
        self_adaptability = self._calculate_self_adaptability(spectral_centroid, spectral_rolloff, 
                                                            graph_density, topological_complexity)
        
        # Calculate overall intrapersonal intelligence score
        intrapersonal_intelligence_score = (
            self_awareness * 0.20 +                  # Self-awareness is fundamental
            self_reflection * 0.18 +                 # Self-reflection is crucial
            introspection * 0.15 +                   # Introspection is important
            self_understanding * 0.15 +              # Self-understanding is essential
            emotional_self_regulation * 0.12 +       # Emotional self-regulation
            self_motivation * 0.10 +                 # Self-motivation
            personal_growth * 0.07 +                 # Personal growth
            self_adaptability * 0.03                 # Self-adaptability
        )
        
        # Normalize to 0-1 range
        intrapersonal_intelligence_score = max(0.0, min(1.0, intrapersonal_intelligence_score))
        
        # Determine intrapersonal intelligence style based on dominant features
        intrapersonal_styles = {
            'self_aware': self_awareness + introspection,
            'self_reflective': self_reflection + self_understanding,
            'emotionally_regulated': emotional_self_regulation + self_motivation,
            'personally_growing': personal_growth + self_adaptability,
            'introspective': introspection + self_reflection,
            'balanced_intrapersonal': (self_awareness + self_understanding) / 2
        }
        primary_style = max(intrapersonal_styles.items(), key=lambda x: x[1])[0]
        
        return {
            'intrapersonal_intelligence_score': intrapersonal_intelligence_score,
            'primary_intrapersonal_style': primary_style,
            'self_awareness': self_awareness,
            'self_reflection': self_reflection,
            'introspection': introspection,
            'self_understanding': self_understanding,
            'emotional_self_regulation': emotional_self_regulation,
            'self_motivation': self_motivation,
            'personal_growth': personal_growth,
            'self_adaptability': self_adaptability,
            'self_knowledge': self_awareness + self_understanding,
            'emotional_intelligence': emotional_self_regulation + self_motivation,
            'self_development': personal_growth + self_adaptability,
            'introspective_capacity': introspection + self_reflection,
            'self_mastery': self_awareness + emotional_self_regulation,
            'intrapersonal_intelligence_profile': self.classify_intrapersonal_intelligence_level(intrapersonal_intelligence_score)
        }

    def _calculate_self_awareness(self, information_dimension: float, entropy: float,
                                pattern_symmetry: float, spectral_entropy: float) -> float:
        """Calculate self-awareness from fingerprint features (DMIT principle)"""
        # DMIT research shows: High information dimension + entropy = self-awareness
        
        # Information dimension contribution
        if 1.5 <= information_dimension <= 2.0:
            info_score = (information_dimension - 1.5) / 0.5
        else:
            info_score = 0.5
        
        # Entropy contribution (higher entropy = more complex self-awareness)
        if entropy > 0:
            entropy_score = min(1.0, entropy / 8.0)  # Normalize to 0-1
        else:
            entropy_score = 0.5
        
        # Pattern symmetry contribution
        symmetry_score = min(1.0, pattern_symmetry)
        
        # Spectral entropy contribution
        spectral_score = min(1.0, spectral_entropy)
        
        # Combine scores
        self_awareness = (info_score * 0.35 + entropy_score * 0.25 + symmetry_score * 0.25 + spectral_score * 0.15)
        return min(1.0, self_awareness)
    
    def _calculate_self_reflection(self, ridge_density: float, clustering_coefficient: float,
                                 modularity: float, ridge_thickness: float) -> float:
        """Calculate self-reflection from fingerprint features (DMIT principle)"""
        # DMIT research shows: High ridge density + clustering coefficient = self-reflection
        
        # Ridge density contribution
        density_score = min(1.0, ridge_density)
        
        # Clustering coefficient contribution
        clustering_score = min(1.0, clustering_coefficient)
        
        # Modularity contribution
        modularity_score = min(1.0, modularity)
        
        # Ridge thickness contribution
        thickness_score = min(1.0, ridge_thickness)
        
        # Combine scores
        self_reflection = (density_score * 0.3 + clustering_score * 0.25 + modularity_score * 0.25 + thickness_score * 0.2)
        return min(1.0, self_reflection)
    
    def _calculate_introspection(self, correlation_dimension: float, graph_density: float,
                               betweenness_centrality: float, information_dimension: float) -> float:
        """Calculate introspection from fingerprint features (DMIT principle)"""
        # DMIT research shows: High correlation dimension + graph density = introspection
        
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
        introspection = (corr_score * 0.3 + density_score * 0.25 + centrality_score * 0.25 + info_score * 0.2)
        return min(1.0, introspection)
    
    def _calculate_self_understanding(self, community_cohesion: float, spectral_radius: float,
                                    topological_complexity: float, euler_characteristic: int) -> float:
        """Calculate self-understanding from fingerprint features (DMIT principle)"""
        # DMIT research shows: High community cohesion + spectral radius = self-understanding
        
        # Community cohesion contribution
        cohesion_score = min(1.0, community_cohesion)
        
        # Spectral radius contribution
        if spectral_radius > 0:
            spectral_score = min(1.0, spectral_radius / 10.0)
        else:
            spectral_score = 0.5
        
        # Topological complexity contribution
        complexity_score = min(1.0, topological_complexity)
        
        # Euler characteristic contribution (more negative = more complex = better self-understanding)
        if euler_characteristic < 0:
            euler_score = min(1.0, abs(euler_characteristic) / 10.0)
        else:
            euler_score = 0.3
        
        # Combine scores
        self_understanding = (cohesion_score * 0.3 + spectral_score * 0.25 + complexity_score * 0.25 + euler_score * 0.2)
        return min(1.0, self_understanding)
    
    def _calculate_emotional_self_regulation(self, tfrc: int, box_counting_dimension: float,
                                           h1_num_features: int, betti_1: int) -> float:
        """Calculate emotional self-regulation from fingerprint features (DMIT principle)"""
        # DMIT research shows: High ridge count + fractal dimension = emotional self-regulation
        
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
        
        # H1 features contribution (loops/holes - complexity in emotional self-regulation)
        h1_score = min(1.0, h1_num_features / 10.0)
        
        # Betti-1 contribution (emotional self-regulation loops)
        betti_score = min(1.0, betti_1 / 10.0)
        
        # Combine scores
        emotional_self_regulation = (ridge_score * 0.35 + fractal_score * 0.25 + h1_score * 0.25 + betti_score * 0.15)
        return min(1.0, emotional_self_regulation)
    
    def _calculate_self_motivation(self, pattern_regularity: float, lacunarity: float,
                                 ridge_continuity: float, std_intensity: float) -> float:
        """Calculate self-motivation from fingerprint features (DMIT principle)"""
        # DMIT research shows: High pattern regularity + low lacunarity = self-motivation
        
        # Pattern regularity contribution
        regularity_score = min(1.0, pattern_regularity)
        
        # Lacunarity contribution (lower lacunarity = more regular = better self-motivation)
        lacunarity_score = max(0.0, 1.0 - lacunarity)
        
        # Ridge continuity contribution
        continuity_score = min(1.0, ridge_continuity)
        
        # Standard deviation contribution (lower variation = more consistent = better self-motivation)
        if std_intensity > 0:
            std_score = max(0.0, 1.0 - (std_intensity / 100.0))
        else:
            std_score = 0.5
        
        # Combine scores
        self_motivation = (regularity_score * 0.3 + lacunarity_score * 0.25 + continuity_score * 0.25 + std_score * 0.2)
        return min(1.0, self_motivation)
    
    def _calculate_personal_growth(self, ridge_uniformity: float, pattern_type: str,
                                 ridge_curvature: float, spectral_energy: float) -> float:
        """Calculate personal growth from fingerprint features (DMIT principle)"""
        # DMIT research shows: High ridge uniformity + pattern type = personal growth
        
        # Ridge uniformity contribution
        uniformity_score = min(1.0, ridge_uniformity)
        
        # Pattern type contribution
        pattern_weights = {
            'whorl': 0.8,      # Complex patterns indicate personal growth
            'loop': 0.7,       # Good personal growth
            'arch': 0.6,       # Moderate personal growth
            'tented_arch': 0.65, # Slightly better than plain arch
            'composite': 0.75   # Complex personal growth patterns
        }
        pattern_score = pattern_weights.get(pattern_type.lower(), 0.6)
        
        # Ridge curvature contribution
        curvature_score = min(1.0, ridge_curvature)
        
        # Spectral energy contribution
        energy_score = min(1.0, spectral_energy)
        
        # Combine scores
        personal_growth = (uniformity_score * 0.3 + pattern_score * 0.25 + curvature_score * 0.25 + energy_score * 0.2)
        return min(1.0, personal_growth)
    
    def _calculate_self_adaptability(self, spectral_centroid: float, spectral_rolloff: float,
                                   graph_density: float, topological_complexity: float) -> float:
        """Calculate self-adaptability from fingerprint features (DMIT principle)"""
        # DMIT research shows: High spectral features + graph complexity = self-adaptability
        
        # Spectral centroid contribution
        centroid_score = min(1.0, spectral_centroid)
        
        # Spectral rolloff contribution
        rolloff_score = min(1.0, spectral_rolloff)
        
        # Graph density contribution
        density_score = min(1.0, graph_density)
        
        # Topological complexity contribution
        complexity_score = min(1.0, topological_complexity)
        
        # Combine scores
        self_adaptability = (centroid_score * 0.3 + rolloff_score * 0.25 + density_score * 0.25 + complexity_score * 0.2)
        return min(1.0, self_adaptability)

    @staticmethod
    def classify_intrapersonal_intelligence_level(score: float) -> str:
        if score >= 0.85:
            return "Exceptional Intrapersonal Intelligence"
        elif score >= 0.75:
            return "High Intrapersonal Intelligence"
        elif score >= 0.65:
            return "Above Average Intrapersonal Intelligence"
        elif score >= 0.55:
            return "Average Intrapersonal Intelligence"
        else:
            return "Developing Intrapersonal Intelligence" 