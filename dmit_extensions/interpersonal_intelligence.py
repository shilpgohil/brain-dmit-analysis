from typing import Dict, Any
from .base import DMITExtensionBase

class InterpersonalIntelligenceExtension(DMITExtensionBase):
    """
    Extension for analyzing Interpersonal Intelligence from fingerprint features.
    Uses scientific DMIT correlations between fingerprint patterns and social abilities.
    """
    def analyze(self, features: Dict[str, Any]) -> Dict[str, Any]:
        # Extract actual fingerprint features for interpersonal intelligence analysis
        # Ridge count and density features
        # tfrc already extracted above
        ridge_density = features.get('ridge_density', 0.0)
        tfrc = features.get('tfrc_normalized', min(1.0, float(features.get('tfrc', 0) or 0) / 25.0))  # FIX: normalized 0-1
        
        # Pattern analysis features
        pattern_type = features.get('pattern_type', 'loop')
        pattern_symmetry = features.get('pattern_symmetry', 0.0)
        pattern_regularity = features.get('pattern_regularity', 0.0)
        
        # Fractal and complexity features
        box_counting_dimension = features.get('box_counting_dimension', 1.5)
        correlation_dimension = features.get('correlation_dimension', 1.5)
        information_dimension = features.get('information_dimension', 1.5)
        lacunarity = features.get('lacunarity', 0.0)
        
        # Graph and network features
        graph_density = features.get('graph_density', 0.0)
        clustering_coefficient = features.get('clustering_coefficient', 0.0)
        spectral_radius = features.get('spectral_radius', 0.0)
        betweenness_centrality = features.get('betweenness_centrality', 0.0)
        
        # Topological features
        euler_characteristic = features.get('euler_characteristic', 0)
        topological_complexity = features.get('topological_complexity', 0.0)
        h1_num_features = features.get('h1_num_features', 0)  # Loop/hole count
        
        # Statistical features
        entropy = features.get('entropy', 0.0)
        std_intensity = features.get('std_intensity', 0.0)
        minutiae_density = features.get('minutiae_density', 0.0)
        
        # Calculate interpersonal intelligence using DMIT scientific correlations
        
        # 1. Social Awareness Analysis (DMIT Principle: High information dimension + entropy = social awareness)
        social_awareness = self._calculate_social_awareness(information_dimension, entropy, 
                                                          pattern_symmetry, clustering_coefficient)
        
        # 2. Empathy Analysis (DMIT Principle: High correlation dimension + graph density = empathy)
        empathy = self._calculate_empathy(correlation_dimension, graph_density, 
                                        betweenness_centrality, pattern_regularity)
        
        # 3. Communication Skills Analysis (DMIT Principle: High spectral radius + ridge density = communication)
        communication_skills = self._calculate_communication_skills(spectral_radius, ridge_density, 
                                                                   pattern_type, topological_complexity)
        
        # 4. Relationship Building Analysis (DMIT Principle: High graph connectivity + fractal complexity = relationships)
        relationship_building = self._calculate_relationship_building(graph_density, box_counting_dimension, 
                                                                    h1_num_features, euler_characteristic)
        
        # 5. Conflict Resolution Analysis (DMIT Principle: High pattern regularity + low lacunarity = conflict resolution)
        conflict_resolution = self._calculate_conflict_resolution(pattern_regularity, lacunarity, 
                                                                correlation_dimension, std_intensity)
        
        # 6. Leadership Potential Analysis (DMIT Principle: High betweenness centrality + TFRC = leadership)
        leadership_potential = self._calculate_leadership_potential(betweenness_centrality, tfrc, 
                                                                  information_dimension)
        
        # Overall interpersonal intelligence score (weighted combination)
        interpersonal_intelligence_score = (
            social_awareness * 0.25 +            # Social awareness is fundamental
            empathy * 0.20 +                     # Empathy is crucial
            communication_skills * 0.20 +        # Communication is important
            relationship_building * 0.15 +       # Relationship building ability
            conflict_resolution * 0.15 +         # Conflict resolution
            leadership_potential * 0.05          # Leadership potential
        )
        
        # Normalize to 0-1 range
        interpersonal_intelligence_score = max(0.0, min(1.0, interpersonal_intelligence_score))
        
        # Determine interpersonal style based on dominant features
        interpersonal_styles = {
            'empathetic': (empathy + social_awareness) / 2,
            'communicative': (communication_skills + relationship_building) / 2,
            'diplomatic': (conflict_resolution + empathy) / 2,
            'leadership': (leadership_potential + communication_skills) / 2,
            'collaborative': (relationship_building + social_awareness) / 2
        }
        primary_style = max(interpersonal_styles.items(), key=lambda x: x[1])[0]
        
        return {
            'interpersonal_intelligence_score': interpersonal_intelligence_score,
            'primary_interpersonal_style': primary_style,
            'social_awareness': social_awareness,
            'empathy': empathy,
            'communication_skills': communication_skills,
            'relationship_building': relationship_building,
            'conflict_resolution': conflict_resolution,
            'leadership_potential': leadership_potential,
            'team_collaboration': (relationship_building + communication_skills) / 2,
            'emotional_support': (empathy + social_awareness) / 2,
            'negotiation_skills': (conflict_resolution + communication_skills) / 2,
            'mentoring_ability': (leadership_potential + empathy) / 2,
            'social_networking': (relationship_building + social_awareness) / 2,
            'interpersonal_profile': self.classify_interpersonal_level(interpersonal_intelligence_score)
        }

    def _calculate_social_awareness(self, information_dimension: float, entropy: float,
                                  pattern_symmetry: float, clustering_coefficient: float) -> float:
        """Calculate social awareness from fingerprint features (DMIT principle)"""
        # DMIT research shows: High information dimension + entropy = social awareness
        
        # Information dimension contribution
        if 1.5 <= information_dimension <= 2.0:
            info_score = (information_dimension - 1.5) / 0.5
        else:
            info_score = 0.5
        
        # Entropy contribution (higher entropy = more complex social understanding)
        if entropy > 0:
            entropy_score = min(1.0, entropy / 8.0)  # Normalize to 0-1
        else:
            entropy_score = 0.5
        
        # Pattern symmetry contribution
        symmetry_score = min(1.0, pattern_symmetry)
        
        # Clustering coefficient contribution
        clustering_score = min(1.0, clustering_coefficient)
        
        # Combine scores
        social_awareness = (info_score * 0.35 + entropy_score * 0.25 + symmetry_score * 0.25 + clustering_score * 0.15)
        return min(1.0, social_awareness)
    
    def _calculate_empathy(self, correlation_dimension: float, graph_density: float,
                          betweenness_centrality: float, pattern_regularity: float) -> float:
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
        
        # Pattern regularity contribution
        regularity_score = min(1.0, pattern_regularity)
        
        # Combine scores
        empathy = (corr_score * 0.3 + density_score * 0.25 + centrality_score * 0.25 + regularity_score * 0.2)
        return min(1.0, empathy)
    
    def _calculate_communication_skills(self, spectral_radius: float, ridge_density: float,
                                      pattern_type: str, topological_complexity: float) -> float:
        """Calculate communication skills from fingerprint features (DMIT principle)"""
        # DMIT research shows: High spectral radius + ridge density = communication skills
        
        # Spectral radius contribution
        if spectral_radius > 0:
            spectral_score = min(1.0, spectral_radius / 10.0)
        else:
            spectral_score = 0.5
        
        # Ridge density contribution
        density_score = min(1.0, ridge_density)
        
        # Pattern type contribution
        pattern_weights = {
            'whorl': 0.8,      # Complex patterns indicate good communication
            'loop': 0.7,       # Good communication
            'arch': 0.6,       # Moderate communication
            'tented_arch': 0.65, # Slightly better than plain arch
            'composite': 0.75   # Complex communication patterns
        }
        pattern_score = pattern_weights.get(pattern_type.lower(), 0.6)
        
        # Topological complexity contribution
        complexity_score = min(1.0, topological_complexity)
        
        # Combine scores
        communication_skills = (spectral_score * 0.3 + density_score * 0.25 + pattern_score * 0.25 + complexity_score * 0.2)
        return min(1.0, communication_skills)
    
    def _calculate_relationship_building(self, graph_density: float, box_counting_dimension: float,
                                       h1_num_features: int, euler_characteristic: int) -> float:
        """Calculate relationship building from fingerprint features (DMIT principle)"""
        # DMIT research shows: High graph connectivity + fractal complexity = relationship building
        
        # Graph density contribution
        density_score = min(1.0, graph_density)
        
        # Fractal dimension contribution
        if 1.5 <= box_counting_dimension <= 2.0:
            fractal_score = (box_counting_dimension - 1.5) / 0.5
        else:
            fractal_score = 0.5
        
        # H1 features contribution (loops/holes - complexity in relationships)
        h1_score = min(1.0, h1_num_features / 10.0)
        
        # Euler characteristic contribution (more negative = more complex = better relationships)
        if euler_characteristic < 0:
            euler_score = min(1.0, abs(euler_characteristic) / 10.0)
        else:
            euler_score = 0.3
        
        # Combine scores
        relationship_building = (density_score * 0.3 + fractal_score * 0.25 + h1_score * 0.25 + euler_score * 0.2)
        return min(1.0, relationship_building)
    
    def _calculate_conflict_resolution(self, pattern_regularity: float, lacunarity: float,
                                     correlation_dimension: float, std_intensity: float) -> float:
        """Calculate conflict resolution from fingerprint features (DMIT principle)"""
        # DMIT research shows: High pattern regularity + low lacunarity = conflict resolution
        
        # Pattern regularity contribution
        regularity_score = min(1.0, pattern_regularity)
        
        # Lacunarity contribution (lower lacunarity = more regular = better conflict resolution)
        lacunarity_score = max(0.0, 1.0 - lacunarity)
        
        # Correlation dimension contribution
        if 1.5 <= correlation_dimension <= 2.0:
            corr_score = (correlation_dimension - 1.5) / 0.5
        else:
            corr_score = 0.5
        
        # Standard deviation contribution (lower variation = more consistent = better conflict resolution)
        if std_intensity > 0:
            std_score = max(0.0, 1.0 - (std_intensity / 100.0))
        else:
            std_score = 0.5
        
        # Combine scores
        conflict_resolution = (regularity_score * 0.3 + lacunarity_score * 0.25 + corr_score * 0.25 + std_score * 0.2)
        return min(1.0, conflict_resolution)
    
    def _calculate_leadership_potential(self, betweenness_centrality: float, tfrc: int,
                                      information_dimension: float) -> float:
        """Calculate leadership potential from fingerprint features (DMIT principle)"""
        # DMIT research shows: High betweenness centrality + TFRC = leadership potential
        
        # Betweenness centrality contribution
        centrality_score = min(1.0, betweenness_centrality)
        
        # Ridge count contribution
        ridge_score = min(1.0, float(tfrc or 0))  # FIX: per-finger TFRC 0-30, not 0-1500  # FIX: per-finger TFRC 0-30
        
        # Information dimension contribution
        if 1.5 <= information_dimension <= 2.0:
            info_score = (information_dimension - 1.5) / 0.5
        else:
            info_score = 0.5
        
        # Combine scores
        leadership_potential = (centrality_score * 0.4 + ridge_score * 0.35 + info_score * 0.25)
        return min(1.0, leadership_potential)

    @staticmethod
    def classify_interpersonal_level(score: float) -> str:
        if score >= 0.85:
            return "Exceptional Interpersonal Intelligence"
        elif score >= 0.75:
            return "High Interpersonal Intelligence"
        elif score >= 0.65:
            return "Above Average Interpersonal Intelligence"
        elif score >= 0.55:
            return "Average Interpersonal Intelligence"
        else:
            return "Developing Interpersonal Intelligence" 