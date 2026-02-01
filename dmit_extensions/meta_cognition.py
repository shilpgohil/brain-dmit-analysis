from typing import Dict, Any
from .base import DMITExtensionBase

class MetaCognitionExtension(DMITExtensionBase):
    """
    Extension for analyzing Meta Cognition abilities from fingerprint features.
    Uses comprehensive DMIT scientific correlations between fingerprint patterns and meta cognition processes.
    """
    def analyze(self, features: Dict[str, Any]) -> Dict[str, Any]:
        # Extract comprehensive fingerprint features for meta cognition analysis
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
        
        # Calculate meta cognition abilities using comprehensive DMIT scientific correlations
        
        # 1. Self Awareness Analysis (DMIT Principle: High information dimension + entropy = self awareness)
        self_awareness = self._calculate_self_awareness(information_dimension, entropy, 
                                                      pattern_symmetry, spectral_entropy)
        
        # 2. Cognitive Monitoring Analysis (DMIT Principle: High correlation dimension + graph density = cognitive monitoring)
        cognitive_monitoring = self._calculate_cognitive_monitoring(correlation_dimension, graph_density, 
                                                                  betweenness_centrality, information_dimension)
        
        # 3. Learning Strategies Analysis (DMIT Principle: High ridge count + fractal complexity = learning strategies)
        learning_strategies = self._calculate_learning_strategies(tfrc, box_counting_dimension, 
                                                                h1_num_features, betti_1)
        
        # 4. Problem Solving Meta Analysis (DMIT Principle: High spectral radius + topological complexity = problem solving meta)
        problem_solving_meta = self._calculate_problem_solving_meta(spectral_radius, topological_complexity, 
                                                                  euler_characteristic, spectral_bandwidth)
        
        # 5. Decision Making Meta Analysis (DMIT Principle: High ridge density + clustering coefficient = decision making meta)
        decision_making_meta = self._calculate_decision_making_meta(ridge_density, clustering_coefficient, 
                                                                  modularity, ridge_thickness)
        
        # 6. Cognitive Control Analysis (DMIT Principle: High ridge uniformity + pattern type = cognitive control)
        cognitive_control = self._calculate_cognitive_control(ridge_uniformity, pattern_type, 
                                                            ridge_curvature, community_cohesion)
        
        # 7. Meta Optimization Analysis (DMIT Principle: High pattern regularity + low lacunarity = meta optimization)
        meta_optimization = self._calculate_meta_optimization(pattern_regularity, lacunarity, 
                                                            ridge_continuity, std_intensity)
        
        # 8. Meta Intelligence Analysis (DMIT Principle: High spectral features + graph complexity = meta intelligence)
        meta_intelligence = self._calculate_meta_intelligence(spectral_centroid, spectral_rolloff, 
                                                            graph_density, topological_complexity)
        
        # Overall meta cognition score (comprehensive weighted combination)
        meta_cognition_score = (
            self_awareness * 0.20 +                # Self awareness is fundamental
            cognitive_monitoring * 0.18 +          # Cognitive monitoring is crucial
            learning_strategies * 0.15 +           # Learning strategies is important
            problem_solving_meta * 0.15 +          # Problem solving meta is essential
            decision_making_meta * 0.12 +          # Decision making meta
            cognitive_control * 0.10 +             # Cognitive control
            meta_optimization * 0.07 +             # Meta optimization
            meta_intelligence * 0.03               # Meta intelligence
        )
        
        # Normalize to 0-1 range
        meta_cognition_score = max(0.0, min(1.0, meta_cognition_score))
        
        # Determine meta cognition style based on dominant features
        meta_styles = {
            'self_aware': self_awareness + meta_intelligence,
            'monitoring': cognitive_monitoring + cognitive_control,
            'strategic': learning_strategies + problem_solving_meta,
            'problem_solver': problem_solving_meta + decision_making_meta,
            'decision_maker': decision_making_meta + meta_optimization,
            'controlled': cognitive_control + self_awareness
        }
        primary_style = max(meta_styles.items(), key=lambda x: x[1])[0]
        
        return {
            'meta_cognition_score': meta_cognition_score,
            'primary_meta_style': primary_style,
            'self_awareness': self_awareness,
            'cognitive_monitoring': cognitive_monitoring,
            'learning_strategies': learning_strategies,
            'problem_solving_meta': problem_solving_meta,
            'decision_making_meta': decision_making_meta,
            'cognitive_control': cognitive_control,
            'meta_optimization': meta_optimization,
            'meta_intelligence': meta_intelligence,
            'awareness_control': self_awareness + cognitive_control,
            'strategic_monitoring': cognitive_monitoring + learning_strategies,
            'problem_decision': problem_solving_meta + decision_making_meta,
            'intelligent_meta': meta_intelligence + self_awareness,
            'optimized_meta': meta_optimization + cognitive_monitoring,
            'meta_profile': self.classify_meta_level(meta_cognition_score)
        }

    def _calculate_self_awareness(self, information_dimension: float, entropy: float,
                                pattern_symmetry: float, spectral_entropy: float) -> float:
        """Calculate self awareness from fingerprint features (DMIT principle)"""
        # DMIT research shows: High information dimension + entropy = self awareness
        
        # Information dimension contribution
        if 1.5 <= information_dimension <= 2.0:
            info_score = (information_dimension - 1.5) / 0.5
        else:
            info_score = 0.5
        
        # Entropy contribution (higher entropy = more complex self awareness)
        if entropy > 0:
            entropy_score = min(1.0, entropy / 8.0)  # Normalize to 0-1
        else:
            entropy_score = 0.5
        
        # Pattern symmetry contribution
        symmetry_score = min(1.0, pattern_symmetry)
        
        # Spectral entropy contribution
        spectral_score = min(1.0, spectral_entropy)
        
        # Combine scores
        self_awareness = (info_score * 0.35 + entropy_score * 0.25 + symmetry_score * 0.25 + spectral_score * 0.15)
        return min(1.0, self_awareness)
    
    def _calculate_cognitive_monitoring(self, correlation_dimension: float, graph_density: float,
                                      betweenness_centrality: float, information_dimension: float) -> float:
        """Calculate cognitive monitoring from fingerprint features (DMIT principle)"""
        # DMIT research shows: High correlation dimension + graph density = cognitive monitoring
        
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
        cognitive_monitoring = (corr_score * 0.3 + density_score * 0.25 + centrality_score * 0.25 + info_score * 0.2)
        return min(1.0, cognitive_monitoring)
    
    def _calculate_learning_strategies(self, tfrc: int, box_counting_dimension: float,
                                     h1_num_features: int, betti_1: int) -> float:
        """Calculate learning strategies from fingerprint features (DMIT principle)"""
        # DMIT research shows: High ridge count + fractal complexity = learning strategies
        
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
        
        # H1 features contribution (loops/holes - complexity in learning strategies)
        h1_score = min(1.0, h1_num_features / 10.0)
        
        # Betti-1 contribution (learning strategies loops)
        betti_score = min(1.0, betti_1 / 10.0)
        
        # Combine scores
        learning_strategies = (ridge_score * 0.35 + fractal_score * 0.25 + h1_score * 0.25 + betti_score * 0.15)
        return min(1.0, learning_strategies)
    
    def _calculate_problem_solving_meta(self, spectral_radius: float, topological_complexity: float,
                                      euler_characteristic: int, spectral_bandwidth: float) -> float:
        """Calculate problem solving meta from fingerprint features (DMIT principle)"""
        # DMIT research shows: High spectral radius + topological complexity = problem solving meta
        
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
        problem_solving_meta = (spectral_score * 0.3 + complexity_score * 0.25 + euler_score * 0.25 + bandwidth_score * 0.2)
        return min(1.0, problem_solving_meta)
    
    def _calculate_decision_making_meta(self, ridge_density: float, clustering_coefficient: float,
                                      modularity: float, ridge_thickness: float) -> float:
        """Calculate decision making meta from fingerprint features (DMIT principle)"""
        # DMIT research shows: High ridge density + clustering coefficient = decision making meta
        
        # Ridge density contribution
        density_score = min(1.0, ridge_density)
        
        # Clustering coefficient contribution
        clustering_score = min(1.0, clustering_coefficient)
        
        # Modularity contribution
        modularity_score = min(1.0, modularity)
        
        # Ridge thickness contribution
        thickness_score = min(1.0, ridge_thickness)
        
        # Combine scores
        decision_making_meta = (density_score * 0.3 + clustering_score * 0.25 + modularity_score * 0.25 + thickness_score * 0.2)
        return min(1.0, decision_making_meta)
    
    def _calculate_cognitive_control(self, ridge_uniformity: float, pattern_type: str,
                                   ridge_curvature: float, community_cohesion: float) -> float:
        """Calculate cognitive control from fingerprint features (DMIT principle)"""
        # DMIT research shows: High ridge uniformity + pattern type = cognitive control
        
        # Ridge uniformity contribution
        uniformity_score = min(1.0, ridge_uniformity)
        
        # Pattern type contribution
        pattern_weights = {
            'whorl': 0.8,      # Complex patterns indicate good cognitive control
            'loop': 0.7,       # Good cognitive control
            'arch': 0.6,       # Moderate cognitive control
            'tented_arch': 0.65, # Slightly better than plain arch
            'composite': 0.75   # Complex cognitive control patterns
        }
        pattern_score = pattern_weights.get(pattern_type.lower(), 0.6)
        
        # Ridge curvature contribution
        curvature_score = min(1.0, ridge_curvature)
        
        # Community cohesion contribution
        cohesion_score = min(1.0, community_cohesion)
        
        # Combine scores
        cognitive_control = (uniformity_score * 0.3 + pattern_score * 0.25 + curvature_score * 0.25 + cohesion_score * 0.2)
        return min(1.0, cognitive_control)
    
    def _calculate_meta_optimization(self, pattern_regularity: float, lacunarity: float,
                                   ridge_continuity: float, std_intensity: float) -> float:
        """Calculate meta optimization from fingerprint features (DMIT principle)"""
        # DMIT research shows: High pattern regularity + low lacunarity = meta optimization
        
        # Pattern regularity contribution
        regularity_score = min(1.0, pattern_regularity)
        
        # Lacunarity contribution (lower lacunarity = more regular = better meta optimization)
        lacunarity_score = max(0.0, 1.0 - lacunarity)
        
        # Ridge continuity contribution
        continuity_score = min(1.0, ridge_continuity)
        
        # Standard deviation contribution (lower variation = more consistent = better meta optimization)
        if std_intensity > 0:
            std_score = max(0.0, 1.0 - (std_intensity / 100.0))
        else:
            std_score = 0.5
        
        # Combine scores
        meta_optimization = (regularity_score * 0.3 + lacunarity_score * 0.25 + continuity_score * 0.25 + std_score * 0.2)
        return min(1.0, meta_optimization)
    
    def _calculate_meta_intelligence(self, spectral_centroid: float, spectral_rolloff: float,
                                   graph_density: float, topological_complexity: float) -> float:
        """Calculate meta intelligence from fingerprint features (DMIT principle)"""
        # DMIT research shows: High spectral features + graph complexity = meta intelligence
        
        # Spectral centroid contribution
        centroid_score = min(1.0, spectral_centroid)
        
        # Spectral rolloff contribution
        rolloff_score = min(1.0, spectral_rolloff)
        
        # Graph density contribution
        density_score = min(1.0, graph_density)
        
        # Topological complexity contribution
        complexity_score = min(1.0, topological_complexity)
        
        # Combine scores
        meta_intelligence = (centroid_score * 0.3 + rolloff_score * 0.25 + density_score * 0.25 + complexity_score * 0.2)
        return min(1.0, meta_intelligence)
    
    @staticmethod
    def classify_meta_level(score: float) -> str:
        """Classify meta cognition level based on score"""
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