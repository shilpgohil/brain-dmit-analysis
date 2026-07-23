#!/usr/bin/env python3
"""
Test Complete DMIT Pipeline on Real Fingerprints
"""

import sys
from pathlib import Path
from integrated_dmit_pipeline import IntegratedDMITPipeline

def main():
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass
    print("=" * 70)
    print("🚀 COMPLETE DMIT PIPELINE TEST")
    print("=" * 70)
    
    # Initialize pipeline
    pipeline = IntegratedDMITPipeline()
    
    # Get finger_prints images
    finger_dir = Path("finger_prints")
    if not finger_dir.exists():
        print(f"❌ Directory not found: {finger_dir}")
        return
    
    # Get all BMP files
    images = sorted(finger_dir.glob("*.bmp"))
    if not images:
        print(f"❌ No BMP files found in {finger_dir}")
        return
    
    print(f"\n📸 Found {len(images)} fingerprint images:")
    for img in images:
        print(f"   - {img.name}")
    
    # Run complete pipeline
    print(f"\n{'=' * 70}")
    print("🔬 RUNNING ANALYSIS...")
    print("=" * 70)
    
    try:
        results = pipeline.run_complete_pipeline(
            [str(p) for p in images],
            generate_pdf=True
        )
        
        print(f"\n{'=' * 70}")
        print("✅ ANALYSIS COMPLETE!")
        print("=" * 70)
        
        # Print summary
        agg = results.get('aggregated_analysis', {})
        dmit = agg.get('dmit_profile', {})
        
        def show(label, scores):
            print(f"\n{label}")
            for key, score in scores.items():
                name = key.replace('_', ' ').title()
                if isinstance(score, (int, float)):
                    print(f"   {name}: {score:.2f}")
                else:
                    print(f"   {name}: N/A" if score is None else f"   {name}: {score}")

        show("📊 INTELLIGENCE PROFILE:", dmit.get('multiple_intelligences', {}))
        
        brain = {k: v for k, v in dmit.get('brain_mapping', {}).items() if k != 'lobe_hemispheres'}
        show("🧠 BRAIN MAPPING:", brain)
        show("📚 LEARNING STYLES:", dmit.get('learning_styles', {}))
        show("🎭 PERSONALITY:", dmit.get('personality_behavior', {}))
        
        print(f"\n{'=' * 70}")
        print("📄 Check output/scientific_reports/ for PDF report")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
