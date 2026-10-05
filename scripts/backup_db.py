#!/usr/bin/env python3
"""Create a timestamped backup of the SQLite database used by the AISYS prototype."""

from __future__ import annotations

import argparse
import shutil
from datetime import datetime
from pathlib import Path


def backup_database(db_path: str | Path, backup_dir: str | Path | None = None) -> Path:
    source = Path(db_path).resolve()
    if not source.exists():
        raise FileNotFoundError(f"Database file not found: {source}")

    target_dir = Path(backup_dir).resolve() if backup_dir else source.parent / "backups"
    target_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"{source.stem}_{timestamp}{source.suffix}"
    destination = target_dir / backup_name
    shutil.copy2(source, destination)
    print(f"Backup created: {destination}")
    return destination


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Backup the AISYS SQLite database.")
    parser.add_argument("--db", default="./aisys_library.db", help="Path to the SQLite database file.")
    parser.add_argument("--backup-dir", default="./backups", help="Folder to store timestamped backups.")
    args = parser.parse_args()

    backup_database(args.db, args.backup_dir)
