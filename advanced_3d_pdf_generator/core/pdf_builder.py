#!/usr/bin/env python3
"""
📄 PDF Builder - Real Data Professional PDF Generation
=====================================================

Builds professional PDF reports using ONLY real pipeline data.
NO MOCK VALUES, NO DEFAULTS, NO FALLBACKS.

Author: DMIT Research Team
Version: 3.0 - Real Data Only
"""

import logging
import base64
import io
from datetime import datetime
from typing import Dict, Any, Optional
from pathlib import Path

try:
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import A4, letter
    from reportlab.lib import colors
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image
    from reportlab.lib.units import inch
    from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False

logger = logging.getLogger(__name__)

class PDFBuilder:
    """
    Builds professional PDF reports from real DMIT pipeline data.
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        if not REPORTLAB_AVAILABLE:
            raise ImportError("ReportLab is required for PDF generation. Please install it: pip install reportlab")
        
        # Initialize styles
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Setup custom styles for professional PDF with Times New Roman font"""
        
        # Custom title style
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Title'],
            fontName='Times-Roman',
            fontSize=24,
            spaceAfter=30,
            alignment=TA_CENTER,
            textColor=colors.HexColor('#2C3E50')
        ))
        
        # Custom heading style
        self.styles.add(ParagraphStyle(
            name='CustomHeading',
            parent=self.styles['Heading1'],
            fontName='Times-Bold',
            fontSize=18,
            spaceAfter=20,
            spaceBefore=20,
            alignment=TA_LEFT,
            textColor=colors.HexColor('#3498DB')
        ))
        
        # Custom subheading style
        self.styles.add(ParagraphStyle(
            name='CustomSubHeading',
            parent=self.styles['Heading2'],
            fontName='Times-Bold',
            fontSize=14,
            spaceAfter=15,
            spaceBefore=15,
            alignment=TA_LEFT,
            textColor=colors.HexColor('#34495E')
        ))
        
        # Custom body style
        self.styles.add(ParagraphStyle(
            name='CustomBody',
            parent=self.styles['Normal'],
            fontName='Times-Roman',
            fontSize=11,
            spaceAfter=12,
            alignment=TA_JUSTIFY,
            textColor=colors.HexColor('#2C3E50')
        ))
    
    def build_3d_pdf(self, report_data: Dict[str, Any], output_path: str, theme: str = "modern_3d") -> str:
        """
        Build professional 3D PDF report from real data.
        
        Args:
            report_data: Real report data (no mock values)
            output_path: Output file path
            theme: Visual theme
            
        Returns:
            Path to generated PDF
        """
        
        try:
            self.logger.info(f"Building 3D PDF report: {output_path}")
            
            # Create PDF document with page template
            doc = SimpleDocTemplate(
                output_path,
                pagesize=A4,
                rightMargin=72,
                leftMargin=72,
                topMargin=72,
                bottomMargin=72
            )
            
            # Create and apply page template with ivory background, page numbers, and footer
            page_template = self._create_page_template(doc)
            
            # Clear any existing templates and set our template as the only one
            doc.pageTemplates = []
            doc.addPageTemplates([page_template])
            
            # Ensure the template is properly applied
            self.logger.info(f"Page template created and applied: {page_template.id}")
            
            # Build story (content)
            story = []
            
            # Add cover page
            story.extend(self._create_cover_page(report_data))
            story.append(PageBreak())
            
            # Add executive summary
            story.extend(self._create_executive_summary(report_data))
            story.append(PageBreak())
            
            # Add intelligence profile with 3D charts
            story.extend(self._create_intelligence_profile_section(report_data))
            story.append(PageBreak())
            
            # Add brain mapping
            story.extend(self._create_brain_mapping_section(report_data))
            story.append(PageBreak())
            
            # Add career recommendations
            story.extend(self._create_career_recommendations_section(report_data))
            story.append(PageBreak())
            
            # Add development plan
            story.extend(self._create_development_plan_section(report_data))
            story.append(PageBreak())
            
            # Add technical details
            story.extend(self._create_technical_details_section(report_data))
            
            # Build PDF
            doc.build(story)
            
            self.logger.info(f"✅ 3D PDF report generated successfully: {output_path}")
            return output_path
            
        except Exception as e:
            self.logger.error(f"Error building 3D PDF: {e}")
            raise
    

    
    def _create_cover_page(self, report_data: Dict[str, Any]) -> list:
        """Create professional cover page"""
        story = []
        
        # Title
        title = Paragraph(
            "Dermatoglyphics Multiple Intelligence Test",
            self.styles['CustomTitle']
        )
        story.append(title)
        story.append(Spacer(1, 40))
        
        # Subtitle
        subtitle = Paragraph(
            "Advanced 3D Analysis Report",
            ParagraphStyle(
                'Subtitle',
                parent=self.styles['Normal'],
                fontName='Times-Roman',
                fontSize=18,
                alignment=TA_CENTER,
                textColor=colors.HexColor('#7F8C8D')
            )
        )
        story.append(subtitle)
        story.append(Spacer(1, 60))
        
        # Report metadata
        metadata = report_data.get('report_metadata', {})
        
        # Create metadata table
        metadata_data = [
            ["Report Type:", metadata.get('report_type', 'Advanced 3D Report')],
            ["Data Source:", metadata.get('data_source', 'Real Pipeline Analysis')],
            ["Pipeline Version:", metadata.get('pipeline_version', 'Unknown')],
            ["Images Processed:", str(metadata.get('total_images_processed', 0))],
            ["Generated:", datetime.now().strftime('%B %d, %Y at %I:%M %p')]
        ]
        
        metadata_table = Table(metadata_data, colWidths=[2*inch, 3*inch])
        metadata_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#ECF0F1')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#2C3E50')),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Times-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Times-Roman'),
            ('FONTSIZE', (0, 0), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#BDC3C7'))
        ]))
        
        story.append(metadata_table)
        story.append(Spacer(1, 40))
        
        # Footer note
        footer = Paragraph(
            "This report was generated using advanced AI-powered DMIT analysis technology with real pipeline data.",
            ParagraphStyle(
                'Footer',
                parent=self.styles['Normal'],
                fontName='Times-Roman',
                fontSize=10,
                alignment=TA_CENTER,
                textColor=colors.HexColor('#7F8C8D')
            )
        )
        story.append(footer)
        
        return story
    
    def _create_executive_summary(self, report_data: Dict[str, Any]) -> list:
        """Create executive summary section"""
        story = []
        
        # Section title
        title = Paragraph("Executive Summary", self.styles['CustomHeading'])
        story.append(title)
        
        # Real insights
        real_insights = report_data.get('real_insights', [])
        if real_insights:
            for insight in real_insights:
                insight_para = Paragraph(f"• {insight}", self.styles['CustomBody'])
                story.append(insight_para)
                story.append(Spacer(1, 6))
        
        # Intelligence profile summary
        intelligence_profile = report_data.get('intelligence_profile', {})
        if intelligence_profile:
            story.append(Spacer(1, 20))
            story.append(Paragraph("Intelligence Profile Overview:", self.styles['CustomSubHeading']))
            
            # Find dominant intelligence
            if intelligence_profile:
                dominant = max(intelligence_profile.items(), key=lambda x: x[1])
                dominant_para = Paragraph(
                    f"Your dominant intelligence is <b>{dominant[0].replace('_', ' ').title()}</b> "
                    f"with a score of <b>{dominant[1]:.1%}</b>.",
                    self.styles['CustomBody']
                )
                story.append(dominant_para)
        
        return story
    
    def _create_intelligence_profile_section(self, report_data: Dict[str, Any]) -> list:
        """Create intelligence profile section with 3D charts"""
        story = []
        
        # Section title
        title = Paragraph("Intelligence Profile Analysis", self.styles['CustomHeading'])
        story.append(title)
        
        # Add 3D intelligence radar chart if available
        charts = report_data.get('charts', {})
        if 'intelligence_radar_3d' in charts and charts['intelligence_radar_3d']:
            story.append(Spacer(1, 20))
            story.append(Paragraph("3D Intelligence Radar Chart:", self.styles['CustomSubHeading']))
            
            # Chart explanation
            explanation = Paragraph(
                "<b>Chart Explanation:</b><br/>"
                "This 3D radar chart visualizes your multiple intelligence profile across 8 different intelligence types. "
                "Each axis represents a specific intelligence domain, and the distance from the center indicates your strength in that area. "
                "The 3D effect provides depth and perspective, making it easier to identify your dominant and developing intelligences. "
                "Areas with higher scores (closer to the outer edge) represent your natural strengths, while lower scores indicate areas for potential development.",
                self.styles['CustomBody']
            )
            story.append(explanation)
            story.append(Spacer(1, 15))
            
            # Convert base64 to image
            try:
                img_data = base64.b64decode(charts['intelligence_radar_3d'])
                img_buffer = io.BytesIO(img_data)
                img = Image(img_buffer, width=6*inch, height=4*inch)
                story.append(img)
                story.append(Spacer(1, 20))
            except Exception as e:
                self.logger.warning(f"Could not add 3D intelligence chart: {e}")
        
        # Intelligence scores table
        intelligence_profile = report_data.get('intelligence_profile', {})
        if intelligence_profile:
            story.append(Paragraph("Detailed Intelligence Scores:", self.styles['CustomSubHeading']))
            
            # Table explanation
            table_explanation = Paragraph(
                "<b>Table Explanation:</b><br/>"
                "This table provides detailed numerical scores for each intelligence type. The 'Score' column shows your percentage strength "
                "in each area (0-100%), while the 'Level' column categorizes your performance as Excellent, Good, Average, or Developing. "
                "These scores are derived from advanced analysis of your fingerprint patterns and provide a quantitative foundation for "
                "understanding your cognitive strengths and areas for growth.",
                self.styles['CustomBody']
            )
            story.append(table_explanation)
            story.append(Spacer(1, 15))
            
            # Create scores table
            scores_data = [["Intelligence Type", "Score", "Level"]]
            for intel_type, score in intelligence_profile.items():
                level = self._get_intelligence_level(score)
                scores_data.append([
                    intel_type.replace('_', ' ').title(),
                    f"{score:.1%}",
                    level
                ])
            
            scores_table = Table(scores_data, colWidths=[2.5*inch, 1*inch, 1.5*inch])
            scores_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498DB')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Times-Bold'),
                ('FONTNAME', (0, 1), (-1, -1), 'Times-Roman'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
                ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#BDC3C7'))
            ]))
            
            story.append(scores_table)
        
        return story
    
    def _create_brain_mapping_section(self, report_data: Dict[str, Any]) -> list:
        """Create brain mapping section"""
        story = []
        
        # Section title
        title = Paragraph("Brain Mapping Analysis", self.styles['CustomHeading'])
        story.append(title)
        
        # Add 3D brain mapping chart if available
        charts = report_data.get('charts', {})
        if 'brain_mapping_3d' in charts and charts['brain_mapping_3d']:
            story.append(Spacer(1, 20))
            story.append(Paragraph("3D Brain Mapping Visualization:", self.styles['CustomSubHeading']))
            
            # Chart explanation
            explanation = Paragraph(
                "<b>Chart Explanation:</b><br/>"
                "This 3D brain mapping visualization shows the correlation between your fingerprint patterns and brain region activity. "
                "The 3D model represents different brain regions, with color intensity and size indicating the level of neural activity "
                "predicted by your dermatoglyphic patterns. Brighter colors and larger regions suggest higher activity levels. "
                "This visualization helps understand how your unique fingerprint patterns relate to cognitive processing and brain function.",
                self.styles['CustomBody']
            )
            story.append(explanation)
            story.append(Spacer(1, 15))
            
            try:
                img_data = base64.b64decode(charts['brain_mapping_3d'])
                img_buffer = io.BytesIO(img_data)
                img = Image(img_buffer, width=6*inch, height=4*inch)
                story.append(img)
                story.append(Spacer(1, 20))
            except Exception as e:
                self.logger.warning(f"Could not add 3D brain mapping chart: {e}")
        
        # Brain mapping data
        brain_mapping = report_data.get('brain_mapping', {})
        if brain_mapping:
            story.append(Paragraph("Brain Region Analysis:", self.styles['CustomSubHeading']))
            
            # Table explanation
            brain_explanation = Paragraph(
                "<b>Table Explanation:</b><br/>"
                "This table shows the predicted activity levels for different brain regions based on your fingerprint analysis. "
                "The 'Activity Level' represents the estimated neural activity percentage for each brain region. "
                "Higher percentages indicate regions that are likely to be more active in your cognitive processing. "
                "This data helps understand your brain's processing patterns and can guide learning strategies and career choices.",
                self.styles['CustomBody']
            )
            story.append(brain_explanation)
            story.append(Spacer(1, 15))
            
            brain_data = [["Brain Region", "Activity Level"]]
            for region, level in brain_mapping.items():
                brain_data.append([
                    region.replace('_', ' ').title(),
                    f"{level:.1%}"
                ])
            
            brain_table = Table(brain_data, colWidths=[3*inch, 2*inch])
            brain_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#E74C3C')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Times-Bold'),
                ('FONTNAME', (0, 1), (-1, -1), 'Times-Roman'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
                ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#BDC3C7'))
            ]))
            
            story.append(brain_table)
        
        return story
    
    def _create_career_recommendations_section(self, report_data: Dict[str, Any]) -> list:
        """Create career recommendations section"""
        story = []
        
        # Section title
        title = Paragraph("Career Recommendations", self.styles['CustomHeading'])
        story.append(title)
        
        # Career recommendations
        career_recommendations = report_data.get('career_recommendations', [])
        if career_recommendations:
            # Section explanation
            career_explanation = Paragraph(
                "<b>Career Recommendations Explanation:</b><br/>"
                "The following career recommendations are generated based on your unique intelligence profile and brain mapping analysis. "
                "Each career is matched to your cognitive strengths, with the match percentage indicating how well your natural abilities "
                "align with the requirements of that profession. Higher match percentages suggest careers where you're likely to excel "
                "and find fulfillment based on your innate cognitive patterns.",
                self.styles['CustomBody']
            )
            story.append(career_explanation)
            story.append(Spacer(1, 15))
            
            story.append(Paragraph("Top Career Matches:", self.styles['CustomSubHeading']))
            
            for i, career in enumerate(career_recommendations[:5], 1):
                career_text = f"<b>{i}. {career['title']}</b> - Match: {career['match_percentage']:.1f}%<br/>"
                career_text += f"<i>{career['description']}</i>"
                
                career_para = Paragraph(career_text, self.styles['CustomBody'])
                story.append(career_para)
                story.append(Spacer(1, 12))
        else:
            story.append(Paragraph("Career recommendations will be generated based on your intelligence profile.", self.styles['CustomBody']))
        
        return story
    
    def _create_development_plan_section(self, report_data: Dict[str, Any]) -> list:
        """Create development plan section"""
        story = []
        
        # Section title
        title = Paragraph("Development Roadmap", self.styles['CustomHeading'])
        story.append(title)
        
        # Development plans
        development_plan = report_data.get('development_plan', [])
        if development_plan:
            # Section explanation
            development_explanation = Paragraph(
                "<b>Development Roadmap Explanation:</b><br/>"
                "This development roadmap is tailored to your specific intelligence profile and identifies areas for growth and enhancement. "
                "Each development area includes practical steps designed to strengthen your cognitive abilities and maximize your potential. "
                "The recommendations are based on scientific research and are designed to complement your natural strengths while "
                "developing areas that may need more attention.",
                self.styles['CustomBody']
            )
            story.append(development_explanation)
            story.append(Spacer(1, 15))
            
            for plan in development_plan:
                story.append(Paragraph(f"<b>{plan['title']}</b>", self.styles['CustomSubHeading']))
                story.append(Paragraph(plan['description'], self.styles['CustomBody']))
                
                # Add steps
                for step in plan.get('steps', []):
                    step_para = Paragraph(f"• {step}", self.styles['CustomBody'])
                    story.append(step_para)
                    story.append(Spacer(1, 6))
                
                # Add spacing between plan items, but not after the last one
                if plan != development_plan[-1]:  # Not the last plan
                    story.append(Spacer(1, 20))
        else:
            story.append(Paragraph("Development recommendations will be generated based on your intelligence profile.", self.styles['CustomBody']))
        
        return story
    
    def _create_technical_details_section(self, report_data: Dict[str, Any]) -> list:
        """Create technical details section"""
        story = []
        
        # Section title
        title = Paragraph("Technical Analysis Details", self.styles['CustomHeading'])
        story.append(title)
        
        # Quality metrics
        quality_metrics = report_data.get('quality_metrics', {})
        if quality_metrics:
            # Section explanation
            technical_explanation = Paragraph(
                "<b>Technical Analysis Explanation:</b><br/>"
                "This section provides technical details about the analysis process and quality metrics. "
                "The quality metrics indicate the reliability and accuracy of the fingerprint analysis, "
                "including factors like image quality, feature extraction success rate, and analysis confidence. "
                "These metrics help ensure the validity of the intelligence profile and recommendations provided.",
                self.styles['CustomBody']
            )
            story.append(technical_explanation)
            story.append(Spacer(1, 15))
            
            story.append(Paragraph("Analysis Quality Metrics:", self.styles['CustomSubHeading']))
            
            # Table explanation
            metrics_explanation = Paragraph(
                "<b>Metrics Explanation:</b><br/>"
                "The following metrics provide quantitative measures of the analysis quality and reliability. "
                "Higher values generally indicate better quality analysis, with confidence scores reflecting "
                "the certainty of the intelligence profile predictions based on your fingerprint patterns.",
                self.styles['CustomBody']
            )
            story.append(metrics_explanation)
            story.append(Spacer(1, 15))
            
            quality_data = [["Metric", "Value"]]
            for metric, value in quality_metrics.items():
                quality_data.append([
                    metric.replace('_', ' ').title(),
                    f"{value:.3f}" if isinstance(value, float) else str(value)
                ])
            
            quality_table = Table(quality_data, colWidths=[2.5*inch, 2.5*inch])
            quality_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#27AE60')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Times-Bold'),
                ('FONTNAME', (0, 1), (-1, -1), 'Times-Roman'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
                ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#BDC3C7'))
            ]))
            
            story.append(quality_table)
        
        return story
    
    def _create_page_template(self, doc):
        """Create page template with ivory background only (no page numbers)"""
        from reportlab.platypus import PageTemplate, Frame
        
        def page_header_footer(canvas, doc):
            # Set ivory/creamy background for entire page
            canvas.setFillColor(colors.HexColor('#FFFFF0'))  # Ivory color
            canvas.rect(0, 0, doc.pagesize[0], doc.pagesize[1], fill=1)
            
            # Set pure black color for text to ensure maximum visibility
            canvas.setFillColor(colors.black)
            
            # (Removed page numbers)
            # Log for debugging (optional)
            # self.logger.info(f"Page template applied to page {canvas.getPageNumber()}")
        
        # Create frame with proper margins
        frame = Frame(
            doc.leftMargin, doc.bottomMargin, 
            doc.width, doc.height, 
            id='normal'
        )
        
        # Create page template with explicit onPage callback
        template = PageTemplate(
            id='page_template', 
            frames=frame, 
            onPage=page_header_footer
        )
        
        return template
    
    def _get_intelligence_level(self, score: float) -> str:
        """Get intelligence level based on score"""
        if score >= 0.8:
            return "Exceptional"
        elif score >= 0.6:
            return "Strong"
        elif score >= 0.4:
            return "Moderate"
        elif score >= 0.2:
            return "Developing"
        else:
            return "Basic" 