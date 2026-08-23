import logging
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.platypus import Frame, PageTemplate, NextPageTemplate
from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas
from .theme_constants import LAYOUT_CONSTANTS

class DashboardPageTemplate:
    """Page template manager for dashboard PDF layouts."""
    
    def __init__(self):
        self.layout = LAYOUT_CONSTANTS
        self.logger = logging.getLogger(__name__)
        self.page_width, self.page_height = A4
        
    def create_page_template(self) -> PageTemplate:
        """Create the main page template with header, body, and footer frames."""
        try:
            # Header frame
            header_frame = Frame(
                self.layout['page_margin'] * inch,
                (self.layout['page_height'] - self.layout['page_margin'] - self.layout['header_height']) * inch,
                (self.layout['page_width'] - 2 * self.layout['page_margin']) * inch,
                self.layout['header_height'] * inch,
                leftPadding=0,
                bottomPadding=0,
                rightPadding=0,
                topPadding=0,
                id='header'
            )
            
            # Body frame
            body_frame = Frame(
                self.layout['page_margin'] * inch,
                (self.layout['footer_height'] + self.layout['page_margin']) * inch,
                (self.layout['page_width'] - 2 * self.layout['page_margin']) * inch,
                (self.layout['body_height']) * inch,
                leftPadding=0.1 * inch,
                bottomPadding=0.1 * inch,
                rightPadding=0.1 * inch,
                topPadding=0.1 * inch,
                id='body'
            )
            
            # Footer frame
            footer_frame = Frame(
                self.layout['page_margin'] * inch,
                self.layout['page_margin'] * inch,
                (self.layout['page_width'] - 2 * self.layout['page_margin']) * inch,
                self.layout['footer_height'] * inch,
                leftPadding=0,
                bottomPadding=0,
                rightPadding=0,
                topPadding=0,
                id='footer'
            )
            
            # Create page template
            page_template = PageTemplate(
                id='main_template',
                frames=[header_frame, body_frame, footer_frame],
                onPage=self._add_page_elements
            )
            
            return page_template
            
        except Exception as e:
            self.logger.error(f"Error creating page template: {e}")
            return None
    
    def create_two_column_template(self) -> PageTemplate:
        """Create a two-column page template for content-heavy sections."""
        try:
            # Header frame
            header_frame = Frame(
                self.layout['page_margin'] * inch,
                (self.layout['page_height'] - self.layout['page_margin'] - self.layout['header_height']) * inch,
                (self.layout['page_width'] - 2 * self.layout['page_margin']) * inch,
                self.layout['header_height'] * inch,
                leftPadding=0,
                bottomPadding=0,
                rightPadding=0,
                topPadding=0,
                id='header'
            )
            
            # Left column frame
            left_frame = Frame(
                self.layout['page_margin'] * inch,
                (self.layout['footer_height'] + self.layout['page_margin']) * inch,
                self.layout['column_width'] * inch,
                (self.layout['body_height']) * inch,
                leftPadding=0.1 * inch,
                bottomPadding=0.1 * inch,
                rightPadding=0.05 * inch,
                topPadding=0.1 * inch,
                id='left_column'
            )
            
            # Right column frame
            right_frame = Frame(
                (self.layout['page_margin'] + self.layout['column_width'] + self.layout['column_gap']) * inch,
                (self.layout['footer_height'] + self.layout['page_margin']) * inch,
                self.layout['column_width'] * inch,
                (self.layout['body_height']) * inch,
                leftPadding=0.05 * inch,
                bottomPadding=0.1 * inch,
                rightPadding=0.1 * inch,
                topPadding=0.1 * inch,
                id='right_column'
            )
            
            # Footer frame
            footer_frame = Frame(
                self.layout['page_margin'] * inch,
                self.layout['page_margin'] * inch,
                (self.layout['page_width'] - 2 * self.layout['page_margin']) * inch,
                self.layout['footer_height'] * inch,
                leftPadding=0,
                bottomPadding=0,
                rightPadding=0,
                topPadding=0,
                id='footer'
            )
            
            # Create two-column page template
            two_column_template = PageTemplate(
                id='two_column_template',
                frames=[header_frame, left_frame, right_frame, footer_frame],
                onPage=self._add_page_elements
            )
            
            return two_column_template
            
        except Exception as e:
            self.logger.error(f"Error creating two-column template: {e}")
            return None
    
    def _add_page_elements(self, canvas, doc):
        """Add page elements like headers, footers, and page numbers."""
        try:
            # Add page number
            page_num = canvas.getPageNumber()
            canvas.setFont('Times-Roman', 10)
            canvas.setFillColorRGB(0.2, 0.2, 0.2)
            canvas.drawString(
                (self.layout['page_width'] - 1) * inch,
                0.3 * inch,
                f"Page {page_num}"
            )
            
            # Add header line
            canvas.setStrokeColorRGB(0.2, 0.2, 0.2)
            canvas.setLineWidth(0.5)
            canvas.line(
                self.layout['page_margin'] * inch,
                (self.layout['page_height'] - self.layout['page_margin'] - self.layout['header_height'] - 0.1) * inch,
                (self.layout['page_width'] - self.layout['page_margin']) * inch,
                (self.layout['page_height'] - self.layout['page_margin'] - self.layout['header_height'] - 0.1) * inch
            )
            
            # Add footer line
            canvas.line(
                self.layout['page_margin'] * inch,
                (self.layout['footer_height'] + self.layout['page_margin'] + 0.1) * inch,
                (self.layout['page_width'] - self.layout['page_margin']) * inch,
                (self.layout['footer_height'] + self.layout['page_margin'] + 0.1) * inch
            )
            
        except Exception as e:
            self.logger.error(f"Error adding page elements: {e}")
    
    def create_section_template(self, section_name: str) -> PageTemplate:
        """Create a section-specific page template."""
        try:
            # Use main template as base
            base_template = self.create_page_template()
            
            # Customize for section
            section_template = PageTemplate(
                id=f'{section_name}_template',
                frames=base_template.frames,
                onPage=lambda canvas, doc: self._add_section_elements(canvas, doc, section_name)
            )
            
            return section_template
            
        except Exception as e:
            self.logger.error(f"Error creating section template: {e}")
            return None
    
    def _add_section_elements(self, canvas, doc, section_name: str):
        """Add section-specific elements to the page."""
        try:
            # Add section name to header
            canvas.setFont('Times-Bold', 12)
            canvas.setFillColorRGB(0.2, 0.2, 0.2)
            canvas.drawString(
                self.layout['page_margin'] * inch,
                (self.layout['page_height'] - self.layout['page_margin'] - 0.3) * inch,
                section_name.upper()
            )
            
            # Call base page elements
            self._add_page_elements(canvas, doc)
            
        except Exception as e:
            self.logger.error(f"Error adding section elements: {e}")
    
    def get_template_by_name(self, template_name: str) -> PageTemplate:
        """Get a specific template by name."""
        templates = {
            'main': self.create_page_template,
            'two_column': self.create_two_column_template,
            'executive_summary': lambda: self.create_section_template('executive_summary'),
            'intelligence_analysis': lambda: self.create_section_template('intelligence_analysis'),
            'finger_analysis': lambda: self.create_section_template('finger_analysis'),
            'personality_insights': lambda: self.create_section_template('personality_insights'),
            'development_roadmap': lambda: self.create_section_template('development_roadmap'),
            'scientific_validation': lambda: self.create_section_template('scientific_validation'),
            'extensions_analysis': lambda: self.create_section_template('extensions_analysis'),
            'technical_analysis': lambda: self.create_section_template('technical_analysis'),
            'comprehensive_info': lambda: self.create_section_template('comprehensive_info'),
            'appendix': lambda: self.create_section_template('appendix')
        }
        
        if template_name in templates:
            return templates[template_name]()
        else:
            self.logger.warning(f"Template '{template_name}' not found, using main template")
            return self.create_page_template() 