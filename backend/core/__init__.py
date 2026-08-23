"""
core — DMIT biometric analysis pipeline modules.

The four central Python modules live here:
  - integrated_dmit_pipeline        main pipeline orchestrator
  - optimized_feature_extractor_clean  raw feature extraction from images
  - dmit_intelligence_mapper        fingerprint → brain/MI/personality mapping
  - pattern_classifier              fingerprint pattern classification

Root-level shim files re-export from this package so legacy imports remain
unchanged during and after the migration period.
"""
