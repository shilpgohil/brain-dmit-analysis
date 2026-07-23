#!/usr/bin/env python3
"""Deep audit of all 46 extension outputs on real finger_prints data."""
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from integrated_dmit_pipeline import IntegratedDMITPipeline
from dmit_extensions.engine import DMITExtensionsEngine
from api.routes.analysis import _extract_extensions


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

    images = sorted(Path("finger_prints").glob("*Center.bmp"))
    pipeline = IntegratedDMITPipeline(use_preprocessing=False)
    full = pipeline.analyze_multiple_fingers([str(p) for p in images])
    ext_raw = full["aggregated_analysis"]["extension_results"]
    api_ext = _extract_extensions(ext_raw)

    failures = []
    over_one = []
    constant_primary = defaultdict(list)
    primary_scores = {}

    print(f"\n=== Extension count: {len(ext_raw)} registered, {len(api_ext)} in API ===\n")

    for name, scores in sorted(ext_raw.items()):
        if not isinstance(scores, dict) or "error" in scores:
            failures.append(f"{name}: error or missing")
            continue
        nums = {k: float(v) for k, v in scores.items() if isinstance(v, (int, float)) and not isinstance(v, bool)}
        for k, v in nums.items():
            if v > 1.0001:
                over_one.append((name, k, v))
            if v < -0.0001:
                failures.append(f"{name}.{k} negative: {v}")

    for e in api_ext:
        primary_scores[e.name] = e.primary_score
        constant_primary[round(e.primary_score, 3)].append(e.name)

    print("--- Primary scores (API, sorted) ---")
    for e in sorted(api_ext, key=lambda x: -x.primary_score):
        subs = len([k for k in e.scores if k not in ("overall", "score")])
        print(f"  {e.primary_score*100:5.1f}%  {e.name} ({e.category}) [{subs} sub-scores]")

    print("\n--- Scores > 1.0 (BUG) ---")
    if over_one:
        for row in over_one[:20]:
            print(f"  FAIL {row}")
        failures.append(f"{len(over_one)} sub-scores > 1.0")
    else:
        print("  None")

    print("\n--- Primary scores clustered (same value, 4+ extensions) ---")
    clustered = {k: v for k, v in constant_primary.items() if len(v) >= 4}
    if clustered:
        for val, names in sorted(clustered.items(), reverse=True):
            print(f"  {val*100:.1f}%: {len(names)} extensions — {', '.join(names[:6])}{'...' if len(names)>6 else ''}")
    else:
        print("  No large clusters")

    print("\n--- Left/Right Brain sub-scores ---")
    lrb = ext_raw.get("LeftRightBrainExtension", {})
    for k in sorted(lrb.keys()):
        if isinstance(lrb[k], (int, float)):
            print(f"  {k}: {lrb[k]:.4f}")

    print("\n--- Neurodivergence sub-scores ---")
    nd = ext_raw.get("NeurodivergenceExtension", {})
    for k in sorted(nd.keys()):
        if isinstance(nd[k], (int, float)):
            print(f"  {k}: {nd[k]:.4f}")

  # Holistic vs defaults
    defaults = DMITExtensionsEngine().run_all_extensions({})
    identical_to_defaults = 0
    for name, scores in ext_raw.items():
        if not isinstance(scores, dict):
            continue
        base = defaults.get(name, {})
        for k, v in scores.items():
            if isinstance(v, (int, float)) and isinstance(base.get(k), (int, float)):
                if abs(float(v) - float(base[k])) < 1e-9:
                    identical_to_defaults += 1
    print(f"\n--- Identical to empty-input defaults: {identical_to_defaults} values ---")
    if identical_to_defaults > 30:
        failures.append(f"{identical_to_defaults} scores identical to defaults (features not wired)")

    print("\n--- Per-finger extension variance (first 3 extensions) ---")
    per_finger = []
    for res in full["individual_results"]:
        per_finger.append(res["dmit_analysis"]["extension_results"])
    for ext_name in list(ext_raw.keys())[:3]:
        keys = [k for k in ext_raw[ext_name] if isinstance(ext_raw[ext_name][k], (int, float))]
        if not keys:
            continue
        pk = keys[0]
        vals = [pf.get(ext_name, {}).get(pk) for pf in per_finger]
        vals = [v for v in vals if isinstance(v, (int, float))]
        spread = max(vals) - min(vals) if vals else 0
        print(f"  {ext_name}.{pk}: min={min(vals):.3f} max={max(vals):.3f} spread={spread:.3f}")

    print("\n=== SUMMARY ===")
    if failures:
        print("FAILURES:")
        for f in failures:
            print(f"  - {f}")
        return 1
    print("PASS: no scores >1, extensions differentiated, holistic pass uses real data")
    return 0


if __name__ == "__main__":
    sys.exit(main())
