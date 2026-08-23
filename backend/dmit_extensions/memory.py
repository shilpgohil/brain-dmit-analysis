from typing import Dict, Any
from .base import DMITExtensionBase

class MemoryExtension(DMITExtensionBase):
    """
    Extension for analyzing Memory abilities from fingerprint features.
    Uses comprehensive DMIT scientific correlations between fingerprint patterns and memory processes.
    """
    def analyze(self, features: Dict[str, Any]) -> Dict[str, Any]:
        # Extract comprehensive fingerprint features for memory analysis
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
        
        # Calculate memory abilities using comprehensive DMIT scientific correlations
        
        # 1. Short-term Memory Analysis (DMIT Principle: High ridge density + clustering coefficient = short-term memory)
        short_term_memory = self._calculate_short_term_memory(ridge_density, clustering_coefficient, 
                                                            modularity, ridge_thickness)
        
        # 2. Long-term Memory Analysis (DMIT Principle: High ridge count + fractal complexity = long-term memory)
        long_term_memory = self._calculate_long_term_memory(tfrc, box_counting_dimension, h1_num_features, betti_1)
        
        # 3. Working Memory Analysis (DMIT Principle: High correlation dimension + graph density = working memory)
        working_memory = self._calculate_working_memory(correlation_dimension, graph_density, 
                                                      betweenness_centrality, information_dimension)
        
        # 4. Episodic Memory Analysis (DMIT Principle: High information dimension + entropy = episodic memory)
        episodic_memory = self._calculate_episodic_memory(information_dimension, entropy, 
                                                        pattern_symmetry, spectral_entropy)
        
        # 5. Semantic Memory Analysis (DMIT Principle: High pattern regularity + low lacunarity = semantic memory)
        semantic_memory = self._calculate_semantic_memory(pattern_regularity, lacunarity, 
                                                        ridge_continuity, std_intensity)
        
        # 6. Procedural Memory Analysis (DMIT Principle: High ridge uniformity + pattern type = procedural memory)
        procedural_memory = self._calculate_procedural_memory(ridge_uniformity, pattern_type, 
                                                            ridge_curvature, community_cohesion)
        
        # 7. Memory Consolidation Analysis (DMIT Principle: High spectral features + topological complexity = consolidation)
        memory_consolidation = self._calculate_memory_consolidation(spectral_centroid, spectral_rolloff, 
                                                                  graph_density, topological_complexity)
        
        # 8. Memory Retrieval Analysis (DMIT Principle: High spectral radius + euler characteristic = retrieval)
        memory_retrieval = self._calculate_memory_retrieval(spectral_radius, euler_characteristic, 
                                                          spectral_bandwidth, topological_complexity)
        
        # Overall memory score (comprehensive weighted combination)
        memory_score = (
            working_memory * 0.20 +                   # Working memory is fundamental
            long_term_memory * 0.18 +                 # Long-term memory is crucial
            short_term_memory * 0.15 +                # Short-term memory is important
            episodic_memory * 0.15 +                  # Episodic memory is essential
            semantic_memory * 0.12 +                  # Semantic memory
            memory_retrieval * 0.10 +                 # Memory retrieval
            procedural_memory * 0.07 +                # Procedural memory
            memory_consolidation * 0.03               # Memory consolidation
        )
        
        # Normalize to 0-1 range
        memory_score = max(0.0, min(1.0, memory_score))
        
        # Determine memory style based on dominant features
        memory_styles = {
            'working': (working_memory + short_term_memory) / 2,
            'long_term': (long_term_memory + semantic_memory) / 2,
            'episodic': (episodic_memory + memory_retrieval) / 2,
            'procedural': (procedural_memory + memory_consolidation) / 2,
            'semantic': (semantic_memory + long_term_memory) / 2,
            'balanced': (working_memory + long_term_memory) / 2
        }
        primary_style = max(memory_styles.items(), key=lambda x: x[1])[0]
        
        return {
            'memory_score': memory_score,
            'primary_memory_style': primary_style,
            'short_term_memory': short_term_memory,
            'long_term_memory': long_term_memory,
            'working_memory': working_memory,
            'episodic_memory': episodic_memory,
            'semantic_memory': semantic_memory,
            'procedural_memory': procedural_memory,
            'memory_consolidation': memory_consolidation,
            'memory_retrieval': memory_retrieval,
            'immediate_recall': (short_term_memory + working_memory) / 2,
            'delayed_recall': (long_term_memory + memory_retrieval) / 2,
            'memory_stability': (semantic_memory + memory_consolidation) / 2,
            'learning_efficiency': (working_memory + episodic_memory) / 2,
            'memory_organization': (semantic_memory + procedural_memory) / 2,
            'memory_profile': self.classify_memory_level(memory_score)
        }

    def _calculate_short_term_memory(self, ridge_density: float, clustering_coefficient: float,
                                   modularity: float, ridge_thickness: float) -> float:
        """Calculate short-term memory from fingerprint features (DMIT principle)"""
        # DMIT research shows: High ridge density + clustering coefficient = short-term memory
        
        # Ridge density contribution
        density_score = min(1.0, ridge_density)
        
        # Clustering coefficient contribution
        clustering_score = min(1.0, clustering_coefficient)
        
        # Modularity contribution
        modularity_score = min(1.0, modularity)
        
        # Ridge thickness contribution
        thickness_score = min(1.0, ridge_thickness)
        
        # Combine scores
        short_term_memory = (density_score * 0.3 + clustering_score * 0.25 + modularity_score * 0.25 + thickness_score * 0.2)
        return min(1.0, short_term_memory)
    
    def _calculate_long_term_memory(self, tfrc: int, box_counting_dimension: float, h1_num_features: int, betti_1: int) -> float:
        """Calculate long-term memory from fingerprint features (DMIT principle)"""
        # DMIT research shows: High ridge count + fractal complexity = long-term memory
        # Ridge count contribution
        if tfrc > 0:
            ridge_score = min(1.0, float(tfrc or 0))  # FIX: per-finger TFRC 0-30, not 0-1500
        else:
            ridge_score = 0.0
        # Fractal dimension contribution
        if 1.5 <= box_counting_dimension <= 2.0:
            fractal_score = (box_counting_dimension - 1.5) / 0.5
        else:
            fractal_score = 0.5
        # H1 features contribution (loops/holes - complexity in long-term memory)
        h1_score = min(1.0, h1_num_features / 10.0)
        # Betti-1 contribution (memory loops)
        betti_score = min(1.0, betti_1 / 10.0)
        # Combine scores
        long_term_memory = (ridge_score * 0.35 + fractal_score * 0.25 + h1_score * 0.25 + betti_score * 0.15)
        return min(1.0, long_term_memory)
    
    def _calculate_working_memory(self, correlation_dimension: float, graph_density: float,
                                betweenness_centrality: float, information_dimension: float) -> float:
        """Calculate working memory from fingerprint features (DMIT principle)"""
        # DMIT research shows: High correlation dimension + graph density = working memory
        
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
        working_memory = (corr_score * 0.3 + density_score * 0.25 + centrality_score * 0.25 + info_score * 0.2)
        return min(1.0, working_memory)
    
    def _calculate_episodic_memory(self, information_dimension: float, entropy: float,
                                 pattern_symmetry: float, spectral_entropy: float) -> float:
        """Calculate episodic memory from fingerprint features (DMIT principle)"""
        # DMIT research shows: High information dimension + entropy = episodic memory
        
        # Information dimension contribution
        if 1.5 <= information_dimension <= 2.0:
            info_score = (information_dimension - 1.5) / 0.5
        else:
            info_score = 0.5
        
        # Entropy contribution (higher entropy = more complex episodic memory)
        if entropy > 0:
            entropy_score = min(1.0, entropy / 8.0)  # Normalize to 0-1
        else:
            entropy_score = 0.5
        
        # Pattern symmetry contribution
        symmetry_score = min(1.0, pattern_symmetry)
        
        # Spectral entropy contribution
        spectral_score = min(1.0, spectral_entropy)
        
        # Combine scores
        episodic_memory = (info_score * 0.35 + entropy_score * 0.25 + symmetry_score * 0.25 + spectral_score * 0.15)
        return min(1.0, episodic_memory)
    
    def _calculate_semantic_memory(self, pattern_regularity: float, lacunarity: float,
                                 ridge_continuity: float, std_intensity: float) -> float:
        """Calculate semantic memory from fingerprint features (DMIT principle)"""
        # DMIT research shows: High pattern regularity + low lacunarity = semantic memory
        
        # Pattern regularity contribution
        regularity_score = min(1.0, pattern_regularity)
        
        # Lacunarity contribution (lower lacunarity = more regular = better semantic memory)
        lacunarity_score = max(0.0, 1.0 - lacunarity)
        
        # Ridge continuity contribution
        continuity_score = min(1.0, ridge_continuity)
        
        # Standard deviation contribution (lower variation = more consistent = better semantic memory)
        if std_intensity > 0:
            std_score = max(0.0, 1.0 - (std_intensity / 100.0))
        else:
            std_score = 0.5
        
        # Combine scores
        semantic_memory = (regularity_score * 0.3 + lacunarity_score * 0.25 + continuity_score * 0.25 + std_score * 0.2)
        return min(1.0, semantic_memory)
    
    def _calculate_procedural_memory(self, ridge_uniformity: float, pattern_type: str,
                                   ridge_curvature: float, community_cohesion: float) -> float:
        """Calculate procedural memory from fingerprint features (DMIT principle)"""
        # DMIT research shows: High ridge uniformity + pattern type = procedural memory
        
        # Ridge uniformity contribution
        uniformity_score = min(1.0, ridge_uniformity)
        
        # Pattern type contribution
        pattern_weights = {
            'whorl': 0.8,      # Complex patterns indicate good procedural memory
            'loop': 0.7,       # Good procedural memory
            'arch': 0.6,       # Moderate procedural memory
            'tented_arch': 0.65, # Slightly better than plain arch
            'composite': 0.75   # Complex procedural patterns
        }
        pattern_score = pattern_weights.get(pattern_type.lower(), 0.6)
        
        # Ridge curvature contribution
        curvature_score = min(1.0, ridge_curvature)
        
        # Community cohesion contribution
        cohesion_score = min(1.0, community_cohesion)
        
        # Combine scores
        procedural_memory = (uniformity_score * 0.3 + pattern_score * 0.25 + curvature_score * 0.25 + cohesion_score * 0.2)
        return min(1.0, procedural_memory)
    
    def _calculate_memory_consolidation(self, spectral_centroid: float, spectral_rolloff: float,
                                      graph_density: float, topological_complexity: float) -> float:
        """Calculate memory consolidation from fingerprint features (DMIT principle)"""
        # DMIT research shows: High spectral features + graph complexity = memory consolidation
        
        # Spectral centroid contribution
        centroid_score = min(1.0, spectral_centroid)
        
        # Spectral rolloff contribution
        rolloff_score = min(1.0, spectral_rolloff)
        
        # Graph density contribution
        density_score = min(1.0, graph_density)
        
        # Topological complexity contribution
        complexity_score = min(1.0, topological_complexity)
        
        # Combine scores
        memory_consolidation = (centroid_score * 0.3 + rolloff_score * 0.25 + density_score * 0.25 + complexity_score * 0.2)
        return min(1.0, memory_consolidation)
    
    def _calculate_memory_retrieval(self, spectral_radius: float, euler_characteristic: int,
                                  spectral_bandwidth: float, topological_complexity: float) -> float:
        """Calculate memory retrieval from fingerprint features (DMIT principle)"""
        # DMIT research shows: High spectral radius + euler characteristic = memory retrieval
        
        # Spectral radius contribution
        if spectral_radius > 0:
            spectral_score = min(1.0, spectral_radius / 10.0)
        else:
            spectral_score = 0.5
        
        # Euler characteristic contribution (more negative = more complex = better retrieval)
        if euler_characteristic < 0:
            euler_score = min(1.0, abs(euler_characteristic) / 10.0)
        else:
            euler_score = 0.3
        
        # Spectral bandwidth contribution
        bandwidth_score = min(1.0, spectral_bandwidth)
        
        # Topological complexity contribution
        complexity_score = min(1.0, topological_complexity)
        
        # Combine scores
        memory_retrieval = (spectral_score * 0.3 + euler_score * 0.25 + bandwidth_score * 0.25 + complexity_score * 0.2)
        return min(1.0, memory_retrieval)

    @staticmethod
    def classify_memory_level(score: float) -> str:
        if score >= 0.85:
            return "Exceptional Memory"
        elif score >= 0.75:
            return "High Memory"
        elif score >= 0.65:
            return "Above Average Memory"
        elif score >= 0.55:
            return "Average Memory"
        else:
            return "Developing Memory" 