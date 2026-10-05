# Architecture Package

## 1. Layered architecture

The current solution follows a layered design consistent with the AISYS SOP:

- User layer: Streamlit dashboard and browser-based access patterns
- Application layer: FastAPI routes and service logic in main.py
- RFID middleware: mock device adapters for gate, handheld, smart-card, and alerting flows
- Interoperability layer: SIP2/NCIP mock endpoints
- Data layer: SQLite database with SQLAlchemy ORM models
- Integration layer: mock email/SMS/print event handlers
- Operations layer: health checks, logging, and local configuration

## 2. Core components

### Application service
- File: main.py
- Responsibilities:
  - item lifecycle and catalog records
  - member management and circulation workflow
  - RFID tag association
  - gate event handling
  - audit logging
  - dashboard metrics

### Migration utility
- File: migration_engine.py
- Responsibilities:
  - CSV import
  - validation and duplicate rejection
  - target DB inserts
  - reconciliation summary

### Dashboard
- File: streamlit_app.py
- Responsibilities:
  - library operations view
  - manual inventory simulation
  - gate alarm simulation

## 3. Data model
The prototype uses SQLAlchemy models for:
- DBItem
- DBMember
- DBCirculation
- DBGateEvent
- DBAuditLog

A local SQLite database is created automatically at runtime.

## 4. Mock integrations
The solution defines adapter-style mock handlers for:
- staff reader
- handheld reader
- security gate
- smart card credential provider
- email notifications
- SMS notifications
- print notifications
- CCTV snapshot path generation

These are not production vendor connectors, but they provide a working boundary for offline or isolated testing.

## 5. Operational view
- Local runtime uses FastAPI + SQLite
- Dashboard reads from local API endpoints
- Logging is configured in main.py
- Health checks are available via /health and /api/v1/reports/dashboard

## 6. Known limitations
- No production-grade deployment packaging
- No formal versioned migrations system
- No real NCIP/SIP2 vendor integrations
- No secure secret management
- No offline installer or rollback automation
- No SLA, monitoring, or support runbook yet

## 7. Recommended next milestone
Transition from prototype to compliant package by adding formal deployment scripts, admin docs, migration rollback checks, and a deployment architecture document.
