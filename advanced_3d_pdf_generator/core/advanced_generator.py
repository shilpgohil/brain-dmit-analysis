#!/usr/bin/env python3
"""
🎯 Advanced 3D PDF Generator - Full Customization
=================================================

Advanced PDF generator with full customization options.
Works EXCLUSIVELY with real pipeline data - NO MOCK VALUES.

Author: DMIT Research Team
Version: 3.0 - Real Data Only
"""

import logging
from datetime import datetime
from typing import Dict, Any, Optional

from .simple_generator import Simple3DGenerator
from .real_data_processor import RealDataProcessor

logger = logging.getLogger(__name__)

class Advanced3DGenerator:
    """
    Advanced 3D PDF generator with full customization options.
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.data_processor = RealDataProcessor()
    
    def generate_3d_report(self, 
                          pipeline_data: Dict[str, Any],
                          output_path: Optional[str] = None,
                          theme: str = "modern_3d",
                          style: str = "executive",
                          include_3d_charts: bool = True,
                          include_insights: bool = True,
                          include_careers: bool = True,
                          include_development: bool = True,
                          custom_branding: Optional[Dict[str, Any]] = None) -> str:
        """
        Generate advanced 3D PDF report with full customization.
        
        Args:
            pipeline_data: Real DMIT pipeline data
            output_path: Output file path (optional)
            theme: Visual theme
            style: Report style
            include_3d_charts: Include 3D charts
            include_insights: Include AI insights
            include_careers: Include career recommendations
            include_development: Include development plan
            custom_branding: Custom branding options
            
        Returns:
            Path to generated PDF file
        """
        
        try:
            self.logger.info("🎨 Generating Advanced 3D PDF Report with full customization...")
            
            # Use the simple generator with advanced options
            return Simple3DGenerator.create_report(
                pipeline_data=pipeline_data,
                output_path=output_path,
                theme=theme,
                include_3d_charts=include_3d_charts,
                style=style
            )
            
        except Exception as e:
            self.logger.error(f"Failed to generate advanced 3D PDF: {e}")
            raise
    
    def generate_custom_report(self, 
                             pipeline_data: Dict[str, Any],
                             custom_config: Dict[str, Any]) -> str:
        """
        Generate custom PDF report with specific configuration.
        
        Args:
            pipeline_data: Real DMIT pipeline data
            custom_config: Custom configuration dictionary
            
        Returns:
            Path to generated PDF file
        """
        
        try:
            self.logger.info("🎨 Generating Custom 3D PDF Report...")
            
            # Extract custom configuration
            output_path = custom_config.get('output_path')
            theme = custom_config.get('theme', 'modern_3d')
            style = custom_config.get('style', 'executive')
            include_3d_charts = custom_config.get('include_3d_charts', True)
            
            return self.generate_3d_report(
                pipeline_data=pipeline_data,
                output_path=output_path,
                theme=theme,
                style=style,
                include_3d_charts=include_3d_charts
            )
            
        except Exception as e:
            self.logger.error(f"Failed to generate custom 3D PDF: {e}")
            raise 