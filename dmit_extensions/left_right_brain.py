from typing import Dict, Any
from .base import DMITExtensionBase

class LeftRightBrainExtension(DMITExtensionBase):
    """
    Extension for analyzing Left-Right Brain Interaction from fingerprint features.
    Uses scientific DMIT correlations between fingerprint features and brain hemispheric balance.
    """
    def analyze(self, features: Dict[str, Any]) -> Dict[str, Any]:
        # Extract actual fingerprint features for brain analysis
        # FIX: ATD angle is a PALM feature (not fingerprint). It is always None here.
        # We detect this and fall back to pattern-based asymmetry analysis.
        atd_raw = features.get('atd_average_angle') or features.get('atd_angle')
        atd_available = atd_raw is not None and float(atd_raw) != 0.0
        atd_angle = float(atd_raw) if atd_available else None

        # Pattern asymmetry features (available from extractor)
        horizontal_symmetry = float(features.get('horizontal_symmetry') or features.get('pattern_symmetry_score', 0.5))
        vertical_symmetry = float(features.get('vertical_symmetry') or features.get('symmetry_index', 0.5))
        pattern_asymmetry = float(features.get('pattern_asymmetry') or (1.0 - horizontal_symmetry))

        # Ridge count and density (FIX: use normalized tfrc)
        ridge_count_left = float(features.get('ridge_count_left') or features.get('tfrc_normalized', 0.5))
        ridge_count_right = float(features.get('ridge_count_right') or features.get('tfrc_normalized', 0.5))
        ridge_density_left = float(features.get('ridge_density_left') or features.get('ridge_density', 0.0))
        ridge_density_right = float(features.get('ridge_density_right') or features.get('ridge_density', 0.0))

        # Fractal and complexity asymmetry
        fractal_dimension_left = float(features.get('fractal_dimension_left') or features.get('box_counting_dimension', 1.5))
        fractal_dimension_right = float(features.get('fractal_dimension_right') or features.get('box_counting_dimension', 1.5))
        complexity_left = float(features.get('complexity_left') or features.get('topological_complexity', 0.0))
        complexity_right = float(features.get('complexity_right') or features.get('topological_complexity', 0.0))

        # Graph and network features
        graph_density_left = float(features.get('graph_density_left') or features.get('graph_density', 0.0))
        graph_density_right = float(features.get('graph_density_right') or features.get('graph_density', 0.0))
        spectral_radius_left = float(features.get('spectral_radius_left') or features.get('spectral_radius', 0.0))
        spectral_radius_right = float(features.get('spectral_radius_right') or features.get('spectral_radius', 0.0))

        # Topological asymmetry
        euler_characteristic_left = int(features.get('euler_characteristic_left') or features.get('euler_characteristic', 0))
        euler_characteristic_right = int(features.get('euler_characteristic_right') or features.get('euler_characteristic', 0))
        topological_complexity_left = float(features.get('topological_complexity_left') or features.get('topological_complexity', 0.0))
        topological_complexity_right = float(features.get('topological_complexity_right') or features.get('topological_complexity', 0.0))

        # Pattern type for dominance inference
        pattern_type = features.get('pattern_type', 'loop')

        # 1. ATD Score — graceful fallback when ATD not available (fingerprint images)
        if atd_available:
            atd_score = self._calculate_atd_score(atd_angle)
        else:
            # Fallback: use pattern symmetry as proxy for balanced brain development
            atd_score = self._calculate_atd_from_symmetry(horizontal_symmetry, pattern_type)

        # 2. Symmetry Analysis
        symmetry_score = self._calculate_symmetry_score(horizontal_symmetry, vertical_symmetry, pattern_asymmetry)
        
        # 3. Ridge Count Asymmetry Analysis (DMIT Principle: Balanced ridge counts = balanced brain)
        ridge_asymmetry_score = self._calculate_ridge_asymmetry_score(ridge_count_left, ridge_count_right, 
                                                                     ridge_density_left, ridge_density_right)
        
        # 4. Fractal Asymmetry Analysis (DMIT Principle: Balanced complexity = balanced processing)
        fractal_asymmetry_score = self._calculate_fractal_asymmetry_score(fractal_dimension_left, fractal_dimension_right,
                                                                         complexity_left, complexity_right)
        
        # 5. Graph Asymmetry Analysis (DMIT Principle: Balanced networks = balanced brain function)
        graph_asymmetry_score = self._calculate_graph_asymmetry_score(graph_density_left, graph_density_right,
                                                                     spectral_radius_left, spectral_radius_right)
        
        # 6. Topological Asymmetry Analysis (DMIT Principle: Balanced topology = balanced reasoning)
        topological_asymmetry_score = self._calculate_topological_asymmetry_score(euler_characteristic_left, euler_characteristic_right,
                                                                                 topological_complexity_left, topological_complexity_right)
        
        # Calculate left and right brain scores
        # FIX: Pass 45.0 (neutral ATD) when ATD is not available, to avoid NoneType math errors
        safe_atd = atd_angle if atd_angle is not None else 45.0
        left_brain_score = self._calculate_left_brain_score(safe_atd, ridge_count_left, fractal_dimension_left,
                                                           graph_density_left, euler_characteristic_left)
        right_brain_score = self._calculate_right_brain_score(safe_atd, ridge_count_right, fractal_dimension_right,
                                                             graph_density_right, euler_characteristic_right)
        
        # Overall brain integration score (weighted combination)
        brain_integration_score = (
            atd_score * 0.25 +                    # ATD angle is fundamental
            symmetry_score * 0.20 +               # Symmetry shows balance
            ridge_asymmetry_score * 0.15 +        # Ridge balance
            fractal_asymmetry_score * 0.15 +      # Complexity balance
            graph_asymmetry_score * 0.15 +        # Network balance
            topological_asymmetry_score * 0.10    # Topology balance
        )
        
        # Normalize to 0-1 range
        brain_integration_score = max(0.0, min(1.0, brain_integration_score))
        
        # Calculate hemispheric balance ratio
        total_score = left_brain_score + right_brain_score
        if total_score > 0:
            left_brain_percentage = left_brain_score / total_score
            right_brain_percentage = right_brain_score / total_score
        else:
            left_brain_percentage = 0.5
            right_brain_percentage = 0.5
        
        # Determine brain dominance type
        brain_dominance_type = self._determine_brain_dominance(left_brain_percentage, right_brain_percentage)

        return {
            'brain_integration_score': brain_integration_score,
            'left_brain_score': left_brain_score,
            'right_brain_score': right_brain_score,
            'left_brain_percentage': left_brain_percentage,
            'right_brain_percentage': right_brain_percentage,
            'brain_dominance_type': brain_dominance_type,
            'hemispheric_balance': 1.0 - abs(left_brain_percentage - right_brain_percentage),
            'neural_efficiency': brain_integration_score,
            'cognitive_integration': symmetry_score,
            'atd_score': atd_score,
            'symmetry_score': symmetry_score,
            'ridge_asymmetry_score': ridge_asymmetry_score,
            'fractal_asymmetry_score': fractal_asymmetry_score,
            'graph_asymmetry_score': graph_asymmetry_score,
            'topological_asymmetry_score': topological_asymmetry_score,
            'brain_profile': self.classify_brain_level(brain_integration_score)
        }
    
    def _calculate_atd_from_symmetry(self, symmetry: float, pattern_type: str) -> float:
        """Fallback for ATD when palm data unavailable.
        Uses pattern symmetry as a proxy indicator for hemispheric balance.
        Whorls tend toward stronger dominance; loops are more balanced."""
        pattern_balance = {'arch': 0.65, 'loop': 0.75, 'whorl': 0.55, 'composite': 0.60}
        pattern_score = pattern_balance.get(pattern_type.lower(), 0.65)
        return (symmetry * 0.6 + pattern_score * 0.4)

    def _calculate_atd_score(self, atd_angle: float) -> float:
        """Calculate brain integration score from ATD angle (DMIT principle)"""
        # DMIT research shows: ATD angle 35-55 degrees indicates balanced brain development
        # Optimal range: 40-50 degrees for balanced integration
        
        if 35.0 <= atd_angle <= 55.0:
            # Within normal range
            if 40.0 <= atd_angle <= 50.0:
                # Optimal range for balanced brain
                return 0.9
            else:
                # Normal but not optimal
                return 0.7
        elif 30.0 <= atd_angle < 35.0 or 55.0 < atd_angle <= 60.0:
            # Slightly outside normal range
            return 0.6
        else:
            # Significantly outside normal range
            return 0.4
    
    def _calculate_symmetry_score(self, horizontal_symmetry: float, vertical_symmetry: float, 
                                 pattern_asymmetry: float) -> float:
        """Calculate brain integration score from pattern symmetry (DMIT principle)"""
        # DMIT research shows: Higher symmetry indicates balanced brain development
        
        # Horizontal symmetry analysis
        horizontal_score = min(1.0, horizontal_symmetry)
        
        # Vertical symmetry analysis
        vertical_score = min(1.0, vertical_symmetry)
        
        # Pattern asymmetry analysis (invert so lower asymmetry = higher score)
        pattern_score = max(0.0, 1.0 - pattern_asymmetry)
        
        # Combine symmetry scores
        symmetry_score = (horizontal_score * 0.4 + vertical_score * 0.4 + pattern_score * 0.2)
        return min(1.0, symmetry_score)
    
    def _calculate_ridge_asymmetry_score(self, ridge_count_left: int, ridge_count_right: int,
                                       ridge_density_left: float, ridge_density_right: float) -> float:
        """Calculate brain integration score from ridge count asymmetry (DMIT principle)"""
        # DMIT research shows: Balanced ridge counts indicate balanced brain development
        
        # Ridge count asymmetry
        if ridge_count_left > 0 and ridge_count_right > 0:
            count_ratio = min(ridge_count_left, ridge_count_right) / max(ridge_count_left, ridge_count_right)
        else:
            count_ratio = 0.5
        
        # Ridge density asymmetry
        if ridge_density_left > 0 and ridge_density_right > 0:
            density_ratio = min(ridge_density_left, ridge_density_right) / max(ridge_density_left, ridge_density_right)
        else:
            density_ratio = 0.5
        
        # Combine ratios (higher ratio = more balanced = better score)
        asymmetry_score = (count_ratio * 0.6 + density_ratio * 0.4)
        return min(1.0, asymmetry_score)
    
    def _calculate_fractal_asymmetry_score(self, fractal_dimension_left: float, fractal_dimension_right: float,
                                         complexity_left: float, complexity_right: float) -> float:
        """Calculate brain integration score from fractal asymmetry (DMIT principle)"""
        # DMIT research shows: Balanced fractal complexity indicates balanced processing
        
        # Fractal dimension asymmetry
        if fractal_dimension_left > 0 and fractal_dimension_right > 0:
            fractal_ratio = min(fractal_dimension_left, fractal_dimension_right) / max(fractal_dimension_left, fractal_dimension_right)
        else:
            fractal_ratio = 0.5
        
        # Complexity asymmetry
        if complexity_left > 0 and complexity_right > 0:
            complexity_ratio = min(complexity_left, complexity_right) / max(complexity_left, complexity_right)
        else:
            complexity_ratio = 0.5
        
        # Combine ratios
        fractal_asymmetry_score = (fractal_ratio * 0.6 + complexity_ratio * 0.4)
        return min(1.0, fractal_asymmetry_score)
    
    def _calculate_graph_asymmetry_score(self, graph_density_left: float, graph_density_right: float,
                                       spectral_radius_left: float, spectral_radius_right: float) -> float:
        """Calculate brain integration score from graph asymmetry (DMIT principle)"""
        # DMIT research shows: Balanced graph structures indicate balanced brain function
        
        # Graph density asymmetry
        if graph_density_left > 0 and graph_density_right > 0:
            density_ratio = min(graph_density_left, graph_density_right) / max(graph_density_left, graph_density_right)
        else:
            density_ratio = 0.5
        
        # Spectral radius asymmetry
        if spectral_radius_left > 0 and spectral_radius_right > 0:
            spectral_ratio = min(spectral_radius_left, spectral_radius_right) / max(spectral_radius_left, spectral_radius_right)
        else:
            spectral_ratio = 0.5
        
        # Combine ratios
        graph_asymmetry_score = (density_ratio * 0.5 + spectral_ratio * 0.5)
        return min(1.0, graph_asymmetry_score)
    
    def _calculate_topological_asymmetry_score(self, euler_characteristic_left: int, euler_characteristic_right: int,
                                             topological_complexity_left: float, topological_complexity_right: float) -> float:
        """Calculate brain integration score from topological asymmetry (DMIT principle)"""
        # DMIT research shows: Balanced topology indicates balanced reasoning
        
        # Euler characteristic asymmetry
        if euler_characteristic_left != 0 and euler_characteristic_right != 0:
            euler_ratio = min(abs(euler_characteristic_left), abs(euler_characteristic_right)) / max(abs(euler_characteristic_left), abs(euler_characteristic_right))
        else:
            euler_ratio = 0.5
        
        # Topological complexity asymmetry
        if topological_complexity_left > 0 and topological_complexity_right > 0:
            complexity_ratio = min(topological_complexity_left, topological_complexity_right) / max(topological_complexity_left, topological_complexity_right)
        else:
            complexity_ratio = 0.5
        
        # Combine ratios
        topological_asymmetry_score = (euler_ratio * 0.4 + complexity_ratio * 0.6)
        return min(1.0, topological_asymmetry_score)
    
    def _calculate_left_brain_score(self, atd_angle: float, ridge_count_left: int, fractal_dimension_left: float,
                                  graph_density_left: float, euler_characteristic_left: int) -> float:
        """Calculate left brain score (analytical, logical, sequential)"""
        # Left brain indicators: lower ATD angle, higher ridge count, lower fractal dimension, higher graph density
        
        # ATD angle contribution (lower angle = more left brain)
        atd_contribution = max(0.0, 1.0 - (atd_angle - 35.0) / 20.0)  # Normalize 35-55 range
        
        # Ridge count contribution (higher count = more left brain)
        ridge_contribution = min(1.0, ridge_count_left / 150.0)
        
        # Fractal dimension contribution (lower dimension = more left brain)
        fractal_contribution = max(0.0, 1.0 - (fractal_dimension_left - 1.5) / 0.5)
        
        # Graph density contribution (higher density = more left brain)
        graph_contribution = min(1.0, graph_density_left)
        
        # Euler characteristic contribution (more negative = more complex = more left brain)
        euler_contribution = min(1.0, abs(euler_characteristic_left) / 10.0)
        
        # Combine contributions
        left_brain_score = (atd_contribution * 0.3 + ridge_contribution * 0.2 + fractal_contribution * 0.2 + 
                           graph_contribution * 0.2 + euler_contribution * 0.1)
        return min(1.0, left_brain_score)
    
    def _calculate_right_brain_score(self, atd_angle: float, ridge_count_right: int, fractal_dimension_right: float,
                                   graph_density_right: float, euler_characteristic_right: int) -> float:
        """Calculate right brain score (creative, intuitive, holistic)"""
        # Right brain indicators: higher ATD angle, lower ridge count, higher fractal dimension, lower graph density
        
        # ATD angle contribution (higher angle = more right brain)
        atd_contribution = max(0.0, (atd_angle - 35.0) / 20.0)  # Normalize 35-55 range
        
        # Ridge count contribution (lower count = more right brain)
        ridge_contribution = max(0.0, 1.0 - (ridge_count_right / 150.0))
        
        # Fractal dimension contribution (higher dimension = more right brain)
        fractal_contribution = min(1.0, (fractal_dimension_right - 1.5) / 0.5)
        
        # Graph density contribution (lower density = more right brain)
        graph_contribution = max(0.0, 1.0 - graph_density_right)
        
        # Euler characteristic contribution (less negative = simpler = more right brain)
        euler_contribution = max(0.0, 1.0 - abs(euler_characteristic_right) / 10.0)
        
        # Combine contributions
        right_brain_score = (atd_contribution * 0.3 + ridge_contribution * 0.2 + fractal_contribution * 0.2 + 
                            graph_contribution * 0.2 + euler_contribution * 0.1)
        return min(1.0, right_brain_score)
    
    def _determine_brain_dominance(self, left_percentage: float, right_percentage: float) -> str:
        """Determine brain dominance type based on percentages"""
        balance_threshold = 0.1  # 10% difference threshold
        
        if abs(left_percentage - right_percentage) <= balance_threshold:
            return "Balanced Integration"
        elif left_percentage > right_percentage:
            if left_percentage >= 0.7:
                return "Strong Left Brain Dominance"
            else:
                return "Moderate Left Brain Dominance"
        else:
            if right_percentage >= 0.7:
                return "Strong Right Brain Dominance"
            else:
                return "Moderate Right Brain Dominance"

    @staticmethod
    def classify_brain_level(score: float) -> str:
        if score >= 0.85:
            return "Exceptional Brain Integration"
        elif score >= 0.75:
            return "High Brain Integration"
        elif score >= 0.65:
            return "Above Average Brain Integration"
        elif score >= 0.55:
            return "Average Brain Integration"
        else:
            return "Developing Brain Integration" 