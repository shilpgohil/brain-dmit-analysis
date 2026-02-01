from typing import Dict, Any
from .base import DMITExtensionBase

class SystemsThinkingExtension(DMITExtensionBase):
    """
    Extension for analyzing Systems Thinking abilities from fingerprint features.
    Uses comprehensive DMIT scientific correlations between fingerprint patterns and systems thinking processes.
    """
    def analyze(self, features: Dict[str, Any]) -> Dict[str, Any]:
        # Extract comprehensive fingerprint features for systems thinking analysis
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
        
        # Calculate systems thinking abilities using comprehensive DMIT scientific correlations
        
        # 1. Holistic Thinking Analysis (DMIT Principle: High information dimension + entropy = holistic thinking)
        holistic_thinking = self._calculate_holistic_thinking(information_dimension, entropy, 
                                                            pattern_symmetry, spectral_entropy)
        
        # 2. Pattern Recognition Analysis (DMIT Principle: High correlation dimension + graph density = pattern recognition)
        pattern_recognition = self._calculate_pattern_recognition(correlation_dimension, graph_density, 
                                                                betweenness_centrality, information_dimension)
        
        # 3. Interconnectedness Analysis (DMIT Principle: High ridge count + fractal complexity = interconnectedness)
        interconnectedness = self._calculate_interconnectedness(tfrc, box_counting_dimension, 
                                                              h1_num_features, betti_1)
        
        # 4. Systems Mapping Analysis (DMIT Principle: High spectral radius + topological complexity = systems mapping)
        systems_mapping = self._calculate_systems_mapping(spectral_radius, topological_complexity, 
                                                        euler_characteristic, spectral_bandwidth)
        
        # 5. Feedback Loop Analysis (DMIT Principle: High ridge density + clustering coefficient = feedback loops)
        feedback_loops = self._calculate_feedback_loops(ridge_density, clustering_coefficient, 
                                                      modularity, ridge_thickness)
        
        # 6. Emergence Understanding Analysis (DMIT Principle: High ridge uniformity + pattern type = emergence understanding)
        emergence_understanding = self._calculate_emergence_understanding(ridge_uniformity, pattern_type, 
                                                                        ridge_curvature, community_cohesion)
        
        # 7. Complexity Management Analysis (DMIT Principle: High pattern regularity + low lacunarity = complexity management)
        complexity_management = self._calculate_complexity_management(pattern_regularity, lacunarity, 
                                                                    ridge_continuity, std_intensity)
        
        # 8. Systems Intelligence Analysis (DMIT Principle: High spectral features + graph complexity = systems intelligence)
        systems_intelligence = self._calculate_systems_intelligence(spectral_centroid, spectral_rolloff, 
                                                                  graph_density, topological_complexity)
        
        # Overall systems thinking score (comprehensive weighted combination)
        systems_thinking_score = (
            holistic_thinking * 0.20 +            # Holistic thinking is fundamental
            pattern_recognition * 0.18 +          # Pattern recognition is crucial
            interconnectedness * 0.15 +           # Interconnectedness is important
            systems_mapping * 0.15 +              # Systems mapping is essential
            feedback_loops * 0.12 +               # Feedback loops
            emergence_understanding * 0.10 +      # Emergence understanding
            complexity_management * 0.07 +        # Complexity management
            systems_intelligence * 0.03           # Systems intelligence
        )
        
        # Normalize to 0-1 range
        systems_thinking_score = max(0.0, min(1.0, systems_thinking_score))
        
        # Determine systems thinking style based on dominant features
        thinking_styles = {
            'holistic': holistic_thinking + systems_intelligence,
            'pattern': pattern_recognition + complexity_management,
            'interconnected': interconnectedness + feedback_loops,
            'mapping': systems_mapping + emergence_understanding,
            'complex': complexity_management + holistic_thinking,
            'intelligent': systems_intelligence + pattern_recognition
        }
        primary_style = max(thinking_styles.items(), key=lambda x: x[1])[0]

        return {
            'systems_thinking_score': systems_thinking_score,
            'primary_thinking_style': primary_style,
            'holistic_thinking': holistic_thinking,
            'pattern_recognition': pattern_recognition,
            'interconnectedness': interconnectedness,
            'systems_mapping': systems_mapping,
            'feedback_loops': feedback_loops,
            'emergence_understanding': emergence_understanding,
            'complexity_management': complexity_management,
            'systems_intelligence': systems_intelligence,
            'big_picture_thinking': holistic_thinking + systems_mapping,
            'pattern_analysis': pattern_recognition + complexity_management,
            'system_understanding': interconnectedness + feedback_loops,
            'complexity_navigation': complexity_management + emergence_understanding,
            'systems_insight': systems_intelligence + holistic_thinking,
            'thinking_profile': self.classify_thinking_level(systems_thinking_score)
        }

    def _calculate_holistic_thinking(self, information_dimension: float, entropy: float,
                                   pattern_symmetry: float, spectral_entropy: float) -> float:
        """Calculate holistic thinking from fingerprint features (DMIT principle)"""
        # DMIT research shows: High information dimension + entropy = holistic thinking
        
        # Information dimension contribution
        if 1.5 <= information_dimension <= 2.0:
            info_score = (information_dimension - 1.5) / 0.5
        else:
            info_score = 0.5
        
        # Entropy contribution (higher entropy = more complex holistic understanding)
        if entropy > 0:
            entropy_score = min(1.0, entropy / 8.0)  # Normalize to 0-1
        else:
            entropy_score = 0.5
        
        # Pattern symmetry contribution
        symmetry_score = min(1.0, pattern_symmetry)
        
        # Spectral entropy contribution
        spectral_score = min(1.0, spectral_entropy)
        
        # Combine scores
        holistic_thinking = (info_score * 0.35 + entropy_score * 0.25 + symmetry_score * 0.25 + spectral_score * 0.15)
        return min(1.0, holistic_thinking)
    
    def _calculate_pattern_recognition(self, correlation_dimension: float, graph_density: float,
                                     betweenness_centrality: float, information_dimension: float) -> float:
        """Calculate pattern recognition from fingerprint features (DMIT principle)"""
        # DMIT research shows: High correlation dimension + graph density = pattern recognition
        
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
        pattern_recognition = (corr_score * 0.3 + density_score * 0.25 + centrality_score * 0.25 + info_score * 0.2)
        return min(1.0, pattern_recognition)
    
    def _calculate_interconnectedness(self, tfrc: int, box_counting_dimension: float,
                                    h1_num_features: int, betti_1: int) -> float:
        """Calculate interconnectedness from fingerprint features (DMIT principle)"""
        # DMIT research shows: High ridge count + fractal complexity = interconnectedness
        
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
        
        # H1 features contribution (loops/holes - complexity in interconnectedness)
        h1_score = min(1.0, h1_num_features / 10.0)
        
        # Betti-1 contribution (interconnection loops)
        betti_score = min(1.0, betti_1 / 10.0)
        
        # Combine scores
        interconnectedness = (ridge_score * 0.35 + fractal_score * 0.25 + h1_score * 0.25 + betti_score * 0.15)
        return min(1.0, interconnectedness)
    
    def _calculate_systems_mapping(self, spectral_radius: float, topological_complexity: float,
                                 euler_characteristic: int, spectral_bandwidth: float) -> float:
        """Calculate systems mapping from fingerprint features (DMIT principle)"""
        # DMIT research shows: High spectral radius + topological complexity = systems mapping
        
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
        systems_mapping = (spectral_score * 0.3 + complexity_score * 0.25 + euler_score * 0.25 + bandwidth_score * 0.2)
        return min(1.0, systems_mapping)
    
    def _calculate_feedback_loops(self, ridge_density: float, clustering_coefficient: float,
                                modularity: float, ridge_thickness: float) -> float:
        """Calculate feedback loops from fingerprint features (DMIT principle)"""
        # DMIT research shows: High ridge density + clustering coefficient = feedback loops
        
        # Ridge density contribution
        density_score = min(1.0, ridge_density)
        
        # Clustering coefficient contribution
        clustering_score = min(1.0, clustering_coefficient)
        
        # Modularity contribution
        modularity_score = min(1.0, modularity)
        
        # Ridge thickness contribution
        thickness_score = min(1.0, ridge_thickness)
        
        # Combine scores
        feedback_loops = (density_score * 0.3 + clustering_score * 0.25 + modularity_score * 0.25 + thickness_score * 0.2)
        return min(1.0, feedback_loops)
    
    def _calculate_emergence_understanding(self, ridge_uniformity: float, pattern_type: str,
                                         ridge_curvature: float, community_cohesion: float) -> float:
        """Calculate emergence understanding from fingerprint features (DMIT principle)"""
        # DMIT research shows: High ridge uniformity + pattern type = emergence understanding
        
        # Ridge uniformity contribution
        uniformity_score = min(1.0, ridge_uniformity)
        
        # Pattern type contribution
        pattern_weights = {
            'whorl': 0.8,      # Complex patterns indicate good emergence understanding
            'loop': 0.7,       # Good emergence understanding
            'arch': 0.6,       # Moderate emergence understanding
            'tented_arch': 0.65, # Slightly better than plain arch
            'composite': 0.75   # Complex emergence understanding patterns
        }
        pattern_score = pattern_weights.get(pattern_type.lower(), 0.6)
        
        # Ridge curvature contribution
        curvature_score = min(1.0, ridge_curvature)
        
        # Community cohesion contribution
        cohesion_score = min(1.0, community_cohesion)
        
        # Combine scores
        emergence_understanding = (uniformity_score * 0.3 + pattern_score * 0.25 + curvature_score * 0.25 + cohesion_score * 0.2)
        return min(1.0, emergence_understanding)
    
    def _calculate_complexity_management(self, pattern_regularity: float, lacunarity: float,
                                       ridge_continuity: float, std_intensity: float) -> float:
        """Calculate complexity management from fingerprint features (DMIT principle)"""
        # DMIT research shows: High pattern regularity + low lacunarity = complexity management
        
        # Pattern regularity contribution
        regularity_score = min(1.0, pattern_regularity)
        
        # Lacunarity contribution (lower lacunarity = more regular = better complexity management)
        lacunarity_score = max(0.0, 1.0 - lacunarity)
        
        # Ridge continuity contribution
        continuity_score = min(1.0, ridge_continuity)
        
        # Standard deviation contribution (lower variation = more consistent = better complexity management)
        if std_intensity > 0:
            std_score = max(0.0, 1.0 - (std_intensity / 100.0))
        else:
            std_score = 0.5
        
        # Combine scores
        complexity_management = (regularity_score * 0.3 + lacunarity_score * 0.25 + continuity_score * 0.25 + std_score * 0.2)
        return min(1.0, complexity_management)
    
    def _calculate_systems_intelligence(self, spectral_centroid: float, spectral_rolloff: float,
                                      graph_density: float, topological_complexity: float) -> float:
        """Calculate systems intelligence from fingerprint features (DMIT principle)"""
        # DMIT research shows: High spectral features + graph complexity = systems intelligence
        
        # Spectral centroid contribution
        centroid_score = min(1.0, spectral_centroid)
        
        # Spectral rolloff contribution
        rolloff_score = min(1.0, spectral_rolloff)
        
        # Graph density contribution
        density_score = min(1.0, graph_density)
        
        # Topological complexity contribution
        complexity_score = min(1.0, topological_complexity)
        
        # Combine scores
        systems_intelligence = (centroid_score * 0.3 + rolloff_score * 0.25 + density_score * 0.25 + complexity_score * 0.2)
        return min(1.0, systems_intelligence)

    @staticmethod
    def classify_thinking_level(score: float) -> str:
        """Classify systems thinking level based on score"""
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