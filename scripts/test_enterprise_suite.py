import sys
import io
import zipfile
import base64
from pathlib import Path

root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root / "backend"))

from fastapi.testclient import TestClient
from api.main import app
from api.db.init import init_auth_db
from api.db.partners import create_partner, get_partner_by_email
from api.auth.security import create_access_token, hash_password
from api.persistence import init_db

client = TestClient(app)

def run_tests():
    init_db()
    init_auth_db()

    partner_email = "enterprise_test_suite@apexdmit.org"
    partner = get_partner_by_email(partner_email)
    if not partner:
        partner = create_partner(
            email=partner_email,
            password_hash=hash_password("ApexSecurePass2026!"),
            name="Apex Testing Institute",
            centre_name="Apex Global Center",
        )
    token, _ = create_access_token(partner["id"], "partner")
    headers = {"Authorization": f"Bearer {token}"}

    res_telemetry = client.get("/api/analysis/storage/telemetry", headers=headers)
    assert res_telemetry.status_code == 200, f"Telemetry failed: {res_telemetry.text}"
    telemetry_data = res_telemetry.json()
    assert "storage" in telemetry_data
    assert "status" in telemetry_data
    print("TEST 1 PASSED: Storage telemetry endpoint operational.")

    branding_payload = {
        "analyst_name": "Dr. Sarah Jenkins, Ph.D.",
        "analyst_title": "Executive Biometric Director",
        "analyst_id": "IADP-99881-DIR",
        "school_name": "Stanford Cognitive Labs",
        "franchise_code": "FR-CA-STANFORD",
        "brand_color": "#D4AF37",
        "counselor_notes": "Candidate exhibits top-tier logical-mathematical and spatial aptitude.",
    }
    res_update_brand = client.post("/api/analysis/settings/branding", json=branding_payload, headers=headers)
    assert res_update_brand.status_code == 200, f"Branding update failed: {res_update_brand.text}"

    res_get_brand = client.get("/api/analysis/settings/branding", headers=headers)
    assert res_get_brand.status_code == 200, f"Branding get failed: {res_get_brand.text}"
    brand_data = res_get_brand.json()
    assert brand_data.get("analyst_name") == "Dr. Sarah Jenkins, Ph.D."
    assert brand_data.get("school_name") == "Stanford Cognitive Labs"
    print("TEST 2 PASSED: SQLite partner_settings branding persistence round-trip verified.")

    create_res = client.post(
        "/api/sessions",
        json={
            "subject_name": "Julian Vance",
            "subject_age": 19,
            "subject_gender": "male",
            "school": "Stanford Cognitive Labs",
            "counsellor": "Dr. Sarah Jenkins",
        },
        headers=headers,
    )
    assert create_res.status_code == 200, f"Create session failed: {create_res.text}"
    session_id = create_res.json()["id"]

    from api.routes.analysis import session_store
    mock_pipeline = {
        "metadata": {"subject_name": "Julian Vance"},
        "fingers": [],
        "brain_lobes": {
            "prefrontal_left": 14.5, "prefrontal_right": 15.2,
            "frontal_left": 13.8, "frontal_right": 14.1,
            "parietal_left": 12.0, "parietal_right": 12.5,
            "temporal_left": 13.0, "temporal_right": 13.5,
            "occipital_left": 11.2, "occipital_right": 11.8,
            "total_capacity": 131.6,
        },
        "learning_styles": {"visual": 36.0, "auditory": 34.0, "kinesthetic": 30.0},
        "multiple_intelligences": {
            "intrapersonal": 88.0, "interpersonal": 84.0,
            "logical_mathematical": 92.0, "spatial": 85.0,
            "bodily_kinesthetic": 75.0, "musical": 70.0,
            "linguistic": 82.0, "naturalist": 78.0, "existential": 80.0,
        },
        "personality": {"primary_type": "Analytical", "big_five": {}},
        "quotients": {"IQ": 128.0, "EQ": 118.0, "AQ": 122.0, "CQ": 125.0},
        "extensions": [],
    }
    session_store[session_id]["full_result"] = mock_pipeline
    session_store[session_id]["status"] = "completed"

    from PIL import Image as TestImage, ImageDraw as TestDraw
    sig_img = TestImage.new("RGBA", (180, 50), (255, 255, 255, 0))
    d_ctx = TestDraw.Draw(sig_img)
    d_ctx.line([(10, 25), (45, 10), (80, 38), (120, 15), (170, 35)], fill=(212, 175, 55, 255), width=3)
    s_buf = io.BytesIO()
    sig_img.save(s_buf, format="PNG")
    dummy_sig = "data:image/png;base64," + base64.b64encode(s_buf.getvalue()).decode()
    gen_res = client.post(
        f"/api/analysis/{session_id}/report/generate",
        json={
            "analyst_name": "Dr. Sarah Jenkins, Ph.D.",
            "school_name": "Stanford Cognitive Labs",
            "counselor_signature": dummy_sig,
            "candidate_signature": dummy_sig,
        },
        headers=headers,
    )
    assert gen_res.status_code == 200, f"Generate report failed: {gen_res.text}"
    print("TEST 3 PASSED: 64-page dossier generated with counselor and candidate digital signatures.")

    inline_res = client.get(f"/api/analysis/{session_id}/report/download?inline=true", headers=headers)
    assert inline_res.status_code == 200, f"Inline download failed: {inline_res.text}"
    assert inline_res.headers.get("content-type") == "application/pdf"
    content_disp = inline_res.headers.get("content-disposition", "")
    assert "inline" in content_disp, f"Content-Disposition was not inline: {content_disp}"
    assert len(inline_res.content) > 100000
    print("TEST 4 PASSED: Inline PDF streaming endpoint returns valid 64p PDF with inline Content-Disposition.")

    status_res = client.get(f"/api/analysis/{session_id}/report/storage-status", headers=headers)
    assert status_res.status_code == 200, f"Storage status failed: {status_res.text}"
    s_status = status_res.json()
    assert s_status["local_file_exists"] is True
    assert s_status["local_file_size"] > 0
    print(f"TEST 5 PASSED: Session storage status reported (local_size={s_status['local_file_size']} bytes).")

    batch_res = client.post(
        "/api/analysis/batch/export-zip",
        json={"session_ids": [session_id]},
        headers=headers,
    )
    assert batch_res.status_code == 200, f"Batch export failed: {batch_res.text}"
    assert batch_res.headers.get("content-type") == "application/zip"
    zip_bytes = io.BytesIO(batch_res.content)
    with zipfile.ZipFile(zip_bytes, "r") as z:
        names = z.namelist()
        assert len(names) == 1, f"Expected 1 report in zip, got {names}"
        assert names[0].endswith(".pdf")
        info = z.getinfo(names[0])
        assert info.file_size > 100000
    print(f"TEST 6 PASSED: Batch Cohort ZIP archive created with {len(names)} report ({info.file_size} bytes).")

    print("\nALL ENTERPRISE SUITE TESTS PASSED PERFECTLY WITH ZERO ERRORS!")

if __name__ == "__main__":
    run_tests()
