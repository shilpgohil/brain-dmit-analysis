---
name: dmit-report-generator
description: >
  19-section premium PDF report generator for the DMIT Analysis Platform.
  Covers ReportLab / Matplotlib vector chart generation, ivory/gold luxury theme layout,
  multi-page document assembly, and real-data verification.
  Use when designing, compiling, or debugging DMIT PDF generation pipelines.
---

# DMIT Premium PDF Report Generator

## 1. 19-Section Report Architecture
- **Section 01**: Title / Cover Page (Gold accent, recipient details, test timestamp, fingerprint watermark)
- **Section 02**: Executive Summary & Top Strengths
- **Section 03**: Scientific Basis & Table 1.1 Methodology Disclaimer
- **Section 04**: Fingerprint Biometric Data Table (L1..L5, R1..R5 CADA classification & ridge counts)
- **Section 05**: Brain Lobe Distribution (Prefrontal, Posterior Frontal, Parietal, Temporal, Occipital)
- **Section 06**: Left vs Right Brain Hemisphere Dominance
- **Section 07**: Gardner's 9 Multiple Intelligences (Gold Radar Chart & Ranked Breakdown)
- **Section 08**: 4 Quotients Dashboard (IQ, EQ, AQ, CQ)
- **Section 09**: VAK Learning Style Distribution (Visual, Auditory, Kinesthetic Pie Chart)
- **Section 10**: Big Five Personality Profile (OCEAN Radar)
- **Section 11**: ATD Angle & Physical Reflex Assessment (or Honest Non-Assessment if palm unprovided)
- **Section 12**: Preferred Working & Leadership Style
- **Section 13**: Career Recommendations Matrix (Derived from top 3 MI combinations)
- **Section 14**: Academic / Subject Guidance
- **Section 15**: Relationship & Communication Dynamics
- **Section 16**: Stress Response & Mitigation Strategies
- **Section 17**: Extracurricular & Hobby Suggestions
- **Section 18**: Actionable Personal Development Roadmap
- **Section 19**: Certified Counselor Notes & Sign-off Appendix

## 2. Design & Rendering Standards
- **Palette**: Ivory (`#FAF8F5`), Deep Charcoal (`#1F2937`), Luxury Gold (`#D4AF37`), Dark Navy (`#0F172A`).
- **Typography**: Clean serif/sans pairing, monospaced tabular numerals for all percent and ridge count figures.
- **Charts**: High-DPI Matplotlib vector figures, anti-aliased arcs, polar radar grids with clean metric labels.
- **Zero Fabrication**: Any section lacking biometric input displays clear `N/A - Uncollected` rather than generic placeholders.
