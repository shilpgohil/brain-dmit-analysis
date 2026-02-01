from typing import Dict, Any
from .base import DMITExtensionBase

class SocialAwarenessExtension(DMITExtensionBase):
    """
    Extension for analyzing Social Awareness abilities from fingerprint features.
    Uses comprehensive DMIT scientific correlations between fingerprint patterns and social awareness processes.
    """
    def analyze(self, features: Dict[str, Any]) -> Dict[str, Any]:
        # Extract comprehensive fingerprint features for social awareness analysis
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
        
        # Calculate social awareness abilities using comprehensive DMIT scientific correlations
        
        # 1. Emotional Perception Analysis (DMIT Principle: High information dimension + entropy = emotional perception)
        emotional_perception = self._calculate_emotional_perception(information_dimension, entropy, 
                                                                  pattern_symmetry, spectral_entropy)
        
        # 2. Social Understanding Analysis (DMIT Principle: High correlation dimension + graph density = social understanding)
        social_understanding = self._calculate_social_understanding(correlation_dimension, graph_density, 
                                                                  betweenness_centrality, community_cohesion)
        
        # 3. Empathy Skills Analysis (DMIT Principle: High ridge density + clustering coefficient = empathy)
        empathy_skills = self._calculate_empathy_skills(ridge_density, clustering_coefficient, 
                                                      modularity, ridge_thickness)
        
        # 4. Social Communication Analysis (DMIT Principle: High spectral radius + topological complexity = communication)
        social_communication = self._calculate_social_communication(spectral_radius, topological_complexity, 
                                                                  euler_characteristic, spectral_bandwidth)
        
        # 5. Relationship Awareness Analysis (DMIT Principle: High ridge count + fractal complexity = relationship awareness)
        relationship_awareness = self._calculate_relationship_awareness(tfrc, box_counting_dimension, 
                                                                      h1_num_features, betti_1)
        
        # 6. Social Adaptability Analysis (DMIT Principle: High ridge uniformity + pattern type = social adaptability)
        social_adaptability = self._calculate_social_adaptability(ridge_uniformity, pattern_type, 
                                                                ridge_curvature, community_cohesion)
        
        # 7. Social Monitoring Analysis (DMIT Principle: High pattern regularity + low lacunarity = social monitoring)
        social_monitoring = self._calculate_social_monitoring(pattern_regularity, lacunarity, 
                                                            ridge_continuity, std_intensity)
        
        # 8. Social Intelligence Analysis (DMIT Principle: High spectral features + graph complexity = social intelligence)
        social_intelligence = self._calculate_social_intelligence(spectral_centroid, spectral_rolloff, 
                                                                graph_density, topological_complexity)
        
        # Overall social awareness score (comprehensive weighted combination)
        social_awareness_score = (
            emotional_perception * 0.20 +         # Emotional perception is fundamental
            social_understanding * 0.18 +         # Social understanding is crucial
            empathy_skills * 0.15 +               # Empathy skills are important
            social_communication * 0.15 +         # Social communication is essential
            relationship_awareness * 0.12 +       # Relationship awareness
            social_adaptability * 0.10 +          # Social adaptability
            social_monitoring * 0.07 +            # Social monitoring
            social_intelligence * 0.03            # Social intelligence
        )
        
        # Normalize to 0-1 range
        social_awareness_score = max(0.0, min(1.0, social_awareness_score))
        
        # Determine social awareness style based on dominant features
        awareness_styles = {
            'empathetic': empathy_skills + emotional_perception,
            'understanding': social_understanding + social_intelligence,
            'communicative': social_communication + relationship_awareness,
            'adaptive': social_adaptability + social_monitoring,
            'perceptive': emotional_perception + social_monitoring,
            'intelligent': social_intelligence + social_understanding
        }
        primary_style = max(awareness_styles.items(), key=lambda x: x[1])[0]

        return {
            'social_awareness_score': social_awareness_score,
            'primary_awareness_style': primary_style,
            'emotional_perception': emotional_perception,
            'social_understanding': social_understanding,
            'empathy_skills': empathy_skills,
            'social_communication': social_communication,
            'relationship_awareness': relationship_awareness,
            'social_adaptability': social_adaptability,
            'social_monitoring': social_monitoring,
            'social_intelligence': social_intelligence,
            'emotional_sensitivity': emotional_perception + empathy_skills,
            'social_insight': social_understanding + social_intelligence,
            'interpersonal_awareness': relationship_awareness + social_communication,
            'social_adaptation': social_adaptability + social_monitoring,
            'social_perception': emotional_perception + social_monitoring,
            'awareness_profile': self.classify_awareness_level(social_awareness_score)
        }

    def _calculate_emotional_perception(self, information_dimension: float, entropy: float,
                                      pattern_symmetry: float, spectral_entropy: float) -> float:
        """Calculate emotional perception from fingerprint features (DMIT principle)"""
        # DMIT research shows: High information dimension + entropy = emotional perception
        
        # Information dimension contribution
        if 1.5 <= information_dimension <= 2.0:
            info_score = (information_dimension - 1.5) / 0.5
        else:
            info_score = 0.5
        
        # Entropy contribution (higher entropy = more complex emotional perception)
        if entropy > 0:
            entropy_score = min(1.0, entropy / 8.0)  # Normalize to 0-1
        else:
            entropy_score = 0.5
        
        # Pattern symmetry contribution
        symmetry_score = min(1.0, pattern_symmetry)
        
        # Spectral entropy contribution
        spectral_score = min(1.0, spectral_entropy)
        
        # Combine scores
        emotional_perception = (info_score * 0.35 + entropy_score * 0.25 + symmetry_score * 0.25 + spectral_score * 0.15)
        return min(1.0, emotional_perception)
    
    def _calculate_social_understanding(self, correlation_dimension: float, graph_density: float,
                                      betweenness_centrality: float, community_cohesion: float) -> float:
        """Calculate social understanding from fingerprint features (DMIT principle)"""
        # DMIT research shows: High correlation dimension + graph density = social understanding
        
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
        social_understanding = (corr_score * 0.3 + density_score * 0.25 + centrality_score * 0.25 + cohesion_score * 0.2)
        return min(1.0, social_understanding)
    
    def _calculate_empathy_skills(self, ridge_density: float, clustering_coefficient: float,
                                modularity: float, ridge_thickness: float) -> float:
        """Calculate empathy skills from fingerprint features (DMIT principle)"""
        # DMIT research shows: High ridge density + clustering coefficient = empathy
        
        # Ridge density contribution
        density_score = min(1.0, ridge_density)
        
        # Clustering coefficient contribution
        clustering_score = min(1.0, clustering_coefficient)
        
        # Modularity contribution
        modularity_score = min(1.0, modularity)
        
        # Ridge thickness contribution
        thickness_score = min(1.0, ridge_thickness)
        
        # Combine scores
        empathy_skills = (density_score * 0.3 + clustering_score * 0.25 + modularity_score * 0.25 + thickness_score * 0.2)
        return min(1.0, empathy_skills)
    
    def _calculate_social_communication(self, spectral_radius: float, topological_complexity: float,
                                      euler_characteristic: int, spectral_bandwidth: float) -> float:
        """Calculate social communication from fingerprint features (DMIT principle)"""
        # DMIT research shows: High spectral radius + topological complexity = social communication
        
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
        social_communication = (spectral_score * 0.3 + complexity_score * 0.25 + euler_score * 0.25 + bandwidth_score * 0.2)
        return min(1.0, social_communication)
    
    def _calculate_relationship_awareness(self, tfrc: int, box_counting_dimension: float,
                                        h1_num_features: int, betti_1: int) -> float:
        """Calculate relationship awareness from fingerprint features (DMIT principle)"""
        # DMIT research shows: High ridge count + fractal complexity = relationship awareness
        
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
        
        # H1 features contribution (loops/holes - complexity in relationships)
        h1_score = min(1.0, h1_num_features / 10.0)
        
        # Betti-1 contribution (relationship loops)
        betti_score = min(1.0, betti_1 / 10.0)
        
        # Combine scores
        relationship_awareness = (ridge_score * 0.35 + fractal_score * 0.25 + h1_score * 0.25 + betti_score * 0.15)
        return min(1.0, relationship_awareness)
    
    def _calculate_social_adaptability(self, ridge_uniformity: float, pattern_type: str,
                                     ridge_curvature: float, community_cohesion: float) -> float:
        """Calculate social adaptability from fingerprint features (DMIT principle)"""
        # DMIT research shows: High ridge uniformity + pattern type = social adaptability
        
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
        social_adaptability = (uniformity_score * 0.3 + pattern_score * 0.25 + curvature_score * 0.25 + cohesion_score * 0.2)
        return min(1.0, social_adaptability)
    
    def _calculate_social_monitoring(self, pattern_regularity: float, lacunarity: float,
                                   ridge_continuity: float, std_intensity: float) -> float:
        """Calculate social monitoring from fingerprint features (DMIT principle)"""
        # DMIT research shows: High pattern regularity + low lacunarity = social monitoring
        
        # Pattern regularity contribution
        regularity_score = min(1.0, pattern_regularity)
        
        # Lacunarity contribution (lower lacunarity = more regular = better monitoring)
        lacunarity_score = max(0.0, 1.0 - lacunarity)
        
        # Ridge continuity contribution
        continuity_score = min(1.0, ridge_continuity)
        
        # Standard deviation contribution (lower variation = more consistent = better monitoring)
        if std_intensity > 0:
            std_score = max(0.0, 1.0 - (std_intensity / 100.0))
        else:
            std_score = 0.5
        
        # Combine scores
        social_monitoring = (regularity_score * 0.3 + lacunarity_score * 0.25 + continuity_score * 0.25 + std_score * 0.2)
        return min(1.0, social_monitoring)
    
    def _calculate_social_intelligence(self, spectral_centroid: float, spectral_rolloff: float,
                                     graph_density: float, topological_complexity: float) -> float:
        """Calculate social intelligence from fingerprint features (DMIT principle)"""
        # DMIT research shows: High spectral features + graph complexity = social intelligence
        
        # Spectral centroid contribution
        centroid_score = min(1.0, spectral_centroid)
        
        # Spectral rolloff contribution
        rolloff_score = min(1.0, spectral_rolloff)
        
        # Graph density contribution
        density_score = min(1.0, graph_density)
        
        # Topological complexity contribution
        complexity_score = min(1.0, topological_complexity)
        
        # Combine scores
        social_intelligence = (centroid_score * 0.3 + rolloff_score * 0.25 + density_score * 0.25 + complexity_score * 0.2)
        return min(1.0, social_intelligence)

    @staticmethod
    def classify_awareness_level(score: float) -> str:
        """Classify social awareness level based on score"""
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