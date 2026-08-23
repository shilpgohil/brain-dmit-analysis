from typing import Dict, Any
from .base import DMITExtensionBase

class VisualIntelligenceExtension(DMITExtensionBase):
    """
    Extension for analyzing Visual Intelligence and artistic abilities from fingerprint features.
    Uses comprehensive DMIT scientific correlations between fingerprint patterns and visual capabilities.
    """
    def analyze(self, features: Dict[str, Any]) -> Dict[str, Any]:
        # Extract comprehensive fingerprint features for visual intelligence analysis
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
        
        # Calculate visual intelligence abilities using comprehensive DMIT scientific correlations
        
        # 1. Visual Processing Analysis (DMIT Principle: High information dimension + entropy = visual processing)
        visual_processing = self._calculate_visual_processing(information_dimension, entropy, 
                                                            pattern_symmetry, spectral_entropy)
        
        # 2. Artistic Perception Analysis (DMIT Principle: High ridge density + clustering coefficient = artistic perception)
        artistic_perception = self._calculate_artistic_perception(ridge_density, clustering_coefficient, 
                                                                modularity, ridge_thickness)
        
        # 3. Visual Creativity Analysis (DMIT Principle: High correlation dimension + graph density = visual creativity)
        visual_creativity = self._calculate_visual_creativity(correlation_dimension, graph_density, 
                                                            betweenness_centrality, information_dimension)
        
        # 4. Aesthetic Judgment Analysis (DMIT Principle: High community cohesion + spectral radius = aesthetic judgment)
        aesthetic_judgment = self._calculate_aesthetic_judgment(community_cohesion, spectral_radius, 
                                                              topological_complexity, euler_characteristic)
        
        # 5. Visual Memory Analysis (DMIT Principle: High ridge count + fractal dimension = visual memory)
        visual_memory = self._calculate_visual_memory(tfrc, box_counting_dimension, 
                                                    h1_num_features, betti_1)
        
        # 6. Color Sensitivity Analysis (DMIT Principle: High pattern regularity + low lacunarity = color sensitivity)
        color_sensitivity = self._calculate_color_sensitivity(pattern_regularity, lacunarity, 
                                                            ridge_continuity, std_intensity)
        
        # 7. Design Ability Analysis (DMIT Principle: High ridge uniformity + pattern type = design ability)
        design_ability = self._calculate_design_ability(ridge_uniformity, pattern_type, 
                                                      ridge_curvature, spectral_energy)
        
        # 8. Visual Adaptability Analysis (DMIT Principle: High spectral features + graph complexity = visual adaptability)
        visual_adaptability = self._calculate_visual_adaptability(spectral_centroid, spectral_rolloff, 
                                                                graph_density, topological_complexity)
        
        # Calculate overall visual intelligence score
        visual_intelligence_score = (
            visual_processing * 0.20 +               # Visual processing is fundamental
            artistic_perception * 0.18 +             # Artistic perception is crucial
            visual_creativity * 0.15 +               # Visual creativity is important
            aesthetic_judgment * 0.15 +              # Aesthetic judgment is essential
            visual_memory * 0.12 +                   # Visual memory
            color_sensitivity * 0.10 +               # Color sensitivity
            design_ability * 0.07 +                  # Design ability
            visual_adaptability * 0.03               # Visual adaptability
        )
        
        # Normalize to 0-1 range
        visual_intelligence_score = max(0.0, min(1.0, visual_intelligence_score))
        
        # Determine visual intelligence style based on dominant features
        visual_styles = {
            'visual_processor': (visual_processing + visual_memory) / 2,
            'artistic_perceiver': (artistic_perception + color_sensitivity) / 2,
            'creative_visualizer': (visual_creativity + design_ability) / 2,
            'aesthetic_judge': (aesthetic_judgment + visual_adaptability) / 2,
            'design_thinker': (design_ability + visual_creativity) / 2,
            'balanced_visual': (visual_processing + artistic_perception) / 2
        }
        primary_style = max(visual_styles.items(), key=lambda x: x[1])[0]
        
        return {
            'visual_intelligence_score': visual_intelligence_score,
            'primary_visual_style': primary_style,
            'visual_processing': visual_processing,
            'artistic_perception': artistic_perception,
            'visual_creativity': visual_creativity,
            'aesthetic_judgment': aesthetic_judgment,
            'visual_memory': visual_memory,
            'color_sensitivity': color_sensitivity,
            'design_ability': design_ability,
            'visual_adaptability': visual_adaptability,
            'processing_capacity': (visual_processing + visual_memory) / 2,
            'perception_capacity': (artistic_perception + color_sensitivity) / 2,
            'creativity_capacity': (visual_creativity + design_ability) / 2,
            'aesthetic_capacity': (aesthetic_judgment + visual_adaptability) / 2,
            'visual_effectiveness': (visual_processing + artistic_perception) / 2,
            'visual_intelligence_profile': self.classify_visual_intelligence_level(visual_intelligence_score)
        }

    def _calculate_visual_processing(self, information_dimension: float, entropy: float,
                                   pattern_symmetry: float, spectral_entropy: float) -> float:
        """Calculate visual processing from fingerprint features (DMIT principle)"""
        # DMIT research shows: High information dimension + entropy = visual processing
        
        # Information dimension contribution
        if 1.5 <= information_dimension <= 2.0:
            info_score = (information_dimension - 1.5) / 0.5
        else:
            info_score = 0.5
        
        # Entropy contribution (higher entropy = more complex visual processing)
        if entropy > 0:
            entropy_score = min(1.0, entropy / 8.0)  # Normalize to 0-1
        else:
            entropy_score = 0.5
        
        # Pattern symmetry contribution
        symmetry_score = min(1.0, pattern_symmetry)
        
        # Spectral entropy contribution
        spectral_score = min(1.0, spectral_entropy)
        
        # Combine scores
        visual_processing = (info_score * 0.35 + entropy_score * 0.25 + symmetry_score * 0.25 + spectral_score * 0.15)
        return min(1.0, visual_processing)
    
    def _calculate_artistic_perception(self, ridge_density: float, clustering_coefficient: float,
                                     modularity: float, ridge_thickness: float) -> float:
        """Calculate artistic perception from fingerprint features (DMIT principle)"""
        # DMIT research shows: High ridge density + clustering coefficient = artistic perception
        
        # Ridge density contribution
        density_score = min(1.0, ridge_density)
        
        # Clustering coefficient contribution
        clustering_score = min(1.0, clustering_coefficient)
        
        # Modularity contribution
        modularity_score = min(1.0, modularity)
        
        # Ridge thickness contribution
        thickness_score = min(1.0, ridge_thickness)
        
        # Combine scores
        artistic_perception = (density_score * 0.3 + clustering_score * 0.25 + modularity_score * 0.25 + thickness_score * 0.2)
        return min(1.0, artistic_perception)
    
    def _calculate_visual_creativity(self, correlation_dimension: float, graph_density: float,
                                   betweenness_centrality: float, information_dimension: float) -> float:
        """Calculate visual creativity from fingerprint features (DMIT principle)"""
        # DMIT research shows: High correlation dimension + graph density = visual creativity
        
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
        visual_creativity = (corr_score * 0.3 + density_score * 0.25 + centrality_score * 0.25 + info_score * 0.2)
        return min(1.0, visual_creativity)
    
    def _calculate_aesthetic_judgment(self, community_cohesion: float, spectral_radius: float,
                                    topological_complexity: float, euler_characteristic: int) -> float:
        """Calculate aesthetic judgment from fingerprint features (DMIT principle)"""
        # DMIT research shows: High community cohesion + spectral radius = aesthetic judgment
        
        # Community cohesion contribution
        cohesion_score = min(1.0, community_cohesion)
        
        # Spectral radius contribution
        if spectral_radius > 0:
            spectral_score = min(1.0, spectral_radius / 10.0)
        else:
            spectral_score = 0.5
        
        # Topological complexity contribution
        complexity_score = min(1.0, topological_complexity)
        
        # Euler characteristic contribution (more negative = more complex = better aesthetic judgment)
        if euler_characteristic < 0:
            euler_score = min(1.0, abs(euler_characteristic) / 10.0)
        else:
            euler_score = 0.3
        
        # Combine scores
        aesthetic_judgment = (cohesion_score * 0.3 + spectral_score * 0.25 + complexity_score * 0.25 + euler_score * 0.2)
        return min(1.0, aesthetic_judgment)
    
    def _calculate_visual_memory(self, tfrc: int, box_counting_dimension: float,
                               h1_num_features: int, betti_1: int) -> float:
        """Calculate visual memory from fingerprint features (DMIT principle)"""
        # DMIT research shows: High ridge count + fractal dimension = visual memory
        
        # Ridge count contribution
        ridge_score = min(1.0, float(tfrc or 0))  # FIX: per-finger TFRC 0-30, not 0-1500  # FIX: per-finger TFRC 0-30
        
        # Fractal dimension contribution
        if 1.5 <= box_counting_dimension <= 2.0:
            fractal_score = (box_counting_dimension - 1.5) / 0.5
        else:
            fractal_score = 0.5
        
        # H1 features contribution (loops/holes - complexity in visual memory)
        h1_score = min(1.0, h1_num_features / 10.0)
        
        # Betti-1 contribution (visual memory loops)
        betti_score = min(1.0, betti_1 / 10.0)
        
        # Combine scores
        visual_memory = (ridge_score * 0.35 + fractal_score * 0.25 + h1_score * 0.25 + betti_score * 0.15)
        return min(1.0, visual_memory)
    
    def _calculate_color_sensitivity(self, pattern_regularity: float, lacunarity: float,
                                   ridge_continuity: float, std_intensity: float) -> float:
        """Calculate color sensitivity from fingerprint features (DMIT principle)"""
        # DMIT research shows: High pattern regularity + low lacunarity = color sensitivity
        
        # Pattern regularity contribution
        regularity_score = min(1.0, pattern_regularity)
        
        # Lacunarity contribution (lower lacunarity = more regular = better color sensitivity)
        lacunarity_score = max(0.0, 1.0 - lacunarity)
        
        # Ridge continuity contribution
        continuity_score = min(1.0, ridge_continuity)
        
        # Standard deviation contribution (lower variation = more consistent = better color sensitivity)
        if std_intensity > 0:
            std_score = max(0.0, 1.0 - (std_intensity / 100.0))
        else:
            std_score = 0.5
        
        # Combine scores
        color_sensitivity = (regularity_score * 0.3 + lacunarity_score * 0.25 + continuity_score * 0.25 + std_score * 0.2)
        return min(1.0, color_sensitivity)
    
    def _calculate_design_ability(self, ridge_uniformity: float, pattern_type: str,
                                ridge_curvature: float, spectral_energy: float) -> float:
        """Calculate design ability from fingerprint features (DMIT principle)"""
        # DMIT research shows: High ridge uniformity + pattern type = design ability
        
        # Ridge uniformity contribution
        uniformity_score = min(1.0, ridge_uniformity)
        
        # Pattern type contribution
        pattern_weights = {
            'whorl': 0.8,      # Complex patterns indicate design ability
            'loop': 0.7,       # Good design ability
            'arch': 0.6,       # Moderate design ability
            'tented_arch': 0.65, # Slightly better than plain arch
            'composite': 0.75   # Complex design ability patterns
        }
        pattern_score = pattern_weights.get(pattern_type.lower(), 0.6)
        
        # Ridge curvature contribution
        curvature_score = min(1.0, ridge_curvature)
        
        # Spectral energy contribution
        energy_score = min(1.0, spectral_energy)
        
        # Combine scores
        design_ability = (uniformity_score * 0.3 + pattern_score * 0.25 + curvature_score * 0.25 + energy_score * 0.2)
        return min(1.0, design_ability)
    
    def _calculate_visual_adaptability(self, spectral_centroid: float, spectral_rolloff: float,
                                     graph_density: float, topological_complexity: float) -> float:
        """Calculate visual adaptability from fingerprint features (DMIT principle)"""
        # DMIT research shows: High spectral features + graph complexity = visual adaptability
        
        # Spectral centroid contribution
        centroid_score = min(1.0, spectral_centroid)
        
        # Spectral rolloff contribution
        rolloff_score = min(1.0, spectral_rolloff)
        
        # Graph density contribution
        density_score = min(1.0, graph_density)
        
        # Topological complexity contribution
        complexity_score = min(1.0, topological_complexity)
        
        # Combine scores
        visual_adaptability = (centroid_score * 0.3 + rolloff_score * 0.25 + density_score * 0.25 + complexity_score * 0.2)
        return min(1.0, visual_adaptability)


    def _calculate_result(self, tfrc: int, box_counting_dimension: float,
                         h1_num_features: int, betti_1: int) -> float:
        """Calculate result from fingerprint features"""
        # This is a fallback method for compatibility
        return self._calculate_visual_memory(tfrc, box_counting_dimension, h1_num_features, betti_1)

    @staticmethod
    def classify_visual_intelligence_level(score: float) -> str:
        if score >= 0.85:
            return "Exceptional Visual Intelligence"
        elif score >= 0.75:
            return "High Visual Intelligence"
        elif score >= 0.65:
            return "Above Average Visual Intelligence"
        elif score >= 0.55:
            return "Average Visual Intelligence"
        else:
            return "Developing Visual Intelligence" 