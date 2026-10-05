# Rollback and Restore Runbook

## 1. Purpose
This runbook provides a controlled process for rollback and restore in the event of migration failure, data corruption suspicion, or incorrect deployment changes.

## 2. Required safeguards
Before any migration or update:
1. create a backup of the SQLite database
2. archive the application source and config files
3. note current dependency versions
4. record the time and scope of the change

## 3. Backup procedure
Recommended manual backup process:
```powershell
Copy-Item "C:\Users\shara\OneDrive\Desktop\PROJECTS\AISYS\aisys-library-system\aisys_library.db" "C:\Users\shara\OneDrive\Desktop\PROJECTS\AISYS\aisys-library-system\backup\aisys_library_backup_YYYYMMDD_HHMMSS.db"
```

Also archive the project folder or relevant release bundle.

## 4. Migration rollback scenario
If a migration creates invalid records or breaks reconciliation:
1. stop the API and dashboard processes
2. restore the previous database copy
3. restore the prior source release package
4. rerun the validation step
5. verify using pytest and a basic data integrity check

## 5. Restore procedure
1. shut down the application
2. replace the current database file with the backup copy
3. restart the API and dashboard
4. confirm data integrity and health status
5. review audit logs and recent transactions

## 6. Post-restore validation
Run:
```powershell
cd "C:\Users\shara\OneDrive\Desktop\PROJECTS\AISYS\aisys-library-system"
pytest -q
```

Also check:
- app health endpoint
- recent circulation records
- inventory counts
- gate events still align with data expectations

## 7. Risk note
This prototype uses a local SQLite database and does not yet implement a full production backup scheduler or automated database snapshot service. The defined steps are suitable for controlled offline recovery but should be expanded for production deployment.
