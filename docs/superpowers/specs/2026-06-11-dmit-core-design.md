# DMIT Core — Cross-lateral lobe/hemisphere model, real-data-only, atd-wired

Date: 2026-06-11
Status: Approved (Cycle 1 of 2). Cycle 2 = palm a/t/d computer vision, separate spec.

## Goal

Make the existing fingerprint analysis faithful to the DMIT model from
`dermatoglyphics_reverified_package/` (Ban Jun Sin et al., 2010): a cross-lateral
finger→lobe→hemisphere grid, with no fabricated/default values anywhere, and the
atd (palm) pathway fully wired so Cycle 2 only needs to supply the measured angle.

## The DMIT model being implemented

```
(finger -> lobe)  x  (hand -> hemisphere)  x  (pattern -> style)  x  (TFRC -> capacity)  x  (atd -> speed)
   Table 1.1            Sperry cross-lateral       CADA                ridge count            palm angle
```

- Finger -> lobe (Table 1.1, pp. 4-7): thumb=prefrontal, index=posterior-frontal,
  middle=parietal, ring=temporal, little=occipital.
- Hand -> hemisphere (Sperry, pp. 8/18): contralateral. Right hand -> left hemisphere;
  left hand -> right hemisphere.
- Composition: a 2x5 grid of finger -> (lobe, hemisphere) cells. R1=left-prefrontal,
  L1=right-prefrontal, ... R5=left-occipital, L5=right-occipital.
- atd (pp. 25-30): palm a-t-d triradii angle = brain<->muscle processing speed.

## Section 1 — Cross-lateral lobe/hemisphere grid

- Pipeline derives `hand` (L/R) and `finger_type` (thumb..little) from the L1-R5 slot.
- Each analyzed finger contributes its primary-lobe capacity (mapper brain_mapping at
  that finger's Table-1.1 lobe) to grid[lobe][contralateral_hemisphere].
- Aggregates:
  - lobe.overall = mean of present {left,right} cells for that lobe.
  - left_hemisphere = mean of present right-hand finger lobe capacities.
  - right_hemisphere = mean of present left-hand finger lobe capacities.
  - dominant_hemisphere = "left"/"right"/"balanced" only when both present.
- A cell with no contralateral finger analyzed is ABSENT (None), never zero.

## Section 2 — Real-data-only (no defaults / no fallbacks)

Contract: every feature is a real value or ABSENT. No constant may stand in for an
absent value. A score appears only when every input behind it is real; else N/A.

- Extractor: remove constant exception fallbacks. Feature failure -> absent; core
  classification failure -> finger excluded (warning).
- Mapper: remove `.get(k, 0)` filler. Each trait computed from present terms only
  (weights renormalized over present terms); all terms absent -> trait None.
- Engine: drop the None->0.0 masking and the `overall_quality*0.5` derivation. Pass
  only real values; guarantee every fingerprint-derived key is present (verified by
  test). atd-family keys are the only legitimate absences.
- Aggregation: cells/lobes/hemispheres aggregate present values only; none -> absent.
- Report: absent -> "Not measurable"; empty sections omitted.

### Scenarios

| Scenario | Result |
|---|---|
| 10 fingers + both palms | full profile |
| finger fails classification | finger excluded; its lobe-hemisphere cell N/A; MIs sourced only from it N/A |
| one hand only | contralateral hemisphere present; other hemisphere + comparison N/A |
| no palm | atd N/A; fingerprint scores unaffected |
| single feature fails | only scores solely dependent on it N/A |
| fewer fingers | profile from available; missing cells N/A; no fill |

## Section 3 — atd wiring

- Schema: `AtdAnalysis{left_hand, right_hand: AtdHand, summary}`; AtdHand carries
  angle_deg, range_category, learning_speed, fine_motor_capacity, sensory_sensitivity,
  interpretation. Absent in Cycle 1 (no palm) -> rendered N/A.
- Mapper `map_atd_angle(angle_deg)` implements the paper ranges:
  - <=35 fast/sensitive/nimble; 36-40 optimal fine-motor; 41-45 needs repetition;
    45+ slow/gross-motor; <38 fine-motor+sensitive; >42 both hands gross-muscle.
- Cross-lateral: right-hand palm atd -> left-hemisphere speed; left-hand palm atd ->
  right-hemisphere speed.
- Feeds (only when present): kinesthetic learning, bodily-kinesthetic MI, processing
  speed/attention. Absent -> those compute from fingerprint features and note exclusion.

## Schema changes (api/schemas.py)

- BrainLobeCapacity: all fields Optional; add `dominant_hemisphere: Optional[str]`
  and `lobe_hemispheres: Optional[Dict[str, Dict[str, Optional[float]]]]`.
- AnalysisResult: add `atd_analysis: Optional[AtdAnalysis]`.

## Out of scope (Cycle 2)

- Palm image upload slots, palm a/t/d triradius detection CV, atd angle computation.
- Frontend type/UI updates to consume the new brain structure and atd block.

## Verification

A scenario harness asserts: cross-lateral cells route to the correct hemisphere;
absence propagates (no 0-fill) under missing-finger/one-hand/no-palm; atd module
matches the paper's range table; no fingerprint-derived feature is ever absent at
extension input. Plus full CLI E2E + premium PDF build.
