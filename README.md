# AISYS RFID Library Management Prototype

This repository contains a working prototype of an RFID-enabled library management system designed to support the AISYS SOP and the priority acceptance scenarios described in the project brief.

## Project purpose
The solution demonstrates a modular library workflow with:
- catalog item tracking
- member circulation logic
- RFID tagging and validation
- handheld inventory checks
- security gate alarm simulation
- smart-card login mock
- spreadsheet-based migration and reconciliation
- local dashboard operations

The implementation is intentionally designed as a controlled, offline-friendly prototype using mock adapters for unavailable external devices and services.

## System overview
The project uses a layered architecture:
- User layer: Streamlit dashboard
- Application layer: FastAPI routes and business logic
- RFID middleware layer: mock device adapters for tag binding, handheld scanning, gate alarms, and smart-card access
- Data layer: SQLAlchemy ORM with SQLite persistence
- Integration layer: mock email, SMS, and print notification adapters
- Operations layer: health checks, audit logging, backup/restore scripts, and release support tooling

## Main project files
- `main.py` — FastAPI application, database models, RFID, circulation, gate, and auth endpoints
- `migration_engine.py` — spreadsheet import, row validation, duplicate rejection, and reconciliation
- `streamlit_app.py` — local dashboard for operational simulation
- `test_solution.py` — automated tests for the priority scenarios
- `requirements.txt` — pinned dependency list for local setup
- `scripts/` — backup, restore, and release support tooling
- `docs/` — traceability matrix, architecture, admin, user, and signoff documentation
- `migrations/` — versioned migration skeleton and release versioning notes
- `config/settings.example.yaml` — sample configuration template

## Features implemented
- RFID tag binding to bibliographic/item records
- checkout and checkin logic with member blocking and fine thresholds
- reference-only item restrictions
- due-date enquiry
- handheld RFID inventory scan reporting missing and misplaced items
- gate alarm and unauthorized removal detection
- smart-card role-based authorization mock
- dashboard metrics for tagged items, loans, and alarms
- migration utility for CSV/spreadsheet ingestion with validation and reconciliation
- backup and restore workflow primitives
- offline release bundle creation support

## Local setup
```powershell
cd C:\Users\shara\OneDrive\Desktop\PROJECTS\AISYS\aisys-library-system
py -m pip install -r requirements.txt
```

## Run the API
```powershell
cd C:\Users\shara\OneDrive\Desktop\PROJECTS\AISYS\aisys-library-system
py -m uvicorn main:app --host 127.0.0.1 --port 8001 --reload
```

## Run the dashboard
```powershell
cd C:\Users\shara\OneDrive\Desktop\PROJECTS\AISYS\aisys-library-system
streamlit run streamlit_app.py
```

## Health check
```powershell
curl http://127.0.0.1:8001/health
```

## Automated verification
```powershell
cd C:\Users\shara\OneDrive\Desktop\PROJECTS\AISYS\aisys-library-system
pytest -q
```

Verified result from the project environment:
- 6 tests passed
- 1 warning from Starlette/FastAPI test client deprecation

## Backup and restore workflow
```powershell
cd C:\Users\shara\OneDrive\Desktop\PROJECTS\AISYS\aisys-library-system
py scripts/backup_db.py --db ./aisys_library.db --backup-dir ./backups
py scripts/restore_db.py --backup ./backups/aisys_library_backup.db --db ./aisys_library.db
```

## Documentation set
The repository includes documentation for:
- requirements traceability and coverage
- architecture package
- administration guide
- user guide
- rollback and restore runbook
- software bill of materials
- final signoff summary
- production-readiness backlog

## Current project status
This project is a validated internal prototype and demonstration package for the AISYS SOP scenario, with working code and test evidence.

It is not a production-certified live library system and should not be presented as a vendor-certified solution for a real institutional environment without additional operational, security, and integration validation.

## Recommended next step
Use this repository as the foundation for a real production implementation plan that includes:
- production backup automation
- formal secure configuration management
- real integration boundaries with vendor systems
- user acceptance signoff and operational readiness review
