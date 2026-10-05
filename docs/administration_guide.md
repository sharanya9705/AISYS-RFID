# Administration Guide

## 1. Overview
The AISYS prototype is designed for local cataloguing, circulation, RFID middleware simulation, and audit logging in an isolated library environment.

## 2. Roles and responsibilities
### Librarian
- manage catalog records
- validate item status
- process checkouts/checkins
- review RFID inventory reports

### Administrator
- configure local settings
- monitor system health
- inspect audit logs
- review assigned roles and permissions

### Security officer
- review gate events
- investigate security alerts
- verify CCTV snapshot paths and alert records

## 3. Access control model
The prototype supports role-based logic for staff members via the smart-card login route.

Current rule:
- STAFF and ADMIN roles are permitted
- other users receive a 401 unauthorized response

## 4. Operational checks
### Health
Use the health endpoint:
```http
GET /health
```

### Dashboard
Use the Streamlit dashboard to monitor:
- total catalog items
- tagged items
- active loans
- security alarms

## 5. Audit logging
The system writes audit events for:
- checkout actions
- checkin actions
- inventory scans
- gate events
- security notifications

Audit entries should be reviewed for:
- unusual inventory patterns
- unauthorized access attempts
- repeated member blocking or fine threshold events

## 6. Database maintenance
- keep the SQLite database under a controlled folder
- perform regular backups before migration or patching
- do not modify library records without validation or a rollback path

## 7. Site configuration recommendations
- keep database files on a local protected path
- maintain separate copies for test and production
- document default shelf locations and RFID tag assignments
- manage staff card UID values in a controlled registry

## 8. Problem triage
### Symptom: API not starting
Check:
- Python environment correctness
- dependency install state
- current working directory
- database file availability

### Symptom: dashboard cannot reach API
Check:
- API server is running on the correct port
- local host URL is reachable
- firewall or local port restrictions are absent

### Symptom: gate alarm triggered unexpectedly
Check:
- item status is available or untagged
- RFID EPC mapping is valid
- item was properly checked out before leaving the library

## 9. Security guidance
- do not store secrets in source files
- mask logs containing personal member details
- review audit logs regularly
- validate all input before data manipulation
