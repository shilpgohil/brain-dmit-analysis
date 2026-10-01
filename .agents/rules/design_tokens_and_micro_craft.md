# Design Tokens & Micro-Craft Standards — DMIT Platform

## 1. Dual Palette Architecture

### Palette A: Cinematic Dark Command Deck (Web Application Default)
```css
:root {
  --canvas-bg: #030712;
  --surface-base: rgba(11, 15, 25, 0.70);
  --surface-elevated: rgba(17, 24, 39, 0.75);
  --surface-overlay: rgba(23, 32, 51, 0.90);
  
  --border-subtle: rgba(255, 255, 255, 0.06);
  --border-default: rgba(255, 255, 255, 0.08);
  --border-elevated: rgba(255, 255, 255, 0.14);
  --border-specular: inset 0 1px 0 0 rgba(255, 255, 255, 0.12);

  --accent-gold: #D4AF37;
  --accent-gold-glow: rgba(212, 175, 55, 0.18);
  --accent-cyan: #06B6D4;
  --accent-cyan-glow: rgba(6, 182, 212, 0.15);
  --accent-emerald: #10B981;
  --accent-violet: #8B5CF6;
  --accent-rose: #F43F5E;
}
```

### Palette B: Ivory & Luxury Gold (Premium PDF Report Default)
```css
:root {
  --report-bg: #FAF8F5;
  --report-card: #FFFFFF;
  --report-primary: #1F2937;
  --report-secondary: #4B5563;
  --report-accent-gold: #C5A059;
  --report-border: #E5E7EB;
}
```

---

## 2. Micro-Craft Standards
- **Machined Subpixel Borders**: Every elevated container features `border: 1px solid rgba(255, 255, 255, 0.08)` coupled with an inner specular line `box-shadow: inset 0 1px 0 0 rgba(255, 255, 255, 0.12)`.
- **Custom Trackless Scrollbars**: 6px width, transparent background, rounded thumb with `rgba(255, 255, 255, 0.12)`.
- **Accessible Cyan Focus Rings**: 2px offset electric cyan (`#06B6D4`) rings on keyboard focus.
- **Tabular Numerics**: All scores, percentages, and ridge counts use `JetBrains Mono` with OpenType `tabular-nums` and `slashed-zero` to eliminate visual jitter.
