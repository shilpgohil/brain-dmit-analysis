from typing import Dict, Any, List, Optional, Type
import numpy as np
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
from .problem_solving import ProblemSolvingExtension
from .learning_agility import LearningAgilityExtension
from .sustainability_intelligence import SustainabilityIntelligenceExtension
from .wellness_intelligence import WellnessIntelligenceExtension
from .adaptability_resilience import AdaptabilityResilienceExtension
from .team_collaboration import TeamCollaborationExtension
from .time_management import TimeManagementExtension
from .work_style import WorkStyleExtension

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
    # Registered so the premium report's COGNITIVE_KEYS (problem_solving_score,
    # analytical_thinking) actually receive data — the class existed but was
    # never in the registry, leaving those report rows permanently empty.
    ProblemSolvingExtension,
    LearningAgilityExtension,
    SustainabilityIntelligenceExtension,
    WellnessIntelligenceExtension,
    AdaptabilityResilienceExtension,
    TeamCollaborationExtension,
    TimeManagementExtension,
    WorkStyleExtension,
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
            'betweenness_centrality': ['betweenness_centrality', 'betweenness_centrality_mean'],
            'continuity_index': ['ridge_continuity', 'continuity_measure'],
            'uniformity_measure': ['ridge_uniformity', 'uniformity_score'],
            'cross_category_correlation': ['cross_category_correlation', 'feature_correlation'],
            'feature_stability_index': ['feature_stability', 'noise_robustness'],
            'community_cohesion': ['community_cohesion', 'modularity'],
            'fractal_imbalance': ['fractal_imbalance', 'fractal_regularity'],
            # Graph aliases
            'clustering_coefficient': ['average_clustering', 'clustering_coefficient'],
            'spectral_entropy': ['spectral_entropy', 'spectral_entropy'],
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
        sanitized = {}
        for key, value in features.items():
            if value is None:
                continue
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

        # ── FIX 1: Translate pattern_family (int) → pattern_type (str) ──────────
        # The extractor outputs pattern_family as 0=arch, 1=loop, 2=whorl, -1=unknown.
        # All extensions expect a string key 'pattern_type'.
        family_to_type = {0: 'arch', 1: 'loop', 2: 'whorl', 3: 'composite', -1: 'loop'}
        raw_family = extracted_features.get('pattern_family', -1)
        try:
            raw_family_int = int(raw_family) if raw_family is not None else -1
        except (ValueError, TypeError):
            raw_family_int = -1
        adapted_features['pattern_type'] = family_to_type.get(raw_family_int, 'loop')

        # ── FIX 2: Normalize TFRC to correct range ───────────────────────────────
        # TFRC per finger is 0–30. Normalize to 0–1 before extensions use it.
        # Extensions should use 'tfrc_normalized' in their formulas.
        raw_tfrc = extracted_features.get('tfrc', 0) or 0
        adapted_features['tfrc_normalized'] = min(1.0, float(raw_tfrc) / 25.0)

        # ── FIX 3: Add graph/clustering aliases ─────────────────────────────────
        # Extensions expect 'clustering_coefficient' but extractor outputs 'average_clustering'
        if 'clustering_coefficient' not in adapted_features:
            adapted_features['clustering_coefficient'] = extracted_features.get('average_clustering', 0.0) or 0.0

        # Extensions expect 'betweenness_centrality' but extractor outputs 'betweenness_centrality_mean'
        if 'betweenness_centrality' not in adapted_features:
            adapted_features['betweenness_centrality'] = extracted_features.get('betweenness_centrality_mean', 0.0) or 0.0

        # ── FIX 4: Map feature aliases from feature_mappings table ───────────────
        for expected_name, possible_names in self.feature_mappings.items():
            if expected_name in adapted_features:
                continue  # Already set by fixes above
            found_value = None
            for possible_name in possible_names:
                if possible_name in extracted_features:
                    found_value = extracted_features[possible_name]
                    break
            if found_value is not None:
                adapted_features[expected_name] = found_value

        # ── FIX 5: Scale-normalize features to the [0,1] domain extensions assume ─
        # The extractor emits RAW-magnitude topological/spectral features, but the
        # extensions consume them through `min(1.0, x / D)` idioms that assume the
        # input is already small. With raw values (betti_1≈183, euler≈-173,
        # spectral_rolloff≈234) every such sub-score saturated at 1.0 for ALL
        # subjects — i.e. it stopped responding to the fingerprint. Likewise ~37
        # keys the extensions read are never produced (h1_num_features,
        # fractal_complexity, spectral_centroid/bandwidth/energy, pattern_symmetry,
        # ridge_continuity, ...), so those sub-scores defaulted to 0/constant.
        # Both destroy differentiation. _normalize_for_extensions provides every
        # consumed key as a real, bounded measurement scaled to the magnitude the
        # extension transforms expect, so scores vary monotonically with the print.
        self._normalize_for_extensions(adapted_features)

        return adapted_features

    @staticmethod
    def _clamp01(value: float) -> float:
        return max(0.0, min(1.0, float(value)))

    def _normalize_for_extensions(self, f: Dict[str, Any]) -> None:
        """
        In-place scaling + derivation so every feature an extension reads is a
        real, bounded biometric measurement. Each scale is documented with the
        observed real range (from finger_prints/) and the consuming idiom.

        Design rule: for a `/D` consumer we supply the value pre-scaled into
        [0, D] so `value/D` lands in [0,1] WITH spread (never a saturated 1.0).
        For a `min(1.0, x)` consumer we supply x already in [0,1]. Raw keys used
        by correct band-checks (fractal dimensions in [1,2]) are left untouched.
        """
        def g(key, default=0.0):
            v = f.get(key, default)
            try:
                return float(v) if v is not None else default
            except (TypeError, ValueError):
                return default

        # --- Topology counts (consumers divide by 10; raw counts are 10x-200x too big) ---
        # betti_1 / h1: 1-D homology loop count. Real range ~150-210 → map to [0,10].
        betti_1_raw = g('betti_1')
        f['betti_1'] = 10.0 * self._clamp01(betti_1_raw / 250.0)
        f['h1_num_features'] = f['betti_1']                       # same concept; was missing entirely
        # betti_0: connected components. Real range ~3-40 → map to [0,10].
        f['betti_0'] = 10.0 * self._clamp01(g('betti_0') / 40.0)
        # Euler characteristic: real range ~ -200..-135 (very negative = complex).
        # Consumers use abs(euler)/10 and sign checks (< 0), so keep the sign and
        # map the magnitude into [0,10].
        euler_raw = g('euler_characteristic')
        euler_mag = 10.0 * self._clamp01(abs(euler_raw) / 250.0)
        f['euler_characteristic'] = -euler_mag if euler_raw < 0 else euler_mag

        # --- Spectral features (mixed consumers) ---
        # spectral_radius: real ~3.4-4.2, consumers use /10 with a >0 guard → map to [0,10].
        f['spectral_radius'] = 10.0 * self._clamp01(g('spectral_radius') / 6.0)
        # spectral_rolloff: extractor emits a 0-255 rolloff index; consumers do min(1.0, x).
        f['spectral_rolloff'] = self._clamp01(g('spectral_rolloff') / 255.0)
        # spectral_entropy: real ~0.008-0.07 (tiny); rescale so it spans [0,1] meaningfully.
        f['spectral_entropy'] = self._clamp01(g('spectral_entropy') / 0.1)
        # spectral_centroid / bandwidth / energy: NEVER produced by the extractor
        # (read by 39 extensions). Derive bounded proxies from real spectral features.
        f['spectral_centroid'] = self._clamp01(g('power_concentration'))            # spectral mass concentration
        f['spectral_bandwidth'] = self._clamp01(g('fourier_harmonic_ratio'))        # harmonic spread proxy
        # fourier_energy_total is ~1e14; log-normalize to [0,1].
        energy_raw = g('fourier_energy_total')
        f['spectral_energy'] = self._clamp01((np.log10(energy_raw + 1.0)) / 16.0) if energy_raw > 0 else 0.0

        # --- Fractal complexity (missing; read by 39 extensions) ---
        # box_counting_dimension is a fractal dimension in [1,2]; map (d-1) → [0,1].
        # Leave the raw dimension keys untouched for the band-check consumers.
        f['fractal_complexity'] = self._clamp01(g('box_counting_dimension', 1.0) - 1.0)

        # --- Pattern descriptors (missing; read by 41 extensions) ---
        f['pattern_symmetry'] = self._clamp01(g('pattern_symmetry_score'))
        # Regularity from stable, real measures of ridge order.
        f['pattern_regularity'] = self._clamp01(
            (g('ridge_flow_quality') + g('scale_consistency') + g('feature_stability')) / 3.0
        )
        # whorl_complexity from the real whorl analysis outputs (0 for non-whorls).
        f['whorl_complexity'] = self._clamp01(
            max(g('whorl_spiral_complexity'), g('whorl_logical_layering_score'))
        )

        # --- Ridge descriptors (missing; read by ~39 extensions) ---
        f['ridge_continuity'] = self._clamp01(g('ridge_flow_quality'))
        f['ridge_uniformity'] = self._clamp01(g('scale_consistency'))
        f['mean_ridge_thickness'] = self._clamp01(g('ridge_thickness') / 5.0) if 'ridge_thickness' in f \
            else self._clamp01(g('ridge_density') * 2.0)
        # dominant_direction is a signed angle proxy in ~[-1,1]; map to [0,1].
        f['mean_ridge_orientation'] = self._clamp01((g('dominant_direction') + 1.0) / 2.0)
        f['mean_ridge_curvature'] = self._clamp01(g('contour_complexity') / 30.0)

        # --- Pore / minutiae counts read by ~39 extensions ---
        # pore_density is a top-hat blob count per 1000px on real scanner crops
        # (~320x480); observed range ~4-9, so /15 spans [0,1] with real spread
        # instead of saturating every image to 1.0 via a bare clamp.
        f['pore_count'] = self._clamp01(g('pore_density') / 15.0)
        # minutiae_density is emitted as minutiae per 10,000 px. With ~12 px
        # non-max-suppression spacing the physical ceiling is ~69 per 10k px;
        # /50 maps realistic prints (~25-45) onto [0.5, 0.9] with real spread.
        f['minutiae_density'] = self._clamp01(g('minutiae_density') / 50.0)

        # --- Bilateral pair features (LeftRightBrainExtension only) ---
        # True left/right hand split is not available per single finger; mirror the
        # single-hand measurement so the extension's symmetry math is well-defined
        # (it already has an internal fallback, this just removes the silent zeros).
        for base, pair in (
            ('ridge_count', ('ridge_count_left', 'ridge_count_right')),
            ('ridge_density', ('ridge_density_left', 'ridge_density_right')),
            ('graph_density', ('graph_density_left', 'graph_density_right')),
            ('spectral_radius', ('spectral_radius_left', 'spectral_radius_right')),
            ('topological_complexity', ('topological_complexity_left', 'topological_complexity_right')),
            ('euler_characteristic', ('euler_characteristic_left', 'euler_characteristic_right')),
            ('fractal_complexity', ('fractal_dimension_left', 'fractal_dimension_right')),
        ):
            val = f.get(base, 0.0)
            for pk in pair:
                f.setdefault(pk, val)
        f.setdefault('horizontal_symmetry', f.get('pattern_symmetry', 0.0))
        f.setdefault('vertical_symmetry', f.get('pattern_symmetry', 0.0))
        f.setdefault('pattern_asymmetry', 1.0 - f.get('pattern_symmetry', 0.0))
        f.setdefault('orientation_coherence', f.get('ridge_flow_quality', 0.0)
                     if 'ridge_flow_quality' in f else f.get('pattern_regularity', 0.0))
        f.setdefault('ridge_flow_curvature', f.get('mean_ridge_curvature', 0.0))
        f.setdefault('ridge_orientation', f.get('mean_ridge_orientation', 0.0))
    
    def _derive_feature_value(self, expected_name: str, extracted_features: Dict[str, Any]) -> Optional[float]:
        if expected_name == 'pore_density':
            pore_count = extracted_features.get('pore_count')
            return min(1.0, pore_count / 100.0) if pore_count is not None else None
        if expected_name == 'ridge_clarity':
            rc = extracted_features.get('ridge_continuity')
            ru = extracted_features.get('ridge_uniformity')
            present = [v for v in (rc, ru) if v is not None]
            return sum(present) / len(present) if present else None
        if expected_name == 'graph_density':
            return extracted_features.get('graph_density')
        if expected_name == 'symmetry_index':
            hs = extracted_features.get('horizontal_symmetry')
            vs = extracted_features.get('vertical_symmetry')
            present = [v for v in (hs, vs) if v is not None]
            return sum(present) / len(present) if present else None
        if expected_name == 'fractal_dimension':
            return extracted_features.get('box_counting_dimension')
        return None

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