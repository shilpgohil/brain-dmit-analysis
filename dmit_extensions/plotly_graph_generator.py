import plotly.graph_objects as go
import plotly.express as px
import plotly.io as pio
import numpy as np
import base64
import io
import logging
from typing import List, Dict, Any, Optional, Tuple
from .theme_constants import (
    INTELLIGENCE_COLORS, CHART_CONFIG, PROFESSIONAL_COLORS, 
    CONFIDENCE_COLORS, SECTION_COLORS
)

class PlotlyGraphGenerator:
    """Advanced Plotly graph generator for dashboard PDF charts."""
    
    def __init__(self):
        self.colors = INTELLIGENCE_COLORS
        self.chart_config = CHART_CONFIG
        self.professional_colors = PROFESSIONAL_COLORS
        self.confidence_colors = CONFIDENCE_COLORS
        self.section_colors = SECTION_COLORS
        self.logger = logging.getLogger(__name__)
        
        # Set Plotly configuration for high-quality exports
        pio.kaleido.scope.default_width = int(self.chart_config['width'] * 100)
        pio.kaleido.scope.default_height = int(self.chart_config['height'] * 100)
        pio.kaleido.scope.default_scale = 2

    def export_plotly_figure_to_base64(self, fig: go.Figure) -> str:
        """Export a Plotly figure to a base64 PNG string for PDF embedding."""
        try:
            img_bytes = fig.to_image(
                format="png", 
                width=int(self.chart_config['width'] * 100), 
                height=int(self.chart_config['height'] * 100), 
                scale=2
            )
            return base64.b64encode(img_bytes).decode()
        except Exception as e:
            self.logger.error(f"Error exporting Plotly figure: {e}")
            return ""

    def create_intelligence_radar_chart(self, intelligence_scores: Dict[str, float], 
                                      title: str = "Intelligence Profile") -> str:
        """Create a radar chart for intelligence scores."""
        try:
            categories = list(intelligence_scores.keys())
            values = list(intelligence_scores.values())
            
            fig = go.Figure()
            fig.add_trace(go.Scatterpolar(
                r=values,
                theta=categories,
                fill='toself',
                name=title,
                line_color=self.professional_colors['primary'],
                fillcolor='rgba(44, 62, 80, 0.4)'  # Using rgba format for transparency
            ))
            
            fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True, 
                        range=[0, 100],
                        tickfont=dict(size=10),
                        gridcolor='lightgray'
                    ),
                    angularaxis=dict(
                        tickfont=dict(size=10),
                        gridcolor='lightgray'
                    ),
                    bgcolor='white'
                ),
                showlegend=False,
                title=dict(
                    text=title,
                    font=dict(size=16, color=self.professional_colors['primary'])
                ),
                paper_bgcolor=self.chart_config['background_color'],
                font_family=self.chart_config['font_family'],
                font_size=self.chart_config['font_size'],
                margin=dict(l=50, r=50, t=80, b=50)
            )
            
            return self.export_plotly_figure_to_base64(fig)
            
        except Exception as e:
            self.logger.error(f"Error creating radar chart: {e}")
            return ""

    def create_intelligence_bar_chart(self, intelligence_scores: Dict[str, float], 
                                    title: str = "Intelligence Scores") -> str:
        """Create a bar chart for intelligence scores."""
        try:
            categories = list(intelligence_scores.keys())
            values = list(intelligence_scores.values())
            
            fig = go.Figure([go.Bar(
                x=categories,
                y=values,
                marker_color=[self.colors.get(cat, self.professional_colors['secondary']) for cat in categories],
                marker_line=dict(color='white', width=1),
                text=[f"{v:.1f}" for v in values],
                textposition='auto',
                textfont=dict(size=10, color='white')
            )])
            
            fig.update_layout(
                title=dict(
                    text=title,
                    font=dict(size=16, color=self.professional_colors['primary'])
                ),
                xaxis=dict(
                    title="Intelligence Types",
                    tickangle=45,
                    tickfont=dict(size=10)
                ),
                yaxis=dict(
                    title="Score",
                    range=[0, 100],
                    tickfont=dict(size=10)
                ),
                paper_bgcolor=self.chart_config['background_color'],
                font_family=self.chart_config['font_family'],
                font_size=self.chart_config['font_size'],
                margin=dict(l=50, r=50, t=80, b=80),
                showlegend=False
            )
            
            return self.export_plotly_figure_to_base64(fig)
            
        except Exception as e:
            self.logger.error(f"Error creating bar chart: {e}")
            return ""

    def create_intelligence_pie_chart(self, intelligence_scores: Dict[str, float], 
                                    title: str = "Intelligence Distribution") -> str:
        """Create a pie chart for intelligence distribution."""
        try:
            labels = list(intelligence_scores.keys())
            values = list(intelligence_scores.values())
            
            fig = go.Figure(go.Pie(
                labels=labels,
                values=values,
                marker_colors=[self.colors.get(lbl, self.professional_colors['secondary']) for lbl in labels],
                textinfo='label+percent',
                textfont=dict(size=10),
                hole=0.3
            ))
            
            fig.update_layout(
                title=dict(
                    text=title,
                    font=dict(size=16, color=self.professional_colors['primary'])
                ),
                paper_bgcolor=self.chart_config['background_color'],
                font_family=self.chart_config['font_family'],
                font_size=self.chart_config['font_size'],
                margin=dict(l=50, r=50, t=80, b=50),
                showlegend=True,
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1
                )
            )
            
            return self.export_plotly_figure_to_base64(fig)
            
        except Exception as e:
            self.logger.error(f"Error creating pie chart: {e}")
            return ""

    def create_finger_analysis_heatmap(self, finger_data: Dict[str, Dict[str, Any]], 
                                     title: str = "Finger Analysis Overview") -> str:
        """Create a heatmap for finger analysis data."""
        try:
            fingers = list(finger_data.keys())
            metrics = ['confidence', 'ridge_count', 'quality_score']
            
            # Prepare data for heatmap
            z_data = []
            for metric in metrics:
                row = []
                for finger in fingers:
                    value = finger_data[finger].get(metric, 0)
                    if metric == 'confidence':
                        value = value  # Already 0-100
                    elif metric == 'ridge_count':
                        value = min(value * 5, 100)  # Scale ridge count to 0-100
                    elif metric == 'quality_score':
                        value = value * 10  # Scale quality score to 0-100
                    row.append(value)
                z_data.append(row)
            
            fig = go.Figure(data=go.Heatmap(
                z=z_data,
                x=fingers,
                y=metrics,
                colorscale='Viridis',
                text=[[f"{z_data[i][j]:.1f}" for j in range(len(fingers))] for i in range(len(metrics))],
                texttemplate="%{text}",
                textfont={"size": 10},
                colorbar=dict(title="Score")
            ))
            
            fig.update_layout(
                title=dict(
                    text=title,
                    font=dict(size=16, color=self.professional_colors['primary'])
                ),
                xaxis=dict(
                    title="Fingers",
                    tickangle=45,
                    tickfont=dict(size=10)
                ),
                yaxis=dict(
                    title="Metrics",
                    tickfont=dict(size=10)
                ),
                paper_bgcolor=self.chart_config['background_color'],
                font_family=self.chart_config['font_family'],
                font_size=self.chart_config['font_size'],
                margin=dict(l=50, r=50, t=80, b=80)
            )
            
            return self.export_plotly_figure_to_base64(fig)
            
        except Exception as e:
            self.logger.error(f"Error creating heatmap: {e}")
            return ""

    def create_grouped_bar_chart(self, categories: List[str], series: List[List[float]], 
                                series_names: List[str], title: str = "Grouped Analysis") -> str:
        """Create a grouped bar chart for comparative analysis."""
        try:
            fig = go.Figure()
            
            for idx, values in enumerate(series):
                fig.add_trace(go.Bar(
                    x=categories,
                    y=values,
                    name=series_names[idx],
                    marker_color=self.colors.get(series_names[idx], self.professional_colors['secondary']),
                    marker_line=dict(color='white', width=1),
                    text=[f"{v:.1f}" for v in values],
                    textposition='auto',
                    textfont=dict(size=9, color='white')
                ))
            
            fig.update_layout(
                barmode='group',
                title=dict(
                    text=title,
                    font=dict(size=16, color=self.professional_colors['primary'])
                ),
                xaxis=dict(
                    title="Categories",
                    tickangle=45,
                    tickfont=dict(size=10)
                ),
                yaxis=dict(
                    title="Values",
                    tickfont=dict(size=10)
                ),
                paper_bgcolor=self.chart_config['background_color'],
                font_family=self.chart_config['font_family'],
                font_size=self.chart_config['font_size'],
                margin=dict(l=50, r=50, t=80, b=80),
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1
                )
            )
            
            return self.export_plotly_figure_to_base64(fig)
            
        except Exception as e:
            self.logger.error(f"Error creating grouped bar chart: {e}")
            return ""

    def create_progress_gauge(self, value: float, title: str = "Progress", 
                            min_val: float = 0, max_val: float = 100) -> str:
        """Create a progress gauge chart."""
        try:
            # Determine color based on value
            if value >= 80:
                color = self.confidence_colors['high']
            elif value >= 60:
                color = self.confidence_colors['medium']
            else:
                color = self.confidence_colors['low']
            
            fig = go.Figure(go.Indicator(
                mode="gauge+number+delta",
                value=value,
                domain={'x': [0, 1], 'y': [0, 1]},
                gauge={
                    'axis': {'range': [min_val, max_val], 'tickwidth': 1, 'tickcolor': "darkblue"},
                    'bar': {'color': color},
                    'bgcolor': "white",
                    'borderwidth': 2,
                    'bordercolor': "gray",
                    'steps': [
                        {'range': [0, 60], 'color': self.confidence_colors['low']},
                        {'range': [60, 80], 'color': self.confidence_colors['medium']},
                        {'range': [80, 100], 'color': self.confidence_colors['high']}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 90
                    }
                },
                title={'text': title, 'font': {'size': 16}},
                delta={'reference': 50}
            ))
            
            fig.update_layout(
                paper_bgcolor=self.chart_config['background_color'],
                font_family=self.chart_config['font_family'],
                font_size=self.chart_config['font_size'],
                margin=dict(l=50, r=50, t=80, b=50)
            )
            
            return self.export_plotly_figure_to_base64(fig)
            
        except Exception as e:
            self.logger.error(f"Error creating progress gauge: {e}")
            return ""

    def create_bubble_chart(self, x: List[float], y: List[float], size: List[float], 
                          labels: List[str], title: str = "Bubble Analysis") -> str:
        """Create a bubble chart for multi-dimensional analysis."""
        try:
            fig = go.Figure(data=[go.Scatter(
                x=x, 
                y=y, 
                mode='markers+text',
                marker=dict(
                    size=size, 
                    color=size, 
                    colorscale='Blues', 
                    showscale=True,
                    colorbar=dict(title="Size Value")
                ),
                text=labels, 
                textposition="top center",
                textfont=dict(size=10)
            )])
            
            fig.update_layout(
                title=dict(
                    text=title,
                    font=dict(size=16, color=self.professional_colors['primary'])
                ),
                xaxis=dict(
                    title="X Axis",
                    tickfont=dict(size=10)
                ),
                yaxis=dict(
                    title="Y Axis",
                    tickfont=dict(size=10)
                ),
                paper_bgcolor=self.chart_config['background_color'],
                font_family=self.chart_config['font_family'],
                font_size=self.chart_config['font_size'],
                margin=dict(l=50, r=50, t=80, b=80)
            )
            
            return self.export_plotly_figure_to_base64(fig)
            
        except Exception as e:
            self.logger.error(f"Error creating bubble chart: {e}")
            return ""

    def create_mini_gauge(self, value: float, title: str = "Mini Gauge", 
                         size: Tuple[int, int] = (200, 120)) -> str:
        """Create a mini gauge for compact display."""
        try:
            # Determine color based on value
            if value >= 80:
                color = self.confidence_colors['high']
            elif value >= 60:
                color = self.confidence_colors['medium']
            else:
                color = self.confidence_colors['low']
            
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=value,
                domain={'x': [0, 1], 'y': [0, 1]},
                gauge={
                    'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
                    'bar': {'color': color},
                    'bgcolor': "white",
                    'borderwidth': 2,
                    'bordercolor': "gray"
                },
                title={'text': title, 'font': {'size': 12}}
            ))
            
            fig.update_layout(
                width=size[0],
                height=size[1],
                paper_bgcolor=self.chart_config['background_color'],
                font_family=self.chart_config['font_family'],
                font_size=10,
                margin=dict(l=20, r=20, t=40, b=20)
            )
            
            return self.export_plotly_figure_to_base64(fig)
            
        except Exception as e:
            self.logger.error(f"Error creating mini gauge: {e}")
            return ""

    def create_confidence_distribution_chart(self, confidence_values: List[float], 
                                           title: str = "Confidence Distribution") -> str:
        """Create a histogram for confidence distribution."""
        try:
            fig = go.Figure()
            fig.add_trace(go.Histogram(
                x=confidence_values,
                nbinsx=10,
                marker_color=self.professional_colors['secondary'],
                marker_line=dict(color='white', width=1),
                opacity=0.7
            ))
            
            fig.update_layout(
                title=dict(
                    text=title,
                    font=dict(size=16, color=self.professional_colors['primary'])
                ),
                xaxis=dict(
                    title="Confidence Level",
                    tickfont=dict(size=10)
                ),
                yaxis=dict(
                    title="Frequency",
                    tickfont=dict(size=10)
                ),
                paper_bgcolor=self.chart_config['background_color'],
                font_family=self.chart_config['font_family'],
                font_size=self.chart_config['font_size'],
                margin=dict(l=50, r=50, t=80, b=80),
                showlegend=False
            )
            
            return self.export_plotly_figure_to_base64(fig)
            
        except Exception as e:
            self.logger.error(f"Error creating confidence distribution chart: {e}")
            return ""

    def create_pattern_type_distribution(self, pattern_counts: Dict[str, int], 
                                       title: str = "Pattern Type Distribution") -> str:
        """Create a chart showing distribution of fingerprint patterns."""
        try:
            labels = list(pattern_counts.keys())
            values = list(pattern_counts.values())
            
            fig = go.Figure(go.Bar(
                x=labels,
                y=values,
                marker_color=[self.professional_colors['secondary'], 
                            self.professional_colors['accent'],
                            self.professional_colors['success']][:len(labels)],
                marker_line=dict(color='white', width=1),
                text=values,
                textposition='auto',
                textfont=dict(size=12, color='white')
            ))
            
            fig.update_layout(
                title=dict(
                    text=title,
                    font=dict(size=16, color=self.professional_colors['primary'])
                ),
                xaxis=dict(
                    title="Pattern Types",
                    tickfont=dict(size=10)
                ),
                yaxis=dict(
                    title="Count",
                    tickfont=dict(size=10)
                ),
                paper_bgcolor=self.chart_config['background_color'],
                font_family=self.chart_config['font_family'],
                font_size=self.chart_config['font_size'],
                margin=dict(l=50, r=50, t=80, b=80),
                showlegend=False
            )
            
            return self.export_plotly_figure_to_base64(fig)
            
        except Exception as e:
            self.logger.error(f"Error creating pattern distribution chart: {e}")
            return ""

    def create_personality_bubble_chart(self, analysis_data: Dict[str, Any], 
                                      title: str = "Personality Traits Analysis") -> str:
        """Create a bubble chart for personality traits analysis."""
        try:
            # Sample personality data
            traits = ['Communication', 'Leadership', 'Problem Solving', 'Work Style', 'Learning']
            x_values = [75, 85, 90, 80, 88]  # Effectiveness scores
            y_values = [70, 80, 85, 75, 82]  # Adaptability scores
            sizes = [20, 25, 30, 22, 28]     # Importance weights
            labels = traits
            
            fig = go.Figure(data=[go.Scatter(
                x=x_values, 
                y=y_values, 
                mode='markers+text',
                marker=dict(
                    size=sizes, 
                    color=sizes, 
                    colorscale='Blues', 
                    showscale=True,
                    colorbar=dict(title="Importance")
                ),
                text=labels, 
                textposition="top center",
                textfont=dict(size=10)
            )])
            
            fig.update_layout(
                title=dict(
                    text=title,
                    font=dict(size=16, color=self.professional_colors['primary'])
                ),
                xaxis=dict(
                    title="Effectiveness Score",
                    range=[60, 100],
                    tickfont=dict(size=10)
                ),
                yaxis=dict(
                    title="Adaptability Score",
                    range=[60, 100],
                    tickfont=dict(size=10)
                ),
                paper_bgcolor=self.chart_config['background_color'],
                font_family=self.chart_config['font_family'],
                font_size=self.chart_config['font_size'],
                margin=dict(l=50, r=50, t=80, b=80)
            )
            
            return self.export_plotly_figure_to_base64(fig)
            
        except Exception as e:
            self.logger.error(f"Error creating personality bubble chart: {e}")
            return ""

    def create_development_progress_chart(self, analysis_data: Dict[str, Any], 
                                        title: str = "Development Progress") -> str:
        """Create a progress gauge for development roadmap."""
        try:
            # Calculate overall progress based on analysis data
            overall_score = analysis_data.get('overall_score', 75.0)
            
            return self.create_progress_gauge(overall_score, title)
            
        except Exception as e:
            self.logger.error(f"Error creating development progress chart: {e}")
            return ""

    def create_validation_grouped_chart(self, analysis_data: Dict[str, Any], 
                                      title: str = "Validation Metrics") -> str:
        """Create a grouped bar chart for validation metrics."""
        try:
            categories = ['Pattern Recognition', 'Ridge Count Accuracy', 'Intelligence Correlation', 'Statistical Significance', 'Cross-Validation']
            accuracy_values = [98.5, 96.2, 87.0, 99.9, 91.0]
            confidence_values = [95.0, 92.0, 85.0, 99.0, 88.0]
            
            fig = go.Figure()
            
            fig.add_trace(go.Bar(
                x=categories,
                y=accuracy_values,
                name='Accuracy',
                marker_color=self.professional_colors['success'],
                marker_line=dict(color='white', width=1),
                text=[f"{v:.1f}%" for v in accuracy_values],
                textposition='auto',
                textfont=dict(size=9, color='white')
            ))
            
            fig.add_trace(go.Bar(
                x=categories,
                y=confidence_values,
                name='Confidence',
                marker_color=self.professional_colors['secondary'],
                marker_line=dict(color='white', width=1),
                text=[f"{v:.1f}%" for v in confidence_values],
                textposition='auto',
                textfont=dict(size=9, color='white')
            ))
            
            fig.update_layout(
                barmode='group',
                title=dict(
                    text=title,
                    font=dict(size=16, color=self.professional_colors['primary'])
                ),
                xaxis=dict(
                    title="Validation Metrics",
                    tickangle=45,
                    tickfont=dict(size=10)
                ),
                yaxis=dict(
                    title="Percentage",
                    range=[0, 100],
                    tickfont=dict(size=10)
                ),
                paper_bgcolor=self.chart_config['background_color'],
                font_family=self.chart_config['font_family'],
                font_size=self.chart_config['font_size'],
                margin=dict(l=50, r=50, t=80, b=80),
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1
                )
            )
            
            return self.export_plotly_figure_to_base64(fig)
            
        except Exception as e:
            self.logger.error(f"Error creating validation grouped chart: {e}")
            return ""

    def create_extensions_pie_chart(self, analysis_data: Dict[str, Any], 
                                  title: str = "DMIT Extensions Analysis") -> str:
        """Create a pie chart for DMIT extensions analysis."""
        try:
            # Sample extensions data
            extensions = ['Adaptability & Resilience', 'Attention & Focus', 'Creativity & Innovation', 'Emotional Intelligence', 'Learning Efficiency']
            scores = [85, 78, 82, 75, 88]
            
            fig = go.Figure(go.Pie(
                labels=extensions,
                values=scores,
                marker_colors=[self.professional_colors['secondary'], 
                             self.professional_colors['accent'],
                             self.professional_colors['success'],
                             self.professional_colors['warning'],
                             self.professional_colors['info']],
                textinfo='label+percent',
                textfont=dict(size=10),
                hole=0.3
            ))
            
            fig.update_layout(
                title=dict(
                    text=title,
                    font=dict(size=16, color=self.professional_colors['primary'])
                ),
                paper_bgcolor=self.chart_config['background_color'],
                font_family=self.chart_config['font_family'],
                font_size=self.chart_config['font_size'],
                margin=dict(l=50, r=50, t=80, b=50),
                showlegend=True,
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1
                )
            )
            
            return self.export_plotly_figure_to_base64(fig)
            
        except Exception as e:
            self.logger.error(f"Error creating extensions pie chart: {e}")
            return ""

    def create_technical_line_chart(self, analysis_data: Dict[str, Any], 
                                  title: str = "Technical Analysis Trends") -> str:
        """Create a line chart for technical analysis trends."""
        try:
            # Sample technical data
            time_periods = ['Baseline', 'Month 1', 'Month 2', 'Month 3', 'Month 6', 'Month 12']
            pattern_accuracy = [85, 87, 89, 91, 93, 95]
            ridge_accuracy = [82, 84, 86, 88, 90, 92]
            correlation_strength = [0.75, 0.78, 0.81, 0.84, 0.87, 0.90]
            
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=time_periods,
                y=pattern_accuracy,
                mode='lines+markers',
                name='Pattern Accuracy',
                line=dict(color=self.professional_colors['success'], width=3),
                marker=dict(size=8)
            ))
            
            fig.add_trace(go.Scatter(
                x=time_periods,
                y=ridge_accuracy,
                mode='lines+markers',
                name='Ridge Accuracy',
                line=dict(color=self.professional_colors['secondary'], width=3),
                marker=dict(size=8)
            ))
            
            fig.add_trace(go.Scatter(
                x=time_periods,
                y=[v * 100 for v in correlation_strength],  # Scale to percentage
                mode='lines+markers',
                name='Correlation Strength',
                line=dict(color=self.professional_colors['accent'], width=3),
                marker=dict(size=8)
            ))
            
            fig.update_layout(
                title=dict(
                    text=title,
                    font=dict(size=16, color=self.professional_colors['primary'])
                ),
                xaxis=dict(
                    title="Time Period",
                    tickfont=dict(size=10)
                ),
                yaxis=dict(
                    title="Accuracy (%)",
                    range=[70, 100],
                    tickfont=dict(size=10)
                ),
                paper_bgcolor=self.chart_config['background_color'],
                font_family=self.chart_config['font_family'],
                font_size=self.chart_config['font_size'],
                margin=dict(l=50, r=50, t=80, b=80),
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1
                )
            )
            
            return self.export_plotly_figure_to_base64(fig)
            
        except Exception as e:
            self.logger.error(f"Error creating technical line chart: {e}")
            return "" 