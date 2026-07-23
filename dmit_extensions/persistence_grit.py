from typing import Dict, Any
from .base import DMITExtensionBase

class PersistenceGritExtension(DMITExtensionBase):
    """
    Extension for analyzing Persistence and Grit abilities from fingerprint features.
    Uses comprehensive DMIT scientific correlations between fingerprint patterns and persistence processes.
    """
    def analyze(self, features: Dict[str, Any]) -> Dict[str, Any]:
        # Extract comprehensive fingerprint features for persistence grit analysis
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
        
        # Calculate persistence grit abilities using comprehensive DMIT scientific correlations
        
        # 1. Goal Persistence Analysis (DMIT Principle: High ridge count + fractal complexity = goal persistence)
        goal_persistence = self._calculate_goal_persistence(tfrc, box_counting_dimension, 
                                                          h1_num_features, betti_1)
        
        # 2. Effort Consistency Analysis (DMIT Principle: High pattern regularity + low lacunarity = effort consistency)
        effort_consistency = self._calculate_effort_consistency(pattern_regularity, lacunarity, 
                                                              ridge_continuity, std_intensity)
        
        # 3. Resilience Analysis (DMIT Principle: High ridge density + clustering coefficient = resilience)
        resilience = self._calculate_resilience(ridge_density, clustering_coefficient, 
                                              modularity, ridge_thickness)
        
        # 4. Determination Analysis (DMIT Principle: High correlation dimension + graph density = determination)
        determination = self._calculate_determination(correlation_dimension, graph_density, 
                                                    betweenness_centrality, information_dimension)
        
        # 5. Endurance Analysis (DMIT Principle: High spectral radius + topological complexity = endurance)
        endurance = self._calculate_endurance(spectral_radius, topological_complexity, 
                                            euler_characteristic, spectral_bandwidth)
        
        # 6. Focus Persistence Analysis (DMIT Principle: High ridge uniformity + pattern type = focus persistence)
        focus_persistence = self._calculate_focus_persistence(ridge_uniformity, pattern_type, 
                                                            ridge_curvature, community_cohesion)
        
        # 7. Motivation Persistence Analysis (DMIT Principle: High information dimension + entropy = motivation persistence)
        motivation_persistence = self._calculate_motivation_persistence(information_dimension, entropy, 
                                                                      pattern_symmetry, spectral_entropy)
        
        # 8. Achievement Drive Analysis (DMIT Principle: High spectral features + graph complexity = achievement drive)
        achievement_drive = self._calculate_achievement_drive(spectral_centroid, spectral_rolloff, 
                                                            graph_density, topological_complexity)
        
        # Overall persistence grit score (comprehensive weighted combination)
        persistence_grit_score = (
            goal_persistence * 0.20 +             # Goal persistence is fundamental
            effort_consistency * 0.18 +           # Effort consistency is crucial
            resilience * 0.15 +                   # Resilience is important
            determination * 0.15 +                # Determination is essential
            endurance * 0.12 +                    # Endurance
            focus_persistence * 0.10 +            # Focus persistence
            motivation_persistence * 0.07 +       # Motivation persistence
            achievement_drive * 0.03              # Achievement drive
        )
        
        # Normalize to 0-1 range
        persistence_grit_score = max(0.0, min(1.0, persistence_grit_score))
        
        # Determine persistence grit style based on dominant features
        grit_styles = {
            'goal_oriented': (goal_persistence + achievement_drive) / 2,
            'consistent': (effort_consistency + focus_persistence) / 2,
            'resilient': (resilience + endurance) / 2,
            'determined': (determination + motivation_persistence) / 2,
            'enduring': (endurance + goal_persistence) / 2,
            'focused': (focus_persistence + effort_consistency) / 2
        }
        primary_style = max(grit_styles.items(), key=lambda x: x[1])[0]

        return {
            'persistence_grit_score': persistence_grit_score,
            'primary_grit_style': primary_style,
            'goal_persistence': goal_persistence,
            'effort_consistency': effort_consistency,
            'resilience': resilience,
            'determination': determination,
            'endurance': endurance,
            'focus_persistence': focus_persistence,
            'motivation_persistence': motivation_persistence,
            'achievement_drive': achievement_drive,
            'goal_achievement': (goal_persistence + achievement_drive) / 2,
            'work_consistency': (effort_consistency + focus_persistence) / 2,
            'stress_resistance': (resilience + endurance) / 2,
            'motivation_stability': (motivation_persistence + determination) / 2,
            'long_term_focus': (focus_persistence + goal_persistence) / 2,
            'grit_profile': self.classify_grit_level(persistence_grit_score)
        }

    def _calculate_goal_persistence(self, tfrc: int, box_counting_dimension: float,
                                  h1_num_features: int, betti_1: int) -> float:
        """Calculate goal persistence from fingerprint features (DMIT principle)"""
        # DMIT research shows: High ridge count + fractal complexity = goal persistence
        
        # Ridge count contribution
        ridge_score = min(1.0, float(tfrc or 0))  # FIX: per-finger TFRC 0-30, not 0-1500  # FIX: per-finger TFRC 0-30
        
        # Fractal dimension contribution
        if 1.5 <= box_counting_dimension <= 2.0:
            fractal_score = (box_counting_dimension - 1.5) / 0.5
        else:
            fractal_score = 0.5
        
        # H1 features contribution (loops/holes - complexity in persistence)
        h1_score = min(1.0, h1_num_features / 10.0)
        
        # Betti-1 contribution (persistence loops)
        betti_score = min(1.0, betti_1 / 10.0)
        
        # Combine scores
        goal_persistence = (ridge_score * 0.35 + fractal_score * 0.25 + h1_score * 0.25 + betti_score * 0.15)
        return min(1.0, goal_persistence)
    
    def _calculate_effort_consistency(self, pattern_regularity: float, lacunarity: float,
                                    ridge_continuity: float, std_intensity: float) -> float:
        """Calculate effort consistency from fingerprint features (DMIT principle)"""
        # DMIT research shows: High pattern regularity + low lacunarity = effort consistency
        
        # Pattern regularity contribution
        regularity_score = min(1.0, pattern_regularity)
        
        # Lacunarity contribution (lower lacunarity = more regular = better consistency)
        lacunarity_score = max(0.0, 1.0 - lacunarity)
        
        # Ridge continuity contribution
        continuity_score = min(1.0, ridge_continuity)
        
        # Standard deviation contribution (lower variation = more consistent = better effort consistency)
        if std_intensity > 0:
            std_score = max(0.0, 1.0 - (std_intensity / 100.0))
        else:
            std_score = 0.5
        
        # Combine scores
        effort_consistency = (regularity_score * 0.3 + lacunarity_score * 0.25 + continuity_score * 0.25 + std_score * 0.2)
        return min(1.0, effort_consistency)
    
    def _calculate_resilience(self, ridge_density: float, clustering_coefficient: float,
                            modularity: float, ridge_thickness: float) -> float:
        """Calculate resilience from fingerprint features (DMIT principle)"""
        # DMIT research shows: High ridge density + clustering coefficient = resilience
        
        # Ridge density contribution
        density_score = min(1.0, ridge_density)
        
        # Clustering coefficient contribution
        clustering_score = min(1.0, clustering_coefficient)
        
        # Modularity contribution
        modularity_score = min(1.0, modularity)
        
        # Ridge thickness contribution
        thickness_score = min(1.0, ridge_thickness)
        
        # Combine scores
        resilience = (density_score * 0.3 + clustering_score * 0.25 + modularity_score * 0.25 + thickness_score * 0.2)
        return min(1.0, resilience)
    
    def _calculate_determination(self, correlation_dimension: float, graph_density: float,
                               betweenness_centrality: float, information_dimension: float) -> float:
        """Calculate determination from fingerprint features (DMIT principle)"""
        # DMIT research shows: High correlation dimension + graph density = determination
        
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
        determination = (corr_score * 0.3 + density_score * 0.25 + centrality_score * 0.25 + info_score * 0.2)
        return min(1.0, determination)
    
    def _calculate_endurance(self, spectral_radius: float, topological_complexity: float,
                           euler_characteristic: int, spectral_bandwidth: float) -> float:
        """Calculate endurance from fingerprint features (DMIT principle)"""
        # DMIT research shows: High spectral radius + topological complexity = endurance
        
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
        endurance = (spectral_score * 0.3 + complexity_score * 0.25 + euler_score * 0.25 + bandwidth_score * 0.2)
        return min(1.0, endurance)
    
    def _calculate_focus_persistence(self, ridge_uniformity: float, pattern_type: str,
                                   ridge_curvature: float, community_cohesion: float) -> float:
        """Calculate focus persistence from fingerprint features (DMIT principle)"""
        # DMIT research shows: High ridge uniformity + pattern type = focus persistence
        
        # Ridge uniformity contribution
        uniformity_score = min(1.0, ridge_uniformity)
        
        # Pattern type contribution
        pattern_weights = {
            'whorl': 0.8,      # Complex patterns indicate strong focus persistence
            'loop': 0.7,       # Good focus persistence
            'arch': 0.6,       # Moderate focus persistence
            'tented_arch': 0.65, # Slightly better than plain arch
            'composite': 0.75   # Complex focus persistence patterns
        }
        pattern_score = pattern_weights.get(pattern_type.lower(), 0.6)
        
        # Ridge curvature contribution
        curvature_score = min(1.0, ridge_curvature)
        
        # Community cohesion contribution
        cohesion_score = min(1.0, community_cohesion)
        
        # Combine scores
        focus_persistence = (uniformity_score * 0.3 + pattern_score * 0.25 + curvature_score * 0.25 + cohesion_score * 0.2)
        return min(1.0, focus_persistence)
    
    def _calculate_motivation_persistence(self, information_dimension: float, entropy: float,
                                        pattern_symmetry: float, spectral_entropy: float) -> float:
        """Calculate motivation persistence from fingerprint features (DMIT principle)"""
        # DMIT research shows: High information dimension + entropy = motivation persistence
        
        # Information dimension contribution
        if 1.5 <= information_dimension <= 2.0:
            info_score = (information_dimension - 1.5) / 0.5
        else:
            info_score = 0.5
        
        # Entropy contribution (higher entropy = more complex motivation persistence)
        if entropy > 0:
            entropy_score = min(1.0, entropy / 8.0)  # Normalize to 0-1
        else:
            entropy_score = 0.5
        
        # Pattern symmetry contribution
        symmetry_score = min(1.0, pattern_symmetry)
        
        # Spectral entropy contribution
        spectral_score = min(1.0, spectral_entropy)
        
        # Combine scores
        motivation_persistence = (info_score * 0.35 + entropy_score * 0.25 + symmetry_score * 0.25 + spectral_score * 0.15)
        return min(1.0, motivation_persistence)
    
    def _calculate_achievement_drive(self, spectral_centroid: float, spectral_rolloff: float,
                                   graph_density: float, topological_complexity: float) -> float:
        """Calculate achievement drive from fingerprint features (DMIT principle)"""
        # DMIT research shows: High spectral features + graph complexity = achievement drive
        
        # Spectral centroid contribution
        centroid_score = min(1.0, spectral_centroid)
        
        # Spectral rolloff contribution
        rolloff_score = min(1.0, spectral_rolloff)
        
        # Graph density contribution
        density_score = min(1.0, graph_density)
        
        # Topological complexity contribution
        complexity_score = min(1.0, topological_complexity)
        
        # Combine scores
        achievement_drive = (centroid_score * 0.3 + rolloff_score * 0.25 + density_score * 0.25 + complexity_score * 0.2)
        return min(1.0, achievement_drive)

    @staticmethod
    def classify_grit_level(score: float) -> str:
        """Classify persistence grit level based on score"""
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