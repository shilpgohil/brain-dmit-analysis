from typing import Dict, Any
from .base import DMITExtensionBase

class AttentionFocusExtension(DMITExtensionBase):
    """
    Extension for analyzing Attention and Focus abilities from fingerprint features.
    Uses comprehensive DMIT scientific correlations between fingerprint patterns and attention processes.
    """
    def analyze(self, features: Dict[str, Any]) -> Dict[str, Any]:
        # Extract comprehensive fingerprint features for attention focus analysis
        # Ridge count and density features
        tfrc = features.get('tfrc', 0)  # Total Fingerprint Ridge Count
        ridge_density = features.get('ridge_density', 0.0)
        ridge_continuity = features.get('ridge_continuity', 0.0)
        ridge_uniformity = features.get('ridge_uniformity', 0.0)
        ridge_thickness = features.get('mean_ridge_thickness', 0.0)
        ridge_orientation = features.get('mean_ridge_orientation', 0.0)
        
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
        
        # Calculate attention focus abilities using comprehensive DMIT scientific correlations
        
        # 1. Sustained Attention Analysis (DMIT Principle: High pattern regularity + low lacunarity = sustained focus)
        sustained_attention = self._calculate_sustained_attention(pattern_regularity, lacunarity, 
                                                                ridge_continuity, std_intensity)
        
        # 2. Selective Attention Analysis (DMIT Principle: High correlation dimension + graph density = selective focus)
        selective_attention = self._calculate_selective_attention(correlation_dimension, graph_density, 
                                                                betweenness_centrality, information_dimension)
        
        # 3. Divided Attention Analysis (DMIT Principle: High spectral radius + topological complexity = divided focus)
        divided_attention = self._calculate_divided_attention(spectral_radius, topological_complexity, 
                                                            euler_characteristic, spectral_bandwidth)
        
        # 4. Attention Span Analysis (DMIT Principle: High TFRC + fractal complexity = attention span)
        attention_span = self._calculate_attention_span(tfrc, box_counting_dimension, 
                                                      h1_num_features, betti_1)
        
        # 5. Focus Quality Analysis (DMIT Principle: High ridge density + clustering coefficient = focus quality)
        focus_quality = self._calculate_focus_quality(ridge_density, clustering_coefficient, 
                                                    modularity, ridge_thickness)
        
        # 6. Attention Control Analysis (DMIT Principle: High ridge uniformity + pattern type = attention control)
        attention_control = self._calculate_attention_control(ridge_uniformity, pattern_type, 
                                                            ridge_orientation, community_cohesion)
        
        # 7. Cognitive Load Management Analysis (DMIT Principle: High spectral features + graph complexity = load management)
        cognitive_load_management = self._calculate_cognitive_load_management(spectral_centroid, spectral_rolloff, 
                                                                            graph_density, topological_complexity)
        
        # 8. Attention Flexibility Analysis (DMIT Principle: High information dimension + entropy = attention flexibility)
        attention_flexibility = self._calculate_attention_flexibility(information_dimension, entropy, 
                                                                    pattern_symmetry, spectral_entropy)
        
        # Overall attention focus score (comprehensive weighted combination)
        attention_focus_score = (
            sustained_attention * 0.20 +              # Sustained attention is fundamental
            selective_attention * 0.18 +              # Selective attention is crucial
            focus_quality * 0.15 +                    # Focus quality is important
            attention_span * 0.15 +                   # Attention span is essential
            attention_control * 0.12 +                # Attention control
            cognitive_load_management * 0.10 +        # Cognitive load management
            divided_attention * 0.07 +                # Divided attention
            attention_flexibility * 0.03              # Attention flexibility
        )
        
        # Normalize to 0-1 range
        attention_focus_score = max(0.0, min(1.0, attention_focus_score))
        
        # Determine attention focus style based on dominant features
        attention_styles = {
            'sustained': sustained_attention + focus_quality,
            'selective': selective_attention + attention_control,
            'flexible': attention_flexibility + divided_attention,
            'intense': focus_quality + attention_span,
            'adaptive': attention_control + cognitive_load_management,
            'balanced': (sustained_attention + selective_attention) / 2
        }
        primary_style = max(attention_styles.items(), key=lambda x: x[1])[0]
        
        return {
            'attention_focus_score': attention_focus_score,
            'primary_attention_style': primary_style,
            'sustained_attention': sustained_attention,
            'selective_attention': selective_attention,
            'divided_attention': divided_attention,
            'attention_span': attention_span,
            'focus_quality': focus_quality,
            'attention_control': attention_control,
            'cognitive_load_management': cognitive_load_management,
            'attention_flexibility': attention_flexibility,
            'concentration_ability': sustained_attention + focus_quality,
            'task_switching': attention_flexibility + divided_attention,
            'mental_endurance': attention_span + cognitive_load_management,
            'focus_stability': attention_control + sustained_attention,
            'attention_efficiency': selective_attention + focus_quality,
            'attention_profile': self.classify_attention_level(attention_focus_score)
        }

    def _calculate_sustained_attention(self, pattern_regularity: float, lacunarity: float,
                                     ridge_continuity: float, std_intensity: float) -> float:
        """Calculate sustained attention from fingerprint features (DMIT principle)"""
        # DMIT research shows: High pattern regularity + low lacunarity = sustained focus
        
        # Pattern regularity contribution
        regularity_score = min(1.0, pattern_regularity)
        
        # Lacunarity contribution (lower lacunarity = more regular = better sustained attention)
        lacunarity_score = max(0.0, 1.0 - lacunarity)
        
        # Ridge continuity contribution
        continuity_score = min(1.0, ridge_continuity)
        
        # Standard deviation contribution (lower variation = more consistent = better sustained attention)
        if std_intensity > 0:
            std_score = max(0.0, 1.0 - (std_intensity / 100.0))
        else:
            std_score = 0.5
        
        # Combine scores
        sustained_attention = (regularity_score * 0.3 + lacunarity_score * 0.25 + continuity_score * 0.25 + std_score * 0.2)
        return min(1.0, sustained_attention)
    
    def _calculate_selective_attention(self, correlation_dimension: float, graph_density: float,
                                     betweenness_centrality: float, information_dimension: float) -> float:
        """Calculate selective attention from fingerprint features (DMIT principle)"""
        # DMIT research shows: High correlation dimension + graph density = selective focus
        
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
        selective_attention = (corr_score * 0.3 + density_score * 0.25 + centrality_score * 0.25 + info_score * 0.2)
        return min(1.0, selective_attention)
    
    def _calculate_divided_attention(self, spectral_radius: float, topological_complexity: float,
                                   euler_characteristic: int, spectral_bandwidth: float) -> float:
        """Calculate divided attention from fingerprint features (DMIT principle)"""
        # DMIT research shows: High spectral radius + topological complexity = divided focus
        
        # Spectral radius contribution
        if spectral_radius > 0:
            spectral_score = min(1.0, spectral_radius / 10.0)
        else:
            spectral_score = 0.5
        
        # Topological complexity contribution
        complexity_score = min(1.0, topological_complexity)
        
        # Euler characteristic contribution (more negative = more complex = better divided attention)
        if euler_characteristic < 0:
            euler_score = min(1.0, abs(euler_characteristic) / 10.0)
        else:
            euler_score = 0.3
        
        # Spectral bandwidth contribution
        bandwidth_score = min(1.0, spectral_bandwidth)
        
        # Combine scores
        divided_attention = (spectral_score * 0.3 + complexity_score * 0.25 + euler_score * 0.25 + bandwidth_score * 0.2)
        return min(1.0, divided_attention)
    
    def _calculate_attention_span(self, tfrc: int, box_counting_dimension: float,
                                h1_num_features: int, betti_1: int) -> float:
        """Calculate attention span from fingerprint features (DMIT principle)"""
        # DMIT research shows: High TFRC + fractal complexity = attention span
        
        # TFRC contribution
        if tfrc > 0:
            ridge_score = min(1.0, tfrc / 1500.0)
        else:
            ridge_score = 0.0
        
        # Fractal dimension contribution
        if 1.5 <= box_counting_dimension <= 2.0:
            fractal_score = (box_counting_dimension - 1.5) / 0.5
        else:
            fractal_score = 0.5
        
        # H1 features contribution (loops/holes - complexity in attention span)
        h1_score = min(1.0, h1_num_features / 10.0)
        
        # Betti-1 contribution (attention loops)
        betti_score = min(1.0, betti_1 / 10.0)
        
        # Combine scores
        attention_span = (ridge_score * 0.35 + fractal_score * 0.25 + h1_score * 0.25 + betti_score * 0.15)
        return min(1.0, attention_span)
    
    def _calculate_focus_quality(self, ridge_density: float, clustering_coefficient: float,
                               modularity: float, ridge_thickness: float) -> float:
        """Calculate focus quality from fingerprint features (DMIT principle)"""
        # DMIT research shows: High ridge density + clustering coefficient = focus quality
        
        # Ridge density contribution
        density_score = min(1.0, ridge_density)
        
        # Clustering coefficient contribution
        clustering_score = min(1.0, clustering_coefficient)
        
        # Modularity contribution
        modularity_score = min(1.0, modularity)
        
        # Ridge thickness contribution
        thickness_score = min(1.0, ridge_thickness)
        
        # Combine scores
        focus_quality = (density_score * 0.3 + clustering_score * 0.25 + modularity_score * 0.25 + thickness_score * 0.2)
        return min(1.0, focus_quality)
    
    def _calculate_attention_control(self, ridge_uniformity: float, pattern_type: str,
                                   ridge_orientation: float, community_cohesion: float) -> float:
        """Calculate attention control from fingerprint features (DMIT principle)"""
        # DMIT research shows: High ridge uniformity + pattern type = attention control
        
        # Ridge uniformity contribution
        uniformity_score = min(1.0, ridge_uniformity)
        
        # Pattern type contribution
        pattern_weights = {
            'whorl': 0.8,      # Complex patterns indicate good control
            'loop': 0.7,       # Good control
            'arch': 0.6,       # Moderate control
            'tented_arch': 0.65, # Slightly better than plain arch
            'composite': 0.75   # Complex control patterns
        }
        pattern_score = pattern_weights.get(pattern_type.lower(), 0.6)
        
        # Ridge orientation contribution
        orientation_score = min(1.0, abs(ridge_orientation) / 180.0)
        
        # Community cohesion contribution
        cohesion_score = min(1.0, community_cohesion)
        
        # Combine scores
        attention_control = (uniformity_score * 0.3 + pattern_score * 0.25 + orientation_score * 0.25 + cohesion_score * 0.2)
        return min(1.0, attention_control)
    
    def _calculate_cognitive_load_management(self, spectral_centroid: float, spectral_rolloff: float,
                                           graph_density: float, topological_complexity: float) -> float:
        """Calculate cognitive load management from fingerprint features (DMIT principle)"""
        # DMIT research shows: High spectral features + graph complexity = load management
        
        # Spectral centroid contribution
        centroid_score = min(1.0, spectral_centroid)
        
        # Spectral rolloff contribution
        rolloff_score = min(1.0, spectral_rolloff)
        
        # Graph density contribution
        density_score = min(1.0, graph_density)
        
        # Topological complexity contribution
        complexity_score = min(1.0, topological_complexity)
        
        # Combine scores
        cognitive_load_management = (centroid_score * 0.3 + rolloff_score * 0.25 + density_score * 0.25 + complexity_score * 0.2)
        return min(1.0, cognitive_load_management)
    
    def _calculate_attention_flexibility(self, information_dimension: float, entropy: float,
                                       pattern_symmetry: float, spectral_entropy: float) -> float:
        """Calculate attention flexibility from fingerprint features (DMIT principle)"""
        # DMIT research shows: High information dimension + entropy = attention flexibility
        
        # Information dimension contribution
        if 1.5 <= information_dimension <= 2.0:
            info_score = (information_dimension - 1.5) / 0.5
        else:
            info_score = 0.5
        
        # Entropy contribution (higher entropy = more complex flexibility)
        if entropy > 0:
            entropy_score = min(1.0, entropy / 8.0)  # Normalize to 0-1
        else:
            entropy_score = 0.5
        
        # Pattern symmetry contribution
        symmetry_score = min(1.0, pattern_symmetry)
        
        # Spectral entropy contribution
        spectral_score = min(1.0, spectral_entropy)
        
        # Combine scores
        attention_flexibility = (info_score * 0.35 + entropy_score * 0.25 + symmetry_score * 0.25 + spectral_score * 0.15)
        return min(1.0, attention_flexibility)

    @staticmethod
    def classify_attention_level(score: float) -> str:
        if score >= 0.85:
            return "Exceptional Attention and Focus"
        elif score >= 0.75:
            return "High Attention and Focus"
        elif score >= 0.65:
            return "Above Average Attention and Focus"
        elif score >= 0.55:
            return "Average Attention and Focus"
        else:
            return "Developing Attention and Focus" 