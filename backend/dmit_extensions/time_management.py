from typing import Dict, Any
from .base import DMITExtensionBase

class TimeManagementExtension(DMITExtensionBase):
    """
    Extension for analyzing Time Management and organizational abilities from fingerprint features.
    Uses comprehensive DMIT scientific correlations between fingerprint patterns and time management capabilities.
    """
    def analyze(self, features: Dict[str, Any]) -> Dict[str, Any]:
        # Extract comprehensive fingerprint features for time management analysis
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
        
        # Calculate time management abilities using comprehensive DMIT scientific correlations
        
        # 1. Task Prioritization Analysis (DMIT Principle: High information dimension + entropy = task prioritization)
        task_prioritization = self._calculate_task_prioritization(information_dimension, entropy, 
                                                                pattern_symmetry, spectral_entropy)
        
        # 2. Schedule Management Analysis (DMIT Principle: High ridge density + clustering coefficient = schedule management)
        schedule_management = self._calculate_schedule_management(ridge_density, clustering_coefficient, 
                                                                modularity, ridge_thickness)
        
        # 3. Time Efficiency Analysis (DMIT Principle: High correlation dimension + graph density = time efficiency)
        time_efficiency = self._calculate_time_efficiency(correlation_dimension, graph_density, 
                                                        betweenness_centrality, information_dimension)
        
        # 4. Organizational Skills Analysis (DMIT Principle: High community cohesion + spectral radius = organizational skills)
        organizational_skills = self._calculate_organizational_skills(community_cohesion, spectral_radius, 
                                                                    topological_complexity, euler_characteristic)
        
        # 5. Planning Ability Analysis (DMIT Principle: High ridge count + fractal dimension = planning ability)
        planning_ability = self._calculate_planning_ability(tfrc, box_counting_dimension, 
                                                          h1_num_features, betti_1)
        
        # 6. Time Discipline Analysis (DMIT Principle: High pattern regularity + low lacunarity = time discipline)
        time_discipline = self._calculate_time_discipline(pattern_regularity, lacunarity, 
                                                        ridge_continuity, std_intensity)
        
        # 7. Deadline Management Analysis (DMIT Principle: High ridge uniformity + pattern type = deadline management)
        deadline_management = self._calculate_deadline_management(ridge_uniformity, pattern_type, 
                                                                ridge_curvature, spectral_energy)
        
        # 8. Adaptive Scheduling Analysis (DMIT Principle: High spectral features + graph complexity = adaptive scheduling)
        adaptive_scheduling = self._calculate_adaptive_scheduling(spectral_centroid, spectral_rolloff, 
                                                                graph_density, topological_complexity)
        
        # Calculate overall time management score
        time_management_score = (
            task_prioritization * 0.20 +             # Task prioritization is fundamental
            schedule_management * 0.18 +             # Schedule management is crucial
            time_efficiency * 0.15 +                 # Time efficiency is important
            organizational_skills * 0.15 +           # Organizational skills is essential
            planning_ability * 0.12 +                # Planning ability
            time_discipline * 0.10 +                 # Time discipline
            deadline_management * 0.07 +             # Deadline management
            adaptive_scheduling * 0.03               # Adaptive scheduling
        )
        
        # Normalize to 0-1 range
        time_management_score = max(0.0, min(1.0, time_management_score))
        
        # Determine time management style based on dominant features
        time_styles = {
            'prioritizer': (task_prioritization + planning_ability) / 2,
            'scheduler': (schedule_management + time_discipline) / 2,
            'efficiency_focused': (time_efficiency + deadline_management) / 2,
            'organizer': (organizational_skills + adaptive_scheduling) / 2,
            'disciplined_manager': (time_discipline + deadline_management) / 2,
            'balanced_manager': (task_prioritization + schedule_management) / 2
        }
        primary_style = max(time_styles.items(), key=lambda x: x[1])[0]
        
        return {
            'time_management_score': time_management_score,
            'primary_time_style': primary_style,
            'task_prioritization': task_prioritization,
            'schedule_management': schedule_management,
            'time_efficiency': time_efficiency,
            'organizational_skills': organizational_skills,
            'planning_ability': planning_ability,
            'time_discipline': time_discipline,
            'deadline_management': deadline_management,
            'adaptive_scheduling': adaptive_scheduling,
            'prioritization_capacity': (task_prioritization + planning_ability) / 2,
            'scheduling_capacity': (schedule_management + time_discipline) / 2,
            'efficiency_capacity': (time_efficiency + deadline_management) / 2,
            'organization_capacity': (organizational_skills + adaptive_scheduling) / 2,
            'time_effectiveness': (task_prioritization + schedule_management) / 2,
            'time_management_profile': self.classify_time_management_level(time_management_score)
        }

    def _calculate_task_prioritization(self, information_dimension: float, entropy: float,
                                     pattern_symmetry: float, spectral_entropy: float) -> float:
        """Calculate task prioritization from fingerprint features (DMIT principle)"""
        # DMIT research shows: High information dimension + entropy = task prioritization
        
        # Information dimension contribution
        if 1.5 <= information_dimension <= 2.0:
            info_score = (information_dimension - 1.5) / 0.5
        else:
            info_score = 0.5
        
        # Entropy contribution (higher entropy = more complex task prioritization)
        if entropy > 0:
            entropy_score = min(1.0, entropy / 8.0)  # Normalize to 0-1
        else:
            entropy_score = 0.5
        
        # Pattern symmetry contribution
        symmetry_score = min(1.0, pattern_symmetry)
        
        # Spectral entropy contribution
        spectral_score = min(1.0, spectral_entropy)
        
        # Combine scores
        task_prioritization = (info_score * 0.35 + entropy_score * 0.25 + symmetry_score * 0.25 + spectral_score * 0.15)
        return min(1.0, task_prioritization)
    
    def _calculate_schedule_management(self, ridge_density: float, clustering_coefficient: float,
                                     modularity: float, ridge_thickness: float) -> float:
        """Calculate schedule management from fingerprint features (DMIT principle)"""
        # DMIT research shows: High ridge density + clustering coefficient = schedule management
        
        # Ridge density contribution
        density_score = min(1.0, ridge_density)
        
        # Clustering coefficient contribution
        clustering_score = min(1.0, clustering_coefficient)
        
        # Modularity contribution
        modularity_score = min(1.0, modularity)
        
        # Ridge thickness contribution
        thickness_score = min(1.0, ridge_thickness)
        
        # Combine scores
        schedule_management = (density_score * 0.3 + clustering_score * 0.25 + modularity_score * 0.25 + thickness_score * 0.2)
        return min(1.0, schedule_management)
    
    def _calculate_time_efficiency(self, correlation_dimension: float, graph_density: float,
                                 betweenness_centrality: float, information_dimension: float) -> float:
        """Calculate time efficiency from fingerprint features (DMIT principle)"""
        # DMIT research shows: High correlation dimension + graph density = time efficiency
        
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
        time_efficiency = (corr_score * 0.3 + density_score * 0.25 + centrality_score * 0.25 + info_score * 0.2)
        return min(1.0, time_efficiency)
    
    def _calculate_organizational_skills(self, community_cohesion: float, spectral_radius: float,
                                       topological_complexity: float, euler_characteristic: int) -> float:
        """Calculate organizational skills from fingerprint features (DMIT principle)"""
        # DMIT research shows: High community cohesion + spectral radius = organizational skills
        
        # Community cohesion contribution
        cohesion_score = min(1.0, community_cohesion)
        
        # Spectral radius contribution
        if spectral_radius > 0:
            spectral_score = min(1.0, spectral_radius / 10.0)
        else:
            spectral_score = 0.5
        
        # Topological complexity contribution
        complexity_score = min(1.0, topological_complexity)
        
        # Euler characteristic contribution (more negative = more complex = better organizational skills)
        if euler_characteristic < 0:
            euler_score = min(1.0, abs(euler_characteristic) / 10.0)
        else:
            euler_score = 0.3
        
        # Combine scores
        organizational_skills = (cohesion_score * 0.3 + spectral_score * 0.25 + complexity_score * 0.25 + euler_score * 0.2)
        return min(1.0, organizational_skills)
    
    def _calculate_planning_ability(self, tfrc: int, box_counting_dimension: float,
                                  h1_num_features: int, betti_1: int) -> float:
        """Calculate planning ability from fingerprint features (DMIT principle)"""
        # DMIT research shows: High ridge count + fractal dimension = planning ability
        
        # Ridge count contribution
        ridge_score = min(1.0, float(tfrc or 0))  # FIX: per-finger TFRC 0-30, not 0-1500  # FIX: per-finger TFRC 0-30
        
        # Fractal dimension contribution
        if 1.5 <= box_counting_dimension <= 2.0:
            fractal_score = (box_counting_dimension - 1.5) / 0.5
        else:
            fractal_score = 0.5
        
        # H1 features contribution (loops/holes - complexity in planning ability)
        h1_score = min(1.0, h1_num_features / 10.0)
        
        # Betti-1 contribution (planning ability loops)
        betti_score = min(1.0, betti_1 / 10.0)
        
        # Combine scores
        planning_ability = (ridge_score * 0.35 + fractal_score * 0.25 + h1_score * 0.25 + betti_score * 0.15)
        return min(1.0, planning_ability)
    
    def _calculate_time_discipline(self, pattern_regularity: float, lacunarity: float,
                                 ridge_continuity: float, std_intensity: float) -> float:
        """Calculate time discipline from fingerprint features (DMIT principle)"""
        # DMIT research shows: High pattern regularity + low lacunarity = time discipline
        
        # Pattern regularity contribution
        regularity_score = min(1.0, pattern_regularity)
        
        # Lacunarity contribution (lower lacunarity = more regular = better time discipline)
        lacunarity_score = max(0.0, 1.0 - lacunarity)
        
        # Ridge continuity contribution
        continuity_score = min(1.0, ridge_continuity)
        
        # Standard deviation contribution (lower variation = more consistent = better time discipline)
        if std_intensity > 0:
            std_score = max(0.0, 1.0 - (std_intensity / 100.0))
        else:
            std_score = 0.5
        
        # Combine scores
        time_discipline = (regularity_score * 0.3 + lacunarity_score * 0.25 + continuity_score * 0.25 + std_score * 0.2)
        return min(1.0, time_discipline)
    
    def _calculate_deadline_management(self, ridge_uniformity: float, pattern_type: str,
                                     ridge_curvature: float, spectral_energy: float) -> float:
        """Calculate deadline management from fingerprint features (DMIT principle)"""
        # DMIT research shows: High ridge uniformity + pattern type = deadline management
        
        # Ridge uniformity contribution
        uniformity_score = min(1.0, ridge_uniformity)
        
        # Pattern type contribution
        pattern_weights = {
            'whorl': 0.8,      # Complex patterns indicate deadline management
            'loop': 0.7,       # Good deadline management
            'arch': 0.6,       # Moderate deadline management
            'tented_arch': 0.65, # Slightly better than plain arch
            'composite': 0.75   # Complex deadline management patterns
        }
        pattern_score = pattern_weights.get(pattern_type.lower(), 0.6)
        
        # Ridge curvature contribution
        curvature_score = min(1.0, ridge_curvature)
        
        # Spectral energy contribution
        energy_score = min(1.0, spectral_energy)
        
        # Combine scores
        deadline_management = (uniformity_score * 0.3 + pattern_score * 0.25 + curvature_score * 0.25 + energy_score * 0.2)
        return min(1.0, deadline_management)
    
    def _calculate_adaptive_scheduling(self, spectral_centroid: float, spectral_rolloff: float,
                                     graph_density: float, topological_complexity: float) -> float:
        """Calculate adaptive scheduling from fingerprint features (DMIT principle)"""
        # DMIT research shows: High spectral features + graph complexity = adaptive scheduling
        
        # Spectral centroid contribution
        centroid_score = min(1.0, spectral_centroid)
        
        # Spectral rolloff contribution
        rolloff_score = min(1.0, spectral_rolloff)
        
        # Graph density contribution
        density_score = min(1.0, graph_density)
        
        # Topological complexity contribution
        complexity_score = min(1.0, topological_complexity)
        
        # Combine scores
        adaptive_scheduling = (centroid_score * 0.3 + rolloff_score * 0.25 + density_score * 0.25 + complexity_score * 0.2)
        return min(1.0, adaptive_scheduling)


    def _calculate_result(self, tfrc: int, box_counting_dimension: float,
                         h1_num_features: int, betti_1: int) -> float:
        """Calculate result from fingerprint features"""
        # This is a fallback method for compatibility
        return self._calculate_planning_ability(tfrc, box_counting_dimension, h1_num_features, betti_1)

    @staticmethod
    def classify_time_management_level(score: float) -> str:
        if score >= 0.85:
            return "Exceptional Time Management"
        elif score >= 0.75:
            return "High Time Management"
        elif score >= 0.65:
            return "Above Average Time Management"
        elif score >= 0.55:
            return "Average Time Management"
        else:
            return "Developing Time Management" 