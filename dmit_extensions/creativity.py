from typing import Dict, Any
from .base import DMITExtensionBase

class CreativityExtension(DMITExtensionBase):
    """
    Extension for analyzing Creativity abilities from fingerprint features.
    Uses comprehensive DMIT scientific correlations between fingerprint patterns and creative processes.
    """
    def analyze(self, features: Dict[str, Any]) -> Dict[str, Any]:
        # Extract comprehensive fingerprint features for creativity analysis
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
        
        # Calculate creativity abilities using comprehensive DMIT scientific correlations
        
        # 1. Divergent Thinking Analysis (DMIT Principle: High information dimension + entropy = divergent thinking)
        divergent_thinking = self._calculate_divergent_thinking(information_dimension, entropy, 
                                                              pattern_symmetry, spectral_entropy)
        
        # 2. Convergent Thinking Analysis (DMIT Principle: High correlation dimension + graph density = convergent thinking)
        convergent_thinking = self._calculate_convergent_thinking(correlation_dimension, graph_density, 
                                                                betweenness_centrality, information_dimension)
        
        # 3. Originality Analysis (DMIT Principle: High fractal complexity + topological complexity = originality)
        originality = self._calculate_originality(fractal_complexity, topological_complexity, 
                                                euler_characteristic, spectral_radius)
        
        # 4. Flexibility Analysis (DMIT Principle: High ridge uniformity + pattern type = flexibility)
        flexibility = self._calculate_flexibility(ridge_uniformity, pattern_type, 
                                                ridge_curvature, community_cohesion)
        
        # 5. Fluency Analysis (DMIT Principle: High ridge density + clustering coefficient = fluency)
        fluency = self._calculate_fluency(ridge_density, clustering_coefficient, 
                                        modularity, ridge_thickness)
        
        # 6. Elaboration Analysis (DMIT Principle: High ridge count + fractal dimension = elaboration)
        elaboration = self._calculate_elaboration(tfrc, box_counting_dimension, 
                                                h1_num_features, betti_1)
        
        # 7. Innovation Analysis (DMIT Principle: High spectral features + graph complexity = innovation)
        innovation = self._calculate_innovation(spectral_centroid, spectral_rolloff, 
                                              graph_density, topological_complexity)
        
        # 8. Artistic Creativity Analysis (DMIT Principle: High pattern irregularity + spectral bandwidth = artistic creativity)
        artistic_creativity = self._calculate_artistic_creativity(pattern_regularity, spectral_bandwidth, 
                                                                lacunarity, std_intensity)
        
        # Overall creativity score (comprehensive weighted combination)
        creativity_score = (
            divergent_thinking * 0.20 +              # Divergent thinking is fundamental
            originality * 0.18 +                     # Originality is crucial
            flexibility * 0.15 +                     # Flexibility is important
            convergent_thinking * 0.15 +             # Convergent thinking is essential
            fluency * 0.12 +                         # Fluency
            elaboration * 0.10 +                     # Elaboration
            innovation * 0.07 +                      # Innovation
            artistic_creativity * 0.03               # Artistic creativity
        )
        
        # Normalize to 0-1 range
        creativity_score = max(0.0, min(1.0, creativity_score))
        
        # Determine creativity style based on dominant features
        creativity_styles = {
            'divergent': divergent_thinking + flexibility,
            'convergent': convergent_thinking + elaboration,
            'original': originality + innovation,
            'artistic': artistic_creativity + divergent_thinking,
            'innovative': innovation + convergent_thinking,
            'balanced': (divergent_thinking + convergent_thinking) / 2
        }
        primary_style = max(creativity_styles.items(), key=lambda x: x[1])[0]
        
        return {
            'creativity_score': creativity_score,
            'primary_creativity_style': primary_style,
            'divergent_thinking': divergent_thinking,
            'convergent_thinking': convergent_thinking,
            'originality': originality,
            'flexibility': flexibility,
            'fluency': fluency,
            'elaboration': elaboration,
            'innovation': innovation,
            'artistic_creativity': artistic_creativity,
            'creative_problem_solving': divergent_thinking + convergent_thinking,
            'creative_expression': artistic_creativity + fluency,
            'creative_adaptability': flexibility + innovation,
            'creative_depth': elaboration + originality,
            'creative_flow': fluency + divergent_thinking,
            'creativity_profile': self.classify_creativity_level(creativity_score)
        }

    def _calculate_divergent_thinking(self, information_dimension: float, entropy: float,
                                    pattern_symmetry: float, spectral_entropy: float) -> float:
        """Calculate divergent thinking from fingerprint features (DMIT principle)"""
        # DMIT research shows: High information dimension + entropy = divergent thinking
        
        # Information dimension contribution
        if 1.5 <= information_dimension <= 2.0:
            info_score = (information_dimension - 1.5) / 0.5
        else:
            info_score = 0.5
        
        # Entropy contribution (higher entropy = more complex divergent thinking)
        if entropy > 0:
            entropy_score = min(1.0, entropy / 8.0)  # Normalize to 0-1
        else:
            entropy_score = 0.5
        
        # Pattern symmetry contribution
        symmetry_score = min(1.0, pattern_symmetry)
        
        # Spectral entropy contribution
        spectral_score = min(1.0, spectral_entropy)
        
        # Combine scores
        divergent_thinking = (info_score * 0.35 + entropy_score * 0.25 + symmetry_score * 0.25 + spectral_score * 0.15)
        return min(1.0, divergent_thinking)
    
    def _calculate_convergent_thinking(self, correlation_dimension: float, graph_density: float,
                                     betweenness_centrality: float, information_dimension: float) -> float:
        """Calculate convergent thinking from fingerprint features (DMIT principle)"""
        # DMIT research shows: High correlation dimension + graph density = convergent thinking
        
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
        convergent_thinking = (corr_score * 0.3 + density_score * 0.25 + centrality_score * 0.25 + info_score * 0.2)
        return min(1.0, convergent_thinking)
    
    def _calculate_originality(self, fractal_complexity: float, topological_complexity: float,
                             euler_characteristic: int, spectral_radius: float) -> float:
        """Calculate originality from fingerprint features (DMIT principle)"""
        # DMIT research shows: High fractal complexity + topological complexity = originality
        
        # Fractal complexity contribution
        complexity_score = min(1.0, fractal_complexity)
        
        # Topological complexity contribution
        topological_score = min(1.0, topological_complexity)
        
        # Euler characteristic contribution (more negative = more complex = more original)
        if euler_characteristic < 0:
            euler_score = min(1.0, abs(euler_characteristic) / 10.0)
        else:
            euler_score = 0.3
        
        # Spectral radius contribution
        if spectral_radius > 0:
            spectral_score = min(1.0, spectral_radius / 10.0)
        else:
            spectral_score = 0.5
        
        # Combine scores
        originality = (complexity_score * 0.3 + topological_score * 0.25 + euler_score * 0.25 + spectral_score * 0.2)
        return min(1.0, originality)
    
    def _calculate_flexibility(self, ridge_uniformity: float, pattern_type: str,
                             ridge_curvature: float, community_cohesion: float) -> float:
        """Calculate flexibility from fingerprint features (DMIT principle)"""
        # DMIT research shows: High ridge uniformity + pattern type = flexibility
        
        # Ridge uniformity contribution
        uniformity_score = min(1.0, ridge_uniformity)
        
        # Pattern type contribution
        pattern_weights = {
            'whorl': 0.8,      # Complex patterns indicate flexibility
            'loop': 0.7,       # Good flexibility
            'arch': 0.6,       # Moderate flexibility
            'tented_arch': 0.65, # Slightly better than plain arch
            'composite': 0.75   # Complex flexibility patterns
        }
        pattern_score = pattern_weights.get(pattern_type.lower(), 0.6)
        
        # Ridge curvature contribution
        curvature_score = min(1.0, ridge_curvature)
        
        # Community cohesion contribution
        cohesion_score = min(1.0, community_cohesion)
        
        # Combine scores
        flexibility = (uniformity_score * 0.3 + pattern_score * 0.25 + curvature_score * 0.25 + cohesion_score * 0.2)
        return min(1.0, flexibility)
    
    def _calculate_fluency(self, ridge_density: float, clustering_coefficient: float,
                         modularity: float, ridge_thickness: float) -> float:
        """Calculate fluency from fingerprint features (DMIT principle)"""
        # DMIT research shows: High ridge density + clustering coefficient = fluency
        
        # Ridge density contribution
        density_score = min(1.0, ridge_density)
        
        # Clustering coefficient contribution
        clustering_score = min(1.0, clustering_coefficient)
        
        # Modularity contribution
        modularity_score = min(1.0, modularity)
        
        # Ridge thickness contribution
        thickness_score = min(1.0, ridge_thickness)
        
        # Combine scores
        fluency = (density_score * 0.3 + clustering_score * 0.25 + modularity_score * 0.25 + thickness_score * 0.2)
        return min(1.0, fluency)
    
    def _calculate_elaboration(self, tfrc: int, box_counting_dimension: float,
                             h1_num_features: int, betti_1: int) -> float:
        """Calculate elaboration from fingerprint features (DMIT principle)"""
        # DMIT research shows: High ridge count + fractal dimension = elaboration
        
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
        
        # H1 features contribution (loops/holes - complexity in elaboration)
        h1_score = min(1.0, h1_num_features / 10.0)
        
        # Betti-1 contribution (elaboration loops)
        betti_score = min(1.0, betti_1 / 10.0)
        
        # Combine scores
        elaboration = (ridge_score * 0.35 + fractal_score * 0.25 + h1_score * 0.25 + betti_score * 0.15)
        return min(1.0, elaboration)
    
    def _calculate_innovation(self, spectral_centroid: float, spectral_rolloff: float,
                            graph_density: float, topological_complexity: float) -> float:
        """Calculate innovation from fingerprint features (DMIT principle)"""
        # DMIT research shows: High spectral features + graph complexity = innovation
        
        # Spectral centroid contribution
        centroid_score = min(1.0, spectral_centroid)
        
        # Spectral rolloff contribution
        rolloff_score = min(1.0, spectral_rolloff)
        
        # Graph density contribution
        density_score = min(1.0, graph_density)
        
        # Topological complexity contribution
        complexity_score = min(1.0, topological_complexity)
        
        # Combine scores
        innovation = (centroid_score * 0.3 + rolloff_score * 0.25 + density_score * 0.25 + complexity_score * 0.2)
        return min(1.0, innovation)
    
    def _calculate_artistic_creativity(self, pattern_regularity: float, spectral_bandwidth: float,
                                     lacunarity: float, std_intensity: float) -> float:
        """Calculate artistic creativity from fingerprint features (DMIT principle)"""
        # DMIT research shows: High pattern irregularity + spectral bandwidth = artistic creativity
        
        # Pattern irregularity contribution (lower regularity = more artistic)
        irregularity_score = max(0.0, 1.0 - pattern_regularity)
        
        # Spectral bandwidth contribution
        bandwidth_score = min(1.0, spectral_bandwidth)
        
        # Lacunarity contribution (higher lacunarity = more artistic)
        lacunarity_score = min(1.0, lacunarity)
        
        # Standard deviation contribution (higher variation = more artistic)
        if std_intensity > 0:
            std_score = min(1.0, std_intensity / 100.0)
        else:
            std_score = 0.5
        
        # Combine scores
        artistic_creativity = (irregularity_score * 0.3 + bandwidth_score * 0.25 + lacunarity_score * 0.25 + std_score * 0.2)
        return min(1.0, artistic_creativity)

    @staticmethod
    def classify_creativity_level(score: float) -> str:
        if score >= 0.85:
            return "Exceptional Creativity"
        elif score >= 0.75:
            return "High Creativity"
        elif score >= 0.65:
            return "Above Average Creativity"
        elif score >= 0.55:
            return "Average Creativity"
        else:
            return "Developing Creativity" 
