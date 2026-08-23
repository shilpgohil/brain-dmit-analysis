"""
Premium DMIT Report - Chart Generator
======================================
All matplotlib charts styled for ivory/gold light theme.
Circular gauges use Style E: gradient glow arc with rounded linecap.
No em dashes anywhere in labels.
"""

import io
import base64
import math
import logging
from typing import Dict, Any, List, Optional, Tuple

import numpy as np

try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    from matplotlib.patches import FancyArrowPatch, Arc, FancyBboxPatch
    from matplotlib.gridspec import GridSpec
    from matplotlib.colors import LinearSegmentedColormap
    import matplotlib.patheffects as pe
    MPL = True
except ImportError:
    MPL = False

from .theme import HEX

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _fig_to_b64(fig) -> str:
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=150, bbox_inches='tight',
                facecolor=fig.get_facecolor())
    buf.seek(0)
    b64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    plt.close(fig)
    return b64


def _ivory_fig(w: float, h: float):
    fig = plt.figure(figsize=(w, h), facecolor=HEX['ivory'])
    return fig


def _ivory_ax(fig, *args, **kwargs):
    ax = fig.add_subplot(*args, **kwargs)
    ax.set_facecolor(HEX['cream_alt'])
    return ax


def _label(key: str) -> str:
    return key.replace('_', ' ').title()


def _wrap(text: str, width: int = 14) -> str:
    """Wrap long labels for chart axes."""
    words = text.split()
    lines, cur = [], []
    for w in words:
        if sum(len(x) for x in cur) + len(cur) + len(w) > width:
            lines.append(' '.join(cur))
            cur = [w]
        else:
            cur.append(w)
    if cur:
        lines.append(' '.join(cur))
    return '\n'.join(lines)


# ---------------------------------------------------------------------------
# Style E: Gradient Glow Arc Gauge
# ---------------------------------------------------------------------------

def create_gauge(score: float, label: str, size: float = 2.2) -> str:
    """
    Single circular gauge - Style E.
    Gradient arc from gold_light to gold, soft glow at endpoint, rounded caps.
    """
    if not MPL:
        return ''
    fig, ax = plt.subplots(figsize=(size, size + 0.35),
                           subplot_kw=dict(aspect='equal'),
                           facecolor=HEX['ivory'])
    ax.set_facecolor(HEX['ivory'])
    ax.set_xlim(-1.3, 1.3)
    ax.set_ylim(-1.3, 1.55)
    ax.axis('off')

    start_angle = 225   # degrees (bottom-left)
    total_sweep = 270   # degrees

    # Background track ring
    theta = np.linspace(np.radians(start_angle),
                        np.radians(start_angle - total_sweep), 300)
    ax.plot(np.cos(theta), np.sin(theta),
            color=HEX['gold_light'], linewidth=10, alpha=0.35,
            solid_capstyle='round')

    # Gradient arc (simulate with colour segments)
    pct = max(0.01, min(1.0, score))
    n_segs = 180
    seg_count = max(1, int(pct * n_segs))
    gold_light = np.array([0xe8/255, 0xd5/255, 0xa3/255])
    gold_bright = np.array([0xc9/255, 0xa4/255, 0x41/255])

    for i in range(seg_count):
        t = i / max(1, n_segs - 1)
        c = tuple(gold_light + t * (gold_bright - gold_light))
        a0 = np.radians(start_angle - (i / n_segs) * total_sweep)
        a1 = np.radians(start_angle - ((i + 1) / n_segs) * total_sweep)
        th = np.linspace(a0, a1, 8)
        lw = 10
        ax.plot(np.cos(th), np.sin(th), color=c, linewidth=lw,
                solid_capstyle='round' if i == 0 or i == seg_count - 1 else 'butt')

    # Glow dot at arc endpoint
    end_angle = np.radians(start_angle - pct * total_sweep)
    ex, ey = np.cos(end_angle), np.sin(end_angle)
    ax.scatter([ex], [ey], s=220, color=HEX['gold'], zorder=5,
               edgecolors=HEX['gold_light'], linewidths=2)
    # halo
    ax.scatter([ex], [ey], s=520, color=HEX['gold_pale'], zorder=4, alpha=0.4)

    # Percentage text
    pct_str = f"{int(round(score * 100))}%"
    ax.text(0, 0.08, pct_str, ha='center', va='center',
            fontsize=size * 9.5, fontweight='bold',
            color=HEX['navy'], fontfamily='serif')

    # Label below
    ax.text(0, -1.1, label, ha='center', va='center',
            fontsize=size * 4.0, color=HEX['grey_text'],
            fontfamily='serif', wrap=True)

    return _fig_to_b64(fig)


def create_gauge_grid(scores: Dict[str, float], cols: int = 4) -> str:
    """
    Multi-gauge grid. scores = {label: value (0-1)}.
    Returns a wide base64 PNG.
    """
    if not MPL or not scores:
        return ''
    items = list(scores.items())
    # Clamp the grid to the number of gauges actually supplied. Sizing the
    # figure for a fixed 4-column grid while only populating 2 subplots left
    # 2 empty columns; savefig's bbox_inches='tight' then cropped tight
    # around just the populated gauges, collapsing a 4-wide figure down to a
    # 2-wide one. chart_image() always stretches the resulting PNG to fill
    # ~full page width regardless of its native crop, so that 2-gauge image
    # got magnified far taller than intended (a squarish 2-across crop
    # blown up to full page width), blowing out the whole dashboard's total
    # height and forcing shrink_block to scale every font on the page down
    # by ~35% to compensate. Matching cols to the real item count keeps the
    # figure's aspect ratio (and therefore its embedded height) predictable
    # no matter how many gauges happen to have data.
    cols = max(1, min(cols, len(items)))
    rows = math.ceil(len(items) / cols)
    fig_w = cols * 2.4
    fig_h = rows * 2.8
    fig = plt.figure(figsize=(fig_w, fig_h), facecolor=HEX['ivory'])

    for idx, (lbl, val) in enumerate(items):
        ax = fig.add_subplot(rows, cols, idx + 1, aspect='equal')
        ax.set_facecolor(HEX['ivory'])
        ax.set_xlim(-1.3, 1.3)
        ax.set_ylim(-1.4, 1.4)
        ax.axis('off')

        start_angle = 225
        total_sweep = 270

        theta = np.linspace(np.radians(start_angle),
                            np.radians(start_angle - total_sweep), 300)
        ax.plot(np.cos(theta), np.sin(theta),
                color=HEX['gold_light'], linewidth=9, alpha=0.35,
                solid_capstyle='round')

        pct = max(0.01, min(1.0, val))
        n_segs = 150
        seg_count = max(1, int(pct * n_segs))
        gold_l = np.array([0xe8/255, 0xd5/255, 0xa3/255])
        gold_b = np.array([0xc9/255, 0xa4/255, 0x41/255])
        for i in range(seg_count):
            t = i / max(1, n_segs - 1)
            c = tuple(gold_l + t * (gold_b - gold_l))
            a0 = np.radians(start_angle - (i / n_segs) * total_sweep)
            a1 = np.radians(start_angle - ((i + 1) / n_segs) * total_sweep)
            th = np.linspace(a0, a1, 6)
            cap = 'round' if (i == 0 or i == seg_count - 1) else 'butt'
            ax.plot(np.cos(th), np.sin(th), color=c, linewidth=9,
                    solid_capstyle=cap)

        end_angle = np.radians(start_angle - pct * total_sweep)
        ex, ey = np.cos(end_angle), np.sin(end_angle)
        ax.scatter([ex], [ey], s=160, color=HEX['gold'], zorder=5,
                   edgecolors=HEX['gold_light'], linewidths=1.5)
        ax.scatter([ex], [ey], s=380, color=HEX['gold_pale'], zorder=4, alpha=0.35)

        ax.text(0, 0.10, f"{int(round(val * 100))}%",
                ha='center', va='center', fontsize=17,
                fontweight='bold', color=HEX['navy'], fontfamily='serif')
        # This grid is always embedded at ~70% of its native figure width
        # (chart_image() fits it to content width, but the figure itself is
        # sized wider than that to accommodate up to 4 gauges), so on-page
        # the label prints far smaller than its nominal matplotlib fontsize
        # — a fontsize=6.5 label was rendering under 5pt effective, much
        # smaller than any surrounding body text. Bumping the source
        # fontsize compensates for that display-time downscale so the
        # printed label matches normal caption-sized text (~8pt). Wrapping
        # onto two lines (instead of a mid-word "..' truncation) keeps
        # longer labels fully readable rather than cut off.
        ax.text(0, -1.05, _wrap(lbl, 13), ha='center', va='center',
                fontsize=10.5, color=HEX['grey_text'], fontfamily='serif')

    fig.tight_layout(pad=0.3)
    return _fig_to_b64(fig)


# ---------------------------------------------------------------------------
# Intelligence Radar
# ---------------------------------------------------------------------------

def create_intelligence_radar(scores: Dict[str, float]) -> str:
    if not MPL or not scores:
        return ''
    labels = [_wrap(_label(k)) for k in scores]
    vals = list(scores.values())
    N = len(vals)
    angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
    vals_plot = vals + [vals[0]]
    angles_plot = angles + [angles[0]]

    fig, ax = plt.subplots(figsize=(6, 5.5), subplot_kw=dict(polar=True),
                           facecolor=HEX['ivory'])
    ax.set_facecolor(HEX['cream_alt'])
    # Outer glow fill first, then sharp line on top
    ax.fill(angles_plot, vals_plot, alpha=0.18, color=HEX['gold'])
    ax.fill(angles_plot, vals_plot, alpha=0.10, color=HEX['gold_light'])
    ax.plot(angles_plot, vals_plot, 'o-', linewidth=2.5,
            color=HEX['gold'], markerfacecolor=HEX['gold_dark'],
            markeredgecolor=HEX['ivory'], markersize=5)
    ax.set_thetagrids(np.degrees(angles), labels,
                      fontsize=8, color=HEX['navy'], fontfamily='serif',
                      fontweight='bold')
    ax.set_ylim(0, 1)
    ax.set_yticks([0.25, 0.5, 0.75, 1.0])
    ax.set_yticklabels(['25%', '50%', '75%', '100%'],
                       fontsize=6.5, color=HEX['grey_text'])
    ax.grid(color=HEX['gold_light'], linewidth=0.6, alpha=0.6)
    ax.spines['polar'].set_color(HEX['gold'])
    ax.spines['polar'].set_linewidth(1.5)
    ax.set_title('Intelligence Profile Radar', color=HEX['navy'],
                 fontsize=11, fontfamily='serif', pad=16, fontweight='bold')
    return _fig_to_b64(fig)


# ---------------------------------------------------------------------------
# Intelligence ranked horizontal bar
# ---------------------------------------------------------------------------

def create_intelligence_bar(scores: Dict[str, float]) -> str:
    if not MPL or not scores:
        return ''
    sorted_items = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    labels = [_label(k) for k, _ in sorted_items]
    vals = [v * 100 for _, v in sorted_items]

    fig, ax = plt.subplots(figsize=(7, 0.55 * len(labels) + 0.8),
                           facecolor=HEX['ivory'])
    ax.set_facecolor(HEX['cream_alt'])

    bar_colors = []
    for v in vals:
        if v >= 75: bar_colors.append(HEX['gold'])
        elif v >= 55: bar_colors.append(HEX['sage'])
        else: bar_colors.append(HEX['terracotta'])

    # Background track bars
    ax.barh(labels, [100] * len(vals), height=0.55,
            color=HEX['gold_pale'], alpha=0.4, edgecolor='none', zorder=1)
    bars = ax.barh(labels, vals, color=bar_colors, height=0.55,
                   edgecolor='none', zorder=2, alpha=0.9)
    for bar, val in zip(bars, vals):
        ax.text(min(bar.get_width() + 1.5, 109),
                bar.get_y() + bar.get_height() / 2,
                f'{val:.0f}%', va='center', fontsize=8.5,
                color=HEX['navy'], fontfamily='serif', fontweight='bold')

    ax.set_xlim(0, 114)
    ax.set_xlabel('Score (%)', color=HEX['navy'], fontsize=9, fontfamily='serif')
    ax.tick_params(colors=HEX['navy'], labelsize=8.5)
    for tick in ax.get_yticklabels():
        tick.set_fontfamily('serif')
        tick.set_color(HEX['navy'])
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_color(HEX['gold_light'])
    ax.spines['left'].set_color(HEX['gold_light'])
    ax.axvline(50, color=HEX['gold_light'], linewidth=0.8, linestyle='--',
               alpha=0.6, zorder=0)
    ax.set_title('Intelligence Scores - Ranked', color=HEX['navy'],
                 fontsize=10, fontfamily='serif', fontweight='bold', pad=8)
    fig.tight_layout()
    return _fig_to_b64(fig)


# ---------------------------------------------------------------------------
# Brain lobe bar chart
# ---------------------------------------------------------------------------

def create_brain_lobe_bar(brain_mapping: Dict[str, float]) -> str:
    if not MPL or not brain_mapping:
        return ''
    all_keys = ['prefrontal_lobe', 'posterior_frontal', 'parietal_lobe',
                'temporal_lobe', 'occipital_lobe']
    all_labels = ['Prefrontal', 'Posterior Frontal', 'Parietal',
                  'Temporal', 'Occipital']
    all_colors = [HEX['gold'], HEX['navy'], HEX['sage'],
                  HEX['plum'], HEX['terracotta']]
    # Real-data policy: lobes without a measurement are omitted from the chart
    # instead of being drawn as a fabricated 0% (the table shows N/A for them).
    present = [
        (label, brain_mapping[key] * 100, color)
        for key, label, color in zip(all_keys, all_labels, all_colors)
        if isinstance(brain_mapping.get(key), (int, float)) and brain_mapping[key] > 0
    ]
    if not present:
        return ''
    lobe_labels = [p[0] for p in present]
    vals = [p[1] for p in present]
    lobe_colors = [p[2] for p in present]

    fig, ax = plt.subplots(figsize=(6.5, 3.2), facecolor=HEX['ivory'])
    ax.set_facecolor(HEX['cream_alt'])
    bars = ax.bar(lobe_labels, vals, color=lobe_colors, width=0.6, edgecolor='none')
    for bar, v in zip(bars, vals):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1.5,
                f'{v:.0f}%', ha='center', fontsize=9,
                color=HEX['navy'], fontfamily='serif')
    ax.set_ylim(0, 110)
    ax.set_ylabel('Activity (%)', color=HEX['navy'], fontsize=9, fontfamily='serif')
    ax.tick_params(colors=HEX['navy'], labelsize=8, rotation=10)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_color(HEX['gold_light'])
    ax.spines['left'].set_color(HEX['gold_light'])
    ax.set_title('Brain Lobe Activity Profile', color=HEX['navy'],
                 fontsize=10, fontfamily='serif', fontweight='bold', pad=8)
    fig.tight_layout()
    return _fig_to_b64(fig)


# ---------------------------------------------------------------------------
# Brain hemisphere split bar
# ---------------------------------------------------------------------------

def create_hemisphere_bar(left: float, right: float) -> str:
    if not MPL:
        return ''
    fig, ax = plt.subplots(figsize=(6.5, 1.4), facecolor=HEX['ivory'])
    ax.set_facecolor(HEX['ivory'])
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 1)
    ax.axis('off')

    left_pct = left * 100
    right_pct = right * 100

    ax.barh([0.5], [left_pct], color=HEX['navy'], height=0.5,
            left=0, label='Left Brain')
    ax.barh([0.5], [right_pct], color=HEX['gold'], height=0.5,
            left=left_pct, label='Right Brain')

    ax.text(left_pct / 2, 0.5, f'Left  {left_pct:.0f}%',
            ha='center', va='center', fontsize=11, color='white',
            fontweight='bold', fontfamily='serif')
    ax.text(left_pct + right_pct / 2, 0.5, f'Right  {right_pct:.0f}%',
            ha='center', va='center', fontsize=11, color=HEX['navy'],
            fontweight='bold', fontfamily='serif')

    ax.set_title('Brain Hemisphere Dominance', color=HEX['navy'],
                 fontsize=10, fontfamily='serif', fontweight='bold', pad=6)
    fig.tight_layout()
    return _fig_to_b64(fig)


# ---------------------------------------------------------------------------
# Learning style pie
# ---------------------------------------------------------------------------

def create_learning_pie(learning: Dict[str, float]) -> str:
    if not MPL or not learning:
        return ''
    labels = [_label(k) for k in learning]
    vals = list(learning.values())
    pie_colors = [HEX['gold'], HEX['navy'], HEX['sage']]
    explode = [0.04] * len(vals)

    fig, ax = plt.subplots(figsize=(5, 4), facecolor=HEX['ivory'])
    ax.set_facecolor(HEX['ivory'])
    _, texts, autotexts = ax.pie(
        vals, labels=labels, autopct='%1.0f%%',
        colors=pie_colors[:len(vals)], startangle=140,
        explode=explode, pctdistance=0.72,
        wedgeprops=dict(edgecolor='white', linewidth=2)
    )
    for t in texts:
        t.set_color(HEX['navy'])
        t.set_fontsize(10)
        t.set_fontfamily('serif')
    for at in autotexts:
        at.set_color('white')
        at.set_fontsize(9)
        at.set_fontweight('bold')
        at.set_fontfamily('serif')
    ax.set_title('Learning Style Distribution', color=HEX['navy'],
                 fontsize=10, fontfamily='serif', fontweight='bold', pad=10)
    fig.tight_layout()
    return _fig_to_b64(fig)


# ---------------------------------------------------------------------------
# Personality Big-5 spider / radar
# ---------------------------------------------------------------------------

def create_personality_radar(personality: Dict[str, float]) -> str:
    if not MPL or not personality:
        return ''
    trait_map = {
        'openness': 'Openness',
        'conscientiousness': 'Conscientiousness',
        'extraversion': 'Extraversion',
        'agreeableness': 'Agreeableness',
        'neuroticism': 'Emotional\nStability',
    }
    labels = [trait_map.get(k, _label(k)) for k in personality]
    # Invert neuroticism for "Emotional Stability"
    vals = []
    for k, v in personality.items():
        vals.append(1 - v if k == 'neuroticism' else v)

    N = len(vals)
    angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
    vals_plot = vals + [vals[0]]
    angles_plot = angles + [angles[0]]

    fig, ax = plt.subplots(figsize=(5.5, 5), subplot_kw=dict(polar=True),
                           facecolor=HEX['ivory'])
    ax.set_facecolor(HEX['cream_alt'])
    ax.plot(angles_plot, vals_plot, 'o-', linewidth=2.0, color=HEX['plum'])
    ax.fill(angles_plot, vals_plot, alpha=0.25, color=HEX['plum'])
    ax.set_thetagrids(np.degrees(angles), labels,
                      fontsize=8.5, color=HEX['navy'], fontfamily='serif')
    ax.set_ylim(0, 1)
    ax.set_yticks([0.25, 0.5, 0.75, 1.0])
    ax.set_yticklabels([], fontsize=0)
    ax.grid(color=HEX['grey_light'], linewidth=0.5)
    ax.spines['polar'].set_color(HEX['gold_light'])
    ax.set_title('Personality Profile (Big Five)', color=HEX['navy'],
                 fontsize=10, fontfamily='serif', pad=14, fontweight='bold')
    return _fig_to_b64(fig)


# ---------------------------------------------------------------------------
# Extension grouped bar
# ---------------------------------------------------------------------------

def _to_mpl_color(c) -> str:
    """Convert a ReportLab Color or hex string to a matplotlib-compatible hex string."""
    if c is None:
        return HEX['gold']
    if isinstance(c, str):
        return c
    # ReportLab Color objects have .red, .green, .blue attributes (0-1 floats)
    try:
        return '#{:02x}{:02x}{:02x}'.format(
            int(c.red * 255), int(c.green * 255), int(c.blue * 255))
    except Exception:
        return HEX['gold']


def create_extension_bar(ext_scores: Dict[str, float], title: str,
                         color=None) -> str:
    if not MPL or not ext_scores:
        return ''
    color = _to_mpl_color(color) or HEX['gold']
    sorted_items = sorted(ext_scores.items(), key=lambda x: x[1], reverse=True)
    labels = [_label(k) for k, _ in sorted_items]
    vals = [v * 100 for _, v in sorted_items]

    # Row-height multiplier trimmed from 0.45in to 0.36in per bar: with
    # 10-11 extension scores (typical for Cognitive/Social/Leadership), the
    # extra height combined with the ranked score table underneath and the
    # section header pushed the whole atomic block just past one page,
    # forcing shrink_block to scale the block down ~8%. Bars stay perfectly
    # readable at the tighter spacing.
    fig, ax = plt.subplots(figsize=(7, max(2.2, 0.36 * len(labels) + 0.5)),
                           facecolor=HEX['ivory'])
    ax.set_facecolor(HEX['cream_alt'])

    bar_colors = []
    for v in vals:
        if v >= 75: bar_colors.append(HEX['green_strong'])
        elif v >= 60: bar_colors.append(color)
        elif v >= 45: bar_colors.append(HEX['amber_mid'])
        else: bar_colors.append(HEX['terracotta'])

    bars = ax.barh(labels, vals, color=bar_colors, height=0.55, edgecolor='none')
    for bar, v in zip(bars, vals):
        ax.text(bar.get_width() + 1.0, bar.get_y() + bar.get_height() / 2,
                f'{v:.0f}%', va='center', fontsize=8, color=HEX['navy'],
                fontfamily='serif')
    ax.set_xlim(0, 115)
    ax.set_xlabel('Score (%)', color=HEX['navy'], fontsize=8.5, fontfamily='serif')
    ax.tick_params(colors=HEX['navy'], labelsize=8)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_color(HEX['gold_light'])
    ax.spines['left'].set_color(HEX['gold_light'])
    ax.set_title(title, color=HEX['navy'], fontsize=10,
                 fontfamily='serif', fontweight='bold', pad=8)
    fig.tight_layout()
    return _fig_to_b64(fig)


# ---------------------------------------------------------------------------
# SWOT 4-quadrant visual
# ---------------------------------------------------------------------------

def create_swot_chart(swot: Dict[str, List[str]]) -> str:
    """swot keys: strengths, weaknesses, opportunities, threats"""
    if not MPL:
        return ''
    fig, axes = plt.subplots(2, 2, figsize=(8, 5.5), facecolor=HEX['ivory'])
    config = [
        ('strengths',    'Strengths',     HEX['green_strong'], 'S'),
        ('weaknesses',   'Weaknesses',    HEX['terracotta'],   'W'),
        ('opportunities','Opportunities', HEX['gold_dark'],    'O'),
        ('threats',      'Threats',       HEX['plum'],         'T'),
    ]
    for ax, (key, title, color, letter) in zip(axes.flat, config):
        ax.set_facecolor(HEX['ivory'])
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        ax.axis('off')
        # Header band
        rect = mpatches.FancyBboxPatch((0.1, 7.8), 9.8, 2.0,
                                       boxstyle='round,pad=0.15',
                                       facecolor=color, edgecolor='none')
        ax.add_patch(rect)
        ax.text(5, 8.8, f'{letter}  {title}', ha='center', va='center',
                fontsize=11, color='white', fontweight='bold',
                fontfamily='serif')
        # Items
        items = swot.get(key, [])[:5]
        for i, item in enumerate(items):
            ax.text(0.5, 7.0 - i * 1.3, f'  {item}',
                    ha='left', va='top', fontsize=8,
                    color=HEX['navy'], fontfamily='serif',
                    wrap=True)
        # Border
        border = mpatches.FancyBboxPatch((0.05, 0.05), 9.9, 9.9,
                                         boxstyle='round,pad=0.1',
                                         facecolor='none',
                                         edgecolor=color, linewidth=1.5)
        ax.add_patch(border)

    # No fig.suptitle here: the ReportLab sub_heading('SWOT Analysis') placed
    # immediately above this chart already renders the section title, so a
    # second "SWOT Analysis" baked into the image itself just duplicated it.
    fig.tight_layout(pad=0.4)
    return _fig_to_b64(fig)


# ---------------------------------------------------------------------------
# Career match horizontal bar
# ---------------------------------------------------------------------------

def create_career_bar(career_scores: Dict[str, float]) -> str:
    if not MPL or not career_scores:
        return ''
    sorted_items = sorted(career_scores.items(), key=lambda x: x[1], reverse=True)
    labels = [k for k, _ in sorted_items]
    vals = [v * 100 for _, v in sorted_items]

    gradient_colors = [
        HEX['gold'], HEX['navy'], HEX['sage'], HEX['plum'],
        HEX['gold_dark'], HEX['terracotta'], HEX['green_strong'],
        HEX['amber_mid'], HEX['gold'], HEX['navy'],
        HEX['sage'], HEX['plum'], HEX['gold_dark'],
    ]

    fig, ax = plt.subplots(figsize=(7, max(3.0, 0.48 * len(labels) + 0.6)),
                           facecolor=HEX['ivory'])
    ax.set_facecolor(HEX['cream_alt'])
    bars = ax.barh(labels, vals, color=gradient_colors[:len(labels)],
                   height=0.6, edgecolor='none')
    for bar, v in zip(bars, vals):
        ax.text(bar.get_width() + 1.0, bar.get_y() + bar.get_height() / 2,
                f'{v:.0f}%', va='center', fontsize=8.5,
                color=HEX['navy'], fontfamily='serif')
    ax.set_xlim(0, 115)
    ax.set_xlabel('Match Score (%)', color=HEX['navy'], fontsize=9,
                  fontfamily='serif')
    ax.tick_params(colors=HEX['navy'], labelsize=8.5)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_color(HEX['gold_light'])
    ax.spines['left'].set_color(HEX['gold_light'])
    ax.set_title('Career Aptitude Scores', color=HEX['navy'],
                 fontsize=10, fontfamily='serif', fontweight='bold', pad=8)
    fig.tight_layout()
    return _fig_to_b64(fig)


# ---------------------------------------------------------------------------
# Finger pattern bar (quality per finger)
# ---------------------------------------------------------------------------

def create_finger_quality_bar(per_finger: List[Dict[str, Any]]) -> str:
    if not MPL or not per_finger:
        return ''
    labels = []
    quals = []
    for f in per_finger:
        pos = f.get('finger_position') or f.get('finger_type', 'Unknown')
        q = f.get('image_quality') if f.get('image_quality') is not None \
            else f.get('quality_score')
        if not isinstance(q, (int, float)) or q <= 0:
            continue  # skip fingers with no real quality measurement
        labels.append(pos)
        quals.append(float(q) * 100 if q <= 1.0 else float(q))
    if not labels:
        return ''

    bar_colors = []
    for q in quals:
        if q >= 75: bar_colors.append(HEX['green_strong'])
        elif q >= 55: bar_colors.append(HEX['gold'])
        else: bar_colors.append(HEX['terracotta'])

    fig, ax = plt.subplots(figsize=(7, 2.8), facecolor=HEX['ivory'])
    ax.set_facecolor(HEX['cream_alt'])
    ax.bar(labels, quals, color=bar_colors, width=0.6, edgecolor='none')
    ax.set_ylim(0, 110)
    ax.set_ylabel('Quality (%)', color=HEX['navy'], fontsize=9, fontfamily='serif')
    ax.tick_params(colors=HEX['navy'], labelsize=8.5, rotation=20)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_color(HEX['gold_light'])
    ax.spines['left'].set_color(HEX['gold_light'])
    ax.set_title('Fingerprint Quality per Finger', color=HEX['navy'],
                 fontsize=10, fontfamily='serif', fontweight='bold', pad=8)
    fig.tight_layout()
    return _fig_to_b64(fig)


# ---------------------------------------------------------------------------
# EQ sub-dimension radar
# ---------------------------------------------------------------------------

def create_eq_radar(eq_scores: Dict[str, float]) -> str:
    """Like intelligence radar but in plum/sage palette."""
    if not MPL or not eq_scores:
        return ''
    labels = [_wrap(_label(k)) for k in eq_scores]
    vals = list(eq_scores.values())
    N = len(vals)
    if N < 3:
        return ''
    angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
    vals_plot = vals + [vals[0]]
    angles_plot = angles + [angles[0]]

    fig, ax = plt.subplots(figsize=(5.5, 5), subplot_kw=dict(polar=True),
                           facecolor=HEX['ivory'])
    ax.set_facecolor(HEX['cream_alt'])
    ax.plot(angles_plot, vals_plot, 'o-', linewidth=2.0, color=HEX['sage'])
    ax.fill(angles_plot, vals_plot, alpha=0.28, color=HEX['sage'])
    ax.set_thetagrids(np.degrees(angles), labels,
                      fontsize=7.5, color=HEX['navy'], fontfamily='serif')
    ax.set_ylim(0, 1)
    ax.set_yticks([0.25, 0.5, 0.75, 1.0])
    ax.set_yticklabels(['25%', '50%', '75%', '100%'],
                       fontsize=6.5, color=HEX['grey_text'])
    ax.grid(color=HEX['grey_light'], linewidth=0.5)
    ax.spines['polar'].set_color(HEX['gold_light'])
    ax.set_title('Emotional Intelligence Profile', color=HEX['navy'],
                 fontsize=10, fontfamily='serif', pad=14, fontweight='bold')
    return _fig_to_b64(fig)


# ---------------------------------------------------------------------------
# MI individual gauge mini-grid  (always renders when MI data present)
# ---------------------------------------------------------------------------

def create_mi_gauge_grid(mi_scores: Dict[str, float]) -> str:
    """
    4-gauge row: top 2 MI + weakest 2 MI displayed as Style-E arcs.
    Returns a wide PNG (7 x 2.4 inches) suitable for full-width embedding.
    """
    if not MPL or not mi_scores:
        return ''

    sorted_mi = sorted(
        [(k, v) for k, v in mi_scores.items() if isinstance(v, (int, float))],
        key=lambda x: x[1], reverse=True
    )
    if not sorted_mi:
        return ''

    # Pick top-2 and bottom-2 (deduplicated)
    top2  = sorted_mi[:2]
    bot2  = sorted_mi[-2:] if len(sorted_mi) >= 4 else sorted_mi[-min(2, len(sorted_mi)):]
    items = top2 + [x for x in bot2 if x not in top2]
    items = items[:4]

    n = len(items)
    fig, axes = plt.subplots(1, n, figsize=(n * 2.0, 2.4),
                             subplot_kw=dict(aspect='equal'),
                             facecolor=HEX['ivory'])
    if n == 1:
        axes = [axes]

    for ax, (key, score) in zip(axes, items):
        pct   = float(score)
        start = 225
        sweep = 270
        n_seg = 60
        seg_c = int(pct * n_seg)

        ax.set_facecolor(HEX['ivory'])
        ax.set_xlim(-1.35, 1.35)
        ax.set_ylim(-1.35, 1.55)
        ax.axis('off')

        # Track
        theta = np.linspace(np.radians(start), np.radians(start - sweep), 180)
        ax.plot(np.cos(theta), np.sin(theta),
                color=HEX['gold_pale'], linewidth=8, alpha=0.5,
                solid_capstyle='round')

        # Arc gradient
        gold_light = np.array([0xe8/255, 0xd5/255, 0x9a/255])
        gold_bright = np.array([0xc9/255, 0xa4/255, 0x41/255])
        for i in range(seg_c):
            t  = i / max(1, n_seg - 1)
            c  = tuple(gold_light + t * (gold_bright - gold_light))
            a0 = np.radians(start - (i / n_seg) * sweep)
            a1 = np.radians(start - ((i + 1) / n_seg) * sweep)
            th = np.linspace(a0, a1, 6)
            lw = 9
            cap = 'round' if i == 0 or i == seg_c - 1 else 'butt'
            ax.plot(np.cos(th), np.sin(th), color=c, linewidth=lw, solid_capstyle=cap)

        # Glow dot
        ea = np.radians(start - pct * sweep)
        ex, ey = np.cos(ea), np.sin(ea)
        ax.scatter([ex], [ey], s=160, color=HEX['gold'], zorder=5,
                   edgecolors=HEX['gold_light'], linewidths=1.5)
        ax.scatter([ex], [ey], s=380, color=HEX['gold_pale'], zorder=4, alpha=0.35)

        # Score text
        ax.text(0, -0.12, f'{pct*100:.0f}%', ha='center', va='center',
                fontsize=13, fontweight='bold', color=HEX['navy'],
                fontfamily='serif')

        # Label (top-2 gold, bot-2 terracotta tint). This grid is embedded
        # at ~83% of its native figure width, so a nominal fontsize=6.5
        # label was printing under 5.5pt effective on the page — visibly
        # smaller than any other text in the report. Bumped to read at a
        # normal caption size once displayed.
        lbl_color = HEX['gold_dark'] if score >= sorted_mi[len(sorted_mi)//2][1] \
                    else HEX['terracotta']
        ax.text(0, -0.52, _wrap(_label(key), 12), ha='center', va='top',
                fontsize=9, color=lbl_color, fontfamily='serif',
                fontweight='bold', multialignment='center')

    fig.suptitle('Key Intelligence Snapshot', fontsize=9, fontfamily='serif',
                 color=HEX['navy'], fontweight='bold', y=0.02)
    fig.tight_layout(pad=0.4)
    return _fig_to_b64(fig)


# ---------------------------------------------------------------------------
# Personality trait horizontal bars (always renders when personality data present)
# ---------------------------------------------------------------------------

def create_personality_bars(personality: Dict[str, float]) -> str:
    """
    Horizontal gradient bar chart for Big-5 personality traits.
    More readable than a radar when only 5 traits are present.
    """
    if not MPL or not personality:
        return ''

    items = [(k, v) for k, v in personality.items()
             if isinstance(v, (int, float))]
    if not items:
        return ''

    labels = [_wrap(_label(k)) for k, v in items]
    values = [v for k, v in items]

    fig, ax = plt.subplots(figsize=(6.5, max(2.5, len(items) * 0.6)),
                            facecolor=HEX['ivory'])
    ax.set_facecolor(HEX['cream_alt'])

    bar_h = 0.55
    y_pos = np.arange(len(values))

    # Background track
    ax.barh(y_pos, [1.0] * len(values), bar_h + 0.08,
            color=HEX['gold_pale'], alpha=0.5, zorder=1)

    # Gold gradient bars via gradient patch
    for y, v in zip(y_pos, values):
        color = HEX['gold'] if v >= 0.6 else (
            HEX['sage'] if v >= 0.45 else HEX['terracotta'])
        ax.barh(y, v, bar_h, color=color, zorder=2, alpha=0.88)
        ax.text(min(v + 0.02, 0.97), y, f'{v*100:.0f}%',
                va='center', ha='left', fontsize=8,
                color=HEX['navy'], fontfamily='serif', fontweight='bold')

    ax.set_yticks(y_pos)
    ax.set_yticklabels(labels, fontsize=8, color=HEX['navy'], fontfamily='serif')
    ax.set_xlim(0, 1.12)
    ax.set_xticks([0, 0.25, 0.5, 0.75, 1.0])
    ax.set_xticklabels(['0%', '25%', '50%', '75%', '100%'],
                        fontsize=7, color=HEX['grey_text'])
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_color(HEX['gold_light'])
    ax.spines['left'].set_color(HEX['gold_light'])
    ax.axvline(x=0.5, color=HEX['gold_light'], linewidth=0.8, linestyle='--', alpha=0.7)
    ax.set_title('Personality Trait Profile (Big Five)', color=HEX['navy'],
                 fontsize=10, fontfamily='serif', fontweight='bold', pad=8)
    fig.tight_layout()
    return _fig_to_b64(fig)


# ---------------------------------------------------------------------------
# Learning style comparison bar (always renders when learning data present)
# ---------------------------------------------------------------------------

def create_learning_bar(learning: Dict[str, float]) -> str:
    """
    Vertical bar chart comparing learning style strengths side by side.
    Complements the pie chart with precise numerical comparison.
    """
    if not MPL or not learning:
        return ''

    items = [(k, v) for k, v in learning.items()
             if isinstance(v, (int, float))]
    if not items:
        return ''

    labels  = [_label(k) for k, v in items]
    values  = [v for k, v in items]
    bar_cols = [HEX['gold'] if v == max(values) else HEX['sage'] for v in values]

    fig, ax = plt.subplots(figsize=(max(4.0, len(items) * 1.4), 3.0),
                            facecolor=HEX['ivory'])
    ax.set_facecolor(HEX['cream_alt'])

    x_pos = np.arange(len(values))
    bars = ax.bar(x_pos, [v * 100 for v in values],
                  color=bar_cols, width=0.55, edgecolor='none', zorder=2)

    # Value labels above bars
    for bar, v in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width() / 2,
                bar.get_height() + 1.5,
                f'{v*100:.0f}%',
                ha='center', va='bottom', fontsize=9,
                color=HEX['navy'], fontfamily='serif', fontweight='bold')

    ax.set_xticks(x_pos)
    ax.set_xticklabels(labels, fontsize=9, color=HEX['navy'], fontfamily='serif')
    ax.set_ylim(0, 115)
    ax.set_ylabel('Strength (%)', color=HEX['navy'], fontsize=9, fontfamily='serif')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_color(HEX['gold_light'])
    ax.spines['left'].set_color(HEX['gold_light'])
    ax.set_title('Learning Style Comparison', color=HEX['navy'],
                 fontsize=10, fontfamily='serif', fontweight='bold', pad=8)
    fig.tight_layout()
    return _fig_to_b64(fig)


# ---------------------------------------------------------------------------
# Pattern distribution donut  (fingerprint diversity overview)
# ---------------------------------------------------------------------------

def create_pattern_donut(per_finger: List[Dict[str, Any]]) -> str:
    """
    Donut chart showing distribution of fingerprint pattern types
    across all fingers (Whorl, Loop, Arch, Composite, etc.).
    """
    if not MPL or not per_finger:
        return ''

    from collections import Counter
    pattern_counts: Counter = Counter()
    for f in per_finger:
        pat = str(f.get('pattern_type') or 'unknown').lower()
        # Normalise common variants
        if 'whorl' in pat:
            pat = 'Whorl'
        elif 'loop' in pat:
            pat = 'Loop'
        elif 'arch' in pat:
            pat = 'Arch'
        elif 'composite' in pat or 'mixed' in pat:
            pat = 'Composite'
        else:
            pat = pat.title() or 'Unknown'
        pattern_counts[pat] += 1

    if not pattern_counts:
        return ''

    palette = [HEX['gold'], HEX['navy'], HEX['sage'],
               HEX['plum'], HEX['terracotta'], HEX['gold_light']]
    labels  = list(pattern_counts.keys())
    sizes   = list(pattern_counts.values())
    colors  = [palette[i % len(palette)] for i in range(len(labels))]

    fig, ax = plt.subplots(figsize=(5.0, 3.8), facecolor=HEX['ivory'])
    ax.set_facecolor(HEX['ivory'])
    wedges, texts, autotexts = ax.pie(
        sizes, labels=None, colors=colors, autopct='%1.0f%%',
        startangle=90, pctdistance=0.72,
        wedgeprops=dict(width=0.52, edgecolor=HEX['ivory'], linewidth=2)
    )
    for at in autotexts:
        at.set_fontsize(8.5)
        at.set_color(HEX['navy'])
        at.set_fontfamily('serif')
        at.set_fontweight('bold')

    ax.legend(wedges, [f'{l} ({c})' for l, c in zip(labels, sizes)],
              loc='center left', bbox_to_anchor=(0.92, 0.5),
              fontsize=8, frameon=False,
              prop={'family': 'serif', 'size': 8})
    ax.set_title('Pattern Type Distribution', color=HEX['navy'],
                 fontsize=10, fontfamily='serif', fontweight='bold', pad=8)
    fig.tight_layout()
    return _fig_to_b64(fig)


# ---------------------------------------------------------------------------
# Full MI ranked bar (wider, more visual than the existing one)
# ---------------------------------------------------------------------------

def create_mi_full_bar(mi_scores: Dict[str, float]) -> str:
    """
    Tall horizontal ranked bar chart for all 8 MI scores.
    Gold bars for strong (>0.65), sage for average, light-red for developing.
    """
    if not MPL or not mi_scores:
        return ''

    items = sorted(
        [(k, v) for k, v in mi_scores.items() if isinstance(v, (int, float))],
        key=lambda x: x[1], reverse=True
    )
    if not items:
        return ''

    labels = [_wrap(_label(k), 16) for k, v in items]
    values = [v for k, v in items]
    colors = [HEX['gold'] if v >= 0.65 else (
              HEX['sage'] if v >= 0.45 else HEX['terracotta']) for v in values]

    fig, ax = plt.subplots(figsize=(6.8, max(3.0, len(items) * 0.7)),
                            facecolor=HEX['ivory'])
    ax.set_facecolor(HEX['cream_alt'])
    y_pos = np.arange(len(values))

    # Track
    ax.barh(y_pos, [1.0] * len(values), 0.58,
            color=HEX['gold_pale'], alpha=0.45, zorder=1)
    # Bars
    ax.barh(y_pos, values, 0.58, color=colors, zorder=2, alpha=0.9)

    # Rank medal for top score
    for i, (y, v) in enumerate(zip(y_pos, values)):
        medal = '#C9A441' if i == 0 else ('#A8A9AD' if i == 1 else
                ('#CD7F32' if i == 2 else HEX['grey_text']))
        ax.text(-0.02, y, f'#{i+1}', va='center', ha='right',
                fontsize=7.5, color=medal, fontweight='bold',
                fontfamily='serif')
        ax.text(min(v + 0.02, 0.99), y, f'{v*100:.0f}%',
                va='center', ha='left', fontsize=8.5,
                color=HEX['navy'], fontfamily='serif', fontweight='bold')

    ax.set_yticks(y_pos)
    ax.set_yticklabels(labels, fontsize=8, color=HEX['navy'], fontfamily='serif')
    ax.set_xlim(-0.08, 1.14)
    ax.set_xticks([0, 0.25, 0.5, 0.75, 1.0])
    ax.set_xticklabels(['0', '25%', '50%', '75%', '100%'],
                        fontsize=7, color=HEX['grey_text'])
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_color(HEX['gold_light'])
    ax.spines['left'].set_color(HEX['gold_light'])
    ax.axvline(0.5, color=HEX['gold_light'], linewidth=0.8,
               linestyle='--', alpha=0.6, zorder=0)
    ax.set_title('Multiple Intelligence Rankings', color=HEX['navy'],
                 fontsize=10, fontfamily='serif', fontweight='bold', pad=8)
    fig.tight_layout()
    return _fig_to_b64(fig)
