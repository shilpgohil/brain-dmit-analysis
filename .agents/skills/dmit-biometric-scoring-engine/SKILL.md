---
name: dmit-biometric-scoring-engine
description: >
  Biometric feature scoring, CADA pattern classification, Total Finger Ridge Count (TFRC),
  and Table 1.1 finger-to-brain-lobe mapping for the DMIT Analysis Platform.
  Use when computing multiple intelligence scores, brain lobe distributions, VAK learning styles,
  quotients (IQ, EQ, AQ, CQ), or Big Five personality dimensions from fingerprint biometric features.
---

# DMIT Biometric Scoring Engine

## Core Scientific Architecture
1. **CADA Pattern Classification**:
   - Arch (0 cores, 0 triradii): Conscientious, orderly, secure, high perseverance.
   - Loop (1 core, 1 triradius): Adaptable, emotionally responsive, communicative, high interpersonal empathy.
   - Whorl (>=1 core, 2 triradii): Independent, goal-driven, strong analytical and spatial cognition.
   - Accidental (complex / >=3 triradii): Multimodal, non-linear thinking.
2. **Table 1.1 Finger-to-Lobe Mapping**:
   - `L1`/`R1` (Thumb) -> Prefrontal Lobe (Executive, Leadership, Inter/Intrapersonal MI)
   - `L2`/`R2` (Index) -> Posterior Frontal Lobe (Logic-Mathematical, Sequential, Spatial Conception)
   - `L3`/`R3` (Middle) -> Parietal Lobe (Bodily-Kinesthetic, Somatosensory, Motor Skills)
   - `L4`/`R4` (Ring) -> Temporal Lobe (Linguistic, Musical, Auditory Processing)
   - `L5`/`R5` (Little) -> Occipital Lobe (Visual, Spatial Observation, Aesthetics)
3. **Aggregation Rules**:
   - Each lobe score is primarily driven by its corresponding finger slot; non-primary finger contributions are damped ($\times 0.20$).
   - Never perform naive unweighted averaging across all fingers.
   - Real-data-only policy: missing finger slots must be honestly reported; never fabricate ridge counts or missing prints.
