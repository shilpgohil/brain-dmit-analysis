#!/usr/bin/env python3
"""E2E: API server -> pipeline -> PremiumReportGenerator PDF (cover watermark)."""

from __future__ import annotations

import sys
import time
from pathlib import Path

import httpx

ROOT = Path(__file__).resolve().parents[1]
FINGER_DIR = ROOT / "finger_prints"
BASE = "http://127.0.0.1:8001/api"
OUT_PDF = ROOT / "test_server_premium_report.pdf"
POLL_SEC = 3
MAX_WAIT = 600


def slot_from_name(name: str) -> str:
    # L1Center.bmp -> L1
    stem = Path(name).stem
    for prefix in ("L", "R"):
        if stem.upper().startswith(prefix) and len(stem) >= 2:
            return stem[:2].upper()
    return stem[:2].upper() if len(stem) >= 2 else stem.upper()


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

    if not FINGER_DIR.is_dir():
        print(f"Missing {FINGER_DIR}")
        return 1

    images = sorted(FINGER_DIR.glob("*.bmp"))
    if len(images) < 10:
        print(f"Need 10 BMP files in {FINGER_DIR}, found {len(images)}")
        return 1

    with httpx.Client(timeout=120.0) as client:
        health = client.get(f"{BASE}/health")
        health.raise_for_status()
        print("API health:", health.json().get("status", "ok"))

        sess = client.post(
            f"{BASE}/sessions",
            json={
                "subject_name": "Cover Watermark Test",
                "subject_age": 14,
                "subject_gender": "Male",
                "notes": "Server E2E premium PDF",
            },
        )
        sess.raise_for_status()
        session_id = sess.json()["id"]
        print("Session:", session_id)

        positions = [slot_from_name(p.name) for p in images]
        multipart = [("files", (p.name, p.open("rb"), "image/bmp")) for p in images]
        try:
            up = client.post(
                f"{BASE}/sessions/{session_id}/images",
                files=multipart,
                data={"finger_positions": ",".join(positions)},
            )
        finally:
            for _, (_, fh, _) in multipart:
                fh.close()
        up.raise_for_status()
        print("Uploaded:", up.json())

        run = client.post(
            f"{BASE}/analysis/run",
            json={
                "session_id": session_id,
                "use_preprocessing": True,
                "generate_pdf": True,
            },
        )
        run.raise_for_status()
        print("Analysis started:", run.json())

        deadline = time.time() + MAX_WAIT
        while time.time() < deadline:
            res = client.get(f"{BASE}/analysis/{session_id}")
            res.raise_for_status()
            data = res.json()
            status = data.get("status")
            print(f"  status={status}")
            if status == "completed":
                break
            if status == "failed":
                print("FAILED:", data.get("error_message"), data.get("warnings"))
                return 1
            time.sleep(POLL_SEC)
        else:
            print("Timed out waiting for analysis")
            return 1

        if not data.get("report_url"):
            print("No report_url; warnings:", data.get("warnings"))
            return 1

        pdf = client.get(f"{BASE}/analysis/{session_id}/report/download")
        pdf.raise_for_status()
        OUT_PDF.write_bytes(pdf.content)
        print(f"Saved {OUT_PDF} ({len(pdf.content)} bytes)")
        print("Open page 1 to verify brain cover watermark.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
