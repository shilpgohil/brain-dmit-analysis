#!/usr/bin/env python3
"""Verification harness for the backend logic-correctness fixes (June 2026).

Checks, on real scanner prints:
1. Holistic extension pass receives real averaged biometric features
   (extension scores must differ from a defaults-only run).
2. ProblemSolvingExtension is registered and produces problem_solving_score.
3. Neurodivergence tfrc_score is no longer stuck at 1.0.
4. Extractor exposes pattern_classification detail with singular points.
5. Pattern-aware detectors: double_loop/peacock only fire with singular-point
   or subtype evidence.
6. API normalizers: pattern_type resolved (not 'unknown'), quality populated,
   hemispheres non-zero, singular points mapped, primary scores use *_score/_index.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

    from integrated_dmit_pipeline import IntegratedDMITPipeline
    from dmit_extensions.engine import DMITExtensionsEngine
    from api.routes.analysis import (
        _extract_brain_lobes,
        _extract_extensions,
        _normalize_finger_results,
    )

    failures = []

    def check(name, ok, detail=""):
        print(f"  {'PASS' if ok else 'FAIL'}  {name}" + (f"  ({detail})" if detail else ""))
        if not ok:
            failures.append(name)

    images = sorted(Path("finger_prints").glob("*.bmp"))
    assert len(images) >= 10, "need finger_prints/ test set"

    # Scanner BMPs: skip the photo->fingerprint preprocessing
    pipeline = IntegratedDMITPipeline(use_preprocessing=False)
    full = pipeline.analyze_multiple_fingers([str(p) for p in images])
    agg = full["aggregated_analysis"]
    ext = agg["extension_results"]
    individual = full["individual_results"]

    print("\n--- 1. Holistic extension pass uses real features ---")
    defaults_only = DMITExtensionsEngine().run_all_extensions({})
    diff = 0
    for name, scores in ext.items():
        if not isinstance(scores, dict) or "error" in scores:
            continue
        base = defaults_only.get(name, {})
        for k, v in scores.items():
            if isinstance(v, (int, float)) and isinstance(base.get(k), (int, float)):
                if abs(float(v) - float(base[k])) > 1e-6:
                    diff += 1
    check("extension scores differ from defaults-only run", diff > 50, f"{diff} differing values")

    print("\n--- 2. ProblemSolvingExtension registered ---")
    ps = ext.get("ProblemSolvingExtension", {})
    check("ProblemSolvingExtension present", isinstance(ps, dict) and "problem_solving_score" in ps,
          f"score={ps.get('problem_solving_score')}")

    print("\n--- 3. Neurodivergence tfrc_score sane ---")
    nd = ext.get("NeurodivergenceExtension", {})
    check("tfrc_score in {0.5, 1.0} and index < 1.0",
          nd.get("tfrc_score") in (0.5, 1.0) and 0.0 <= nd.get("neurodivergence_index", 1.0) < 1.0,
          f"tfrc_score={nd.get('tfrc_score')}, index={nd.get('neurodivergence_index'):.3f}")

    print("\n--- 4. Classification detail + singular points exposed ---")
    with_detail = [r for r in individual if r["feature_extraction"].get("pattern_classification")]
    check("pattern_classification present on fingers", len(with_detail) == len(individual),
          f"{len(with_detail)}/{len(individual)}")
    any_points = any(
        (r["feature_extraction"]["pattern_classification"] or {}).get("singular_points", {}).get("cores")
        or (r["feature_extraction"]["pattern_classification"] or {}).get("singular_points", {}).get("deltas")
        for r in with_detail
    )
    check("singular point coordinates present on at least one finger", any_points)

    print("\n--- 5. Pattern-aware detectors consistent with classifier ---")
    inconsistent = 0
    for r in individual:
        feats = r["feature_extraction"]["consolidated_features"]
        cls = r["feature_extraction"].get("pattern_classification") or {}
        if feats.get("double_loop_detected") == 1.0:
            if not (cls.get("subtype") in ("Wc", "Wd", "Wi")
                    or (cls.get("core_count", 0) >= 2 and cls.get("triradii_count", 0) >= 2)):
                inconsistent += 1
        if feats.get("peacock_eye_detected") == 1.0 and cls.get("family") != "whorl" \
                and cls.get("subtype") not in ("Wp", "Rp"):
            inconsistent += 1
    check("no detector fires without classifier evidence", inconsistent == 0,
          f"{inconsistent} inconsistencies")
    dl_count = sum(1 for r in individual
                   if r["feature_extraction"]["consolidated_features"].get("double_loop_detected") == 1.0)
    pe_count = sum(1 for r in individual
                   if r["feature_extraction"]["consolidated_features"].get("peacock_eye_detected") == 1.0)
    print(f"        double loops detected: {dl_count}/10, peacock eyes: {pe_count}/10 "
          "(old code: ~10/10 false positives)")

    print("\n--- 6. API normalizers ---")
    fingers = _normalize_finger_results(individual)
    pattern_ok = sum(1 for f in fingers if f.pattern_type.value != "unknown")
    check("pattern_type resolved for all fingers", pattern_ok == len(fingers),
          f"{pattern_ok}/{len(fingers)}: " + ",".join(f.pattern_type.value[0] for f in fingers))
    quality_ok = sum(1 for f in fingers if f.quality_score is not None and f.quality_tier)
    check("quality score+tier populated", quality_ok == len(fingers), f"{quality_ok}/{len(fingers)}")
    sp_ok = sum(1 for f in fingers if f.singular_points)
    check("singular points populated on fingers with cores/deltas", sp_ok > 0, f"{sp_ok}/{len(fingers)}")
    subtype_ok = sum(1 for f in fingers if f.pattern_subtype)
    check("pattern_subtype populated", subtype_ok == len(fingers), f"{subtype_ok}/{len(fingers)}")

    lobes = _extract_brain_lobes(agg["dmit_profile"])
    check("hemispheres non-zero via *_bias fallback",
          lobes is not None and (lobes.left_hemisphere > 0 or lobes.right_hemisphere > 0),
          f"L={lobes.left_hemisphere:.2f} R={lobes.right_hemisphere:.2f}")

    api_ext = _extract_extensions(ext)
    eq = next((e for e in api_ext if e.name == "Emotional Intelligence"), None)
    check("EQ primary_score = emotional_intelligence_score",
          eq is not None and abs(eq.primary_score
                                 - ext["EmotionalIntelligenceExtension"]["emotional_intelligence_score"]) < 1e-9,
          f"primary={eq.primary_score:.3f}" if eq else "missing")

    print("\n" + ("ALL CHECKS PASSED" if not failures else f"FAILURES: {failures}"))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
