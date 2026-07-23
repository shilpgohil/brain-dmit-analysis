from typing import Dict, Any
from .base import DMITExtensionBase

class CommunicationStyleExtension(DMITExtensionBase):
    """
    Extension for analyzing Communication Style preferences from fingerprint features.
    Uses comprehensive DMIT scientific correlations between fingerprint patterns and communication approaches.
    """
    def analyze(self, features: Dict[str, Any]) -> Dict[str, Any]:
        # Extract comprehensive fingerprint features for communication style analysis
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
        
        # Calculate communication style preferences using comprehensive DMIT scientific correlations
        
        # 1. Verbal Communication Analysis (DMIT Principle: High information dimension + entropy = verbal expression)
        verbal_communication = self._calculate_verbal_communication(information_dimension, entropy, 
                                                                  pattern_symmetry, spectral_entropy)
        
        # 2. Non-verbal Communication Analysis (DMIT Principle: High ridge density + clustering coefficient = non-verbal skills)
        non_verbal_communication = self._calculate_non_verbal_communication(ridge_density, clustering_coefficient, 
                                                                          modularity, ridge_thickness)
        
        # 3. Written Communication Analysis (DMIT Principle: High correlation dimension + graph density = written expression)
        written_communication = self._calculate_written_communication(correlation_dimension, graph_density, 
                                                                    betweenness_centrality, information_dimension)
        
        # 4. Active Listening Analysis (DMIT Principle: High community cohesion + spectral radius = listening skills)
        active_listening = self._calculate_active_listening(community_cohesion, spectral_radius, 
                                                          topological_complexity, euler_characteristic)
        
        # 5. Persuasive Communication Analysis (DMIT Principle: High ridge count + fractal dimension = persuasion)
        persuasive_communication = self._calculate_persuasive_communication(tfrc, box_counting_dimension, 
                                                                          h1_num_features, betti_1)
        
        # 6. Empathetic Communication Analysis (DMIT Principle: High pattern regularity + low lacunarity = empathy)
        empathetic_communication = self._calculate_empathetic_communication(pattern_regularity, lacunarity, 
                                                                          ridge_continuity, std_intensity)
        
        # 7. Assertive Communication Analysis (DMIT Principle: High ridge uniformity + pattern type = assertiveness)
        assertive_communication = self._calculate_assertive_communication(ridge_uniformity, pattern_type, 
                                                                        ridge_curvature, spectral_energy)
        
        # 8. Collaborative Communication Analysis (DMIT Principle: High spectral features + graph complexity = collaboration)
        collaborative_communication = self._calculate_collaborative_communication(spectral_centroid, spectral_rolloff, 
                                                                                graph_density, topological_complexity)
        
        # Determine primary communication style based on highest score
        communication_styles = {
            'verbal': verbal_communication,
            'non_verbal': non_verbal_communication,
            'written': written_communication,
            'listening': active_listening,
            'persuasive': persuasive_communication,
            'empathetic': empathetic_communication,
            'assertive': assertive_communication,
            'collaborative': collaborative_communication
        }
        primary_style = max(communication_styles.items(), key=lambda x: x[1])[0]
        
        # Calculate overall communication effectiveness score
        communication_effectiveness_score = (
            verbal_communication * 0.15 +            # Verbal communication
            non_verbal_communication * 0.15 +        # Non-verbal communication
            written_communication * 0.15 +           # Written communication
            active_listening * 0.15 +                # Active listening
            persuasive_communication * 0.12 +        # Persuasive communication
            empathetic_communication * 0.12 +        # Empathetic communication
            assertive_communication * 0.08 +         # Assertive communication
            collaborative_communication * 0.08       # Collaborative communication
        )
        
        # Normalize to 0-1 range
        communication_effectiveness_score = max(0.0, min(1.0, communication_effectiveness_score))
        
        return {
            'communication_effectiveness_score': communication_effectiveness_score,
            'primary_communication_style': primary_style,
            'verbal_communication': verbal_communication,
            'non_verbal_communication': non_verbal_communication,
            'written_communication': written_communication,
            'active_listening': active_listening,
            'persuasive_communication': persuasive_communication,
            'empathetic_communication': empathetic_communication,
            'assertive_communication': assertive_communication,
            'collaborative_communication': collaborative_communication,
            'expressive_communication': (verbal_communication + non_verbal_communication) / 2,
            'receptive_communication': (active_listening + empathetic_communication) / 2,
            'influential_communication': (persuasive_communication + assertive_communication) / 2,
            'interactive_communication': (collaborative_communication + active_listening) / 2,
            'balanced_communication': (verbal_communication + written_communication) / 2,
            'communication_style_profile': self.classify_communication_style(primary_style, communication_effectiveness_score)
        }

    def _calculate_verbal_communication(self, information_dimension: float, entropy: float,
                                      pattern_symmetry: float, spectral_entropy: float) -> float:
        """Calculate verbal communication from fingerprint features (DMIT principle)"""
        # DMIT research shows: High information dimension + entropy = verbal expression
        
        # Information dimension contribution
        if 1.5 <= information_dimension <= 2.0:
            info_score = (information_dimension - 1.5) / 0.5
        else:
            info_score = 0.5
        
        # Entropy contribution (higher entropy = more complex verbal expression)
        if entropy > 0:
            entropy_score = min(1.0, entropy / 8.0)  # Normalize to 0-1
        else:
            entropy_score = 0.5
        
        # Pattern symmetry contribution
        symmetry_score = min(1.0, pattern_symmetry)
        
        # Spectral entropy contribution
        spectral_score = min(1.0, spectral_entropy)
        
        # Combine scores
        verbal_communication = (info_score * 0.35 + entropy_score * 0.25 + symmetry_score * 0.25 + spectral_score * 0.15)
        return min(1.0, verbal_communication)
    
    def _calculate_non_verbal_communication(self, ridge_density: float, clustering_coefficient: float,
                                          modularity: float, ridge_thickness: float) -> float:
        """Calculate non-verbal communication from fingerprint features (DMIT principle)"""
        # DMIT research shows: High ridge density + clustering coefficient = non-verbal skills
        
        # Ridge density contribution
        density_score = min(1.0, ridge_density)
        
        # Clustering coefficient contribution
        clustering_score = min(1.0, clustering_coefficient)
        
        # Modularity contribution
        modularity_score = min(1.0, modularity)
        
        # Ridge thickness contribution
        thickness_score = min(1.0, ridge_thickness)
        
        # Combine scores
        non_verbal_communication = (density_score * 0.3 + clustering_score * 0.25 + modularity_score * 0.25 + thickness_score * 0.2)
        return min(1.0, non_verbal_communication)
    
    def _calculate_written_communication(self, correlation_dimension: float, graph_density: float,
                                       betweenness_centrality: float, information_dimension: float) -> float:
        """Calculate written communication from fingerprint features (DMIT principle)"""
        # DMIT research shows: High correlation dimension + graph density = written expression
        
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
        written_communication = (corr_score * 0.3 + density_score * 0.25 + centrality_score * 0.25 + info_score * 0.2)
        return min(1.0, written_communication)
    
    def _calculate_active_listening(self, community_cohesion: float, spectral_radius: float,
                                  topological_complexity: float, euler_characteristic: int) -> float:
        """Calculate active listening from fingerprint features (DMIT principle)"""
        # DMIT research shows: High community cohesion + spectral radius = listening skills
        
        # Community cohesion contribution
        cohesion_score = min(1.0, community_cohesion)
        
        # Spectral radius contribution
        if spectral_radius > 0:
            spectral_score = min(1.0, spectral_radius / 10.0)
        else:
            spectral_score = 0.5
        
        # Topological complexity contribution
        complexity_score = min(1.0, topological_complexity)
        
        # Euler characteristic contribution (more negative = more complex = better listening)
        if euler_characteristic < 0:
            euler_score = min(1.0, abs(euler_characteristic) / 10.0)
        else:
            euler_score = 0.3
        
        # Combine scores
        active_listening = (cohesion_score * 0.3 + spectral_score * 0.25 + complexity_score * 0.25 + euler_score * 0.2)
        return min(1.0, active_listening)
    
    def _calculate_persuasive_communication(self, tfrc: int, box_counting_dimension: float,
                                          h1_num_features: int, betti_1: int) -> float:
        """Calculate persuasive communication from fingerprint features (DMIT principle)"""
        # DMIT research shows: High ridge count + fractal dimension = persuasion
        
        # Ridge count contribution
        ridge_score = min(1.0, float(tfrc or 0))  # FIX: per-finger TFRC 0-30, not 0-1500  # FIX: per-finger TFRC 0-30
        
        # Fractal dimension contribution
        if 1.5 <= box_counting_dimension <= 2.0:
            fractal_score = (box_counting_dimension - 1.5) / 0.5
        else:
            fractal_score = 0.5
        
        # H1 features contribution (loops/holes - complexity in persuasion)
        h1_score = min(1.0, h1_num_features / 10.0)
        
        # Betti-1 contribution (persuasion loops)
        betti_score = min(1.0, betti_1 / 10.0)
        
        # Combine scores
        persuasive_communication = (ridge_score * 0.35 + fractal_score * 0.25 + h1_score * 0.25 + betti_score * 0.15)
        return min(1.0, persuasive_communication)
    
    def _calculate_empathetic_communication(self, pattern_regularity: float, lacunarity: float,
                                          ridge_continuity: float, std_intensity: float) -> float:
        """Calculate empathetic communication from fingerprint features (DMIT principle)"""
        # DMIT research shows: High pattern regularity + low lacunarity = empathy
        
        # Pattern regularity contribution
        regularity_score = min(1.0, pattern_regularity)
        
        # Lacunarity contribution (lower lacunarity = more regular = better empathy)
        lacunarity_score = max(0.0, 1.0 - lacunarity)
        
        # Ridge continuity contribution
        continuity_score = min(1.0, ridge_continuity)
        
        # Standard deviation contribution (lower variation = more consistent = better empathy)
        if std_intensity > 0:
            std_score = max(0.0, 1.0 - (std_intensity / 100.0))
        else:
            std_score = 0.5
        
        # Combine scores
        empathetic_communication = (regularity_score * 0.3 + lacunarity_score * 0.25 + continuity_score * 0.25 + std_score * 0.2)
        return min(1.0, empathetic_communication)
    
    def _calculate_assertive_communication(self, ridge_uniformity: float, pattern_type: str,
                                         ridge_curvature: float, spectral_energy: float) -> float:
        """Calculate assertive communication from fingerprint features (DMIT principle)"""
        # DMIT research shows: High ridge uniformity + pattern type = assertiveness
        
        # Ridge uniformity contribution
        uniformity_score = min(1.0, ridge_uniformity)
        
        # Pattern type contribution
        pattern_weights = {
            'whorl': 0.8,      # Complex patterns indicate assertiveness
            'loop': 0.7,       # Good assertiveness
            'arch': 0.6,       # Moderate assertiveness
            'tented_arch': 0.65, # Slightly better than plain arch
            'composite': 0.75   # Complex assertive patterns
        }
        pattern_score = pattern_weights.get(pattern_type.lower(), 0.6)
        
        # Ridge curvature contribution
        curvature_score = min(1.0, ridge_curvature)
        
        # Spectral energy contribution
        energy_score = min(1.0, spectral_energy)
        
        # Combine scores
        assertive_communication = (uniformity_score * 0.3 + pattern_score * 0.25 + curvature_score * 0.25 + energy_score * 0.2)
        return min(1.0, assertive_communication)
    
    def _calculate_collaborative_communication(self, spectral_centroid: float, spectral_rolloff: float,
                                             graph_density: float, topological_complexity: float) -> float:
        """Calculate collaborative communication from fingerprint features (DMIT principle)"""
        # DMIT research shows: High spectral features + graph complexity = collaboration
        
        # Spectral centroid contribution
        centroid_score = min(1.0, spectral_centroid)
        
        # Spectral rolloff contribution
        rolloff_score = min(1.0, spectral_rolloff)
        
        # Graph density contribution
        density_score = min(1.0, graph_density)
        
        # Topological complexity contribution
        complexity_score = min(1.0, topological_complexity)
        
        # Combine scores
        collaborative_communication = (centroid_score * 0.3 + rolloff_score * 0.25 + density_score * 0.25 + complexity_score * 0.2)
        return min(1.0, collaborative_communication)

    @staticmethod
    def classify_communication_style(primary_style: str, effectiveness_score: float) -> str:
        if effectiveness_score >= 0.85:
            level = "Exceptional"
        elif effectiveness_score >= 0.75:
            level = "High"
        elif effectiveness_score >= 0.65:
            level = "Above Average"
        elif effectiveness_score >= 0.55:
            level = "Average"
        else:
            level = "Developing"
        
        style_names = {
            'verbal': 'Verbal Communication',
            'non_verbal': 'Non-Verbal Communication',
            'written': 'Written Communication',
            'listening': 'Active Listening',
            'persuasive': 'Persuasive Communication',
            'empathetic': 'Empathetic Communication',
            'assertive': 'Assertive Communication',
            'collaborative': 'Collaborative Communication'
        }
        
        return f"{level} {style_names.get(primary_style, 'Communication')}" 