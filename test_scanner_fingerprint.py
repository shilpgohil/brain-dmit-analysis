#!/usr/bin/env python3
"""Test scanner fingerprint feature extraction with pattern classification."""
import cv2
from optimized_feature_extractor_clean import OptimizedFeatureExtractor

# Test on scanned fingerprint
extractor = OptimizedFeatureExtractor()
img = cv2.imread('sample data/00000_00.bmp', cv2.IMREAD_GRAYSCALE)
print(f'Image shape: {img.shape}')

result = extractor.extract_optimized_features(img)
features = result['consolidated_features']

print(f'Total features: {len(features)}')
print(f'Quality score: {result["quality_metrics"]["image_quality"]:.3f}')
print(f'Quality level: {result["extraction_summary"]["quality_level"]}')

# Pattern classification features
print('\n📊 Pattern Classification:')
pattern_map = {0: 'Arch', 1: 'Loop', 2: 'Whorl', 3: 'Accidental', -1: 'Unknown'}
pattern_family = int(features.get('pattern_family', -1))
print(f'  Pattern Family: {pattern_map.get(pattern_family, "Unknown")} ({pattern_family})')
print(f'  Subtype Code: {features.get("pattern_subtype_code", -1):.0f}')
print(f'  Triradii Count: {features.get("triradii_count", 0):.0f}')
print(f'  Core Count: {features.get("core_count", 0):.0f}')
print(f'  Pattern Confidence: {features.get("pattern_confidence", 0):.2f}')

# Other key features
print('\n📊 Key Features:')
key_features = ['minutiae_count', 'ridge_density', 'tfrc', 'box_counting_dimension', 'entropy']
for f in key_features:
    if f in features:
        print(f'  {f}: {features[f]:.3f}')
print('\nKey Features:')
for f in key_features:
    if f in features:
        print(f'  {f}: {features[f]:.3f}')

# Show all features
print(f'\nAll {len(features)} features:')
for name, value in sorted(features.items()):
    print(f'  {name}: {value:.4f}')
