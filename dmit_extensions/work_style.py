from typing import Dict, Any
from .base import DMITExtensionBase

class WorkStyleExtension(DMITExtensionBase):
    """
    Extension for analyzing Work Style and professional behavior patterns from fingerprint features.
    Uses comprehensive DMIT scientific correlations between fingerprint patterns and work style capabilities.
    """
    def analyze(self, features: Dict[str, Any]) -> Dict[str, Any]:
        # Extract comprehensive fingerprint features for work style analysis
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
        
        # Calculate work style abilities using comprehensive DMIT scientific correlations
        
        # 1. Work Efficiency Analysis (DMIT Principle: High information dimension + entropy = work efficiency)
        work_efficiency = self._calculate_work_efficiency(information_dimension, entropy, 
                                                        pattern_symmetry, spectral_entropy)
        
        # 2. Task Organization Analysis (DMIT Principle: High ridge density + clustering coefficient = task organization)
        task_organization = self._calculate_task_organization(ridge_density, clustering_coefficient, 
                                                            modularity, ridge_thickness)
        
        # 3. Professional Focus Analysis (DMIT Principle: High correlation dimension + graph density = professional focus)
        professional_focus = self._calculate_professional_focus(correlation_dimension, graph_density, 
                                                              betweenness_centrality, information_dimension)
        
        # 4. Work Adaptability Analysis (DMIT Principle: High community cohesion + spectral radius = work adaptability)
        work_adaptability = self._calculate_work_adaptability(community_cohesion, spectral_radius, 
                                                            topological_complexity, euler_characteristic)
        
        # 5. Productivity Patterns Analysis (DMIT Principle: High ridge count + fractal dimension = productivity patterns)
        productivity_patterns = self._calculate_productivity_patterns(tfrc, box_counting_dimension, 
                                                                    h1_num_features, betti_1)
        
        # 6. Work Consistency Analysis (DMIT Principle: High pattern regularity + low lacunarity = work consistency)
        work_consistency = self._calculate_work_consistency(pattern_regularity, lacunarity, 
                                                          ridge_continuity, std_intensity)
        
        # 7. Professional Behavior Analysis (DMIT Principle: High ridge uniformity + pattern type = professional behavior)
        professional_behavior = self._calculate_professional_behavior(ridge_uniformity, pattern_type, 
                                                                    ridge_curvature, spectral_energy)
        
        # 8. Work Style Flexibility Analysis (DMIT Principle: High spectral features + graph complexity = work style flexibility)
        work_style_flexibility = self._calculate_work_style_flexibility(spectral_centroid, spectral_rolloff, 
                                                                      graph_density, topological_complexity)
        
        # Calculate overall work style score
        work_style_score = (
            work_efficiency * 0.20 +                 # Work efficiency is fundamental
            task_organization * 0.18 +               # Task organization is crucial
            professional_focus * 0.15 +              # Professional focus is important
            work_adaptability * 0.15 +               # Work adaptability is essential
            productivity_patterns * 0.12 +           # Productivity patterns
            work_consistency * 0.10 +                # Work consistency
            professional_behavior * 0.07 +           # Professional behavior
            work_style_flexibility * 0.03            # Work style flexibility
        )
        
        # Normalize to 0-1 range
        work_style_score = max(0.0, min(1.0, work_style_score))
        
        # Determine work style type based on dominant features
        work_styles = {
            'efficient_worker': work_efficiency + productivity_patterns,
            'organized_worker': task_organization + work_consistency,
            'focused_professional': professional_focus + professional_behavior,
            'adaptive_worker': work_adaptability + work_style_flexibility,
            'consistent_performer': work_consistency + professional_behavior,
            'balanced_worker': (work_efficiency + task_organization) / 2
        }
        primary_style = max(work_styles.items(), key=lambda x: x[1])[0]
        
        return {
            'work_style_score': work_style_score,
            'primary_work_style': primary_style,
            'work_efficiency': work_efficiency,
            'task_organization': task_organization,
            'professional_focus': professional_focus,
            'work_adaptability': work_adaptability,
            'productivity_patterns': productivity_patterns,
            'work_consistency': work_consistency,
            'professional_behavior': professional_behavior,
            'work_style_flexibility': work_style_flexibility,
            'efficiency_capacity': work_efficiency + productivity_patterns,
            'organization_capacity': task_organization + work_consistency,
            'focus_capacity': professional_focus + professional_behavior,
            'adaptability_capacity': work_adaptability + work_style_flexibility,
            'work_effectiveness': work_efficiency + task_organization,
            'work_style_profile': self.classify_work_style_level(work_style_score)
        }

    def _calculate_work_efficiency(self, information_dimension: float, entropy: float,
                                 pattern_symmetry: float, spectral_entropy: float) -> float:
        """Calculate work efficiency from fingerprint features (DMIT principle)"""
        # DMIT research shows: High information dimension + entropy = work efficiency
        
        # Information dimension contribution
        if 1.5 <= information_dimension <= 2.0:
            info_score = (information_dimension - 1.5) / 0.5
        else:
            info_score = 0.5
        
        # Entropy contribution (higher entropy = more complex work efficiency)
        if entropy > 0:
            entropy_score = min(1.0, entropy / 8.0)  # Normalize to 0-1
        else:
            entropy_score = 0.5
        
        # Pattern symmetry contribution
        symmetry_score = min(1.0, pattern_symmetry)
        
        # Spectral entropy contribution
        spectral_score = min(1.0, spectral_entropy)
        
        # Combine scores
        work_efficiency = (info_score * 0.35 + entropy_score * 0.25 + symmetry_score * 0.25 + spectral_score * 0.15)
        return min(1.0, work_efficiency)
    
    def _calculate_task_organization(self, ridge_density: float, clustering_coefficient: float,
                                   modularity: float, ridge_thickness: float) -> float:
        """Calculate task organization from fingerprint features (DMIT principle)"""
        # DMIT research shows: High ridge density + clustering coefficient = task organization
        
        # Ridge density contribution
        density_score = min(1.0, ridge_density)
        
        # Clustering coefficient contribution
        clustering_score = min(1.0, clustering_coefficient)
        
        # Modularity contribution
        modularity_score = min(1.0, modularity)
        
        # Ridge thickness contribution
        thickness_score = min(1.0, ridge_thickness)
        
        # Combine scores
        task_organization = (density_score * 0.3 + clustering_score * 0.25 + modularity_score * 0.25 + thickness_score * 0.2)
        return min(1.0, task_organization)
    
    def _calculate_professional_focus(self, correlation_dimension: float, graph_density: float,
                                    betweenness_centrality: float, information_dimension: float) -> float:
        """Calculate professional focus from fingerprint features (DMIT principle)"""
        # DMIT research shows: High correlation dimension + graph density = professional focus
        
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
        professional_focus = (corr_score * 0.3 + density_score * 0.25 + centrality_score * 0.25 + info_score * 0.2)
        return min(1.0, professional_focus)
    
    def _calculate_work_adaptability(self, community_cohesion: float, spectral_radius: float,
                                   topological_complexity: float, euler_characteristic: int) -> float:
        """Calculate work adaptability from fingerprint features (DMIT principle)"""
        # DMIT research shows: High community cohesion + spectral radius = work adaptability
        
        # Community cohesion contribution
        cohesion_score = min(1.0, community_cohesion)
        
        # Spectral radius contribution
        if spectral_radius > 0:
            spectral_score = min(1.0, spectral_radius / 10.0)
        else:
            spectral_score = 0.5
        
        # Topological complexity contribution
        complexity_score = min(1.0, topological_complexity)
        
        # Euler characteristic contribution (more negative = more complex = better work adaptability)
        if euler_characteristic < 0:
            euler_score = min(1.0, abs(euler_characteristic) / 10.0)
        else:
            euler_score = 0.3
        
        # Combine scores
        work_adaptability = (cohesion_score * 0.3 + spectral_score * 0.25 + complexity_score * 0.25 + euler_score * 0.2)
        return min(1.0, work_adaptability)
    
    def _calculate_productivity_patterns(self, tfrc: int, box_counting_dimension: float,
                                       h1_num_features: int, betti_1: int) -> float:
        """Calculate productivity patterns from fingerprint features (DMIT principle)"""
        # DMIT research shows: High ridge count + fractal dimension = productivity patterns
        
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
        
        # H1 features contribution (loops/holes - complexity in productivity patterns)
        h1_score = min(1.0, h1_num_features / 10.0)
        
        # Betti-1 contribution (productivity patterns loops)
        betti_score = min(1.0, betti_1 / 10.0)
        
        # Combine scores
        productivity_patterns = (ridge_score * 0.35 + fractal_score * 0.25 + h1_score * 0.25 + betti_score * 0.15)
        return min(1.0, productivity_patterns)
    
    def _calculate_work_consistency(self, pattern_regularity: float, lacunarity: float,
                                  ridge_continuity: float, std_intensity: float) -> float:
        """Calculate work consistency from fingerprint features (DMIT principle)"""
        # DMIT research shows: High pattern regularity + low lacunarity = work consistency
        
        # Pattern regularity contribution
        regularity_score = min(1.0, pattern_regularity)
        
        # Lacunarity contribution (lower lacunarity = more regular = better work consistency)
        lacunarity_score = max(0.0, 1.0 - lacunarity)
        
        # Ridge continuity contribution
        continuity_score = min(1.0, ridge_continuity)
        
        # Standard deviation contribution (lower variation = more consistent = better work consistency)
        if std_intensity > 0:
            std_score = max(0.0, 1.0 - (std_intensity / 100.0))
        else:
            std_score = 0.5
        
        # Combine scores
        work_consistency = (regularity_score * 0.3 + lacunarity_score * 0.25 + continuity_score * 0.25 + std_score * 0.2)
        return min(1.0, work_consistency)
    
    def _calculate_professional_behavior(self, ridge_uniformity: float, pattern_type: str,
                                       ridge_curvature: float, spectral_energy: float) -> float:
        """Calculate professional behavior from fingerprint features (DMIT principle)"""
        # DMIT research shows: High ridge uniformity + pattern type = professional behavior
        
        # Ridge uniformity contribution
        uniformity_score = min(1.0, ridge_uniformity)
        
        # Pattern type contribution
        pattern_weights = {
            'whorl': 0.8,      # Complex patterns indicate professional behavior
            'loop': 0.7,       # Good professional behavior
            'arch': 0.6,       # Moderate professional behavior
            'tented_arch': 0.65, # Slightly better than plain arch
            'composite': 0.75   # Complex professional behavior patterns
        }
        pattern_score = pattern_weights.get(pattern_type.lower(), 0.6)
        
        # Ridge curvature contribution
        curvature_score = min(1.0, ridge_curvature)
        
        # Spectral energy contribution
        energy_score = min(1.0, spectral_energy)
        
        # Combine scores
        professional_behavior = (uniformity_score * 0.3 + pattern_score * 0.25 + curvature_score * 0.25 + energy_score * 0.2)
        return min(1.0, professional_behavior)
    
    def _calculate_work_style_flexibility(self, spectral_centroid: float, spectral_rolloff: float,
                                        graph_density: float, topological_complexity: float) -> float:
        """Calculate work style flexibility from fingerprint features (DMIT principle)"""
        # DMIT research shows: High spectral features + graph complexity = work style flexibility
        
        # Spectral centroid contribution
        centroid_score = min(1.0, spectral_centroid)
        
        # Spectral rolloff contribution
        rolloff_score = min(1.0, spectral_rolloff)
        
        # Graph density contribution
        density_score = min(1.0, graph_density)
        
        # Topological complexity contribution
        complexity_score = min(1.0, topological_complexity)
        
        # Combine scores
        work_style_flexibility = (centroid_score * 0.3 + rolloff_score * 0.25 + density_score * 0.25 + complexity_score * 0.2)
        return min(1.0, work_style_flexibility)

    @staticmethod
    def classify_work_style_level(score: float) -> str:
        if score >= 0.85:
            return "Exceptional Work Style"
        elif score >= 0.75:
            return "High Work Style"
        elif score >= 0.65:
            return "Above Average Work Style"
        elif score >= 0.55:
            return "Average Work Style"
        else:
            return "Developing Work Style" 
