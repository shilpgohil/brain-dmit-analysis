from typing import Dict, Any
from .base import DMITExtensionBase

class CuriosityExploratoryExtension(DMITExtensionBase):
    """
    Extension for analyzing Curiosity and Exploratory behavior patterns from fingerprint features.
    Uses comprehensive DMIT scientific correlations between fingerprint patterns and exploratory tendencies.
    """
    def analyze(self, features: Dict[str, Any]) -> Dict[str, Any]:
        # Extract comprehensive fingerprint features for curiosity exploratory analysis
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
        
        # Calculate curiosity exploratory abilities using comprehensive DMIT scientific correlations
        
        # 1. Intellectual Curiosity Analysis (DMIT Principle: High information dimension + entropy = intellectual curiosity)
        intellectual_curiosity = self._calculate_intellectual_curiosity(information_dimension, entropy, 
                                                                      pattern_symmetry, spectral_entropy)
        
        # 2. Sensory Exploration Analysis (DMIT Principle: High ridge density + clustering coefficient = sensory exploration)
        sensory_exploration = self._calculate_sensory_exploration(ridge_density, clustering_coefficient, 
                                                                modularity, ridge_thickness)
        
        # 3. Cognitive Exploration Analysis (DMIT Principle: High correlation dimension + graph density = cognitive exploration)
        cognitive_exploration = self._calculate_cognitive_exploration(correlation_dimension, graph_density, 
                                                                    betweenness_centrality, information_dimension)
        
        # 4. Behavioral Exploration Analysis (DMIT Principle: High community cohesion + spectral radius = behavioral exploration)
        behavioral_exploration = self._calculate_behavioral_exploration(community_cohesion, spectral_radius, 
                                                                      topological_complexity, euler_characteristic)
        
        # 5. Knowledge Seeking Analysis (DMIT Principle: High ridge count + fractal dimension = knowledge seeking)
        knowledge_seeking = self._calculate_knowledge_seeking(tfrc, box_counting_dimension, 
                                                            h1_num_features, betti_1)
        
        # 6. Novelty Seeking Analysis (DMIT Principle: High pattern irregularity + high lacunarity = novelty seeking)
        novelty_seeking = self._calculate_novelty_seeking(pattern_regularity, lacunarity, 
                                                        ridge_continuity, std_intensity)
        
        # 7. Risk-taking Exploration Analysis (DMIT Principle: High ridge uniformity + pattern type = risk-taking)
        risk_taking_exploration = self._calculate_risk_taking_exploration(ridge_uniformity, pattern_type, 
                                                                        ridge_curvature, spectral_energy)
        
        # 8. Adaptive Exploration Analysis (DMIT Principle: High spectral features + graph complexity = adaptive exploration)
        adaptive_exploration = self._calculate_adaptive_exploration(spectral_centroid, spectral_rolloff, 
                                                                  graph_density, topological_complexity)
        
        # Calculate overall curiosity exploratory score
        curiosity_exploratory_score = (
            intellectual_curiosity * 0.20 +          # Intellectual curiosity is fundamental
            sensory_exploration * 0.18 +             # Sensory exploration is crucial
            cognitive_exploration * 0.15 +           # Cognitive exploration is important
            behavioral_exploration * 0.15 +          # Behavioral exploration is essential
            knowledge_seeking * 0.12 +               # Knowledge seeking
            novelty_seeking * 0.10 +                 # Novelty seeking
            risk_taking_exploration * 0.07 +         # Risk-taking exploration
            adaptive_exploration * 0.03              # Adaptive exploration
        )
        
        # Normalize to 0-1 range
        curiosity_exploratory_score = max(0.0, min(1.0, curiosity_exploratory_score))
        
        # Determine curiosity exploratory style based on dominant features
        curiosity_styles = {
            'intellectual_explorer': (intellectual_curiosity + knowledge_seeking) / 2,
            'sensory_explorer': (sensory_exploration + novelty_seeking) / 2,
            'cognitive_explorer': (cognitive_exploration + adaptive_exploration) / 2,
            'behavioral_explorer': (behavioral_exploration + risk_taking_exploration) / 2,
            'novelty_seeker': (novelty_seeking + sensory_exploration) / 2,
            'balanced_explorer': (intellectual_curiosity + behavioral_exploration) / 2
        }
        primary_style = max(curiosity_styles.items(), key=lambda x: x[1])[0]
        
        return {
            'curiosity_exploratory_score': curiosity_exploratory_score,
            'primary_curiosity_style': primary_style,
            'intellectual_curiosity': intellectual_curiosity,
            'sensory_exploration': sensory_exploration,
            'cognitive_exploration': cognitive_exploration,
            'behavioral_exploration': behavioral_exploration,
            'knowledge_seeking': knowledge_seeking,
            'novelty_seeking': novelty_seeking,
            'risk_taking_exploration': risk_taking_exploration,
            'adaptive_exploration': adaptive_exploration,
            'learning_curiosity': (intellectual_curiosity + knowledge_seeking) / 2,
            'experiential_exploration': (sensory_exploration + behavioral_exploration) / 2,
            'discovery_orientation': (cognitive_exploration + adaptive_exploration) / 2,
            'adventure_seeking': (novelty_seeking + risk_taking_exploration) / 2,
            'investigative_curiosity': (intellectual_curiosity + cognitive_exploration) / 2,
            'curiosity_exploratory_profile': self.classify_curiosity_level(curiosity_exploratory_score)
        }

    def _calculate_intellectual_curiosity(self, information_dimension: float, entropy: float,
                                        pattern_symmetry: float, spectral_entropy: float) -> float:
        """Calculate intellectual curiosity from fingerprint features (DMIT principle)"""
        # DMIT research shows: High information dimension + entropy = intellectual curiosity
        
        # Information dimension contribution
        if 1.5 <= information_dimension <= 2.0:
            info_score = (information_dimension - 1.5) / 0.5
        else:
            info_score = 0.5
        
        # Entropy contribution (higher entropy = more complex intellectual curiosity)
        if entropy > 0:
            entropy_score = min(1.0, entropy / 8.0)  # Normalize to 0-1
        else:
            entropy_score = 0.5
        
        # Pattern symmetry contribution
        symmetry_score = min(1.0, pattern_symmetry)
        
        # Spectral entropy contribution
        spectral_score = min(1.0, spectral_entropy)
        
        # Combine scores
        intellectual_curiosity = (info_score * 0.35 + entropy_score * 0.25 + symmetry_score * 0.25 + spectral_score * 0.15)
        return min(1.0, intellectual_curiosity)
    
    def _calculate_sensory_exploration(self, ridge_density: float, clustering_coefficient: float,
                                     modularity: float, ridge_thickness: float) -> float:
        """Calculate sensory exploration from fingerprint features (DMIT principle)"""
        # DMIT research shows: High ridge density + clustering coefficient = sensory exploration
        
        # Ridge density contribution
        density_score = min(1.0, ridge_density)
        
        # Clustering coefficient contribution
        clustering_score = min(1.0, clustering_coefficient)
        
        # Modularity contribution
        modularity_score = min(1.0, modularity)
        
        # Ridge thickness contribution
        thickness_score = min(1.0, ridge_thickness)
        
        # Combine scores
        sensory_exploration = (density_score * 0.3 + clustering_score * 0.25 + modularity_score * 0.25 + thickness_score * 0.2)
        return min(1.0, sensory_exploration)
    
    def _calculate_cognitive_exploration(self, correlation_dimension: float, graph_density: float,
                                       betweenness_centrality: float, information_dimension: float) -> float:
        """Calculate cognitive exploration from fingerprint features (DMIT principle)"""
        # DMIT research shows: High correlation dimension + graph density = cognitive exploration
        
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
        cognitive_exploration = (corr_score * 0.3 + density_score * 0.25 + centrality_score * 0.25 + info_score * 0.2)
        return min(1.0, cognitive_exploration)
    
    def _calculate_behavioral_exploration(self, community_cohesion: float, spectral_radius: float,
                                        topological_complexity: float, euler_characteristic: int) -> float:
        """Calculate behavioral exploration from fingerprint features (DMIT principle)"""
        # DMIT research shows: High community cohesion + spectral radius = behavioral exploration
        
        # Community cohesion contribution
        cohesion_score = min(1.0, community_cohesion)
        
        # Spectral radius contribution
        if spectral_radius > 0:
            spectral_score = min(1.0, spectral_radius / 10.0)
        else:
            spectral_score = 0.5
        
        # Topological complexity contribution
        complexity_score = min(1.0, topological_complexity)
        
        # Euler characteristic contribution (more negative = more complex = better exploration)
        if euler_characteristic < 0:
            euler_score = min(1.0, abs(euler_characteristic) / 10.0)
        else:
            euler_score = 0.3
        
        # Combine scores
        behavioral_exploration = (cohesion_score * 0.3 + spectral_score * 0.25 + complexity_score * 0.25 + euler_score * 0.2)
        return min(1.0, behavioral_exploration)
    
    def _calculate_knowledge_seeking(self, tfrc: int, box_counting_dimension: float,
                                   h1_num_features: int, betti_1: int) -> float:
        """Calculate knowledge seeking from fingerprint features (DMIT principle)"""
        # DMIT research shows: High ridge count + fractal dimension = knowledge seeking
        
        # Ridge count contribution
        ridge_score = min(1.0, float(tfrc or 0))  # FIX: per-finger TFRC 0-30, not 0-1500  # FIX: per-finger TFRC 0-30
        
        # Fractal dimension contribution
        if 1.5 <= box_counting_dimension <= 2.0:
            fractal_score = (box_counting_dimension - 1.5) / 0.5
        else:
            fractal_score = 0.5
        
        # H1 features contribution (loops/holes - complexity in knowledge seeking)
        h1_score = min(1.0, h1_num_features / 10.0)
        
        # Betti-1 contribution (knowledge seeking loops)
        betti_score = min(1.0, betti_1 / 10.0)
        
        # Combine scores
        knowledge_seeking = (ridge_score * 0.35 + fractal_score * 0.25 + h1_score * 0.25 + betti_score * 0.15)
        return min(1.0, knowledge_seeking)
    
    def _calculate_novelty_seeking(self, pattern_regularity: float, lacunarity: float,
                                 ridge_continuity: float, std_intensity: float) -> float:
        """Calculate novelty seeking from fingerprint features (DMIT principle)"""
        # DMIT research shows: High pattern irregularity + high lacunarity = novelty seeking
        
        # Pattern irregularity contribution (inverse of regularity)
        irregularity_score = max(0.0, 1.0 - pattern_regularity)
        
        # Lacunarity contribution (higher lacunarity = more irregular = better novelty seeking)
        lacunarity_score = min(1.0, lacunarity)
        
        # Ridge discontinuity contribution (inverse of continuity)
        discontinuity_score = max(0.0, 1.0 - ridge_continuity)
        
        # Standard deviation contribution (higher variation = more novel = better novelty seeking)
        if std_intensity > 0:
            std_score = min(1.0, std_intensity / 100.0)
        else:
            std_score = 0.5
        
        # Combine scores
        novelty_seeking = (irregularity_score * 0.3 + lacunarity_score * 0.25 + discontinuity_score * 0.25 + std_score * 0.2)
        return min(1.0, novelty_seeking)
    
    def _calculate_risk_taking_exploration(self, ridge_uniformity: float, pattern_type: str,
                                         ridge_curvature: float, spectral_energy: float) -> float:
        """Calculate risk-taking exploration from fingerprint features (DMIT principle)"""
        # DMIT research shows: High ridge uniformity + pattern type = risk-taking exploration
        
        # Ridge uniformity contribution
        uniformity_score = min(1.0, ridge_uniformity)
        
        # Pattern type contribution
        pattern_weights = {
            'whorl': 0.8,      # Complex patterns indicate risk-taking
            'loop': 0.7,       # Good risk-taking
            'arch': 0.6,       # Moderate risk-taking
            'tented_arch': 0.65, # Slightly better than plain arch
            'composite': 0.75   # Complex risk-taking patterns
        }
        pattern_score = pattern_weights.get(pattern_type.lower(), 0.6)
        
        # Ridge curvature contribution
        curvature_score = min(1.0, ridge_curvature)
        
        # Spectral energy contribution
        energy_score = min(1.0, spectral_energy)
        
        # Combine scores
        risk_taking_exploration = (uniformity_score * 0.3 + pattern_score * 0.25 + curvature_score * 0.25 + energy_score * 0.2)
        return min(1.0, risk_taking_exploration)
    
    def _calculate_adaptive_exploration(self, spectral_centroid: float, spectral_rolloff: float,
                                      graph_density: float, topological_complexity: float) -> float:
        """Calculate adaptive exploration from fingerprint features (DMIT principle)"""
        # DMIT research shows: High spectral features + graph complexity = adaptive exploration
        
        # Spectral centroid contribution
        centroid_score = min(1.0, spectral_centroid)
        
        # Spectral rolloff contribution
        rolloff_score = min(1.0, spectral_rolloff)
        
        # Graph density contribution
        density_score = min(1.0, graph_density)
        
        # Topological complexity contribution
        complexity_score = min(1.0, topological_complexity)
        
        # Combine scores
        adaptive_exploration = (centroid_score * 0.3 + rolloff_score * 0.25 + density_score * 0.25 + complexity_score * 0.2)
        return min(1.0, adaptive_exploration)

    @staticmethod
    def classify_curiosity_level(score: float) -> str:
        if score >= 0.85:
            return "Exceptional Curiosity and Exploration"
        elif score >= 0.75:
            return "High Curiosity and Exploration"
        elif score >= 0.65:
            return "Above Average Curiosity and Exploration"
        elif score >= 0.55:
            return "Average Curiosity and Exploration"
        else:
            return "Developing Curiosity and Exploration" 