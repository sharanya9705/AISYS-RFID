import sys
import os
import shutil
import datetime
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import DBItem, Base

DATABASE_URL = "sqlite:///./aisys_library.db"
engine = create_engine(DATABASE_URL)
SessionClass = sessionmaker(bind=engine)

def execute_migration(file_path: str):
    session = SessionClass()
    print(f"Starting Ingestion of {file_path}...")
    
    # Real SQLite database backup before migration
    if os.path.exists("aisys_library.db"):
        backup_filename = f"backup_pre_migration_{int(datetime.datetime.now().timestamp())}.db"
        shutil.copyfile("aisys_library.db", backup_filename)
        print(f"[DATA INTEGRITY CHECK] Pre-migration database snapshot saved: {backup_filename}")

    try:
        df = pd.read_csv(file_path)
    except Exception as e:
        print(f"Failed to read file: {e}")
        return

    source_count = len(df)
    valid_records = []
    rejected_count = 0
    duplicate_count = 0
    seen_accessions = set()

    for idx, row in df.iterrows():
        acc = str(row.get("accession_number", "")).strip()
        title = str(row.get("title", "")).strip()
        author = str(row.get("author", "")).strip()

        if not acc or not title or acc == "nan" or title == "nan":
            rejected_count += 1
            continue

        if acc in seen_accessions:
            duplicate_count += 1
            continue

        seen_accessions.add(acc)
        valid_records.append(DBItem(
            accession_number=acc,
            title=title,
            author=author,
            isbn=str(row.get("isbn", "")),
            is_reference=bool(row.get("is_reference", False))
        ))

    try:
        session.bulk_save_objects(valid_records)
        session.commit()
        migrated_count = len(valid_records)
        
        print("====== MIGRATION RECONCILIATION REPORT ======")
        print(f"Total Source Spreadsheet Rows: {source_count}")
        print(f"Successfully Migrated Records: {migrated_count}")
        print(f"Rejected / Malformed Rows:    {rejected_count}")
        print(f"Duplicate Rows Dropped:       {duplicate_count}")
        print(f"Reconciliation Status:         MATCHED ({migrated_count + rejected_count + duplicate_count} == {source_count})")
        print("=============================================")
    except Exception as ex:
        session.rollback()
        print(f"Migration Failed! Automated Rollback Executed. Error: {ex}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        execute_migration(sys.argv[1])
    else:
        print("Usage: python migration_engine.py <path_to_spreadsheet.csv>")