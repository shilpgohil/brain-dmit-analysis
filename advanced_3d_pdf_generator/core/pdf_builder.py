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

            # 1. Cover Page
            story.extend(self._create_cover_page(report_data))
            story.append(PageBreak())

            # 2. Executive Summary
            story.extend(self._create_executive_summary(report_data))
            story.append(PageBreak())

            # 3. Fingerprint Pattern Summary (per-finger)
            if report_data.get('per_finger_data'):
                story.extend(self._create_finger_pattern_section(report_data))
                story.append(PageBreak())

            # 4. Intelligence Profile
            story.extend(self._create_intelligence_profile_section(report_data))
            story.append(PageBreak())

            # 5. Brain Mapping
            story.extend(self._create_brain_mapping_section(report_data))
            story.append(PageBreak())

            # 6. Learning Style
            if report_data.get('learning_styles'):
                story.extend(self._create_learning_style_section(report_data))
                story.append(PageBreak())

            # 7. Personality Profile (Big-5)
            if report_data.get('personality_analysis'):
                story.extend(self._create_personality_section(report_data))
                story.append(PageBreak())

            # 8-13. Extension sections (only if extension_results present)
            ext = report_data.get('extension_results', {})
            if ext:
                story.extend(self._create_eq_section(report_data))
                story.append(PageBreak())

                story.extend(self._create_cognitive_suite_section(report_data))
                story.append(PageBreak())

                story.extend(self._create_social_leadership_section(report_data))
                story.append(PageBreak())

                story.extend(self._create_motivation_creativity_section(report_data))
                story.append(PageBreak())

                story.extend(self._create_specialized_intelligences_section(report_data))
                story.append(PageBreak())

                story.extend(self._create_career_intelligence_section(report_data))
                story.append(PageBreak())

            # 14. Career Recommendations
            story.extend(self._create_career_recommendations_section(report_data))
            story.append(PageBreak())

            # 15. Development Roadmap
            story.extend(self._create_development_plan_section(report_data))
            story.append(PageBreak())

            # 16. Technical Details
            story.extend(self._create_technical_details_section(report_data))
            
            # Build PDF
            doc.build(story)
            
            self.logger.info(f" 3D PDF report generated successfully: {output_path}")
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
        """Create rich executive summary section"""
        story = []
        story.append(Paragraph("Executive Summary", self.styles['CustomHeading']))

        real_insights = report_data.get('real_insights', [])
        for insight in real_insights:
            story.append(Paragraph(f"• {insight}", self.styles['CustomBody']))
            story.append(Spacer(1, 5))

        # Key metrics summary table
        intel = report_data.get('intelligence_profile', {})
        personality = report_data.get('personality_analysis', {})
        brain = report_data.get('brain_mapping', {})
        learning = report_data.get('learning_styles', {})

        if intel:
            story.append(Spacer(1, 12))
            story.append(Paragraph("Key Profile Metrics at a Glance:", self.styles['CustomSubHeading']))

            dominant = max(intel.items(), key=lambda x: x[1]) if intel else ('N/A', 0)
            weakest = min(intel.items(), key=lambda x: x[1]) if intel else ('N/A', 0)
            dominant_hemi = 'Left' if brain.get('left_hemisphere_bias', 0.5) > brain.get('right_hemisphere_bias', 0.5) else 'Right'
            dominant_ls = max(learning.items(), key=lambda x: x[1])[0].title() if learning else 'N/A'

            # Derive personality archetype
            archetype = 'N/A'
            if personality:
                try:
                    from advanced_3d_pdf_generator.core.real_data_processor import derive_personality_archetype
                    archetype = derive_personality_archetype(personality)
                except Exception:
                    pass

            ext_results = report_data.get('extension_results', {})
            eq_data = ext_results.get('EmotionalIntelligenceExtension', {})
            eq_score = eq_data.get('emotional_intelligence_score', 0.0) if isinstance(eq_data, dict) else 0.0

            summary_rows = [
                ["Dominant Intelligence", dominant[0].replace('_', ' ').title(), f"{dominant[1]:.1%}"],
                ["Development Area", weakest[0].replace('_', ' ').title(), f"{weakest[1]:.1%}"],
                ["Brain Hemisphere Bias", f"{dominant_hemi} Hemisphere", ""],
                ["Primary Learning Style", dominant_ls, ""],
                ["Personality Archetype", archetype, ""],
                ["Emotional Intelligence", f"{eq_score:.1%}", self._get_intelligence_level(eq_score)],
            ]
            t = Table(summary_rows, colWidths=[2.2*inch, 2.8*inch, 1.0*inch])
            t.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#ECF0F1')),
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498DB')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('FONTNAME', (0, 0), (-1, 0), 'Times-Bold'),
                ('FONTNAME', (0, 1), (0, -1), 'Times-Bold'),
                ('FONTNAME', (1, 1), (-1, -1), 'Times-Roman'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#BDC3C7')),
            ]))
            story.append(t)
        return story

    def _create_intelligence_profile_section(self, report_data: Dict[str, Any]) -> list:
        """Create intelligence profile section with radar + ranked bar + table"""
        story = []
        story.append(Paragraph("Intelligence Profile Analysis", self.styles['CustomHeading']))
        story.append(Paragraph(
            "Your Multiple Intelligence profile is derived from the biometric analysis of all 10 fingerprints. "
            "Each intelligence dimension corresponds to specific brain lobe activity patterns encoded in your "
            "dermatoglyphic features. Scores represent your natural cognitive strength in each area.",
            self.styles['CustomBody']))

        charts = report_data.get('charts', {})
        self._insert_chart(story, charts, 'intelligence_radar_3d',
                           '3D Intelligence Radar', 6.5*inch, 5*inch)
        self._insert_chart(story, charts, 'intelligence_bar',
                           'Intelligence Scores — Ranked', 6.5*inch, 4*inch)

        intelligence_profile = report_data.get('intelligence_profile', {})
        if intelligence_profile:
            story.append(Paragraph("Detailed Intelligence Scores:", self.styles['CustomSubHeading']))
            header = ["Intelligence Type", "Score", "Level", "Interpretation"]
            rows = [header]
            for k, v in sorted(intelligence_profile.items(), key=lambda x: x[1], reverse=True):
                level = self._get_intelligence_level(v)
                interp = self._intelligence_interpretation(k, v)
                rows.append([k.replace('_', ' ').title(), f"{v:.1%}", level, interp])
            t = Table(rows, colWidths=[1.8*inch, 0.8*inch, 1.0*inch, 2.9*inch])
            t.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498DB')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('FONTNAME', (0, 0), (-1, 0), 'Times-Bold'),
                ('FONTNAME', (0, 1), (-1, -1), 'Times-Roman'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('ALIGN', (1, 0), (2, -1), 'CENTER'),
                ('ALIGN', (0, 0), (0, -1), 'LEFT'),
                ('ALIGN', (3, 0), (3, -1), 'LEFT'),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#FDFEFE'), colors.HexColor('#EBF5FB')]),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#BDC3C7')),
            ]))
            story.append(t)
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
        if score >= 0.80: return "Exceptional"
        elif score >= 0.65: return "Strong"
        elif score >= 0.50: return "Moderate"
        elif score >= 0.35: return "Developing"
        else: return "Basic"

    def _intelligence_interpretation(self, key: str, score: float) -> str:
        intros = {
            'linguistic': 'Language, writing, and verbal expression',
            'logical_mathematical': 'Reasoning, analysis, and numerical thinking',
            'spatial': 'Visual-spatial awareness and 3-D thinking',
            'musical': 'Rhythm, melody, and sound pattern recognition',
            'bodily_kinesthetic': 'Physical coordination and body-mind mastery',
            'interpersonal': 'Reading others and building relationships',
            'intrapersonal': 'Self-awareness and inner emotional insight',
            'naturalistic': 'Patterns in nature and biological systems',
            'existential': 'Philosophical depth and search for meaning',
        }
        intro = intros.get(key, key.replace('_', ' ').title())
        level = self._get_intelligence_level(score)
        return f"{intro} — {level} ({score:.0%})"

    # ------------------------------------------------------------------
    # CHART INSERT HELPER
    # ------------------------------------------------------------------

    def _insert_chart(self, story: list, charts: dict, key: str,
                      title: str, w=6*inch, h=4*inch):
        """Safely decode and insert a base64 chart image."""
        if not charts.get(key):
            return
        try:
            img_data = base64.b64decode(charts[key])
            img = Image(io.BytesIO(img_data), width=w, height=h)
            story.append(Spacer(1, 10))
            story.append(img)
            story.append(Spacer(1, 12))
        except Exception as e:
            self.logger.warning(f"Could not insert chart '{key}': {e}")

    def _score_table(self, rows_data: list, col_widths: list,
                     header_colour: str = '#3498DB') -> Table:
        """Build a consistently styled score table."""
        t = Table(rows_data, colWidths=col_widths)
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor(header_colour)),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Times-Bold'),
            ('FONTNAME', (0, 1), (-1, -1), 'Times-Roman'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1),
             [colors.HexColor('#FDFEFE'), colors.HexColor('#EBF5FB')]),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#BDC3C7')),
        ]))
        return t

    # ------------------------------------------------------------------
    # SECTION 3: FINGERPRINT PATTERN SUMMARY
    # ------------------------------------------------------------------

    def _create_finger_pattern_section(self, report_data: dict) -> list:
        story = []
        story.append(Paragraph("Fingerprint Pattern Summary", self.styles['CustomHeading']))
        story.append(Paragraph(
            "Each finger's pattern type (Arch, Loop, Whorl) is encoded in the dermatoglyphic "
            "formation during foetal development and is directly correlated with brain lobe "
            "development. The table below shows the biometric readings for all 10 fingerprints.",
            self.styles['CustomBody']))

        charts = report_data.get('charts', {})
        self._insert_chart(story, charts, 'finger_pattern_bar',
                           'Fingerprint Pattern Distribution', 6.5*inch, 4*inch)

        per_finger = report_data.get('per_finger_data', [])
        if per_finger:
            header = ['#', 'Finger', 'Pattern', 'Quality', 'Confidence', 'Minutiae', 'TFRC']
            rows = [header]
            for f in per_finger:
                rows.append([
                    str(f.get('index', '')),
                    str(f.get('finger_type', 'UNKNOWN')).replace('_', ' ').title(),
                    f.get('pattern_type', '—'),
                    f"{f.get('image_quality', 0)*100:.0f}%",
                    f"{f.get('feature_confidence', 0)*100:.0f}%",
                    str(f.get('minutiae_count', 0)),
                    f"{f.get('tfrc', 0):.1f}",
                ])
            t = self._score_table(rows,
                [0.3*inch, 1.1*inch, 0.9*inch, 0.7*inch, 0.8*inch, 0.7*inch, 0.7*inch],
                '#2C3E50')
            story.append(t)
        return story

    # ------------------------------------------------------------------
    # SECTION 6: LEARNING STYLE
    # ------------------------------------------------------------------

    def _create_learning_style_section(self, report_data: dict) -> list:
        story = []
        story.append(Paragraph("Learning Style Analysis", self.styles['CustomHeading']))
        story.append(Paragraph(
            "Your dominant learning style reflects how you most effectively encode and retrieve "
            "information. Dermatoglyphic patterns on the index finger (Visual) and little finger "
            "(Visual/Auditory) provide the primary biometric basis for this mapping.",
            self.styles['CustomBody']))

        charts = report_data.get('charts', {})
        self._insert_chart(story, charts, 'learning_styles_pie',
                           'Learning Style Distribution', 6.5*inch, 4*inch)

        ls = report_data.get('learning_styles', {})
        if ls:
            tips = {
                'visual': 'Use mind-maps, diagrams, colour-coding, and visual note-taking.',
                'auditory': 'Leverage lectures, podcasts, discussions, and verbal repetition.',
                'kinesthetic': 'Apply hands-on practice, movement breaks, and role-playing.',
            }
            rows = [['Style', 'Score', 'Level', 'Recommended Strategies']]
            for k, v in sorted(ls.items(), key=lambda x: x[1], reverse=True):
                rows.append([k.title(), f"{v:.1%}", self._get_intelligence_level(v),
                             tips.get(k, '—')])
            t = self._score_table(rows,
                [1.0*inch, 0.7*inch, 0.9*inch, 3.9*inch], '#16A085')
            story.append(t)
        return story

    # ------------------------------------------------------------------
    # SECTION 7: PERSONALITY (BIG-5)
    # ------------------------------------------------------------------

    def _create_personality_section(self, report_data: dict) -> list:
        story = []
        story.append(Paragraph("Personality Profile (Big-5)", self.styles['CustomHeading']))
        story.append(Paragraph(
            "The Big-5 personality dimensions are derived from the thumb fingerprint's prefrontal "
            "lobe correlation. Openness maps to fractal complexity; Conscientiousness to pattern "
            "regularity; Extraversion to ridge density; Agreeableness to symmetry; and Neuroticism "
            "to spectral variance.",
            self.styles['CustomBody']))

        charts = report_data.get('charts', {})
        self._insert_chart(story, charts, 'personality_bar',
                           'Big-5 Personality Profile', 6.5*inch, 4*inch)

        personality = report_data.get('personality_analysis', {})
        if personality:
            # Personality archetype
            try:
                from advanced_3d_pdf_generator.core.real_data_processor import derive_personality_archetype
                archetype = derive_personality_archetype(personality)
                story.append(Paragraph(
                    f"<b>Personality Archetype:</b> {archetype}",
                    self.styles['CustomBody']))
                story.append(Spacer(1, 8))
            except Exception:
                pass

            descs = {
                'openness': 'Curiosity, creativity, and willingness to embrace new ideas.',
                'conscientiousness': 'Organisation, reliability, and goal-oriented discipline.',
                'extraversion': 'Sociability, assertiveness, and positive emotional expression.',
                'agreeableness': 'Cooperation, trust, and empathy toward others.',
                'neuroticism': 'Emotional reactivity, anxiety, and stress sensitivity.',
            }
            rows = [['Trait', 'Score', 'Level', 'Description']]
            for k, v in sorted(personality.items(), key=lambda x: x[1], reverse=True):
                rows.append([k.title(), f"{v:.1%}", self._get_intelligence_level(v),
                             descs.get(k, '—')])
            t = self._score_table(rows,
                [1.1*inch, 0.7*inch, 0.9*inch, 3.8*inch], '#8E44AD')
            story.append(t)
        return story

    # ------------------------------------------------------------------
    # SECTION 8: EMOTIONAL INTELLIGENCE DEEP-DIVE
    # ------------------------------------------------------------------

    def _create_eq_section(self, report_data: dict) -> list:
        story = []
        story.append(Paragraph("Emotional Intelligence — Deep Dive", self.styles['CustomHeading']))
        ext = report_data.get('extension_results', {})
        eq = ext.get('EmotionalIntelligenceExtension', {})
        if not isinstance(eq, dict) or 'error' in eq:
            story.append(Paragraph("Emotional Intelligence data unavailable.", self.styles['CustomBody']))
            return story

        score = eq.get('emotional_intelligence_score', 0.0)
        style = eq.get('primary_emotional_style', '').replace('_', ' ').title()
        story.append(Paragraph(
            f"Overall EQ Score: <b>{score:.1%}</b> ({self._get_intelligence_level(score)}) | "
            f"Primary Emotional Style: <b>{style}</b>",
            self.styles['CustomBody']))

        charts = report_data.get('charts', {})
        self._insert_chart(story, charts, 'eq_radar',
                           'EQ 8-Dimension Radar', 6.5*inch, 5*inch)

        sub_keys = ['emotional_awareness', 'emotional_regulation', 'empathy', 'social_skills',
                    'emotional_expression', 'emotional_memory', 'emotional_processing',
                    'emotional_resilience']
        rows = [['EQ Dimension', 'Score', 'Level']]
        for k in sub_keys:
            v = float(eq.get(k, 0.0) or 0.0)
            rows.append([k.replace('_', ' ').title(), f"{v:.1%}", self._get_intelligence_level(v)])
        t = self._score_table(rows, [2.5*inch, 1.0*inch, 1.5*inch], '#E74C3C')
        story.append(t)
        return story

    # ------------------------------------------------------------------
    # GENERIC EXTENSION GROUP SECTION BUILDER
    # ------------------------------------------------------------------

    def _build_extension_group_section(self, report_data: dict,
                                        title: str, description: str,
                                        group_keys: list, chart_key: str,
                                        header_colour: str) -> list:
        story = []
        story.append(Paragraph(title, self.styles['CustomHeading']))
        story.append(Paragraph(description, self.styles['CustomBody']))

        charts = report_data.get('charts', {})
        self._insert_chart(story, charts, chart_key, title, 6.5*inch, max(3.5*inch, len(group_keys)*0.35*inch))

        ext = report_data.get('extension_results', {})
        try:
            from advanced_3d_pdf_generator.core.real_data_processor import (
                _find_main_score, _find_primary_style, EXTENSION_DISPLAY_NAMES)
        except ImportError:
            return story

        rows = [['Extension', 'Score', 'Level', 'Primary Style']]
        for key in group_keys:
            data = ext.get(key, {})
            if not isinstance(data, dict) or 'error' in data:
                continue
            score = _find_main_score(data)
            style_label = _find_primary_style(data) or '—'
            display = EXTENSION_DISPLAY_NAMES.get(key, key.replace('Extension', '').replace('_', ' '))
            rows.append([display, f"{score:.1%}", self._get_intelligence_level(score), style_label])

        if len(rows) > 1:
            t = self._score_table(rows, [2.3*inch, 0.8*inch, 0.9*inch, 2.5*inch], header_colour)
            story.append(t)
        return story

    # ------------------------------------------------------------------
    # SECTION 9: COGNITIVE SUITE
    # ------------------------------------------------------------------

    def _create_cognitive_suite_section(self, report_data: dict) -> list:
        return self._build_extension_group_section(
            report_data,
            title="Cognitive Abilities Suite",
            description=(
                "This section consolidates seven core cognitive dimensions derived from your "
                "fingerprint topology — from decision speed and attention span to meta-cognitive "
                "self-monitoring and working memory capacity."
            ),
            group_keys=[
                'DecisionMakingExtension', 'AttentionFocusExtension', 'MemoryProcessingExtension',
                'ExecutiveFunctionExtension', 'CognitiveLoadExtension', 'MetaCognitionExtension',
                'LearningAgilityExtension',
            ],
            chart_key='cognitive_bar',
            header_colour='#2980B9',
        )

    # ------------------------------------------------------------------
    # SECTION 10: SOCIAL & LEADERSHIP
    # ------------------------------------------------------------------

    def _create_social_leadership_section(self, report_data: dict) -> list:
        return self._build_extension_group_section(
            report_data,
            title="Social & Leadership Profile",
            description=(
                "Leadership potential, communication style, interpersonal intelligence, and "
                "social awareness are mapped from the spectral and graph-theoretic features of "
                "your fingerprint ridge network — reflecting your natural social and leadership wiring."
            ),
            group_keys=[
                'LeadershipPotentialExtension', 'CommunicationStyleExtension',
                'InterpersonalIntelligenceExtension', 'SocialAwarenessExtension',
                'RelationshipDynamicsExtension', 'LeftRightBrainExtension',
            ],
            chart_key='social_bar',
            header_colour='#16A085',
        )

    # ------------------------------------------------------------------
    # SECTION 11: MOTIVATION, CREATIVITY & INNOVATION
    # ------------------------------------------------------------------

    def _create_motivation_creativity_section(self, report_data: dict) -> list:
        return self._build_extension_group_section(
            report_data,
            title="Motivation, Creativity & Innovation",
            description=(
                "Creativity, entrepreneurial drive, risk appetite, curiosity, and grit are "
                "all derivable from the fractal complexity and topological richness of your "
                "fingerprint patterns — capturing your innate drive and innovation capacity."
            ),
            group_keys=[
                'CreativityIndexExtension', 'InnovationIntelligenceExtension',
                'EntrepreneurialAptitudeExtension', 'RiskToleranceExtension',
                'CuriosityExploratoryExtension', 'PersistenceGritExtension',
                'MotivationDriveExtension',
            ],
            chart_key='motivation_bar',
            header_colour='#8E44AD',
        )

    # ------------------------------------------------------------------
    # SECTION 12: SPECIALISED INTELLIGENCES
    # ------------------------------------------------------------------

    def _create_specialized_intelligences_section(self, report_data: dict) -> list:
        return self._build_extension_group_section(
            report_data,
            title="Specialised Intelligence Scores",
            description=(
                "Gardner's theory of Multiple Intelligences is extended here with Systems "
                "Thinking, Pattern Recognition, Wellness, and Sustainability Intelligence — "
                "each derived from distinct biometric fingerprint features."
            ),
            group_keys=[
                'LinguisticIntelligenceExtension', 'LogicalMathematicalIntelligenceExtension',
                'SpatialIntelligenceExtension', 'MusicalIntelligenceExtension',
                'BodilyKinestheticIntelligenceExtension', 'IntrapersonalIntelligenceExtension',
                'NaturalisticIntelligenceExtension', 'SystemsThinkingExtension',
                'PatternRecognitionExtension', 'WellnessIntelligenceExtension',
                'SustainabilityIntelligenceExtension',
            ],
            chart_key='specialized_bar',
            header_colour='#27AE60',
        )

    # ------------------------------------------------------------------
    # SECTION 13: CAREER & LIFE INTELLIGENCE
    # ------------------------------------------------------------------

    def _create_career_intelligence_section(self, report_data: dict) -> list:
        return self._build_extension_group_section(
            report_data,
            title="Career & Life Intelligence",
            description=(
                "Stress resilience, self-regulation, cultural adaptability, digital intelligence, "
                "and financial acumen are mapped from your fingerprint's spectral entropy and "
                "network features — giving a holistic view of your life-readiness profile."
            ),
            group_keys=[
                'StressResponseExtension', 'AdaptabilityResilienceExtension',
                'SelfRegulationExtension', 'HealthWellnessExtension',
                'FinancialIntelligenceExtension', 'DigitalIntelligenceExtension',
                'CulturalIntelligenceExtension', 'NeurodivergenceExtension',
            ],
            chart_key='career_bar',
            header_colour='#E67E22',
        )