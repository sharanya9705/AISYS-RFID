# Software Bill of Materials (SBOM)

## 1. Summary
The AISYS prototype relies on a small set of Python packages and local runtime services for demonstration and validation.

## 2. Dependencies
| Package | Version / constraint | Purpose |
| --- | --- | --- |
| fastapi | >=0.100.0 | API layer |
| uvicorn | >=0.22.0 | ASGI server |
| sqlalchemy | >=2.0.0 | ORM and database access |
| pydantic | >=2.0.0 | request/response validation |
| pandas | >=2.0.0 | spreadsheet processing |
| openpyxl | >=3.1.0 | Excel workbook support |
| pytest | >=8.0.0 | automated test execution |
| httpx | >=0.27.0 | test client support |
| streamlit | >=1.35.0 | dashboard interface |
| requests | >=2.31.0 | HTTP client to local API |

## 3. Licensing notes
This prototype uses open-source dependencies. The project should maintain and review package licences before any reuse beyond internal prototype use. 

## 4. Offline deployment note
For isolated environments, keep a local wheel cache or packaged dependency bundle to install without internet access.

## 5. Action required before production release
- record package licences
- confirm redistribution rights
- pin dependency versions in a lock file or internal package store
- validate compatibility with the target Windows environment
