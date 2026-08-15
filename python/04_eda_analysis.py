from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
"""
04_eda_analysis.py
Generates all required EDA visualizations from the cleaned dataset / SQLite DB.
Saved as PNG files under visualizations/ for use in README and reports.
"""
import sqlite3
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import os

DB_PATH = str(ROOT / "database/hospital_analytics.db")
VIZ = str(ROOT / "visualizations")
os.makedirs(VIZ, exist_ok=True)
conn = sqlite3.connect(DB_PATH)

plt.rcParams.update({
    "figure.facecolor": "white", "axes.facecolor": "white",
    "axes.edgecolor": "#333333", "axes.grid": True, "grid.alpha": 0.25,
    "font.size": 11, "axes.titlesize": 13, "axes.titleweight": "bold",
})
PALETTE = ["#2563eb", "#0891b2", "#059669", "#d97706", "#dc2626",
           "#7c3aed", "#db2777", "#65a30d", "#0d9488", "#4f46e5"]

def savefig(name):
    plt.tight_layout()
    plt.savefig(f"{VIZ}/{name}.png", dpi=150)
    plt.close()
    print("saved", name)

# 1. Encounters by department
df = pd.read_sql_query("""SELECT d.department_name, COUNT(*) c FROM encounters e
    JOIN departments d ON e.department_id=d.department_id
    GROUP BY d.department_name ORDER BY c DESC""", conn)
plt.figure(figsize=(9, 5))
plt.barh(df["department_name"][::-1], df["c"][::-1], color=PALETTE[0])
plt.title("Total Encounters by Department")
plt.xlabel("Encounters")
savefig("01_encounters_by_department")

# 2. Average wait time by department
df = pd.read_sql_query("""SELECT d.department_name, AVG(wait_time_minutes) w FROM encounters e
    JOIN departments d ON e.department_id=d.department_id
    GROUP BY d.department_name ORDER BY w DESC""", conn)
plt.figure(figsize=(9, 5))
plt.barh(df["department_name"][::-1], df["w"][::-1], color=PALETTE[3])
plt.title("Average Wait Time by Department (minutes)")
plt.xlabel("Minutes")
savefig("02_avg_wait_time_by_department")

# 3. Monthly encounter trend
df = pd.read_sql_query("""SELECT strftime('%Y-%m', encounter_date) month, COUNT(*) c
    FROM encounters GROUP BY month ORDER BY month""", conn)
plt.figure(figsize=(11, 5))
plt.plot(df["month"], df["c"], marker="o", color=PALETTE[1], linewidth=2)
plt.title("Monthly Encounter Volume Trend (2024-2025)")
plt.xticks(rotation=60)
plt.ylabel("Encounters")
savefig("03_monthly_encounter_trend")

# 4. Severity distribution
df = pd.read_sql_query("SELECT severity, COUNT(*) c FROM encounters GROUP BY severity ORDER BY c DESC", conn)
plt.figure(figsize=(6, 6))
plt.pie(df["c"], labels=df["severity"], autopct="%1.1f%%", colors=PALETTE, startangle=90)
plt.title("Encounter Severity Distribution")
savefig("04_severity_distribution")

# 5. LOS distribution
los = pd.read_sql_query("SELECT length_of_stay FROM admissions", conn)["length_of_stay"]
plt.figure(figsize=(9, 5))
plt.hist(los, bins=40, color=PALETTE[2], edgecolor="white")
plt.title("Length of Stay Distribution (days)")
plt.xlabel("Days"); plt.ylabel("Admissions")
savefig("05_length_of_stay_distribution")

# 6. Discharge delay reasons
df = pd.read_sql_query("""SELECT delay_reason, COUNT(*) c FROM discharges
    WHERE delay_reason != 'No delay' GROUP BY delay_reason ORDER BY c DESC""", conn)
plt.figure(figsize=(9, 5))
plt.barh(df["delay_reason"][::-1], df["c"][::-1], color=PALETTE[4])
plt.title("Discharge Delay Reasons")
plt.xlabel("Count")
savefig("06_discharge_delay_reasons")

# 7. Bed occupancy rate by department
df = pd.read_sql_query("""SELECT d.department_name,
    100.0*SUM(CASE WHEN b.occupancy_status='Occupied' THEN 1 ELSE 0 END)/COUNT(*) pct
    FROM beds b JOIN departments d ON b.department_id=d.department_id
    GROUP BY d.department_name ORDER BY pct DESC""", conn)
plt.figure(figsize=(9, 5))
plt.bar(df["department_name"], df["pct"], color=PALETTE[5])
plt.title("Bed Occupancy Rate by Department (%)")
plt.xticks(rotation=45, ha="right")
plt.ylabel("% Occupied")
savefig("07_bed_occupancy_by_department")

# 8. Appointment status breakdown
df = pd.read_sql_query("SELECT appointment_status, COUNT(*) c FROM appointments GROUP BY appointment_status", conn)
plt.figure(figsize=(6, 6))
plt.pie(df["c"], labels=df["appointment_status"], autopct="%1.1f%%", colors=PALETTE[1:], startangle=90)
plt.title("Appointment Status Breakdown")
savefig("08_appointment_status_breakdown")

# 9. Patient age distribution
age = pd.read_sql_query("SELECT age FROM patients", conn)["age"]
plt.figure(figsize=(9, 5))
plt.hist(age, bins=30, color=PALETTE[6], edgecolor="white")
plt.title("Patient Age Distribution")
plt.xlabel("Age"); plt.ylabel("Patients")
savefig("09_patient_age_distribution")

# 10. Readmission reasons
df = pd.read_sql_query("""SELECT readmission_reason, COUNT(*) c FROM readmissions
    WHERE readmission_flag=1 GROUP BY readmission_reason ORDER BY c DESC""", conn)
plt.figure(figsize=(9, 5))
plt.barh(df["readmission_reason"][::-1], df["c"][::-1], color=PALETTE[7])
plt.title("30-Day Readmission Reasons")
plt.xlabel("Count")
savefig("10_readmission_reasons")

# 11. Patient journey funnel (avg minutes at each stage)
df = pd.read_sql_query("""SELECT
    AVG((julianday(registration_time)-julianday(arrival_time))*1440) reg,
    AVG((julianday(triage_time)-julianday(registration_time))*1440) triage,
    AVG((julianday(doctor_start_time)-julianday(triage_time))*1440) doc,
    AVG((julianday(investigation_start_time)-julianday(doctor_start_time))*1440) invest,
    AVG((julianday(treatment_start_time)-julianday(investigation_start_time))*1440) treat,
    AVG((julianday(discharge_time)-julianday(treatment_start_time))*1440) disch
    FROM encounters""", conn)
stages = ["Arrival->\nRegistration", "Registration->\nTriage", "Triage->\nConsultation",
          "Consultation->\nInvestigation", "Investigation->\nTreatment", "Treatment->\nDischarge"]
vals = df.iloc[0].values
plt.figure(figsize=(10, 5))
plt.bar(stages, vals, color=PALETTE[:6])
plt.title("Average Time Spent per Patient Journey Stage (minutes)")
plt.ylabel("Minutes")
savefig("11_patient_journey_stage_times")

# 12. Encounter type vs outcome heatmap-style bar
df = pd.read_sql_query("""SELECT encounter_type, outcome, COUNT(*) c FROM encounters
    GROUP BY encounter_type, outcome""", conn)
pivot = df.pivot(index="encounter_type", columns="outcome", values="c").fillna(0)
pivot.plot(kind="bar", stacked=True, figsize=(10, 6), color=PALETTE)
plt.title("Encounter Outcomes by Encounter Type")
plt.ylabel("Encounters")
plt.xticks(rotation=0)
plt.legend(title="Outcome", bbox_to_anchor=(1.02, 1), loc="upper left")
savefig("12_outcomes_by_encounter_type")

conn.close()
print("\n=== EDA COMPLETE:", len(os.listdir(VIZ)), "visualizations saved ===")
