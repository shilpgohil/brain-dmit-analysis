# World-Class UI/UX & Kinetic Animation Craft — DMIT Platform

## 1. Design Standard & Quality Tier
The DMIT Analysis Platform interface must match the visual excellence, kinetic precision, and design intelligence of **GPT Astra, Claude, Fable, Linear, Apple, and Stripe**.

### Visual Pillars
- **Cinematic Biometric Command Deck**: Deep obsidian base canvas (`#030712`) layered with sapphire frosted glass panels (`#0B0F19` with `backdrop-filter: blur(24px)`).
- **Luxury Gold & Ivory Accents**: Warm gold (`#D4AF37` / `#F59E0B`) highlights for top intelligences, executive badges, and radar charts.
- **Machined Subpixel Borders**: 1px machined edges (`rgba(255, 255, 255, 0.08)`) with specular inner highlights (`box-shadow: inset 0 1px 0 0 rgba(255, 255, 255, 0.12)`).
- **Anti-Jitter Typography**: `Plus Jakarta Sans` / `Inter` for UI typography paired with `JetBrains Mono` (`font-mono tabular-nums slashed-zero`) for all scores, percentiles, and ridge counts.

---

## 2. Kinetic Animation & Spring Physics
All interactions must be organic, physical, and hardware-accelerated:

### Easing Tokens
- Snappy Micro-Interactions: `cubic-bezier(0.16, 1, 0.3, 1)` (150ms-250ms).
- Fluid Layout Morphing: `cubic-bezier(0.22, 1, 0.36, 1)` (350ms-500ms).
- Tactile Springs: `stiffness: 400`, `damping: 30`, `mass: 0.8` for button presses, tab indicators, and finger slot highlights.

### Strict Hardware Acceleration
- Animate ONLY `transform`, `opacity`, and composited filter values (`backdrop-filter`).
- NEVER animate `width`, `height`, `margin`, `padding`, or `top/left/bottom/right` during transitions.
- Maintain a strict 60fps frame budget (16.6ms) on standard displays and 120fps (8.3ms) on ProMotion displays.

---

## 3. Interactive Biometric Visualization Suite

1. **Interactive 10-Finger Hand Guide (`FingerHandSvg.tsx`)**:
   - High-fidelity vector SVG hands (Left & Right) with designated interactive zones for `L1`..`L5` and `R1`..`R5`.
   - Dynamic upload status: Empty slot (subtle dashed border), Uploaded (glowing cyan outline), Processing (pulse wave), Complete (emerald badge).
2. **Brain Lobe 3D/SVG Heatmap (`BrainLobeDiagram.tsx`)**:
   - Interactive brain diagram displaying Prefrontal, Posterior Frontal, Parietal, Temporal, and Occipital lobes.
   - Dynamic luminescence: Lobes glow with intensity proportional to their computed percentage score.
3. **Gold Radar Chart (`GoldRadarChart.tsx` / `IntelligenceRadar.tsx`)**:
   - Polar coordinate radar polygon representing the 9 Gardner Multiple Intelligences with smooth spring tweening on data load.
4. **VAK Learning Style Pie / Doughnut (`LearningStylePie.tsx`)**:
   - Visual (Blue), Auditory (Violet), Kinesthetic (Amber) breakdown with hover expansion and center metric readout.

---

## 4. Zero Layout Shift (CLS = 0)
- Every card, chart container, and upload grid must have explicit aspect ratios or pre-allocated bounding dimensions.
- Analysis pipeline stages mount into pre-measured height shells with smooth height transitions (`overflow-hidden`).
