"""
Database connection — auto-selects SQLite (local dev) or PostgreSQL (production/Neon).

When DATABASE_URL is set, uses psycopg2 with a thin compatibility wrapper that:
  • converts ? placeholders to %s
  • translates INSERT OR IGNORE → INSERT INTO … ON CONFLICT DO NOTHING
  • translates SQLite strftime/randomblob/date functions to PostgreSQL equivalents
  • translates executescript() into individual execute() calls
  • returns DictRow objects (support both key and positional [0] access like sqlite3.Row)
  • closes the connection on context-manager exit (one connection per request)

When DATABASE_URL is not set, returns a plain sqlite3.Connection as before.
"""
from __future__ import annotations
import os
import re

DATABASE_URL = os.environ.get("DATABASE_URL")

# ──────────────────────────────────────────────────────────────────────────────
# PostgreSQL mode
# ──────────────────────────────────────────────────────────────────────────────
if DATABASE_URL:
    import psycopg2
    import psycopg2.extras

    # Exact replacement for SQLite's NOW-equivalent
    _PG_NOW = (
        "to_char(NOW() AT TIME ZONE 'UTC', 'YYYY-MM-DD\"T\"HH24:MI:SS\"Z\"')"
    )

    _PRAGMA_RE = re.compile(r"^\s*PRAGMA\s", re.IGNORECASE)
    _INSERT_OR_IGNORE_RE = re.compile(r"INSERT\s+OR\s+IGNORE\s+INTO", re.IGNORECASE)

    def _to_pg(sql: str) -> str | None:
        """
        Translate a single SQLite-flavour SQL statement to PostgreSQL.
        Returns None to signal the caller should skip this statement.
        """
        if _PRAGMA_RE.match(sql):
            return None

        # SQLite strftime for timestamps → PostgreSQL to_char
        sql = sql.replace("strftime('%Y-%m-%dT%H:%M:%SZ','now')", _PG_NOW)

        # SQLite date('now') → PostgreSQL CURRENT_DATE as text
        sql = sql.replace("date('now')", "CURRENT_DATE::text")

        # SQLite lower(hex(randomblob(16))) → PostgreSQL gen_random_uuid()
        sql = sql.replace("lower(hex(randomblob(16)))", "gen_random_uuid()::text")

        # ? → %s
        sql = sql.replace("?", "%s")

        # INSERT OR IGNORE → INSERT INTO … ON CONFLICT DO NOTHING
        if _INSERT_OR_IGNORE_RE.search(sql):
            sql = _INSERT_OR_IGNORE_RE.sub("INSERT INTO", sql)
            if "ON CONFLICT" not in sql.upper():
                sql = sql.rstrip().rstrip(";") + " ON CONFLICT DO NOTHING"

        return sql

    class _Cursor:
        """Wraps psycopg2 DictCursor to match sqlite3 cursor API."""

        __slots__ = ("_c",)

        def __init__(self, cursor: psycopg2.extensions.cursor) -> None:
            self._c = cursor

        def fetchone(self):
            return self._c.fetchone()

        def fetchall(self):
            return self._c.fetchall()

        def __iter__(self):
            return iter(self._c)

    class _Conn:
        """
        Wraps a psycopg2 connection to look like sqlite3.Connection.
        Each instance owns exactly one underlying connection, which is
        closed when the context manager exits (or when close() is called).
        """

        __slots__ = ("_conn",)

        def __init__(self) -> None:
            self._conn = psycopg2.connect(DATABASE_URL)
            self._conn.autocommit = False

        # ── Core API ───────────────────────────────────────────────────────────

        def execute(self, sql: str, params=None) -> _Cursor:
            cur = self._conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            pg_sql = _to_pg(sql)
            if pg_sql is None:
                return _Cursor(cur)
            if params is not None:
                cur.execute(pg_sql, params)
            else:
                cur.execute(pg_sql)
            return _Cursor(cur)

        def executescript(self, script: str) -> None:
            """Execute a ';'-separated batch of DDL/DML statements."""
            for stmt in script.split(";"):
                stmt = stmt.strip()
                if not stmt or stmt.startswith("--"):
                    continue
                pg = _to_pg(stmt)
                if pg:
                    cur = self._conn.cursor()
                    cur.execute(pg)

        def commit(self) -> None:
            self._conn.commit()

        def close(self) -> None:
            try:
                self._conn.close()
            except Exception:
                pass

        # ── Context-manager ───────────────────────────────────────────────────

        def __enter__(self) -> "_Conn":
            return self

        def __exit__(self, exc_type, exc, tb) -> None:
            if exc_type:
                try:
                    self._conn.rollback()
                except Exception:
                    pass
            else:
                try:
                    self._conn.commit()
                except Exception:
                    pass
            self.close()

    def get_conn() -> _Conn:  # type: ignore[return-value]
        return _Conn()

# ──────────────────────────────────────────────────────────────────────────────
# SQLite mode (local development)
# ──────────────────────────────────────────────────────────────────────────────
else:
    import sqlite3
    from pathlib import Path

    _DB_PATH = Path("data/sessions.db")

    def get_conn() -> sqlite3.Connection:  # type: ignore[misc]
        _DB_PATH.parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(str(_DB_PATH), check_same_thread=False)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA foreign_keys=ON")
        return conn
