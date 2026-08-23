#!/usr/bin/env python3
"""
Simple 3D PDF Generator - Real Data Only
Version: 4.0 - Full data pipeline with all extensions
"""

import logging
import sys
import os
from datetime import datetime
from typing import Dict, Any, Optional
from pathlib import Path

_original_print = print
def safe_print(*args, **kwargs):
    try:
        _original_print(*args, **kwargs)
    except UnicodeEncodeError:
        safe_args = [str(a).encode('ascii', 'ignore').decode('ascii') for a in args]
        _original_print(*safe_args, **kwargs)
print = safe_print

from .real_data_processor import RealDataProcessor
from ..visual.real_chart_generator import Real3DChartGenerator
from ..core.pdf_builder import PDFBuilder

logger = logging.getLogger(__name__)


class Simple3DGenerator:
    """One-line 3D PDF generation using ONLY real pipeline data."""

    @classmethod
    def create_report(cls,
                      pipeline_data: Dict[str, Any],
                      output_path: Optional[str] = None,
                      theme: str = "modern_3d",
                      include_3d_charts: bool = True,
                      style: str = "executive") -> str:

        try:
            print("Generating Advanced DMIT PDF Report from REAL DATA...")

            data_processor = RealDataProcessor()
            is_valid, errors = data_processor.validate_real_data(pipeline_data)
            if not is_valid:
                raise ValueError(f"Invalid pipeline data: {'; '.join(errors)}")

            print("Real pipeline data validated successfully")

            if output_path is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_dir = Path("output/scientific_reports")
                output_dir.mkdir(parents=True, exist_ok=True)
                output_path = str(output_dir / f"dmit_scientific_{timestamp}.pdf")

            # -----------------------------------------------------------------
            # Step 1: Extract ALL real data (aggregated profile + per-finger)
            # -----------------------------------------------------------------
            print("Processing real pipeline data...")
            real_data = data_processor.extract_real_intelligence_data(pipeline_data)

            # -----------------------------------------------------------------
            # Step 2: Generate narrative content
            # -----------------------------------------------------------------
            print("Generating insights from real data...")
            real_insights = data_processor.generate_real_insights(real_data)
            real_careers = data_processor.generate_real_career_recommendations(real_data)
            real_development = data_processor.generate_real_development_plan(real_data)

            # -----------------------------------------------------------------
            # Step 3: Generate all charts
            # -----------------------------------------------------------------
            charts = {}
            if include_3d_charts:
                print("Creating charts from real data...")
                chart_gen = Real3DChartGenerator()
                charts = chart_gen.generate_all_3d_charts(real_data)
                real_data['charts'] = charts
                print(f"Generated {len(charts)} charts")

            # -----------------------------------------------------------------
            # Step 4: Assemble final report_data dict (everything goes in here)
            # -----------------------------------------------------------------
            pipeline_info = real_data['pipeline_info']
            report_data = {
                # Metadata
                'report_metadata': {
                    'generation_timestamp': datetime.now().isoformat(),
                    'pipeline_version': pipeline_info.get('pipeline_version', 'Unknown'),
                    'total_images_processed': pipeline_info.get(
                        'total_images_processed',
                        pipeline_info.get('total_fingers_analyzed', 0)
                    ),
                    'report_type': 'Advanced DMIT Scientific Report',
                    'data_source': 'Real Pipeline Analysis',
                },
                # Core profiles
                'intelligence_profile': real_data['intelligence_scores'],
                'brain_mapping': real_data['brain_mapping'],
                'learning_styles': real_data['learning_styles'],
                'personality_analysis': real_data['personality_behavior'],
                # Extension results (39 extensions)
                'extension_results': real_data['extension_results'],
                # Per-finger data
                'per_finger_data': real_data['per_finger_data'],
                # Quality metrics
                'quality_metrics': real_data['quality_metrics'],
                # Narrative
                'real_insights': real_insights,
                'career_recommendations': real_careers,
                'development_plan': real_development,
                # Charts
                'charts': charts,
            }

            # -----------------------------------------------------------------
            # Step 5: Build PDF
            # -----------------------------------------------------------------
            print("Building professional PDF from real data...")
            pdf_builder = PDFBuilder()
            pdf_path = pdf_builder.build_3d_pdf(report_data, output_path, theme)

            print(f"Advanced DMIT PDF generated: {pdf_path}")
            return pdf_path

        except Exception as e:
            logger.exception(f"Failed to generate PDF: {e}")
            raise

    @classmethod
    def create_executive_report(cls, pipeline_data: Dict[str, Any]) -> str:
        return cls.create_report(pipeline_data, style="executive", include_3d_charts=True)

    @classmethod
    def create_detailed_report(cls, pipeline_data: Dict[str, Any]) -> str:
        return cls.create_report(pipeline_data, style="detailed", include_3d_charts=True)

    @classmethod
    def create_dashboard(cls, pipeline_data: Dict[str, Any]) -> str:
        return cls.create_report(pipeline_data, style="dashboard", include_3d_charts=True)