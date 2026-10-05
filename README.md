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

## Local setup for a new system

### 1) Prerequisites
- Python 3.11 or newer
- Git
- Internet access for package installation

### 2) Clone the repository
```powershell
git clone https://github.com/sharanya9705/AISYS-RFID.git
cd AISYS-RFID
```

### 3) Create a virtual environment
```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 4) Install dependencies
```powershell
py -m pip install --upgrade pip
py -m pip install -r requirements.txt
```

### 5) Validate the app installation
```powershell
py -m pytest -q
```

The expected result is all acceptance tests passing. In the project environment, the verified result was:
- 6 tests passed
- 1 warning from the FastAPI/Starlette test client deprecation path

## Run the API
From the project root:
```powershell
cd AISYS-RFID\aisys-library-system
py -m uvicorn main:app --host 127.0.0.1 --port 8001 --reload
```

## Run the dashboard
Open a second terminal and run:
```powershell
cd AISYS-RFID\aisys-library-system
streamlit run streamlit_app.py
```

## Health check
```powershell
curl http://127.0.0.1:8001/health
```

Example success response:
```json
{"status": "HEALTHY", "system_version": "1.0.0-offline", "database": "CONNECTED"}
```

## Troubleshooting
If the API port is already in use:
```powershell
netstat -ano | findstr :8001
taskkill /PID <PID> /F
```

If the app does not start because the working directory is wrong, make sure you run the commands from:
```powershell
AISYS-RFID\aisys-library-system
```

## Backup and restore workflow
```powershell
cd AISYS-RFID\aisys-library-system
py scripts/backup_db.py --db ./aisys_library.db --backup-dir ./backups
py scripts/restore_db.py --backup ./backups/aisys_library_backup.db --db ./aisys_library.db
```

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
