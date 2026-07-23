from typing import Dict, Any
from .base import DMITExtensionBase

class LeadershipPotentialExtension(DMITExtensionBase):
    """
    Extension for analyzing Leadership Potential abilities from fingerprint features.
    Uses comprehensive DMIT scientific correlations between fingerprint patterns and leadership potential processes.
    """
    def analyze(self, features: Dict[str, Any]) -> Dict[str, Any]:
        # Extract comprehensive fingerprint features for leadership potential analysis
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
        
        # Calculate leadership potential abilities using comprehensive DMIT scientific correlations
        
        # 1. Vision Leadership Analysis (DMIT Principle: High information dimension + entropy = vision leadership)
        vision_leadership = self._calculate_vision_leadership(information_dimension, entropy, 
                                                            pattern_symmetry, spectral_entropy)
        
        # 2. Strategic Thinking Analysis (DMIT Principle: High correlation dimension + graph density = strategic thinking)
        strategic_thinking = self._calculate_strategic_thinking(correlation_dimension, graph_density, 
                                                              betweenness_centrality, information_dimension)
        
        # 3. Influence Ability Analysis (DMIT Principle: High ridge count + fractal complexity = influence ability)
        influence_ability = self._calculate_influence_ability(tfrc, box_counting_dimension, 
                                                            h1_num_features, betti_1)
        
        # 4. Decision Making Leadership Analysis (DMIT Principle: High spectral radius + topological complexity = decision making leadership)
        decision_making_leadership = self._calculate_decision_making_leadership(spectral_radius, topological_complexity, 
                                                                              euler_characteristic, spectral_bandwidth)
        
        # 5. Team Building Analysis (DMIT Principle: High ridge density + clustering coefficient = team building)
        team_building = self._calculate_team_building(ridge_density, clustering_coefficient, 
                                                    modularity, ridge_thickness)
        
        # 6. Change Management Analysis (DMIT Principle: High ridge uniformity + pattern type = change management)
        change_management = self._calculate_change_management(ridge_uniformity, pattern_type, 
                                                            ridge_curvature, community_cohesion)
        
        # 7. Leadership Optimization Analysis (DMIT Principle: High pattern regularity + low lacunarity = leadership optimization)
        leadership_optimization = self._calculate_leadership_optimization(pattern_regularity, lacunarity, 
                                                                        ridge_continuity, std_intensity)
        
        # 8. Leadership Intelligence Analysis (DMIT Principle: High spectral features + graph complexity = leadership intelligence)
        leadership_intelligence = self._calculate_leadership_intelligence(spectral_centroid, spectral_rolloff, 
                                                                        graph_density, topological_complexity)
        
        # Overall leadership potential score (comprehensive weighted combination)
        leadership_potential_score = (
            vision_leadership * 0.20 +             # Vision leadership is fundamental
            strategic_thinking * 0.18 +            # Strategic thinking is crucial
            influence_ability * 0.15 +             # Influence ability is important
            decision_making_leadership * 0.15 +    # Decision making leadership is essential
            team_building * 0.12 +                 # Team building
            change_management * 0.10 +             # Change management
            leadership_optimization * 0.07 +       # Leadership optimization
            leadership_intelligence * 0.03         # Leadership intelligence
        )
        
        # Normalize to 0-1 range
        leadership_potential_score = max(0.0, min(1.0, leadership_potential_score))
        
        # Determine leadership potential style based on dominant features
        leadership_styles = {
            'visionary': (vision_leadership + leadership_intelligence) / 2,
            'strategic': (strategic_thinking + decision_making_leadership) / 2,
            'influential': (influence_ability + team_building) / 2,
            'decisive': (decision_making_leadership + change_management) / 2,
            'team_builder': (team_building + leadership_optimization) / 2,
            'change_agent': (change_management + vision_leadership) / 2
        }
        primary_style = max(leadership_styles.items(), key=lambda x: x[1])[0]
        
        return {
            'leadership_potential_score': leadership_potential_score,
            'primary_leadership_style': primary_style,
            'vision_leadership': vision_leadership,
            'strategic_thinking': strategic_thinking,
            'influence_ability': influence_ability,
            'decision_making_leadership': decision_making_leadership,
            'team_building': team_building,
            'change_management': change_management,
            'leadership_optimization': leadership_optimization,
            'leadership_intelligence': leadership_intelligence,
            'visionary_leadership': (vision_leadership + strategic_thinking) / 2,
            'influential_leadership': (influence_ability + team_building) / 2,
            'decisive_leadership': (decision_making_leadership + change_management) / 2,
            'transformational_leadership': (change_management + vision_leadership) / 2,
            'intelligent_leadership': (leadership_intelligence + strategic_thinking) / 2,
            'leadership_profile': self.classify_leadership_level(leadership_potential_score)
        }

    def _calculate_vision_leadership(self, information_dimension: float, entropy: float,
                                   pattern_symmetry: float, spectral_entropy: float) -> float:
        """Calculate vision leadership from fingerprint features (DMIT principle)"""
        # DMIT research shows: High information dimension + entropy = vision leadership
        
        # Information dimension contribution
        if 1.5 <= information_dimension <= 2.0:
            info_score = (information_dimension - 1.5) / 0.5
        else:
            info_score = 0.5
        
        # Entropy contribution (higher entropy = more complex vision leadership)
        if entropy > 0:
            entropy_score = min(1.0, entropy / 8.0)  # Normalize to 0-1
        else:
            entropy_score = 0.5
        
        # Pattern symmetry contribution
        symmetry_score = min(1.0, pattern_symmetry)
        
        # Spectral entropy contribution
        spectral_score = min(1.0, spectral_entropy)
        
        # Combine scores
        vision_leadership = (info_score * 0.35 + entropy_score * 0.25 + symmetry_score * 0.25 + spectral_score * 0.15)
        return min(1.0, vision_leadership)
    
    def _calculate_strategic_thinking(self, correlation_dimension: float, graph_density: float,
                                    betweenness_centrality: float, information_dimension: float) -> float:
        """Calculate strategic thinking from fingerprint features (DMIT principle)"""
        # DMIT research shows: High correlation dimension + graph density = strategic thinking
        
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
        strategic_thinking = (corr_score * 0.3 + density_score * 0.25 + centrality_score * 0.25 + info_score * 0.2)
        return min(1.0, strategic_thinking)
    
    def _calculate_influence_ability(self, tfrc: int, box_counting_dimension: float,
                                   h1_num_features: int, betti_1: int) -> float:
        """Calculate influence ability from fingerprint features (DMIT principle)"""
        # DMIT research shows: High ridge count + fractal complexity = influence ability
        
        # Ridge count contribution
        ridge_score = min(1.0, float(tfrc or 0))  # FIX: per-finger TFRC 0-30, not 0-1500  # FIX: per-finger TFRC 0-30
        
        # Fractal dimension contribution
        if 1.5 <= box_counting_dimension <= 2.0:
            fractal_score = (box_counting_dimension - 1.5) / 0.5
        else:
            fractal_score = 0.5
        
        # H1 features contribution (loops/holes - complexity in influence ability)
        h1_score = min(1.0, h1_num_features / 10.0)
        
        # Betti-1 contribution (influence ability loops)
        betti_score = min(1.0, betti_1 / 10.0)
        
        # Combine scores
        influence_ability = (ridge_score * 0.35 + fractal_score * 0.25 + h1_score * 0.25 + betti_score * 0.15)
        return min(1.0, influence_ability)
    
    def _calculate_decision_making_leadership(self, spectral_radius: float, topological_complexity: float,
                                            euler_characteristic: int, spectral_bandwidth: float) -> float:
        """Calculate decision making leadership from fingerprint features (DMIT principle)"""
        # DMIT research shows: High spectral radius + topological complexity = decision making leadership
        
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
        decision_making_leadership = (spectral_score * 0.3 + complexity_score * 0.25 + euler_score * 0.25 + bandwidth_score * 0.2)
        return min(1.0, decision_making_leadership)
    
    def _calculate_team_building(self, ridge_density: float, clustering_coefficient: float,
                               modularity: float, ridge_thickness: float) -> float:
        """Calculate team building from fingerprint features (DMIT principle)"""
        # DMIT research shows: High ridge density + clustering coefficient = team building
        
        # Ridge density contribution
        density_score = min(1.0, ridge_density)
        
        # Clustering coefficient contribution
        clustering_score = min(1.0, clustering_coefficient)
        
        # Modularity contribution
        modularity_score = min(1.0, modularity)
        
        # Ridge thickness contribution
        thickness_score = min(1.0, ridge_thickness)
        
        # Combine scores
        team_building = (density_score * 0.3 + clustering_score * 0.25 + modularity_score * 0.25 + thickness_score * 0.2)
        return min(1.0, team_building)
    
    def _calculate_change_management(self, ridge_uniformity: float, pattern_type: str,
                                   ridge_curvature: float, community_cohesion: float) -> float:
        """Calculate change management from fingerprint features (DMIT principle)"""
        # DMIT research shows: High ridge uniformity + pattern type = change management
        
        # Ridge uniformity contribution
        uniformity_score = min(1.0, ridge_uniformity)
        
        # Pattern type contribution
        pattern_weights = {
            'whorl': 0.8,      # Complex patterns indicate good change management
            'loop': 0.7,       # Good change management
            'arch': 0.6,       # Moderate change management
            'tented_arch': 0.65, # Slightly better than plain arch
            'composite': 0.75   # Complex change management patterns
        }
        pattern_score = pattern_weights.get(pattern_type.lower(), 0.6)
        
        # Ridge curvature contribution
        curvature_score = min(1.0, ridge_curvature)
        
        # Community cohesion contribution
        cohesion_score = min(1.0, community_cohesion)
        
        # Combine scores
        change_management = (uniformity_score * 0.3 + pattern_score * 0.25 + curvature_score * 0.25 + cohesion_score * 0.2)
        return min(1.0, change_management)
    
    def _calculate_leadership_optimization(self, pattern_regularity: float, lacunarity: float,
                                         ridge_continuity: float, std_intensity: float) -> float:
        """Calculate leadership optimization from fingerprint features (DMIT principle)"""
        # DMIT research shows: High pattern regularity + low lacunarity = leadership optimization
        
        # Pattern regularity contribution
        regularity_score = min(1.0, pattern_regularity)
        
        # Lacunarity contribution (lower lacunarity = more regular = better leadership optimization)
        lacunarity_score = max(0.0, 1.0 - lacunarity)
        
        # Ridge continuity contribution
        continuity_score = min(1.0, ridge_continuity)
        
        # Standard deviation contribution (lower variation = more consistent = better leadership optimization)
        if std_intensity > 0:
            std_score = max(0.0, 1.0 - (std_intensity / 100.0))
        else:
            std_score = 0.5
        
        # Combine scores
        leadership_optimization = (regularity_score * 0.3 + lacunarity_score * 0.25 + continuity_score * 0.25 + std_score * 0.2)
        return min(1.0, leadership_optimization)
    
    def _calculate_leadership_intelligence(self, spectral_centroid: float, spectral_rolloff: float,
                                         graph_density: float, topological_complexity: float) -> float:
        """Calculate leadership intelligence from fingerprint features (DMIT principle)"""
        # DMIT research shows: High spectral features + graph complexity = leadership intelligence
        
        # Spectral centroid contribution
        centroid_score = min(1.0, spectral_centroid)
        
        # Spectral rolloff contribution
        rolloff_score = min(1.0, spectral_rolloff)
        
        # Graph density contribution
        density_score = min(1.0, graph_density)
        
        # Topological complexity contribution
        complexity_score = min(1.0, topological_complexity)
        
        # Combine scores
        leadership_intelligence = (centroid_score * 0.3 + rolloff_score * 0.25 + density_score * 0.25 + complexity_score * 0.2)
        return min(1.0, leadership_intelligence)
    
    @staticmethod
    def classify_leadership_level(score: float) -> str:
        """Classify leadership potential level based on score"""
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