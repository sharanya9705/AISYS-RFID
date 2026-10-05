"""Initial schema migration for the AISYS prototype.

This is a lightweight migration example for a future versioned migration workflow.
It demonstrates the migration pattern expected by the SOP: upgrade and downgrade
functions plus a clear data model baseline.
"""

from __future__ import annotations

from sqlalchemy import text


class Migration:
    version = "001_initial_schema"

    @staticmethod
    def upgrade(engine):
        with engine.begin() as conn:
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS items (
                    id TEXT PRIMARY KEY,
                    accession_number TEXT UNIQUE,
                    title TEXT NOT NULL,
                    author TEXT NOT NULL,
                    isbn TEXT,
                    is_reference BOOLEAN DEFAULT FALSE,
                    rfid_epc TEXT,
                    status TEXT DEFAULT 'AVAILABLE',
                    shelf_location TEXT DEFAULT 'A1'
                )
            """))
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS members (
                    id TEXT PRIMARY KEY,
                    card_number TEXT UNIQUE,
                    rfid_uid TEXT UNIQUE,
                    name TEXT NOT NULL,
                    email TEXT NOT NULL,
                    is_blocked BOOLEAN DEFAULT FALSE,
                    fine_balance FLOAT DEFAULT 0.0,
                    role TEXT DEFAULT 'PATRON'
                )
            """))
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS circulations (
                    id TEXT PRIMARY KEY,
                    item_id TEXT,
                    member_id TEXT,
                    issue_date DATETIME,
                    due_date DATETIME,
                    return_date DATETIME,
                    status TEXT DEFAULT 'ISSUED'
                )
            """))
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS gate_events (
                    id TEXT PRIMARY KEY,
                    timestamp DATETIME,
                    epc TEXT,
                    accession_number TEXT,
                    is_authorized BOOLEAN,
                    snapshot_path TEXT,
                    alarm_triggered BOOLEAN DEFAULT FALSE
                )
            """))
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS audit_logs (
                    id TEXT PRIMARY KEY,
                    timestamp DATETIME,
                    actor TEXT,
                    action TEXT,
                    details TEXT
                )
            """))
        print("[migration 001] Initial schema upgrade complete.")

    @staticmethod
    def downgrade(engine):
        with engine.begin() as conn:
            conn.execute(text("DROP TABLE IF EXISTS audit_logs"))
            conn.execute(text("DROP TABLE IF EXISTS gate_events"))
            conn.execute(text("DROP TABLE IF EXISTS circulations"))
            conn.execute(text("DROP TABLE IF EXISTS members"))
            conn.execute(text("DROP TABLE IF EXISTS items"))
        print("[migration 001] Initial schema downgrade complete.")
