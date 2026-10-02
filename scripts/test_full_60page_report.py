from __future__ import annotations

import json
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'backend'))

from premium_pdf_report.generator import PremiumReportGenerator

DB_PATH = ROOT / 'data' / 'sessions.db'
OUT_PDF = ROOT / 'test_output' / 'dmit_60page_master_test.pdf'
OUT_PDF.parent.mkdir(parents=True, exist_ok=True)

conn = sqlite3.connect(str(DB_PATH))
cur = conn.cursor()

cur.execute("SELECT id, data FROM sessions ORDER BY updated_at DESC LIMIT 1")
row = cur.fetchone()

pipeline_data = {}
session_meta = {
    'subject_name': 'Aarav Sharma',
    'subject_age': 16,
    'subject_gender': 'Male',
    'subject_dob': '14 March 2010',
    'guardian_name': 'Dr. Rajesh Sharma',
    'contact_phone': '+91 98250 12345',
    'contact_email': 'rajesh.sharma@example.com',
    'analyst_name': 'Prof. Shilp Gohil, Ph.D.',
    'analyst_id': 'IADP-89241-SR',
    'hand_dominance': 'Right Hand Dominant',
}

if row:
    session_id, data_str = row
    data = json.loads(data_str)
    print(f"Loaded session {session_id} from database")
    if 'analysis_results' in data:
        pipeline_data = data['analysis_results']
    elif 'pipeline_data' in data:
        pipeline_data = data['pipeline_data']
    else:
        pipeline_data = data
else:
    print("No completed session found in database, using synthetic test payload")

if not pipeline_data.get('aggregated_analysis'):
    pipeline_data['aggregated_analysis'] = {
        'dmit_profile': {
            'multiple_intelligences': {
                'intrapersonal': 0.78,
                'interpersonal': 0.74,
                'logical_mathematical': 0.82,
                'spatial': 0.76,
                'bodily_kinesthetic': 0.70,
                'linguistic': 0.75,
                'musical': 0.68,
                'naturalistic': 0.65,
                'existential': 0.72,
            },
            'brain_mapping': {
                'left_hemisphere': 52.4,
                'right_hemisphere': 47.6,
                'dominant_hemisphere': 'left',
                'prefrontal_l': 10.8,
                'prefrontal_r': 10.4,
                'frontal_l': 11.4,
                'frontal_r': 10.2,
                'parietal_l': 10.0,
                'parietal_r': 9.8,
                'temporal_l': 10.2,
                'temporal_r': 9.2,
                'occipital_l': 10.0,
                'occipital_r': 8.0,
                'lobe_hemispheres': {
                    'left_prefrontal': 0.108,
                    'right_prefrontal': 0.104,
                    'left_frontal': 0.114,
                    'right_frontal': 0.102,
                    'left_parietal': 0.100,
                    'right_parietal': 0.098,
                    'left_temporal': 0.102,
                    'right_temporal': 0.092,
                    'left_occipital': 0.100,
                    'right_occipital': 0.080,
                }
            },
            'learning_styles': {
                'visual': 0.44,
                'auditory': 0.34,
                'kinesthetic': 0.22,
            },
            'personality_behavior': {
                'openness': 0.76,
                'conscientiousness': 0.72,
                'extraversion': 0.66,
                'agreeableness': 0.70,
                'emotional_stability': 0.68,
            },
            'atd_analysis': {
                'left_hand': {
                    'angle_deg': 41.2,
                    'confidence': 0.88,
                    'range_category': 'normal',
                    'learning_speed': 0.78,
                    'fine_motor_capacity': 0.75,
                    'sensory_sensitivity': 0.72,
                    'interpretation': 'Normal ATD range — optimal bilateral conduction latency and balanced motor control.'
                },
                'right_hand': {
                    'angle_deg': 39.8,
                    'confidence': 0.90,
                    'range_category': 'low',
                    'learning_speed': 0.84,
                    'fine_motor_capacity': 0.82,
                    'sensory_sensitivity': 0.76,
                    'interpretation': 'Below average ATD angle — accelerated neuromuscular reflex dexterity and fine motor precision.'
                }
            }
        }
    }

if not pipeline_data.get('individual_results'):
    fingers = []
    slots = ['L1', 'L2', 'L3', 'L4', 'L5', 'R1', 'R2', 'R3', 'R4', 'R5']
    types = ['thumb', 'index', 'middle', 'ring', 'little'] * 2
    patterns = ['whorl', 'loop', 'loop', 'whorl', 'arch', 'whorl', 'whorl', 'loop', 'loop', 'loop']
    tfrcs = [18, 16, 14, 17, 12, 19, 17, 15, 16, 13]
    for s, t, p, rc in zip(slots, types, patterns, tfrcs):
        fingers.append({
            'pipeline_info': {'finger_position': s, 'finger_type': t},
            'feature_extraction': {
                'consolidated_features': {
                    'pattern_type': p,
                    'tfrc': rc,
                    'minutiae_count': 42 + rc,
                    'box_counting_dimension': 1.68 + (rc * 0.01),
                    'overall_quality_score': 0.88,
                    'extraction_confidence': 0.92,
                },
                'quality_metrics': {
                    'image_quality': 0.88,
                }
            }
        })
    pipeline_data['individual_results'] = fingers

print("Triggering PremiumReportGenerator.create_report...")
out = PremiumReportGenerator.create_report(pipeline_data, str(OUT_PDF), session_meta)
print(f"Generated PDF: {out}")

try:
    import fitz
    doc = fitz.open(str(OUT_PDF))
    print(f"Verified PDF page count: {len(doc)} pages")
    for i in [0, 4, 6, 15, 34, 42, 59, 60, 63]:
        if i < len(doc):
            p = doc[i]
            text = p.get_text()[:120].replace('\n', ' ')
            print(f"Page {i+1} title/snippet: {text}")
except ImportError:
    print("fitz not installed, skipping detailed page inspection")
