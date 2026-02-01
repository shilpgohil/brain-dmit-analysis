#!/usr/bin/env python3
"""
🧪 Test Preprocessing Pipeline
==============================
Tests the finger-to-fingerprint preprocessing with sample images.
"""

import os
import sys
import cv2
import numpy as np
from pathlib import Path
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from preprocessing_images import FingerToFingerprintPipeline

def test_preprocessing():
    """Test preprocessing pipeline with finger images."""
    
    print("=" * 70)
    print("🧪 FINGER-TO-FINGERPRINT PREPROCESSING TEST")
    print("=" * 70)
    
    # Find finger images
    fingers_dir = Path("fingers")
    if not fingers_dir.exists():
        print(f"❌ Fingers directory not found: {fingers_dir}")
        return
    
    # Get all image files
    image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif']
    image_files = []
    for ext in image_extensions:
        image_files.extend(fingers_dir.glob(f"*{ext}"))
        image_files.extend(fingers_dir.glob(f"*{ext.upper()}"))
    
    if not image_files:
        print(f"❌ No images found in {fingers_dir}")
        return
    
    print(f"📸 Found {len(image_files)} images")
    
    # Create output directory
    output_dir = Path("test_output/preprocessing_results")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Initialize pipeline
    pipeline = FingerToFingerprintPipeline()
    
    results = []
    
    for i, image_path in enumerate(image_files, 1):
        print(f"\n{'─' * 60}")
        print(f"📷 [{i}/{len(image_files)}] Processing: {image_path.name}")
        
        # Process image
        result = pipeline.process(str(image_path))
        
        # Save results
        if result['success'] and result['fingerprint'] is not None:
            # Save processed fingerprint
            output_filename = f"{image_path.stem}_fingerprint.png"
            output_path = output_dir / output_filename
            cv2.imwrite(str(output_path), result['fingerprint'])
            
            # Also create a comparison image (side by side)
            original = cv2.imread(str(image_path))
            if original is not None:
                # Resize for comparison
                target_height = 400
                
                # Resize original
                orig_ratio = target_height / original.shape[0]
                orig_resized = cv2.resize(original, None, fx=orig_ratio, fy=orig_ratio)
                
                # Resize fingerprint
                fp = result['fingerprint']
                fp_ratio = target_height / fp.shape[0]
                fp_resized = cv2.resize(fp, None, fx=fp_ratio, fy=fp_ratio)
                
                # Convert fingerprint to BGR for comparison
                if len(fp_resized.shape) == 2:
                    fp_resized = cv2.cvtColor(fp_resized, cv2.COLOR_GRAY2BGR)
                
                # Create comparison image
                comparison = np.hstack([orig_resized, fp_resized])
                
                # Add labels
                cv2.putText(comparison, "Original", (10, 30), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                cv2.putText(comparison, "Processed", (orig_resized.shape[1] + 10, 30),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                
                comparison_path = output_dir / f"{image_path.stem}_comparison.png"
                cv2.imwrite(str(comparison_path), comparison)
            
            print(f"   ✅ Success! Confidence: {result['confidence']:.1%}")
            print(f"   📁 Saved: {output_path}")
            
            results.append({
                'file': image_path.name,
                'success': True,
                'confidence': result['confidence'],
                'stages': result['stages_completed'],
                'output': str(output_path)
            })
        else:
            print(f"   ❌ Failed: {result.get('metadata', {}).get('error', 'Unknown error')}")
            results.append({
                'file': image_path.name,
                'success': False,
                'confidence': result['confidence'],
                'stages': result['stages_completed']
            })
        
        # Print stage details
        if 'metadata' in result:
            meta = result['metadata']
            print(f"   📊 Stages completed: {', '.join(result['stages_completed'])}")
            
            if 'stage1_segmentation' in meta:
                seg = meta['stage1_segmentation']
                print(f"   └─ Segmentation: confidence={seg.get('confidence', 0):.2f}")
            
            if 'stage2_validation' in meta:
                val = meta['stage2_validation']
                print(f"   └─ Validation: valid={val.get('is_valid', False)}")
            
            if 'stage3_roi_detection' in meta:
                roi = meta['stage3_roi_detection']
                print(f"   └─ ROI: {roi.get('roi_shape', 'N/A')}")
            
            if 'stage5_ridge_enhancement' in meta:
                enh = meta['stage5_ridge_enhancement']
                print(f"   └─ Enhancement: clarity={enh.get('ridge_clarity', 0):.2f}")
    
    # Summary
    print(f"\n{'=' * 70}")
    print("📊 SUMMARY")
    print("=" * 70)
    
    successful = sum(1 for r in results if r['success'])
    print(f"✅ Successful: {successful}/{len(results)}")
    print(f"📁 Output directory: {output_dir}")
    
    if successful > 0:
        avg_confidence = np.mean([r['confidence'] for r in results if r['success']])
        print(f"📈 Average confidence: {avg_confidence:.1%}")
    
    print(f"\n💡 View results in: {output_dir.absolute()}")
    
    return results


if __name__ == "__main__":
    test_preprocessing()
