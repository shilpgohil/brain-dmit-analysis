#!/usr/bin/env python3
"""
🎨 Advanced 3D PDF Generator for DMIT Analysis
==============================================

A modern, dependency-free PDF generator with stunning 3D visualizations,
working EXCLUSIVELY with real pipeline data - NO MOCK VALUES.

Features:
- 3D charts and visualizations using real data
- AI-powered insights from real analysis
- Professional styling
- One-line PDF generation
- Zero system dependencies

Author: DMIT Research Team
Version: 3.0 - Real Data Only
"""

from .core.simple_generator import Simple3DGenerator
from .core.advanced_generator import Advanced3DGenerator
from .core.real_data_processor import RealDataProcessor
from .visual.real_chart_generator import Real3DChartGenerator

__version__ = "3.0.0"
__author__ = "DMIT Research Team"

__all__ = [
    'Simple3DGenerator',
    'Advanced3DGenerator', 
    'RealDataProcessor',
    'Real3DChartGenerator'
]

# Quick access functions
def create_3d_report(pipeline_data, **kwargs):
    """One-line 3D PDF generation using real pipeline data"""
    return Simple3DGenerator.create_report(pipeline_data, **kwargs)

def generate_advanced_3d_report(pipeline_data, **kwargs):
    """Advanced 3D PDF generation with full customization"""
    generator = Advanced3DGenerator()
    return generator.generate_3d_report(pipeline_data, **kwargs)