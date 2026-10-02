import sqlite3
import json

conn = sqlite3.connect('backend/data/sessions.db')
cursor = conn.cursor()
rows = cursor.execute("SELECT id, data FROM sessions WHERE data LIKE '%smith%' LIMIT 1").fetchall()
if not rows:
    rows = cursor.execute("SELECT id, data FROM sessions ORDER BY updated_at DESC LIMIT 1").fetchall()

for row in rows:
    sid = row[0]
    data = json.loads(row[1])
    print(f"=== SESSION {sid} ===")
    print("Subject:", data.get("subject_name"))
    print("Keys in data:", list(data.keys()))
    res = data.get("result")
    if res and isinstance(res, dict):
        fingers = res.get("fingers", [])
        print(f"Fingers count: {len(fingers)}")
        import sys
        sys.path.insert(0, 'backend')
        from premium_pdf_report import PremiumReportGenerator
        out = PremiumReportGenerator.create_report(pipeline_data=res, output_path="output/test_tfrc_smith.pdf", session=data)
        print("GENERATED REPORT:", out)



print("\n--- ALL SESSIONS IN DB ---")
all_rows = cursor.execute("SELECT id, data FROM sessions").fetchall()
for sid, raw in all_rows:
    d = json.loads(raw)
    print(f"ID: {sid} | Name: {d.get('subject_name')} | Status: {d.get('status')} | Report: {bool(d.get('report_path'))}")

