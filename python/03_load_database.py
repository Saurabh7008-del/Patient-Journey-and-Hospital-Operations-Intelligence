from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
"""
03_load_database.py
Loads cleaned CSVs into a SQL database (SQLite engine - chosen because it
requires no separate server process, ships with Python, and is fully
GitHub-portable; the schema and SQL below are standard ANSI SQL and will
run unmodified on MySQL/Postgres if the reader prefers a server-based engine).
"""
import sqlite3
import pandas as pd
import os

CLEAN = str(ROOT / "data/cleaned")
DB_PATH = str(ROOT / "database/hospital_analytics.db")
SCHEMA_PATH = str(ROOT / "database/schema.sql")

if os.path.exists(DB_PATH):
    os.remove(DB_PATH)

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()
cur.executescript(open(SCHEMA_PATH).read())
conn.commit()

tables = ["departments", "doctors", "patients", "encounters", "admissions",
          "clinical_events", "discharges", "beds", "appointments", "readmissions"]

for t in tables:
    df = pd.read_csv(f"{CLEAN}/{t}.csv")
    df.to_sql(t, conn, if_exists="append", index=False)
    print(f"Loaded {t}: {len(df):,} rows")

# Helpful indexes for join-heavy analytical queries
index_stmts = [
    "CREATE INDEX IF NOT EXISTS idx_enc_patient ON encounters(patient_id)",
    "CREATE INDEX IF NOT EXISTS idx_enc_dept ON encounters(department_id)",
    "CREATE INDEX IF NOT EXISTS idx_enc_date ON encounters(encounter_date)",
    "CREATE INDEX IF NOT EXISTS idx_adm_encounter ON admissions(encounter_id)",
    "CREATE INDEX IF NOT EXISTS idx_adm_patient ON admissions(patient_id)",
    "CREATE INDEX IF NOT EXISTS idx_ce_encounter ON clinical_events(encounter_id)",
    "CREATE INDEX IF NOT EXISTS idx_ce_doctor ON clinical_events(doctor_id)",
    "CREATE INDEX IF NOT EXISTS idx_disch_encounter ON discharges(encounter_id)",
    "CREATE INDEX IF NOT EXISTS idx_beds_admission ON beds(admission_id)",
    "CREATE INDEX IF NOT EXISTS idx_appt_patient ON appointments(patient_id)",
    "CREATE INDEX IF NOT EXISTS idx_appt_doctor ON appointments(doctor_id)",
    "CREATE INDEX IF NOT EXISTS idx_readm_patient ON readmissions(patient_id)",
]
for stmt in index_stmts:
    cur.execute(stmt)
conn.commit()

# Validation
print("\n=== DATABASE VALIDATION ===")
cur.execute("SELECT COUNT(*) FROM encounters")
n = cur.fetchone()[0]
print(f"encounters row count: {n:,} (expected 200,000: {'PASS' if n == 200000 else 'CHECK - see cleaning step'})")

cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
all_tables = [r[0] for r in cur.fetchall()]
print(f"Tables in database: {len(all_tables)} -> {all_tables}")

conn.close()
print("\nDatabase written to:", DB_PATH)
