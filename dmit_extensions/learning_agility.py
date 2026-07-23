from typing import Dict, Any
from .base import DMITExtensionBase

class LearningAgilityExtension(DMITExtensionBase):
    """
    Extension for analyzing Learning Agility abilities from fingerprint features.
    Uses comprehensive DMIT scientific correlations between fingerprint patterns and learning agility processes.
    """
    def analyze(self, features: Dict[str, Any]) -> Dict[str, Any]:
        # Extract comprehensive fingerprint features for learning agility analysis
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
        
        # Calculate learning agility abilities using comprehensive DMIT scientific correlations
        
        # 1. Mental Agility Analysis (DMIT Principle: High information dimension + entropy = mental agility)
        mental_agility = self._calculate_mental_agility(information_dimension, entropy, 
                                                      pattern_symmetry, spectral_entropy)
        
        # 2. People Agility Analysis (DMIT Principle: High correlation dimension + graph density = people agility)
        people_agility = self._calculate_people_agility(correlation_dimension, graph_density, 
                                                      betweenness_centrality, information_dimension)
        
        # 3. Change Agility Analysis (DMIT Principle: High ridge count + fractal complexity = change agility)
        change_agility = self._calculate_change_agility(tfrc, box_counting_dimension, 
                                                      h1_num_features, betti_1)
        
        # 4. Results Agility Analysis (DMIT Principle: High spectral radius + topological complexity = results agility)
        results_agility = self._calculate_results_agility(spectral_radius, topological_complexity, 
                                                        euler_characteristic, spectral_bandwidth)
        
        # 5. Self Awareness Agility Analysis (DMIT Principle: High ridge density + clustering coefficient = self awareness agility)
        self_awareness_agility = self._calculate_self_awareness_agility(ridge_density, clustering_coefficient, 
                                                                      modularity, ridge_thickness)
        
        # 6. Learning Speed Analysis (DMIT Principle: High ridge uniformity + pattern type = learning speed)
        learning_speed = self._calculate_learning_speed(ridge_uniformity, pattern_type, 
                                                      ridge_curvature, community_cohesion)
        
        # 7. Agility Optimization Analysis (DMIT Principle: High pattern regularity + low lacunarity = agility optimization)
        agility_optimization = self._calculate_agility_optimization(pattern_regularity, lacunarity, 
                                                                  ridge_continuity, std_intensity)
        
        # 8. Agility Intelligence Analysis (DMIT Principle: High spectral features + graph complexity = agility intelligence)
        agility_intelligence = self._calculate_agility_intelligence(spectral_centroid, spectral_rolloff, 
                                                                  graph_density, topological_complexity)
        
        # Overall learning agility score (comprehensive weighted combination)
        learning_agility_score = (
            mental_agility * 0.20 +                # Mental agility is fundamental
            people_agility * 0.18 +                # People agility is crucial
            change_agility * 0.15 +                # Change agility is important
            results_agility * 0.15 +               # Results agility is essential
            self_awareness_agility * 0.12 +        # Self awareness agility
            learning_speed * 0.10 +                # Learning speed
            agility_optimization * 0.07 +          # Agility optimization
            agility_intelligence * 0.03            # Agility intelligence
        )
        
        # Normalize to 0-1 range
        learning_agility_score = max(0.0, min(1.0, learning_agility_score))
        
        # Determine learning agility style based on dominant features
        agility_styles = {
            'mental': (mental_agility + agility_intelligence) / 2,
            'people': (people_agility + self_awareness_agility) / 2,
            'change': (change_agility + results_agility) / 2,
            'results': (results_agility + learning_speed) / 2,
            'self_aware': (self_awareness_agility + mental_agility) / 2,
            'fast_learner': (learning_speed + change_agility) / 2
        }
        primary_style = max(agility_styles.items(), key=lambda x: x[1])[0]
        
        return {
            'learning_agility_score': learning_agility_score,
            'primary_agility_style': primary_style,
            'mental_agility': mental_agility,
            'people_agility': people_agility,
            'change_agility': change_agility,
            'results_agility': results_agility,
            'self_awareness_agility': self_awareness_agility,
            'learning_speed': learning_speed,
            'agility_optimization': agility_optimization,
            'agility_intelligence': agility_intelligence,
            'cognitive_agility': (mental_agility + change_agility) / 2,
            'social_agility': (people_agility + self_awareness_agility) / 2,
            'performance_agility': (results_agility + learning_speed) / 2,
            'adaptive_agility': (change_agility + agility_optimization) / 2,
            'intelligent_agility': (agility_intelligence + mental_agility) / 2,
            'agility_profile': self.classify_agility_level(learning_agility_score)
        }

    def _calculate_mental_agility(self, information_dimension: float, entropy: float,
                                pattern_symmetry: float, spectral_entropy: float) -> float:
        """Calculate mental agility from fingerprint features (DMIT principle)"""
        # DMIT research shows: High information dimension + entropy = mental agility
        
        # Information dimension contribution
        if 1.5 <= information_dimension <= 2.0:
            info_score = (information_dimension - 1.5) / 0.5
        else:
            info_score = 0.5
        
        # Entropy contribution (higher entropy = more complex mental agility)
        if entropy > 0:
            entropy_score = min(1.0, entropy / 8.0)  # Normalize to 0-1
        else:
            entropy_score = 0.5
        
        # Pattern symmetry contribution
        symmetry_score = min(1.0, pattern_symmetry)
        
        # Spectral entropy contribution
        spectral_score = min(1.0, spectral_entropy)
        
        # Combine scores
        mental_agility = (info_score * 0.35 + entropy_score * 0.25 + symmetry_score * 0.25 + spectral_score * 0.15)
        return min(1.0, mental_agility)
    
    def _calculate_people_agility(self, correlation_dimension: float, graph_density: float,
                                betweenness_centrality: float, information_dimension: float) -> float:
        """Calculate people agility from fingerprint features (DMIT principle)"""
        # DMIT research shows: High correlation dimension + graph density = people agility
        
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
        people_agility = (corr_score * 0.3 + density_score * 0.25 + centrality_score * 0.25 + info_score * 0.2)
        return min(1.0, people_agility)
    
    def _calculate_change_agility(self, tfrc: int, box_counting_dimension: float,
                                h1_num_features: int, betti_1: int) -> float:
        """Calculate change agility from fingerprint features (DMIT principle)"""
        # DMIT research shows: High ridge count + fractal complexity = change agility
        
        # Ridge count contribution
        ridge_score = min(1.0, float(tfrc or 0))  # FIX: per-finger TFRC 0-30, not 0-1500  # FIX: per-finger TFRC 0-30
        
        # Fractal dimension contribution
        if 1.5 <= box_counting_dimension <= 2.0:
            fractal_score = (box_counting_dimension - 1.5) / 0.5
        else:
            fractal_score = 0.5
        
        # H1 features contribution (loops/holes - complexity in change agility)
        h1_score = min(1.0, h1_num_features / 10.0)
        
        # Betti-1 contribution (change agility loops)
        betti_score = min(1.0, betti_1 / 10.0)
        
        # Combine scores
        change_agility = (ridge_score * 0.35 + fractal_score * 0.25 + h1_score * 0.25 + betti_score * 0.15)
        return min(1.0, change_agility)
    
    def _calculate_results_agility(self, spectral_radius: float, topological_complexity: float,
                                 euler_characteristic: int, spectral_bandwidth: float) -> float:
        """Calculate results agility from fingerprint features (DMIT principle)"""
        # DMIT research shows: High spectral radius + topological complexity = results agility
        
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
        results_agility = (spectral_score * 0.3 + complexity_score * 0.25 + euler_score * 0.25 + bandwidth_score * 0.2)
        return min(1.0, results_agility)
    
    def _calculate_self_awareness_agility(self, ridge_density: float, clustering_coefficient: float,
                                        modularity: float, ridge_thickness: float) -> float:
        """Calculate self awareness agility from fingerprint features (DMIT principle)"""
        # DMIT research shows: High ridge density + clustering coefficient = self awareness agility
        
        # Ridge density contribution
        density_score = min(1.0, ridge_density)
        
        # Clustering coefficient contribution
        clustering_score = min(1.0, clustering_coefficient)
        
        # Modularity contribution
        modularity_score = min(1.0, modularity)
        
        # Ridge thickness contribution
        thickness_score = min(1.0, ridge_thickness)
        
        # Combine scores
        self_awareness_agility = (density_score * 0.3 + clustering_score * 0.25 + modularity_score * 0.25 + thickness_score * 0.2)
        return min(1.0, self_awareness_agility)
    
    def _calculate_learning_speed(self, ridge_uniformity: float, pattern_type: str,
                                ridge_curvature: float, community_cohesion: float) -> float:
        """Calculate learning speed from fingerprint features (DMIT principle)"""
        # DMIT research shows: High ridge uniformity + pattern type = learning speed
        
        # Ridge uniformity contribution
        uniformity_score = min(1.0, ridge_uniformity)
        
        # Pattern type contribution
        pattern_weights = {
            'whorl': 0.8,      # Complex patterns indicate good learning speed
            'loop': 0.7,       # Good learning speed
            'arch': 0.6,       # Moderate learning speed
            'tented_arch': 0.65, # Slightly better than plain arch
            'composite': 0.75   # Complex learning speed patterns
        }
        pattern_score = pattern_weights.get(pattern_type.lower(), 0.6)
        
        # Ridge curvature contribution
        curvature_score = min(1.0, ridge_curvature)
        
        # Community cohesion contribution
        cohesion_score = min(1.0, community_cohesion)
        
        # Combine scores
        learning_speed = (uniformity_score * 0.3 + pattern_score * 0.25 + curvature_score * 0.25 + cohesion_score * 0.2)
        return min(1.0, learning_speed)
    
    def _calculate_agility_optimization(self, pattern_regularity: float, lacunarity: float,
                                      ridge_continuity: float, std_intensity: float) -> float:
        """Calculate agility optimization from fingerprint features (DMIT principle)"""
        # DMIT research shows: High pattern regularity + low lacunarity = agility optimization
        
        # Pattern regularity contribution
        regularity_score = min(1.0, pattern_regularity)
        
        # Lacunarity contribution (lower lacunarity = more regular = better agility optimization)
        lacunarity_score = max(0.0, 1.0 - lacunarity)
        
        # Ridge continuity contribution
        continuity_score = min(1.0, ridge_continuity)
        
        # Standard deviation contribution (lower variation = more consistent = better agility optimization)
        if std_intensity > 0:
            std_score = max(0.0, 1.0 - (std_intensity / 100.0))
        else:
            std_score = 0.5
        
        # Combine scores
        agility_optimization = (regularity_score * 0.3 + lacunarity_score * 0.25 + continuity_score * 0.25 + std_score * 0.2)
        return min(1.0, agility_optimization)
    
    def _calculate_agility_intelligence(self, spectral_centroid: float, spectral_rolloff: float,
                                      graph_density: float, topological_complexity: float) -> float:
        """Calculate agility intelligence from fingerprint features (DMIT principle)"""
        # DMIT research shows: High spectral features + graph complexity = agility intelligence
        
        # Spectral centroid contribution
        centroid_score = min(1.0, spectral_centroid)
        
        # Spectral rolloff contribution
        rolloff_score = min(1.0, spectral_rolloff)
        
        # Graph density contribution
        density_score = min(1.0, graph_density)
        
        # Topological complexity contribution
        complexity_score = min(1.0, topological_complexity)
        
        # Combine scores
        agility_intelligence = (centroid_score * 0.3 + rolloff_score * 0.25 + density_score * 0.25 + complexity_score * 0.2)
        return min(1.0, agility_intelligence)
    
    @staticmethod
    def classify_agility_level(score: float) -> str:
        """Classify learning agility level based on score"""
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