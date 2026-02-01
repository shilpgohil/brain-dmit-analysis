from typing import Dict, Any
from .base import DMITExtensionBase

class EmotionalIntelligenceExtension(DMITExtensionBase):
    """
    Extension for analyzing Emotional Intelligence from fingerprint features.
    Uses comprehensive DMIT scientific correlations between fingerprint patterns and emotional abilities.
    """
    def analyze(self, features: Dict[str, Any]) -> Dict[str, Any]:
        # Extract comprehensive fingerprint features for emotional intelligence analysis
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
        
        # Calculate emotional intelligence using comprehensive DMIT scientific correlations
        
        # 1. Emotional Awareness Analysis (DMIT Principle: High information dimension + entropy = emotional awareness)
        emotional_awareness = self._calculate_emotional_awareness(information_dimension, entropy, 
                                                                pattern_symmetry, spectral_entropy)
        
        # 2. Emotional Regulation Analysis (DMIT Principle: High pattern regularity + low lacunarity = emotional regulation)
        emotional_regulation = self._calculate_emotional_regulation(pattern_regularity, lacunarity, 
                                                                  ridge_continuity, std_intensity)
        
        # 3. Empathy Analysis (DMIT Principle: High correlation dimension + graph density = empathy)
        empathy = self._calculate_empathy(correlation_dimension, graph_density, 
                                        betweenness_centrality, community_cohesion)
        
        # 4. Social Skills Analysis (DMIT Principle: High clustering coefficient + modularity = social skills)
        social_skills = self._calculate_social_skills(clustering_coefficient, modularity, 
                                                     spectral_radius, topological_complexity)
        
        # 5. Emotional Expression Analysis (DMIT Principle: High ridge density + pattern type = emotional expression)
        emotional_expression = self._calculate_emotional_expression(ridge_density, pattern_type, 
                                                                  ridge_curvature, spectral_energy)
        
        # 6. Emotional Memory Analysis (DMIT Principle: High ridge count + fractal complexity = emotional memory)
        emotional_memory = self._calculate_emotional_memory(tfrc, box_counting_dimension, 
                                                          h1_num_features, betti_1)
        
        # 7. Emotional Processing Analysis (DMIT Principle: High spectral features + topological complexity = processing)
        emotional_processing = self._calculate_emotional_processing(spectral_centroid, spectral_bandwidth, 
                                                                  topological_complexity, euler_characteristic)
        
        # 8. Emotional Resilience Analysis (DMIT Principle: High ridge uniformity + pattern regularity = resilience)
        emotional_resilience = self._calculate_emotional_resilience(ridge_uniformity, pattern_regularity, 
                                                                  ridge_thickness, pore_density)
        
        # Overall emotional intelligence score (comprehensive weighted combination)
        emotional_intelligence_score = (
            emotional_awareness * 0.20 +        # Emotional awareness is fundamental
            emotional_regulation * 0.18 +       # Emotional regulation is crucial
            empathy * 0.15 +                    # Empathy is important
            social_skills * 0.15 +              # Social skills are essential
            emotional_expression * 0.12 +       # Emotional expression ability
            emotional_memory * 0.10 +           # Emotional memory
            emotional_processing * 0.07 +       # Emotional processing
            emotional_resilience * 0.03         # Emotional resilience
        )
        
        # Normalize to 0-1 range
        emotional_intelligence_score = max(0.0, min(1.0, emotional_intelligence_score))
        
        # Determine emotional intelligence style based on dominant features
        emotional_styles = {
            'aware': emotional_awareness + emotional_processing,
            'regulated': emotional_regulation + emotional_resilience,
            'empathetic': empathy + emotional_awareness,
            'social': social_skills + emotional_expression,
            'resilient': emotional_resilience + emotional_regulation,
            'expressive': emotional_expression + emotional_awareness
        }
        primary_style = max(emotional_styles.items(), key=lambda x: x[1])[0]
        
        return {
            'emotional_intelligence_score': emotional_intelligence_score,
            'primary_emotional_style': primary_style,
            'emotional_awareness': emotional_awareness,
            'emotional_regulation': emotional_regulation,
            'empathy': empathy,
            'social_skills': social_skills,
            'emotional_expression': emotional_expression,
            'emotional_memory': emotional_memory,
            'emotional_processing': emotional_processing,
            'emotional_resilience': emotional_resilience,
            'self_awareness': emotional_awareness + emotional_processing,
            'relationship_management': empathy + social_skills,
            'emotional_balance': emotional_regulation + emotional_resilience,
            'emotional_communication': emotional_expression + empathy,
            'stress_management': emotional_resilience + emotional_regulation,
            'emotional_profile': self.classify_emotional_level(emotional_intelligence_score)
        }

    def _calculate_emotional_awareness(self, information_dimension: float, entropy: float,
                                     pattern_symmetry: float, spectral_entropy: float) -> float:
        """Calculate emotional awareness from fingerprint features (DMIT principle)"""
        # DMIT research shows: High information dimension + entropy = emotional awareness
        
        # Information dimension contribution
        if 1.5 <= information_dimension <= 2.0:
            info_score = (information_dimension - 1.5) / 0.5
        else:
            info_score = 0.5
        
        # Entropy contribution (higher entropy = more complex emotional understanding)
        if entropy > 0:
            entropy_score = min(1.0, entropy / 8.0)  # Normalize to 0-1
        else:
            entropy_score = 0.5
        
        # Pattern symmetry contribution
        symmetry_score = min(1.0, pattern_symmetry)
        
        # Spectral entropy contribution
        spectral_score = min(1.0, spectral_entropy)
        
        # Combine scores
        emotional_awareness = (info_score * 0.35 + entropy_score * 0.25 + symmetry_score * 0.25 + spectral_score * 0.15)
        return min(1.0, emotional_awareness)
    
    def _calculate_emotional_regulation(self, pattern_regularity: float, lacunarity: float,
                                      ridge_continuity: float, std_intensity: float) -> float:
        """Calculate emotional regulation from fingerprint features (DMIT principle)"""
        # DMIT research shows: High pattern regularity + low lacunarity = emotional regulation
        
        # Pattern regularity contribution
        regularity_score = min(1.0, pattern_regularity)
        
        # Lacunarity contribution (lower lacunarity = more regular = better regulation)
        lacunarity_score = max(0.0, 1.0 - lacunarity)
        
        # Ridge continuity contribution
        continuity_score = min(1.0, ridge_continuity)
        
        # Standard deviation contribution (lower variation = more consistent = better regulation)
        if std_intensity > 0:
            std_score = max(0.0, 1.0 - (std_intensity / 100.0))
        else:
            std_score = 0.5
        
        # Combine scores
        emotional_regulation = (regularity_score * 0.3 + lacunarity_score * 0.25 + continuity_score * 0.25 + std_score * 0.2)
        return min(1.0, emotional_regulation)
    
    def _calculate_empathy(self, correlation_dimension: float, graph_density: float,
                          betweenness_centrality: float, community_cohesion: float) -> float:
        """Calculate empathy from fingerprint features (DMIT principle)"""
        # DMIT research shows: High correlation dimension + graph density = empathy
        
        # Correlation dimension contribution
        if 1.5 <= correlation_dimension <= 2.0:
            corr_score = (correlation_dimension - 1.5) / 0.5
        else:
            corr_score = 0.5
        
        # Graph density contribution
        density_score = min(1.0, graph_density)
        
        # Betweenness centrality contribution
        centrality_score = min(1.0, betweenness_centrality)
        
        # Community cohesion contribution
        cohesion_score = min(1.0, community_cohesion)
        
        # Combine scores
        empathy = (corr_score * 0.3 + density_score * 0.25 + centrality_score * 0.25 + cohesion_score * 0.2)
        return min(1.0, empathy)
    
    def _calculate_social_skills(self, clustering_coefficient: float, modularity: float,
                               spectral_radius: float, topological_complexity: float) -> float:
        """Calculate social skills from fingerprint features (DMIT principle)"""
        # DMIT research shows: High clustering coefficient + modularity = social skills
        
        # Clustering coefficient contribution
        clustering_score = min(1.0, clustering_coefficient)
        
        # Modularity contribution
        modularity_score = min(1.0, modularity)
        
        # Spectral radius contribution
        if spectral_radius > 0:
            spectral_score = min(1.0, spectral_radius / 10.0)
        else:
            spectral_score = 0.5
        
        # Topological complexity contribution
        complexity_score = min(1.0, topological_complexity)
        
        # Combine scores
        social_skills = (clustering_score * 0.3 + modularity_score * 0.25 + spectral_score * 0.25 + complexity_score * 0.2)
        return min(1.0, social_skills)
    
    def _calculate_emotional_expression(self, ridge_density: float, pattern_type: str,
                                      ridge_curvature: float, spectral_energy: float) -> float:
        """Calculate emotional expression from fingerprint features (DMIT principle)"""
        # DMIT research shows: High ridge density + pattern type = emotional expression
        
        # Ridge density contribution
        density_score = min(1.0, ridge_density)
        
        # Pattern type contribution
        pattern_weights = {
            'whorl': 0.8,      # Complex patterns indicate expressive ability
            'loop': 0.7,       # Good expression
            'arch': 0.6,       # Moderate expression
            'tented_arch': 0.65, # Slightly better than plain arch
            'composite': 0.75   # Complex expression patterns
        }
        pattern_score = pattern_weights.get(pattern_type.lower(), 0.6)
        
        # Ridge curvature contribution
        curvature_score = min(1.0, ridge_curvature)
        
        # Spectral energy contribution
        energy_score = min(1.0, spectral_energy)
        
        # Combine scores
        emotional_expression = (density_score * 0.3 + pattern_score * 0.25 + curvature_score * 0.25 + energy_score * 0.2)
        return min(1.0, emotional_expression)
    
    def _calculate_emotional_memory(self, tfrc: int, box_counting_dimension: float,
                                  h1_num_features: int, betti_1: int) -> float:
        """Calculate emotional memory from fingerprint features (DMIT principle)"""
        # DMIT research shows: High ridge count + fractal complexity = emotional memory
        
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
        
        # H1 features contribution (loops/holes - complexity in memory)
        h1_score = min(1.0, h1_num_features / 10.0)
        
        # Betti-1 contribution (emotional loops)
        betti_score = min(1.0, betti_1 / 10.0)
        
        # Combine scores
        emotional_memory = (ridge_score * 0.35 + fractal_score * 0.25 + h1_score * 0.25 + betti_score * 0.15)
        return min(1.0, emotional_memory)
    
    def _calculate_emotional_processing(self, spectral_centroid: float, spectral_bandwidth: float,
                                      topological_complexity: float, euler_characteristic: int) -> float:
        """Calculate emotional processing from fingerprint features (DMIT principle)"""
        # DMIT research shows: High spectral features + topological complexity = emotional processing
        
        # Spectral centroid contribution
        centroid_score = min(1.0, spectral_centroid)
        
        # Spectral bandwidth contribution
        bandwidth_score = min(1.0, spectral_bandwidth)
        
        # Topological complexity contribution
        complexity_score = min(1.0, topological_complexity)
        
        # Euler characteristic contribution (more negative = more complex = better processing)
        if euler_characteristic < 0:
            euler_score = min(1.0, abs(euler_characteristic) / 10.0)
        else:
            euler_score = 0.3
        
        # Combine scores
        emotional_processing = (centroid_score * 0.3 + bandwidth_score * 0.25 + complexity_score * 0.25 + euler_score * 0.2)
        return min(1.0, emotional_processing)
    
    def _calculate_emotional_resilience(self, ridge_uniformity: float, pattern_regularity: float,
                                      ridge_thickness: float, pore_density: float) -> float:
        """Calculate emotional resilience from fingerprint features (DMIT principle)"""
        # DMIT research shows: High ridge uniformity + pattern regularity = emotional resilience
        
        # Ridge uniformity contribution
        uniformity_score = min(1.0, ridge_uniformity)
        
        # Pattern regularity contribution
        regularity_score = min(1.0, pattern_regularity)
        
        # Ridge thickness contribution
        thickness_score = min(1.0, ridge_thickness)
        
        # Pore density contribution
        pore_score = min(1.0, pore_density)
        
        # Combine scores
        emotional_resilience = (uniformity_score * 0.3 + regularity_score * 0.25 + thickness_score * 0.25 + pore_score * 0.2)
        return min(1.0, emotional_resilience)

    @staticmethod
    def classify_emotional_level(score: float) -> str:
        if score >= 0.85:
            return "Exceptional Emotional Intelligence"
        elif score >= 0.75:
            return "High Emotional Intelligence"
        elif score >= 0.65:
            return "Above Average Emotional Intelligence"
        elif score >= 0.55:
            return "Average Emotional Intelligence"
        else:
            return "Developing Emotional Intelligence" 