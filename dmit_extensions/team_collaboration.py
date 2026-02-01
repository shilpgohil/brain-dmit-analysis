from typing import Dict, Any
from .base import DMITExtensionBase

class TeamCollaborationExtension(DMITExtensionBase):
    """
    Extension for analyzing Team Collaboration and teamwork abilities from fingerprint features.
    Uses comprehensive DMIT scientific correlations between fingerprint patterns and collaboration capabilities.
    """
    def analyze(self, features: Dict[str, Any]) -> Dict[str, Any]:
        # Extract comprehensive fingerprint features for team collaboration analysis
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
        
        # Calculate team collaboration abilities using comprehensive DMIT scientific correlations
        
        # 1. Team Communication Analysis (DMIT Principle: High information dimension + entropy = team communication)
        team_communication = self._calculate_team_communication(information_dimension, entropy, 
                                                              pattern_symmetry, spectral_entropy)
        
        # 2. Group Coordination Analysis (DMIT Principle: High ridge density + clustering coefficient = group coordination)
        group_coordination = self._calculate_group_coordination(ridge_density, clustering_coefficient, 
                                                              modularity, ridge_thickness)
        
        # 3. Collaborative Problem Solving Analysis (DMIT Principle: High correlation dimension + graph density = collaborative problem solving)
        collaborative_problem_solving = self._calculate_collaborative_problem_solving(correlation_dimension, graph_density, 
                                                                                    betweenness_centrality, information_dimension)
        
        # 4. Team Synergy Analysis (DMIT Principle: High community cohesion + spectral radius = team synergy)
        team_synergy = self._calculate_team_synergy(community_cohesion, spectral_radius, 
                                                   topological_complexity, euler_characteristic)
        
        # 5. Collective Intelligence Analysis (DMIT Principle: High ridge count + fractal dimension = collective intelligence)
        collective_intelligence = self._calculate_result(tfrc, box_counting_dimension, 
                                                                        h1_num_features, betti_1)
        
        # 6. Team Harmony Analysis (DMIT Principle: High pattern regularity + low lacunarity = team harmony)
        team_harmony = self._calculate_team_harmony(pattern_regularity, lacunarity, 
                                                   ridge_continuity, std_intensity)
        
        # 7. Interpersonal Collaboration Analysis (DMIT Principle: High ridge uniformity + pattern type = interpersonal collaboration)
        interpersonal_collaboration = self._calculate_interpersonal_collaboration(ridge_uniformity, pattern_type, 
                                                                                ridge_curvature, spectral_energy)
        
        # 8. Adaptive Teamwork Analysis (DMIT Principle: High spectral features + graph complexity = adaptive teamwork)
        adaptive_teamwork = self._calculate_adaptive_teamwork(spectral_centroid, spectral_rolloff, 
                                                            graph_density, topological_complexity)
        
        # Calculate overall team collaboration score
        team_collaboration_score = (
            team_communication * 0.20 +              # Team communication is fundamental
            group_coordination * 0.18 +              # Group coordination is crucial
            collaborative_problem_solving * 0.15 +   # Collaborative problem solving is important
            team_synergy * 0.15 +                    # Team synergy is essential
            collective_intelligence * 0.12 +         # Collective intelligence
            team_harmony * 0.10 +                    # Team harmony
            interpersonal_collaboration * 0.07 +     # Interpersonal collaboration
            adaptive_teamwork * 0.03                 # Adaptive teamwork
        )
        
        # Normalize to 0-1 range
        team_collaboration_score = max(0.0, min(1.0, team_collaboration_score))
        
        # Determine team collaboration style based on dominant features
        team_styles = {
            'communicative_collaborator': team_communication + interpersonal_collaboration,
            'coordinated_team_player': group_coordination + team_harmony,
            'synergistic_problem_solver': collaborative_problem_solving + team_synergy,
            'adaptive_team_member': adaptive_teamwork + collective_intelligence,
            'harmonious_collaborator': team_harmony + interpersonal_collaboration,
            'balanced_team_player': (team_communication + group_coordination) / 2
        }
        primary_style = max(team_styles.items(), key=lambda x: x[1])[0]
        
        return {
            'team_collaboration_score': team_collaboration_score,
            'primary_team_style': primary_style,
            'team_communication': team_communication,
            'group_coordination': group_coordination,
            'collaborative_problem_solving': collaborative_problem_solving,
            'team_synergy': team_synergy,
            'collective_intelligence': collective_intelligence,
            'team_harmony': team_harmony,
            'interpersonal_collaboration': interpersonal_collaboration,
            'adaptive_teamwork': adaptive_teamwork,
            'communication_capacity': team_communication + interpersonal_collaboration,
            'coordination_capacity': group_coordination + team_harmony,
            'synergy_capacity': collaborative_problem_solving + team_synergy,
            'adaptability_capacity': adaptive_teamwork + collective_intelligence,
            'team_effectiveness': team_communication + group_coordination,
            'team_collaboration_profile': self.classify_team_collaboration_level(team_collaboration_score)
        }

    def _calculate_team_communication(self, information_dimension: float, entropy: float,
                                    pattern_symmetry: float, spectral_entropy: float) -> float:
        """Calculate team communication from fingerprint features (DMIT principle)"""
        # DMIT research shows: High information dimension + entropy = team communication
        
        # Information dimension contribution
        if 1.5 <= information_dimension <= 2.0:
            info_score = (information_dimension - 1.5) / 0.5
        else:
            info_score = 0.5
        
        # Entropy contribution (higher entropy = more complex team communication)
        if entropy > 0:
            entropy_score = min(1.0, entropy / 8.0)  # Normalize to 0-1
        else:
            entropy_score = 0.5
        
        # Pattern symmetry contribution
        symmetry_score = min(1.0, pattern_symmetry)
        
        # Spectral entropy contribution
        spectral_score = min(1.0, spectral_entropy)
        
        # Combine scores
        team_communication = (info_score * 0.35 + entropy_score * 0.25 + symmetry_score * 0.25 + spectral_score * 0.15)
        return min(1.0, team_communication)
    
    def _calculate_group_coordination(self, ridge_density: float, clustering_coefficient: float,
                                    modularity: float, ridge_thickness: float) -> float:
        """Calculate group coordination from fingerprint features (DMIT principle)"""
        # DMIT research shows: High ridge density + clustering coefficient = group coordination
        
        # Ridge density contribution
        density_score = min(1.0, ridge_density)
        
        # Clustering coefficient contribution
        clustering_score = min(1.0, clustering_coefficient)
        
        # Modularity contribution
        modularity_score = min(1.0, modularity)
        
        # Ridge thickness contribution
        thickness_score = min(1.0, ridge_thickness)
        
        # Combine scores
        group_coordination = (density_score * 0.3 + clustering_score * 0.25 + modularity_score * 0.25 + thickness_score * 0.2)
        return min(1.0, group_coordination)
    
    def _calculate_collaborative_problem_solving(self, correlation_dimension: float, graph_density: float,
                                               betweenness_centrality: float, information_dimension: float) -> float:
        """Calculate collaborative problem solving from fingerprint features (DMIT principle)"""
        # DMIT research shows: High correlation dimension + graph density = collaborative problem solving
        
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
        collaborative_problem_solving = (corr_score * 0.3 + density_score * 0.25 + centrality_score * 0.25 + info_score * 0.2)
        return min(1.0, collaborative_problem_solving)
    
    def _calculate_team_synergy(self, community_cohesion: float, spectral_radius: float,
                              topological_complexity: float, euler_characteristic: int) -> float:
        """Calculate team synergy from fingerprint features (DMIT principle)"""
        # DMIT research shows: High community cohesion + spectral radius = team synergy
        
        # Community cohesion contribution
        cohesion_score = min(1.0, community_cohesion)
        
        # Spectral radius contribution
        if spectral_radius > 0:
            spectral_score = min(1.0, spectral_radius / 10.0)
        else:
            spectral_score = 0.5
        
        # Topological complexity contribution
        complexity_score = min(1.0, topological_complexity)
        
        # Euler characteristic contribution (more negative = more complex = better team synergy)
        if euler_characteristic < 0:
            euler_score = min(1.0, abs(euler_characteristic) / 10.0)
        else:
            euler_score = 0.3
        
        # Combine scores
        team_synergy = (cohesion_score * 0.3 + spectral_score * 0.25 + complexity_score * 0.25 + euler_score * 0.2)
        return min(1.0, team_synergy)
    
    def _calculate_team_leadership(self, tfrc: int, box_counting_dimension: float,
                                         h1_num_features: int, betti_1: int) -> float:
        """Calculate collective intelligence from fingerprint features (DMIT principle)"""
        # DMIT research shows: High ridge count + fractal dimension = collective intelligence
        
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
        
        # H1 features contribution (loops/holes - complexity in collective intelligence)
        h1_score = min(1.0, h1_num_features / 10.0)
        
        # Betti-1 contribution (collective intelligence loops)
        betti_score = min(1.0, betti_1 / 10.0)
        
        # Combine scores
        collective_intelligence = (ridge_score * 0.35 + fractal_score * 0.25 + h1_score * 0.25 + betti_score * 0.15)
        return min(1.0, collective_intelligence)
    
    def _calculate_team_harmony(self, pattern_regularity: float, lacunarity: float,
                              ridge_continuity: float, std_intensity: float) -> float:
        """Calculate team harmony from fingerprint features (DMIT principle)"""
        # DMIT research shows: High pattern regularity + low lacunarity = team harmony
        
        # Pattern regularity contribution
        regularity_score = min(1.0, pattern_regularity)
        
        # Lacunarity contribution (lower lacunarity = more regular = better team harmony)
        lacunarity_score = max(0.0, 1.0 - lacunarity)
        
        # Ridge continuity contribution
        continuity_score = min(1.0, ridge_continuity)
        
        # Standard deviation contribution (lower variation = more consistent = better team harmony)
        if std_intensity > 0:
            std_score = max(0.0, 1.0 - (std_intensity / 100.0))
        else:
            std_score = 0.5
        
        # Combine scores
        team_harmony = (regularity_score * 0.3 + lacunarity_score * 0.25 + continuity_score * 0.25 + std_score * 0.2)
        return min(1.0, team_harmony)
    
    def _calculate_interpersonal_collaboration(self, ridge_uniformity: float, pattern_type: str,
                                             ridge_curvature: float, spectral_energy: float) -> float:
        """Calculate interpersonal collaboration from fingerprint features (DMIT principle)"""
        # DMIT research shows: High ridge uniformity + pattern type = interpersonal collaboration
        
        # Ridge uniformity contribution
        uniformity_score = min(1.0, ridge_uniformity)
        
        # Pattern type contribution
        pattern_weights = {
            'whorl': 0.8,      # Complex patterns indicate interpersonal collaboration
            'loop': 0.7,       # Good interpersonal collaboration
            'arch': 0.6,       # Moderate interpersonal collaboration
            'tented_arch': 0.65, # Slightly better than plain arch
            'composite': 0.75   # Complex interpersonal collaboration patterns
        }
        pattern_score = pattern_weights.get(pattern_type.lower(), 0.6)
        
        # Ridge curvature contribution
        curvature_score = min(1.0, ridge_curvature)
        
        # Spectral energy contribution
        energy_score = min(1.0, spectral_energy)
        
        # Combine scores
        interpersonal_collaboration = (uniformity_score * 0.3 + pattern_score * 0.25 + curvature_score * 0.25 + energy_score * 0.2)
        return min(1.0, interpersonal_collaboration)
    
    def _calculate_adaptive_teamwork(self, spectral_centroid: float, spectral_rolloff: float,
                                   graph_density: float, topological_complexity: float) -> float:
        """Calculate adaptive teamwork from fingerprint features (DMIT principle)"""
        # DMIT research shows: High spectral features + graph complexity = adaptive teamwork
        
        # Spectral centroid contribution
        centroid_score = min(1.0, spectral_centroid)
        
        # Spectral rolloff contribution
        rolloff_score = min(1.0, spectral_rolloff)
        
        # Graph density contribution
        density_score = min(1.0, graph_density)
        
        # Topological complexity contribution
        complexity_score = min(1.0, topological_complexity)
        
        # Combine scores
        adaptive_teamwork = (centroid_score * 0.3 + rolloff_score * 0.25 + density_score * 0.25 + complexity_score * 0.2)
        return min(1.0, adaptive_teamwork)


    def _calculate_result(self, tfrc: int, box_counting_dimension: float,
                         h1_num_features: int, betti_1: int) -> float:
        """Calculate result from fingerprint features"""
        # This is a fallback method for compatibility
        return self._calculate_team_leadership(tfrc, box_counting_dimension, h1_num_features, betti_1)

    @staticmethod
    def classify_team_collaboration_level(score: float) -> str:
        if score >= 0.85:
            return "Exceptional Team Collaboration"
        elif score >= 0.75:
            return "High Team Collaboration"
        elif score >= 0.65:
            return "Above Average Team Collaboration"
        elif score >= 0.55:
            return "Average Team Collaboration"
        else:
            return "Developing Team Collaboration" 