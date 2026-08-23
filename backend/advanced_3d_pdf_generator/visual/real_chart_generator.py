#!/usr/bin/env python3
"""
Real 3D Chart Generator - Uses ONLY Real Pipeline Data
Version: 4.0 - Full chart suite for all extensions
"""

import logging
import base64
import io
from typing import Dict, Any, List, Optional
import numpy as np

try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    from matplotlib.gridspec import GridSpec
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False

try:
    import plotly.graph_objects as go
    import plotly.express as px
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False

logger = logging.getLogger(__name__)

# Colour palette
PALETTE = {
    'primary':   '#3498DB',
    'secondary': '#E74C3C',
    'success':   '#27AE60',
    'warning':   '#F39C12',
    'purple':    '#8E44AD',
    'teal':      '#16A085',
    'navy':      '#2C3E50',
    'light':     '#ECF0F1',
    'accent':    '#E67E22',
}

GRADIENT = ['#2980B9', '#27AE60', '#8E44AD', '#E74C3C', '#F39C12',
            '#16A085', '#2C3E50', '#E67E22', '#1ABC9C', '#D35400',
            '#C0392B', '#2ECC71']


def _to_b64(fig: 'plt.Figure') -> str:
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=150, bbox_inches='tight',
                facecolor=fig.get_facecolor())
    buf.seek(0)
    result = base64.b64encode(buf.getvalue()).decode('utf-8')
    plt.close(fig)
    return result


def _label(key: str) -> str:
    """Convert snake_case to Title Case label."""
    return key.replace('_', ' ').title()


class Real3DChartGenerator:
    """Generates all charts from real DMIT pipeline data."""

    def __init__(self):
        if not MATPLOTLIB_AVAILABLE and not PLOTLY_AVAILABLE:
            raise ImportError("matplotlib or plotly required")

    # ------------------------------------------------------------------ #
    #  MAIN ENTRY — generate everything                                    #
    # ------------------------------------------------------------------ #

    def generate_all_3d_charts(self, real_data: Dict[str, Any]) -> Dict[str, str]:
        charts = {}
        try:
            if real_data.get('intelligence_scores'):
                charts['intelligence_radar_3d'] = self.create_3d_intelligence_radar(
                    real_data['intelligence_scores'])
                charts['intelligence_bar'] = self.create_intelligence_bar(
                    real_data['intelligence_scores'])

            if real_data.get('brain_mapping'):
                charts['brain_mapping_3d'] = self.create_3d_brain_mapping(
                    real_data['brain_mapping'])
                charts['brain_bar'] = self.create_brain_bar(
                    real_data['brain_mapping'])

            if real_data.get('learning_styles'):
                charts['learning_styles_pie'] = self.create_learning_styles_pie(
                    real_data['learning_styles'])

            if real_data.get('personality_behavior'):
                charts['personality_bar'] = self.create_personality_bar(
                    real_data['personality_behavior'])

            if real_data.get('extension_results'):
                charts['eq_radar'] = self.create_eq_radar(
                    real_data['extension_results'])
                charts['cognitive_bar'] = self.create_cognitive_grouped_bar(
                    real_data['extension_results'])
                charts['social_bar'] = self.create_social_grouped_bar(
                    real_data['extension_results'])
                charts['motivation_bar'] = self.create_motivation_grouped_bar(
                    real_data['extension_results'])
                charts['specialized_bar'] = self.create_specialized_bar(
                    real_data['extension_results'])
                charts['career_bar'] = self.create_career_life_bar(
                    real_data['extension_results'])
                charts['extensions_overview'] = self.create_extensions_overview(
                    real_data['extension_results'])

            if real_data.get('per_finger_data'):
                charts['finger_pattern_bar'] = self.create_finger_pattern_bar(
                    real_data['per_finger_data'])

            logger.info(f"Generated {len(charts)} charts")
        except Exception as e:
            logger.exception(f"Error generating charts: {e}")
        return charts

    # ------------------------------------------------------------------ #
    #  INTELLIGENCE RADAR  (Matplotlib polar)                              #
    # ------------------------------------------------------------------ #

    def create_3d_intelligence_radar(self, scores: Dict[str, float]) -> str:
        if not scores or not MATPLOTLIB_AVAILABLE:
            return ''
        try:
            labels = [_label(k) for k in scores]
            vals = list(scores.values())
            N = len(labels)
            angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
            vals_plot = vals + [vals[0]]
            angles_plot = angles + [angles[0]]

            fig, ax = plt.subplots(figsize=(8, 7), subplot_kw=dict(polar=True),
                                   facecolor='#1a1a2e')
            ax.set_facecolor('#16213e')
            ax.plot(angles_plot, vals_plot, 'o-', linewidth=2.5,
                    color=PALETTE['primary'])
            ax.fill(angles_plot, vals_plot, alpha=0.30, color=PALETTE['primary'])
            ax.set_thetagrids(np.degrees(angles), labels, fontsize=9,
                              color='white')
            ax.set_ylim(0, 1)
            ax.set_yticks([0.2, 0.4, 0.6, 0.8, 1.0])
            ax.set_yticklabels(['20%', '40%', '60%', '80%', '100%'],
                               fontsize=7, color='#aaaaaa')
            ax.grid(color='#444466', linewidth=0.5)
            ax.set_title('Multiple Intelligence Profile', color='white',
                         fontsize=14, fontweight='bold', pad=20)
            return _to_b64(fig)
        except Exception as e:
            logger.exception(f"Radar chart error: {e}")
            return ''

    # ------------------------------------------------------------------ #
    #  INTELLIGENCE BAR                                                    #
    # ------------------------------------------------------------------ #

    def create_intelligence_bar(self, scores: Dict[str, float]) -> str:
        if not scores or not MATPLOTLIB_AVAILABLE:
            return ''
        try:
            sorted_items = sorted(scores.items(), key=lambda x: x[1], reverse=True)
            labels = [_label(k) for k, _ in sorted_items]
            vals = [v * 100 for _, v in sorted_items]
            colours = [GRADIENT[i % len(GRADIENT)] for i in range(len(labels))]

            fig, ax = plt.subplots(figsize=(10, 5), facecolor='#1a1a2e')
            ax.set_facecolor('#16213e')
            bars = ax.barh(labels, vals, color=colours, height=0.6,
                           edgecolor='none')
            for bar, val in zip(bars, vals):
                ax.text(bar.get_width() + 0.8, bar.get_y() + bar.get_height() / 2,
                        f'{val:.1f}%', va='center', fontsize=9, color='white')
            ax.set_xlim(0, 110)
            ax.set_xlabel('Score (%)', color='white', fontsize=10)
            ax.set_title('Intelligence Scores — Ranked', color='white',
                         fontsize=13, fontweight='bold')
            ax.tick_params(colors='white', labelsize=9)
            ax.spines[:].set_visible(False)
            ax.axvline(x=50, color='#555577', linestyle='--', linewidth=0.8,
                       label='50% baseline')
            fig.tight_layout()
            return _to_b64(fig)
        except Exception as e:
            logger.exception(f"Intelligence bar error: {e}")
            return ''

    # ------------------------------------------------------------------ #
    #  BRAIN MAPPING                                                       #
    # ------------------------------------------------------------------ #

    def create_3d_brain_mapping(self, brain: Dict[str, float]) -> str:
        return self.create_brain_bar(brain)

    def create_brain_bar(self, brain: Dict[str, float]) -> str:
        if not brain or not MATPLOTLIB_AVAILABLE:
            return ''
        try:
            items = list(brain.items())
            labels = [_label(k) for k, _ in items]
            vals = [v * 100 for _, v in items]
            colours = [PALETTE['secondary'] if 'right' in k else PALETTE['primary']
                       for k, _ in items]

            fig, ax = plt.subplots(figsize=(9, 5), facecolor='#1a1a2e')
            ax.set_facecolor('#16213e')
            bars = ax.bar(labels, vals, color=colours, width=0.6, edgecolor='none')
            for bar, val in zip(bars, vals):
                ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1,
                        f'{val:.0f}%', ha='center', fontsize=9, color='white')
            ax.set_ylim(0, 110)
            ax.set_ylabel('Activity Level (%)', color='white', fontsize=10)
            ax.set_title('Brain Region Activity Map', color='white',
                         fontsize=13, fontweight='bold')
            ax.tick_params(colors='white', labelsize=8)
            ax.spines[:].set_visible(False)
            plt.xticks(rotation=25, ha='right')
            fig.tight_layout()
            return _to_b64(fig)
        except Exception as e:
            logger.exception(f"Brain bar error: {e}")
            return ''

    # ------------------------------------------------------------------ #
    #  LEARNING STYLES PIE                                                 #
    # ------------------------------------------------------------------ #

    def create_3d_learning_styles(self, learning_styles: Dict[str, float]) -> str:
        return self.create_learning_styles_pie(learning_styles)

    def create_learning_styles_pie(self, learning_styles: Dict[str, float]) -> str:
        if not learning_styles or not MATPLOTLIB_AVAILABLE:
            return ''
        try:
            labels = [_label(k) for k in learning_styles]
            sizes = list(learning_styles.values())
            colours = [PALETTE['primary'], PALETTE['success'], PALETTE['warning']][:len(labels)]

            fig, (ax_pie, ax_bar) = plt.subplots(1, 2, figsize=(11, 5),
                                                  facecolor='#1a1a2e')
            ax_pie.set_facecolor('#16213e')
            ax_bar.set_facecolor('#16213e')

            wedges, texts, autotexts = ax_pie.pie(
                sizes, labels=labels, colors=colours, autopct='%1.1f%%',
                startangle=90, pctdistance=0.75,
                wedgeprops=dict(edgecolor='#1a1a2e', linewidth=2))
            for t in texts:
                t.set_color('white')
                t.set_fontsize(10)
            for at in autotexts:
                at.set_color('white')
                at.set_fontweight('bold')
            ax_pie.set_title('Learning Style Distribution', color='white',
                             fontsize=12, fontweight='bold')

            bars = ax_bar.barh(labels, [v * 100 for v in sizes],
                               color=colours, height=0.5, edgecolor='none')
            for bar, val in zip(bars, sizes):
                ax_bar.text(bar.get_width() + 1, bar.get_y() + bar.get_height() / 2,
                            f'{val*100:.1f}%', va='center', color='white', fontsize=10)
            ax_bar.set_xlim(0, 110)
            ax_bar.tick_params(colors='white', labelsize=10)
            ax_bar.spines[:].set_visible(False)
            ax_bar.set_title('Learning Style Scores', color='white',
                             fontsize=12, fontweight='bold')
            fig.tight_layout()
            return _to_b64(fig)
        except Exception as e:
            logger.exception(f"Learning styles chart error: {e}")
            return ''

    # ------------------------------------------------------------------ #
    #  PERSONALITY (Big-5) HORIZONTAL BAR                                 #
    # ------------------------------------------------------------------ #

    def create_3d_personality_analysis(self, personality_data: Dict[str, float]) -> str:
        return self.create_personality_bar(personality_data)

    def create_personality_bar(self, personality: Dict[str, float]) -> str:
        if not personality or not MATPLOTLIB_AVAILABLE:
            return ''
        try:
            trait_colours = {
                'openness': '#8E44AD',
                'conscientiousness': '#27AE60',
                'extraversion': '#E67E22',
                'agreeableness': '#3498DB',
                'neuroticism': '#E74C3C',
            }
            items = list(personality.items())
            labels = [_label(k) for k, _ in items]
            vals = [v * 100 for _, v in items]
            colours = [trait_colours.get(k, PALETTE['primary']) for k, _ in items]

            fig, ax = plt.subplots(figsize=(10, 5), facecolor='#1a1a2e')
            ax.set_facecolor('#16213e')
            bars = ax.barh(labels, vals, color=colours, height=0.55, edgecolor='none')
            for bar, val in zip(bars, vals):
                ax.text(bar.get_width() + 1, bar.get_y() + bar.get_height() / 2,
                        f'{val:.1f}%', va='center', color='white', fontsize=10)
            ax.set_xlim(0, 115)
            ax.axvline(x=50, color='#555577', linestyle='--', linewidth=0.8)
            ax.set_xlabel('Score (%)', color='white', fontsize=10)
            ax.set_title('Big-5 Personality Profile', color='white',
                         fontsize=13, fontweight='bold')
            ax.tick_params(colors='white', labelsize=10)
            ax.spines[:].set_visible(False)
            fig.tight_layout()
            return _to_b64(fig)
        except Exception as e:
            logger.exception(f"Personality bar error: {e}")
            return ''

    # ------------------------------------------------------------------ #
    #  EQ RADAR (8 sub-dimensions)                                        #
    # ------------------------------------------------------------------ #

    def create_eq_radar(self, extension_results: Dict[str, Any]) -> str:
        if not MATPLOTLIB_AVAILABLE:
            return ''
        try:
            eq = extension_results.get('EmotionalIntelligenceExtension', {})
            if not eq or isinstance(eq, dict) and 'error' in eq:
                return ''

            sub_keys = ['emotional_awareness', 'emotional_regulation', 'empathy',
                        'social_skills', 'emotional_expression', 'emotional_memory',
                        'emotional_processing', 'emotional_resilience']
            labels = [_label(k) for k in sub_keys]
            vals = [float(eq.get(k, 0.0) or 0.0) for k in sub_keys]

            N = len(labels)
            angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
            v_plot = vals + [vals[0]]
            a_plot = angles + [angles[0]]

            fig, ax = plt.subplots(figsize=(7, 7), subplot_kw=dict(polar=True),
                                   facecolor='#1a1a2e')
            ax.set_facecolor('#16213e')
            ax.plot(a_plot, v_plot, 'o-', linewidth=2.5, color='#E74C3C')
            ax.fill(a_plot, v_plot, alpha=0.28, color='#E74C3C')
            ax.set_thetagrids(np.degrees(angles), labels, fontsize=8, color='white')
            ax.set_ylim(0, 1)
            ax.set_yticks([0.25, 0.5, 0.75, 1.0])
            ax.set_yticklabels(['25%', '50%', '75%', '100%'], fontsize=7, color='#aaaaaa')
            ax.grid(color='#444466', linewidth=0.5)
            ax.set_title('Emotional Intelligence — 8 Dimensions', color='white',
                         fontsize=13, fontweight='bold', pad=20)
            return _to_b64(fig)
        except Exception as e:
            logger.exception(f"EQ radar error: {e}")
            return ''

    # ------------------------------------------------------------------ #
    #  EXTENSIONS OVERVIEW — bar chart of all main scores                 #
    # ------------------------------------------------------------------ #

    def create_extensions_overview(self, extension_results: Dict[str, Any]) -> str:
        if not extension_results or not MATPLOTLIB_AVAILABLE:
            return ''
        try:
            from advanced_3d_pdf_generator.core.real_data_processor import _find_main_score, EXTENSION_DISPLAY_NAMES
            scores = {}
            for ext_name, ext_data in extension_results.items():
                if isinstance(ext_data, dict) and 'error' not in ext_data:
                    score = _find_main_score(ext_data)
                    display = EXTENSION_DISPLAY_NAMES.get(ext_name, _label(ext_name.replace('Extension', '')))
                    scores[display] = score

            if not scores:
                return ''

            sorted_items = sorted(scores.items(), key=lambda x: x[1], reverse=True)
            labels = [k for k, _ in sorted_items]
            vals = [v * 100 for _, v in sorted_items]
            colours = [GRADIENT[i % len(GRADIENT)] for i in range(len(labels))]

            fig, ax = plt.subplots(figsize=(12, max(6, len(labels) * 0.35 + 1)),
                                   facecolor='#1a1a2e')
            ax.set_facecolor('#16213e')
            bars = ax.barh(labels, vals, color=colours, height=0.65, edgecolor='none')
            for bar, val in zip(bars, vals):
                ax.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height() / 2,
                        f'{val:.0f}%', va='center', fontsize=8, color='white')
            ax.set_xlim(0, 115)
            ax.axvline(x=50, color='#555577', linestyle='--', linewidth=0.8)
            ax.set_xlabel('Score (%)', color='white', fontsize=10)
            ax.set_title('All Extensions — Score Overview', color='white',
                         fontsize=13, fontweight='bold')
            ax.tick_params(colors='white', labelsize=8)
            ax.spines[:].set_visible(False)
            fig.tight_layout()
            return _to_b64(fig)
        except Exception as e:
            logger.exception(f"Extensions overview error: {e}")
            return ''

    # ------------------------------------------------------------------ #
    #  GROUPED BAR HELPERS                                                 #
    # ------------------------------------------------------------------ #

    def _create_grouped_bar(self, extension_results: Dict[str, Any],
                            group_keys: List[str], title: str,
                            colour: str) -> str:
        if not MATPLOTLIB_AVAILABLE:
            return ''
        try:
            from advanced_3d_pdf_generator.core.real_data_processor import _find_main_score, EXTENSION_DISPLAY_NAMES
            data = {}
            for key in group_keys:
                ext_data = extension_results.get(key, {})
                if isinstance(ext_data, dict) and 'error' not in ext_data:
                    score = _find_main_score(ext_data)
                    display = EXTENSION_DISPLAY_NAMES.get(key, _label(key.replace('Extension', '')))
                    data[display] = score

            if not data:
                return ''

            labels = list(data.keys())
            vals = [v * 100 for v in data.values()]
            shades = [colour] * len(labels)

            fig, ax = plt.subplots(figsize=(10, max(4, len(labels) * 0.55 + 1)),
                                   facecolor='#1a1a2e')
            ax.set_facecolor('#16213e')
            bars = ax.barh(labels, vals, color=shades, height=0.6, edgecolor='none')
            for bar, val in zip(bars, vals):
                ax.text(bar.get_width() + 0.8, bar.get_y() + bar.get_height() / 2,
                        f'{val:.0f}%', va='center', fontsize=9, color='white')
            ax.set_xlim(0, 115)
            ax.axvline(x=50, color='#555577', linestyle='--', linewidth=0.8)
            ax.set_xlabel('Score (%)', color='white', fontsize=10)
            ax.set_title(title, color='white', fontsize=12, fontweight='bold')
            ax.tick_params(colors='white', labelsize=9)
            ax.spines[:].set_visible(False)
            fig.tight_layout()
            return _to_b64(fig)
        except Exception as e:
            logger.exception(f"Grouped bar '{title}' error: {e}")
            return ''

    def create_cognitive_grouped_bar(self, ext: Dict[str, Any]) -> str:
        return self._create_grouped_bar(ext, [
            'DecisionMakingExtension', 'AttentionFocusExtension',
            'MemoryProcessingExtension', 'ExecutiveFunctionExtension',
            'CognitiveLoadExtension', 'MetaCognitionExtension', 'LearningAgilityExtension'
        ], 'Cognitive Abilities Suite', PALETTE['primary'])

    def create_social_grouped_bar(self, ext: Dict[str, Any]) -> str:
        return self._create_grouped_bar(ext, [
            'LeadershipPotentialExtension', 'CommunicationStyleExtension',
            'InterpersonalIntelligenceExtension', 'SocialAwarenessExtension',
            'RelationshipDynamicsExtension', 'LeftRightBrainExtension'
        ], 'Social & Leadership Profile', PALETTE['teal'])

    def create_motivation_grouped_bar(self, ext: Dict[str, Any]) -> str:
        return self._create_grouped_bar(ext, [
            'CreativityIndexExtension', 'InnovationIntelligenceExtension',
            'EntrepreneurialAptitudeExtension', 'RiskToleranceExtension',
            'CuriosityExploratoryExtension', 'PersistenceGritExtension',
            'MotivationDriveExtension'
        ], 'Motivation, Creativity & Innovation', PALETTE['purple'])

    def create_specialized_bar(self, ext: Dict[str, Any]) -> str:
        return self._create_grouped_bar(ext, [
            'LinguisticIntelligenceExtension', 'LogicalMathematicalIntelligenceExtension',
            'SpatialIntelligenceExtension', 'MusicalIntelligenceExtension',
            'BodilyKinestheticIntelligenceExtension', 'IntrapersonalIntelligenceExtension',
            'NaturalisticIntelligenceExtension', 'SystemsThinkingExtension',
            'PatternRecognitionExtension', 'WellnessIntelligenceExtension',
            'SustainabilityIntelligenceExtension'
        ], 'Specialised Intelligence Scores', PALETTE['success'])

    def create_career_life_bar(self, ext: Dict[str, Any]) -> str:
        return self._create_grouped_bar(ext, [
            'StressResponseExtension', 'AdaptabilityResilienceExtension',
            'SelfRegulationExtension', 'HealthWellnessExtension',
            'FinancialIntelligenceExtension', 'DigitalIntelligenceExtension',
            'CulturalIntelligenceExtension', 'NeurodivergenceExtension'
        ], 'Career & Life Intelligence', PALETTE['accent'])

    def create_3d_career_landscape(self, intelligence_scores: Dict[str, float]) -> str:
        return self.create_intelligence_bar(intelligence_scores)

    # ------------------------------------------------------------------ #
    #  FINGER PATTERN DISTRIBUTION BAR                                    #
    # ------------------------------------------------------------------ #

    def create_finger_pattern_bar(self, per_finger_data: List[Dict[str, Any]]) -> str:
        if not per_finger_data or not MATPLOTLIB_AVAILABLE:
            return ''
        try:
            from collections import Counter
            patterns = [f.get('pattern_type', 'Unknown') for f in per_finger_data]
            count = Counter(patterns)
            labels = list(count.keys())
            vals = list(count.values())
            colours_map = {'Arch': '#E74C3C', 'Loop': '#3498DB',
                           'Whorl': '#27AE60', 'Composite': '#F39C12',
                           'Unknown': '#7F8C8D'}
            colours = [colours_map.get(l, PALETTE['primary']) for l in labels]

            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5), facecolor='#1a1a2e')
            ax1.set_facecolor('#16213e')
            ax2.set_facecolor('#16213e')

            # Pie
            wedges, texts, autotexts = ax1.pie(
                vals, labels=labels, colors=colours, autopct='%1.0f%%',
                startangle=90, wedgeprops=dict(edgecolor='#1a1a2e', linewidth=2))
            for t in texts:
                t.set_color('white')
            for at in autotexts:
                at.set_color('white')
                at.set_fontweight('bold')
            ax1.set_title('Pattern Distribution (10 Fingers)', color='white',
                          fontsize=12, fontweight='bold')

            # Per-finger quality bar
            fingers = [f.get('finger_type', f'F{f["index"]}') for f in per_finger_data]
            quality = [f.get('image_quality', 0.0) * 100 for f in per_finger_data]
            bar_colours = [colours_map.get(f.get('pattern_type', 'Unknown'), PALETTE['primary'])
                           for f in per_finger_data]
            bars = ax2.bar(range(len(fingers)), quality, color=bar_colours,
                           width=0.65, edgecolor='none')
            for bar, val in zip(bars, quality):
                ax2.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1,
                         f'{val:.0f}%', ha='center', fontsize=8, color='white')
            ax2.set_xticks(range(len(fingers)))
            ax2.set_xticklabels(fingers, rotation=30, ha='right', fontsize=8, color='white')
            ax2.set_ylim(0, 115)
            ax2.set_ylabel('Image Quality (%)', color='white', fontsize=9)
            ax2.set_title('Per-Finger Image Quality', color='white',
                          fontsize=12, fontweight='bold')
            ax2.tick_params(colors='white', labelsize=8)
            ax2.spines[:].set_visible(False)

            # Legend
            legend_patches = [mpatches.Patch(color=v, label=k)
                              for k, v in colours_map.items() if k in labels]
            ax2.legend(handles=legend_patches, loc='upper right', fontsize=8,
                       facecolor='#1a1a2e', labelcolor='white', edgecolor='none')
            fig.tight_layout()
            return _to_b64(fig)
        except Exception as e:
            logger.exception(f"Finger pattern bar error: {e}")
            return ''