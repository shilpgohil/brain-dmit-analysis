#!/usr/bin/env python3
"""
DMIT FEATURE MAPPING VALIDATOR
==============================
Validates mapping between fingerprint features and DMIT extensions.
"""

import json
import logging
from typing import Dict, Any, List
from datetime import datetime
from .base import DMITExtensionBase

logger = logging.getLogger(__name__)

class DMITFeatureMappingValidator:
    """Validates feature mapping between fingerprint features and DMIT extensions."""
    
    def __init__(self):
        self.feature_categories = {
            'basic_stats': ['mean_intensity', 'std_intensity', 'minutiae_count', 'minutiae_density'],
            'fractal_features': ['box_counting_dimension', 'fractal_dimension', 'lacunarity'],
            'topological_features': ['total_persistence', 'persistence_entropy', 'betti_0_estimate'],
            'graph_features': ['graph_density', 'betweenness_centrality', 'modularity'],
            'ridge_features': ['ridge_density', 'ridge_clarity', 'ridge_continuity'],
            'level3_features': ['pore_density', 'pore_spatial_distribution'],
            'spectral_features': ['frequency_entropy', 'dominant_frequency'],
            'meta_features': ['overall_quality', 'extraction_confidence']
        }
        
        # Extension-to-feature mappings
        self.extension_feature_mappings = {
            'EmotionalIntelligenceExtension': {
                'primary_features': ['pore_density', 'intrapersonal_intelligence_score', 'interpersonal_intelligence_score'],
                'secondary_features': ['ridge_clarity', 'continuity_index', 'graph_density'],
                'confidence_threshold': 0.7
            },
            'SpatialIntelligenceExtension': {
                'primary_features': ['spatial_awareness', 'visual_perception', 'spatial_reasoning'],
                'secondary_features': ['spatial_memory', 'spatial_creativity', 'architectural_thinking'],
                'confidence_threshold': 0.7
            },
            'LogicalMathematicalIntelligenceExtension': {
                'primary_features': ['logical_reasoning', 'mathematical_aptitude', 'analytical_thinking'],
                'secondary_features': ['critical_thinking', 'computational_thinking', 'pattern_recognition'],
                'confidence_threshold': 0.75
            }
        }
    
    def validate_feature_mapping(self, extracted_features: Dict[str, Any]) -> Dict[str, Any]:
        """Validate that all required features are present for each extension."""
        validation_results = {
            'timestamp': datetime.now().isoformat(),
            'total_extensions': len(self.extension_feature_mappings),
            'total_features_available': len(extracted_features),
            'extension_validation': {},
            'missing_features': {},
            'coverage_analysis': {},
            'recommendations': []
        }
        
        # Validate each extension
        for extension_name, mapping in self.extension_feature_mappings.items():
            ext_validation = {
                'primary_features_available': 0,
                'primary_features_missing': [],
                'secondary_features_available': 0,
                'secondary_features_missing': [],
                'coverage_percentage': 0.0,
                'confidence_level': 'low'
            }
            
            # Check primary features
            for feature in mapping['primary_features']:
                if feature in extracted_features:
                    ext_validation['primary_features_available'] += 1
                else:
                    ext_validation['primary_features_missing'].append(feature)
            
            # Check secondary features
            for feature in mapping['secondary_features']:
                if feature in extracted_features:
                    ext_validation['secondary_features_available'] += 1
                else:
                    ext_validation['secondary_features_missing'].append(feature)
            
            # Calculate coverage
            total_required = len(mapping['primary_features']) + len(mapping['secondary_features'])
            if total_required > 0:
                ext_validation['coverage_percentage'] = (
                    (ext_validation['primary_features_available'] + ext_validation['secondary_features_available']) 
                    / total_required * 100
                )
            
            # Determine confidence level
            if ext_validation['coverage_percentage'] >= 90:
                ext_validation['confidence_level'] = 'high'
            elif ext_validation['coverage_percentage'] >= 70:
                ext_validation['confidence_level'] = 'medium'
            else:
                ext_validation['confidence_level'] = 'low'
            
            validation_results['extension_validation'][extension_name] = ext_validation
            
            # Track missing features
            if ext_validation['primary_features_missing'] or ext_validation['secondary_features_missing']:
                validation_results['missing_features'][extension_name] = {
                    'primary': ext_validation['primary_features_missing'],
                    'secondary': ext_validation['secondary_features_missing']
                }
        
        # Coverage analysis
        total_extensions = len(self.extension_feature_mappings)
        high_confidence = sum(1 for ext in validation_results['extension_validation'].values() 
                            if ext['confidence_level'] == 'high')
        medium_confidence = sum(1 for ext in validation_results['extension_validation'].values() 
                              if ext['confidence_level'] == 'medium')
        low_confidence = sum(1 for ext in validation_results['extension_validation'].values() 
                           if ext['confidence_level'] == 'low')
        
        validation_results['coverage_analysis'] = {
            'high_confidence_extensions': high_confidence,
            'medium_confidence_extensions': medium_confidence,
            'low_confidence_extensions': low_confidence,
            'overall_coverage_percentage': (high_confidence + medium_confidence) / total_extensions * 100
        }
        
        return validation_results
    
    def generate_feature_mapping_document(self) -> str:
        """Generate a feature-to-extension mapping document."""
        doc_lines = [
            "# DMIT FEATURE-TO-EXTENSION MAPPING DOCUMENT",
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "## OVERVIEW",
            f"- Total Extensions: {len(self.extension_feature_mappings)}",
            f"- Total Feature Categories: {len(self.feature_categories)}",
            "",
            "## FEATURE CATEGORIES",
            ""
        ]
        
        for category, features in self.feature_categories.items():
            doc_lines.extend([
                f"### {category.upper().replace('_', ' ')} ({len(features)} features)",
                "```",
                ", ".join(features),
                "```",
                ""
            ])
        
        return "\n".join(doc_lines)

class FeatureMappingValidatorExtension(DMITExtensionBase):
    """
    Extension for analyzing Feature Mapping Validator from fingerprint features.
    Uses comprehensive fingerprint features for feature mapping validation analysis based on DMIT principles.
    """
    def analyze(self, features: Dict[str, Any]) -> Dict[str, Any]:
        # Extract real fingerprint features for feature mapping validation analysis
        ridge_clarity = features.get('ridge_clarity', 0.0)
        continuity_index = features.get('continuity_index', 0.0)
        uniformity_measure = features.get('uniformity_measure', 0.0)
        feature_stability_index = features.get('feature_stability_index', 0.0)
        pore_density = features.get('pore_density', 0.0)
        graph_density = features.get('graph_density', 0.0)
        modularity = features.get('modularity', 0.0)
        betweenness_centrality = features.get('betweenness_centrality', 0.0)
        symmetry_index = features.get('symmetry_index', 0.0)
        cross_category_correlation = features.get('cross_category_correlation', 0.0)
        community_cohesion = features.get('community_cohesion', 0.0)
        fractal_imbalance = features.get('fractal_imbalance', 0.0)
        fractal_dimension = features.get('fractal_dimension', 0.0)
        lacunarity = features.get('lacunarity', 0.0)
        ridge_density = features.get('ridge_density', 0.0)
        minutiae_count = features.get('minutiae_count', 0.0)
        ridge_count = features.get('ridge_count', 0.0)
        ridge_spacing = features.get('ridge_spacing', 0.0)
        ridge_orientation = features.get('ridge_orientation', 0.0)
        ridge_curvature = features.get('ridge_curvature', 0.0)
        ridge_ending_count = features.get('ridge_ending_count', 0.0)
        bifurcation_count = features.get('bifurcation_count', 0.0)
        island_count = features.get('island_count', 0.0)
        lake_count = features.get('lake_count', 0.0)
        delta_count = features.get('delta_count', 0.0)
        core_count = features.get('core_count', 0.0)
        whorl_count = features.get('whorl_count', 0.0)
        loop_count = features.get('loop_count', 0.0)
        arch_count = features.get('arch_count', 0.0)
        pattern_complexity = features.get('pattern_complexity', 0.0)
        pattern_regularity = features.get('pattern_regularity', 0.0)
        pattern_symmetry = features.get('pattern_symmetry', 0.0)
        pattern_diversity = features.get('pattern_diversity', 0.0)
        pattern_stability = features.get('pattern_stability', 0.0)
        pattern_consistency = features.get('pattern_consistency', 0.0)
        pattern_adaptability = features.get('pattern_adaptability', 0.0)
        pattern_optimization = features.get('pattern_optimization', 0.0)
        pattern_innovation = features.get('pattern_innovation', 0.0)
        pattern_learning = features.get('pattern_learning', 0.0)
        pattern_communication = features.get('pattern_communication', 0.0)
        pattern_collaboration = features.get('pattern_collaboration', 0.0)
        pattern_leadership = features.get('pattern_leadership', 0.0)
        pattern_creativity = features.get('pattern_creativity', 0.0)
        pattern_problem_solving = features.get('pattern_problem_solving', 0.0)
        pattern_resilience = features.get('pattern_resilience', 0.0)
        pattern_balance = features.get('pattern_balance', 0.0)
        pattern_effectiveness = features.get('pattern_effectiveness', 0.0)
        pattern_sustainability = features.get('pattern_sustainability', 0.0)
        pattern_impact = features.get('pattern_impact', 0.0)
        pattern_fulfillment = features.get('pattern_fulfillment', 0.0)
        pattern_consistency = features.get('pattern_consistency', 0.0)
        pattern_growth = features.get('pattern_growth', 0.0)
        pattern_awareness = features.get('pattern_awareness', 0.0)
        pattern_processing = features.get('pattern_processing', 0.0)
        pattern_decision_making = features.get('pattern_decision_making', 0.0)
        pattern_problem_solving_advanced = features.get('pattern_problem_solving_advanced', 0.0)
        pattern_memory = features.get('pattern_memory', 0.0)
        pattern_attention = features.get('pattern_attention', 0.0)
        pattern_holistic_thinking = features.get('pattern_holistic_thinking', 0.0)

        # Feature mapping validator analysis using DMIT scientific correlations
        validation_accuracy = (
            ridge_clarity * 0.25 +
            continuity_index * 0.20 +
            uniformity_measure * 0.20 +
            feature_stability_index * 0.20 +
            pore_density * 0.15
        )
        
        consistency_checking = (
            graph_density * 0.25 +
            modularity * 0.20 +
            betweenness_centrality * 0.20 +
            symmetry_index * 0.20 +
            cross_category_correlation * 0.15
        )
        
        quality_assurance = (
            community_cohesion * 0.25 +
            fractal_imbalance * 0.20 +
            fractal_dimension * 0.20 +
            lacunarity * 0.20 +
            ridge_density * 0.15
        )
        
        error_detection = (
            minutiae_count * 0.25 +
            ridge_count * 0.20 +
            ridge_spacing * 0.20 +
            ridge_orientation * 0.20 +
            ridge_curvature * 0.15
        )
        
        reliability_assessment = (
            ridge_ending_count * 0.25 +
            bifurcation_count * 0.20 +
            island_count * 0.20 +
            lake_count * 0.20 +
            delta_count * 0.15
        )
        
        integrity_verification = (
            core_count * 0.25 +
            whorl_count * 0.20 +
            loop_count * 0.20 +
            arch_count * 0.20 +
            pattern_complexity * 0.15
        )
        
        validator_optimization = (
            pattern_regularity * 0.25 +
            pattern_symmetry * 0.20 +
            pattern_diversity * 0.20 +
            pattern_stability * 0.20 +
            pattern_consistency * 0.15
        )
        
        validator_innovation = (
            pattern_adaptability * 0.25 +
            pattern_optimization * 0.20 +
            pattern_innovation * 0.20 +
            pattern_learning * 0.20 +
            pattern_communication * 0.15
        )
        
        validator_collaboration = (
            pattern_collaboration * 0.25 +
            pattern_leadership * 0.20 +
            pattern_creativity * 0.20 +
            pattern_problem_solving * 0.20 +
            pattern_resilience * 0.15
        )
        
        validator_effectiveness = (
            pattern_balance * 0.25 +
            pattern_effectiveness * 0.20 +
            pattern_sustainability * 0.20 +
            pattern_impact * 0.20 +
            pattern_fulfillment * 0.15
        )
        
        validator_consistency = (
            pattern_consistency * 0.25 +
            pattern_growth * 0.20 +
            pattern_awareness * 0.20 +
            pattern_processing * 0.20 +
            pattern_decision_making * 0.15
        )
        
        validator_advanced = (
            pattern_problem_solving_advanced * 0.25 +
            pattern_memory * 0.20 +
            pattern_attention * 0.20 +
            pattern_holistic_thinking * 0.20 +
            feature_stability_index * 0.15
        )

        # Overall feature mapping validator score
        feature_mapping_validator_score = (
            validation_accuracy * 0.20 +
            consistency_checking * 0.20 +
            quality_assurance * 0.15 +
            error_detection * 0.15 +
            reliability_assessment * 0.10 +
            integrity_verification * 0.10 +
            validator_optimization * 0.05 +
            validator_innovation * 0.05
        )

        # Determine feature mapping validator type
        validator_types = {
            'accurate': validation_accuracy,
            'consistent': consistency_checking,
            'quality_focused': quality_assurance,
            'error_detector': error_detection,
            'reliable': reliability_assessment,
            'integrity_focused': integrity_verification
        }
        primary_validator_type = max(validator_types.items(), key=lambda x: x[1])[0]

        # Normalize scores
        feature_mapping_validator_score = min(1.0, feature_mapping_validator_score * 2.3)
        validation_accuracy = min(1.0, validation_accuracy * 2.3)
        consistency_checking = min(1.0, consistency_checking * 2.3)
        quality_assurance = min(1.0, quality_assurance * 2.3)
        error_detection = min(1.0, error_detection * 2.3)

        return {
            'feature_mapping_validator_score': feature_mapping_validator_score,
            'primary_validator_type': primary_validator_type,
            'validation_accuracy': validation_accuracy,
            'consistency_checking': consistency_checking,
            'quality_assurance': quality_assurance,
            'error_detection': error_detection,
            'reliability_assessment': reliability_assessment,
            'integrity_verification': integrity_verification,
            'validator_optimization': validator_optimization,
            'validator_innovation': validator_innovation,
            'validator_collaboration': validator_collaboration,
            'validator_effectiveness': validator_effectiveness,
            'validator_consistency': validator_consistency,
            'validator_advanced': validator_advanced,
            'validator_profile': self.classify_validator_level(feature_mapping_validator_score)
        }

    @staticmethod
    def classify_validator_level(score: float) -> str:
        if score >= 0.85:
            return "Exceptional Feature Mapping Validator"
        elif score >= 0.75:
            return "High Feature Mapping Validator"
        elif score >= 0.65:
            return "Above Average Feature Mapping Validator"
        elif score >= 0.55:
            return "Average Feature Mapping Validator"
        else:
            return "Developing Feature Mapping Validator" 