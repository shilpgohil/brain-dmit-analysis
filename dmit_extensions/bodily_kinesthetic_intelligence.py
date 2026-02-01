from typing import Dict, Any
from .base import DMITExtensionBase

class BodilyKinestheticIntelligenceExtension(DMITExtensionBase):
    """
    Extension for analyzing Bodily-Kinesthetic Intelligence from fingerprint features.
    Uses scientific DMIT correlations between fingerprint patterns and physical abilities.
    """
    def analyze(self, features: Dict[str, Any]) -> Dict[str, Any]:
        # Extract actual fingerprint features for kinesthetic intelligence analysis
        # Ridge count and density features
        # tfrc already extracted above
        ridge_density = features.get('ridge_density', 0.0)
        tfrc = features.get('tfrc', 0)  # Total Fingerprint Ridge Count
        
        # Pattern analysis features
        pattern_type = features.get('pattern_type', 'loop')
        pattern_symmetry = features.get('pattern_symmetry', 0.0)
        pattern_regularity = features.get('pattern_regularity', 0.0)
        
        # Fractal and complexity features
        box_counting_dimension = features.get('box_counting_dimension', 1.5)
        correlation_dimension = features.get('correlation_dimension', 1.5)
        information_dimension = features.get('information_dimension', 1.5)
        lacunarity = features.get('lacunarity', 0.0)
        
        # Graph and network features
        graph_density = features.get('graph_density', 0.0)
        clustering_coefficient = features.get('clustering_coefficient', 0.0)
        spectral_radius = features.get('spectral_radius', 0.0)
        betweenness_centrality = features.get('betweenness_centrality', 0.0)
        
        # Topological features
        euler_characteristic = features.get('euler_characteristic', 0)
        topological_complexity = features.get('topological_complexity', 0.0)
        h1_num_features = features.get('h1_num_features', 0)  # Loop/hole count
        
        # Ridge flow features
        ridge_orientation = features.get('ridge_orientation', 0.0)
        ridge_flow_curvature = features.get('ridge_flow_curvature', 0.0)
        orientation_coherence = features.get('orientation_coherence', 0.0)
        
        # Calculate kinesthetic intelligence using DMIT scientific correlations
        
        # 1. Physical Coordination Analysis (DMIT Principle: High ridge density + pattern regularity = coordination)
        physical_coordination = self._calculate_physical_coordination(ridge_density, pattern_regularity, 
                                                                    orientation_coherence, clustering_coefficient)
        
        # 2. Motor Skills Analysis (DMIT Principle: High ridge count + graph density = motor skills)
        motor_skills = self._calculate_motor_skills(tfrc, graph_density, spectral_radius)
        
        # 3. Body Awareness Analysis (DMIT Principle: High pattern symmetry + fractal complexity = body awareness)
        body_awareness = self._calculate_body_awareness(pattern_symmetry, box_counting_dimension, 
                                                      topological_complexity, h1_num_features)
        
        # 4. Physical Expression Analysis (DMIT Principle: High ridge flow curvature + betweenness centrality = expression)
        physical_expression = self._calculate_physical_expression(ridge_flow_curvature, betweenness_centrality, 
                                                                pattern_type, ridge_orientation)
        
        # 5. Movement Precision Analysis (DMIT Principle: High correlation dimension + lacunarity = precision)
        movement_precision = self._calculate_movement_precision(correlation_dimension, lacunarity, 
                                                              information_dimension, euler_characteristic)
        
        # 6. Physical Learning Analysis (DMIT Principle: High graph connectivity + pattern complexity = physical learning)
        physical_learning = self._calculate_physical_learning(graph_density, clustering_coefficient, 
                                                            pattern_regularity, topological_complexity)
        
        # Overall kinesthetic intelligence score (weighted combination)
        kinesthetic_intelligence_score = (
            physical_coordination * 0.25 +       # Physical coordination is fundamental
            motor_skills * 0.20 +                # Motor skills are crucial
            body_awareness * 0.20 +              # Body awareness is important
            physical_expression * 0.15 +         # Physical expression ability
            movement_precision * 0.15 +          # Movement precision
            physical_learning * 0.05             # Physical learning ability
        )
        
        # Normalize to 0-1 range
        kinesthetic_intelligence_score = max(0.0, min(1.0, kinesthetic_intelligence_score))
        
        # Determine kinesthetic style based on dominant features
        kinesthetic_styles = {
            'coordinated': physical_coordination + motor_skills,
            'expressive': physical_expression + body_awareness,
            'precise': movement_precision + physical_coordination,
            'athletic': motor_skills + physical_expression,
            'graceful': body_awareness + movement_precision
        }
        primary_style = max(kinesthetic_styles.items(), key=lambda x: x[1])[0]

        return {
            'bodily_kinesthetic_intelligence_score': kinesthetic_intelligence_score,
            'primary_kinesthetic_style': primary_style,
            'physical_coordination': physical_coordination,
            'motor_skills': motor_skills,
            'body_awareness': body_awareness,
            'physical_expression': physical_expression,
            'movement_precision': movement_precision,
            'physical_learning': physical_learning,
            'athletic_ability': motor_skills + physical_coordination,
            'dance_performance': physical_expression + body_awareness,
            'sports_excellence': motor_skills + movement_precision,
            'manual_dexterity': movement_precision + physical_coordination,
            'physical_creativity': physical_expression + body_awareness,
            'kinesthetic_profile': self.classify_kinesthetic_level(kinesthetic_intelligence_score)
        }

    def _calculate_physical_coordination(self, ridge_density: float, pattern_regularity: float,
                                       orientation_coherence: float, clustering_coefficient: float) -> float:
        """Calculate physical coordination from fingerprint features (DMIT principle)"""
        # DMIT research shows: High ridge density + pattern regularity = coordination
        
        # Ridge density contribution
        density_score = min(1.0, ridge_density)
        
        # Pattern regularity contribution
        regularity_score = min(1.0, pattern_regularity)
        
        # Orientation coherence contribution
        coherence_score = min(1.0, orientation_coherence)
        
        # Clustering coefficient contribution
        clustering_score = min(1.0, clustering_coefficient)
        
        # Combine scores
        physical_coordination = (density_score * 0.3 + regularity_score * 0.3 + coherence_score * 0.25 + clustering_score * 0.15)
        return min(1.0, physical_coordination)
    
    def _calculate_motor_skills(self, tfrc: int, graph_density: float, spectral_radius: float) -> float:
        """Calculate motor skills from fingerprint features (DMIT principle)"""
        # DMIT research shows: High ridge count + graph density = motor skills
        
        # Ridge count contribution
        if tfrc > 0:
            ridge_score = min(1.0, tfrc / 1500.0)
        else:
            ridge_score = min(1.0, tfrc / 1500.0) if tfrc > 0 else 0.0
        
        # Graph density contribution
        density_score = min(1.0, graph_density)
        
        # Spectral radius contribution
        if spectral_radius > 0:
            spectral_score = min(1.0, spectral_radius / 10.0)
        else:
            spectral_score = 0.5
        
        # Combine scores
        motor_skills = (ridge_score * 0.4 + density_score * 0.35 + spectral_score * 0.25)
        return min(1.0, motor_skills)
    
    def _calculate_body_awareness(self, pattern_symmetry: float, box_counting_dimension: float,
                                topological_complexity: float, h1_num_features: int) -> float:
        """Calculate body awareness from fingerprint features (DMIT principle)"""
        # DMIT research shows: High pattern symmetry + fractal complexity = body awareness
        
        # Pattern symmetry contribution
        symmetry_score = min(1.0, pattern_symmetry)
        
        # Fractal dimension contribution
        if 1.5 <= box_counting_dimension <= 2.0:
            fractal_score = (box_counting_dimension - 1.5) / 0.5
        else:
            fractal_score = 0.5
        
        # Topological complexity contribution
        complexity_score = min(1.0, topological_complexity)
        
        # H1 features contribution (loops/holes - complexity in body awareness)
        h1_score = min(1.0, h1_num_features / 10.0)
        
        # Combine scores
        body_awareness = (symmetry_score * 0.3 + fractal_score * 0.25 + complexity_score * 0.25 + h1_score * 0.2)
        return min(1.0, body_awareness)
    
    def _calculate_physical_expression(self, ridge_flow_curvature: float, betweenness_centrality: float,
                                     pattern_type: str, ridge_orientation: float) -> float:
        """Calculate physical expression from fingerprint features (DMIT principle)"""
        # DMIT research shows: High ridge flow curvature + betweenness centrality = physical expression
        
        # Ridge flow curvature contribution
        curvature_score = min(1.0, ridge_flow_curvature)
        
        # Betweenness centrality contribution
        centrality_score = min(1.0, betweenness_centrality)
        
        # Pattern type contribution
        pattern_weights = {
            'whorl': 0.8,      # Complex patterns indicate expressive ability
            'loop': 0.7,       # Good expression
            'arch': 0.6,       # Moderate expression
            'tented_arch': 0.65, # Slightly better than plain arch
            'composite': 0.75   # Complex expression patterns
        }
        pattern_score = pattern_weights.get(pattern_type.lower(), 0.6)
        
        # Ridge orientation contribution
        orientation_score = min(1.0, abs(ridge_orientation) / 180.0)
        
        # Combine scores
        physical_expression = (curvature_score * 0.3 + centrality_score * 0.3 + pattern_score * 0.25 + orientation_score * 0.15)
        return min(1.0, physical_expression)
    
    def _calculate_movement_precision(self, correlation_dimension: float, lacunarity: float,
                                    information_dimension: float, euler_characteristic: int) -> float:
        """Calculate movement precision from fingerprint features (DMIT principle)"""
        # DMIT research shows: High correlation dimension + low lacunarity = movement precision
        
        # Correlation dimension contribution
        if 1.5 <= correlation_dimension <= 2.0:
            corr_score = (correlation_dimension - 1.5) / 0.5
        else:
            corr_score = 0.5
        
        # Lacunarity contribution (lower lacunarity = more regular = better precision)
        lacunarity_score = max(0.0, 1.0 - lacunarity)
        
        # Information dimension contribution
        if 1.5 <= information_dimension <= 2.0:
            info_score = (information_dimension - 1.5) / 0.5
        else:
            info_score = 0.5
        
        # Euler characteristic contribution (more negative = more complex = better precision)
        if euler_characteristic < 0:
            euler_score = min(1.0, abs(euler_characteristic) / 10.0)
        else:
            euler_score = 0.3
        
        # Combine scores
        movement_precision = (corr_score * 0.3 + lacunarity_score * 0.25 + info_score * 0.25 + euler_score * 0.2)
        return min(1.0, movement_precision)
    
    def _calculate_physical_learning(self, graph_density: float, clustering_coefficient: float,
                                   pattern_regularity: float, topological_complexity: float) -> float:
        """Calculate physical learning from fingerprint features (DMIT principle)"""
        # DMIT research shows: High graph connectivity + pattern complexity = physical learning
        
        # Graph density contribution
        density_score = min(1.0, graph_density)
        
        # Clustering coefficient contribution
        clustering_score = min(1.0, clustering_coefficient)
        
        # Pattern regularity contribution
        regularity_score = min(1.0, pattern_regularity)
        
        # Topological complexity contribution
        complexity_score = min(1.0, topological_complexity)
        
        # Combine scores
        physical_learning = (density_score * 0.3 + clustering_score * 0.25 + regularity_score * 0.25 + complexity_score * 0.2)
        return min(1.0, physical_learning)

    @staticmethod
    def classify_kinesthetic_level(score: float) -> str:
        if score >= 0.85:
            return "Exceptional Bodily-Kinesthetic Intelligence"
        elif score >= 0.75:
            return "High Bodily-Kinesthetic Intelligence"
        elif score >= 0.65:
            return "Above Average Bodily-Kinesthetic Intelligence"
        elif score >= 0.55:
            return "Average Bodily-Kinesthetic Intelligence"
        else:
            return "Developing Bodily-Kinesthetic Intelligence" 