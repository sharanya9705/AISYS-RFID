#!/usr/bin/env python3
"""Restore the AISYS SQLite database from a prepared backup file."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path


def restore_database(backup_path: str | Path, db_path: str | Path) -> Path:
    backup_file = Path(backup_path).resolve()
    target = Path(db_path).resolve()

    if not backup_file.exists():
        raise FileNotFoundError(f"Backup file not found: {backup_file}")

    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(backup_file, target)
    print(f"Database restored: {target}")
    return target


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Restore the AISYS SQLite database from a backup.")
    parser.add_argument("--backup", required=True, help="Path to the database backup file.")
    parser.add_argument("--db", default="./aisys_library.db", help="Target database file path.")
    args = parser.parse_args()

    restore_database(args.backup, args.db)
