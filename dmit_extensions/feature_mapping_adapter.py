#!/usr/bin/env python3
"""
DMIT FEATURE MAPPING ADAPTER
============================
Bridges the gap between extracted fingerprint features and DMIT extension expectations.

Handles attribute naming inconsistencies between analyzers and DMIT extensions.
Ensures all features are properly mapped regardless of naming variations.

Author: DMIT Research Team
"""

import logging
from typing import Dict, Any, List, Optional
from .base import DMITExtensionBase

logger = logging.getLogger(__name__)

class DMITFeatureMappingAdapter:
    """
    Adapts extracted fingerprint features to match DMIT extension expectations.
    """
    
    def __init__(self):
        # Expanded feature mapping dictionary: extension_expected_name -> actual_feature_names
        self.feature_mappings = {
            'pore_density': ['pore_density', 'pore_combined_density', 'pore_blob_density', 'pore_morphological_density', 'pore_count', 'pore_spatial_distribution'],
            'ridge_clarity': ['ridge_clarity', 'ridge_continuity', 'ridge_uniformity'],
            'graph_density': ['graph_density', 'network_density'],
            'fractal_dimension': ['fractal_dimension', 'box_counting_dimension', 'mean_fractal_dimension'],
            'symmetry_index': ['symmetry_index', 'horizontal_symmetry', 'vertical_symmetry'],
            'lacunarity': ['lacunarity', 'fractal_lacunarity'],
            'modularity': ['modularity', 'community_modularity'],
            'betweenness_centrality': ['betweenness_centrality', 'betweenness_centrality_mean', 'centrality_betweenness'],
            'continuity_index': ['ridge_continuity', 'continuity_measure'],
            'uniformity_measure': ['ridge_uniformity', 'uniformity_score'],
            'cross_category_correlation': ['cross_category_correlation', 'feature_correlation'],
            'feature_stability_index': ['feature_stability', 'noise_robustness'],
            'community_cohesion': ['community_cohesion', 'modularity'],
            'fractal_imbalance': ['fractal_imbalance', 'fractal_regularity'],
            'minutiae_count': ['minutiae_count', 'h0_num_features'],
            'minutiae_density': ['minutiae_density'],
            'ridge_density': ['ridge_density', 'global_ridge_density', 'local_density_mean'],
            'ridge_thickness': ['mean_ridge_thickness'],
            'ridge_orientation': ['mean_ridge_orientation'],
            'ridge_length': ['mean_ridge_length'],
            'ridge_curvature': ['mean_ridge_curvature'],
            'pattern_regularity': ['pattern_regularity'],
            'spectral_entropy': ['spectral_entropy', 'frequency_spectrum_entropy'],
            'spectral_energy': ['spectral_energy'],
            'spectral_radius': ['spectral_radius'],
            'diameter': ['diameter'],
            'radius': ['radius'],
            'average_shortest_path': ['average_shortest_path'],
            'mean_degree': ['mean_degree'],
            'std_degree': ['std_degree'],
            'max_degree': ['max_degree'],
            'min_degree': ['min_degree'],
            'average_clustering': ['average_clustering'],
            'transitivity': ['transitivity'],
            'num_communities': ['num_communities'],
            'mean_community_size': ['mean_community_size'],
            'std_community_size': ['std_community_size'],
            'max_community_size': ['max_community_size'],
            'num_triangles': ['num_triangles'],
            'triangle_density': ['triangle_density'],
            'num_squares': ['num_squares'],
            'num_star_centers': ['num_star_centers'],
            'mean_edge_weight': ['mean_edge_weight'],
            'std_edge_weight': ['std_edge_weight'],
            'mean_edge_distance': ['mean_edge_distance'],
            'std_edge_distance': ['std_edge_distance'],
            'mean_angle_difference': ['mean_angle_difference'],
            'std_angle_difference': ['std_angle_difference'],
            'num_isolated_nodes': ['num_isolated_nodes'],
            'num_pendant_nodes': ['num_pendant_nodes'],
            'tfrc': ['tfrc'],
            'average_ridge_count': ['average_ridge_count'],
            'std_ridge_count': ['std_ridge_count'],
            'max_ridge_count': ['max_ridge_count'],
            'min_ridge_count': ['min_ridge_count'],
            'ridge_count_pairs': ['ridge_count_pairs'],
            'global_ridge_density': ['global_ridge_density'],
            'local_density_mean': ['local_density_mean'],
            'local_density_std': ['local_density_std'],
            'local_density_max': ['local_density_max'],
            'local_density_min': ['local_density_min'],
            'mean_ridge_thickness': ['mean_ridge_thickness'],
            'std_ridge_thickness': ['std_ridge_thickness'],
            'max_ridge_thickness': ['max_ridge_thickness'],
            'min_ridge_thickness': ['min_ridge_thickness'],
            'mean_ridge_orientation': ['mean_ridge_orientation'],
            'ridge_orientation_consistency': ['ridge_orientation_consistency'],
            'ridge_orientation_variance': ['ridge_orientation_variance'],
            'ridge_orientation_std': ['ridge_orientation_std'],
            'ridge_flow_curvature_mean': ['ridge_flow_curvature_mean'],
            'ridge_flow_curvature_std': ['ridge_flow_curvature_std'],
            'ridge_flow_smoothness': ['ridge_flow_smoothness'],
            'mean_ridge_length': ['mean_ridge_length'],
            'std_ridge_length': ['std_ridge_length'],
            'max_ridge_length': ['max_ridge_length'],
            'num_ridge_segments': ['num_ridge_segments'],
            'ridge_spacing_pixels': ['ridge_spacing_pixels'],
            'frequency_spectrum_entropy': ['frequency_spectrum_entropy'],
            'frequency_peak_sharpness': ['frequency_peak_sharpness'],
            'mean_valley_width': ['mean_valley_width'],
            'std_valley_width': ['std_valley_width'],
            'max_valley_width': ['max_valley_width'],
            'mean_inter_ridge_distance': ['mean_inter_ridge_distance'],
            'std_inter_ridge_distance': ['std_inter_ridge_distance'],
            'min_inter_ridge_distance': ['min_inter_ridge_distance'],
            'max_inter_ridge_distance': ['max_inter_ridge_distance'],
            'mean_ridge_curvature': ['mean_ridge_curvature'],
            'std_ridge_curvature': ['std_ridge_curvature'],
            'max_ridge_curvature': ['max_ridge_curvature'],
            'ridge_pattern_complexity': ['ridge_pattern_complexity'],
            'horizontal_symmetry': ['horizontal_symmetry'],
            'vertical_symmetry': ['vertical_symmetry'],
            'pore_blob_count': ['pore_blob_count'],
            'pore_blob_density': ['pore_blob_density'],
            'pore_blob_mean_size': ['pore_blob_mean_size'],
            'pore_blob_size_std': ['pore_blob_size_std'],
            'pore_blob_max_size': ['pore_blob_max_size'],
            'pore_blob_min_size': ['pore_blob_min_size'],
            'pore_blob_mean_distance': ['pore_blob_mean_distance'],
            'pore_blob_distance_std': ['pore_blob_distance_std'],
            'pore_template_count': ['pore_template_count'],
            'pore_template_density': ['pore_template_density'],
            'pore_template_mean_size': ['pore_template_mean_size'],
            'pore_template_size_std': ['pore_template_size_std'],
            'pore_morphological_count': ['pore_morphological_count'],
            'pore_morphological_density': ['pore_morphological_density'],
            'pore_morphological_mean_size': ['pore_morphological_mean_size'],
            'pore_morphological_size_std': ['pore_morphological_size_std'],
            'pore_morphological_max_size': ['pore_morphological_max_size'],
            'pore_morphological_min_size': ['pore_morphological_min_size'],
            'pore_morphological_mean_distance': ['pore_morphological_mean_distance'],
            'pore_morphological_distance_std': ['pore_morphological_distance_std'],
            'pore_combined_count': ['pore_combined_count'],
            'pore_combined_density': ['pore_combined_density'],
            'pore_combined_mean_size': ['pore_combined_mean_size'],
            'pore_combined_size_std': ['pore_combined_size_std'],
            'pore_combined_max_size': ['pore_combined_max_size'],
            'pore_combined_min_size': ['pore_combined_min_size'],
            'pore_combined_mean_distance': ['pore_combined_mean_distance'],
            'pore_combined_distance_std': ['pore_combined_distance_std'],
            'incipient_ridge_count': ['incipient_ridge_count'],
            'incipient_ridge_mean_length': ['incipient_ridge_mean_length'],
            'incipient_ridge_length_std': ['incipient_ridge_length_std'],
            'incipient_ridge_angle_std': ['incipient_ridge_angle_std'],
            'contour_count': ['contour_count'],
            'total_contour_length': ['total_contour_length'],
            'mean_contour_length': ['mean_contour_length'],
            'contour_length_std': ['contour_length_std'],
            'mean_contour_area': ['mean_contour_area'],
            'contour_area_std': ['contour_area_std'],
            'mean_contour_complexity': ['mean_contour_complexity'],
            'contour_complexity_std': ['contour_complexity_std'],
            'lbp_mean': ['lbp_mean'],
            'lbp_std': ['lbp_std'],
            'lbp_entropy': ['lbp_entropy'],
            'glcm_contrast': ['glcm_contrast'],
            'glcm_homogeneity': ['glcm_homogeneity'],
            'glcm_energy': ['glcm_energy'],
            'glcm_correlation': ['glcm_correlation'],
            'dc_component': ['dc_component'],
            'radial_power_spectrum': ['radial_power_spectrum']
        }
    
    def adapt_features(self, extracted_features: Dict[str, Any]) -> Dict[str, Any]:
        """
        Adapt extracted features to match extension expectations.
        """
        adapted_features = {}
        
        # First, copy all original features
        adapted_features.update(extracted_features)
        
        # Then map extension-expected features to actual features
        for expected_name, possible_names in self.feature_mappings.items():
            # Try to find a matching feature
            found_value = None
            for possible_name in possible_names:
                if possible_name in extracted_features:
                    found_value = extracted_features[possible_name]
                    break
            
            # If not found, try to derive from related features
            if found_value is None:
                found_value = self._derive_feature_value(expected_name, extracted_features)
            
            # Add the mapped feature
            if found_value is not None:
                adapted_features[expected_name] = found_value
        
        return adapted_features
    
    def _derive_feature_value(self, expected_name: str, extracted_features: Dict[str, Any]) -> float:
        """
        Derive feature values from related features when exact matches aren't found.
        """
        # Pore density fallback
        if expected_name == 'pore_density':
            # Try all possible pore density features
            for key in ['pore_combined_density', 'pore_blob_density', 'pore_morphological_density', 'pore_density', 'pore_count']:
                if key in extracted_features:
                    val = extracted_features[key]
                    if key == 'pore_count':
                        return min(1.0, val / 100.0)
                    return val
            return 0.0
        # Ridge clarity fallback
        elif expected_name == 'ridge_clarity':
            vals = [extracted_features.get(k, None) for k in ['ridge_clarity', 'ridge_continuity', 'ridge_uniformity'] if k in extracted_features]
            # Filter out None values
            vals = [v for v in vals if v is not None]
            if vals:
                return sum(vals) / len(vals)
            return 0.5
        # Graph density fallback
        elif expected_name == 'graph_density':
            return extracted_features.get('graph_density', extracted_features.get('network_density', 0.5))
        # Symmetry index fallback
        elif expected_name == 'symmetry_index':
            h = extracted_features.get('horizontal_symmetry', None)
            v = extracted_features.get('vertical_symmetry', None)
            if h is not None and v is not None:
                return (h + v) / 2.0
            elif h is not None:
                return h
            elif v is not None:
                return v
            return 0.5
        # Fractal dimension fallback
        elif expected_name == 'fractal_dimension':
            for key in ['fractal_dimension', 'box_counting_dimension', 'mean_fractal_dimension']:
                if key in extracted_features:
                    return extracted_features[key]
            return 0.5
        # Minutiae count fallback
        elif expected_name == 'minutiae_count':
            return extracted_features.get('minutiae_count', extracted_features.get('h0_num_features', 0))
        # Ridge density fallback
        elif expected_name == 'ridge_density':
            for key in ['ridge_density', 'global_ridge_density', 'local_density_mean']:
                if key in extracted_features:
                    return extracted_features[key]
            return 0.5
        # Ridge thickness fallback
        elif expected_name == 'ridge_thickness':
            return extracted_features.get('mean_ridge_thickness', 0.5)
        # Ridge orientation fallback
        elif expected_name == 'ridge_orientation':
            return extracted_features.get('mean_ridge_orientation', 0.5)
        # Ridge length fallback
        elif expected_name == 'ridge_length':
            return extracted_features.get('mean_ridge_length', 0.5)
        # Ridge curvature fallback
        elif expected_name == 'ridge_curvature':
            return extracted_features.get('mean_ridge_curvature', 0.5)
        # Pattern regularity fallback
        elif expected_name == 'pattern_regularity':
            return extracted_features.get('pattern_regularity', 0.5)
        # Spectral entropy fallback
        elif expected_name == 'spectral_entropy':
            return extracted_features.get('spectral_entropy', extracted_features.get('frequency_spectrum_entropy', 0.5))
        # Spectral energy fallback
        elif expected_name == 'spectral_energy':
            return extracted_features.get('spectral_energy', 0.5)
        # Betweenness centrality fallback
        elif expected_name == 'betweenness_centrality':
            for key in ['betweenness_centrality', 'betweenness_centrality_mean', 'centrality_betweenness']:
                if key in extracted_features:
                    return extracted_features[key]
            return 0.0
        # Modularity fallback
        elif expected_name == 'modularity':
            return extracted_features.get('modularity', 0.5)
        # General fallback: use overall_quality if available
        else:
            return extracted_features.get('overall_quality', 0.5) * 0.5
    
    def get_mapping_statistics(self, extracted_features: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get statistics about feature mapping success.
        """
        adapted_features = self.adapt_features(extracted_features)
        
        total_expected = len(self.feature_mappings)
        total_mapped = sum(1 for expected_name in self.feature_mappings.keys() 
                          if expected_name in adapted_features)
        
        return {
            'total_expected_features': total_expected,
            'total_mapped_features': total_mapped,
            'mapping_success_rate': total_mapped / total_expected if total_expected > 0 else 0.0,
            'original_features': len(extracted_features),
            'adapted_features': len(adapted_features)
        }

class FeatureMappingAdapterExtension(DMITExtensionBase):
    """
    Comprehensive feature mapping adapter that handles all naming inconsistencies
    between different analyzers and DMIT extensions.
    """
    
    def __init__(self):
        super().__init__()
        self.extension_name = "Feature Mapping Adapter"
        self.extension_version = "2.0"
        
        # 🔧 COMPREHENSIVE FEATURE MAPPINGS
        # Maps expected DMIT feature names to all possible variations found in analyzers
        self.feature_mappings = {
            # Ridge-related features
            'ridge_density': ['ridge_density', 'global_ridge_density', 'local_density_mean', 'density_mean'],
            'ridge_thickness': ['ridge_thickness', 'mean_ridge_thickness', 'thickness_mean'],
            'ridge_orientation': ['ridge_orientation', 'mean_ridge_orientation', 'orientation_mean'],
            'ridge_curvature': ['ridge_curvature', 'mean_ridge_curvature', 'ridge_flow_curvature_mean', 'curvature_mean'],
            'ridge_count': ['ridge_count', 'tfrc', 'average_ridge_count', 'total_ridge_count'],
            'ridge_spacing': ['ridge_spacing', 'mean_ridge_spacing', 'spacing_mean'],
            'ridge_clarity': ['ridge_clarity', 'clarity_score', 'clarity'],
            
            # Pattern-related features
            'pattern_type': ['pattern_type', 'primary_pattern', 'pattern_classification'],
            'pattern_complexity': ['pattern_complexity', 'ridge_pattern_complexity', 'complexity_score'],
            'pattern_regularity': ['pattern_regularity', 'regularity_score', 'regularity'],
            
            # Minutiae features
            'minutiae_count': ['minutiae_count', 'total_minutiae', 'minutiae_total'],
            'minutiae_density': ['minutiae_density', 'minutiae_per_area', 'density_minutiae'],
            'bifurcation_count': ['bifurcation_count', 'bifurcations', 'bifurcation_total'],
            'ridge_ending_count': ['ridge_ending_count', 'ridge_endings', 'ending_count'],
            
            # Quality and confidence features
            'quality_score': ['quality_score', 'image_quality', 'overall_quality', 'quality'],
            'confidence_score': ['confidence_score', 'confidence', 'analysis_confidence', 'overall_confidence'],
            
            # Statistical features
            'mean_intensity': ['mean_intensity', 'intensity_mean', 'average_intensity'],
            'std_intensity': ['std_intensity', 'intensity_std', 'intensity_standard_deviation'],
            'entropy': ['entropy', 'image_entropy', 'information_entropy'],
            
            # Fractal features
            'fractal_dimension': ['fractal_dimension', 'box_counting_dimension', 'fractal_d'],
            'lacunarity': ['lacunarity', 'fractal_lacunarity', 'lacunarity_score'],
            
            # Topological features
            'euler_characteristic': ['euler_characteristic', 'euler_number', 'topology_euler'],
            'connectivity': ['connectivity', 'topological_connectivity', 'connectivity_score'],
            
            # Graph features
            'graph_density': ['graph_density', 'network_density', 'density_graph'],
            'modularity': ['modularity', 'graph_modularity', 'modularity_score'],
            'betweenness_centrality': ['betweenness_centrality', 'centrality_betweenness', 'betweenness'],
            
            # Spectral features
            'spectral_density': ['spectral_density', 'frequency_density', 'spectral_power'],
            'dominant_frequency': ['dominant_frequency', 'peak_frequency', 'main_frequency'],
            
            # Meta features
            'feature_count': ['feature_count', 'total_features', 'features_extracted'],
            'analysis_level': ['analysis_level', 'level', 'analysis_type'],
        }
        
        # Priority order for feature extraction (most reliable sources first)
        self.feature_priorities = {
            'ridge_density': ['ridge_density', 'global_ridge_density', 'local_density_mean'],
            'ridge_thickness': ['ridge_thickness', 'mean_ridge_thickness'],
            'ridge_orientation': ['ridge_orientation', 'mean_ridge_orientation'],
            'ridge_curvature': ['ridge_curvature', 'mean_ridge_curvature'],
            'pattern_complexity': ['pattern_complexity', 'ridge_pattern_complexity'],
            'minutiae_count': ['minutiae_count', 'total_minutiae'],
            'quality_score': ['quality_score', 'image_quality'],
            'confidence_score': ['confidence_score', 'confidence'],
        }
        
        logger.info(f"🔧 {self.extension_name} v{self.extension_version} initialized with {len(self.feature_mappings)} feature mappings")

    def analyze(self, features: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze and standardize features using comprehensive mapping.
        
        Args:
            features: Raw features from analyzers with potential naming inconsistencies
            
        Returns:
            Standardized features with consistent naming for DMIT extensions
        """
        try:
            logger.info(f"🔧 Starting feature mapping analysis for {len(features)} features")
            
            # Create standardized feature dictionary
            standardized_features = {}
            mapping_stats = {
                'total_features_input': len(features),
                'features_mapped': 0,
                'features_missing': 0,
                'mapping_errors': 0,
                'mapping_details': {}
            }
            
            # Map each expected feature
            for expected_name, possible_names in self.feature_mappings.items():
                try:
                    # Try to find the feature using any of the possible names
                    found_value = None
                    found_name = None
                    
                    for possible_name in possible_names:
                        if possible_name in features:
                            found_value = features[possible_name]
                            found_name = possible_name
                            break
                    
                    if found_value is not None:
                        standardized_features[expected_name] = found_value
                        mapping_stats['features_mapped'] += 1
                        mapping_stats['mapping_details'][expected_name] = {
                            'found_as': found_name,
                            'value': found_value,
                            'status': 'mapped'
                        }
                        logger.debug(f"✅ Mapped {expected_name} from {found_name}")
                    else:
                        # Try to find in nested structures
                        found_value = self._search_nested_features(features, possible_names)
                        if found_value is not None:
                            standardized_features[expected_name] = found_value
                            mapping_stats['features_mapped'] += 1
                            mapping_stats['mapping_details'][expected_name] = {
                                'found_as': 'nested_search',
                                'value': found_value,
                                'status': 'mapped_nested'
                            }
                            logger.debug(f"✅ Mapped {expected_name} from nested search")
                        else:
                            # Use default value based on feature type
                            default_value = self._get_default_value(expected_name)
                            standardized_features[expected_name] = default_value
                            mapping_stats['features_missing'] += 1
                            mapping_stats['mapping_details'][expected_name] = {
                                'found_as': None,
                                'value': default_value,
                                'status': 'default_used'
                            }
                            logger.warning(f"⚠️ Feature {expected_name} not found, using default: {default_value}")
                            
                except Exception as e:
                    logger.error(f"❌ Error mapping feature {expected_name}: {e}")
                    mapping_stats['mapping_errors'] += 1
                    mapping_stats['mapping_details'][expected_name] = {
                        'found_as': None,
                        'value': self._get_default_value(expected_name),
                        'status': 'error',
                        'error': str(e)
                    }
            
            # Add mapping statistics to results
            standardized_features['_mapping_stats'] = mapping_stats
            
            # Validate critical features
            validation_result = self._validate_critical_features(standardized_features)
            standardized_features['_validation'] = validation_result
            
            logger.info(f"✅ Feature mapping completed: {mapping_stats['features_mapped']} mapped, "
                       f"{mapping_stats['features_missing']} missing, {mapping_stats['mapping_errors']} errors")
            
            return standardized_features
            
        except Exception as e:
            logger.error(f"❌ Feature mapping analysis failed: {e}")
            return {
                'error': str(e),
                '_mapping_stats': {
                    'total_features_input': len(features),
                    'features_mapped': 0,
                    'features_missing': len(features),
                    'mapping_errors': 1,
                    'mapping_details': {}
                }
            }

    def _search_nested_features(self, features: Dict[str, Any], possible_names: List[str]) -> Optional[Any]:
        """
        Search for features in nested structures (e.g., ridge_features, basic_stats, etc.)
        """
        try:
            # Common nested structure names
            nested_structures = ['ridge_features', 'basic_stats', 'fractal_features', 
                               'topological_features', 'graph_features', 'spectral_features', 
                               'meta_features', 'level3_features']
            
            for structure_name in nested_structures:
                if structure_name in features and isinstance(features[structure_name], dict):
                    structure = features[structure_name]
                    for possible_name in possible_names:
                        if possible_name in structure:
                            return structure[possible_name]
            
            return None
            
        except Exception as e:
            logger.debug(f"Error in nested feature search: {e}")
            return None

    def _get_default_value(self, feature_name: str) -> Any:
        """
        Get appropriate default value based on feature type
        """
        # Numeric features
        if any(keyword in feature_name for keyword in ['count', 'density', 'score', 'confidence', 'quality']):
            return 0.0
        elif any(keyword in feature_name for keyword in ['dimension', 'entropy', 'intensity', 'thickness', 'spacing']):
            return 0.5
        elif any(keyword in feature_name for keyword in ['type', 'classification']):
            return 'unknown'
        elif any(keyword in feature_name for keyword in ['level', 'analysis_level']):
            return 'basic'
        else:
            return 0.0

    def _validate_critical_features(self, features: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate that critical features are present and have reasonable values
        """
        validation_result = {
            'critical_features_present': 0,
            'critical_features_missing': 0,
            'validation_errors': [],
            'warnings': []
        }
        
        # Critical features that must be present
        critical_features = [
            'ridge_density', 'ridge_count', 'minutiae_count', 
            'pattern_type', 'quality_score', 'confidence_score'
        ]
        
        for feature in critical_features:
            if feature in features:
                value = features[feature]
                
                # Validate value ranges
                if isinstance(value, (int, float)):
                    if feature in ['quality_score', 'confidence_score'] and (value < 0 or value > 1):
                        validation_result['warnings'].append(f"{feature} value {value} outside expected range [0,1]")
                    elif feature in ['ridge_count', 'minutiae_count'] and value < 0:
                        validation_result['warnings'].append(f"{feature} value {value} is negative")
                
                validation_result['critical_features_present'] += 1
            else:
                validation_result['critical_features_missing'] += 1
                validation_result['validation_errors'].append(f"Critical feature {feature} is missing")
        
        # Calculate validation score
        total_critical = len(critical_features)
        validation_result['validation_score'] = validation_result['critical_features_present'] / total_critical
        
        return validation_result

    def get_mapping_report(self) -> Dict[str, Any]:
        """
        Get a comprehensive report of the feature mapping system
        """
        return {
            'extension_name': self.extension_name,
            'extension_version': self.extension_version,
            'total_mappings': len(self.feature_mappings),
            'feature_categories': {
                'ridge_features': len([k for k in self.feature_mappings.keys() if 'ridge' in k]),
                'pattern_features': len([k for k in self.feature_mappings.keys() if 'pattern' in k]),
                'minutiae_features': len([k for k in self.feature_mappings.keys() if 'minutiae' in k]),
                'quality_features': len([k for k in self.feature_mappings.keys() if 'quality' in k or 'confidence' in k]),
                'statistical_features': len([k for k in self.feature_mappings.keys() if any(x in k for x in ['intensity', 'entropy', 'dimension'])]),
            },
            'priority_features': list(self.feature_priorities.keys()),
            'mapping_examples': {
                'ridge_density': self.feature_mappings['ridge_density'],
                'pattern_complexity': self.feature_mappings['pattern_complexity'],
                'minutiae_count': self.feature_mappings['minutiae_count'],
            }
        } 