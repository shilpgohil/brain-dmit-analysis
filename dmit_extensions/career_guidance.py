from typing import Dict, Any
from .base import DMITExtensionBase

class CareerGuidanceExtension(DMITExtensionBase):
    """
    Extension for analyzing Career Guidance and professional aptitudes from fingerprint features.
    Uses comprehensive DMIT scientific correlations between fingerprint patterns and career potentials.
    """
    def analyze(self, features: Dict[str, Any]) -> Dict[str, Any]:
        # Extract comprehensive fingerprint features for career guidance analysis
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
        
        # Calculate career guidance using comprehensive DMIT scientific correlations
        
        # 1. Technical Career Analysis (DMIT Principle: High correlation dimension + graph density = technical aptitude)
        technical_career = self._calculate_technical_career(correlation_dimension, graph_density, 
                                                          betweenness_centrality, information_dimension)
        
        # 2. Creative Career Analysis (DMIT Principle: High information dimension + entropy = creative aptitude)
        creative_career = self._calculate_creative_career(information_dimension, entropy, 
                                                        pattern_symmetry, spectral_entropy)
        
        # 3. Analytical Career Analysis (DMIT Principle: High ridge count + fractal dimension = analytical aptitude)
        analytical_career = self._calculate_analytical_career(tfrc, box_counting_dimension, 
                                                            h1_num_features, betti_1)
        
        # 4. Leadership Career Analysis (DMIT Principle: High spectral radius + topological complexity = leadership)
        leadership_career = self._calculate_leadership_career(spectral_radius, topological_complexity, 
                                                            euler_characteristic, spectral_bandwidth)
        
        # 5. Social Career Analysis (DMIT Principle: High community cohesion + clustering coefficient = social aptitude)
        social_career = self._calculate_social_career(community_cohesion, clustering_coefficient, 
                                                    modularity, ridge_thickness)
        
        # 6. Administrative Career Analysis (DMIT Principle: High pattern regularity + low lacunarity = administrative)
        administrative_career = self._calculate_administrative_career(pattern_regularity, lacunarity, 
                                                                    ridge_continuity, std_intensity)
        
        # 7. Research Career Analysis (DMIT Principle: High fractal complexity + spectral features = research aptitude)
        research_career = self._calculate_research_career(fractal_complexity, spectral_centroid, spectral_rolloff, 
                                                        graph_density, topological_complexity)
        
        # 8. Entrepreneurial Career Analysis (DMIT Principle: High ridge uniformity + pattern type = entrepreneurial)
        entrepreneurial_career = self._calculate_entrepreneurial_career(ridge_uniformity, pattern_type, 
                                                                      ridge_curvature, spectral_energy)
        
        # Determine primary career aptitude based on highest score
        career_aptitudes = {
            'technical': technical_career,
            'creative': creative_career,
            'analytical': analytical_career,
            'leadership': leadership_career,
            'social': social_career,
            'administrative': administrative_career,
            'research': research_career,
            'entrepreneurial': entrepreneurial_career
        }
        primary_aptitude = max(career_aptitudes.items(), key=lambda x: x[1])[0]
        
        # Calculate overall career potential score
        career_potential_score = (
            technical_career * 0.15 +                # Technical aptitude
            creative_career * 0.15 +                 # Creative aptitude
            analytical_career * 0.15 +               # Analytical aptitude
            leadership_career * 0.15 +               # Leadership aptitude
            social_career * 0.12 +                   # Social aptitude
            administrative_career * 0.12 +           # Administrative aptitude
            research_career * 0.08 +                 # Research aptitude
            entrepreneurial_career * 0.08            # Entrepreneurial aptitude
        )
        
        # Normalize to 0-1 range
        career_potential_score = max(0.0, min(1.0, career_potential_score))
        
        return {
            'career_potential_score': career_potential_score,
            'primary_career_aptitude': primary_aptitude,
            'technical_career': technical_career,
            'creative_career': creative_career,
            'analytical_career': analytical_career,
            'leadership_career': leadership_career,
            'social_career': social_career,
            'administrative_career': administrative_career,
            'research_career': research_career,
            'entrepreneurial_career': entrepreneurial_career,
            'stem_careers': technical_career + analytical_career + research_career,
            'arts_media_careers': creative_career + social_career,
            'business_careers': leadership_career + administrative_career + entrepreneurial_career,
            'service_careers': social_career + administrative_career,
            'innovation_careers': creative_career + research_career + entrepreneurial_career,
            'career_guidance_profile': self.classify_career_potential(primary_aptitude, career_potential_score)
        }

    def _calculate_technical_career(self, correlation_dimension: float, graph_density: float,
                                  betweenness_centrality: float, information_dimension: float) -> float:
        """Calculate technical career aptitude from fingerprint features (DMIT principle)"""
        # DMIT research shows: High correlation dimension + graph density = technical aptitude
        
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
        technical_career = (corr_score * 0.3 + density_score * 0.25 + centrality_score * 0.25 + info_score * 0.2)
        return min(1.0, technical_career)
    
    def _calculate_creative_career(self, information_dimension: float, entropy: float,
                                 pattern_symmetry: float, spectral_entropy: float) -> float:
        """Calculate creative career aptitude from fingerprint features (DMIT principle)"""
        # DMIT research shows: High information dimension + entropy = creative aptitude
        
        # Information dimension contribution
        if 1.5 <= information_dimension <= 2.0:
            info_score = (information_dimension - 1.5) / 0.5
        else:
            info_score = 0.5
        
        # Entropy contribution (higher entropy = more complex creative aptitude)
        if entropy > 0:
            entropy_score = min(1.0, entropy / 8.0)  # Normalize to 0-1
        else:
            entropy_score = 0.5
        
        # Pattern symmetry contribution
        symmetry_score = min(1.0, pattern_symmetry)
        
        # Spectral entropy contribution
        spectral_score = min(1.0, spectral_entropy)
        
        # Combine scores
        creative_career = (info_score * 0.35 + entropy_score * 0.25 + symmetry_score * 0.25 + spectral_score * 0.15)
        return min(1.0, creative_career)
    
    def _calculate_analytical_career(self, tfrc: int, box_counting_dimension: float,
                                   h1_num_features: int, betti_1: int) -> float:
        """Calculate analytical career aptitude from fingerprint features (DMIT principle)"""
        # DMIT research shows: High ridge count + fractal dimension = analytical aptitude
        
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
        
        # H1 features contribution (loops/holes - complexity in analytical thinking)
        h1_score = min(1.0, h1_num_features / 10.0)
        
        # Betti-1 contribution (analytical loops)
        betti_score = min(1.0, betti_1 / 10.0)
        
        # Combine scores
        analytical_career = (ridge_score * 0.35 + fractal_score * 0.25 + h1_score * 0.25 + betti_score * 0.15)
        return min(1.0, analytical_career)
    
    def _calculate_leadership_career(self, spectral_radius: float, topological_complexity: float,
                                   euler_characteristic: int, spectral_bandwidth: float) -> float:
        """Calculate leadership career aptitude from fingerprint features (DMIT principle)"""
        # DMIT research shows: High spectral radius + topological complexity = leadership
        
        # Spectral radius contribution
        if spectral_radius > 0:
            spectral_score = min(1.0, spectral_radius / 10.0)
        else:
            spectral_score = 0.5
        
        # Topological complexity contribution
        complexity_score = min(1.0, topological_complexity)
        
        # Euler characteristic contribution (more negative = more complex = better leadership)
        if euler_characteristic < 0:
            euler_score = min(1.0, abs(euler_characteristic) / 10.0)
        else:
            euler_score = 0.3
        
        # Spectral bandwidth contribution
        bandwidth_score = min(1.0, spectral_bandwidth)
        
        # Combine scores
        leadership_career = (spectral_score * 0.3 + complexity_score * 0.25 + euler_score * 0.25 + bandwidth_score * 0.2)
        return min(1.0, leadership_career)
    
    def _calculate_social_career(self, community_cohesion: float, clustering_coefficient: float,
                               modularity: float, ridge_thickness: float) -> float:
        """Calculate social career aptitude from fingerprint features (DMIT principle)"""
        # DMIT research shows: High community cohesion + clustering coefficient = social aptitude
        
        # Community cohesion contribution
        cohesion_score = min(1.0, community_cohesion)
        
        # Clustering coefficient contribution
        clustering_score = min(1.0, clustering_coefficient)
        
        # Modularity contribution
        modularity_score = min(1.0, modularity)
        
        # Ridge thickness contribution
        thickness_score = min(1.0, ridge_thickness)
        
        # Combine scores
        social_career = (cohesion_score * 0.3 + clustering_score * 0.25 + modularity_score * 0.25 + thickness_score * 0.2)
        return min(1.0, social_career)
    
    def _calculate_administrative_career(self, pattern_regularity: float, lacunarity: float,
                                       ridge_continuity: float, std_intensity: float) -> float:
        """Calculate administrative career aptitude from fingerprint features (DMIT principle)"""
        # DMIT research shows: High pattern regularity + low lacunarity = administrative aptitude
        
        # Pattern regularity contribution
        regularity_score = min(1.0, pattern_regularity)
        
        # Lacunarity contribution (lower lacunarity = more regular = better administrative)
        lacunarity_score = max(0.0, 1.0 - lacunarity)
        
        # Ridge continuity contribution
        continuity_score = min(1.0, ridge_continuity)
        
        # Standard deviation contribution (lower variation = more consistent = better administrative)
        if std_intensity > 0:
            std_score = max(0.0, 1.0 - (std_intensity / 100.0))
        else:
            std_score = 0.5
        
        # Combine scores
        administrative_career = (regularity_score * 0.3 + lacunarity_score * 0.25 + continuity_score * 0.25 + std_score * 0.2)
        return min(1.0, administrative_career)
    
    def _calculate_research_career(self, fractal_complexity: float, spectral_centroid: float, spectral_rolloff: float,
                                 graph_density: float, topological_complexity: float) -> float:
        """Calculate research career aptitude from fingerprint features (DMIT principle)"""
        # DMIT research shows: High fractal complexity + spectral features = research aptitude
        
        # Fractal complexity contribution
        complexity_score = min(1.0, fractal_complexity)
        
        # Spectral centroid contribution
        centroid_score = min(1.0, spectral_centroid)
        
        # Spectral rolloff contribution
        rolloff_score = min(1.0, spectral_rolloff)
        
        # Graph density contribution
        density_score = min(1.0, graph_density)
        
        # Topological complexity contribution
        topological_score = min(1.0, topological_complexity)
        
        # Combine scores
        research_career = (complexity_score * 0.25 + centroid_score * 0.2 + rolloff_score * 0.2 + density_score * 0.2 + topological_score * 0.15)
        return min(1.0, research_career)
    
    def _calculate_entrepreneurial_career(self, ridge_uniformity: float, pattern_type: str,
                                       ridge_curvature: float, spectral_energy: float) -> float:
        """Calculate entrepreneurial career aptitude from fingerprint features (DMIT principle)"""
        # DMIT research shows: High ridge uniformity + pattern type = entrepreneurial aptitude
        
        # Ridge uniformity contribution
        uniformity_score = min(1.0, ridge_uniformity)
        
        # Pattern type contribution
        pattern_weights = {
            'whorl': 0.8,      # Complex patterns indicate entrepreneurial aptitude
            'loop': 0.7,       # Good entrepreneurial aptitude
            'arch': 0.6,       # Moderate entrepreneurial aptitude
            'tented_arch': 0.65, # Slightly better than plain arch
            'composite': 0.75   # Complex entrepreneurial patterns
        }
        pattern_score = pattern_weights.get(pattern_type.lower(), 0.6)
        
        # Ridge curvature contribution
        curvature_score = min(1.0, ridge_curvature)
        
        # Spectral energy contribution
        energy_score = min(1.0, spectral_energy)
        
        # Combine scores
        entrepreneurial_career = (uniformity_score * 0.3 + pattern_score * 0.25 + curvature_score * 0.25 + energy_score * 0.2)
        return min(1.0, entrepreneurial_career)

    @staticmethod
    def classify_career_potential(primary_aptitude: str, potential_score: float) -> str:
        if potential_score >= 0.85:
            level = "Exceptional"
        elif potential_score >= 0.75:
            level = "High"
        elif potential_score >= 0.65:
            level = "Above Average"
        elif potential_score >= 0.55:
            level = "Average"
        else:
            level = "Developing"
        
        aptitude_names = {
            'technical': 'Technical Career',
            'creative': 'Creative Career',
            'analytical': 'Analytical Career',
            'leadership': 'Leadership Career',
            'social': 'Social Career',
            'administrative': 'Administrative Career',
            'research': 'Research Career',
            'entrepreneurial': 'Entrepreneurial Career'
        }
        
        return f"{level} {aptitude_names.get(primary_aptitude, 'Career')} Potential" 