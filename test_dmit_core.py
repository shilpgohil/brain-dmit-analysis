#!/usr/bin/env python3
"""Verification for the DMIT core: cross-lateral grid, real-data-only, atd wiring."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

    from integrated_dmit_pipeline import IntegratedDMITPipeline
    from dmit_intelligence_mapper import map_atd_angle
    from api.routes.analysis import _extract_brain_lobes, _extract_atd

    fails = []

    def chk(name, ok, detail=""):
        print(f"  {'PASS' if ok else 'FAIL'}  {name}" + (f"  ({detail})" if detail else ""))
        if not ok:
            fails.append(name)

    images = sorted(Path("finger_prints").glob("*.bmp"))
    pipe = IntegratedDMITPipeline(use_preprocessing=False)

    print("\n--- 1. atd range table matches the paper (pp. 29-30) ---")
    chk("<=35 fast/sensitive", map_atd_angle(33)["range_category"] == "<=35"
        and map_atd_angle(33)["learning_speed"] > map_atd_angle(43)["learning_speed"])
    chk("36-40 optimal", map_atd_angle(38)["range_category"] == "36-40")
    chk("41-45 needs repetition", map_atd_angle(43)["range_category"] == "41-45")
    chk("45+ slow/gross-motor", map_atd_angle(50)["range_category"] == "45+"
        and map_atd_angle(50)["learning_speed"] < map_atd_angle(38)["learning_speed"])
    chk("absent angle -> None (no fabrication)", map_atd_angle(None) is None)
    chk("monotonic: smaller angle -> faster", all(
        map_atd_angle(a)["learning_speed"] >= map_atd_angle(b)["learning_speed"]
        for a, b in [(33, 38), (38, 43), (43, 50)]))

    print("\n--- 2. Full 10-finger cross-lateral grid ---")
    full = pipe.analyze_multiple_fingers([str(p) for p in images])
    agg = full["aggregated_analysis"]["dmit_profile"]
    bl = _extract_brain_lobes(agg)
    chk("both hemispheres present (10 fingers)", bl.left_hemisphere is not None and bl.right_hemisphere is not None,
        f"L={bl.left_hemisphere} R={bl.right_hemisphere}")
    chk("dominant_hemisphere set", bl.dominant_hemisphere in ("left", "right", "balanced"), bl.dominant_hemisphere)
    chk("per-lobe L/R present for all 5 lobes",
        bl.lobe_hemispheres is not None and all(
            bl.lobe_hemispheres[l].left is not None and bl.lobe_hemispheres[l].right is not None
            for l in ("prefrontal_lobe", "posterior_frontal", "parietal_lobe", "temporal_lobe", "occipital_lobe")))
    chk("atd absent (no palm) -> N/A, not fabricated", _extract_atd(agg) is None)
    chk("existential MI absent (not in paper)", agg["multiple_intelligences"].get("existential") is None)

    print("\n--- 3. Cross-lateral routing correctness (R-hand -> LEFT hemisphere) ---")
    # Right thumb only -> should populate prefrontal LEFT, leave prefrontal RIGHT absent.
    r1 = [str(p) for p in images if p.name.upper().startswith("R1")]
    res_r1 = pipe.analyze_multiple_fingers(r1)
    bl_r1 = _extract_brain_lobes(res_r1["aggregated_analysis"]["dmit_profile"])
    pf = bl_r1.lobe_hemispheres["prefrontal_lobe"]
    chk("R1 routes to LEFT prefrontal only", pf.left is not None and pf.right is None,
        f"left={pf.left} right={pf.right}")
    chk("R1 -> left hemisphere present, right hemisphere absent",
        bl_r1.left_hemisphere is not None and bl_r1.right_hemisphere is None)
    chk("single hand -> dominant_hemisphere None (cannot compare)", bl_r1.dominant_hemisphere is None)

    print("\n--- 4. Left thumb -> RIGHT prefrontal (contralateral) ---")
    l1 = [str(p) for p in images if p.name.upper().startswith("L1")]
    res_l1 = pipe.analyze_multiple_fingers(l1)
    bl_l1 = _extract_brain_lobes(res_l1["aggregated_analysis"]["dmit_profile"])
    pf_l = bl_l1.lobe_hemispheres["prefrontal_lobe"]
    chk("L1 routes to RIGHT prefrontal only", pf_l.right is not None and pf_l.left is None,
        f"left={pf_l.left} right={pf_l.right}")

    print("\n--- 5. Real-data-only: no fabricated constants in features ---")
    import cv2
    ex = pipe.feature_extractor
    img = cv2.imread(r1[0], cv2.IMREAD_GRAYSCALE)
    cf = ex.extract_optimized_features(img)["consolidated_features"]
    absent = [k for k, v in cf.items() if v is None]
    expected_absent = {"quantum", "criticality", "atd", "avalanche", "consciousness", "microtubule",
                       "nuclear", "orchestrated", "edge_of_chaos", "scale_free", "power_law",
                       "critical_slowing", "network_efficiency"}
    unexpected = [k for k in absent if not any(t in k for t in expected_absent)]
    chk("only pseudoscience/palm features are absent", not unexpected, f"unexpected absent: {unexpected}")

    print("\n--- 6. atd injected -> analysis present + cross-lateral summary ---")
    pipe.session_atd = {"atd_left_deg": 33.0, "atd_right_deg": 47.0}
    res_atd = pipe.analyze_multiple_fingers([str(p) for p in images])
    atd = _extract_atd(res_atd["aggregated_analysis"]["dmit_profile"])
    chk("atd analysis present when provided", atd is not None and atd.left_hand is not None and atd.right_hand is not None)
    chk("left palm 33deg -> <=35 fast", atd and atd.left_hand.range_category == "<=35")
    chk("right palm 47deg -> 45+ slow", atd and atd.right_hand.range_category == "45+")
    pipe.session_atd = None

    print("\n" + ("ALL CHECKS PASSED" if not fails else f"FAILURES: {fails}"))
    return 0 if not fails else 1


if __name__ == "__main__":
    raise SystemExit(main())
