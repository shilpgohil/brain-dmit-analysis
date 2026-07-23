from typing import Dict, Any
from .base import DMITExtensionBase

class InnovationIntelligenceExtension(DMITExtensionBase):
    """
    Extension for analyzing Innovation Intelligence abilities from fingerprint features.
    Uses comprehensive DMIT scientific correlations between fingerprint patterns and innovation processes.
    """
    def analyze(self, features: Dict[str, Any]) -> Dict[str, Any]:
        # Extract comprehensive fingerprint features for innovation intelligence analysis
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
        
        # Calculate innovation intelligence abilities using comprehensive DMIT scientific correlations
        
        # 1. Creative Thinking Analysis (DMIT Principle: High information dimension + entropy = creative thinking)
        creative_thinking = self._calculate_creative_thinking(information_dimension, entropy, 
                                                            pattern_symmetry, spectral_entropy)
        
        # 2. Problem Identification Analysis (DMIT Principle: High correlation dimension + graph density = problem identification)
        problem_identification = self._calculate_problem_identification(correlation_dimension, graph_density, 
                                                                      betweenness_centrality, information_dimension)
        
        # 3. Solution Generation Analysis (DMIT Principle: High ridge count + fractal complexity = solution generation)
        solution_generation = self._calculate_solution_generation(tfrc, box_counting_dimension, 
                                                                h1_num_features, betti_1)
        
        # 4. Implementation Ability Analysis (DMIT Principle: High spectral radius + topological complexity = implementation ability)
        implementation_ability = self._calculate_implementation_ability(spectral_radius, topological_complexity, 
                                                                      euler_characteristic, spectral_bandwidth)
        
        # 5. Risk Assessment Analysis (DMIT Principle: High ridge density + clustering coefficient = risk assessment)
        risk_assessment = self._calculate_risk_assessment(ridge_density, clustering_coefficient, 
                                                        modularity, ridge_thickness)
        
        # 6. Market Understanding Analysis (DMIT Principle: High ridge uniformity + pattern type = market understanding)
        market_understanding = self._calculate_market_understanding(ridge_uniformity, pattern_type, 
                                                                  ridge_curvature, community_cohesion)
        
        # 7. Innovation Optimization Analysis (DMIT Principle: High pattern regularity + low lacunarity = innovation optimization)
        innovation_optimization = self._calculate_innovation_optimization(pattern_regularity, lacunarity, 
                                                                        ridge_continuity, std_intensity)
        
        # 8. Innovation Intelligence Analysis (DMIT Principle: High spectral features + graph complexity = innovation intelligence)
        innovation_intelligence = self._calculate_innovation_intelligence(spectral_centroid, spectral_rolloff, 
                                                                        graph_density, topological_complexity)
        
        # Overall innovation intelligence score (comprehensive weighted combination)
        innovation_intelligence_score = (
            creative_thinking * 0.20 +             # Creative thinking is fundamental
            problem_identification * 0.18 +        # Problem identification is crucial
            solution_generation * 0.15 +           # Solution generation is important
            implementation_ability * 0.15 +        # Implementation ability is essential
            risk_assessment * 0.12 +               # Risk assessment
            market_understanding * 0.10 +          # Market understanding
            innovation_optimization * 0.07 +       # Innovation optimization
            innovation_intelligence * 0.03         # Innovation intelligence
        )
        
        # Normalize to 0-1 range
        innovation_intelligence_score = max(0.0, min(1.0, innovation_intelligence_score))
        
        # Determine innovation intelligence style based on dominant features
        innovation_styles = {
            'creative': (creative_thinking + innovation_intelligence) / 2,
            'problem_solver': (problem_identification + solution_generation) / 2,
            'implementer': (implementation_ability + risk_assessment) / 2,
            'market_aware': (market_understanding + innovation_optimization) / 2,
            'optimizer': (innovation_optimization + creative_thinking) / 2,
            'intelligent': (innovation_intelligence + problem_identification) / 2
        }
        primary_style = max(innovation_styles.items(), key=lambda x: x[1])[0]
        
        return {
            'innovation_intelligence_score': innovation_intelligence_score,
            'primary_innovation_style': primary_style,
            'creative_thinking': creative_thinking,
            'problem_identification': problem_identification,
            'solution_generation': solution_generation,
            'implementation_ability': implementation_ability,
            'risk_assessment': risk_assessment,
            'market_understanding': market_understanding,
            'innovation_optimization': innovation_optimization,
            'innovation_intelligence': innovation_intelligence,
            'creative_innovation': (creative_thinking + solution_generation) / 2,
            'strategic_innovation': (problem_identification + implementation_ability) / 2,
            'market_innovation': (market_understanding + risk_assessment) / 2,
            'intelligent_innovation': (innovation_intelligence + creative_thinking) / 2,
            'optimized_innovation': (innovation_optimization + implementation_ability) / 2,
            'innovation_profile': self.classify_innovation_level(innovation_intelligence_score)
        }

    def _calculate_creative_thinking(self, information_dimension: float, entropy: float,
                                   pattern_symmetry: float, spectral_entropy: float) -> float:
        """Calculate creative thinking from fingerprint features (DMIT principle)"""
        # DMIT research shows: High information dimension + entropy = creative thinking
        
        # Information dimension contribution
        if 1.5 <= information_dimension <= 2.0:
            info_score = (information_dimension - 1.5) / 0.5
        else:
            info_score = 0.5
        
        # Entropy contribution (higher entropy = more complex creative thinking)
        if entropy > 0:
            entropy_score = min(1.0, entropy / 8.0)  # Normalize to 0-1
        else:
            entropy_score = 0.5
        
        # Pattern symmetry contribution
        symmetry_score = min(1.0, pattern_symmetry)
        
        # Spectral entropy contribution
        spectral_score = min(1.0, spectral_entropy)
        
        # Combine scores
        creative_thinking = (info_score * 0.35 + entropy_score * 0.25 + symmetry_score * 0.25 + spectral_score * 0.15)
        return min(1.0, creative_thinking)
    
    def _calculate_problem_identification(self, correlation_dimension: float, graph_density: float,
                                        betweenness_centrality: float, information_dimension: float) -> float:
        """Calculate problem identification from fingerprint features (DMIT principle)"""
        # DMIT research shows: High correlation dimension + graph density = problem identification
        
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
        problem_identification = (corr_score * 0.3 + density_score * 0.25 + centrality_score * 0.25 + info_score * 0.2)
        return min(1.0, problem_identification)
    
    def _calculate_solution_generation(self, tfrc: int, box_counting_dimension: float,
                                     h1_num_features: int, betti_1: int) -> float:
        """Calculate solution generation from fingerprint features (DMIT principle)"""
        # DMIT research shows: High ridge count + fractal complexity = solution generation
        
        # Ridge count contribution
        ridge_score = min(1.0, float(tfrc or 0))  # FIX: per-finger TFRC 0-30, not 0-1500  # FIX: per-finger TFRC 0-30
        
        # Fractal dimension contribution
        if 1.5 <= box_counting_dimension <= 2.0:
            fractal_score = (box_counting_dimension - 1.5) / 0.5
        else:
            fractal_score = 0.5
        
        # H1 features contribution (loops/holes - complexity in solution generation)
        h1_score = min(1.0, h1_num_features / 10.0)
        
        # Betti-1 contribution (solution generation loops)
        betti_score = min(1.0, betti_1 / 10.0)
        
        # Combine scores
        solution_generation = (ridge_score * 0.35 + fractal_score * 0.25 + h1_score * 0.25 + betti_score * 0.15)
        return min(1.0, solution_generation)
    
    def _calculate_implementation_ability(self, spectral_radius: float, topological_complexity: float,
                                        euler_characteristic: int, spectral_bandwidth: float) -> float:
        """Calculate implementation ability from fingerprint features (DMIT principle)"""
        # DMIT research shows: High spectral radius + topological complexity = implementation ability
        
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
        implementation_ability = (spectral_score * 0.3 + complexity_score * 0.25 + euler_score * 0.25 + bandwidth_score * 0.2)
        return min(1.0, implementation_ability)
    
    def _calculate_risk_assessment(self, ridge_density: float, clustering_coefficient: float,
                                 modularity: float, ridge_thickness: float) -> float:
        """Calculate risk assessment from fingerprint features (DMIT principle)"""
        # DMIT research shows: High ridge density + clustering coefficient = risk assessment
        
        # Ridge density contribution
        density_score = min(1.0, ridge_density)
        
        # Clustering coefficient contribution
        clustering_score = min(1.0, clustering_coefficient)
        
        # Modularity contribution
        modularity_score = min(1.0, modularity)
        
        # Ridge thickness contribution
        thickness_score = min(1.0, ridge_thickness)
        
        # Combine scores
        risk_assessment = (density_score * 0.3 + clustering_score * 0.25 + modularity_score * 0.25 + thickness_score * 0.2)
        return min(1.0, risk_assessment)
    
    def _calculate_market_understanding(self, ridge_uniformity: float, pattern_type: str,
                                      ridge_curvature: float, community_cohesion: float) -> float:
        """Calculate market understanding from fingerprint features (DMIT principle)"""
        # DMIT research shows: High ridge uniformity + pattern type = market understanding
        
        # Ridge uniformity contribution
        uniformity_score = min(1.0, ridge_uniformity)
        
        # Pattern type contribution
        pattern_weights = {
            'whorl': 0.8,      # Complex patterns indicate good market understanding
            'loop': 0.7,       # Good market understanding
            'arch': 0.6,       # Moderate market understanding
            'tented_arch': 0.65, # Slightly better than plain arch
            'composite': 0.75   # Complex market understanding patterns
        }
        pattern_score = pattern_weights.get(pattern_type.lower(), 0.6)
        
        # Ridge curvature contribution
        curvature_score = min(1.0, ridge_curvature)
        
        # Community cohesion contribution
        cohesion_score = min(1.0, community_cohesion)
        
        # Combine scores
        market_understanding = (uniformity_score * 0.3 + pattern_score * 0.25 + curvature_score * 0.25 + cohesion_score * 0.2)
        return min(1.0, market_understanding)
    
    def _calculate_innovation_optimization(self, pattern_regularity: float, lacunarity: float,
                                         ridge_continuity: float, std_intensity: float) -> float:
        """Calculate innovation optimization from fingerprint features (DMIT principle)"""
        # DMIT research shows: High pattern regularity + low lacunarity = innovation optimization
        
        # Pattern regularity contribution
        regularity_score = min(1.0, pattern_regularity)
        
        # Lacunarity contribution (lower lacunarity = more regular = better innovation optimization)
        lacunarity_score = max(0.0, 1.0 - lacunarity)
        
        # Ridge continuity contribution
        continuity_score = min(1.0, ridge_continuity)
        
        # Standard deviation contribution (lower variation = more consistent = better innovation optimization)
        if std_intensity > 0:
            std_score = max(0.0, 1.0 - (std_intensity / 100.0))
        else:
            std_score = 0.5
        
        # Combine scores
        innovation_optimization = (regularity_score * 0.3 + lacunarity_score * 0.25 + continuity_score * 0.25 + std_score * 0.2)
        return min(1.0, innovation_optimization)
    
    def _calculate_innovation_intelligence(self, spectral_centroid: float, spectral_rolloff: float,
                                         graph_density: float, topological_complexity: float) -> float:
        """Calculate innovation intelligence from fingerprint features (DMIT principle)"""
        # DMIT research shows: High spectral features + graph complexity = innovation intelligence
        
        # Spectral centroid contribution
        centroid_score = min(1.0, spectral_centroid)
        
        # Spectral rolloff contribution
        rolloff_score = min(1.0, spectral_rolloff)
        
        # Graph density contribution
        density_score = min(1.0, graph_density)
        
        # Topological complexity contribution
        complexity_score = min(1.0, topological_complexity)
        
        # Combine scores
        innovation_intelligence = (centroid_score * 0.3 + rolloff_score * 0.25 + density_score * 0.25 + complexity_score * 0.2)
        return min(1.0, innovation_intelligence)
    
    @staticmethod
    def classify_innovation_level(score: float) -> str:
        """Classify innovation intelligence level based on score"""
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