from typing import Dict, Any, List, Type
from .base import DMITExtensionBase
from .emotional_intelligence import EmotionalIntelligenceExtension
from .decision_making import DecisionMakingExtension
from .attention_focus import AttentionFocusExtension
from .creativity_index import CreativityIndexExtension
from .stress_response import StressResponseExtension
from .left_right_brain import LeftRightBrainExtension
from .neurodivergence import NeurodivergenceExtension
from .cognitive_load import CognitiveLoadExtension
from .executive_function import ExecutiveFunctionExtension
from .memory_processing import MemoryProcessingExtension
from .career_guidance import CareerGuidanceExtension
from .learning_style import LearningStyleExtension
from .communication_style import CommunicationStyleExtension
from .relationship_dynamics import RelationshipDynamicsExtension
from .health_wellness import HealthWellnessExtension
from .leadership_potential import LeadershipPotentialExtension
from .entrepreneurial_aptitude import EntrepreneurialAptitudeExtension
from .motivation_drive import MotivationDriveExtension
from .self_regulation import SelfRegulationExtension
from .social_awareness import SocialAwarenessExtension
from .linguistic_intelligence import LinguisticIntelligenceExtension
from .logical_mathematical_intelligence import LogicalMathematicalIntelligenceExtension
from .spatial_intelligence import SpatialIntelligenceExtension
from .bodily_kinesthetic_intelligence import BodilyKinestheticIntelligenceExtension
from .musical_intelligence import MusicalIntelligenceExtension
from .interpersonal_intelligence import InterpersonalIntelligenceExtension
from .intrapersonal_intelligence import IntrapersonalIntelligenceExtension
from .naturalistic_intelligence import NaturalisticIntelligenceExtension
from .risk_tolerance import RiskToleranceExtension
from .curiosity_exploratory import CuriosityExploratoryExtension
from .persistence_grit import PersistenceGritExtension
from .digital_intelligence import DigitalIntelligenceExtension
from .cultural_intelligence import CulturalIntelligenceExtension
from .financial_intelligence import FinancialIntelligenceExtension
from .meta_cognition import MetaCognitionExtension
from .innovation_intelligence import InnovationIntelligenceExtension
from .systems_thinking import SystemsThinkingExtension
from .pattern_recognition import PatternRecognitionExtension
from .learning_agility import LearningAgilityExtension
from .sustainability_intelligence import SustainabilityIntelligenceExtension
from .wellness_intelligence import WellnessIntelligenceExtension

# Extension base class imported from base module

# Extension registry (to be populated with actual extension classes)
extension_registry: List[Type[DMITExtensionBase]] = [
    EmotionalIntelligenceExtension,
    DecisionMakingExtension,
    AttentionFocusExtension,
    CreativityIndexExtension,
    StressResponseExtension,
    LeftRightBrainExtension,
    NeurodivergenceExtension,
    CognitiveLoadExtension,
    ExecutiveFunctionExtension,
    MemoryProcessingExtension,
    CareerGuidanceExtension,
    LearningStyleExtension,
    CommunicationStyleExtension,
    RelationshipDynamicsExtension,
    HealthWellnessExtension,
    LeadershipPotentialExtension,
    EntrepreneurialAptitudeExtension,
    MotivationDriveExtension,
    SelfRegulationExtension,
    SocialAwarenessExtension,
    LinguisticIntelligenceExtension,
    LogicalMathematicalIntelligenceExtension,
    SpatialIntelligenceExtension,
    BodilyKinestheticIntelligenceExtension,
    MusicalIntelligenceExtension,
    InterpersonalIntelligenceExtension,
    IntrapersonalIntelligenceExtension,
    NaturalisticIntelligenceExtension,
    RiskToleranceExtension,
    CuriosityExploratoryExtension,
    PersistenceGritExtension,
    DigitalIntelligenceExtension,
    CulturalIntelligenceExtension,
    FinancialIntelligenceExtension,
    MetaCognitionExtension,
    InnovationIntelligenceExtension,
    SystemsThinkingExtension,
    PatternRecognitionExtension,
    LearningAgilityExtension,
    SustainabilityIntelligenceExtension,
    WellnessIntelligenceExtension,
]

class DMITExtensionsEngine:
    def __init__(self):
        self.extensions = [ext() for ext in extension_registry]
        
        # Intelligence profile key aliases (legacy to new format)
        self.intelligence_aliases = {
            'spatial_intelligence': 'spatial',
            'logical_intelligence': 'logical', 
            'linguistic_intelligence': 'linguistic',
            'musical_intelligence': 'musical',
            'kinesthetic_intelligence': 'kinesthetic',
            'interpersonal_intelligence': 'interpersonal',
            'intrapersonal_intelligence': 'intrapersonal',
            'naturalistic_intelligence': 'naturalistic'
        }
        
        # Initialize feature mapping adapter
        self.feature_mappings = {
            'pore_density': ['pore_density', 'pore_count', 'pore_spatial_distribution'],
            'ridge_clarity': ['ridge_clarity', 'ridge_continuity', 'ridge_uniformity'],
            'graph_density': ['graph_density', 'network_density'],
            'fractal_dimension': ['fractal_dimension', 'box_counting_dimension'],
            'symmetry_index': ['symmetry_index', 'horizontal_symmetry', 'vertical_symmetry'],
            'lacunarity': ['lacunarity', 'fractal_lacunarity'],
            'modularity': ['modularity', 'community_modularity'],
            'betweenness_centrality': ['betweenness_centrality', 'centrality_betweenness'],
            'continuity_index': ['ridge_continuity', 'continuity_measure'],
            'uniformity_measure': ['ridge_uniformity', 'uniformity_score'],
            'cross_category_correlation': ['cross_category_correlation', 'feature_correlation'],
            'feature_stability_index': ['feature_stability', 'noise_robustness'],
            'community_cohesion': ['community_cohesion', 'modularity'],
            'fractal_imbalance': ['fractal_imbalance', 'fractal_regularity']
        }

    def _safe_value(self, val, key_name):
        """
        Safely handle values that extensions might call .lower() on.
        Returns appropriate type based on the key name and value.
        """
        # Special handling for pattern_type - should remain as string for .lower() calls
        if key_name == 'pattern_type':
            if isinstance(val, str):
                return val.lower()
            else:
                return str(val).lower()
        
        # For numeric features, keep as numeric
        if isinstance(val, (int, float)):
            return val
        
        # For string features that might need .lower(), convert to lowercase
        elif isinstance(val, str):
            return val.lower()
        
        # Fallback: convert to string then lowercase
        else:
            return str(val).lower()

    def _sanitize_features(self, features: Dict[str, Any]) -> Dict[str, Any]:
        """
        Sanitize all feature values to prevent type errors in extensions.
        """
        sanitized = {}
        for key, value in features.items():
            sanitized[key] = self._safe_value(value, key)
        return sanitized

    def _add_intelligence_aliases(self, features: Dict[str, Any]) -> Dict[str, Any]:
        """
        Add legacy intelligence key aliases for backward compatibility.
        """
        aliased_features = features.copy()
        
        # Add intelligence profile aliases
        for legacy_key, new_key in self.intelligence_aliases.items():
            if new_key in features and legacy_key not in features:
                aliased_features[legacy_key] = features[new_key]
        
        return aliased_features

    def adapt_features(self, extracted_features: Dict[str, Any]) -> Dict[str, Any]:
        """Adapt extracted features to match extension expectations."""
        adapted_features = {}
        adapted_features.update(extracted_features)
        
        for expected_name, possible_names in self.feature_mappings.items():
            found_value = None
            for possible_name in possible_names:
                if possible_name in extracted_features:
                    found_value = extracted_features[possible_name]
                    break
            
            if found_value is None:
                found_value = self._derive_feature_value(expected_name, extracted_features)
            
            if found_value is not None:
                adapted_features[expected_name] = found_value
        
        return adapted_features
    
    def _derive_feature_value(self, expected_name: str, extracted_features: Dict[str, Any]) -> float:
        """Derive feature values from related features."""
        if expected_name == 'pore_density':
            pore_count = extracted_features.get('pore_count', 0)
            return min(1.0, pore_count / 100.0)
        elif expected_name == 'ridge_clarity':
            ridge_continuity = extracted_features.get('ridge_continuity', 0.5)
            ridge_uniformity = extracted_features.get('ridge_uniformity', 0.5)
            return (ridge_continuity + ridge_uniformity) / 2.0
        elif expected_name == 'graph_density':
            return extracted_features.get('graph_density', 0.5)
        elif expected_name == 'symmetry_index':
            horizontal_symmetry = extracted_features.get('horizontal_symmetry', 0.5)
            vertical_symmetry = extracted_features.get('vertical_symmetry', 0.5)
            return (horizontal_symmetry + vertical_symmetry) / 2.0
        elif expected_name == 'fractal_dimension':
            return extracted_features.get('box_counting_dimension', 0.5)
        else:
            overall_quality = extracted_features.get('overall_quality', 0.5)
            return overall_quality * 0.5

    def run_all_extensions(self, features: Dict[str, Any]) -> Dict[str, Any]:
        """
        Run all registered extensions and aggregate their results.
        """
        # Step 1: Adapt features to match extension expectations
        adapted_features = self.adapt_features(features)
        
        # Step 2: Add intelligence profile aliases for backward compatibility
        aliased_features = self._add_intelligence_aliases(adapted_features)
        
        # Step 3: Sanitize all values to prevent type errors
        sanitized_features = self._sanitize_features(aliased_features)
        
        results = {}
        for ext in self.extensions:
            ext_name = ext.__class__.__name__
            try:
                results[ext_name] = ext.analyze(sanitized_features)
            except Exception as e:
                results[ext_name] = {'error': str(e)}
        return results 