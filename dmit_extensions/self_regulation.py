from typing import Dict, Any
from .base import DMITExtensionBase

class SelfRegulationExtension(DMITExtensionBase):
    """
    Extension for analyzing Self Regulation abilities from fingerprint features.
    Uses comprehensive DMIT scientific correlations between fingerprint patterns and self-regulation processes.
    """
    def analyze(self, features: Dict[str, Any]) -> Dict[str, Any]:
        # Extract comprehensive fingerprint features for self regulation analysis
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
        
        # Calculate self regulation abilities using comprehensive DMIT scientific correlations
        
        # 1. Emotional Control Analysis (DMIT Principle: High pattern regularity + low lacunarity = emotional control)
        emotional_control = self._calculate_emotional_control(pattern_regularity, lacunarity, 
                                                            ridge_continuity, std_intensity)
        
        # 2. Impulse Management Analysis (DMIT Principle: High correlation dimension + graph density = impulse control)
        impulse_management = self._calculate_impulse_management(correlation_dimension, graph_density, 
                                                              betweenness_centrality, information_dimension)
        
        # 3. Self-Discipline Analysis (DMIT Principle: High ridge uniformity + pattern type = self-discipline)
        self_discipline = self._calculate_self_discipline(ridge_uniformity, pattern_type, 
                                                        ridge_curvature, community_cohesion)
        
        # 4. Behavioral Regulation Analysis (DMIT Principle: High ridge density + clustering coefficient = behavioral control)
        behavioral_regulation = self._calculate_behavioral_regulation(ridge_density, clustering_coefficient, 
                                                                    modularity, ridge_thickness)
        
        # 5. Attention Control Analysis (DMIT Principle: High spectral radius + topological complexity = attention control)
        attention_control = self._calculate_attention_control(spectral_radius, topological_complexity, 
                                                            euler_characteristic, spectral_bandwidth)
        
        # 6. Goal Persistence Analysis (DMIT Principle: High ridge count + fractal complexity = goal persistence)
        goal_persistence = self._calculate_goal_persistence(tfrc, box_counting_dimension, 
                                                          h1_num_features, betti_1)
        
        # 7. Self-Monitoring Analysis (DMIT Principle: High information dimension + entropy = self-monitoring)
        self_monitoring = self._calculate_self_monitoring(information_dimension, entropy, 
                                                        pattern_symmetry, spectral_entropy)
        
        # 8. Adaptive Control Analysis (DMIT Principle: High spectral features + graph complexity = adaptive control)
        adaptive_control = self._calculate_adaptive_control(spectral_centroid, spectral_rolloff, 
                                                          graph_density, topological_complexity)
        
        # Overall self regulation score (comprehensive weighted combination)
        self_regulation_score = (
            emotional_control * 0.20 +            # Emotional control is fundamental
            impulse_management * 0.18 +           # Impulse management is crucial
            self_discipline * 0.15 +              # Self-discipline is important
            behavioral_regulation * 0.15 +        # Behavioral regulation is essential
            attention_control * 0.12 +            # Attention control
            goal_persistence * 0.10 +             # Goal persistence
            self_monitoring * 0.07 +              # Self-monitoring
            adaptive_control * 0.03               # Adaptive control
        )
        
        # Normalize to 0-1 range
        self_regulation_score = max(0.0, min(1.0, self_regulation_score))
        
        # Determine self regulation style based on dominant features
        regulation_styles = {
            'emotional': emotional_control + self_monitoring,
            'impulsive': impulse_management + attention_control,
            'disciplined': self_discipline + goal_persistence,
            'behavioral': behavioral_regulation + adaptive_control,
            'attentive': attention_control + emotional_control,
            'persistent': goal_persistence + self_discipline
        }
        primary_style = max(regulation_styles.items(), key=lambda x: x[1])[0]
        
        return {
            'self_regulation_score': self_regulation_score,
            'primary_regulation_style': primary_style,
            'emotional_control': emotional_control,
            'impulse_management': impulse_management,
            'self_discipline': self_discipline,
            'behavioral_regulation': behavioral_regulation,
            'attention_control': attention_control,
            'goal_persistence': goal_persistence,
            'self_monitoring': self_monitoring,
            'adaptive_control': adaptive_control,
            'emotional_stability': emotional_control + self_monitoring,
            'behavioral_consistency': behavioral_regulation + self_discipline,
            'cognitive_control': attention_control + impulse_management,
            'goal_orientation': goal_persistence + adaptive_control,
            'self_awareness': self_monitoring + emotional_control,
            'regulation_profile': self.classify_regulation_level(self_regulation_score)
        }

    def _calculate_emotional_control(self, pattern_regularity: float, lacunarity: float,
                                   ridge_continuity: float, std_intensity: float) -> float:
        """Calculate emotional control from fingerprint features (DMIT principle)"""
        # DMIT research shows: High pattern regularity + low lacunarity = emotional control
        
        # Pattern regularity contribution
        regularity_score = min(1.0, pattern_regularity)
        
        # Lacunarity contribution (lower lacunarity = more regular = better emotional control)
        lacunarity_score = max(0.0, 1.0 - lacunarity)
        
        # Ridge continuity contribution
        continuity_score = min(1.0, ridge_continuity)
        
        # Standard deviation contribution (lower variation = more consistent = better emotional control)
        if std_intensity > 0:
            std_score = max(0.0, 1.0 - (std_intensity / 100.0))
        else:
            std_score = 0.5
        
        # Combine scores
        emotional_control = (regularity_score * 0.3 + lacunarity_score * 0.25 + continuity_score * 0.25 + std_score * 0.2)
        return min(1.0, emotional_control)
    
    def _calculate_impulse_management(self, correlation_dimension: float, graph_density: float,
                                    betweenness_centrality: float, information_dimension: float) -> float:
        """Calculate impulse management from fingerprint features (DMIT principle)"""
        # DMIT research shows: High correlation dimension + graph density = impulse control
        
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
        impulse_management = (corr_score * 0.3 + density_score * 0.25 + centrality_score * 0.25 + info_score * 0.2)
        return min(1.0, impulse_management)
    
    def _calculate_self_discipline(self, ridge_uniformity: float, pattern_type: str,
                                 ridge_curvature: float, community_cohesion: float) -> float:
        """Calculate self-discipline from fingerprint features (DMIT principle)"""
        # DMIT research shows: High ridge uniformity + pattern type = self-discipline
        
        # Ridge uniformity contribution
        uniformity_score = min(1.0, ridge_uniformity)
        
        # Pattern type contribution
        pattern_weights = {
            'whorl': 0.8,      # Complex patterns indicate strong discipline
            'loop': 0.7,       # Good discipline
            'arch': 0.6,       # Moderate discipline
            'tented_arch': 0.65, # Slightly better than plain arch
            'composite': 0.75   # Complex discipline patterns
        }
        pattern_score = pattern_weights.get(pattern_type.lower(), 0.6)
        
        # Ridge curvature contribution
        curvature_score = min(1.0, ridge_curvature)
        
        # Community cohesion contribution
        cohesion_score = min(1.0, community_cohesion)
        
        # Combine scores
        self_discipline = (uniformity_score * 0.3 + pattern_score * 0.25 + curvature_score * 0.25 + cohesion_score * 0.2)
        return min(1.0, self_discipline)
    
    def _calculate_behavioral_regulation(self, ridge_density: float, clustering_coefficient: float,
                                       modularity: float, ridge_thickness: float) -> float:
        """Calculate behavioral regulation from fingerprint features (DMIT principle)"""
        # DMIT research shows: High ridge density + clustering coefficient = behavioral control
        
        # Ridge density contribution
        density_score = min(1.0, ridge_density)
        
        # Clustering coefficient contribution
        clustering_score = min(1.0, clustering_coefficient)
        
        # Modularity contribution
        modularity_score = min(1.0, modularity)
        
        # Ridge thickness contribution
        thickness_score = min(1.0, ridge_thickness)
        
        # Combine scores
        behavioral_regulation = (density_score * 0.3 + clustering_score * 0.25 + modularity_score * 0.25 + thickness_score * 0.2)
        return min(1.0, behavioral_regulation)
    
    def _calculate_attention_control(self, spectral_radius: float, topological_complexity: float,
                                   euler_characteristic: int, spectral_bandwidth: float) -> float:
        """Calculate attention control from fingerprint features (DMIT principle)"""
        # DMIT research shows: High spectral radius + topological complexity = attention control
        
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
        attention_control = (spectral_score * 0.3 + complexity_score * 0.25 + euler_score * 0.25 + bandwidth_score * 0.2)
        return min(1.0, attention_control)
    
    def _calculate_goal_persistence(self, tfrc: int, box_counting_dimension: float,
                                  h1_num_features: int, betti_1: int) -> float:
        """Calculate goal persistence from fingerprint features (DMIT principle)"""
        # DMIT research shows: High ridge count + fractal complexity = goal persistence
        
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
        
        # H1 features contribution (loops/holes - complexity in persistence)
        h1_score = min(1.0, h1_num_features / 10.0)
        
        # Betti-1 contribution (persistence loops)
        betti_score = min(1.0, betti_1 / 10.0)
        
        # Combine scores
        goal_persistence = (ridge_score * 0.35 + fractal_score * 0.25 + h1_score * 0.25 + betti_score * 0.15)
        return min(1.0, goal_persistence)
    
    def _calculate_self_monitoring(self, information_dimension: float, entropy: float,
                                 pattern_symmetry: float, spectral_entropy: float) -> float:
        """Calculate self-monitoring from fingerprint features (DMIT principle)"""
        # DMIT research shows: High information dimension + entropy = self-monitoring
        
        # Information dimension contribution
        if 1.5 <= information_dimension <= 2.0:
            info_score = (information_dimension - 1.5) / 0.5
        else:
            info_score = 0.5
        
        # Entropy contribution (higher entropy = more complex self-monitoring)
        if entropy > 0:
            entropy_score = min(1.0, entropy / 8.0)  # Normalize to 0-1
        else:
            entropy_score = 0.5
        
        # Pattern symmetry contribution
        symmetry_score = min(1.0, pattern_symmetry)
        
        # Spectral entropy contribution
        spectral_score = min(1.0, spectral_entropy)
        
        # Combine scores
        self_monitoring = (info_score * 0.35 + entropy_score * 0.25 + symmetry_score * 0.25 + spectral_score * 0.15)
        return min(1.0, self_monitoring)
    
    def _calculate_adaptive_control(self, spectral_centroid: float, spectral_rolloff: float,
                                  graph_density: float, topological_complexity: float) -> float:
        """Calculate adaptive control from fingerprint features (DMIT principle)"""
        # DMIT research shows: High spectral features + graph complexity = adaptive control
        
        # Spectral centroid contribution
        centroid_score = min(1.0, spectral_centroid)
        
        # Spectral rolloff contribution
        rolloff_score = min(1.0, spectral_rolloff)
        
        # Graph density contribution
        density_score = min(1.0, graph_density)
        
        # Topological complexity contribution
        complexity_score = min(1.0, topological_complexity)
        
        # Combine scores
        adaptive_control = (centroid_score * 0.3 + rolloff_score * 0.25 + density_score * 0.25 + complexity_score * 0.2)
        return min(1.0, adaptive_control)
    
    @staticmethod
    def classify_regulation_level(score: float) -> str:
        """Classify self regulation level based on score"""
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