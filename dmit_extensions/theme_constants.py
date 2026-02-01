"""
Theme constants for the AI-Powered Quantum DMIT Analysis Dashboard
"""

from reportlab.lib.colors import HexColor

# Color Palette
PRIMARY_COLOR = '#2C3E50'  # Dark Blue-Gray
SECONDARY_COLOR = '#3498DB'  # Blue
ACCENT_COLOR = '#E74C3C'  # Red
SUCCESS_COLOR = '#27AE60'  # Green
WARNING_COLOR = '#F39C12'  # Orange
INFO_COLOR = '#1ABC9C'  # Teal
LIGHT_COLOR = '#ECF0F1'  # Light Gray
DARK_COLOR = '#34495E'  # Dark Gray

# Intelligence Type Colors
INTELLIGENCE_COLORS = {
    'Linguistic': '#3498DB',
    'Logical-Mathematical': '#E74C3C',
    'Spatial': '#9B59B6',
    'Musical': '#F39C12',
    'Bodily-Kinesthetic': '#27AE60',
    'Interpersonal': '#1ABC9C',
    'Intrapersonal': '#34495E',
    'Naturalistic': '#95A5A6',
    'Existential': '#8E44AD',
    'Spiritual': '#16A085'
}

# Confidence Level Colors
CONFIDENCE_COLORS = {
    'high': '#27AE60',    # Green for ≥80%
    'medium': '#F39C12',  # Amber for 60-79%
    'low': '#E74C3C'      # Red for <60%
}

# Font Settings
FONT_FAMILY = 'Times-Roman'
FONT_FAMILY_BOLD = 'Times-Bold'
FONT_FAMILY_ITALIC = 'Times-Italic'

# Font Sizes
FONT_SIZE_TITLE = 28
FONT_SIZE_SUBTITLE = 18
FONT_SIZE_HEADING = 16
FONT_SIZE_SUBHEADING = 14
FONT_SIZE_BODY = 12
FONT_SIZE_SMALL = 10
FONT_SIZE_TINY = 8

# Spacing
SPACING_LARGE = 30
SPACING_MEDIUM = 20
SPACING_SMALL = 10
SPACING_TINY = 5

# Page Settings
PAGE_MARGIN = 0.5  # inches
PAGE_WIDTH = 8.5   # inches (Letter size)
PAGE_HEIGHT = 11   # inches (Letter size)

# Table Settings
TABLE_HEADER_BACKGROUND = PRIMARY_COLOR
TABLE_HEADER_TEXT_COLOR = '#FFFFFF'
TABLE_ROW_BACKGROUND = LIGHT_COLOR
TABLE_GRID_COLOR = '#000000'
TABLE_GRID_WIDTH = 1

# Chart Settings
CHART_WIDTH = 7.5  # inches
CHART_HEIGHT = 4   # inches
CHART_DPI = 300    # High resolution for print

# Badge Settings
BADGE_SIZE = (200, 200)  # pixels
BADGE_DEFAULT_COLOR = SECONDARY_COLOR

# Gradient Settings
GRADIENT_WIDTH = 800   # pixels
GRADIENT_HEIGHT = 60   # pixels
GRADIENT_OPACITY = 180  # Semi-transparent

# Confidence Indicator Settings
CONFIDENCE_INDICATOR_SIZE = (100, 20)  # pixels
CONFIDENCE_THRESHOLDS = {
    'high': 80,
    'medium': 60,
    'low': 0
}

# Auto-shrink Table Settings
MIN_FONT_SIZE = 6
MAX_FONT_SIZE = 12
DEFAULT_TABLE_HEIGHT = 6  # inches

# Mini-chart Settings
MINI_CHART_WIDTH = 3  # inches
MINI_CHART_HEIGHT = 1  # inches

# Two-column Layout Settings
COLUMN_GAP = 0.25  # inches
COLUMN_WIDTH = (PAGE_WIDTH - 2 * PAGE_MARGIN - COLUMN_GAP) / 2

# Header and Footer Settings
HEADER_HEIGHT = 1    # inches
FOOTER_HEIGHT = 0.5  # inches
BODY_HEIGHT = PAGE_HEIGHT - 2 * PAGE_MARGIN - HEADER_HEIGHT - FOOTER_HEIGHT

# Professional Color Schemes
PROFESSIONAL_COLORS = {
    'primary': PRIMARY_COLOR,
    'secondary': SECONDARY_COLOR,
    'accent': ACCENT_COLOR,
    'success': SUCCESS_COLOR,
    'warning': WARNING_COLOR,
    'info': INFO_COLOR,
    'light': LIGHT_COLOR,
    'dark': DARK_COLOR
}

# Section-specific Colors
SECTION_COLORS = {
    'executive_summary': SECONDARY_COLOR,
    'intelligence_analysis': ACCENT_COLOR,
    'finger_analysis': SUCCESS_COLOR,
    'personality_insights': '#9B59B6',  # Purple
    'development_roadmap': WARNING_COLOR,
    'scientific_validation': INFO_COLOR,
    'extensions_analysis': '#E67E22',   # Orange
    'technical_analysis': DARK_COLOR,
    'comprehensive_info': PRIMARY_COLOR,
    'appendix': '#95A5A6'               # Gray
}

# Typography Styles
TYPOGRAPHY_STYLES = {
    'title': {
        'fontName': FONT_FAMILY_BOLD,
        'fontSize': FONT_SIZE_TITLE,
        'textColor': PRIMARY_COLOR,
        'alignment': 'center',
        'spaceAfter': SPACING_LARGE
    },
    'subtitle': {
        'fontName': FONT_FAMILY_BOLD,
        'fontSize': FONT_SIZE_SUBTITLE,
        'textColor': PRIMARY_COLOR,
        'alignment': 'center',
        'spaceAfter': SPACING_MEDIUM
    },
    'heading': {
        'fontName': FONT_FAMILY_BOLD,
        'fontSize': FONT_SIZE_HEADING,
        'textColor': PRIMARY_COLOR,
        'alignment': 'left',
        'spaceAfter': SPACING_MEDIUM
    },
    'subheading': {
        'fontName': FONT_FAMILY_BOLD,
        'fontSize': FONT_SIZE_SUBHEADING,
        'textColor': DARK_COLOR,
        'alignment': 'left',
        'spaceAfter': SPACING_SMALL
    },
    'body': {
        'fontName': FONT_FAMILY,
        'fontSize': FONT_SIZE_BODY,
        'textColor': PRIMARY_COLOR,
        'alignment': 'justify',
        'spaceAfter': SPACING_SMALL
    },
    'small': {
        'fontName': FONT_FAMILY,
        'fontSize': FONT_SIZE_SMALL,
        'textColor': DARK_COLOR,
        'alignment': 'left',
        'spaceAfter': SPACING_TINY
    }
}

# Layout Constants
LAYOUT_CONSTANTS = {
    'page_margin': PAGE_MARGIN,
    'page_width': PAGE_WIDTH,
    'page_height': PAGE_HEIGHT,
    'header_height': HEADER_HEIGHT,
    'footer_height': FOOTER_HEIGHT,
    'body_height': BODY_HEIGHT,
    'column_gap': COLUMN_GAP,
    'column_width': COLUMN_WIDTH
}

# Chart Configuration
CHART_CONFIG = {
    'width': CHART_WIDTH,
    'height': CHART_HEIGHT,
    'dpi': CHART_DPI,
    'background_color': '#FFFFFF',
    'font_family': FONT_FAMILY,
    'font_size': FONT_SIZE_SMALL
}

# Badge Configuration
BADGE_CONFIG = {
    'size': BADGE_SIZE,
    'default_color': BADGE_DEFAULT_COLOR,
    'background_transparent': True
}

# Gradient Configuration
GRADIENT_CONFIG = {
    'width': GRADIENT_WIDTH,
    'height': GRADIENT_HEIGHT,
    'opacity': GRADIENT_OPACITY,
    'default_start_color': SECONDARY_COLOR,
    'default_end_color': PRIMARY_COLOR
} 