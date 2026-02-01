from typing import Dict, Any
from .base import DMITExtensionBase

class LearningStyleExtension(DMITExtensionBase):
    """
    Extension for analyzing Learning Style preferences from fingerprint features.
    Uses comprehensive DMIT scientific correlations between fingerprint patterns and learning approaches.
    """
    def analyze(self, features: Dict[str, Any]) -> Dict[str, Any]:
        # Extract comprehensive fingerprint features for learning style analysis
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
        
        # Calculate learning style preferences using comprehensive DMIT scientific correlations
        
        # 1. Visual Learning Analysis (DMIT Principle: High information dimension + entropy = visual processing)
        visual_learning = self._calculate_visual_learning(information_dimension, entropy, 
                                                        pattern_symmetry, spectral_entropy)
        
        # 2. Auditory Learning Analysis (DMIT Principle: High correlation dimension + graph density = auditory processing)
        auditory_learning = self._calculate_auditory_learning(correlation_dimension, graph_density, 
                                                            betweenness_centrality, information_dimension)
        
        # 3. Kinesthetic Learning Analysis (DMIT Principle: High ridge density + clustering coefficient = kinesthetic processing)
        kinesthetic_learning = self._calculate_kinesthetic_learning(ridge_density, clustering_coefficient, 
                                                                  modularity, ridge_thickness)
        
        # 4. Reading/Writing Learning Analysis (DMIT Principle: High pattern regularity + low lacunarity = reading/writing)
        reading_writing_learning = self._calculate_reading_writing_learning(pattern_regularity, lacunarity, 
                                                                          ridge_continuity, std_intensity)
        
        # 5. Social Learning Analysis (DMIT Principle: High community cohesion + spectral radius = social learning)
        social_learning = self._calculate_social_learning(community_cohesion, spectral_radius, 
                                                        topological_complexity, euler_characteristic)
        
        # 6. Solitary Learning Analysis (DMIT Principle: High ridge uniformity + pattern type = solitary learning)
        solitary_learning = self._calculate_solitary_learning(ridge_uniformity, pattern_type, 
                                                            ridge_curvature, spectral_energy)
        
        # 7. Logical Learning Analysis (DMIT Principle: High ridge count + fractal dimension = logical learning)
        logical_learning = self._calculate_logical_learning(tfrc, box_counting_dimension, 
                                                          h1_num_features, betti_1)
        
        # 8. Creative Learning Analysis (DMIT Principle: High fractal complexity + spectral features = creative learning)
        creative_learning = self._calculate_creative_learning(fractal_complexity, spectral_centroid, spectral_rolloff, 
                                                            graph_density, topological_complexity)
        
        # Determine primary learning style based on highest score
        learning_styles = {
            'visual': visual_learning,
            'auditory': auditory_learning,
            'kinesthetic': kinesthetic_learning,
            'reading_writing': reading_writing_learning,
            'social': social_learning,
            'solitary': solitary_learning,
            'logical': logical_learning,
            'creative': creative_learning
        }
        primary_style = max(learning_styles.items(), key=lambda x: x[1])[0]
        
        # Calculate overall learning effectiveness score
        learning_effectiveness_score = (
            visual_learning * 0.15 +                 # Visual learning
            auditory_learning * 0.15 +               # Auditory learning
            kinesthetic_learning * 0.15 +            # Kinesthetic learning
            reading_writing_learning * 0.15 +        # Reading/writing learning
            social_learning * 0.12 +                 # Social learning
            solitary_learning * 0.12 +               # Solitary learning
            logical_learning * 0.08 +                # Logical learning
            creative_learning * 0.08                 # Creative learning
        )
        
        # Normalize to 0-1 range
        learning_effectiveness_score = max(0.0, min(1.0, learning_effectiveness_score))
        
        return {
            'learning_effectiveness_score': learning_effectiveness_score,
            'primary_learning_style': primary_style,
            'visual_learning': visual_learning,
            'auditory_learning': auditory_learning,
            'kinesthetic_learning': kinesthetic_learning,
            'reading_writing_learning': reading_writing_learning,
            'social_learning': social_learning,
            'solitary_learning': solitary_learning,
            'logical_learning': logical_learning,
            'creative_learning': creative_learning,
            'multimodal_learning': max(visual_learning, auditory_learning, kinesthetic_learning),
            'cognitive_learning': logical_learning + reading_writing_learning,
            'experiential_learning': kinesthetic_learning + creative_learning,
            'collaborative_learning': social_learning + auditory_learning,
            'independent_learning': solitary_learning + reading_writing_learning,
            'learning_style_profile': self.classify_learning_style(primary_style, learning_effectiveness_score)
        }

    def _calculate_visual_learning(self, information_dimension: float, entropy: float,
                                 pattern_symmetry: float, spectral_entropy: float) -> float:
        """Calculate visual learning from fingerprint features (DMIT principle)"""
        # DMIT research shows: High information dimension + entropy = visual processing
        
        # Information dimension contribution
        if 1.5 <= information_dimension <= 2.0:
            info_score = (information_dimension - 1.5) / 0.5
        else:
            info_score = 0.5
        
        # Entropy contribution (higher entropy = more complex visual processing)
        if entropy > 0:
            entropy_score = min(1.0, entropy / 8.0)  # Normalize to 0-1
        else:
            entropy_score = 0.5
        
        # Pattern symmetry contribution
        symmetry_score = min(1.0, pattern_symmetry)
        
        # Spectral entropy contribution
        spectral_score = min(1.0, spectral_entropy)
        
        # Combine scores
        visual_learning = (info_score * 0.35 + entropy_score * 0.25 + symmetry_score * 0.25 + spectral_score * 0.15)
        return min(1.0, visual_learning)
    
    def _calculate_auditory_learning(self, correlation_dimension: float, graph_density: float,
                                   betweenness_centrality: float, information_dimension: float) -> float:
        """Calculate auditory learning from fingerprint features (DMIT principle)"""
        # DMIT research shows: High correlation dimension + graph density = auditory processing
        
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
        auditory_learning = (corr_score * 0.3 + density_score * 0.25 + centrality_score * 0.25 + info_score * 0.2)
        return min(1.0, auditory_learning)
    
    def _calculate_kinesthetic_learning(self, ridge_density: float, clustering_coefficient: float,
                                      modularity: float, ridge_thickness: float) -> float:
        """Calculate kinesthetic learning from fingerprint features (DMIT principle)"""
        # DMIT research shows: High ridge density + clustering coefficient = kinesthetic processing
        
        # Ridge density contribution
        density_score = min(1.0, ridge_density)
        
        # Clustering coefficient contribution
        clustering_score = min(1.0, clustering_coefficient)
        
        # Modularity contribution
        modularity_score = min(1.0, modularity)
        
        # Ridge thickness contribution
        thickness_score = min(1.0, ridge_thickness)
        
        # Combine scores
        kinesthetic_learning = (density_score * 0.3 + clustering_score * 0.25 + modularity_score * 0.25 + thickness_score * 0.2)
        return min(1.0, kinesthetic_learning)
    
    def _calculate_reading_writing_learning(self, pattern_regularity: float, lacunarity: float,
                                          ridge_continuity: float, std_intensity: float) -> float:
        """Calculate reading/writing learning from fingerprint features (DMIT principle)"""
        # DMIT research shows: High pattern regularity + low lacunarity = reading/writing preference
        
        # Pattern regularity contribution
        regularity_score = min(1.0, pattern_regularity)
        
        # Lacunarity contribution (lower lacunarity = more regular = better reading/writing)
        lacunarity_score = max(0.0, 1.0 - lacunarity)
        
        # Ridge continuity contribution
        continuity_score = min(1.0, ridge_continuity)
        
        # Standard deviation contribution (lower variation = more consistent = better reading/writing)
        if std_intensity > 0:
            std_score = max(0.0, 1.0 - (std_intensity / 100.0))
        else:
            std_score = 0.5
        
        # Combine scores
        reading_writing_learning = (regularity_score * 0.3 + lacunarity_score * 0.25 + continuity_score * 0.25 + std_score * 0.2)
        return min(1.0, reading_writing_learning)
    
    def _calculate_social_learning(self, community_cohesion: float, spectral_radius: float,
                                 topological_complexity: float, euler_characteristic: int) -> float:
        """Calculate social learning from fingerprint features (DMIT principle)"""
        # DMIT research shows: High community cohesion + spectral radius = social learning
        
        # Community cohesion contribution
        cohesion_score = min(1.0, community_cohesion)
        
        # Spectral radius contribution
        if spectral_radius > 0:
            spectral_score = min(1.0, spectral_radius / 10.0)
        else:
            spectral_score = 0.5
        
        # Topological complexity contribution
        complexity_score = min(1.0, topological_complexity)
        
        # Euler characteristic contribution (more negative = more complex = better social learning)
        if euler_characteristic < 0:
            euler_score = min(1.0, abs(euler_characteristic) / 10.0)
        else:
            euler_score = 0.3
        
        # Combine scores
        social_learning = (cohesion_score * 0.3 + spectral_score * 0.25 + complexity_score * 0.25 + euler_score * 0.2)
        return min(1.0, social_learning)
    
    def _calculate_solitary_learning(self, ridge_uniformity: float, pattern_type: str,
                                   ridge_curvature: float, spectral_energy: float) -> float:
        """Calculate solitary learning from fingerprint features (DMIT principle)"""
        # DMIT research shows: High ridge uniformity + pattern type = solitary learning
        
        # Ridge uniformity contribution
        uniformity_score = min(1.0, ridge_uniformity)
        
        # Pattern type contribution
        pattern_weights = {
            'whorl': 0.8,      # Complex patterns indicate solitary learning
            'loop': 0.7,       # Good solitary learning
            'arch': 0.6,       # Moderate solitary learning
            'tented_arch': 0.65, # Slightly better than plain arch
            'composite': 0.75   # Complex solitary patterns
        }
        pattern_score = pattern_weights.get(pattern_type.lower(), 0.6)
        
        # Ridge curvature contribution
        curvature_score = min(1.0, ridge_curvature)
        
        # Spectral energy contribution
        energy_score = min(1.0, spectral_energy)
        
        # Combine scores
        solitary_learning = (uniformity_score * 0.3 + pattern_score * 0.25 + curvature_score * 0.25 + energy_score * 0.2)
        return min(1.0, solitary_learning)
    
    def _calculate_logical_learning(self, tfrc: int, box_counting_dimension: float,
                                  h1_num_features: int, betti_1: int) -> float:
        """Calculate logical learning from fingerprint features (DMIT principle)"""
        # DMIT research shows: High ridge count + fractal dimension = logical learning
        
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
        
        # H1 features contribution (loops/holes - complexity in logical learning)
        h1_score = min(1.0, h1_num_features / 10.0)
        
        # Betti-1 contribution (logical loops)
        betti_score = min(1.0, betti_1 / 10.0)
        
        # Combine scores
        logical_learning = (ridge_score * 0.35 + fractal_score * 0.25 + h1_score * 0.25 + betti_score * 0.15)
        return min(1.0, logical_learning)
    
    def _calculate_creative_learning(self, fractal_complexity: float, spectral_centroid: float, spectral_rolloff: float,
                                   graph_density: float, topological_complexity: float) -> float:
        """Calculate creative learning from fingerprint features (DMIT principle)"""
        # DMIT research shows: High fractal complexity + spectral features = creative learning
        
        # Fractal complexity contribution
        complexity_score = min(1.0, fractal_complexity)
        
        # Spectral centroid contribution
        centroid_score = min(1.0, spectral_centroid)
        
        # Spectral rolloff contribution
        rolloff_score = min(1.0, spectral_rolloff)
        
        # Graph density contribution
        density_score = min(1.0, graph_density)
        
        # Topological complexity contribution
        topological_score = min(1.0, topological_complexity)
        
        # Combine scores
        creative_learning = (complexity_score * 0.25 + centroid_score * 0.2 + rolloff_score * 0.2 + density_score * 0.2 + topological_score * 0.15)
        return min(1.0, creative_learning)

    @staticmethod
    def classify_learning_style(primary_style: str, effectiveness_score: float) -> str:
        if effectiveness_score >= 0.85:
            level = "Exceptional"
        elif effectiveness_score >= 0.75:
            level = "High"
        elif effectiveness_score >= 0.65:
            level = "Above Average"
        elif effectiveness_score >= 0.55:
            level = "Average"
        else:
            level = "Developing"
        
        style_names = {
            'visual': 'Visual Learning',
            'auditory': 'Auditory Learning',
            'kinesthetic': 'Kinesthetic Learning',
            'reading_writing': 'Reading/Writing Learning',
            'social': 'Social Learning',
            'solitary': 'Solitary Learning',
            'logical': 'Logical Learning',
            'creative': 'Creative Learning'
        }
        
        return f"{level} {style_names.get(primary_style, 'Learning')}" 