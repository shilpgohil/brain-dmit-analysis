# DMIT Biometrics & Lobe Mapping Rules

## 1. Table 1.1 Finger-to-Brain Correlation Architecture
The spine of the entire DMIT scoring engine is Table 1.1 from the foundational research literature. The correlation matrix is non-negotiable:

| Digit Slot | Dominant Hand | Brain Region | Primary Functional Focus | Primary MI Dimensions |
| :--- | :--- | :--- | :--- | :--- |
| **L1** | Left Thumb | Right Prefrontal | Goal setting, vision, leadership, charisma | Interpersonal Intelligence |
| **R1** | Right Thumb | Left Prefrontal | Self-reflection, planning, self-discipline | Intrapersonal Intelligence |
| **L2** | Left Index | Right Posterior Frontal | Spatial concepts, creative imagination | Visual-Spatial Intelligence |
| **R2** | Right Index | Left Posterior Frontal | Logical reasoning, calculations, syntax | Logical-Mathematical Intelligence |
| **L3** | Left Middle | Right Parietal | Rhythm, physical feel, 3D motor coordination | Bodily-Kinesthetic (Gross Motor) |
| **R3** | Right Middle | Left Parietal | Fine motor control, manipulation, dexterity | Bodily-Kinesthetic (Fine Motor) |
| **L4** | Left Ring | Right Temporal | Tone discrimination, musicality, environmental audio | Musical Intelligence |
| **R4** | Right Ring | Left Temporal | Language comprehension, verbal memory, vocabulary | Linguistic Intelligence |
| **L5** | Left Little | Right Occipital | Visual aesthetics, color sensitivity, art appreciation | Spatial / Visual Perception |
| **R5** | Right Little | Left Occipital | Visual observation, reading, detail discrimination | Naturalistic & Visual Memory |

### Weighting Constraint
- Primary digit contributes **100%** to its respective brain lobe.
- Secondary/cross-lobe contributions are strictly damped by **0.20** ($\times 0.20$).
- Naive arithmetic averaging across digits is strictly forbidden.

---

## 2. CADA Pattern Classification Taxonomy
Every fingerprint belongs to one of four families, evaluated via singular points (Cores & Deltas):

1. **Arch Family (0 Cores, 0 Deltas)**:
   - Subtypes: Simple Arch, Tented Arch, Enclosed Arch.
   - Behavioral Profile: Methodical, security-oriented, highly practical, high perseverance, low risk tolerance.
   - Boosts: Conscientiousness, methodical execution.
2. **Loop Family (1 Core, 1 Delta)**:
   - Subtypes: Ulnar Loop (flows toward little finger), Radial Loop (flows toward thumb), Falling Loop.
   - Behavioral Profile: Adaptable, empathetic, social, emotionally responsive, highly communicative.
   - Boosts: Interpersonal, Linguistic, Agreeableness.
3. **Whorl Family (>=1 Core, 2 Deltas)**:
   - Subtypes: Plain/Target Whorl, Spiral, Double Loop / Composite, Central Pocket (Peacock's Eye).
   - Behavioral Profile: Independent, goal-driven, self-motivated, high cognitive focus, original.
   - Boosts: Intrapersonal, Logical-Mathematical, Openness.
4. **Accidental Family (Complex / >=3 Deltas)**:
   - Subtypes: Combination patterns, malformations.
   - Behavioral Profile: Polymathic, non-traditional thinking, highly adaptive multi-tasker.

---

## 3. Total Finger Ridge Count (TFRC) Standards
- TFRC is calculated by counting ridges along the line of intersection between the core and the delta triradius.
- High TFRC (>140): High innate learning speed, high brain cortex capacity, thrives in information-dense environments.
- Moderate TFRC (90-140): Balanced learning capacity, steady pacing, stable retention.
- Low TFRC (<90): Step-by-step learner, requires visual/experiential anchors, thrives with structured repetition.

---

## 4. Palm ATD Angle Invariant
- Measured at the palm triradius between point `t` (near wrist) and triradii `a` (below index) and `d` (below little finger).
- **ATD < 35°**: Superior neuromuscular reflex, high agility, athletic aptitude.
- **ATD 35° - 40°**: Standard healthy neuromuscular coordination.
- **ATD 41° - 45°**: Deliberate, contemplative movement; benefits from rhythm training.
- **ATD > 45°**: Slower physical motor response; potential fatigue susceptibility.
- **CRITICAL INVARIANT**: If palm prints (`LPALM`, `RPALM`) are not provided, ATD Angle MUST return `None` and display `N/A - Uncollected` in all UI and reports. Never fabricate palm measurements.
