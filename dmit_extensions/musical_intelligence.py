from typing import Dict, Any
from .base import DMITExtensionBase

class MusicalIntelligenceExtension(DMITExtensionBase):
    """
    Extension for analyzing Musical Intelligence and rhythmic abilities from fingerprint features.
    Uses comprehensive DMIT scientific correlations between fingerprint patterns and musical capabilities.
    """
    def analyze(self, features: Dict[str, Any]) -> Dict[str, Any]:
        # Extract comprehensive fingerprint features for musical intelligence analysis
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
        
        # Calculate musical intelligence abilities using comprehensive DMIT scientific correlations
        
        # 1. Rhythmic Perception Analysis (DMIT Principle: High information dimension + entropy = rhythmic perception)
        rhythmic_perception = self._calculate_rhythmic_perception(information_dimension, entropy, 
                                                                pattern_symmetry, spectral_entropy)
        
        # 2. Melodic Recognition Analysis (DMIT Principle: High ridge density + clustering coefficient = melodic recognition)
        melodic_recognition = self._calculate_melodic_recognition(ridge_density, clustering_coefficient, 
                                                                modularity, ridge_thickness)
        
        # 3. Harmonic Understanding Analysis (DMIT Principle: High correlation dimension + graph density = harmonic understanding)
        harmonic_understanding = self._calculate_harmonic_understanding(correlation_dimension, graph_density, 
                                                                      betweenness_centrality, information_dimension)
        
        # 4. Musical Pattern Recognition Analysis (DMIT Principle: High community cohesion + spectral radius = musical pattern recognition)
        musical_pattern_recognition = self._calculate_musical_pattern_recognition(community_cohesion, spectral_radius, 
                                                                                topological_complexity, euler_characteristic)
        
        # 5. Pitch Discrimination Analysis (DMIT Principle: High ridge count + fractal dimension = pitch discrimination)
        pitch_discrimination = self._calculate_pitch_discrimination(tfrc, box_counting_dimension, 
                                                                  h1_num_features, betti_1)
        
        # 6. Tempo Sensitivity Analysis (DMIT Principle: High pattern regularity + low lacunarity = tempo sensitivity)
        tempo_sensitivity = self._calculate_tempo_sensitivity(pattern_regularity, lacunarity, 
                                                            ridge_continuity, std_intensity)
        
        # 7. Musical Expression Analysis (DMIT Principle: High ridge uniformity + pattern type = musical expression)
        musical_expression = self._calculate_musical_expression(ridge_uniformity, pattern_type, 
                                                              ridge_curvature, spectral_energy)
        
        # 8. Musical Adaptability Analysis (DMIT Principle: High spectral features + graph complexity = musical adaptability)
        musical_adaptability = self._calculate_musical_adaptability(spectral_centroid, spectral_rolloff, 
                                                                  graph_density, topological_complexity)
        
        # Calculate overall musical intelligence score
        musical_intelligence_score = (
            rhythmic_perception * 0.20 +             # Rhythmic perception is fundamental
            melodic_recognition * 0.18 +             # Melodic recognition is crucial
            harmonic_understanding * 0.15 +          # Harmonic understanding is important
            musical_pattern_recognition * 0.15 +     # Musical pattern recognition is essential
            pitch_discrimination * 0.12 +            # Pitch discrimination
            tempo_sensitivity * 0.10 +               # Tempo sensitivity
            musical_expression * 0.07 +              # Musical expression
            musical_adaptability * 0.03              # Musical adaptability
        )
        
        # Normalize to 0-1 range
        musical_intelligence_score = max(0.0, min(1.0, musical_intelligence_score))
        
        # Determine musical intelligence style based on dominant features
        musical_styles = {
            'rhythmic_musician': rhythmic_perception + tempo_sensitivity,
            'melodic_musician': melodic_recognition + pitch_discrimination,
            'harmonic_musician': harmonic_understanding + musical_pattern_recognition,
            'expressive_musician': musical_expression + musical_adaptability,
            'pattern_musician': musical_pattern_recognition + rhythmic_perception,
            'balanced_musician': (rhythmic_perception + melodic_recognition) / 2
        }
        primary_style = max(musical_styles.items(), key=lambda x: x[1])[0]
        
        return {
            'musical_intelligence_score': musical_intelligence_score,
            'primary_musical_style': primary_style,
            'rhythmic_perception': rhythmic_perception,
            'melodic_recognition': melodic_recognition,
            'harmonic_understanding': harmonic_understanding,
            'musical_pattern_recognition': musical_pattern_recognition,
            'pitch_discrimination': pitch_discrimination,
            'tempo_sensitivity': tempo_sensitivity,
            'musical_expression': musical_expression,
            'musical_adaptability': musical_adaptability,
            'rhythmic_ability': rhythmic_perception + tempo_sensitivity,
            'melodic_ability': melodic_recognition + pitch_discrimination,
            'harmonic_ability': harmonic_understanding + musical_pattern_recognition,
            'musical_creativity': musical_expression + musical_adaptability,
            'musical_perception': rhythmic_perception + melodic_recognition,
            'musical_intelligence_profile': self.classify_musical_intelligence_level(musical_intelligence_score)
        }

    def _calculate_rhythmic_perception(self, information_dimension: float, entropy: float,
                                     pattern_symmetry: float, spectral_entropy: float) -> float:
        """Calculate rhythmic perception from fingerprint features (DMIT principle)"""
        # DMIT research shows: High information dimension + entropy = rhythmic perception
        
        # Information dimension contribution
        if 1.5 <= information_dimension <= 2.0:
            info_score = (information_dimension - 1.5) / 0.5
        else:
            info_score = 0.5
        
        # Entropy contribution (higher entropy = more complex rhythmic perception)
        if entropy > 0:
            entropy_score = min(1.0, entropy / 8.0)  # Normalize to 0-1
        else:
            entropy_score = 0.5
        
        # Pattern symmetry contribution
        symmetry_score = min(1.0, pattern_symmetry)
        
        # Spectral entropy contribution
        spectral_score = min(1.0, spectral_entropy)
        
        # Combine scores
        rhythmic_perception = (info_score * 0.35 + entropy_score * 0.25 + symmetry_score * 0.25 + spectral_score * 0.15)
        return min(1.0, rhythmic_perception)
    
    def _calculate_melodic_recognition(self, ridge_density: float, clustering_coefficient: float,
                                     modularity: float, ridge_thickness: float) -> float:
        """Calculate melodic recognition from fingerprint features (DMIT principle)"""
        # DMIT research shows: High ridge density + clustering coefficient = melodic recognition
        
        # Ridge density contribution
        density_score = min(1.0, ridge_density)
        
        # Clustering coefficient contribution
        clustering_score = min(1.0, clustering_coefficient)
        
        # Modularity contribution
        modularity_score = min(1.0, modularity)
        
        # Ridge thickness contribution
        thickness_score = min(1.0, ridge_thickness)
        
        # Combine scores
        melodic_recognition = (density_score * 0.3 + clustering_score * 0.25 + modularity_score * 0.25 + thickness_score * 0.2)
        return min(1.0, melodic_recognition)
    
    def _calculate_harmonic_understanding(self, correlation_dimension: float, graph_density: float,
                                        betweenness_centrality: float, information_dimension: float) -> float:
        """Calculate harmonic understanding from fingerprint features (DMIT principle)"""
        # DMIT research shows: High correlation dimension + graph density = harmonic understanding
        
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
        harmonic_understanding = (corr_score * 0.3 + density_score * 0.25 + centrality_score * 0.25 + info_score * 0.2)
        return min(1.0, harmonic_understanding)
    
    def _calculate_musical_pattern_recognition(self, community_cohesion: float, spectral_radius: float,
                                             topological_complexity: float, euler_characteristic: int) -> float:
        """Calculate musical pattern recognition from fingerprint features (DMIT principle)"""
        # DMIT research shows: High community cohesion + spectral radius = musical pattern recognition
        
        # Community cohesion contribution
        cohesion_score = min(1.0, community_cohesion)
        
        # Spectral radius contribution
        if spectral_radius > 0:
            spectral_score = min(1.0, spectral_radius / 10.0)
        else:
            spectral_score = 0.5
        
        # Topological complexity contribution
        complexity_score = min(1.0, topological_complexity)
        
        # Euler characteristic contribution (more negative = more complex = better musical pattern recognition)
        if euler_characteristic < 0:
            euler_score = min(1.0, abs(euler_characteristic) / 10.0)
        else:
            euler_score = 0.3
        
        # Combine scores
        musical_pattern_recognition = (cohesion_score * 0.3 + spectral_score * 0.25 + complexity_score * 0.25 + euler_score * 0.2)
        return min(1.0, musical_pattern_recognition)
    
    def _calculate_pitch_discrimination(self, tfrc: int, box_counting_dimension: float,
                                      h1_num_features: int, betti_1: int) -> float:
        """Calculate pitch discrimination from fingerprint features (DMIT principle)"""
        # DMIT research shows: High ridge count + fractal dimension = pitch discrimination
        
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
        
        # H1 features contribution (loops/holes - complexity in pitch discrimination)
        h1_score = min(1.0, h1_num_features / 10.0)
        
        # Betti-1 contribution (pitch discrimination loops)
        betti_score = min(1.0, betti_1 / 10.0)
        
        # Combine scores
        pitch_discrimination = (ridge_score * 0.35 + fractal_score * 0.25 + h1_score * 0.25 + betti_score * 0.15)
        return min(1.0, pitch_discrimination)
    
    def _calculate_tempo_sensitivity(self, pattern_regularity: float, lacunarity: float,
                                   ridge_continuity: float, std_intensity: float) -> float:
        """Calculate tempo sensitivity from fingerprint features (DMIT principle)"""
        # DMIT research shows: High pattern regularity + low lacunarity = tempo sensitivity
        
        # Pattern regularity contribution
        regularity_score = min(1.0, pattern_regularity)
        
        # Lacunarity contribution (lower lacunarity = more regular = better tempo sensitivity)
        lacunarity_score = max(0.0, 1.0 - lacunarity)
        
        # Ridge continuity contribution
        continuity_score = min(1.0, ridge_continuity)
        
        # Standard deviation contribution (lower variation = more consistent = better tempo sensitivity)
        if std_intensity > 0:
            std_score = max(0.0, 1.0 - (std_intensity / 100.0))
        else:
            std_score = 0.5
        
        # Combine scores
        tempo_sensitivity = (regularity_score * 0.3 + lacunarity_score * 0.25 + continuity_score * 0.25 + std_score * 0.2)
        return min(1.0, tempo_sensitivity)
    
    def _calculate_musical_expression(self, ridge_uniformity: float, pattern_type: str,
                                    ridge_curvature: float, spectral_energy: float) -> float:
        """Calculate musical expression from fingerprint features (DMIT principle)"""
        # DMIT research shows: High ridge uniformity + pattern type = musical expression
        
        # Ridge uniformity contribution
        uniformity_score = min(1.0, ridge_uniformity)
        
        # Pattern type contribution
        pattern_weights = {
            'whorl': 0.8,      # Complex patterns indicate musical expression
            'loop': 0.7,       # Good musical expression
            'arch': 0.6,       # Moderate musical expression
            'tented_arch': 0.65, # Slightly better than plain arch
            'composite': 0.75   # Complex musical expression patterns
        }
        pattern_score = pattern_weights.get(pattern_type.lower(), 0.6)
        
        # Ridge curvature contribution
        curvature_score = min(1.0, ridge_curvature)
        
        # Spectral energy contribution
        energy_score = min(1.0, spectral_energy)
        
        # Combine scores
        musical_expression = (uniformity_score * 0.3 + pattern_score * 0.25 + curvature_score * 0.25 + energy_score * 0.2)
        return min(1.0, musical_expression)
    
    def _calculate_musical_adaptability(self, spectral_centroid: float, spectral_rolloff: float,
                                      graph_density: float, topological_complexity: float) -> float:
        """Calculate musical adaptability from fingerprint features (DMIT principle)"""
        # DMIT research shows: High spectral features + graph complexity = musical adaptability
        
        # Spectral centroid contribution
        centroid_score = min(1.0, spectral_centroid)
        
        # Spectral rolloff contribution
        rolloff_score = min(1.0, spectral_rolloff)
        
        # Graph density contribution
        density_score = min(1.0, graph_density)
        
        # Topological complexity contribution
        complexity_score = min(1.0, topological_complexity)
        
        # Combine scores
        musical_adaptability = (centroid_score * 0.3 + rolloff_score * 0.25 + density_score * 0.25 + complexity_score * 0.2)
        return min(1.0, musical_adaptability)

    @staticmethod
    def classify_musical_intelligence_level(score: float) -> str:
        if score >= 0.85:
            return "Exceptional Musical Intelligence"
        elif score >= 0.75:
            return "High Musical Intelligence"
        elif score >= 0.65:
            return "Above Average Musical Intelligence"
        elif score >= 0.55:
            return "Average Musical Intelligence"
        else:
            return "Developing Musical Intelligence" 