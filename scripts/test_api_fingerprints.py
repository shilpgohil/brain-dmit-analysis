#!/usr/bin/env python3
"""E2E: upload finger_prints BMPs via API and verify ridge counts."""
import json
import sys
import time
from pathlib import Path

import httpx

API = "http://127.0.0.1:8001/api"
ROOT = Path(__file__).resolve().parents[1]
PRINTS = sorted(ROOT.glob("finger_prints/*Center.bmp"))


def main() -> int:
    if len(PRINTS) < 10:
        print("FAIL: need 10 finger_prints/*Center.bmp")
        return 1

    with httpx.Client(timeout=120.0) as client:
        r = client.post(f"{API}/sessions", json={"subject_name": "api_ridge_test"})
        r.raise_for_status()
        session_id = r.json()["id"]

        positions = []
        file_tuples = []
        for p in PRINTS:
            pos = p.stem[:2].upper()
            positions.append(pos)
            file_tuples.append(("files", (f"{pos}.bmp", p.read_bytes(), "image/bmp")))

        up = client.post(
            f"{API}/sessions/{session_id}/images",
            data={"finger_positions": ",".join(positions)},
            files=file_tuples,
        )
        up.raise_for_status()

        run = client.post(
            f"{API}/analysis/run",
            json={"session_id": session_id, "use_preprocessing": True, "generate_pdf": False},
        )
        run.raise_for_status()

        for _ in range(60):
            time.sleep(2)
            res = client.get(f"{API}/analysis/{session_id}")
            res.raise_for_status()
            data = res.json()
            if data["status"] == "completed":
                break
            if data["status"] == "failed":
                print("FAIL: analysis failed", data.get("error_message"))
                return 1
        else:
            print("FAIL: timeout")
            return 1

        fingers = data.get("fingers", [])
        failures = []
        for f in fingers:
            pos = f.get("finger_position")
            ridge = f.get("ridge_count")
            pat = f.get("pattern_type")
            print(f"  {pos}: ridges={ridge} pattern={pat}")
            if not ridge or ridge == 0:
                failures.append(pos)
            if pat == "arch":
                failures.append(f"{pos}_arch")

        if failures:
            print("FAIL: bad fingers:", failures)
            print("warnings:", data.get("warnings"))
            return 1

        print("PASS: all 10 fingers have ridge counts and non-arch patterns")
        return 0


if __name__ == "__main__":
    sys.exit(main())
