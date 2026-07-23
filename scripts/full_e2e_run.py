#!/usr/bin/env python3
"""
Full end-to-end run against the live API + SQLite-backed session store:
  1. Create a session
  2. Upload all 10 finger_prints/*Center.bmp + Lpalm.jpg/Rpalm.jpg
  3. Run analysis (no preprocessing — these are scanner BMPs; generate PDF)
  4. Poll until completion
  5. Dump the full JSON result to test_output/full_e2e_result.json
  6. Print a structured summary for manual/automated review
"""
import json
import sys
import time
from pathlib import Path

import httpx

API = "http://127.0.0.1:8001/api"
ROOT = Path(__file__).resolve().parents[1]
FINGERS = sorted(ROOT.glob("finger_prints/*Center.bmp"))
PALMS = {
    "LPALM": ROOT / "finger_prints" / "Lpalm.jpg",
    "RPALM": ROOT / "finger_prints" / "Rpalm.jpg",
}
OUT_DIR = ROOT / "test_output"
OUT_DIR.mkdir(exist_ok=True)


def main() -> int:
    if len(FINGERS) != 10:
        print(f"FAIL: expected 10 finger BMPs, found {len(FINGERS)}")
        return 1
    for pos, p in PALMS.items():
        if not p.exists():
            print(f"FAIL: missing palm image {p}")
            return 1

    with httpx.Client(timeout=180.0) as client:
        print("== Creating session ==")
        r = client.post(f"{API}/sessions", json={"subject_name": "full_e2e_run"})
        r.raise_for_status()
        session_id = r.json()["id"]
        print(f"session_id = {session_id}")

        positions = []
        file_tuples = []
        for p in FINGERS:
            pos = p.stem[:2].upper()
            positions.append(pos)
            file_tuples.append(("files", (f"{pos}.bmp", p.read_bytes(), "image/bmp")))
        for pos, p in PALMS.items():
            positions.append(pos)
            file_tuples.append(("files", (f"{pos}.jpg", p.read_bytes(), "image/jpeg")))

        print(f"== Uploading {len(positions)} images: {positions} ==")
        up = client.post(
            f"{API}/sessions/{session_id}/images",
            data={"finger_positions": ",".join(positions)},
            files=file_tuples,
        )
        up.raise_for_status()
        print(json.dumps(up.json(), indent=2)[:1000])

        print("== Running analysis (use_preprocessing=False, generate_pdf=True) ==")
        run = client.post(
            f"{API}/analysis/run",
            json={"session_id": session_id, "use_preprocessing": False, "generate_pdf": True},
        )
        run.raise_for_status()
        print(run.json())

        data = None
        for i in range(90):
            time.sleep(2)
            res = client.get(f"{API}/analysis/{session_id}")
            res.raise_for_status()
            data = res.json()
            print(f"  [{i*2:>4}s] status={data['status']} progress={data.get('progress')}")
            if data["status"] in ("completed", "failed"):
                break
        else:
            print("FAIL: timed out waiting for completion")
            return 1

        if data["status"] == "failed":
            print("FAIL: analysis failed:", data.get("error_message"))
            return 1

        out_path = OUT_DIR / "full_e2e_result.json"
        out_path.write_text(json.dumps(data, indent=2), encoding="utf-8")
        print(f"\n== Full result written to {out_path} ==")

        # ---- Structured summary -------------------------------------------------
        print("\n=== FINGERS ===")
        for f in data.get("fingers", []):
            print(
                f"  {f.get('finger_position')}: pattern={f.get('pattern_type')} "
                f"ridge_count={f.get('ridge_count')} quality={f.get('image_quality_score')}"
            )

        print("\n=== WARNINGS ===")
        for w in data.get("warnings", []) or []:
            print(f"  ! {w}")
        if not data.get("warnings"):
            print("  (none)")

        print("\n=== BRAIN LOBES (per-lobe left/right/dominant) ===")
        lobes = data.get("brain_lobes") or {}
        for lobe_name, val in lobes.items():
            print(f"  {lobe_name}: {val}")

        print("\n=== MULTIPLE INTELLIGENCES ===")
        mi = data.get("multiple_intelligences") or {}
        for k, v in mi.items():
            print(f"  {k}: {v}")

        print("\n=== LEARNING STYLES ===")
        ls = data.get("learning_styles") or {}
        for k, v in ls.items():
            print(f"  {k}: {v}")

        print("\n=== PERSONALITY ===")
        pb = data.get("personality") or {}
        for k, v in pb.items():
            print(f"  {k}: {v}")

        print("\n=== ATD ANALYSIS ===")
        print(json.dumps(data.get("atd_analysis"), indent=2))

        print("\n=== PALMS ===")
        for palm in data.get("palms") or []:
            print(f"  {palm}")

        exts = data.get("extensions") or []
        print(f"\n=== EXTENSIONS: {len(exts)} registered ===")
        out_of_range = []
        errored = []
        primary_scores = {}
        for ext in exts:
            name = ext.get("name")
            if "error" in ext or ext.get("primary_score") is None:
                errored.append(name)
            primary_scores[name] = ext.get("primary_score")
            for k, v in (ext.get("scores") or {}).items():
                if isinstance(v, (int, float)) and not isinstance(v, bool):
                    if v > 1.0001 or v < -0.0001:
                        out_of_range.append((name, k, v))
            p = ext.get("primary_score")
            if isinstance(p, (int, float)) and (p > 1.0001 or p < -0.0001):
                out_of_range.append((name, "primary_score", p))

        print(f"  errored/missing extensions: {errored}")
        print(f"  out-of-range [0,1] sub-scores: {out_of_range}")

        # Duplicate/clustered primary score detection
        from collections import Counter
        rounded = Counter(round(v, 3) for v in primary_scores.values() if isinstance(v, (int, float)))
        clustered = {v: c for v, c in rounded.items() if c >= 4}
        print(f"  primary_score clusters (>=4 extensions sharing same rounded value): {clustered}")

        print("\n=== CAREER MATCHES ===")
        for cm in data.get("career_matches") or []:
            print(f"  {cm}")

        print("\n=== PDF REPORT ===")
        print(f"  report_url: {data.get('report_url')}")
        print(f"  processing_time_ms: {data.get('processing_time_ms')}")
        print(f"  total_features_extracted: {data.get('total_features_extracted')}")

        return 0


if __name__ == "__main__":
    sys.exit(main())
