#!/usr/bin/env python3
"""
🎯 Simple 3D PDF Generator - Real Data Only
===========================================

Super simple interface for generating stunning 3D PDF reports.
Works EXCLUSIVELY with real pipeline data - NO MOCK VALUES.

Author: DMIT Research Team
Version: 3.0 - Real Data Only
"""

import os
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional

from .real_data_processor import RealDataProcessor
from ..visual.real_chart_generator import Real3DChartGenerator
from ..core.pdf_builder import PDFBuilder

logger = logging.getLogger(__name__)

class Simple3DGenerator:
    """
    One-line 3D PDF generation using ONLY real pipeline data.
    """
    
    @classmethod
    def create_report(cls, 
                     pipeline_data: Dict[str, Any],
                     output_path: Optional[str] = None,
                     theme: str = "modern_3d",
                     include_3d_charts: bool = True,
                     style: str = "executive") -> str:
        """
        Generate a stunning 3D PDF report with one line of code!
        Uses ONLY real pipeline data - NO MOCK VALUES.
        
        Args:
            pipeline_data: Real DMIT pipeline data
            output_path: Output file path (optional)
            theme: Visual theme (modern_3d, executive_3d, scientific_3d)
            include_3d_charts: Include 3D charts
            style: Report style (executive, detailed, dashboard)
            
        Returns:
            Path to generated PDF file
        """
        
        try:
            print("🎨 Generating Advanced 3D PDF Report from REAL DATA...")
            
            # Validate that we have real pipeline data
            data_processor = RealDataProcessor()
            is_valid, errors = data_processor.validate_real_data(pipeline_data)
            
            if not is_valid:
                raise ValueError(f"Invalid pipeline data: {'; '.join(errors)}")
            
            print("✅ Real pipeline data validated successfully")
            
            # Auto-generate output path if not provided
            if output_path is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_dir = Path("output/3d_reports")
                output_dir.mkdir(parents=True, exist_ok=True)
                output_path = str(output_dir / f"dmit_3d_report_{timestamp}.pdf")
            
            # Step 1: Extract and process real data
            print("🔍 Processing real pipeline data...")
            real_data = data_processor.extract_real_intelligence_data(pipeline_data)
            
            # Step 2: Generate real insights (no mock values)
            print("🤖 Generating insights from real data...")
            real_insights = data_processor.generate_real_insights(real_data)
            real_careers = data_processor.generate_real_career_recommendations(real_data)
            real_development = data_processor.generate_real_development_plan(real_data)
            
            # Step 3: Generate 3D charts from real data
            if include_3d_charts:
                print("🎨 Creating stunning 3D charts from real data...")
                chart_generator = Real3DChartGenerator()
                charts = chart_generator.generate_all_3d_charts(real_data)
                real_data['charts'] = charts
            
            # Step 4: Prepare final report data (all real)
            report_data = {
                'report_metadata': {
                    'generation_timestamp': datetime.now().isoformat(),
                    'pipeline_version': real_data['pipeline_info'].get('pipeline_version', 'Unknown'),
                    'total_images_processed': real_data['pipeline_info'].get('total_images_processed', 0),
                    'report_type': 'Advanced 3D Report',
                    'data_source': 'Real Pipeline Analysis'
                },
                'intelligence_profile': real_data['intelligence_scores'],
                'brain_mapping': real_data['brain_mapping'],
                'learning_styles': real_data['learning_styles'],
                'personality_analysis': real_data['personality_behavior'],
                'extension_results': real_data['extension_results'],
                'quality_metrics': real_data['quality_metrics'],
                'real_insights': real_insights,
                'career_recommendations': real_careers,
                'development_plan': real_development,
                'charts': real_data.get('charts', {})
            }
            
            # Step 5: Build PDF
            print("📄 Building professional PDF from real data...")
            pdf_builder = PDFBuilder()
            pdf_path = pdf_builder.build_3d_pdf(report_data, output_path, theme)
            
            print(f"✅ Advanced 3D PDF generated from REAL DATA: {pdf_path}")
            return pdf_path
            
        except Exception as e:
            logger.error(f"Failed to generate 3D PDF from real data: {e}")
            raise
    
    @classmethod
    def create_executive_report(cls, pipeline_data: Dict[str, Any]) -> str:
        """Generate executive summary with 3D charts from real data"""
        return cls.create_report(pipeline_data, style="executive", include_3d_charts=True)
    
    @classmethod
    def create_detailed_report(cls, pipeline_data: Dict[str, Any]) -> str:
        """Generate detailed analysis with all 3D charts from real data"""
        return cls.create_report(pipeline_data, style="detailed", include_3d_charts=True)
    
    @classmethod
    def create_dashboard(cls, pipeline_data: Dict[str, Any]) -> str:
        """Generate dashboard-style report from real data"""
        return cls.create_report(pipeline_data, style="dashboard", include_3d_charts=True) 