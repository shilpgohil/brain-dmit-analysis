from typing import Dict, Any
from .base import DMITExtensionBase

class DigitalIntelligenceExtension(DMITExtensionBase):
    """
    Extension for analyzing Digital Intelligence and technology aptitude from fingerprint features.
    Uses comprehensive DMIT scientific correlations between fingerprint patterns and digital capabilities.
    """
    def analyze(self, features: Dict[str, Any]) -> Dict[str, Any]:
        # Extract comprehensive fingerprint features for digital intelligence analysis
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
        
        # Calculate digital intelligence abilities using comprehensive DMIT scientific correlations
        
        # 1. Digital Literacy Analysis (DMIT Principle: High information dimension + entropy = digital literacy)
        digital_literacy = self._calculate_digital_literacy(information_dimension, entropy, 
                                                          pattern_symmetry, spectral_entropy)
        
        # 2. Technology Adaptability Analysis (DMIT Principle: High ridge density + clustering coefficient = tech adaptability)
        technology_adaptability = self._calculate_technology_adaptability(ridge_density, clustering_coefficient, 
                                                                        modularity, ridge_thickness)
        
        # 3. Digital Problem Solving Analysis (DMIT Principle: High correlation dimension + graph density = digital problem solving)
        digital_problem_solving = self._calculate_digital_problem_solving(correlation_dimension, graph_density, 
                                                                        betweenness_centrality, information_dimension)
        
        # 4. Digital Innovation Analysis (DMIT Principle: High community cohesion + spectral radius = digital innovation)
        digital_innovation = self._calculate_digital_innovation(community_cohesion, spectral_radius, 
                                                              topological_complexity, euler_characteristic)
        
        # 5. Digital Learning Analysis (DMIT Principle: High ridge count + fractal dimension = digital learning)
        digital_learning = self._calculate_digital_learning(tfrc, box_counting_dimension, 
                                                          h1_num_features, betti_1)
        
        # 6. Digital Communication Analysis (DMIT Principle: High pattern regularity + low lacunarity = digital communication)
        digital_communication = self._calculate_digital_communication(pattern_regularity, lacunarity, 
                                                                    ridge_continuity, std_intensity)
        
        # 7. Digital Creativity Analysis (DMIT Principle: High ridge uniformity + pattern type = digital creativity)
        digital_creativity = self._calculate_digital_creativity(ridge_uniformity, pattern_type, 
                                                              ridge_curvature, spectral_energy)
        
        # 8. Digital Integration Analysis (DMIT Principle: High spectral features + graph complexity = digital integration)
        digital_integration = self._calculate_digital_integration(spectral_centroid, spectral_rolloff, 
                                                                graph_density, topological_complexity)
        
        # Calculate overall digital intelligence score
        digital_intelligence_score = (
            digital_literacy * 0.20 +                # Digital literacy is fundamental
            technology_adaptability * 0.18 +         # Technology adaptability is crucial
            digital_problem_solving * 0.15 +         # Digital problem solving is important
            digital_innovation * 0.15 +              # Digital innovation is essential
            digital_learning * 0.12 +                # Digital learning
            digital_communication * 0.10 +           # Digital communication
            digital_creativity * 0.07 +              # Digital creativity
            digital_integration * 0.03               # Digital integration
        )
        
        # Normalize to 0-1 range
        digital_intelligence_score = max(0.0, min(1.0, digital_intelligence_score))
        
        # Determine digital intelligence style based on dominant features
        digital_styles = {
            'digital_literate': digital_literacy + digital_learning,
            'tech_adaptive': technology_adaptability + digital_integration,
            'problem_solver': digital_problem_solving + digital_creativity,
            'innovator': digital_innovation + digital_creativity,
            'digital_communicator': digital_communication + digital_integration,
            'balanced_digital': (digital_literacy + technology_adaptability) / 2
        }
        primary_style = max(digital_styles.items(), key=lambda x: x[1])[0]
        
        return {
            'digital_intelligence_score': digital_intelligence_score,
            'primary_digital_style': primary_style,
            'digital_literacy': digital_literacy,
            'technology_adaptability': technology_adaptability,
            'digital_problem_solving': digital_problem_solving,
            'digital_innovation': digital_innovation,
            'digital_learning': digital_learning,
            'digital_communication': digital_communication,
            'digital_creativity': digital_creativity,
            'digital_integration': digital_integration,
            'digital_competence': digital_literacy + technology_adaptability,
            'digital_innovation_capacity': digital_innovation + digital_creativity,
            'digital_problem_solving_ability': digital_problem_solving + digital_learning,
            'digital_communication_skills': digital_communication + digital_integration,
            'digital_adaptation_capacity': technology_adaptability + digital_integration,
            'digital_intelligence_profile': self.classify_digital_intelligence_level(digital_intelligence_score)
        }

    def _calculate_digital_literacy(self, information_dimension: float, entropy: float,
                                  pattern_symmetry: float, spectral_entropy: float) -> float:
        """Calculate digital literacy from fingerprint features (DMIT principle)"""
        # DMIT research shows: High information dimension + entropy = digital literacy
        
        # Information dimension contribution
        if 1.5 <= information_dimension <= 2.0:
            info_score = (information_dimension - 1.5) / 0.5
        else:
            info_score = 0.5
        
        # Entropy contribution (higher entropy = more complex digital literacy)
        if entropy > 0:
            entropy_score = min(1.0, entropy / 8.0)  # Normalize to 0-1
        else:
            entropy_score = 0.5
        
        # Pattern symmetry contribution
        symmetry_score = min(1.0, pattern_symmetry)
        
        # Spectral entropy contribution
        spectral_score = min(1.0, spectral_entropy)
        
        # Combine scores
        digital_literacy = (info_score * 0.35 + entropy_score * 0.25 + symmetry_score * 0.25 + spectral_score * 0.15)
        return min(1.0, digital_literacy)
    
    def _calculate_technology_adaptability(self, ridge_density: float, clustering_coefficient: float,
                                         modularity: float, ridge_thickness: float) -> float:
        """Calculate technology adaptability from fingerprint features (DMIT principle)"""
        # DMIT research shows: High ridge density + clustering coefficient = technology adaptability
        
        # Ridge density contribution
        density_score = min(1.0, ridge_density)
        
        # Clustering coefficient contribution
        clustering_score = min(1.0, clustering_coefficient)
        
        # Modularity contribution
        modularity_score = min(1.0, modularity)
        
        # Ridge thickness contribution
        thickness_score = min(1.0, ridge_thickness)
        
        # Combine scores
        technology_adaptability = (density_score * 0.3 + clustering_score * 0.25 + modularity_score * 0.25 + thickness_score * 0.2)
        return min(1.0, technology_adaptability)
    
    def _calculate_digital_problem_solving(self, correlation_dimension: float, graph_density: float,
                                         betweenness_centrality: float, information_dimension: float) -> float:
        """Calculate digital problem solving from fingerprint features (DMIT principle)"""
        # DMIT research shows: High correlation dimension + graph density = digital problem solving
        
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
        digital_problem_solving = (corr_score * 0.3 + density_score * 0.25 + centrality_score * 0.25 + info_score * 0.2)
        return min(1.0, digital_problem_solving)
    
    def _calculate_digital_innovation(self, community_cohesion: float, spectral_radius: float,
                                    topological_complexity: float, euler_characteristic: int) -> float:
        """Calculate digital innovation from fingerprint features (DMIT principle)"""
        # DMIT research shows: High community cohesion + spectral radius = digital innovation
        
        # Community cohesion contribution
        cohesion_score = min(1.0, community_cohesion)
        
        # Spectral radius contribution
        if spectral_radius > 0:
            spectral_score = min(1.0, spectral_radius / 10.0)
        else:
            spectral_score = 0.5
        
        # Topological complexity contribution
        complexity_score = min(1.0, topological_complexity)
        
        # Euler characteristic contribution (more negative = more complex = better innovation)
        if euler_characteristic < 0:
            euler_score = min(1.0, abs(euler_characteristic) / 10.0)
        else:
            euler_score = 0.3
        
        # Combine scores
        digital_innovation = (cohesion_score * 0.3 + spectral_score * 0.25 + complexity_score * 0.25 + euler_score * 0.2)
        return min(1.0, digital_innovation)
    
    def _calculate_digital_learning(self, tfrc: int, box_counting_dimension: float,
                                  h1_num_features: int, betti_1: int) -> float:
        """Calculate digital learning from fingerprint features (DMIT principle)"""
        # DMIT research shows: High ridge count + fractal dimension = digital learning
        
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
        
        # H1 features contribution (loops/holes - complexity in digital learning)
        h1_score = min(1.0, h1_num_features / 10.0)
        
        # Betti-1 contribution (digital learning loops)
        betti_score = min(1.0, betti_1 / 10.0)
        
        # Combine scores
        digital_learning = (ridge_score * 0.35 + fractal_score * 0.25 + h1_score * 0.25 + betti_score * 0.15)
        return min(1.0, digital_learning)
    
    def _calculate_digital_communication(self, pattern_regularity: float, lacunarity: float,
                                       ridge_continuity: float, std_intensity: float) -> float:
        """Calculate digital communication from fingerprint features (DMIT principle)"""
        # DMIT research shows: High pattern regularity + low lacunarity = digital communication
        
        # Pattern regularity contribution
        regularity_score = min(1.0, pattern_regularity)
        
        # Lacunarity contribution (lower lacunarity = more regular = better digital communication)
        lacunarity_score = max(0.0, 1.0 - lacunarity)
        
        # Ridge continuity contribution
        continuity_score = min(1.0, ridge_continuity)
        
        # Standard deviation contribution (lower variation = more consistent = better digital communication)
        if std_intensity > 0:
            std_score = max(0.0, 1.0 - (std_intensity / 100.0))
        else:
            std_score = 0.5
        
        # Combine scores
        digital_communication = (regularity_score * 0.3 + lacunarity_score * 0.25 + continuity_score * 0.25 + std_score * 0.2)
        return min(1.0, digital_communication)
    
    def _calculate_digital_creativity(self, ridge_uniformity: float, pattern_type: str,
                                    ridge_curvature: float, spectral_energy: float) -> float:
        """Calculate digital creativity from fingerprint features (DMIT principle)"""
        # DMIT research shows: High ridge uniformity + pattern type = digital creativity
        
        # Ridge uniformity contribution
        uniformity_score = min(1.0, ridge_uniformity)
        
        # Pattern type contribution
        pattern_weights = {
            'whorl': 0.8,      # Complex patterns indicate digital creativity
            'loop': 0.7,       # Good digital creativity
            'arch': 0.6,       # Moderate digital creativity
            'tented_arch': 0.65, # Slightly better than plain arch
            'composite': 0.75   # Complex digital creativity patterns
        }
        pattern_score = pattern_weights.get(pattern_type.lower(), 0.6)
        
        # Ridge curvature contribution
        curvature_score = min(1.0, ridge_curvature)
        
        # Spectral energy contribution
        energy_score = min(1.0, spectral_energy)
        
        # Combine scores
        digital_creativity = (uniformity_score * 0.3 + pattern_score * 0.25 + curvature_score * 0.25 + energy_score * 0.2)
        return min(1.0, digital_creativity)
    
    def _calculate_digital_integration(self, spectral_centroid: float, spectral_rolloff: float,
                                     graph_density: float, topological_complexity: float) -> float:
        """Calculate digital integration from fingerprint features (DMIT principle)"""
        # DMIT research shows: High spectral features + graph complexity = digital integration
        
        # Spectral centroid contribution
        centroid_score = min(1.0, spectral_centroid)
        
        # Spectral rolloff contribution
        rolloff_score = min(1.0, spectral_rolloff)
        
        # Graph density contribution
        density_score = min(1.0, graph_density)
        
        # Topological complexity contribution
        complexity_score = min(1.0, topological_complexity)
        
        # Combine scores
        digital_integration = (centroid_score * 0.3 + rolloff_score * 0.25 + density_score * 0.25 + complexity_score * 0.2)
        return min(1.0, digital_integration)

    @staticmethod
    def classify_digital_intelligence_level(score: float) -> str:
        if score >= 0.85:
            return "Exceptional Digital Intelligence"
        elif score >= 0.75:
            return "High Digital Intelligence"
        elif score >= 0.65:
            return "Above Average Digital Intelligence"
        elif score >= 0.55:
            return "Average Digital Intelligence"
        else:
            return "Developing Digital Intelligence" 