from typing import Dict, Any
from .base import DMITExtensionBase

class NaturalisticIntelligenceExtension(DMITExtensionBase):
    """
    Extension for analyzing Naturalistic Intelligence and environmental awareness from fingerprint features.
    Uses comprehensive DMIT scientific correlations between fingerprint patterns and naturalistic capabilities.
    """
    def analyze(self, features: Dict[str, Any]) -> Dict[str, Any]:
        # Extract comprehensive fingerprint features for naturalistic intelligence analysis
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
        
        # Calculate naturalistic intelligence abilities using comprehensive DMIT scientific correlations
        
        # 1. Environmental Awareness Analysis (DMIT Principle: High information dimension + entropy = environmental awareness)
        environmental_awareness = self._calculate_environmental_awareness(information_dimension, entropy, 
                                                                        pattern_symmetry, spectral_entropy)
        
        # 2. Natural Pattern Recognition Analysis (DMIT Principle: High ridge density + clustering coefficient = natural pattern recognition)
        natural_pattern_recognition = self._calculate_natural_pattern_recognition(ridge_density, clustering_coefficient, 
                                                                                modularity, ridge_thickness)
        
        # 3. Ecological Understanding Analysis (DMIT Principle: High correlation dimension + graph density = ecological understanding)
        ecological_understanding = self._calculate_ecological_understanding(correlation_dimension, graph_density, 
                                                                          betweenness_centrality, information_dimension)
        
        # 4. Biodiversity Recognition Analysis (DMIT Principle: High community cohesion + spectral radius = biodiversity recognition)
        biodiversity_recognition = self._calculate_biodiversity_recognition(community_cohesion, spectral_radius, 
                                                                          topological_complexity, euler_characteristic)
        
        # 5. Natural System Analysis (DMIT Principle: High ridge count + fractal dimension = natural system analysis)
        natural_system_analysis = self._calculate_natural_system_analysis(tfrc, box_counting_dimension, 
                                                                        h1_num_features, betti_1)
        
        # 6. Environmental Sensitivity Analysis (DMIT Principle: High pattern regularity + low lacunarity = environmental sensitivity)
        environmental_sensitivity = self._calculate_environmental_sensitivity(pattern_regularity, lacunarity, 
                                                                            ridge_continuity, std_intensity)
        
        # 7. Natural Classification Analysis (DMIT Principle: High ridge uniformity + pattern type = natural classification)
        natural_classification = self._calculate_natural_classification(ridge_uniformity, pattern_type, 
                                                                      ridge_curvature, spectral_energy)
        
        # 8. Environmental Adaptability Analysis (DMIT Principle: High spectral features + graph complexity = environmental adaptability)
        environmental_adaptability = self._calculate_environmental_adaptability(spectral_centroid, spectral_rolloff, 
                                                                              graph_density, topological_complexity)
        
        # Calculate overall naturalistic intelligence score
        naturalistic_intelligence_score = (
            environmental_awareness * 0.20 +         # Environmental awareness is fundamental
            natural_pattern_recognition * 0.18 +     # Natural pattern recognition is crucial
            ecological_understanding * 0.15 +        # Ecological understanding is important
            biodiversity_recognition * 0.15 +        # Biodiversity recognition is essential
            natural_system_analysis * 0.12 +         # Natural system analysis
            environmental_sensitivity * 0.10 +       # Environmental sensitivity
            natural_classification * 0.07 +          # Natural classification
            environmental_adaptability * 0.03        # Environmental adaptability
        )
        
        # Normalize to 0-1 range
        naturalistic_intelligence_score = max(0.0, min(1.0, naturalistic_intelligence_score))
        
        # Determine naturalistic intelligence style based on dominant features
        naturalistic_styles = {
            'environmental_observer': environmental_awareness + environmental_sensitivity,
            'pattern_recognizer': natural_pattern_recognition + natural_classification,
            'ecological_thinker': ecological_understanding + natural_system_analysis,
            'biodiversity_expert': biodiversity_recognition + environmental_adaptability,
            'natural_system_analyst': natural_system_analysis + ecological_understanding,
            'balanced_naturalist': (environmental_awareness + natural_pattern_recognition) / 2
        }
        primary_style = max(naturalistic_styles.items(), key=lambda x: x[1])[0]
        
        return {
            'naturalistic_intelligence_score': naturalistic_intelligence_score,
            'primary_naturalistic_style': primary_style,
            'environmental_awareness': environmental_awareness,
            'natural_pattern_recognition': natural_pattern_recognition,
            'ecological_understanding': ecological_understanding,
            'biodiversity_recognition': biodiversity_recognition,
            'natural_system_analysis': natural_system_analysis,
            'environmental_sensitivity': environmental_sensitivity,
            'natural_classification': natural_classification,
            'environmental_adaptability': environmental_adaptability,
            'environmental_perception': environmental_awareness + environmental_sensitivity,
            'natural_analysis': natural_pattern_recognition + natural_system_analysis,
            'ecological_expertise': ecological_understanding + biodiversity_recognition,
            'environmental_adaptation': environmental_adaptability + natural_classification,
            'natural_observation': environmental_awareness + natural_pattern_recognition,
            'naturalistic_intelligence_profile': self.classify_naturalistic_intelligence_level(naturalistic_intelligence_score)
        }

    def _calculate_environmental_awareness(self, information_dimension: float, entropy: float,
                                         pattern_symmetry: float, spectral_entropy: float) -> float:
        """Calculate environmental awareness from fingerprint features (DMIT principle)"""
        # DMIT research shows: High information dimension + entropy = environmental awareness
        
        # Information dimension contribution
        if 1.5 <= information_dimension <= 2.0:
            info_score = (information_dimension - 1.5) / 0.5
        else:
            info_score = 0.5
        
        # Entropy contribution (higher entropy = more complex environmental awareness)
        if entropy > 0:
            entropy_score = min(1.0, entropy / 8.0)  # Normalize to 0-1
        else:
            entropy_score = 0.5
        
        # Pattern symmetry contribution
        symmetry_score = min(1.0, pattern_symmetry)
        
        # Spectral entropy contribution
        spectral_score = min(1.0, spectral_entropy)
        
        # Combine scores
        environmental_awareness = (info_score * 0.35 + entropy_score * 0.25 + symmetry_score * 0.25 + spectral_score * 0.15)
        return min(1.0, environmental_awareness)
    
    def _calculate_natural_pattern_recognition(self, ridge_density: float, clustering_coefficient: float,
                                             modularity: float, ridge_thickness: float) -> float:
        """Calculate natural pattern recognition from fingerprint features (DMIT principle)"""
        # DMIT research shows: High ridge density + clustering coefficient = natural pattern recognition
        
        # Ridge density contribution
        density_score = min(1.0, ridge_density)
        
        # Clustering coefficient contribution
        clustering_score = min(1.0, clustering_coefficient)
        
        # Modularity contribution
        modularity_score = min(1.0, modularity)
        
        # Ridge thickness contribution
        thickness_score = min(1.0, ridge_thickness)
        
        # Combine scores
        natural_pattern_recognition = (density_score * 0.3 + clustering_score * 0.25 + modularity_score * 0.25 + thickness_score * 0.2)
        return min(1.0, natural_pattern_recognition)
    
    def _calculate_ecological_understanding(self, correlation_dimension: float, graph_density: float,
                                          betweenness_centrality: float, information_dimension: float) -> float:
        """Calculate ecological understanding from fingerprint features (DMIT principle)"""
        # DMIT research shows: High correlation dimension + graph density = ecological understanding
        
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
        ecological_understanding = (corr_score * 0.3 + density_score * 0.25 + centrality_score * 0.25 + info_score * 0.2)
        return min(1.0, ecological_understanding)
    
    def _calculate_biodiversity_recognition(self, community_cohesion: float, spectral_radius: float,
                                          topological_complexity: float, euler_characteristic: int) -> float:
        """Calculate biodiversity recognition from fingerprint features (DMIT principle)"""
        # DMIT research shows: High community cohesion + spectral radius = biodiversity recognition
        
        # Community cohesion contribution
        cohesion_score = min(1.0, community_cohesion)
        
        # Spectral radius contribution
        if spectral_radius > 0:
            spectral_score = min(1.0, spectral_radius / 10.0)
        else:
            spectral_score = 0.5
        
        # Topological complexity contribution
        complexity_score = min(1.0, topological_complexity)
        
        # Euler characteristic contribution (more negative = more complex = better biodiversity recognition)
        if euler_characteristic < 0:
            euler_score = min(1.0, abs(euler_characteristic) / 10.0)
        else:
            euler_score = 0.3
        
        # Combine scores
        biodiversity_recognition = (cohesion_score * 0.3 + spectral_score * 0.25 + complexity_score * 0.25 + euler_score * 0.2)
        return min(1.0, biodiversity_recognition)
    
    def _calculate_natural_system_analysis(self, tfrc: int, box_counting_dimension: float,
                                         h1_num_features: int, betti_1: int) -> float:
        """Calculate natural system analysis from fingerprint features (DMIT principle)"""
        # DMIT research shows: High ridge count + fractal dimension = natural system analysis
        
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
        
        # H1 features contribution (loops/holes - complexity in natural system analysis)
        h1_score = min(1.0, h1_num_features / 10.0)
        
        # Betti-1 contribution (natural system analysis loops)
        betti_score = min(1.0, betti_1 / 10.0)
        
        # Combine scores
        natural_system_analysis = (ridge_score * 0.35 + fractal_score * 0.25 + h1_score * 0.25 + betti_score * 0.15)
        return min(1.0, natural_system_analysis)
    
    def _calculate_environmental_sensitivity(self, pattern_regularity: float, lacunarity: float,
                                           ridge_continuity: float, std_intensity: float) -> float:
        """Calculate environmental sensitivity from fingerprint features (DMIT principle)"""
        # DMIT research shows: High pattern regularity + low lacunarity = environmental sensitivity
        
        # Pattern regularity contribution
        regularity_score = min(1.0, pattern_regularity)
        
        # Lacunarity contribution (lower lacunarity = more regular = better environmental sensitivity)
        lacunarity_score = max(0.0, 1.0 - lacunarity)
        
        # Ridge continuity contribution
        continuity_score = min(1.0, ridge_continuity)
        
        # Standard deviation contribution (lower variation = more consistent = better environmental sensitivity)
        if std_intensity > 0:
            std_score = max(0.0, 1.0 - (std_intensity / 100.0))
        else:
            std_score = 0.5
        
        # Combine scores
        environmental_sensitivity = (regularity_score * 0.3 + lacunarity_score * 0.25 + continuity_score * 0.25 + std_score * 0.2)
        return min(1.0, environmental_sensitivity)
    
    def _calculate_natural_classification(self, ridge_uniformity: float, pattern_type: str,
                                        ridge_curvature: float, spectral_energy: float) -> float:
        """Calculate natural classification from fingerprint features (DMIT principle)"""
        # DMIT research shows: High ridge uniformity + pattern type = natural classification
        
        # Ridge uniformity contribution
        uniformity_score = min(1.0, ridge_uniformity)
        
        # Pattern type contribution
        pattern_weights = {
            'whorl': 0.8,      # Complex patterns indicate natural classification
            'loop': 0.7,       # Good natural classification
            'arch': 0.6,       # Moderate natural classification
            'tented_arch': 0.65, # Slightly better than plain arch
            'composite': 0.75   # Complex natural classification patterns
        }
        pattern_score = pattern_weights.get(pattern_type.lower(), 0.6)
        
        # Ridge curvature contribution
        curvature_score = min(1.0, ridge_curvature)
        
        # Spectral energy contribution
        energy_score = min(1.0, spectral_energy)
        
        # Combine scores
        natural_classification = (uniformity_score * 0.3 + pattern_score * 0.25 + curvature_score * 0.25 + energy_score * 0.2)
        return min(1.0, natural_classification)
    
    def _calculate_environmental_adaptability(self, spectral_centroid: float, spectral_rolloff: float,
                                            graph_density: float, topological_complexity: float) -> float:
        """Calculate environmental adaptability from fingerprint features (DMIT principle)"""
        # DMIT research shows: High spectral features + graph complexity = environmental adaptability
        
        # Spectral centroid contribution
        centroid_score = min(1.0, spectral_centroid)
        
        # Spectral rolloff contribution
        rolloff_score = min(1.0, spectral_rolloff)
        
        # Graph density contribution
        density_score = min(1.0, graph_density)
        
        # Topological complexity contribution
        complexity_score = min(1.0, topological_complexity)
        
        # Combine scores
        environmental_adaptability = (centroid_score * 0.3 + rolloff_score * 0.25 + density_score * 0.25 + complexity_score * 0.2)
        return min(1.0, environmental_adaptability)

    @staticmethod
    def classify_naturalistic_intelligence_level(score: float) -> str:
        if score >= 0.85:
            return "Exceptional Naturalistic Intelligence"
        elif score >= 0.75:
            return "High Naturalistic Intelligence"
        elif score >= 0.65:
            return "Above Average Naturalistic Intelligence"
        elif score >= 0.55:
            return "Average Naturalistic Intelligence"
        else:
            return "Developing Naturalistic Intelligence" 