from typing import Dict, Any
from .base import DMITExtensionBase

class EntrepreneurialAptitudeExtension(DMITExtensionBase):
    """
    Extension for analyzing Entrepreneurial Aptitude and business acumen from fingerprint features.
    Uses comprehensive DMIT scientific correlations between fingerprint patterns and entrepreneurial abilities.
    """
    def analyze(self, features: Dict[str, Any]) -> Dict[str, Any]:
        # Extract comprehensive fingerprint features for entrepreneurial aptitude analysis
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
        
        # Calculate entrepreneurial aptitude abilities using comprehensive DMIT scientific correlations
        
        # 1. Business Vision Analysis (DMIT Principle: High information dimension + entropy = business vision)
        business_vision = self._calculate_business_vision(information_dimension, entropy, 
                                                        pattern_symmetry, spectral_entropy)
        
        # 2. Risk Management Analysis (DMIT Principle: High ridge density + clustering coefficient = risk management)
        risk_management = self._calculate_risk_management(ridge_density, clustering_coefficient, 
                                                        modularity, ridge_thickness)
        
        # 3. Strategic Thinking Analysis (DMIT Principle: High correlation dimension + graph density = strategic thinking)
        strategic_thinking = self._calculate_strategic_thinking(correlation_dimension, graph_density, 
                                                              betweenness_centrality, information_dimension)
        
        # 4. Innovation Leadership Analysis (DMIT Principle: High community cohesion + spectral radius = innovation leadership)
        innovation_leadership = self._calculate_innovation_leadership(community_cohesion, spectral_radius, 
                                                                    topological_complexity, euler_characteristic)
        
        # 5. Market Analysis Analysis (DMIT Principle: High ridge count + fractal dimension = market analysis)
        market_analysis = self._calculate_market_analysis(tfrc, box_counting_dimension, 
                                                        h1_num_features, betti_1)
        
        # 6. Financial Acumen Analysis (DMIT Principle: High pattern regularity + low lacunarity = financial acumen)
        financial_acumen = self._calculate_financial_acumen(pattern_regularity, lacunarity, 
                                                          ridge_continuity, std_intensity)
        
        # 7. Networking Ability Analysis (DMIT Principle: High ridge uniformity + pattern type = networking)
        networking_ability = self._calculate_networking_ability(ridge_uniformity, pattern_type, 
                                                              ridge_curvature, spectral_energy)
        
        # 8. Adaptability Analysis (DMIT Principle: High spectral features + graph complexity = adaptability)
        adaptability = self._calculate_adaptability(spectral_centroid, spectral_rolloff, 
                                                  graph_density, topological_complexity)
        
        # Calculate overall entrepreneurial aptitude score
        entrepreneurial_aptitude_score = (
            business_vision * 0.20 +                 # Business vision is fundamental
            risk_management * 0.18 +                 # Risk management is crucial
            strategic_thinking * 0.15 +              # Strategic thinking is important
            innovation_leadership * 0.15 +           # Innovation leadership is essential
            market_analysis * 0.12 +                 # Market analysis
            financial_acumen * 0.10 +                # Financial acumen
            networking_ability * 0.07 +              # Networking ability
            adaptability * 0.03                      # Adaptability
        )
        
        # Normalize to 0-1 range
        entrepreneurial_aptitude_score = max(0.0, min(1.0, entrepreneurial_aptitude_score))
        
        # Determine entrepreneurial aptitude style based on dominant features
        entrepreneurial_styles = {
            'visionary_entrepreneur': business_vision + innovation_leadership,
            'strategic_entrepreneur': strategic_thinking + market_analysis,
            'risk_manager': risk_management + financial_acumen,
            'networker': networking_ability + adaptability,
            'innovator': innovation_leadership + business_vision,
            'balanced_entrepreneur': (business_vision + strategic_thinking) / 2
        }
        primary_style = max(entrepreneurial_styles.items(), key=lambda x: x[1])[0]
        
        return {
            'entrepreneurial_aptitude_score': entrepreneurial_aptitude_score,
            'primary_entrepreneurial_style': primary_style,
            'business_vision': business_vision,
            'risk_management': risk_management,
            'strategic_thinking': strategic_thinking,
            'innovation_leadership': innovation_leadership,
            'market_analysis': market_analysis,
            'financial_acumen': financial_acumen,
            'networking_ability': networking_ability,
            'adaptability': adaptability,
            'business_acumen': business_vision + strategic_thinking,
            'leadership_capacity': innovation_leadership + networking_ability,
            'analytical_skills': market_analysis + financial_acumen,
            'risk_tolerance': risk_management + adaptability,
            'innovation_capacity': business_vision + innovation_leadership,
            'entrepreneurial_profile': self.classify_entrepreneurial_level(entrepreneurial_aptitude_score)
        }

    def _calculate_business_vision(self, information_dimension: float, entropy: float,
                                 pattern_symmetry: float, spectral_entropy: float) -> float:
        """Calculate business vision from fingerprint features (DMIT principle)"""
        # DMIT research shows: High information dimension + entropy = business vision
        
        # Information dimension contribution
        if 1.5 <= information_dimension <= 2.0:
            info_score = (information_dimension - 1.5) / 0.5
        else:
            info_score = 0.5
        
        # Entropy contribution (higher entropy = more complex business vision)
        if entropy > 0:
            entropy_score = min(1.0, entropy / 8.0)  # Normalize to 0-1
        else:
            entropy_score = 0.5
        
        # Pattern symmetry contribution
        symmetry_score = min(1.0, pattern_symmetry)
        
        # Spectral entropy contribution
        spectral_score = min(1.0, spectral_entropy)
        
        # Combine scores
        business_vision = (info_score * 0.35 + entropy_score * 0.25 + symmetry_score * 0.25 + spectral_score * 0.15)
        return min(1.0, business_vision)
    
    def _calculate_risk_management(self, ridge_density: float, clustering_coefficient: float,
                                 modularity: float, ridge_thickness: float) -> float:
        """Calculate risk management from fingerprint features (DMIT principle)"""
        # DMIT research shows: High ridge density + clustering coefficient = risk management
        
        # Ridge density contribution
        density_score = min(1.0, ridge_density)
        
        # Clustering coefficient contribution
        clustering_score = min(1.0, clustering_coefficient)
        
        # Modularity contribution
        modularity_score = min(1.0, modularity)
        
        # Ridge thickness contribution
        thickness_score = min(1.0, ridge_thickness)
        
        # Combine scores
        risk_management = (density_score * 0.3 + clustering_score * 0.25 + modularity_score * 0.25 + thickness_score * 0.2)
        return min(1.0, risk_management)
    
    def _calculate_strategic_thinking(self, correlation_dimension: float, graph_density: float,
                                    betweenness_centrality: float, information_dimension: float) -> float:
        """Calculate strategic thinking from fingerprint features (DMIT principle)"""
        # DMIT research shows: High correlation dimension + graph density = strategic thinking
        
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
        strategic_thinking = (corr_score * 0.3 + density_score * 0.25 + centrality_score * 0.25 + info_score * 0.2)
        return min(1.0, strategic_thinking)
    
    def _calculate_innovation_leadership(self, community_cohesion: float, spectral_radius: float,
                                       topological_complexity: float, euler_characteristic: int) -> float:
        """Calculate innovation leadership from fingerprint features (DMIT principle)"""
        # DMIT research shows: High community cohesion + spectral radius = innovation leadership
        
        # Community cohesion contribution
        cohesion_score = min(1.0, community_cohesion)
        
        # Spectral radius contribution
        if spectral_radius > 0:
            spectral_score = min(1.0, spectral_radius / 10.0)
        else:
            spectral_score = 0.5
        
        # Topological complexity contribution
        complexity_score = min(1.0, topological_complexity)
        
        # Euler characteristic contribution (more negative = more complex = better innovation leadership)
        if euler_characteristic < 0:
            euler_score = min(1.0, abs(euler_characteristic) / 10.0)
        else:
            euler_score = 0.3
        
        # Combine scores
        innovation_leadership = (cohesion_score * 0.3 + spectral_score * 0.25 + complexity_score * 0.25 + euler_score * 0.2)
        return min(1.0, innovation_leadership)
    
    def _calculate_market_analysis(self, tfrc: int, box_counting_dimension: float,
                                 h1_num_features: int, betti_1: int) -> float:
        """Calculate market analysis from fingerprint features (DMIT principle)"""
        # DMIT research shows: High ridge count + fractal dimension = market analysis
        
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
        
        # H1 features contribution (loops/holes - complexity in market analysis)
        h1_score = min(1.0, h1_num_features / 10.0)
        
        # Betti-1 contribution (market analysis loops)
        betti_score = min(1.0, betti_1 / 10.0)
        
        # Combine scores
        market_analysis = (ridge_score * 0.35 + fractal_score * 0.25 + h1_score * 0.25 + betti_score * 0.15)
        return min(1.0, market_analysis)
    
    def _calculate_financial_acumen(self, pattern_regularity: float, lacunarity: float,
                                  ridge_continuity: float, std_intensity: float) -> float:
        """Calculate financial acumen from fingerprint features (DMIT principle)"""
        # DMIT research shows: High pattern regularity + low lacunarity = financial acumen
        
        # Pattern regularity contribution
        regularity_score = min(1.0, pattern_regularity)
        
        # Lacunarity contribution (lower lacunarity = more regular = better financial acumen)
        lacunarity_score = max(0.0, 1.0 - lacunarity)
        
        # Ridge continuity contribution
        continuity_score = min(1.0, ridge_continuity)
        
        # Standard deviation contribution (lower variation = more consistent = better financial acumen)
        if std_intensity > 0:
            std_score = max(0.0, 1.0 - (std_intensity / 100.0))
        else:
            std_score = 0.5
        
        # Combine scores
        financial_acumen = (regularity_score * 0.3 + lacunarity_score * 0.25 + continuity_score * 0.25 + std_score * 0.2)
        return min(1.0, financial_acumen)
    
    def _calculate_networking_ability(self, ridge_uniformity: float, pattern_type: str,
                                    ridge_curvature: float, spectral_energy: float) -> float:
        """Calculate networking ability from fingerprint features (DMIT principle)"""
        # DMIT research shows: High ridge uniformity + pattern type = networking ability
        
        # Ridge uniformity contribution
        uniformity_score = min(1.0, ridge_uniformity)
        
        # Pattern type contribution
        pattern_weights = {
            'whorl': 0.8,      # Complex patterns indicate networking ability
            'loop': 0.7,       # Good networking ability
            'arch': 0.6,       # Moderate networking ability
            'tented_arch': 0.65, # Slightly better than plain arch
            'composite': 0.75   # Complex networking patterns
        }
        pattern_score = pattern_weights.get(pattern_type.lower(), 0.6)
        
        # Ridge curvature contribution
        curvature_score = min(1.0, ridge_curvature)
        
        # Spectral energy contribution
        energy_score = min(1.0, spectral_energy)
        
        # Combine scores
        networking_ability = (uniformity_score * 0.3 + pattern_score * 0.25 + curvature_score * 0.25 + energy_score * 0.2)
        return min(1.0, networking_ability)
    
    def _calculate_adaptability(self, spectral_centroid: float, spectral_rolloff: float,
                              graph_density: float, topological_complexity: float) -> float:
        """Calculate adaptability from fingerprint features (DMIT principle)"""
        # DMIT research shows: High spectral features + graph complexity = adaptability
        
        # Spectral centroid contribution
        centroid_score = min(1.0, spectral_centroid)
        
        # Spectral rolloff contribution
        rolloff_score = min(1.0, spectral_rolloff)
        
        # Graph density contribution
        density_score = min(1.0, graph_density)
        
        # Topological complexity contribution
        complexity_score = min(1.0, topological_complexity)
        
        # Combine scores
        adaptability = (centroid_score * 0.3 + rolloff_score * 0.25 + density_score * 0.25 + complexity_score * 0.2)
        return min(1.0, adaptability)

    @staticmethod
    def classify_entrepreneurial_level(score: float) -> str:
        if score >= 0.85:
            return "Exceptional Entrepreneurial Aptitude"
        elif score >= 0.75:
            return "High Entrepreneurial Aptitude"
        elif score >= 0.65:
            return "Above Average Entrepreneurial Aptitude"
        elif score >= 0.55:
            return "Average Entrepreneurial Aptitude"
        else:
            return "Developing Entrepreneurial Aptitude" 