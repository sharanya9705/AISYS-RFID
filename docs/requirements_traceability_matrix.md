# Requirements Traceability Matrix

## Scope
This document maps the AISYS prototype to the SOP requirements and identifies the implemented, partially implemented, and remaining production-readiness items.

## Status legend
- Implemented: working evidence exists in code or tests
- Partial: present but not yet production-grade
- Missing: no implementation or evidence in the repository yet

## Functional requirement coverage

| ID | Requirement area | Status | Evidence | Notes |
| --- | --- | --- | --- | --- |
| FR 01 | Core ILMS | Partial | [main.py](../main.py) | Cataloguing and circulation logic exists; not a full ILMS product |
| FR 02 | Web and search | Partial | [streamlit_app.py](../streamlit_app.py) | Search and dashboard are present; broader OPAC features remain limited |
| FR 03 | RFID interoperability | Implemented | [main.py](../main.py) | Mock RFID middleware and adapter logic are present |
| FR 04 | Circulation | Implemented | [main.py](../main.py) | Checkout, checkin, fine limit, and reference restriction flows implemented |
| FR 05 | Tagging | Implemented | [main.py](../main.py) | Tag-to-item binding is implemented |
| FR 06 | Inventory | Implemented | [main.py](../main.py) | Handheld scan logic covers missing/misplaced items |
| FR 07 | Security gate events | Implemented | [main.py](../main.py) | Gate alarm and notification logic implemented |
| FR 08 | Dashboard and reports | Partial | [main.py](../main.py), [streamlit_app.py](../streamlit_app.py) | Dashboard metrics are present but not a full operational reporting suite |
| FR 09 | Notifications | Partial | [main.py](../main.py) | Mock email/SMS/print adapters exist |
| FR 10 | Data migration | Implemented | [migration_engine.py](../migration_engine.py) | Validation, duplicate rejection, and reconciliation are included |
| FR 11 | Administration | Partial | [main.py](../main.py) | Audit log and health endpoints exist; full admin console remains limited |
| FR 12 | Offline lifecycle | Partial | [docs/deployment_guide.md](deployment_guide.md), [docs/rollback_and_restore_runbook.md](rollback_and_restore_runbook.md) | Offline process guidance added, but not a production installer |
| NFR 01 | Data integrity | Partial | [docs/rollback_and_restore_runbook.md](rollback_and_restore_runbook.md), [migration_engine.py](../migration_engine.py) | Backup and restore guidance exists; automation remains limited |
| NFR 02 | Security/privacy | Partial | [main.py](../main.py) | Input validation and logging are present; production secrets handling not yet operational |
| NFR 03 | Compatibility | Partial | [docs/deployment_guide.md](deployment_guide.md) | Windows-compatible local model is described but not production-hardened |
| NFR 04 | Licensing | Partial | [docs/software_bill_of_materials.md](software_bill_of_materials.md) | SBOM exists; package license review remains a project governance step |
| NFR 05 | Testability | Implemented | [test_solution.py](../test_solution.py) | Automated test evidence exists |
| NFR 06 | Maintainability | Partial | [migrations/README.md](../migrations/README.md) | Migration versioning concept exists; wider maintainability remains a next-phase task |
| NFR 07 | Supportability | Partial | [docs/administration_guide.md](administration_guide.md) | Support guidance exists; no 24x7 production support model yet |
| NFR 08 | Documentation | Partial | [docs](./) | Documentation set is in place but not a final production package |
| NFR 09 | Delivery | Partial | [README.md](../README.md) | Prototype package exists; not yet full production release certification |

## Acceptance scenario mapping

| AC ID | Scenario | Status | Evidence |
| --- | --- | --- | --- |
| AC 01 | Migration import and reconciliation | Implemented | [migration_engine.py](../migration_engine.py) |
| AC 02 | Tag binding | Implemented | [main.py](../main.py) |
| AC 03 | Checkout flow | Implemented | [main.py](../main.py), [test_solution.py](../test_solution.py) |
| AC 04 | Blocked member and fine limit | Implemented | [main.py](../main.py), [test_solution.py](../test_solution.py) |
| AC 05 | Handheld inventory scan | Implemented | [main.py](../main.py), [test_solution.py](../test_solution.py) |
| AC 06 | Gate alarm generation | Implemented | [main.py](../main.py), [test_solution.py](../test_solution.py) |
| AC 07 | Smart-card login | Implemented | [main.py](../main.py), [test_solution.py](../test_solution.py) |
| AC 08 | Dashboard and reports | Partial | [streamlit_app.py](../streamlit_app.py), [main.py](../main.py) |
| AC 09 | Offline update and rollback | Partial | [docs/deployment_guide.md](deployment_guide.md), [docs/rollback_and_restore_runbook.md](rollback_and_restore_runbook.md) |
| AC 10 | Restore from backup | Partial | [docs/rollback_and_restore_runbook.md](rollback_and_restore_runbook.md) |

## Deliverable mapping

| Deliverable | Status | Evidence |
| --- | --- | --- |
| D1 Requirements package | Partial | [docs/requirements_traceability_matrix.md](requirements_traceability_matrix.md) |
| D2 Architecture package | Implemented | [docs/architecture_package.md](architecture_package.md) |
| D3 Working prototype | Implemented | [main.py](../main.py), [streamlit_app.py](../streamlit_app.py) |
| D4 Source repository | Partial | [README.md](../README.md) and repo structure |
| D5 Database and migration | Partial | [migration_engine.py](../migration_engine.py), [migrations/README.md](../migrations/README.md) |
| D6 Test package | Implemented | [test_solution.py](../test_solution.py), [docs/test_evidence.md](test_evidence.md) |
| D7 Deployment package | Partial | [docs/deployment_guide.md](deployment_guide.md) |
| D8 Operational documentation | Partial | [docs/administration_guide.md](administration_guide.md), [docs/user_guide.md](user_guide.md) |
| D9 Demonstration | Partial | Prototype demonstrated through working app and tests |

## Conclusion
The repository demonstrates a substantial prototype and has enough evidence to support a demonstration-level submission. The remaining work is concentrated in production-hardening, release controls, and evidence for full SOP compliance rather than in the core application logic itself.
