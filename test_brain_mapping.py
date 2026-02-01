
import sys
import logging
from typing import Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

from dmit_intelligence_mapper import map_features_to_dmit_profile

def test_brain_mapping_logic():
    print("Testing Brain-Finger Mapping Logic...")
    
    # Mock Features (Generic high quality)
    features = {
        'whorl_logical_layering_score': 0.8,
        'box_counting_dimension': 1.8,
        'ridge_density': 0.5,
        'tfrc': 20,
        'fourier_energy_total': 1000,
        'pattern_symmetry_score': 0.7,
        'minutiae_count': 50,
        'extraction_confidence': 0.9,
        # Required for completeness check
        'entropy': 4.0, 'minutiae_density': 0.2, 'overall_quality_score': 0.8,
        'betti_0': 10, 'betti_1': 5, 'euler_characteristic': 5,
        'graph_density': 0.1, 'average_clustering': 0.1, 'pore_density': 0.1,
        'incipient_ridge_count': 0, 'fourier_harmonic_ratio': 0.1,
        'feature_stability': 0.8, 'correlation_dimension': 1.5,
        'scale_consistency': 0.8, 'persistence_entropy': 0.5, 'topological_complexity': 0.6
    }
    
    # 1. Test Neutral (No Finger)
    print("\n--- Test 1: Neutral (No Finger Type) ---")
    profile_neutral = map_features_to_dmit_profile(features)
    brain_neutral = profile_neutral.get('brain_mapping', {})
    print(f"Frontal: {brain_neutral.get('frontal_lobe', 0):.3f}")
    print(f"Parietal: {brain_neutral.get('parietal_lobe', 0):.3f}")
    
    # 2. Test Thumb (Should boost Frontal)
    print("\n--- Test 2: Thumb (Expect Frontal Boost) ---")
    profile_thumb = map_features_to_dmit_profile(features, finger_type='thumb')
    brain_thumb = profile_thumb.get('brain_mapping', {})
    print(f"Frontal: {brain_thumb.get('frontal_lobe', 0):.3f} (vs {brain_neutral.get('frontal_lobe', 0):.3f})")
    
    if brain_thumb.get('frontal_lobe') > brain_neutral.get('frontal_lobe'):
        print("✅ PASS: Frontal score boosted for Thumb")
    else:
        print("❌ FAIL: Frontal score NOT boosted for Thumb")

    # 3. Test Middle (Should boost Parietal)
    print("\n--- Test 3: Middle (Expect Parietal Boost) ---")
    profile_middle = map_features_to_dmit_profile(features, finger_type='middle')
    brain_middle = profile_middle.get('brain_mapping', {})
    print(f"Parietal: {brain_middle.get('parietal_lobe', 0):.3f} (vs {brain_neutral.get('parietal_lobe', 0):.3f})")
    
    if brain_middle.get('parietal_lobe') > brain_neutral.get('parietal_lobe'):
        print("✅ PASS: Parietal score boosted for Middle")
    else:
        print("❌ FAIL: Parietal score NOT boosted for Middle")

    # 4. Test Little (Should boost Occipital)
    print("\n--- Test 4: Little (Expect Occipital Boost) ---")
    profile_little = map_features_to_dmit_profile(features, finger_type='little')
    brain_little = profile_little.get('brain_mapping', {})
    print(f"Occipital: {brain_little.get('occipital_lobe', 0):.3f} (vs {brain_neutral.get('occipital_lobe', 0):.3f})")

    if brain_little.get('occipital_lobe', 0) > brain_neutral.get('occipital_lobe', 0):
         print("✅ PASS: Occipital score boosted for Little")
    else:
         print("❌ FAIL: Occipital score NOT boosted for Little")

if __name__ == "__main__":
    test_brain_mapping_logic()
