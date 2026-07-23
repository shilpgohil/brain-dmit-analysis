#!/usr/bin/env python3
import json
import sqlite3
import sys
import time
from pathlib import Path

import httpx

SESSION = sys.argv[1] if len(sys.argv) > 1 else "ad0f54d9-e422-4745-ab7c-1b67dbfb1d90"
API = "http://127.0.0.1:8001/api"

row = sqlite3.connect("data/sessions.db").execute(
    "SELECT data FROM sessions WHERE id=?", (SESSION,)
).fetchone()
if not row:
    print("session not found")
    sys.exit(1)

data = json.loads(row[0])
paths = data.get("image_paths", [])
print(f"paths: {len(paths)}, exist: {sum(Path(p).exists() for p in paths)}")

if not paths or not all(Path(p).exists() for p in paths):
    print("cannot re-run — upload images missing")
    sys.exit(1)

with httpx.Client(timeout=120) as client:
    client.post(
        f"{API}/analysis/run",
        json={"session_id": SESSION, "use_preprocessing": True, "generate_pdf": False},
    ).raise_for_status()
    for _ in range(40):
        time.sleep(2)
        res = client.get(f"{API}/analysis/{SESSION}").json()
        if res["status"] in ("completed", "failed"):
            break
    for f in res.get("fingers", []):
        print(f"{f['finger_position']}: ridges={f['ridge_count']} pattern={f['pattern_type']}")
    print("warnings:", res.get("warnings"))
