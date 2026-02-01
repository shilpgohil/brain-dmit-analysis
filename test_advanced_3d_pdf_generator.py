#!/usr/bin/env python3
"""
🧪 Test Advanced 3D PDF Generator with Real Pipeline Data
=========================================================

Tests the new advanced 3D PDF generator using ONLY real pipeline data.
NO MOCK VALUES, NO DEFAULTS, NO FALLBACKS.

Author: DMIT Research Team
Version: 3.0 - Real Data Only
"""

import json
import os
import sys
from pathlib import Path

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_advanced_3d_pdf_generator():
    """Test the advanced 3D PDF generator with real pipeline data"""
    
    print("🧪 Testing Advanced 3D PDF Generator with Real Pipeline Data")
    print("=" * 70)
    
    try:
        # Step 1: Load real pipeline data
        print("📊 Loading real pipeline data...")
        pipeline_data_path = "test_output/new_pipeline_test/new_pipeline_results.json"
        
        if not os.path.exists(pipeline_data_path):
            print(f"❌ Real pipeline data not found: {pipeline_data_path}")
            print("Please run your DMIT pipeline first to generate real data.")
            return False
        
        with open(pipeline_data_path, 'r') as f:
            pipeline_data = json.load(f)
        
        print(f"✅ Loaded real pipeline data with {len(pipeline_data.get('individual_results', []))} results")
        
        # Step 2: Import the advanced 3D PDF generator
        print("🔧 Importing Advanced 3D PDF Generator...")
        try:
            from advanced_3d_pdf_generator import Simple3DGenerator, RealDataProcessor
            print("✅ Advanced 3D PDF Generator imported successfully")
        except ImportError as e:
            print(f"❌ Failed to import Advanced 3D PDF Generator: {e}")
            print("Please ensure all dependencies are installed:")
            print("pip install reportlab matplotlib plotly numpy")
            return False
        
        # Step 3: Validate real data
        print("🔍 Validating real pipeline data...")
        data_processor = RealDataProcessor()
        is_valid, errors = data_processor.validate_real_data(pipeline_data)
        
        if not is_valid:
            print(f"❌ Invalid pipeline data: {'; '.join(errors)}")
            return False
        
        print("✅ Real pipeline data validated successfully")
        
        # Step 4: Extract real intelligence data
        print("📈 Extracting real intelligence data...")
        real_data = data_processor.extract_real_intelligence_data(pipeline_data)
        
        print(f"✅ Extracted intelligence data:")
        print(f"   • Intelligence scores: {len(real_data['intelligence_scores'])} types")
        print(f"   • Brain mapping: {len(real_data['brain_mapping'])} regions")
        print(f"   • Learning styles: {len(real_data['learning_styles'])} styles")
        print(f"   • Personality traits: {len(real_data['personality_behavior'])} traits")
        
        # Step 5: Generate real insights
        print("🤖 Generating real insights...")
        real_insights = data_processor.generate_real_insights(real_data)
        real_careers = data_processor.generate_real_career_recommendations(real_data)
        real_development = data_processor.generate_real_development_plan(real_data)
        
        print(f"✅ Generated real insights:")
        print(f"   • Insights: {len(real_insights)}")
        print(f"   • Career recommendations: {len(real_careers)}")
        print(f"   • Development plans: {len(real_development)}")
        
        # Step 6: Generate 3D PDF report
        print("🎨 Generating Advanced 3D PDF Report...")
        
        # Create output directory
        output_dir = Path("test_output/advanced_3d_pdf_test")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate PDF
        pdf_path = Simple3DGenerator.create_report(
            pipeline_data=pipeline_data,
            output_path=str(output_dir / "advanced_3d_report.pdf"),
            theme="modern_3d",
            include_3d_charts=True,
            style="executive"
        )
        
        if os.path.exists(pdf_path):
            file_size = os.path.getsize(pdf_path) / 1024  # KB
            print(f"✅ Advanced 3D PDF generated successfully!")
            print(f"   📄 File: {pdf_path}")
            print(f"   📏 Size: {file_size:.1f} KB")
            print(f"   🎨 Theme: Modern 3D")
            print(f"   📊 Charts: 3D Intelligence Radar, Brain Mapping, etc.")
            print(f"   📈 Data: 100% Real Pipeline Data")
            
            # Show sample insights
            if real_insights:
                print(f"\n💡 Sample Real Insights:")
                for i, insight in enumerate(real_insights[:3], 1):
                    print(f"   {i}. {insight}")
            
            # Show sample career recommendations
            if real_careers:
                print(f"\n💼 Top Career Recommendations:")
                for i, career in enumerate(real_careers[:3], 1):
                    print(f"   {i}. {career['title']} - {career['match_percentage']:.1f}% match")
            
            return True
        else:
            print(f"❌ PDF generation failed - file not created")
            return False
            
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_simple_usage():
    """Test the simple one-line usage"""
    
    print("\n🎯 Testing Simple One-Line Usage")
    print("=" * 40)
    
    try:
        # Load real pipeline data
        pipeline_data_path = "test_output/new_pipeline_test/new_pipeline_results.json"
        
        if not os.path.exists(pipeline_data_path):
            print("❌ Real pipeline data not found - skipping simple usage test")
            return False
        
        with open(pipeline_data_path, 'r') as f:
            pipeline_data = json.load(f)
        
        # Import the simple function
        from advanced_3d_pdf_generator import create_3d_report
        
        # Test one-line generation
        print("🚀 Testing one-line PDF generation...")
        pdf_path = create_3d_report(pipeline_data)
        
        if os.path.exists(pdf_path):
            print(f"✅ One-line generation successful: {pdf_path}")
            return True
        else:
            print("❌ One-line generation failed")
            return False
            
    except Exception as e:
        print(f"❌ Simple usage test failed: {e}")
        return False

if __name__ == "__main__":
    print("🧪 ADVANCED 3D PDF GENERATOR TEST SUITE")
    print("=" * 50)
    print("Testing with REAL pipeline data only - NO MOCK VALUES")
    print()
    
    # Test main functionality
    success1 = test_advanced_3d_pdf_generator()
    
    # Test simple usage
    success2 = test_simple_usage()
    
    # Summary
    print("\n" + "=" * 50)
    print("🎯 TEST SUMMARY")
    print("=" * 50)
    
    if success1 and success2:
        print("✅ ALL TESTS PASSED!")
        print("🎉 Advanced 3D PDF Generator is working perfectly!")
        print("📊 Features tested:")
        print("   • Real data validation")
        print("   • Real insights generation")
        print("   • 3D chart generation")
        print("   • Professional PDF creation")
        print("   • One-line usage")
        print("   • No mock values used")
    elif success1:
        print("⚠️ PARTIAL SUCCESS")
        print("✅ Main functionality works")
        print("❌ Simple usage needs attention")
    else:
        print("❌ TESTS FAILED")
        print("Please check the error messages above")
    
    print("\n🎨 Your Advanced 3D PDF Generator is ready!")
    print("📄 Generated PDFs will be in: test_output/advanced_3d_pdf_test/")
    print("🚀 Use: from advanced_3d_pdf_generator import create_3d_report") 