from typing import Dict, Any
from .base import DMITExtensionBase

class DecisionMakingExtension(DMITExtensionBase):
    """
    Extension for analyzing Decision Making abilities from fingerprint features.
    Uses comprehensive DMIT scientific correlations between fingerprint patterns and decision-making processes.
    """
    def analyze(self, features: Dict[str, Any]) -> Dict[str, Any]:
        # Extract comprehensive fingerprint features for decision making analysis
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
        
        # Calculate decision making abilities using comprehensive DMIT scientific correlations
        
        # 1. Analytical Decision Making Analysis (DMIT Principle: High correlation dimension + graph density = analytical thinking)
        analytical_decision_making = self._calculate_analytical_decision_making(correlation_dimension, graph_density, 
                                                                              betweenness_centrality, information_dimension)
        
        # 2. Intuitive Decision Making Analysis (DMIT Principle: High information dimension + entropy = intuitive processing)
        intuitive_decision_making = self._calculate_intuitive_decision_making(information_dimension, entropy, 
                                                                            pattern_symmetry, spectral_entropy)
        
        # 3. Systematic Decision Making Analysis (DMIT Principle: High pattern regularity + low lacunarity = systematic approach)
        systematic_decision_making = self._calculate_systematic_decision_making(pattern_regularity, lacunarity, 
                                                                              ridge_continuity, std_intensity)
        
        # 4. Risk Assessment Analysis (DMIT Principle: High spectral radius + topological complexity = risk evaluation)
        risk_assessment = self._calculate_risk_assessment(spectral_radius, topological_complexity, 
                                                        euler_characteristic, spectral_bandwidth)
        
        # 5. Speed of Decision Making Analysis (DMIT Principle: High ridge density + clustering coefficient = quick processing)
        speed_of_decision_making = self._calculate_speed_of_decision_making(ridge_density, clustering_coefficient, 
                                                                          modularity, ridge_thickness)
        
        # 6. Decision Quality Analysis (DMIT Principle: High ridge count + fractal complexity = decision quality)
        decision_quality = self._calculate_decision_quality(tfrc, box_counting_dimension, 
                                                          h1_num_features, betti_1)
        
        # 7. Adaptability in Decision Making Analysis (DMIT Principle: High ridge uniformity + pattern type = adaptability)
        adaptability_in_decision_making = self._calculate_adaptability_in_decision_making(ridge_uniformity, pattern_type, 
                                                                                        ridge_curvature, community_cohesion)
        
        # 8. Strategic Decision Making Analysis (DMIT Principle: High spectral features + graph complexity = strategic thinking)
        strategic_decision_making = self._calculate_strategic_decision_making(spectral_centroid, spectral_rolloff, 
                                                                            graph_density, topological_complexity)
        
        # Overall decision making score (comprehensive weighted combination)
        decision_making_score = (
            analytical_decision_making * 0.20 +        # Analytical thinking is fundamental
            systematic_decision_making * 0.18 +        # Systematic approach is crucial
            decision_quality * 0.15 +                  # Decision quality is important
            risk_assessment * 0.15 +                   # Risk assessment is essential
            speed_of_decision_making * 0.12 +          # Speed of processing
            strategic_decision_making * 0.10 +         # Strategic thinking
            intuitive_decision_making * 0.07 +         # Intuitive processing
            adaptability_in_decision_making * 0.03     # Adaptability
        )
        
        # Normalize to 0-1 range
        decision_making_score = max(0.0, min(1.0, decision_making_score))
        
        # Determine decision making style based on dominant features
        decision_styles = {
            'analytical': analytical_decision_making + systematic_decision_making,
            'intuitive': intuitive_decision_making + speed_of_decision_making,
            'strategic': strategic_decision_making + risk_assessment,
            'systematic': systematic_decision_making + decision_quality,
            'adaptive': adaptability_in_decision_making + intuitive_decision_making,
            'balanced': (analytical_decision_making + intuitive_decision_making) / 2
        }
        primary_style = max(decision_styles.items(), key=lambda x: x[1])[0]
        
        return {
            'decision_making_score': decision_making_score,
            'primary_decision_style': primary_style,
            'analytical_decision_making': analytical_decision_making,
            'intuitive_decision_making': intuitive_decision_making,
            'systematic_decision_making': systematic_decision_making,
            'risk_assessment': risk_assessment,
            'speed_of_decision_making': speed_of_decision_making,
            'decision_quality': decision_quality,
            'adaptability_in_decision_making': adaptability_in_decision_making,
            'strategic_decision_making': strategic_decision_making,
            'logical_reasoning': analytical_decision_making + systematic_decision_making,
            'quick_thinking': speed_of_decision_making + intuitive_decision_making,
            'risk_management': risk_assessment + strategic_decision_making,
            'problem_solving': decision_quality + analytical_decision_making,
            'cognitive_flexibility': adaptability_in_decision_making + intuitive_decision_making,
            'decision_profile': self.classify_decision_level(decision_making_score)
        }

    def _calculate_analytical_decision_making(self, correlation_dimension: float, graph_density: float,
                                            betweenness_centrality: float, information_dimension: float) -> float:
        """Calculate analytical decision making from fingerprint features (DMIT principle)"""
        # DMIT research shows: High correlation dimension + graph density = analytical thinking
        
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
        analytical_decision_making = (corr_score * 0.3 + density_score * 0.25 + centrality_score * 0.25 + info_score * 0.2)
        return min(1.0, analytical_decision_making)
    
    def _calculate_intuitive_decision_making(self, information_dimension: float, entropy: float,
                                           pattern_symmetry: float, spectral_entropy: float) -> float:
        """Calculate intuitive decision making from fingerprint features (DMIT principle)"""
        # DMIT research shows: High information dimension + entropy = intuitive processing
        
        # Information dimension contribution
        if 1.5 <= information_dimension <= 2.0:
            info_score = (information_dimension - 1.5) / 0.5
        else:
            info_score = 0.5
        
        # Entropy contribution (higher entropy = more complex intuitive processing)
        if entropy > 0:
            entropy_score = min(1.0, entropy / 8.0)  # Normalize to 0-1
        else:
            entropy_score = 0.5
        
        # Pattern symmetry contribution
        symmetry_score = min(1.0, pattern_symmetry)
        
        # Spectral entropy contribution
        spectral_score = min(1.0, spectral_entropy)
        
        # Combine scores
        intuitive_decision_making = (info_score * 0.35 + entropy_score * 0.25 + symmetry_score * 0.25 + spectral_score * 0.15)
        return min(1.0, intuitive_decision_making)
    
    def _calculate_systematic_decision_making(self, pattern_regularity: float, lacunarity: float,
                                            ridge_continuity: float, std_intensity: float) -> float:
        """Calculate systematic decision making from fingerprint features (DMIT principle)"""
        # DMIT research shows: High pattern regularity + low lacunarity = systematic approach
        
        # Pattern regularity contribution
        regularity_score = min(1.0, pattern_regularity)
        
        # Lacunarity contribution (lower lacunarity = more regular = better systematic approach)
        lacunarity_score = max(0.0, 1.0 - lacunarity)
        
        # Ridge continuity contribution
        continuity_score = min(1.0, ridge_continuity)
        
        # Standard deviation contribution (lower variation = more consistent = better systematic approach)
        if std_intensity > 0:
            std_score = max(0.0, 1.0 - (std_intensity / 100.0))
        else:
            std_score = 0.5
        
        # Combine scores
        systematic_decision_making = (regularity_score * 0.3 + lacunarity_score * 0.25 + continuity_score * 0.25 + std_score * 0.2)
        return min(1.0, systematic_decision_making)
    
    def _calculate_risk_assessment(self, spectral_radius: float, topological_complexity: float,
                                 euler_characteristic: int, spectral_bandwidth: float) -> float:
        """Calculate risk assessment from fingerprint features (DMIT principle)"""
        # DMIT research shows: High spectral radius + topological complexity = risk evaluation
        
        # Spectral radius contribution
        if spectral_radius > 0:
            spectral_score = min(1.0, spectral_radius / 10.0)
        else:
            spectral_score = 0.5
        
        # Topological complexity contribution
        complexity_score = min(1.0, topological_complexity)
        
        # Euler characteristic contribution (more negative = more complex = better risk assessment)
        if euler_characteristic < 0:
            euler_score = min(1.0, abs(euler_characteristic) / 10.0)
        else:
            euler_score = 0.3
        
        # Spectral bandwidth contribution
        bandwidth_score = min(1.0, spectral_bandwidth)
        
        # Combine scores
        risk_assessment = (spectral_score * 0.3 + complexity_score * 0.25 + euler_score * 0.25 + bandwidth_score * 0.2)
        return min(1.0, risk_assessment)
    
    def _calculate_speed_of_decision_making(self, ridge_density: float, clustering_coefficient: float,
                                          modularity: float, ridge_thickness: float) -> float:
        """Calculate speed of decision making from fingerprint features (DMIT principle)"""
        # DMIT research shows: High ridge density + clustering coefficient = quick processing
        
        # Ridge density contribution
        density_score = min(1.0, ridge_density)
        
        # Clustering coefficient contribution
        clustering_score = min(1.0, clustering_coefficient)
        
        # Modularity contribution
        modularity_score = min(1.0, modularity)
        
        # Ridge thickness contribution
        thickness_score = min(1.0, ridge_thickness)
        
        # Combine scores
        speed_of_decision_making = (density_score * 0.3 + clustering_score * 0.25 + modularity_score * 0.25 + thickness_score * 0.2)
        return min(1.0, speed_of_decision_making)
    
    def _calculate_decision_quality(self, tfrc: int, box_counting_dimension: float,
                                  h1_num_features: int, betti_1: int) -> float:
        """Calculate decision quality from fingerprint features (DMIT principle)"""
        # DMIT research shows: High ridge count + fractal complexity = decision quality
        
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
        
        # H1 features contribution (loops/holes - complexity in decision quality)
        h1_score = min(1.0, h1_num_features / 10.0)
        
        # Betti-1 contribution (decision loops)
        betti_score = min(1.0, betti_1 / 10.0)
        
        # Combine scores
        decision_quality = (ridge_score * 0.35 + fractal_score * 0.25 + h1_score * 0.25 + betti_score * 0.15)
        return min(1.0, decision_quality)
    
    def _calculate_adaptability_in_decision_making(self, ridge_uniformity: float, pattern_type: str,
                                                 ridge_curvature: float, community_cohesion: float) -> float:
        """Calculate adaptability in decision making from fingerprint features (DMIT principle)"""
        # DMIT research shows: High ridge uniformity + pattern type = adaptability
        
        # Ridge uniformity contribution
        uniformity_score = min(1.0, ridge_uniformity)
        
        # Pattern type contribution
        pattern_weights = {
            'whorl': 0.8,      # Complex patterns indicate adaptability
            'loop': 0.7,       # Good adaptability
            'arch': 0.6,       # Moderate adaptability
            'tented_arch': 0.65, # Slightly better than plain arch
            'composite': 0.75   # Complex adaptability patterns
        }
        pattern_score = pattern_weights.get(pattern_type.lower(), 0.6)
        
        # Ridge curvature contribution
        curvature_score = min(1.0, ridge_curvature)
        
        # Community cohesion contribution
        cohesion_score = min(1.0, community_cohesion)
        
        # Combine scores
        adaptability_in_decision_making = (uniformity_score * 0.3 + pattern_score * 0.25 + curvature_score * 0.25 + cohesion_score * 0.2)
        return min(1.0, adaptability_in_decision_making)
    
    def _calculate_strategic_decision_making(self, spectral_centroid: float, spectral_rolloff: float,
                                           graph_density: float, topological_complexity: float) -> float:
        """Calculate strategic decision making from fingerprint features (DMIT principle)"""
        # DMIT research shows: High spectral features + graph complexity = strategic thinking
        
        # Spectral centroid contribution
        centroid_score = min(1.0, spectral_centroid)
        
        # Spectral rolloff contribution
        rolloff_score = min(1.0, spectral_rolloff)
        
        # Graph density contribution
        density_score = min(1.0, graph_density)
        
        # Topological complexity contribution
        complexity_score = min(1.0, topological_complexity)
        
        # Combine scores
        strategic_decision_making = (centroid_score * 0.3 + rolloff_score * 0.25 + density_score * 0.25 + complexity_score * 0.2)
        return min(1.0, strategic_decision_making)

    @staticmethod
    def classify_decision_level(score: float) -> str:
        if score >= 0.85:
            return "Exceptional Decision Making"
        elif score >= 0.75:
            return "High Decision Making"
        elif score >= 0.65:
            return "Above Average Decision Making"
        elif score >= 0.55:
            return "Average Decision Making"
        else:
            return "Developing Decision Making" 