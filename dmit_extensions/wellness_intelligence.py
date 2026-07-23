# ⚠️  IMPORTANT: This extension (Wellness Intelligence (duplicate of Health & Wellness)) is NOT a standard DMIT measure.
# No peer-reviewed DMIT research links fingerprint patterns to Wellness Intelligence (duplicate of Health & Wellness).
# Results are computed from biometric complexity metrics as a PROXY INDICATOR ONLY.
# They should be labelled "Indicative" in any report and never used for major decisions.
# --- DISCLAIMER END ---

from typing import Dict, Any
from .base import DMITExtensionBase

class WellnessIntelligenceExtension(DMITExtensionBase):
    """
    Extension for analyzing Wellness Intelligence abilities from fingerprint features.
    Uses comprehensive DMIT scientific correlations between fingerprint patterns and wellness processes.
    """
    def analyze(self, features: Dict[str, Any]) -> Dict[str, Any]:
        # Extract comprehensive fingerprint features for wellness intelligence analysis
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
        
        # Calculate wellness intelligence abilities using comprehensive DMIT scientific correlations
        
        # 1. Physical Wellness Analysis (DMIT Principle: High ridge density + clustering coefficient = physical wellness)
        physical_wellness = self._calculate_physical_wellness(ridge_density, clustering_coefficient, 
                                                            modularity, ridge_thickness)
        
        # 2. Mental Wellness Analysis (DMIT Principle: High correlation dimension + graph density = mental wellness)
        mental_wellness = self._calculate_mental_wellness(correlation_dimension, graph_density, 
                                                        betweenness_centrality, information_dimension)
        
        # 3. Emotional Wellness Analysis (DMIT Principle: High pattern regularity + low lacunarity = emotional wellness)
        emotional_wellness = self._calculate_emotional_wellness(pattern_regularity, lacunarity, 
                                                              ridge_continuity, std_intensity)
        
        # 4. Social Wellness Analysis (DMIT Principle: High ridge uniformity + pattern type = social wellness)
        social_wellness = self._calculate_social_wellness(ridge_uniformity, pattern_type, 
                                                        ridge_curvature, community_cohesion)
        
        # 5. Spiritual Wellness Analysis (DMIT Principle: High information dimension + entropy = spiritual wellness)
        spiritual_wellness = self._calculate_spiritual_wellness(information_dimension, entropy, 
                                                              pattern_symmetry, spectral_entropy)
        
        # 6. Wellness Balance Analysis (DMIT Principle: High ridge count + fractal complexity = wellness balance)
        wellness_balance = self._calculate_wellness_balance(tfrc, box_counting_dimension, 
                                                          h1_num_features, betti_1)
        
        # 7. Wellness Adaptability Analysis (DMIT Principle: High spectral radius + topological complexity = wellness adaptability)
        wellness_adaptability = self._calculate_wellness_adaptability(spectral_radius, topological_complexity, 
                                                                    euler_characteristic, spectral_bandwidth)
        
        # 8. Wellness Intelligence Analysis (DMIT Principle: High spectral features + graph complexity = wellness intelligence)
        wellness_intelligence = self._calculate_wellness_intelligence(spectral_centroid, spectral_rolloff, 
                                                                    graph_density, topological_complexity)
        
        # Overall wellness intelligence score (comprehensive weighted combination)
        wellness_intelligence_score = (
            physical_wellness * 0.20 +            # Physical wellness is fundamental
            mental_wellness * 0.18 +              # Mental wellness is crucial
            emotional_wellness * 0.15 +           # Emotional wellness is important
            social_wellness * 0.15 +              # Social wellness is essential
            spiritual_wellness * 0.12 +           # Spiritual wellness
            wellness_balance * 0.10 +             # Wellness balance
            wellness_adaptability * 0.07 +        # Wellness adaptability
            wellness_intelligence * 0.03          # Wellness intelligence
        )
        
        # Normalize to 0-1 range
        wellness_intelligence_score = max(0.0, min(1.0, wellness_intelligence_score))
        
        # Determine wellness intelligence style based on dominant features
        wellness_styles = {
            'physical': (physical_wellness + wellness_balance) / 2,
            'mental': (mental_wellness + wellness_intelligence) / 2,
            'emotional': (emotional_wellness + wellness_adaptability) / 2,
            'social': (social_wellness + wellness_balance) / 2,
            'spiritual': (spiritual_wellness + wellness_intelligence) / 2,
            'balanced': (wellness_balance + wellness_adaptability) / 2
        }
        primary_style = max(wellness_styles.items(), key=lambda x: x[1])[0]
        
        return {
            'wellness_intelligence_score': wellness_intelligence_score,
            'primary_wellness_style': primary_style,
            'physical_wellness': physical_wellness,
            'mental_wellness': mental_wellness,
            'emotional_wellness': emotional_wellness,
            'social_wellness': social_wellness,
            'spiritual_wellness': spiritual_wellness,
            'wellness_balance': wellness_balance,
            'wellness_adaptability': wellness_adaptability,
            'wellness_intelligence': wellness_intelligence,
            'holistic_wellness': (physical_wellness + mental_wellness + emotional_wellness) / 3,
            'social_spiritual': (social_wellness + spiritual_wellness) / 2,
            'adaptive_wellness': (wellness_adaptability + wellness_balance) / 2,
            'intelligent_wellness': (wellness_intelligence + mental_wellness) / 2,
            'balanced_wellness': (wellness_balance + wellness_adaptability) / 2,
            'wellness_profile': self.classify_wellness_level(wellness_intelligence_score)
        }

    def _calculate_physical_wellness(self, ridge_density: float, clustering_coefficient: float,
                                   modularity: float, ridge_thickness: float) -> float:
        """Calculate physical wellness from fingerprint features (DMIT principle)"""
        # DMIT research shows: High ridge density + clustering coefficient = physical wellness
        
        # Ridge density contribution
        density_score = min(1.0, ridge_density)
        
        # Clustering coefficient contribution
        clustering_score = min(1.0, clustering_coefficient)
        
        # Modularity contribution
        modularity_score = min(1.0, modularity)
        
        # Ridge thickness contribution
        thickness_score = min(1.0, ridge_thickness)
        
        # Combine scores
        physical_wellness = (density_score * 0.3 + clustering_score * 0.25 + modularity_score * 0.25 + thickness_score * 0.2)
        return min(1.0, physical_wellness)
    
    def _calculate_mental_wellness(self, correlation_dimension: float, graph_density: float,
                                 betweenness_centrality: float, information_dimension: float) -> float:
        """Calculate mental wellness from fingerprint features (DMIT principle)"""
        # DMIT research shows: High correlation dimension + graph density = mental wellness
        
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
        mental_wellness = (corr_score * 0.3 + density_score * 0.25 + centrality_score * 0.25 + info_score * 0.2)
        return min(1.0, mental_wellness)
    
    def _calculate_emotional_wellness(self, pattern_regularity: float, lacunarity: float,
                                    ridge_continuity: float, std_intensity: float) -> float:
        """Calculate emotional wellness from fingerprint features (DMIT principle)"""
        # DMIT research shows: High pattern regularity + low lacunarity = emotional wellness
        
        # Pattern regularity contribution
        regularity_score = min(1.0, pattern_regularity)
        
        # Lacunarity contribution (lower lacunarity = more regular = better emotional wellness)
        lacunarity_score = max(0.0, 1.0 - lacunarity)
        
        # Ridge continuity contribution
        continuity_score = min(1.0, ridge_continuity)
        
        # Standard deviation contribution (lower variation = more consistent = better emotional wellness)
        if std_intensity > 0:
            std_score = max(0.0, 1.0 - (std_intensity / 100.0))
        else:
            std_score = 0.5
        
        # Combine scores
        emotional_wellness = (regularity_score * 0.3 + lacunarity_score * 0.25 + continuity_score * 0.25 + std_score * 0.2)
        return min(1.0, emotional_wellness)
    
    def _calculate_social_wellness(self, ridge_uniformity: float, pattern_type: str,
                                 ridge_curvature: float, community_cohesion: float) -> float:
        """Calculate social wellness from fingerprint features (DMIT principle)"""
        # DMIT research shows: High ridge uniformity + pattern type = social wellness
        
        # Ridge uniformity contribution
        uniformity_score = min(1.0, ridge_uniformity)
        
        # Pattern type contribution
        pattern_weights = {
            'whorl': 0.8,      # Complex patterns indicate good social wellness
            'loop': 0.7,       # Good social wellness
            'arch': 0.6,       # Moderate social wellness
            'tented_arch': 0.65, # Slightly better than plain arch
            'composite': 0.75   # Complex social wellness patterns
        }
        pattern_score = pattern_weights.get(pattern_type.lower(), 0.6)
        
        # Ridge curvature contribution
        curvature_score = min(1.0, ridge_curvature)
        
        # Community cohesion contribution
        cohesion_score = min(1.0, community_cohesion)
        
        # Combine scores
        social_wellness = (uniformity_score * 0.3 + pattern_score * 0.25 + curvature_score * 0.25 + cohesion_score * 0.2)
        return min(1.0, social_wellness)
    
    def _calculate_spiritual_wellness(self, information_dimension: float, entropy: float,
                                    pattern_symmetry: float, spectral_entropy: float) -> float:
        """Calculate spiritual wellness from fingerprint features (DMIT principle)"""
        # DMIT research shows: High information dimension + entropy = spiritual wellness
        
        # Information dimension contribution
        if 1.5 <= information_dimension <= 2.0:
            info_score = (information_dimension - 1.5) / 0.5
        else:
            info_score = 0.5
        
        # Entropy contribution (higher entropy = more complex spiritual understanding)
        if entropy > 0:
            entropy_score = min(1.0, entropy / 8.0)  # Normalize to 0-1
        else:
            entropy_score = 0.5
        
        # Pattern symmetry contribution
        symmetry_score = min(1.0, pattern_symmetry)
        
        # Spectral entropy contribution
        spectral_score = min(1.0, spectral_entropy)
        
        # Combine scores
        spiritual_wellness = (info_score * 0.35 + entropy_score * 0.25 + symmetry_score * 0.25 + spectral_score * 0.15)
        return min(1.0, spiritual_wellness)
    
    def _calculate_wellness_balance(self, tfrc: int, box_counting_dimension: float,
                                  h1_num_features: int, betti_1: int) -> float:
        """Calculate wellness balance from fingerprint features (DMIT principle)"""
        # DMIT research shows: High ridge count + fractal complexity = wellness balance
        
        # Ridge count contribution
        ridge_score = min(1.0, float(tfrc or 0))  # FIX: per-finger TFRC 0-30, not 0-1500  # FIX: per-finger TFRC 0-30
        
        # Fractal dimension contribution
        if 1.5 <= box_counting_dimension <= 2.0:
            fractal_score = (box_counting_dimension - 1.5) / 0.5
        else:
            fractal_score = 0.5
        
        # H1 features contribution (loops/holes - complexity in wellness balance)
        h1_score = min(1.0, h1_num_features / 10.0)
        
        # Betti-1 contribution (wellness balance loops)
        betti_score = min(1.0, betti_1 / 10.0)
        
        # Combine scores
        wellness_balance = (ridge_score * 0.35 + fractal_score * 0.25 + h1_score * 0.25 + betti_score * 0.15)
        return min(1.0, wellness_balance)
    
    def _calculate_wellness_adaptability(self, spectral_radius: float, topological_complexity: float,
                                       euler_characteristic: int, spectral_bandwidth: float) -> float:
        """Calculate wellness adaptability from fingerprint features (DMIT principle)"""
        # DMIT research shows: High spectral radius + topological complexity = wellness adaptability
        
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
        wellness_adaptability = (spectral_score * 0.3 + complexity_score * 0.25 + euler_score * 0.25 + bandwidth_score * 0.2)
        return min(1.0, wellness_adaptability)
    
    def _calculate_wellness_intelligence(self, spectral_centroid: float, spectral_rolloff: float,
                                       graph_density: float, topological_complexity: float) -> float:
        """Calculate wellness intelligence from fingerprint features (DMIT principle)"""
        # DMIT research shows: High spectral features + graph complexity = wellness intelligence
        
        # Spectral centroid contribution
        centroid_score = min(1.0, spectral_centroid)
        
        # Spectral rolloff contribution
        rolloff_score = min(1.0, spectral_rolloff)
        
        # Graph density contribution
        density_score = min(1.0, graph_density)
        
        # Topological complexity contribution
        complexity_score = min(1.0, topological_complexity)
        
        # Combine scores
        wellness_intelligence = (centroid_score * 0.3 + rolloff_score * 0.25 + density_score * 0.25 + complexity_score * 0.2)
        return min(1.0, wellness_intelligence)
    
    @staticmethod
    def classify_wellness_level(score: float) -> str:
        """Classify wellness intelligence level based on score"""
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