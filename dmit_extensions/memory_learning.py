from typing import Dict, Any
from .base import DMITExtensionBase

class MemoryLearningExtension(DMITExtensionBase):
    """
    Extension for analyzing Memory and Learning abilities from fingerprint features.
    Uses comprehensive DMIT scientific correlations between fingerprint patterns and memory-learning capabilities.
    """
    def analyze(self, features: Dict[str, Any]) -> Dict[str, Any]:
        # Extract comprehensive fingerprint features for memory learning analysis
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
        
        # Calculate memory learning abilities using comprehensive DMIT scientific correlations
        
        # 1. Memory Capacity Analysis (DMIT Principle: High information dimension + entropy = memory capacity)
        memory_capacity = self._calculate_memory_capacity(information_dimension, entropy, 
                                                        pattern_symmetry, spectral_entropy)
        
        # 2. Learning Speed Analysis (DMIT Principle: High ridge density + clustering coefficient = learning speed)
        learning_speed = self._calculate_learning_speed(ridge_density, clustering_coefficient, 
                                                      modularity, ridge_thickness)
        
        # 3. Information Retention Analysis (DMIT Principle: High correlation dimension + graph density = information retention)
        information_retention = self._calculate_information_retention(correlation_dimension, graph_density, 
                                                                    betweenness_centrality, information_dimension)
        
        # 4. Knowledge Integration Analysis (DMIT Principle: High community cohesion + spectral radius = knowledge integration)
        knowledge_integration = self._calculate_knowledge_integration(community_cohesion, spectral_radius, 
                                                                    topological_complexity, euler_characteristic)
        
        # 5. Recall Ability Analysis (DMIT Principle: High ridge count + fractal dimension = recall ability)
        recall_ability = self._calculate_recall_ability(tfrc, box_counting_dimension, 
                                                      h1_num_features, betti_1)
        
        # 6. Learning Efficiency Analysis (DMIT Principle: High pattern regularity + low lacunarity = learning efficiency)
        learning_efficiency = self._calculate_learning_efficiency(pattern_regularity, lacunarity, 
                                                                ridge_continuity, std_intensity)
        
        # 7. Memory Consolidation Analysis (DMIT Principle: High ridge uniformity + pattern type = memory consolidation)
        memory_consolidation = self._calculate_memory_consolidation(ridge_uniformity, pattern_type, 
                                                                  ridge_curvature, spectral_energy)
        
        # 8. Adaptive Learning Analysis (DMIT Principle: High spectral features + graph complexity = adaptive learning)
        adaptive_learning = self._calculate_adaptive_learning(spectral_centroid, spectral_rolloff, 
                                                            graph_density, topological_complexity)
        
        # Calculate overall memory learning score
        memory_learning_score = (
            memory_capacity * 0.20 +                 # Memory capacity is fundamental
            learning_speed * 0.18 +                  # Learning speed is crucial
            information_retention * 0.15 +           # Information retention is important
            knowledge_integration * 0.15 +           # Knowledge integration is essential
            recall_ability * 0.12 +                  # Recall ability
            learning_efficiency * 0.10 +             # Learning efficiency
            memory_consolidation * 0.07 +            # Memory consolidation
            adaptive_learning * 0.03                 # Adaptive learning
        )
        
        # Normalize to 0-1 range
        memory_learning_score = max(0.0, min(1.0, memory_learning_score))
        
        # Determine memory learning style based on dominant features
        memory_styles = {
            'memory_strong': (memory_capacity + recall_ability) / 2,
            'fast_learner': (learning_speed + learning_efficiency) / 2,
            'knowledge_integrator': (knowledge_integration + information_retention) / 2,
            'adaptive_learner': (adaptive_learning + memory_consolidation) / 2,
            'retention_expert': (information_retention + memory_consolidation) / 2,
            'balanced_learner': (memory_capacity + learning_speed) / 2
        }
        primary_style = max(memory_styles.items(), key=lambda x: x[1])[0]
        
        return {
            'memory_learning_score': memory_learning_score,
            'primary_memory_style': primary_style,
            'memory_capacity': memory_capacity,
            'learning_speed': learning_speed,
            'information_retention': information_retention,
            'knowledge_integration': knowledge_integration,
            'recall_ability': recall_ability,
            'learning_efficiency': learning_efficiency,
            'memory_consolidation': memory_consolidation,
            'adaptive_learning': adaptive_learning,
            'memory_performance': (memory_capacity + recall_ability) / 2,
            'learning_effectiveness': (learning_speed + learning_efficiency) / 2,
            'knowledge_management': (information_retention + knowledge_integration) / 2,
            'memory_adaptability': (adaptive_learning + memory_consolidation) / 2,
            'cognitive_learning': (memory_capacity + learning_speed) / 2,
            'memory_learning_profile': self.classify_memory_learning_level(memory_learning_score)
        }

    def _calculate_memory_capacity(self, information_dimension: float, entropy: float,
                                 pattern_symmetry: float, spectral_entropy: float) -> float:
        """Calculate memory capacity from fingerprint features (DMIT principle)"""
        # DMIT research shows: High information dimension + entropy = memory capacity
        
        # Information dimension contribution
        if 1.5 <= information_dimension <= 2.0:
            info_score = (information_dimension - 1.5) / 0.5
        else:
            info_score = 0.5
        
        # Entropy contribution (higher entropy = more complex memory capacity)
        if entropy > 0:
            entropy_score = min(1.0, entropy / 8.0)  # Normalize to 0-1
        else:
            entropy_score = 0.5
        
        # Pattern symmetry contribution
        symmetry_score = min(1.0, pattern_symmetry)
        
        # Spectral entropy contribution
        spectral_score = min(1.0, spectral_entropy)
        
        # Combine scores
        memory_capacity = (info_score * 0.35 + entropy_score * 0.25 + symmetry_score * 0.25 + spectral_score * 0.15)
        return min(1.0, memory_capacity)
    
    def _calculate_learning_speed(self, ridge_density: float, clustering_coefficient: float,
                                modularity: float, ridge_thickness: float) -> float:
        """Calculate learning speed from fingerprint features (DMIT principle)"""
        # DMIT research shows: High ridge density + clustering coefficient = learning speed
        
        # Ridge density contribution
        density_score = min(1.0, ridge_density)
        
        # Clustering coefficient contribution
        clustering_score = min(1.0, clustering_coefficient)
        
        # Modularity contribution
        modularity_score = min(1.0, modularity)
        
        # Ridge thickness contribution
        thickness_score = min(1.0, ridge_thickness)
        
        # Combine scores
        learning_speed = (density_score * 0.3 + clustering_score * 0.25 + modularity_score * 0.25 + thickness_score * 0.2)
        return min(1.0, learning_speed)
    
    def _calculate_information_retention(self, correlation_dimension: float, graph_density: float,
                                       betweenness_centrality: float, information_dimension: float) -> float:
        """Calculate information retention from fingerprint features (DMIT principle)"""
        # DMIT research shows: High correlation dimension + graph density = information retention
        
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
        information_retention = (corr_score * 0.3 + density_score * 0.25 + centrality_score * 0.25 + info_score * 0.2)
        return min(1.0, information_retention)
    
    def _calculate_knowledge_integration(self, community_cohesion: float, spectral_radius: float,
                                       topological_complexity: float, euler_characteristic: int) -> float:
        """Calculate knowledge integration from fingerprint features (DMIT principle)"""
        # DMIT research shows: High community cohesion + spectral radius = knowledge integration
        
        # Community cohesion contribution
        cohesion_score = min(1.0, community_cohesion)
        
        # Spectral radius contribution
        if spectral_radius > 0:
            spectral_score = min(1.0, spectral_radius / 10.0)
        else:
            spectral_score = 0.5
        
        # Topological complexity contribution
        complexity_score = min(1.0, topological_complexity)
        
        # Euler characteristic contribution (more negative = more complex = better knowledge integration)
        if euler_characteristic < 0:
            euler_score = min(1.0, abs(euler_characteristic) / 10.0)
        else:
            euler_score = 0.3
        
        # Combine scores
        knowledge_integration = (cohesion_score * 0.3 + spectral_score * 0.25 + complexity_score * 0.25 + euler_score * 0.2)
        return min(1.0, knowledge_integration)
    
    def _calculate_recall_ability(self, tfrc: int, box_counting_dimension: float,
                                h1_num_features: int, betti_1: int) -> float:
        """Calculate recall ability from fingerprint features (DMIT principle)"""
        # DMIT research shows: High ridge count + fractal dimension = recall ability
        
        # Ridge count contribution
        ridge_score = min(1.0, float(tfrc or 0))  # FIX: per-finger TFRC 0-30, not 0-1500  # FIX: per-finger TFRC 0-30
        
        # Fractal dimension contribution
        if 1.5 <= box_counting_dimension <= 2.0:
            fractal_score = (box_counting_dimension - 1.5) / 0.5
        else:
            fractal_score = 0.5
        
        # H1 features contribution (loops/holes - complexity in recall ability)
        h1_score = min(1.0, h1_num_features / 10.0)
        
        # Betti-1 contribution (recall ability loops)
        betti_score = min(1.0, betti_1 / 10.0)
        
        # Combine scores
        recall_ability = (ridge_score * 0.35 + fractal_score * 0.25 + h1_score * 0.25 + betti_score * 0.15)
        return min(1.0, recall_ability)
    
    def _calculate_learning_efficiency(self, pattern_regularity: float, lacunarity: float,
                                     ridge_continuity: float, std_intensity: float) -> float:
        """Calculate learning efficiency from fingerprint features (DMIT principle)"""
        # DMIT research shows: High pattern regularity + low lacunarity = learning efficiency
        
        # Pattern regularity contribution
        regularity_score = min(1.0, pattern_regularity)
        
        # Lacunarity contribution (lower lacunarity = more regular = better learning efficiency)
        lacunarity_score = max(0.0, 1.0 - lacunarity)
        
        # Ridge continuity contribution
        continuity_score = min(1.0, ridge_continuity)
        
        # Standard deviation contribution (lower variation = more consistent = better learning efficiency)
        if std_intensity > 0:
            std_score = max(0.0, 1.0 - (std_intensity / 100.0))
        else:
            std_score = 0.5
        
        # Combine scores
        learning_efficiency = (regularity_score * 0.3 + lacunarity_score * 0.25 + continuity_score * 0.25 + std_score * 0.2)
        return min(1.0, learning_efficiency)
    
    def _calculate_memory_consolidation(self, ridge_uniformity: float, pattern_type: str,
                                      ridge_curvature: float, spectral_energy: float) -> float:
        """Calculate memory consolidation from fingerprint features (DMIT principle)"""
        # DMIT research shows: High ridge uniformity + pattern type = memory consolidation
        
        # Ridge uniformity contribution
        uniformity_score = min(1.0, ridge_uniformity)
        
        # Pattern type contribution
        pattern_weights = {
            'whorl': 0.8,      # Complex patterns indicate memory consolidation
            'loop': 0.7,       # Good memory consolidation
            'arch': 0.6,       # Moderate memory consolidation
            'tented_arch': 0.65, # Slightly better than plain arch
            'composite': 0.75   # Complex memory consolidation patterns
        }
        pattern_score = pattern_weights.get(pattern_type.lower(), 0.6)
        
        # Ridge curvature contribution
        curvature_score = min(1.0, ridge_curvature)
        
        # Spectral energy contribution
        energy_score = min(1.0, spectral_energy)
        
        # Combine scores
        memory_consolidation = (uniformity_score * 0.3 + pattern_score * 0.25 + curvature_score * 0.25 + energy_score * 0.2)
        return min(1.0, memory_consolidation)
    
    def _calculate_adaptive_learning(self, spectral_centroid: float, spectral_rolloff: float,
                                   graph_density: float, topological_complexity: float) -> float:
        """Calculate adaptive learning from fingerprint features (DMIT principle)"""
        # DMIT research shows: High spectral features + graph complexity = adaptive learning
        
        # Spectral centroid contribution
        centroid_score = min(1.0, spectral_centroid)
        
        # Spectral rolloff contribution
        rolloff_score = min(1.0, spectral_rolloff)
        
        # Graph density contribution
        density_score = min(1.0, graph_density)
        
        # Topological complexity contribution
        complexity_score = min(1.0, topological_complexity)
        
        # Combine scores
        adaptive_learning = (centroid_score * 0.3 + rolloff_score * 0.25 + density_score * 0.25 + complexity_score * 0.2)
        return min(1.0, adaptive_learning)

    @staticmethod
    def classify_memory_learning_level(score: float) -> str:
        if score >= 0.85:
            return "Exceptional Memory and Learning"
        elif score >= 0.75:
            return "High Memory and Learning"
        elif score >= 0.65:
            return "Above Average Memory and Learning"
        elif score >= 0.55:
            return "Average Memory and Learning"
        else:
            return "Developing Memory and Learning" 
