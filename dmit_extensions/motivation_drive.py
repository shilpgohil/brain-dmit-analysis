from typing import Dict, Any
from .base import DMITExtensionBase

class MotivationDriveExtension(DMITExtensionBase):
    """
    Extension for analyzing Motivation & Drive abilities from fingerprint features.
    Uses comprehensive DMIT scientific correlations between fingerprint patterns and motivation processes.
    """
    def analyze(self, features: Dict[str, Any]) -> Dict[str, Any]:
        # Extract comprehensive fingerprint features for motivation drive analysis
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
        
        # Calculate motivation drive abilities using comprehensive DMIT scientific correlations
        
        # 1. Intrinsic Motivation Analysis (DMIT Principle: High information dimension + entropy = intrinsic motivation)
        intrinsic_motivation = self._calculate_intrinsic_motivation(information_dimension, entropy, 
                                                                  pattern_symmetry, spectral_entropy)
        
        # 2. Extrinsic Motivation Analysis (DMIT Principle: High correlation dimension + graph density = extrinsic motivation)
        extrinsic_motivation = self._calculate_extrinsic_motivation(correlation_dimension, graph_density, 
                                                                  betweenness_centrality, information_dimension)
        
        # 3. Achievement Drive Analysis (DMIT Principle: High ridge count + fractal complexity = achievement drive)
        achievement_drive = self._calculate_achievement_drive(tfrc, box_counting_dimension, 
                                                            h1_num_features, betti_1)
        
        # 4. Goal Orientation Analysis (DMIT Principle: High spectral radius + topological complexity = goal orientation)
        goal_orientation = self._calculate_goal_orientation(spectral_radius, topological_complexity, 
                                                          euler_characteristic, spectral_bandwidth)
        
        # 5. Persistence Drive Analysis (DMIT Principle: High ridge density + clustering coefficient = persistence drive)
        persistence_drive = self._calculate_persistence_drive(ridge_density, clustering_coefficient, 
                                                            modularity, ridge_thickness)
        
        # 6. Passion Intensity Analysis (DMIT Principle: High ridge uniformity + pattern type = passion intensity)
        passion_intensity = self._calculate_passion_intensity(ridge_uniformity, pattern_type, 
                                                            ridge_curvature, community_cohesion)
        
        # 7. Motivation Optimization Analysis (DMIT Principle: High pattern regularity + low lacunarity = motivation optimization)
        motivation_optimization = self._calculate_motivation_optimization(pattern_regularity, lacunarity, 
                                                                        ridge_continuity, std_intensity)
        
        # 8. Motivation Intelligence Analysis (DMIT Principle: High spectral features + graph complexity = motivation intelligence)
        motivation_intelligence = self._calculate_motivation_intelligence(spectral_centroid, spectral_rolloff, 
                                                                        graph_density, topological_complexity)
        
        # Overall motivation drive score (comprehensive weighted combination)
        motivation_drive_score = (
            intrinsic_motivation * 0.20 +          # Intrinsic motivation is fundamental
            extrinsic_motivation * 0.18 +          # Extrinsic motivation is crucial
            achievement_drive * 0.15 +             # Achievement drive is important
            goal_orientation * 0.15 +              # Goal orientation is essential
            persistence_drive * 0.12 +             # Persistence drive
            passion_intensity * 0.10 +             # Passion intensity
            motivation_optimization * 0.07 +       # Motivation optimization
            motivation_intelligence * 0.03         # Motivation intelligence
        )
        
        # Normalize to 0-1 range
        motivation_drive_score = max(0.0, min(1.0, motivation_drive_score))
        
        # Determine motivation drive style based on dominant features
        motivation_styles = {
            'intrinsic': intrinsic_motivation + motivation_intelligence,
            'extrinsic': extrinsic_motivation + goal_orientation,
            'achievement': achievement_drive + persistence_drive,
            'goal_oriented': goal_orientation + passion_intensity,
            'persistent': persistence_drive + motivation_optimization,
            'passionate': passion_intensity + intrinsic_motivation
        }
        primary_style = max(motivation_styles.items(), key=lambda x: x[1])[0]
        
        return {
            'motivation_drive_score': motivation_drive_score,
            'primary_motivation_style': primary_style,
            'intrinsic_motivation': intrinsic_motivation,
            'extrinsic_motivation': extrinsic_motivation,
            'achievement_drive': achievement_drive,
            'goal_orientation': goal_orientation,
            'persistence_drive': persistence_drive,
            'passion_intensity': passion_intensity,
            'motivation_optimization': motivation_optimization,
            'motivation_intelligence': motivation_intelligence,
            'internal_drive': intrinsic_motivation + achievement_drive,
            'external_focus': extrinsic_motivation + goal_orientation,
            'persistent_achievement': persistence_drive + passion_intensity,
            'intelligent_motivation': motivation_intelligence + intrinsic_motivation,
            'optimized_drive': motivation_optimization + persistence_drive,
            'motivation_profile': self.classify_motivation_level(motivation_drive_score)
        }

    def _calculate_intrinsic_motivation(self, information_dimension: float, entropy: float,
                                      pattern_symmetry: float, spectral_entropy: float) -> float:
        """Calculate intrinsic motivation from fingerprint features (DMIT principle)"""
        # DMIT research shows: High information dimension + entropy = intrinsic motivation
        
        # Information dimension contribution
        if 1.5 <= information_dimension <= 2.0:
            info_score = (information_dimension - 1.5) / 0.5
        else:
            info_score = 0.5
        
        # Entropy contribution (higher entropy = more complex intrinsic motivation)
        if entropy > 0:
            entropy_score = min(1.0, entropy / 8.0)  # Normalize to 0-1
        else:
            entropy_score = 0.5
        
        # Pattern symmetry contribution
        symmetry_score = min(1.0, pattern_symmetry)
        
        # Spectral entropy contribution
        spectral_score = min(1.0, spectral_entropy)
        
        # Combine scores
        intrinsic_motivation = (info_score * 0.35 + entropy_score * 0.25 + symmetry_score * 0.25 + spectral_score * 0.15)
        return min(1.0, intrinsic_motivation)
    
    def _calculate_extrinsic_motivation(self, correlation_dimension: float, graph_density: float,
                                      betweenness_centrality: float, information_dimension: float) -> float:
        """Calculate extrinsic motivation from fingerprint features (DMIT principle)"""
        # DMIT research shows: High correlation dimension + graph density = extrinsic motivation
        
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
        extrinsic_motivation = (corr_score * 0.3 + density_score * 0.25 + centrality_score * 0.25 + info_score * 0.2)
        return min(1.0, extrinsic_motivation)
    
    def _calculate_achievement_drive(self, tfrc: int, box_counting_dimension: float,
                                   h1_num_features: int, betti_1: int) -> float:
        """Calculate achievement drive from fingerprint features (DMIT principle)"""
        # DMIT research shows: High ridge count + fractal complexity = achievement drive
        
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
        
        # H1 features contribution (loops/holes - complexity in achievement drive)
        h1_score = min(1.0, h1_num_features / 10.0)
        
        # Betti-1 contribution (achievement drive loops)
        betti_score = min(1.0, betti_1 / 10.0)
        
        # Combine scores
        achievement_drive = (ridge_score * 0.35 + fractal_score * 0.25 + h1_score * 0.25 + betti_score * 0.15)
        return min(1.0, achievement_drive)
    
    def _calculate_goal_orientation(self, spectral_radius: float, topological_complexity: float,
                                  euler_characteristic: int, spectral_bandwidth: float) -> float:
        """Calculate goal orientation from fingerprint features (DMIT principle)"""
        # DMIT research shows: High spectral radius + topological complexity = goal orientation
        
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
        goal_orientation = (spectral_score * 0.3 + complexity_score * 0.25 + euler_score * 0.25 + bandwidth_score * 0.2)
        return min(1.0, goal_orientation)
    
    def _calculate_persistence_drive(self, ridge_density: float, clustering_coefficient: float,
                                   modularity: float, ridge_thickness: float) -> float:
        """Calculate persistence drive from fingerprint features (DMIT principle)"""
        # DMIT research shows: High ridge density + clustering coefficient = persistence drive
        
        # Ridge density contribution
        density_score = min(1.0, ridge_density)
        
        # Clustering coefficient contribution
        clustering_score = min(1.0, clustering_coefficient)
        
        # Modularity contribution
        modularity_score = min(1.0, modularity)
        
        # Ridge thickness contribution
        thickness_score = min(1.0, ridge_thickness)
        
        # Combine scores
        persistence_drive = (density_score * 0.3 + clustering_score * 0.25 + modularity_score * 0.25 + thickness_score * 0.2)
        return min(1.0, persistence_drive)
    
    def _calculate_passion_intensity(self, ridge_uniformity: float, pattern_type: str,
                                   ridge_curvature: float, community_cohesion: float) -> float:
        """Calculate passion intensity from fingerprint features (DMIT principle)"""
        # DMIT research shows: High ridge uniformity + pattern type = passion intensity
        
        # Ridge uniformity contribution
        uniformity_score = min(1.0, ridge_uniformity)
        
        # Pattern type contribution
        pattern_weights = {
            'whorl': 0.8,      # Complex patterns indicate high passion intensity
            'loop': 0.7,       # Good passion intensity
            'arch': 0.6,       # Moderate passion intensity
            'tented_arch': 0.65, # Slightly better than plain arch
            'composite': 0.75   # Complex passion intensity patterns
        }
        pattern_score = pattern_weights.get(pattern_type.lower(), 0.6)
        
        # Ridge curvature contribution
        curvature_score = min(1.0, ridge_curvature)
        
        # Community cohesion contribution
        cohesion_score = min(1.0, community_cohesion)
        
        # Combine scores
        passion_intensity = (uniformity_score * 0.3 + pattern_score * 0.25 + curvature_score * 0.25 + cohesion_score * 0.2)
        return min(1.0, passion_intensity)
    
    def _calculate_motivation_optimization(self, pattern_regularity: float, lacunarity: float,
                                         ridge_continuity: float, std_intensity: float) -> float:
        """Calculate motivation optimization from fingerprint features (DMIT principle)"""
        # DMIT research shows: High pattern regularity + low lacunarity = motivation optimization
        
        # Pattern regularity contribution
        regularity_score = min(1.0, pattern_regularity)
        
        # Lacunarity contribution (lower lacunarity = more regular = better motivation optimization)
        lacunarity_score = max(0.0, 1.0 - lacunarity)
        
        # Ridge continuity contribution
        continuity_score = min(1.0, ridge_continuity)
        
        # Standard deviation contribution (lower variation = more consistent = better motivation optimization)
        if std_intensity > 0:
            std_score = max(0.0, 1.0 - (std_intensity / 100.0))
        else:
            std_score = 0.5
        
        # Combine scores
        motivation_optimization = (regularity_score * 0.3 + lacunarity_score * 0.25 + continuity_score * 0.25 + std_score * 0.2)
        return min(1.0, motivation_optimization)
    
    def _calculate_motivation_intelligence(self, spectral_centroid: float, spectral_rolloff: float,
                                         graph_density: float, topological_complexity: float) -> float:
        """Calculate motivation intelligence from fingerprint features (DMIT principle)"""
        # DMIT research shows: High spectral features + graph complexity = motivation intelligence
        
        # Spectral centroid contribution
        centroid_score = min(1.0, spectral_centroid)
        
        # Spectral rolloff contribution
        rolloff_score = min(1.0, spectral_rolloff)
        
        # Graph density contribution
        density_score = min(1.0, graph_density)
        
        # Topological complexity contribution
        complexity_score = min(1.0, topological_complexity)
        
        # Combine scores
        motivation_intelligence = (centroid_score * 0.3 + rolloff_score * 0.25 + density_score * 0.25 + complexity_score * 0.2)
        return min(1.0, motivation_intelligence)
    
    @staticmethod
    def classify_motivation_level(score: float) -> str:
        """Classify motivation drive level based on score"""
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