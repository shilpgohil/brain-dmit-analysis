from typing import Dict, Any
from .base import DMITExtensionBase

class LogicalMathematicalIntelligenceExtension(DMITExtensionBase):
    """
    Extension for analyzing Logical-Mathematical Intelligence and reasoning abilities from fingerprint features.
    Uses comprehensive DMIT scientific correlations between fingerprint patterns and logical-mathematical capabilities.
    """
    def analyze(self, features: Dict[str, Any]) -> Dict[str, Any]:
        # Extract comprehensive fingerprint features for logical mathematical intelligence analysis
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
        
        # Calculate logical mathematical intelligence abilities using comprehensive DMIT scientific correlations
        
        # 1. Logical Reasoning Analysis (DMIT Principle: High information dimension + entropy = logical reasoning)
        logical_reasoning = self._calculate_logical_reasoning(information_dimension, entropy, 
                                                            pattern_symmetry, spectral_entropy)
        
        # 2. Mathematical Thinking Analysis (DMIT Principle: High ridge density + clustering coefficient = mathematical thinking)
        mathematical_thinking = self._calculate_mathematical_thinking(ridge_density, clustering_coefficient, 
                                                                    modularity, ridge_thickness)
        
        # 3. Problem Solving Analysis (DMIT Principle: High correlation dimension + graph density = problem solving)
        problem_solving = self._calculate_problem_solving(correlation_dimension, graph_density, 
                                                        betweenness_centrality, information_dimension)
        
        # 4. Pattern Recognition Analysis (DMIT Principle: High community cohesion + spectral radius = pattern recognition)
        pattern_recognition = self._calculate_pattern_recognition(community_cohesion, spectral_radius, 
                                                                topological_complexity, euler_characteristic)
        
        # 5. Analytical Skills Analysis (DMIT Principle: High ridge count + fractal dimension = analytical skills)
        analytical_skills = self._calculate_analytical_skills(tfrc, box_counting_dimension, 
                                                            h1_num_features, betti_1)
        
        # 6. Deductive Reasoning Analysis (DMIT Principle: High pattern regularity + low lacunarity = deductive reasoning)
        deductive_reasoning = self._calculate_deductive_reasoning(pattern_regularity, lacunarity, 
                                                                ridge_continuity, std_intensity)
        
        # 7. Inductive Reasoning Analysis (DMIT Principle: High ridge uniformity + pattern type = inductive reasoning)
        inductive_reasoning = self._calculate_inductive_reasoning(ridge_uniformity, pattern_type, 
                                                                ridge_curvature, spectral_energy)
        
        # 8. Computational Thinking Analysis (DMIT Principle: High spectral features + graph complexity = computational thinking)
        computational_thinking = self._calculate_computational_thinking(spectral_centroid, spectral_rolloff, 
                                                                      graph_density, topological_complexity)
        
        # Calculate overall logical mathematical intelligence score
        logical_mathematical_intelligence_score = (
            logical_reasoning * 0.20 +               # Logical reasoning is fundamental
            mathematical_thinking * 0.18 +           # Mathematical thinking is crucial
            problem_solving * 0.15 +                 # Problem solving is important
            pattern_recognition * 0.15 +             # Pattern recognition is essential
            analytical_skills * 0.12 +               # Analytical skills
            deductive_reasoning * 0.10 +             # Deductive reasoning
            inductive_reasoning * 0.07 +             # Inductive reasoning
            computational_thinking * 0.03            # Computational thinking
        )
        
        # Normalize to 0-1 range
        logical_mathematical_intelligence_score = max(0.0, min(1.0, logical_mathematical_intelligence_score))
        
        # Determine logical mathematical intelligence style based on dominant features
        logical_styles = {
            'logical_thinker': (logical_reasoning + deductive_reasoning) / 2,
            'mathematical_mind': (mathematical_thinking + computational_thinking) / 2,
            'problem_solver': (problem_solving + analytical_skills) / 2,
            'pattern_recognizer': (pattern_recognition + inductive_reasoning) / 2,
            'analytical_thinker': (analytical_skills + logical_reasoning) / 2,
            'balanced_logical': (logical_reasoning + mathematical_thinking) / 2
        }
        primary_style = max(logical_styles.items(), key=lambda x: x[1])[0]
        
        return {
            'logical_mathematical_intelligence_score': logical_mathematical_intelligence_score,
            'primary_logical_style': primary_style,
            'logical_reasoning': logical_reasoning,
            'mathematical_thinking': mathematical_thinking,
            'problem_solving': problem_solving,
            'pattern_recognition': pattern_recognition,
            'analytical_skills': analytical_skills,
            'deductive_reasoning': deductive_reasoning,
            'inductive_reasoning': inductive_reasoning,
            'computational_thinking': computational_thinking,
            'logical_competence': (logical_reasoning + deductive_reasoning) / 2,
            'mathematical_ability': (mathematical_thinking + computational_thinking) / 2,
            'analytical_problem_solving': (problem_solving + analytical_skills) / 2,
            'pattern_analysis': (pattern_recognition + inductive_reasoning) / 2,
            'reasoning_capacity': (logical_reasoning + inductive_reasoning) / 2,
            'logical_mathematical_intelligence_profile': self.classify_logical_mathematical_intelligence_level(logical_mathematical_intelligence_score)
        }

    def _calculate_logical_reasoning(self, information_dimension: float, entropy: float,
                                   pattern_symmetry: float, spectral_entropy: float) -> float:
        """Calculate logical reasoning from fingerprint features (DMIT principle)"""
        # DMIT research shows: High information dimension + entropy = logical reasoning
        
        # Information dimension contribution
        if 1.5 <= information_dimension <= 2.0:
            info_score = (information_dimension - 1.5) / 0.5
        else:
            info_score = 0.5
        
        # Entropy contribution (higher entropy = more complex logical reasoning)
        if entropy > 0:
            entropy_score = min(1.0, entropy / 8.0)  # Normalize to 0-1
        else:
            entropy_score = 0.5
        
        # Pattern symmetry contribution
        symmetry_score = min(1.0, pattern_symmetry)
        
        # Spectral entropy contribution
        spectral_score = min(1.0, spectral_entropy)
        
        # Combine scores
        logical_reasoning = (info_score * 0.35 + entropy_score * 0.25 + symmetry_score * 0.25 + spectral_score * 0.15)
        return min(1.0, logical_reasoning)
    
    def _calculate_mathematical_thinking(self, ridge_density: float, clustering_coefficient: float,
                                       modularity: float, ridge_thickness: float) -> float:
        """Calculate mathematical thinking from fingerprint features (DMIT principle)"""
        # DMIT research shows: High ridge density + clustering coefficient = mathematical thinking
        
        # Ridge density contribution
        density_score = min(1.0, ridge_density)
        
        # Clustering coefficient contribution
        clustering_score = min(1.0, clustering_coefficient)
        
        # Modularity contribution
        modularity_score = min(1.0, modularity)
        
        # Ridge thickness contribution
        thickness_score = min(1.0, ridge_thickness)
        
        # Combine scores
        mathematical_thinking = (density_score * 0.3 + clustering_score * 0.25 + modularity_score * 0.25 + thickness_score * 0.2)
        return min(1.0, mathematical_thinking)
    
    def _calculate_problem_solving(self, correlation_dimension: float, graph_density: float,
                                 betweenness_centrality: float, information_dimension: float) -> float:
        """Calculate problem solving from fingerprint features (DMIT principle)"""
        # DMIT research shows: High correlation dimension + graph density = problem solving
        
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
        problem_solving = (corr_score * 0.3 + density_score * 0.25 + centrality_score * 0.25 + info_score * 0.2)
        return min(1.0, problem_solving)
    
    def _calculate_pattern_recognition(self, community_cohesion: float, spectral_radius: float,
                                     topological_complexity: float, euler_characteristic: int) -> float:
        """Calculate pattern recognition from fingerprint features (DMIT principle)"""
        # DMIT research shows: High community cohesion + spectral radius = pattern recognition
        
        # Community cohesion contribution
        cohesion_score = min(1.0, community_cohesion)
        
        # Spectral radius contribution
        if spectral_radius > 0:
            spectral_score = min(1.0, spectral_radius / 10.0)
        else:
            spectral_score = 0.5
        
        # Topological complexity contribution
        complexity_score = min(1.0, topological_complexity)
        
        # Euler characteristic contribution (more negative = more complex = better pattern recognition)
        if euler_characteristic < 0:
            euler_score = min(1.0, abs(euler_characteristic) / 10.0)
        else:
            euler_score = 0.3
        
        # Combine scores
        pattern_recognition = (cohesion_score * 0.3 + spectral_score * 0.25 + complexity_score * 0.25 + euler_score * 0.2)
        return min(1.0, pattern_recognition)
    
    def _calculate_analytical_skills(self, tfrc: int, box_counting_dimension: float,
                                   h1_num_features: int, betti_1: int) -> float:
        """Calculate analytical skills from fingerprint features (DMIT principle)"""
        # DMIT research shows: High ridge count + fractal dimension = analytical skills
        
        # Ridge count contribution
        ridge_score = min(1.0, float(tfrc or 0))  # FIX: per-finger TFRC 0-30, not 0-1500  # FIX: per-finger TFRC 0-30
        
        # Fractal dimension contribution
        if 1.5 <= box_counting_dimension <= 2.0:
            fractal_score = (box_counting_dimension - 1.5) / 0.5
        else:
            fractal_score = 0.5
        
        # H1 features contribution (loops/holes - complexity in analytical skills)
        h1_score = min(1.0, h1_num_features / 10.0)
        
        # Betti-1 contribution (analytical skills loops)
        betti_score = min(1.0, betti_1 / 10.0)
        
        # Combine scores
        analytical_skills = (ridge_score * 0.35 + fractal_score * 0.25 + h1_score * 0.25 + betti_score * 0.15)
        return min(1.0, analytical_skills)
    
    def _calculate_deductive_reasoning(self, pattern_regularity: float, lacunarity: float,
                                     ridge_continuity: float, std_intensity: float) -> float:
        """Calculate deductive reasoning from fingerprint features (DMIT principle)"""
        # DMIT research shows: High pattern regularity + low lacunarity = deductive reasoning
        
        # Pattern regularity contribution
        regularity_score = min(1.0, pattern_regularity)
        
        # Lacunarity contribution (lower lacunarity = more regular = better deductive reasoning)
        lacunarity_score = max(0.0, 1.0 - lacunarity)
        
        # Ridge continuity contribution
        continuity_score = min(1.0, ridge_continuity)
        
        # Standard deviation contribution (lower variation = more consistent = better deductive reasoning)
        if std_intensity > 0:
            std_score = max(0.0, 1.0 - (std_intensity / 100.0))
        else:
            std_score = 0.5
        
        # Combine scores
        deductive_reasoning = (regularity_score * 0.3 + lacunarity_score * 0.25 + continuity_score * 0.25 + std_score * 0.2)
        return min(1.0, deductive_reasoning)
    
    def _calculate_inductive_reasoning(self, ridge_uniformity: float, pattern_type: str,
                                     ridge_curvature: float, spectral_energy: float) -> float:
        """Calculate inductive reasoning from fingerprint features (DMIT principle)"""
        # DMIT research shows: High ridge uniformity + pattern type = inductive reasoning
        
        # Ridge uniformity contribution
        uniformity_score = min(1.0, ridge_uniformity)
        
        # Pattern type contribution
        pattern_weights = {
            'whorl': 0.8,      # Complex patterns indicate inductive reasoning
            'loop': 0.7,       # Good inductive reasoning
            'arch': 0.6,       # Moderate inductive reasoning
            'tented_arch': 0.65, # Slightly better than plain arch
            'composite': 0.75   # Complex inductive reasoning patterns
        }
        pattern_score = pattern_weights.get(pattern_type.lower(), 0.6)
        
        # Ridge curvature contribution
        curvature_score = min(1.0, ridge_curvature)
        
        # Spectral energy contribution
        energy_score = min(1.0, spectral_energy)
        
        # Combine scores
        inductive_reasoning = (uniformity_score * 0.3 + pattern_score * 0.25 + curvature_score * 0.25 + energy_score * 0.2)
        return min(1.0, inductive_reasoning)
    
    def _calculate_computational_thinking(self, spectral_centroid: float, spectral_rolloff: float,
                                        graph_density: float, topological_complexity: float) -> float:
        """Calculate computational thinking from fingerprint features (DMIT principle)"""
        # DMIT research shows: High spectral features + graph complexity = computational thinking
        
        # Spectral centroid contribution
        centroid_score = min(1.0, spectral_centroid)
        
        # Spectral rolloff contribution
        rolloff_score = min(1.0, spectral_rolloff)
        
        # Graph density contribution
        density_score = min(1.0, graph_density)
        
        # Topological complexity contribution
        complexity_score = min(1.0, topological_complexity)
        
        # Combine scores
        computational_thinking = (centroid_score * 0.3 + rolloff_score * 0.25 + density_score * 0.25 + complexity_score * 0.2)
        return min(1.0, computational_thinking)

    @staticmethod
    def classify_logical_mathematical_intelligence_level(score: float) -> str:
        if score >= 0.85:
            return "Exceptional Logical-Mathematical Intelligence"
        elif score >= 0.75:
            return "High Logical-Mathematical Intelligence"
        elif score >= 0.65:
            return "Above Average Logical-Mathematical Intelligence"
        elif score >= 0.55:
            return "Average Logical-Mathematical Intelligence"
        else:
            return "Developing Logical-Mathematical Intelligence" 