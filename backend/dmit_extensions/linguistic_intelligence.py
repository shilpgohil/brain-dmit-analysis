from typing import Dict, Any
from .base import DMITExtensionBase

class LinguisticIntelligenceExtension(DMITExtensionBase):
    """
    Extension for analyzing Linguistic Intelligence and language abilities from fingerprint features.
    Uses comprehensive DMIT scientific correlations between fingerprint patterns and linguistic capabilities.
    """
    def analyze(self, features: Dict[str, Any]) -> Dict[str, Any]:
        # Extract comprehensive fingerprint features for linguistic intelligence analysis
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
        
        # Calculate linguistic intelligence abilities using comprehensive DMIT scientific correlations
        
        # 1. Verbal Communication Analysis (DMIT Principle: High information dimension + entropy = verbal communication)
        verbal_communication = self._calculate_verbal_communication(information_dimension, entropy, 
                                                                  pattern_symmetry, spectral_entropy)
        
        # 2. Language Processing Analysis (DMIT Principle: High ridge density + clustering coefficient = language processing)
        language_processing = self._calculate_language_processing(ridge_density, clustering_coefficient, 
                                                                modularity, ridge_thickness)
        
        # 3. Vocabulary Acquisition Analysis (DMIT Principle: High correlation dimension + graph density = vocabulary acquisition)
        vocabulary_acquisition = self._calculate_vocabulary_acquisition(correlation_dimension, graph_density, 
                                                                      betweenness_centrality, information_dimension)
        
        # 4. Grammar Understanding Analysis (DMIT Principle: High community cohesion + spectral radius = grammar understanding)
        grammar_understanding = self._calculate_grammar_understanding(community_cohesion, spectral_radius, 
                                                                    topological_complexity, euler_characteristic)
        
        # 5. Reading Comprehension Analysis (DMIT Principle: High ridge count + fractal dimension = reading comprehension)
        reading_comprehension = self._calculate_reading_comprehension(tfrc, box_counting_dimension, 
                                                                    h1_num_features, betti_1)
        
        # 6. Writing Skills Analysis (DMIT Principle: High pattern regularity + low lacunarity = writing skills)
        writing_skills = self._calculate_writing_skills(pattern_regularity, lacunarity, 
                                                      ridge_continuity, std_intensity)
        
        # 7. Language Expression Analysis (DMIT Principle: High ridge uniformity + pattern type = language expression)
        language_expression = self._calculate_language_expression(ridge_uniformity, pattern_type, 
                                                                ridge_curvature, spectral_energy)
        
        # 8. Multilingual Capacity Analysis (DMIT Principle: High spectral features + graph complexity = multilingual capacity)
        multilingual_capacity = self._calculate_multilingual_capacity(spectral_centroid, spectral_rolloff, 
                                                                    graph_density, topological_complexity)
        
        # Calculate overall linguistic intelligence score
        linguistic_intelligence_score = (
            verbal_communication * 0.20 +            # Verbal communication is fundamental
            language_processing * 0.18 +             # Language processing is crucial
            vocabulary_acquisition * 0.15 +          # Vocabulary acquisition is important
            grammar_understanding * 0.15 +           # Grammar understanding is essential
            reading_comprehension * 0.12 +           # Reading comprehension
            writing_skills * 0.10 +                  # Writing skills
            language_expression * 0.07 +             # Language expression
            multilingual_capacity * 0.03             # Multilingual capacity
        )
        
        # Normalize to 0-1 range
        linguistic_intelligence_score = max(0.0, min(1.0, linguistic_intelligence_score))
        
        # Determine linguistic intelligence style based on dominant features
        linguistic_styles = {
            'verbal_communicator': (verbal_communication + language_expression) / 2,
            'language_processor': (language_processing + vocabulary_acquisition) / 2,
            'grammar_expert': (grammar_understanding + writing_skills) / 2,
            'reading_writer': (reading_comprehension + writing_skills) / 2,
            'multilingual_learner': (multilingual_capacity + vocabulary_acquisition) / 2,
            'balanced_linguistic': (verbal_communication + grammar_understanding) / 2
        }
        primary_style = max(linguistic_styles.items(), key=lambda x: x[1])[0]
        
        return {
            'linguistic_intelligence_score': linguistic_intelligence_score,
            'primary_linguistic_style': primary_style,
            'verbal_communication': verbal_communication,
            'language_processing': language_processing,
            'vocabulary_acquisition': vocabulary_acquisition,
            'grammar_understanding': grammar_understanding,
            'reading_comprehension': reading_comprehension,
            'writing_skills': writing_skills,
            'language_expression': language_expression,
            'multilingual_capacity': multilingual_capacity,
            'language_fluency': (verbal_communication + language_processing) / 2,
            'literacy_skills': (reading_comprehension + writing_skills) / 2,
            'language_learning': (vocabulary_acquisition + multilingual_capacity) / 2,
            'communication_effectiveness': (verbal_communication + language_expression) / 2,
            'linguistic_competence': (grammar_understanding + vocabulary_acquisition) / 2,
            'linguistic_intelligence_profile': self.classify_linguistic_intelligence_level(linguistic_intelligence_score)
        }

    def _calculate_verbal_communication(self, information_dimension: float, entropy: float,
                                      pattern_symmetry: float, spectral_entropy: float) -> float:
        """Calculate verbal communication from fingerprint features (DMIT principle)"""
        # DMIT research shows: High information dimension + entropy = verbal communication
        
        # Information dimension contribution
        if 1.5 <= information_dimension <= 2.0:
            info_score = (information_dimension - 1.5) / 0.5
        else:
            info_score = 0.5
        
        # Entropy contribution (higher entropy = more complex verbal communication)
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
    
    def _calculate_language_processing(self, ridge_density: float, clustering_coefficient: float,
                                     modularity: float, ridge_thickness: float) -> float:
        """Calculate language processing from fingerprint features (DMIT principle)"""
        # DMIT research shows: High ridge density + clustering coefficient = language processing
        
        # Ridge density contribution
        density_score = min(1.0, ridge_density)
        
        # Clustering coefficient contribution
        clustering_score = min(1.0, clustering_coefficient)
        
        # Modularity contribution
        modularity_score = min(1.0, modularity)
        
        # Ridge thickness contribution
        thickness_score = min(1.0, ridge_thickness)
        
        # Combine scores
        language_processing = (density_score * 0.3 + clustering_score * 0.25 + modularity_score * 0.25 + thickness_score * 0.2)
        return min(1.0, language_processing)
    
    def _calculate_vocabulary_acquisition(self, correlation_dimension: float, graph_density: float,
                                        betweenness_centrality: float, information_dimension: float) -> float:
        """Calculate vocabulary acquisition from fingerprint features (DMIT principle)"""
        # DMIT research shows: High correlation dimension + graph density = vocabulary acquisition
        
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
        vocabulary_acquisition = (corr_score * 0.3 + density_score * 0.25 + centrality_score * 0.25 + info_score * 0.2)
        return min(1.0, vocabulary_acquisition)
    
    def _calculate_grammar_understanding(self, community_cohesion: float, spectral_radius: float,
                                       topological_complexity: float, euler_characteristic: int) -> float:
        """Calculate grammar understanding from fingerprint features (DMIT principle)"""
        # DMIT research shows: High community cohesion + spectral radius = grammar understanding
        
        # Community cohesion contribution
        cohesion_score = min(1.0, community_cohesion)
        
        # Spectral radius contribution
        if spectral_radius > 0:
            spectral_score = min(1.0, spectral_radius / 10.0)
        else:
            spectral_score = 0.5
        
        # Topological complexity contribution
        complexity_score = min(1.0, topological_complexity)
        
        # Euler characteristic contribution (more negative = more complex = better grammar understanding)
        if euler_characteristic < 0:
            euler_score = min(1.0, abs(euler_characteristic) / 10.0)
        else:
            euler_score = 0.3
        
        # Combine scores
        grammar_understanding = (cohesion_score * 0.3 + spectral_score * 0.25 + complexity_score * 0.25 + euler_score * 0.2)
        return min(1.0, grammar_understanding)
    
    def _calculate_reading_comprehension(self, tfrc: int, box_counting_dimension: float,
                                       h1_num_features: int, betti_1: int) -> float:
        """Calculate reading comprehension from fingerprint features (DMIT principle)"""
        # DMIT research shows: High ridge count + fractal dimension = reading comprehension
        
        # Ridge count contribution
        ridge_score = min(1.0, float(tfrc or 0))  # FIX: per-finger TFRC 0-30, not 0-1500  # FIX: per-finger TFRC 0-30
        
        # Fractal dimension contribution
        if 1.5 <= box_counting_dimension <= 2.0:
            fractal_score = (box_counting_dimension - 1.5) / 0.5
        else:
            fractal_score = 0.5
        
        # H1 features contribution (loops/holes - complexity in reading comprehension)
        h1_score = min(1.0, h1_num_features / 10.0)
        
        # Betti-1 contribution (reading comprehension loops)
        betti_score = min(1.0, betti_1 / 10.0)
        
        # Combine scores
        reading_comprehension = (ridge_score * 0.35 + fractal_score * 0.25 + h1_score * 0.25 + betti_score * 0.15)
        return min(1.0, reading_comprehension)
    
    def _calculate_writing_skills(self, pattern_regularity: float, lacunarity: float,
                                ridge_continuity: float, std_intensity: float) -> float:
        """Calculate writing skills from fingerprint features (DMIT principle)"""
        # DMIT research shows: High pattern regularity + low lacunarity = writing skills
        
        # Pattern regularity contribution
        regularity_score = min(1.0, pattern_regularity)
        
        # Lacunarity contribution (lower lacunarity = more regular = better writing skills)
        lacunarity_score = max(0.0, 1.0 - lacunarity)
        
        # Ridge continuity contribution
        continuity_score = min(1.0, ridge_continuity)
        
        # Standard deviation contribution (lower variation = more consistent = better writing skills)
        if std_intensity > 0:
            std_score = max(0.0, 1.0 - (std_intensity / 100.0))
        else:
            std_score = 0.5
        
        # Combine scores
        writing_skills = (regularity_score * 0.3 + lacunarity_score * 0.25 + continuity_score * 0.25 + std_score * 0.2)
        return min(1.0, writing_skills)
    
    def _calculate_language_expression(self, ridge_uniformity: float, pattern_type: str,
                                     ridge_curvature: float, spectral_energy: float) -> float:
        """Calculate language expression from fingerprint features (DMIT principle)"""
        # DMIT research shows: High ridge uniformity + pattern type = language expression
        
        # Ridge uniformity contribution
        uniformity_score = min(1.0, ridge_uniformity)
        
        # Pattern type contribution
        pattern_weights = {
            'whorl': 0.8,      # Complex patterns indicate language expression
            'loop': 0.7,       # Good language expression
            'arch': 0.6,       # Moderate language expression
            'tented_arch': 0.65, # Slightly better than plain arch
            'composite': 0.75   # Complex language expression patterns
        }
        pattern_score = pattern_weights.get(pattern_type.lower(), 0.6)
        
        # Ridge curvature contribution
        curvature_score = min(1.0, ridge_curvature)
        
        # Spectral energy contribution
        energy_score = min(1.0, spectral_energy)
        
        # Combine scores
        language_expression = (uniformity_score * 0.3 + pattern_score * 0.25 + curvature_score * 0.25 + energy_score * 0.2)
        return min(1.0, language_expression)
    
    def _calculate_multilingual_capacity(self, spectral_centroid: float, spectral_rolloff: float,
                                       graph_density: float, topological_complexity: float) -> float:
        """Calculate multilingual capacity from fingerprint features (DMIT principle)"""
        # DMIT research shows: High spectral features + graph complexity = multilingual capacity
        
        # Spectral centroid contribution
        centroid_score = min(1.0, spectral_centroid)
        
        # Spectral rolloff contribution
        rolloff_score = min(1.0, spectral_rolloff)
        
        # Graph density contribution
        density_score = min(1.0, graph_density)
        
        # Topological complexity contribution
        complexity_score = min(1.0, topological_complexity)
        
        # Combine scores
        multilingual_capacity = (centroid_score * 0.3 + rolloff_score * 0.25 + density_score * 0.25 + complexity_score * 0.2)
        return min(1.0, multilingual_capacity)

    @staticmethod
    def classify_linguistic_intelligence_level(score: float) -> str:
        if score >= 0.85:
            return "Exceptional Linguistic Intelligence"
        elif score >= 0.75:
            return "High Linguistic Intelligence"
        elif score >= 0.65:
            return "Above Average Linguistic Intelligence"
        elif score >= 0.55:
            return "Average Linguistic Intelligence"
        else:
            return "Developing Linguistic Intelligence" 