#!/usr/bin/env python3
"""Create a simple offline deployment bundle for the AISYS prototype."""

from __future__ import annotations

import argparse
import zipfile
from pathlib import Path


def build_bundle(project_root: str | Path, output_zip: str | Path) -> Path:
    root = Path(project_root).resolve()
    bundle = Path(output_zip).resolve()
    bundle.parent.mkdir(parents=True, exist_ok=True)

    include_items = [
        "README.md",
        "requirements.txt",
        "main.py",
        "migration_engine.py",
        "streamlit_app.py",
        "test_solution.py",
        "scripts",
        "docs",
        "migrations",
        "config",
    ]

    with zipfile.ZipFile(bundle, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for item in include_items:
            path = root / item
            if path.is_dir():
                for file_path in sorted(path.rglob("*")):
                    if file_path.is_file():
                        arcname = file_path.relative_to(root)
                        zf.write(file_path, arcname)
            elif path.exists():
                zf.write(path, path.relative_to(root))

    print(f"Offline bundle created: {bundle}")
    return bundle


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create an offline ZIP bundle for the AISYS prototype.")
    parser.add_argument("--root", default=".", help="Project root directory.")
    parser.add_argument("--output", default="./release/offline_bundle.zip", help="Output ZIP path.")
    args = parser.parse_args()

    build_bundle(args.root, args.output)
