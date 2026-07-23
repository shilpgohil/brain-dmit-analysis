from typing import Dict, Any
from .base import DMITExtensionBase

class CognitiveLoadExtension(DMITExtensionBase):
    """
    Extension for analyzing Cognitive Load capacity and management from fingerprint features.
    Uses comprehensive DMIT scientific correlations between fingerprint patterns and cognitive processing abilities.
    """
    def analyze(self, features: Dict[str, Any]) -> Dict[str, Any]:
        # Extract comprehensive fingerprint features for cognitive load analysis
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
        
        # Calculate cognitive load capacities using comprehensive DMIT scientific correlations
        
        # 1. Working Memory Capacity Analysis (DMIT Principle: High information dimension + entropy = working memory)
        working_memory_capacity = self._calculate_working_memory_capacity(information_dimension, entropy, 
                                                                        pattern_symmetry, spectral_entropy)
        
        # 2. Processing Speed Analysis (DMIT Principle: High ridge density + clustering coefficient = processing speed)
        processing_speed = self._calculate_processing_speed(ridge_density, clustering_coefficient, 
                                                          modularity, ridge_thickness)
        
        # 3. Attention Capacity Analysis (DMIT Principle: High correlation dimension + graph density = attention span)
        attention_capacity = self._calculate_attention_capacity(correlation_dimension, graph_density, 
                                                              betweenness_centrality, information_dimension)
        
        # 4. Cognitive Flexibility Analysis (DMIT Principle: High community cohesion + spectral radius = flexibility)
        cognitive_flexibility = self._calculate_cognitive_flexibility(community_cohesion, spectral_radius, 
                                                                    topological_complexity, euler_characteristic)
        
        # 5. Mental Endurance Analysis (DMIT Principle: High ridge count + fractal dimension = endurance)
        mental_endurance = self._calculate_mental_endurance(tfrc, box_counting_dimension, 
                                                          h1_num_features, betti_1)
        
        # 6. Cognitive Efficiency Analysis (DMIT Principle: High pattern regularity + low lacunarity = efficiency)
        cognitive_efficiency = self._calculate_cognitive_efficiency(pattern_regularity, lacunarity, 
                                                                  ridge_continuity, std_intensity)
        
        # 7. Multitasking Capacity Analysis (DMIT Principle: High ridge uniformity + pattern type = multitasking)
        multitasking_capacity = self._calculate_multitasking_capacity(ridge_uniformity, pattern_type, 
                                                                    ridge_curvature, spectral_energy)
        
        # 8. Cognitive Recovery Analysis (DMIT Principle: High spectral features + graph complexity = recovery)
        cognitive_recovery = self._calculate_cognitive_recovery(spectral_centroid, spectral_rolloff, 
                                                              graph_density, topological_complexity)
        
        # Calculate overall cognitive load management score
        cognitive_load_management_score = (
            working_memory_capacity * 0.20 +         # Working memory is fundamental
            processing_speed * 0.18 +                # Processing speed is crucial
            attention_capacity * 0.15 +              # Attention capacity is important
            cognitive_flexibility * 0.15 +           # Cognitive flexibility is essential
            mental_endurance * 0.12 +                # Mental endurance
            cognitive_efficiency * 0.10 +            # Cognitive efficiency
            multitasking_capacity * 0.07 +           # Multitasking capacity
            cognitive_recovery * 0.03                # Cognitive recovery
        )
        
        # Normalize to 0-1 range
        cognitive_load_management_score = max(0.0, min(1.0, cognitive_load_management_score))
        
        # Determine cognitive load style based on dominant features
        cognitive_styles = {
            'high_capacity': (working_memory_capacity + attention_capacity) / 2,
            'fast_processor': (processing_speed + cognitive_efficiency) / 2,
            'flexible_thinker': (cognitive_flexibility + multitasking_capacity) / 2,
            'endurance_focused': (mental_endurance + cognitive_recovery) / 2,
            'efficient_processor': (cognitive_efficiency + processing_speed) / 2,
            'balanced_cognitive': (working_memory_capacity + attention_capacity) / 2
        }
        primary_style = max(cognitive_styles.items(), key=lambda x: x[1])[0]
        
        return {
            'cognitive_load_management_score': cognitive_load_management_score,
            'primary_cognitive_style': primary_style,
            'working_memory_capacity': working_memory_capacity,
            'processing_speed': processing_speed,
            'attention_capacity': attention_capacity,
            'cognitive_flexibility': cognitive_flexibility,
            'mental_endurance': mental_endurance,
            'cognitive_efficiency': cognitive_efficiency,
            'multitasking_capacity': multitasking_capacity,
            'cognitive_recovery': cognitive_recovery,
            'information_processing': (working_memory_capacity + processing_speed) / 2,
            'attention_management': (attention_capacity + cognitive_flexibility) / 2,
            'mental_stamina': (mental_endurance + cognitive_recovery) / 2,
            'cognitive_optimization': (cognitive_efficiency + multitasking_capacity) / 2,
            'load_handling_capacity': (working_memory_capacity + mental_endurance) / 2,
            'cognitive_load_profile': self.classify_cognitive_load_level(cognitive_load_management_score)
        }

    def _calculate_working_memory_capacity(self, information_dimension: float, entropy: float,
                                         pattern_symmetry: float, spectral_entropy: float) -> float:
        """Calculate working memory capacity from fingerprint features (DMIT principle)"""
        # DMIT research shows: High information dimension + entropy = working memory capacity
        
        # Information dimension contribution
        if 1.5 <= information_dimension <= 2.0:
            info_score = (information_dimension - 1.5) / 0.5
        else:
            info_score = 0.5
        
        # Entropy contribution (higher entropy = more complex working memory)
        if entropy > 0:
            entropy_score = min(1.0, entropy / 8.0)  # Normalize to 0-1
        else:
            entropy_score = 0.5
        
        # Pattern symmetry contribution
        symmetry_score = min(1.0, pattern_symmetry)
        
        # Spectral entropy contribution
        spectral_score = min(1.0, spectral_entropy)
        
        # Combine scores
        working_memory_capacity = (info_score * 0.35 + entropy_score * 0.25 + symmetry_score * 0.25 + spectral_score * 0.15)
        return min(1.0, working_memory_capacity)
    
    def _calculate_processing_speed(self, ridge_density: float, clustering_coefficient: float,
                                  modularity: float, ridge_thickness: float) -> float:
        """Calculate processing speed from fingerprint features (DMIT principle)"""
        # DMIT research shows: High ridge density + clustering coefficient = processing speed
        
        # Ridge density contribution
        density_score = min(1.0, ridge_density)
        
        # Clustering coefficient contribution
        clustering_score = min(1.0, clustering_coefficient)
        
        # Modularity contribution
        modularity_score = min(1.0, modularity)
        
        # Ridge thickness contribution
        thickness_score = min(1.0, ridge_thickness)
        
        # Combine scores
        processing_speed = (density_score * 0.3 + clustering_score * 0.25 + modularity_score * 0.25 + thickness_score * 0.2)
        return min(1.0, processing_speed)
    
    def _calculate_attention_capacity(self, correlation_dimension: float, graph_density: float,
                                    betweenness_centrality: float, information_dimension: float) -> float:
        """Calculate attention capacity from fingerprint features (DMIT principle)"""
        # DMIT research shows: High correlation dimension + graph density = attention span
        
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
        attention_capacity = (corr_score * 0.3 + density_score * 0.25 + centrality_score * 0.25 + info_score * 0.2)
        return min(1.0, attention_capacity)
    
    def _calculate_cognitive_flexibility(self, community_cohesion: float, spectral_radius: float,
                                       topological_complexity: float, euler_characteristic: int) -> float:
        """Calculate cognitive flexibility from fingerprint features (DMIT principle)"""
        # DMIT research shows: High community cohesion + spectral radius = cognitive flexibility
        
        # Community cohesion contribution
        cohesion_score = min(1.0, community_cohesion)
        
        # Spectral radius contribution
        if spectral_radius > 0:
            spectral_score = min(1.0, spectral_radius / 10.0)
        else:
            spectral_score = 0.5
        
        # Topological complexity contribution
        complexity_score = min(1.0, topological_complexity)
        
        # Euler characteristic contribution (more negative = more complex = better flexibility)
        if euler_characteristic < 0:
            euler_score = min(1.0, abs(euler_characteristic) / 10.0)
        else:
            euler_score = 0.3
        
        # Combine scores
        cognitive_flexibility = (cohesion_score * 0.3 + spectral_score * 0.25 + complexity_score * 0.25 + euler_score * 0.2)
        return min(1.0, cognitive_flexibility)
    
    def _calculate_mental_endurance(self, tfrc: int, box_counting_dimension: float,
                                  h1_num_features: int, betti_1: int) -> float:
        """Calculate mental endurance from fingerprint features (DMIT principle)"""
        # DMIT research shows: High ridge count + fractal dimension = mental endurance
        
        # Ridge count contribution
        ridge_score = min(1.0, float(tfrc or 0))  # FIX: per-finger TFRC 0-30, not 0-1500  # FIX: per-finger TFRC 0-30
        
        # Fractal dimension contribution
        if 1.5 <= box_counting_dimension <= 2.0:
            fractal_score = (box_counting_dimension - 1.5) / 0.5
        else:
            fractal_score = 0.5
        
        # H1 features contribution (loops/holes - complexity in endurance)
        h1_score = min(1.0, h1_num_features / 10.0)
        
        # Betti-1 contribution (endurance loops)
        betti_score = min(1.0, betti_1 / 10.0)
        
        # Combine scores
        mental_endurance = (ridge_score * 0.35 + fractal_score * 0.25 + h1_score * 0.25 + betti_score * 0.15)
        return min(1.0, mental_endurance)
    
    def _calculate_cognitive_efficiency(self, pattern_regularity: float, lacunarity: float,
                                      ridge_continuity: float, std_intensity: float) -> float:
        """Calculate cognitive efficiency from fingerprint features (DMIT principle)"""
        # DMIT research shows: High pattern regularity + low lacunarity = cognitive efficiency
        
        # Pattern regularity contribution
        regularity_score = min(1.0, pattern_regularity)
        
        # Lacunarity contribution (lower lacunarity = more regular = better efficiency)
        lacunarity_score = max(0.0, 1.0 - lacunarity)
        
        # Ridge continuity contribution
        continuity_score = min(1.0, ridge_continuity)
        
        # Standard deviation contribution (lower variation = more consistent = better efficiency)
        if std_intensity > 0:
            std_score = max(0.0, 1.0 - (std_intensity / 100.0))
        else:
            std_score = 0.5
        
        # Combine scores
        cognitive_efficiency = (regularity_score * 0.3 + lacunarity_score * 0.25 + continuity_score * 0.25 + std_score * 0.2)
        return min(1.0, cognitive_efficiency)
    
    def _calculate_multitasking_capacity(self, ridge_uniformity: float, pattern_type: str,
                                       ridge_curvature: float, spectral_energy: float) -> float:
        """Calculate multitasking capacity from fingerprint features (DMIT principle)"""
        # DMIT research shows: High ridge uniformity + pattern type = multitasking ability
        
        # Ridge uniformity contribution
        uniformity_score = min(1.0, ridge_uniformity)
        
        # Pattern type contribution
        pattern_weights = {
            'whorl': 0.8,      # Complex patterns indicate multitasking
            'loop': 0.7,       # Good multitasking
            'arch': 0.6,       # Moderate multitasking
            'tented_arch': 0.65, # Slightly better than plain arch
            'composite': 0.75   # Complex multitasking patterns
        }
        pattern_score = pattern_weights.get(pattern_type.lower(), 0.6)
        
        # Ridge curvature contribution
        curvature_score = min(1.0, ridge_curvature)
        
        # Spectral energy contribution
        energy_score = min(1.0, spectral_energy)
        
        # Combine scores
        multitasking_capacity = (uniformity_score * 0.3 + pattern_score * 0.25 + curvature_score * 0.25 + energy_score * 0.2)
        return min(1.0, multitasking_capacity)
    
    def _calculate_cognitive_recovery(self, spectral_centroid: float, spectral_rolloff: float,
                                    graph_density: float, topological_complexity: float) -> float:
        """Calculate cognitive recovery from fingerprint features (DMIT principle)"""
        # DMIT research shows: High spectral features + graph complexity = cognitive recovery
        
        # Spectral centroid contribution
        centroid_score = min(1.0, spectral_centroid)
        
        # Spectral rolloff contribution
        rolloff_score = min(1.0, spectral_rolloff)
        
        # Graph density contribution
        density_score = min(1.0, graph_density)
        
        # Topological complexity contribution
        complexity_score = min(1.0, topological_complexity)
        
        # Combine scores
        cognitive_recovery = (centroid_score * 0.3 + rolloff_score * 0.25 + density_score * 0.25 + complexity_score * 0.2)
        return min(1.0, cognitive_recovery)

    @staticmethod
    def classify_cognitive_load_level(score: float) -> str:
        if score >= 0.85:
            return "Exceptional Cognitive Load Management"
        elif score >= 0.75:
            return "High Cognitive Load Management"
        elif score >= 0.65:
            return "Above Average Cognitive Load Management"
        elif score >= 0.55:
            return "Average Cognitive Load Management"
        else:
            return "Developing Cognitive Load Management" 