"""
Feature catalog, plan management, and effective-feature resolution.
"""
from __future__ import annotations
from typing import Any, Dict, List, Optional
from api.db.connection import get_conn

# Default feature catalog seeded on first startup
DEFAULT_FEATURES = [
    ("pdf_report",            "PDF Report Generation",       "analysis", "boolean", "false"),
    ("quotient_dashboard",    "10-Quotient Dashboard",       "analysis", "boolean", "false"),
    ("ai_consultant",         "AI DMIT Consultant",          "analysis", "boolean", "false"),
    ("compare_sessions",      "Side-by-Side Comparison",     "analysis", "boolean", "false"),
    ("compatibility_report",  "Couple Compatibility PDF",    "report",   "boolean", "false"),
    ("bulk_upload",           "Bulk Fingerprint Upload",     "analysis", "boolean", "true"),
    ("public_report_qr",      "Public Report QR Sharing",   "report",   "boolean", "false"),
    ("sessions_per_month",    "Analyses Per Month (-1=unlimited)", "quota", "numeric", "10"),
    ("report_validity_days",  "Report Public Link Validity (days)", "quota", "numeric", "365"),
    ("white_label_branding",  "Custom Branding",             "integration", "boolean", "false"),
    ("api_direct_access",     "Direct API Access",           "integration", "boolean", "false"),
    ("export_raw_data",       "Export Raw Feature Data",     "report",   "boolean", "false"),
    ("palm_atd",              "Palm ATD Angle Analysis",     "analysis", "boolean", "true"),
]

DEFAULT_PLANS = [
    ("basic",      "Basic",       "Starter plan — limited analyses, no PDF",  "#6b7280", 0),
    ("standard",   "Standard",    "Most popular — PDF + quotients included",  "#c4a574", 1),
    ("premium",    "Premium",     "Full access including AI consultant",      "#9d8bb5", 2),
    ("enterprise", "Enterprise",  "Unlimited + white-label + API access",     "#10b981", 3),
]

# Feature values per default plan
_PLAN_FEATURES: Dict[str, Dict[str, str]] = {
    "basic":      {"pdf_report": "false", "quotient_dashboard": "false", "sessions_per_month": "10"},
    "standard":   {"pdf_report": "true",  "quotient_dashboard": "true",  "sessions_per_month": "50",
                   "compare_sessions": "true", "public_report_qr": "true"},
    "premium":    {"pdf_report": "true",  "quotient_dashboard": "true",  "sessions_per_month": "-1",
                   "compare_sessions": "true", "public_report_qr": "true",
                   "ai_consultant": "true", "compatibility_report": "true", "export_raw_data": "true"},
    "enterprise": {"pdf_report": "true",  "quotient_dashboard": "true",  "sessions_per_month": "-1",
                   "compare_sessions": "true", "public_report_qr": "true",
                   "ai_consultant": "true", "compatibility_report": "true", "export_raw_data": "true",
                   "white_label_branding": "true", "api_direct_access": "true"},
}


def seed_features_and_plans() -> None:
    """Idempotent seed of feature catalog and default plans."""
    with get_conn() as conn:
        for key, display, cat, vtype, default in DEFAULT_FEATURES:
            conn.execute(
                "INSERT OR IGNORE INTO features (key, display_name, category, value_type, default_value) "
                "VALUES (?, ?, ?, ?, ?)",
                (key, display, cat, vtype, default),
            )
        for name, display, desc, color, order in DEFAULT_PLANS:
            conn.execute(
                "INSERT OR IGNORE INTO plans (name, display_name, description, color_hex, sort_order) "
                "VALUES (?, ?, ?, ?, ?)",
                (name, display, desc, color, order),
            )
        conn.commit()

        # Wire plan features
        plans = {r[0]: r[1] for r in conn.execute("SELECT name, id FROM plans").fetchall()}
        feats = {r[0]: r[1] for r in conn.execute("SELECT key, id FROM features").fetchall()}
        for plan_name, feat_dict in _PLAN_FEATURES.items():
            plan_id = plans.get(plan_name)
            if not plan_id:
                continue
            for feat_key, val in feat_dict.items():
                feat_id = feats.get(feat_key)
                if not feat_id:
                    continue
                conn.execute(
                    "INSERT OR IGNORE INTO plan_features (plan_id, feature_id, feature_value) "
                    "VALUES (?, ?, ?)",
                    (plan_id, feat_id, val),
                )
        conn.commit()


def get_effective_features(partner_id: str) -> Dict[str, str]:
    """
    Three-layer feature resolution:
      1. partner_feature_overrides (highest — per-partner exception)
      2. plan_features            (mid — plan's configured value)
      3. features.default_value  (lowest — catalog default)
    Returns a flat {feature_key: value} dict for all active features.
    Expired overrides are ignored.
    """
    sql = """
    SELECT
        f.key,
        COALESCE(
            CASE WHEN pfo.expires_at IS NULL OR pfo.expires_at > strftime('%Y-%m-%dT%H:%M:%SZ','now')
                 THEN pfo.feature_value ELSE NULL END,
            pf.feature_value,
            f.default_value
        ) AS effective_value
    FROM features f
    LEFT JOIN partners p ON p.id = ?
    LEFT JOIN plan_features pf ON pf.plan_id = p.plan_id AND pf.feature_id = f.id
    LEFT JOIN partner_feature_overrides pfo ON pfo.partner_id = ? AND pfo.feature_id = f.id
    WHERE f.is_active = 1
    """
    with get_conn() as conn:
        rows = conn.execute(sql, (partner_id, partner_id)).fetchall()
    return {r[0]: r[1] for r in rows}


def list_features() -> List[Dict[str, Any]]:
    with get_conn() as conn:
        rows = conn.execute("SELECT * FROM features WHERE is_active = 1 ORDER BY category, key").fetchall()
    return [dict(r) for r in rows]


def list_plans() -> List[Dict[str, Any]]:
    with get_conn() as conn:
        rows = conn.execute("SELECT * FROM plans WHERE is_active = 1 ORDER BY sort_order").fetchall()
    return [dict(r) for r in rows]


def get_plan_features(plan_id: str) -> List[Dict[str, Any]]:
    with get_conn() as conn:
        rows = conn.execute(
            """
            SELECT f.id, f.key, f.display_name, f.value_type, f.default_value,
                   pf.feature_value, f.category
            FROM features f
            LEFT JOIN plan_features pf ON pf.feature_id = f.id AND pf.plan_id = ?
            WHERE f.is_active = 1 ORDER BY f.category, f.key
            """,
            (plan_id,),
        ).fetchall()
    return [dict(r) for r in rows]


def upsert_plan_feature(plan_id: str, feature_id: str, value: str, admin_id: str) -> None:
    with get_conn() as conn:
        conn.execute(
            """
            INSERT INTO plan_features (plan_id, feature_id, feature_value, updated_by)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(plan_id, feature_id)
            DO UPDATE SET feature_value = excluded.feature_value,
                          updated_by = excluded.updated_by,
                          updated_at = strftime('%Y-%m-%dT%H:%M:%SZ','now')
            """,
            (plan_id, feature_id, value, admin_id),
        )
        conn.commit()


def set_partner_override(
    partner_id: str, feature_id: str, value: str,
    admin_id: str, reason: str = "", expires_at: Optional[str] = None,
) -> None:
    with get_conn() as conn:
        conn.execute(
            """
            INSERT INTO partner_feature_overrides
              (partner_id, feature_id, feature_value, set_by, override_reason, expires_at)
            VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT(partner_id, feature_id)
            DO UPDATE SET feature_value = excluded.feature_value,
                          set_by = excluded.set_by,
                          override_reason = excluded.override_reason,
                          expires_at = excluded.expires_at,
                          set_at = strftime('%Y-%m-%dT%H:%M:%SZ','now')
            """,
            (partner_id, feature_id, value, admin_id, reason, expires_at),
        )
        conn.commit()


def remove_partner_override(partner_id: str, feature_id: str) -> None:
    with get_conn() as conn:
        conn.execute(
            "DELETE FROM partner_feature_overrides WHERE partner_id = ? AND feature_id = ?",
            (partner_id, feature_id),
        )
        conn.commit()


def list_partner_overrides(partner_id: str) -> List[Dict[str, Any]]:
    with get_conn() as conn:
        rows = conn.execute(
            """
            SELECT pfo.*, f.key, f.display_name
            FROM partner_feature_overrides pfo
            JOIN features f ON f.id = pfo.feature_id
            WHERE pfo.partner_id = ?
            """,
            (partner_id,),
        ).fetchall()
    return [dict(r) for r in rows]
