import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.path import Path
import matplotlib.lines as lines

BG_IVORY = "#FAF8F5"
CARD_WHITE = "#FFFFFF"
NAVY = "#162035"
GOLD = "#D4AF37"
GOLD_LIGHT = "#E8DCC4"
TERRACOTTA = "#C46849"
SANDSTONE = "#E5D3B3"
SAGE = "#5A7865"
OCHRE = "#D99B38"
DUSTY_ROSE = "#D8A48F"
CHARCOAL = "#1F2937"
SLATE = "#64748B"

os.makedirs("test_output/boho_samples", exist_ok=True)


def create_cover_hero(output_path: str):
    fig, ax = plt.subplots(figsize=(8, 7), dpi=300)
    fig.patch.set_facecolor(BG_IVORY)
    ax.set_facecolor(BG_IVORY)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 8.5)
    ax.axis("off")

    sun_center = (4.0, 4.2)
    sun = patches.Wedge(sun_center, r=2.6, theta1=0, theta2=180,
                        facecolor=TERRACOTTA, alpha=0.92, edgecolor="none", zorder=1)
    ax.add_patch(sun)

    pebble_verts = [
        (4.5, 1.8), (6.8, 2.2), (7.4, 4.0), (6.5, 5.8),
        (5.0, 6.0), (3.8, 5.0), (3.5, 3.0), (4.5, 1.8)
    ]
    pebble_codes = [Path.MOVETO, Path.CURVE4, Path.CURVE4, Path.CURVE4,
                     Path.CURVE4, Path.CURVE4, Path.CURVE4, Path.CLOSEPOLY]
    pebble_path = Path(pebble_verts, pebble_codes)
    pebble_patch = patches.PathPatch(pebble_path, facecolor=SANDSTONE,
                                     alpha=0.65, edgecolor="none", zorder=2)
    ax.add_patch(pebble_patch)

    ochre_crescent = patches.Arc((3.4, 3.8), width=3.8, height=4.2, angle=25,
                                 theta1=40, theta2=220, color=OCHRE,
                                 linewidth=18, alpha=0.5, zorder=2)
    ax.add_patch(ochre_crescent)

    for deg in range(15, 170, 15):
        rad = np.radians(deg)
        x0 = sun_center[0] + 2.75 * np.cos(rad)
        y0 = sun_center[1] + 2.75 * np.sin(rad)
        x1 = sun_center[0] + 3.25 * np.cos(rad)
        y1 = sun_center[1] + 3.25 * np.sin(rad)
        ax.plot([x0, x1], [y0, y1], color=GOLD, lw=1.2, alpha=0.7, zorder=2)

    profile_verts = [
        (3.8, 1.5),
        (3.8, 2.2),
        (3.9, 2.6),
        (3.4, 2.9),
        (3.5, 3.3),
        (3.3, 3.5),
        (3.4, 3.8),
        (3.0, 4.3),
        (3.4, 4.4),
        (3.2, 4.8),
        (3.7, 5.2),
        (4.4, 5.5),
        (5.2, 5.4),
        (5.8, 4.8),
        (5.9, 3.8),
        (5.6, 2.5),
        (5.3, 1.5)
    ]
    profile_codes = [Path.MOVETO] + [Path.CURVE4] * (len(profile_verts) - 1)
    profile_path = Path(profile_verts, profile_codes)
    profile_patch = patches.PathPatch(profile_path, facecolor="none",
                                      edgecolor=NAVY, lw=2.4, capstyle="round",
                                      joinstyle="round", zorder=4)
    ax.add_patch(profile_patch)

    t = np.linspace(0, 3.8 * np.pi, 250)
    a, b = 0.05, 0.08
    r_spiral = a + b * t
    x_spiral = 4.8 + r_spiral * np.cos(t)
    y_spiral = 4.7 + r_spiral * np.sin(t)
    ax.plot(x_spiral, y_spiral, color=GOLD, lw=1.6, alpha=0.9, zorder=5)

    stem_x = np.linspace(4.8, 6.2, 100)
    stem_y = 5.2 + 0.6 * np.sin((stem_x - 4.8) * 1.8) + 0.3 * (stem_x - 4.8)
    ax.plot(stem_x, stem_y, color=SAGE, lw=1.8, zorder=5)

    leaf_points = [(5.1, 5.5, 35), (5.5, 5.9, -25), (5.8, 6.1, 40), (6.1, 6.5, 15)]
    for lx, ly, lang in leaf_points:
        leaf = patches.Ellipse((lx, ly), width=0.45, height=0.22, angle=lang,
                               facecolor=SAGE, edgecolor=NAVY, lw=0.6, alpha=0.9, zorder=6)
        ax.add_patch(leaf)

    circle_ring = patches.Circle((4.7, 4.2), radius=3.6, facecolor="none",
                                 edgecolor=GOLD, lw=0.7, linestyle="--", alpha=0.45, zorder=1)
    ax.add_patch(circle_ring)

    ax.text(5.0, 0.9, "COMPREHENSIVE DERMATOGLYPHICS & NEURAL MAPPING",
            ha="center", va="center", color=NAVY, fontsize=10.5,
            fontweight="bold", family="sans-serif", zorder=5)
    ax.text(5.0, 0.55, "Boho-Modernist Editorial Cover Vignette (Sample 01)",
            ha="center", va="center", color=SLATE, fontsize=8.5, family="sans-serif", zorder=5)

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, facecolor=BG_IVORY, bbox_inches="tight")
    plt.close(fig)
    print(f"Generated: {output_path}")


def create_dual_hemisphere_brain(output_path: str):
    fig, ax = plt.subplots(figsize=(9, 6.5), dpi=300)
    fig.patch.set_facecolor(BG_IVORY)
    ax.set_facecolor(BG_IVORY)
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 8.5)
    ax.axis("off")

    card = patches.FancyBboxPatch((0.5, 0.4), 10.0, 7.7, boxstyle="round,pad=0.2,rounding_size=0.3",
                                  facecolor=CARD_WHITE, edgecolor=GOLD, lw=1.2, zorder=1)
    ax.add_patch(card)

    ax.text(5.5, 7.5, "BRAIN LOBE & NEURAL POTENTIAL ARCHITECTURE",
            ha="center", va="center", color=NAVY, fontsize=12, fontweight="bold", family="sans-serif", zorder=3)
    ax.text(5.5, 7.15, "Dual-Hemisphere Boho-Modernist Editorial Silhouette (Sample 02)",
            ha="center", va="center", color=SLATE, fontsize=8.5, family="sans-serif", zorder=3)

    ax.plot([5.5, 5.5], [1.4, 6.7], color=GOLD, lw=1.4, linestyle="-.", alpha=0.8, zorder=3)
    ax.scatter([5.5, 5.5], [1.4, 6.7], color=GOLD, s=25, zorder=4)

    left_base = patches.Ellipse((3.8, 4.0), width=3.0, height=4.4, angle=8,
                                facecolor=TERRACOTTA, alpha=0.22, edgecolor="none", zorder=2)
    ax.add_patch(left_base)

    left_lobes = [
        ((3.8, 5.6), 1.6, 1.1, 0, TERRACOTTA, 0.85, "Prefrontal", "Planning & Execution"),
        ((2.8, 4.6), 1.3, 1.2, 20, NAVY, 0.80, "Frontal", "Logical Deduction"),
        ((4.1, 4.4), 1.4, 1.1, -10, SLATE, 0.70, "Parietal", "Fine Motor Craft"),
        ((3.0, 3.2), 1.4, 1.0, 15, OCHRE, 0.75, "Temporal", "Linguistic Articulation"),
        ((4.2, 2.3), 1.3, 0.9, -15, CHARCOAL, 0.85, "Occipital", "Detail Reading"),
    ]

    for (lx, ly), lw, lh, lang, lcol, lalp, lname, lsub in left_lobes:
        patch = patches.FancyBboxPatch((lx - lw/2, ly - lh/2), lw, lh,
                                      boxstyle="round,pad=0.08,rounding_size=0.2",
                                      facecolor=lcol, alpha=lalp, edgecolor=NAVY, lw=1.1, zorder=3)
        ax.add_patch(patch)
        for hline in np.linspace(ly - lh/3, ly + lh/3, 4):
            ax.plot([lx - lw/2.6, lx + lw/2.6], [hline, hline], color=CARD_WHITE, lw=0.6, alpha=0.6, zorder=4)
        ax.text(lx, ly + 0.12, lname, ha="center", va="center", color=CARD_WHITE, fontsize=7.5, fontweight="bold", zorder=5)
        ax.text(lx, ly - 0.16, lsub, ha="center", va="center", color=GOLD_LIGHT, fontsize=5.8, zorder=5)

    right_base = patches.Ellipse((7.2, 4.0), width=3.0, height=4.4, angle=-8,
                                 facecolor=SAGE, alpha=0.22, edgecolor="none", zorder=2)
    ax.add_patch(right_base)

    right_lobes = [
        ((7.2, 5.6), 1.6, 1.1, 0, SAGE, 0.85, "Prefrontal", "Visionary Empathy"),
        ((8.2, 4.6), 1.3, 1.2, -20, OCHRE, 0.80, "Frontal", "Spatial Imagination"),
        ((6.9, 4.4), 1.4, 1.1, 10, DUSTY_ROSE, 0.85, "Parietal", "Gross Athletic Rhythm"),
        ((8.0, 3.2), 1.4, 1.0, -15, TERRACOTTA, 0.80, "Temporal", "Musical Perception"),
        ((6.8, 2.3), 1.3, 0.9, 15, SAGE, 0.70, "Occipital", "Aesthetic Processing"),
    ]

    for (rx, ry), rw, rh, rang, rcol, ralp, rname, rsub in right_lobes:
        patch = patches.Ellipse((rx, ry), width=rw, height=rh, angle=rang,
                                facecolor=rcol, alpha=ralp, edgecolor=GOLD, lw=1.1, zorder=3)
        ax.add_patch(patch)
        t_leaf = np.linspace(-rw/2.8, rw/2.8, 40)
        y_wave = ry + 0.12 * np.sin(t_leaf * 4)
        ax.plot(rx + t_leaf, y_wave, color=CARD_WHITE, lw=0.7, alpha=0.65, zorder=4)
        ax.text(rx, ry + 0.12, rname, ha="center", va="center", color=CARD_WHITE, fontsize=7.5, fontweight="bold", zorder=5)
        ax.text(rx, ry - 0.16, rsub, ha="center", va="center", color=NAVY, fontsize=5.8, zorder=5)

    ax.text(3.8, 6.75, "LEFT HEMISPHERE", ha="center", va="center", color=NAVY, fontsize=9.5, fontweight="bold", zorder=4)
    ax.text(3.8, 6.45, "Analytical • Structured • Action Focused", ha="center", va="center", color=SLATE, fontsize=7.5, zorder=4)

    ax.text(7.2, 6.75, "RIGHT HEMISPHERE", ha="center", va="center", color=NAVY, fontsize=9.5, fontweight="bold", zorder=4)
    ax.text(7.2, 6.45, "Intuitive • Creative • Holistic Synthesis", ha="center", va="center", color=SLATE, fontsize=7.5, zorder=4)

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, facecolor=BG_IVORY, bbox_inches="tight")
    plt.close(fig)
    print(f"Generated: {output_path}")


def create_swot_quadrants(output_path: str):
    fig, axes = plt.subplots(2, 2, figsize=(9, 8), dpi=300)
    fig.patch.set_facecolor(BG_IVORY)

    quads = [
        (axes[0, 0], "STRENGTHS (S)", "Foundational Ascent & Core Drive", TERRACOTTA, "S", "rising_sun"),
        (axes[0, 1], "WEAKNESSES (W)", "Zen Equilibrium & Calibration", SAGE, "W", "zen_stones"),
        (axes[1, 0], "OPPORTUNITIES (O)", "Expanding Horizons & Vision", OCHRE, "O", "open_arch"),
        (axes[1, 1], "THREATS (T)", "Protective Boundary & Resilience", NAVY, "T", "protective_shell"),
    ]

    for ax, title, sub, main_col, letter, visual_type in quads:
        ax.set_facecolor(CARD_WHITE)
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        ax.axis("off")

        card_box = patches.FancyBboxPatch((0.4, 0.4), 9.2, 9.2,
                                          boxstyle="round,pad=0.2,rounding_size=0.4",
                                          facecolor=CARD_WHITE, edgecolor=GOLD, lw=1.1, zorder=1)
        ax.add_patch(card_box)

        ax.text(1.2, 8.8, letter, color=main_col, fontsize=32, fontweight="bold", alpha=0.25, family="serif", zorder=2)
        ax.text(1.2, 8.6, title, color=NAVY, fontsize=11, fontweight="bold", zorder=4)
        ax.text(1.2, 8.1, sub, color=SLATE, fontsize=7.5, zorder=4)

        if visual_type == "rising_sun":
            sun_w = patches.Wedge((5.0, 4.4), r=2.2, theta1=0, theta2=180,
                                  facecolor=TERRACOTTA, alpha=0.9, zorder=3)
            ax.add_patch(sun_w)
            arch_base = patches.FancyBboxPatch((3.4, 2.2), 3.2, 2.3,
                                               boxstyle="round,pad=0.1,rounding_size=0.6",
                                               facecolor=SANDSTONE, edgecolor=NAVY, lw=1.2, zorder=4)
            ax.add_patch(arch_base)
            for ray in np.linspace(20, 160, 9):
                rad = np.radians(ray)
                rx0, ry0 = 5.0 + 2.35 * np.cos(rad), 4.4 + 2.35 * np.sin(rad)
                rx1, ry1 = 5.0 + 2.85 * np.cos(rad), 4.4 + 2.85 * np.sin(rad)
                ax.plot([rx0, rx1], [ry0, ry1], color=GOLD, lw=1.1, zorder=2)

        elif visual_type == "zen_stones":
            stone1 = patches.Ellipse((5.0, 2.7), width=3.8, height=1.5, angle=2,
                                     facecolor=SAGE, alpha=0.85, edgecolor=NAVY, lw=1.1, zorder=2)
            stone2 = patches.Ellipse((5.0, 4.1), width=2.8, height=1.3, angle=-4,
                                     facecolor=SANDSTONE, alpha=0.9, edgecolor=NAVY, lw=1.1, zorder=3)
            stone3 = patches.Ellipse((5.0, 5.2), width=1.8, height=1.0, angle=3,
                                     facecolor=GOLD, alpha=0.95, edgecolor=NAVY, lw=1.1, zorder=4)
            ax.add_patch(stone1)
            ax.add_patch(stone2)
            ax.add_patch(stone3)
            ax.plot([5.0, 5.0], [1.8, 6.2], color=SLATE, lw=0.8, linestyle=":", alpha=0.6, zorder=1)

        elif visual_type == "open_arch":
            for rad_w in [1.3, 1.9, 2.5]:
                arc_w = patches.Arc((5.0, 3.2), width=rad_w*2, height=rad_w*2.4, theta1=0, theta2=180,
                                    color=OCHRE, lw=1.4, alpha=0.75, zorder=2)
                ax.add_patch(arc_w)
            arch_portal = patches.FancyBboxPatch((3.8, 2.0), 2.4, 3.4,
                                                boxstyle="round,pad=0.1,rounding_size=0.9",
                                                facecolor=TERRACOTTA, alpha=0.88, edgecolor=NAVY, lw=1.2, zorder=3)
            ax.add_patch(arch_portal)
            sun_inner = patches.Circle((5.0, 4.3), radius=0.6, facecolor=GOLD, edgecolor=CARD_WHITE, lw=1.0, zorder=4)
            ax.add_patch(sun_inner)

        elif visual_type == "protective_shell":
            shell_outer = patches.Wedge((5.0, 4.0), r=2.6, theta1=20, theta2=220,
                                        facecolor=NAVY, alpha=0.92, edgecolor=GOLD, lw=1.2, zorder=2)
            shell_inner = patches.Wedge((5.0, 4.0), r=1.9, theta1=30, theta2=210,
                                        facecolor=DUSTY_ROSE, alpha=0.85, zorder=3)
            pearl = patches.Circle((4.5, 3.8), radius=0.55, facecolor=GOLD, edgecolor=CARD_WHITE, lw=1.2, zorder=4)
            ax.add_patch(shell_outer)
            ax.add_patch(shell_inner)
            ax.add_patch(pearl)

        ax.text(5.0, 1.2, "Bespoke Boho Vignette Sample", ha="center", va="center", color=SLATE, fontsize=7, zorder=5)

    plt.suptitle("PERSONALITY SWOT QUADRANT ARTWORK SUITE (Sample 03)", fontsize=13, fontweight="bold", color=NAVY, y=0.98)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, facecolor=BG_IVORY, bbox_inches="tight")
    plt.close(fig)
    print(f"Generated: {output_path}")


if __name__ == "__main__":
    create_cover_hero("test_output/boho_samples/sample_cover_hero.png")
    create_dual_hemisphere_brain("test_output/boho_samples/sample_dual_hemisphere_brain.png")
    create_swot_quadrants("test_output/boho_samples/sample_swot_quadrants.png")
    print("All sample artworks generated successfully.")
