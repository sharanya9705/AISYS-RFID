# Deployment Guide

## 1. Purpose
This guide describes how to deploy the AISYS prototype in a local or isolated environment using a Windows-based host and local file-based SQLite database.

## 2. Supported environment
- Operating system: Windows 11 or Windows Server 2022+
- Python: 3.11 or later recommended
- Database: SQLite for prototype deployment
- Network: local LAN or isolated site network
- Runtime: FastAPI API + Streamlit dashboard locally

## 3. Pre-requisites
1. Install Python 3.11 or newer.
2. Install Git if version control is required.
3. Create a virtual environment.
4. Install dependencies from requirements.txt.

Example:
```powershell
cd C:\Users\shara\OneDrive\Desktop\PROJECTS\AISYS\aisys-library-system
py -m venv .venv
.\.venv\Scripts\Activate.ps1
py -m pip install --upgrade pip
py -m pip install -r requirements.txt
```

## 4. Local deployment steps
### Start API server
```powershell
cd C:\Users\shara\OneDrive\Desktop\PROJECTS\AISYS\aisys-library-system
py -m uvicorn main:app --host 127.0.0.1 --port 8001 --reload
```

### Start dashboard
Open a second terminal:
```powershell
cd C:\Users\shara\OneDrive\Desktop\PROJECTS\AISYS\aisys-library-system
streamlit run streamlit_app.py
```

## 5. Backend health check
Access the API with a browser or curl:
```powershell
curl http://127.0.0.1:8001/health
```

Expected response includes:
- status: HEALTHY
- system_version
- timestamp
- database status

## 6. Offline deployment model
For isolated sites:
- package Python runtime and project sources together
- include requirements.txt with pinned versions
- avoid external internet dependencies at runtime
- pre-stage the .venv or wheel cache
- keep data in local SQLite or a site-controlled data path

## 7. Configuration management
Keep environment-specific values outside source code where possible:
- database path
- site code or institution name
- alert thresholds
- email/SMS provider endpoints

Recommended pattern:
- .env or local config file
- do not commit secrets
- keep credentials in a protected local store

## 8. Logging and diagnostics
Key files:
- runtime logs from the terminal session
- application-level logs in Python logging output
- local database file: aisys_library.db

## 9. Update preparation
To prepare an offline or controlled update:
1. freeze current dependency versions
2. archive working code in a release folder
3. back up the database
4. validate with pytest
5. apply update in a staging copy
6. restore only after verification

## 10. Operational note
This is a working prototype deployment model and not a full commercial production installer. A future production deployment should add:
- Windows service packaging
- proper database backup automation
- secret management
- central monitoring
- zero-downtime update mechanism
