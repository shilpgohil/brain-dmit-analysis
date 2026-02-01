from typing import Dict, Any
from .base import DMITExtensionBase

class LeadershipSkillsExtension(DMITExtensionBase):
    """
    Extension for analyzing Leadership Skills and management abilities from fingerprint features.
    Uses comprehensive DMIT scientific correlations between fingerprint patterns and leadership capabilities.
    """
    def analyze(self, features: Dict[str, Any]) -> Dict[str, Any]:
        # Extract comprehensive fingerprint features for leadership skills analysis
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
        
        # Calculate leadership skills abilities using comprehensive DMIT scientific correlations
        
        # 1. Visionary Leadership Analysis (DMIT Principle: High information dimension + entropy = visionary leadership)
        visionary_leadership = self._calculate_visionary_leadership(information_dimension, entropy, 
                                                                 pattern_symmetry, spectral_entropy)
        
        # 2. Team Management Analysis (DMIT Principle: High ridge density + clustering coefficient = team management)
        team_management = self._calculate_team_management(ridge_density, clustering_coefficient, 
                                                        modularity, ridge_thickness)
        
        # 3. Strategic Thinking Analysis (DMIT Principle: High correlation dimension + graph density = strategic thinking)
        strategic_thinking = self._calculate_strategic_thinking(correlation_dimension, graph_density, 
                                                              betweenness_centrality, information_dimension)
        
        # 4. Decision Making Analysis (DMIT Principle: High community cohesion + spectral radius = decision making)
        decision_making = self._calculate_decision_making(community_cohesion, spectral_radius, 
                                                        topological_complexity, euler_characteristic)
        
        # 5. Communication Leadership Analysis (DMIT Principle: High ridge count + fractal dimension = communication leadership)
        communication_leadership = self._calculate_communication_leadership(tfrc, box_counting_dimension, h1_num_features, betti_1)
        
        # 6. Conflict Resolution Analysis (DMIT Principle: High pattern regularity + low lacunarity = conflict resolution)
        conflict_resolution = self._calculate_conflict_resolution(pattern_regularity, lacunarity, 
                                                                ridge_continuity, std_intensity)
        
        # 7. Inspirational Leadership Analysis (DMIT Principle: High ridge uniformity + pattern type = inspirational leadership)
        inspirational_leadership = self._calculate_inspirational_leadership(ridge_uniformity, pattern_type, 
                                                                          ridge_curvature, spectral_energy)
        
        # 8. Adaptive Leadership Analysis (DMIT Principle: High spectral features + graph complexity = adaptive leadership)
        adaptive_leadership = self._calculate_adaptive_leadership(spectral_centroid, spectral_rolloff, 
                                                                graph_density, topological_complexity)
        
        # Calculate overall leadership skills score
        leadership_skills_score = (
            visionary_leadership * 0.20 +            # Visionary leadership is fundamental
            team_management * 0.18 +                 # Team management is crucial
            strategic_thinking * 0.15 +              # Strategic thinking is important
            decision_making * 0.15 +                 # Decision making is essential
            communication_leadership * 0.12 +        # Communication leadership
            conflict_resolution * 0.10 +             # Conflict resolution
            inspirational_leadership * 0.07 +        # Inspirational leadership
            adaptive_leadership * 0.03               # Adaptive leadership
        )
        
        # Normalize to 0-1 range
        leadership_skills_score = max(0.0, min(1.0, leadership_skills_score))
        
        # Determine leadership skills style based on dominant features
        leadership_styles = {
            'visionary_leader': visionary_leadership + strategic_thinking,
            'team_manager': team_management + decision_making,
            'strategic_leader': strategic_thinking + communication_leadership,
            'conflict_resolver': conflict_resolution + adaptive_leadership,
            'inspirational_leader': inspirational_leadership + visionary_leadership,
            'balanced_leader': (visionary_leadership + team_management) / 2
        }
        primary_style = max(leadership_styles.items(), key=lambda x: x[1])[0]
        
        return {
            'leadership_skills_score': leadership_skills_score,
            'primary_leadership_style': primary_style,
            'visionary_leadership': visionary_leadership,
            'team_management': team_management,
            'strategic_thinking': strategic_thinking,
            'decision_making': decision_making,
            'communication_leadership': communication_leadership,
            'conflict_resolution': conflict_resolution,
            'inspirational_leadership': inspirational_leadership,
            'adaptive_leadership': adaptive_leadership,
            'leadership_effectiveness': visionary_leadership + team_management,
            'strategic_leadership': strategic_thinking + decision_making,
            'people_leadership': team_management + conflict_resolution,
            'vision_communication': visionary_leadership + communication_leadership,
            'adaptive_management': adaptive_leadership + strategic_thinking,
            'leadership_skills_profile': self.classify_leadership_skills_level(leadership_skills_score)
        }

    def _calculate_visionary_leadership(self, information_dimension: float, entropy: float,
                                      pattern_symmetry: float, spectral_entropy: float) -> float:
        """Calculate visionary leadership from fingerprint features (DMIT principle)"""
        # DMIT research shows: High information dimension + entropy = visionary leadership
        
        # Information dimension contribution
        if 1.5 <= information_dimension <= 2.0:
            info_score = (information_dimension - 1.5) / 0.5
        else:
            info_score = 0.5
        
        # Entropy contribution (higher entropy = more complex visionary leadership)
        if entropy > 0:
            entropy_score = min(1.0, entropy / 8.0)  # Normalize to 0-1
        else:
            entropy_score = 0.5
        
        # Pattern symmetry contribution
        symmetry_score = min(1.0, pattern_symmetry)
        
        # Spectral entropy contribution
        spectral_score = min(1.0, spectral_entropy)
        
        # Combine scores
        visionary_leadership = (info_score * 0.35 + entropy_score * 0.25 + symmetry_score * 0.25 + spectral_score * 0.15)
        return min(1.0, visionary_leadership)
    
    def _calculate_team_management(self, ridge_density: float, clustering_coefficient: float,
                                 modularity: float, ridge_thickness: float) -> float:
        """Calculate team management from fingerprint features (DMIT principle)"""
        # DMIT research shows: High ridge density + clustering coefficient = team management
        
        # Ridge density contribution
        density_score = min(1.0, ridge_density)
        
        # Clustering coefficient contribution
        clustering_score = min(1.0, clustering_coefficient)
        
        # Modularity contribution
        modularity_score = min(1.0, modularity)
        
        # Ridge thickness contribution
        thickness_score = min(1.0, ridge_thickness)
        
        # Combine scores
        team_management = (density_score * 0.3 + clustering_score * 0.25 + modularity_score * 0.25 + thickness_score * 0.2)
        return min(1.0, team_management)
    
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
    
    def _calculate_decision_making(self, community_cohesion: float, spectral_radius: float,
                                 topological_complexity: float, euler_characteristic: int) -> float:
        """Calculate decision making from fingerprint features (DMIT principle)"""
        # DMIT research shows: High community cohesion + spectral radius = decision making
        
        # Community cohesion contribution
        cohesion_score = min(1.0, community_cohesion)
        
        # Spectral radius contribution
        if spectral_radius > 0:
            spectral_score = min(1.0, spectral_radius / 10.0)
        else:
            spectral_score = 0.5
        
        # Topological complexity contribution
        complexity_score = min(1.0, topological_complexity)
        
        # Euler characteristic contribution (more negative = more complex = better decision making)
        if euler_characteristic < 0:
            euler_score = min(1.0, abs(euler_characteristic) / 10.0)
        else:
            euler_score = 0.3
        
        # Combine scores
        decision_making = (cohesion_score * 0.3 + spectral_score * 0.25 + complexity_score * 0.25 + euler_score * 0.2)
        return min(1.0, decision_making)
    
    def _calculate_communication_leadership(self, tfrc: int, box_counting_dimension: float, h1_num_features: int, betti_1: int) -> float:
        """Calculate communication leadership from fingerprint features (DMIT principle)"""
        # DMIT research shows: High ridge count + fractal dimension = communication leadership
        # Ridge count contribution
        if tfrc > 0:
            ridge_score = min(1.0, tfrc / 1500.0)
        else:
            ridge_score = 0.0
        # Fractal dimension contribution
        if 1.5 <= box_counting_dimension <= 2.0:
            fractal_score = (box_counting_dimension - 1.5) / 0.5
        else:
            fractal_score = 0.5
        # H1 features contribution (loops/holes - complexity in communication leadership)
        h1_score = min(1.0, h1_num_features / 10.0)
        # Betti-1 contribution (communication leadership loops)
        betti_score = min(1.0, betti_1 / 10.0)
        # Combine scores
        communication_leadership = (ridge_score * 0.35 + fractal_score * 0.25 + h1_score * 0.25 + betti_score * 0.15)
        return min(1.0, communication_leadership)
    
    def _calculate_conflict_resolution(self, pattern_regularity: float, lacunarity: float,
                                     ridge_continuity: float, std_intensity: float) -> float:
        """Calculate conflict resolution from fingerprint features (DMIT principle)"""
        # DMIT research shows: High pattern regularity + low lacunarity = conflict resolution
        
        # Pattern regularity contribution
        regularity_score = min(1.0, pattern_regularity)
        
        # Lacunarity contribution (lower lacunarity = more regular = better conflict resolution)
        lacunarity_score = max(0.0, 1.0 - lacunarity)
        
        # Ridge continuity contribution
        continuity_score = min(1.0, ridge_continuity)
        
        # Standard deviation contribution (lower variation = more consistent = better conflict resolution)
        if std_intensity > 0:
            std_score = max(0.0, 1.0 - (std_intensity / 100.0))
        else:
            std_score = 0.5
        
        # Combine scores
        conflict_resolution = (regularity_score * 0.3 + lacunarity_score * 0.25 + continuity_score * 0.25 + std_score * 0.2)
        return min(1.0, conflict_resolution)
    
    def _calculate_inspirational_leadership(self, ridge_uniformity: float, pattern_type: str,
                                          ridge_curvature: float, spectral_energy: float) -> float:
        """Calculate inspirational leadership from fingerprint features (DMIT principle)"""
        # DMIT research shows: High ridge uniformity + pattern type = inspirational leadership
        
        # Ridge uniformity contribution
        uniformity_score = min(1.0, ridge_uniformity)
        
        # Pattern type contribution
        pattern_weights = {
            'whorl': 0.8,      # Complex patterns indicate inspirational leadership
            'loop': 0.7,       # Good inspirational leadership
            'arch': 0.6,       # Moderate inspirational leadership
            'tented_arch': 0.65, # Slightly better than plain arch
            'composite': 0.75   # Complex inspirational leadership patterns
        }
        pattern_score = pattern_weights.get(pattern_type.lower(), 0.6)
        
        # Ridge curvature contribution
        curvature_score = min(1.0, ridge_curvature)
        
        # Spectral energy contribution
        energy_score = min(1.0, spectral_energy)
        
        # Combine scores
        inspirational_leadership = (uniformity_score * 0.3 + pattern_score * 0.25 + curvature_score * 0.25 + energy_score * 0.2)
        return min(1.0, inspirational_leadership)
    
    def _calculate_adaptive_leadership(self, spectral_centroid: float, spectral_rolloff: float,
                                     graph_density: float, topological_complexity: float) -> float:
        """Calculate adaptive leadership from fingerprint features (DMIT principle)"""
        # DMIT research shows: High spectral features + graph complexity = adaptive leadership
        
        # Spectral centroid contribution
        centroid_score = min(1.0, spectral_centroid)
        
        # Spectral rolloff contribution
        rolloff_score = min(1.0, spectral_rolloff)
        
        # Graph density contribution
        density_score = min(1.0, graph_density)
        
        # Topological complexity contribution
        complexity_score = min(1.0, topological_complexity)
        
        # Combine scores
        adaptive_leadership = (centroid_score * 0.3 + rolloff_score * 0.25 + density_score * 0.25 + complexity_score * 0.2)
        return min(1.0, adaptive_leadership)

    @staticmethod
    def classify_leadership_skills_level(score: float) -> str:
        if score >= 0.85:
            return "Exceptional Leadership Skills"
        elif score >= 0.75:
            return "High Leadership Skills"
        elif score >= 0.65:
            return "Above Average Leadership Skills"
        elif score >= 0.55:
            return "Average Leadership Skills"
        else:
            return "Developing Leadership Skills" 
