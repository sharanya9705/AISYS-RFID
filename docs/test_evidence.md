# Test Evidence

## Command run
```powershell
cd "C:\Users\shara\OneDrive\Desktop\PROJECTS\AISYS\aisys-library-system"; pytest -q
```

## Result
```text
......                                                                   [100%]
6 passed, 1 warning in 3.32s
```

## Covered scenarios
The automated tests cover the key prototype acceptance flows:
- AC 02: RFID tag binding
- AC 03 and AC 04: checkout and circulation block rules
- AC 05: handheld inventory scan
- AC 06: gate unauthorized-removal detection
- AC 07: smart-card login authorization

## Warning noted
The warning is a Starlette/FastAPI deprecation warning for using httpx with starlette.testclient. This does not break the prototype, but it should be reviewed during a later hardening pass.

## Assessment
The current project has strong test evidence for the prototype level, but it does not yet provide complete evidence for:
- backup/restore
- offline-update rollback
- UAT evidence
- migration rollback and restore scenarios
- security and performance benchmarking

## Recommended next step
Add end-to-end regression tests for backup, migration rollback, and deployment package verification before claiming full SOP compliance.
