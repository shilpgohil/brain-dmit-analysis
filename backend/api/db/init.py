"""
Database initialisation — CREATE TABLE IF NOT EXISTS for all auth/partner tables.
Called once at API startup after the existing sessions table is initialised.
"""
from __future__ import annotations
from .connection import get_conn

_SCHEMA = """
-- ── Admins ───────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS admins (
    id            TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
    email         TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    name          TEXT NOT NULL,
    photo_url     TEXT,
    is_active     INTEGER NOT NULL DEFAULT 1,
    created_at    TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ','now')),
    updated_at    TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ','now'))
);
CREATE UNIQUE INDEX IF NOT EXISTS idx_admins_email ON admins(email);

-- ── Plans ─────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS plans (
    id            TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
    name          TEXT UNIQUE NOT NULL,
    display_name  TEXT NOT NULL,
    description   TEXT,
    color_hex     TEXT NOT NULL DEFAULT '#6b7280',
    is_active     INTEGER NOT NULL DEFAULT 1,
    sort_order    INTEGER NOT NULL DEFAULT 0,
    created_by    TEXT REFERENCES admins(id),
    created_at    TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ','now')),
    updated_at    TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ','now'))
);

-- ── Feature catalog ───────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS features (
    id            TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
    key           TEXT UNIQUE NOT NULL,
    display_name  TEXT NOT NULL,
    description   TEXT,
    category      TEXT NOT NULL DEFAULT 'analysis',
    value_type    TEXT NOT NULL DEFAULT 'boolean',
    default_value TEXT NOT NULL DEFAULT 'false',
    is_active     INTEGER NOT NULL DEFAULT 1,
    created_at    TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ','now'))
);
CREATE UNIQUE INDEX IF NOT EXISTS idx_features_key ON features(key);

-- ── Plan → Feature values ─────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS plan_features (
    id            TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
    plan_id       TEXT NOT NULL REFERENCES plans(id) ON DELETE CASCADE,
    feature_id    TEXT NOT NULL REFERENCES features(id) ON DELETE CASCADE,
    feature_value TEXT NOT NULL,
    updated_by    TEXT REFERENCES admins(id),
    updated_at    TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ','now')),
    UNIQUE (plan_id, feature_id)
);
CREATE INDEX IF NOT EXISTS idx_plan_features_plan    ON plan_features(plan_id);
CREATE INDEX IF NOT EXISTS idx_plan_features_feature ON plan_features(feature_id);

-- ── Partners ──────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS partners (
    id                   TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
    email                TEXT UNIQUE NOT NULL,
    password_hash        TEXT NOT NULL,
    name                 TEXT NOT NULL,
    centre_name          TEXT,
    phone                TEXT,
    city                 TEXT,
    state                TEXT,
    photo_url            TEXT,
    plan_id              TEXT REFERENCES plans(id) ON DELETE SET NULL,
    is_active            INTEGER NOT NULL DEFAULT 1,
    onboarding_completed INTEGER NOT NULL DEFAULT 0,
    public_slug          TEXT UNIQUE,
    allocated_by         TEXT REFERENCES admins(id),
    notes                TEXT,
    created_at           TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ','now')),
    updated_at           TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ','now')),
    deleted_at           TEXT
);
CREATE UNIQUE INDEX IF NOT EXISTS idx_partners_email ON partners(email);
CREATE UNIQUE INDEX IF NOT EXISTS idx_partners_slug  ON partners(public_slug);
CREATE INDEX        IF NOT EXISTS idx_partners_plan  ON partners(plan_id);
CREATE INDEX        IF NOT EXISTS idx_partners_active ON partners(is_active);

-- ── Per-partner feature overrides ─────────────────────────────────────────
CREATE TABLE IF NOT EXISTS partner_feature_overrides (
    id              TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
    partner_id      TEXT NOT NULL REFERENCES partners(id) ON DELETE CASCADE,
    feature_id      TEXT NOT NULL REFERENCES features(id) ON DELETE CASCADE,
    feature_value   TEXT NOT NULL,
    override_reason TEXT,
    set_by          TEXT REFERENCES admins(id),
    set_at          TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ','now')),
    expires_at      TEXT,
    UNIQUE (partner_id, feature_id)
);
CREATE INDEX IF NOT EXISTS idx_overrides_partner ON partner_feature_overrides(partner_id);

-- ── Session reports (QR public token) ─────────────────────────────────────
CREATE TABLE IF NOT EXISTS session_reports (
    id             TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
    session_id     TEXT NOT NULL REFERENCES sessions(id) ON DELETE CASCADE,
    partner_id     TEXT NOT NULL REFERENCES partners(id),
    public_token   TEXT UNIQUE NOT NULL,
    report_path    TEXT,
    quotients_json TEXT,
    generated_at   TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ','now')),
    expires_at     TEXT,
    view_count     INTEGER NOT NULL DEFAULT 0,
    last_viewed_at TEXT
);
CREATE UNIQUE INDEX IF NOT EXISTS idx_reports_token   ON session_reports(public_token);
CREATE INDEX        IF NOT EXISTS idx_reports_session ON session_reports(session_id);
CREATE INDEX        IF NOT EXISTS idx_reports_partner ON session_reports(partner_id);

-- ── Intake requests (from partner QR card) ────────────────────────────────
CREATE TABLE IF NOT EXISTS intake_requests (
    id                   TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
    partner_id           TEXT NOT NULL REFERENCES partners(id),
    subject_name         TEXT NOT NULL,
    subject_age          INTEGER,
    subject_phone        TEXT,
    purpose              TEXT,
    note                 TEXT,
    status               TEXT NOT NULL DEFAULT 'new',
    converted_session_id TEXT REFERENCES sessions(id),
    submitted_at         TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ','now'))
);
CREATE INDEX IF NOT EXISTS idx_intake_partner ON intake_requests(partner_id);
CREATE INDEX IF NOT EXISTS idx_intake_status  ON intake_requests(partner_id, status);

-- ── Partner interest requests (public form) ───────────────────────────────
CREATE TABLE IF NOT EXISTS partner_requests (
    id                 TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
    name               TEXT NOT NULL,
    email              TEXT NOT NULL,
    phone              TEXT,
    centre_name        TEXT,
    city               TEXT,
    state              TEXT,
    plan_interest      TEXT,
    message            TEXT,
    status             TEXT NOT NULL DEFAULT 'pending',
    reviewed_by        TEXT REFERENCES admins(id),
    reviewed_at        TEXT,
    created_partner_id TEXT REFERENCES partners(id),
    submitted_at       TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ','now'))
);
CREATE INDEX IF NOT EXISTS idx_preq_status ON partner_requests(status);
CREATE INDEX IF NOT EXISTS idx_preq_email  ON partner_requests(email);

-- ── Refresh tokens (for revocation) ──────────────────────────────────────
CREATE TABLE IF NOT EXISTS refresh_tokens (
    id         TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
    jti        TEXT UNIQUE NOT NULL,
    user_id    TEXT NOT NULL,
    user_type  TEXT NOT NULL,
    is_revoked INTEGER NOT NULL DEFAULT 0,
    issued_at  TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ','now')),
    expires_at TEXT NOT NULL
);
CREATE UNIQUE INDEX IF NOT EXISTS idx_refresh_jti  ON refresh_tokens(jti);
CREATE INDEX        IF NOT EXISTS idx_refresh_user ON refresh_tokens(user_id, user_type);

-- ── Audit log ─────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS audit_logs (
    id          TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
    actor_id    TEXT NOT NULL,
    actor_type  TEXT NOT NULL,
    action      TEXT NOT NULL,
    target_type TEXT,
    target_id   TEXT,
    old_value   TEXT,
    new_value   TEXT,
    ip_address  TEXT,
    occurred_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ','now'))
);
CREATE INDEX IF NOT EXISTS idx_audit_actor  ON audit_logs(actor_id, occurred_at);
CREATE INDEX IF NOT EXISTS idx_audit_target ON audit_logs(target_type, target_id, occurred_at);
CREATE INDEX IF NOT EXISTS idx_audit_action ON audit_logs(action, occurred_at);

-- ── Add partner_id to existing sessions ──────────────────────────────────
-- SQLite's ALTER TABLE only supports ADD COLUMN; the column may already exist.
"""

# Sessions gets partner_id separately (ALTER TABLE is idempotent with try/except)
_ALTER_SESSIONS = "ALTER TABLE sessions ADD COLUMN partner_id TEXT REFERENCES partners(id)"
_ALTER_SESSIONS_IDX = "CREATE INDEX IF NOT EXISTS idx_sessions_partner ON sessions(partner_id)"


def init_auth_db() -> None:
    """
    Create all auth/partner tables. Safe to call repeatedly (IF NOT EXISTS).

    Each ALTER TABLE runs in its own connection so that a 'column already
    exists' error on one statement cannot leave the transaction in an aborted
    state and block the next statement (psycopg2 InFailedSqlTransaction).
    """
    # ── Schema DDL — one transaction ─────────────────────────────────────────
    with get_conn() as conn:
        conn.executescript(_SCHEMA)
        conn.commit()

    # ── Idempotent migrations — each in its own connection ────────────────────
    for stmt in (
        _ALTER_SESSIONS,
        _ALTER_SESSIONS_IDX,
        "ALTER TABLE session_reports ADD COLUMN quotients_json TEXT",
    ):
        try:
            with get_conn() as conn:
                conn.execute(stmt)
                conn.commit()
        except Exception:
            pass  # Column / index already exists — that is fine
