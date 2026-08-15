from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
"""
01_generate_data.py
Generates synthetic hospital operations dataset:
10 core relational tables, with encounters table containing EXACTLY 200,000 rows.
No external network / API calls - fully self-contained, reproducible (seeded).
"""
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import os

SEED = 42
rng = np.random.default_rng(SEED)
OUT = str(ROOT / "data/raw")
os.makedirs(OUT, exist_ok=True)

N_ENCOUNTERS = 200_000
N_PATIENTS = 78_000
START_DATE = datetime(2024, 1, 1)
END_DATE = datetime(2025, 12, 31)
TOTAL_DAYS = (END_DATE - START_DATE).days

# ---------------------------------------------------------------------------
# 1. DEPARTMENTS
# ---------------------------------------------------------------------------
dept_names = ["Emergency", "General Medicine", "Cardiology", "Orthopedics",
              "Pediatrics", "Neurology", "Surgery", "Radiology", "ICU", "Outpatient"]
dept_types = ["Emergency Care", "Inpatient", "Specialty", "Specialty", "Specialty",
              "Specialty", "Inpatient", "Diagnostic", "Critical Care", "Outpatient"]
dept_bed_capacity = [40, 60, 30, 35, 25, 20, 45, 0, 30, 0]
dept_hours = ["24x7", "24x7", "8:00-20:00", "8:00-18:00", "8:00-18:00",
              "8:00-18:00", "24x7", "24x7", "24x7", "9:00-17:00"]

departments = pd.DataFrame({
    "department_id": range(1, 11),
    "department_name": dept_names,
    "department_type": dept_types,
    "bed_capacity": dept_bed_capacity,
    "operating_hours": dept_hours,
})
departments.to_csv(f"{OUT}/departments.csv", index=False)

# ---------------------------------------------------------------------------
# 2. DOCTORS
# ---------------------------------------------------------------------------
N_DOCTORS = 160
first_names = ["Aarav","Vivaan","Aditya","Vihaan","Arjun","Sai","Reyansh","Krishna",
                "Ishaan","Rohan","Ananya","Diya","Saanvi","Aadhya","Kiara","Myra",
                "Anika","Navya","Priya","Sneha","Rahul","Amit","Vikram","Sanjay",
                "Neha","Pooja","Kavya","Riya","Karan","Arnav","Dev","Ishita","Meera",
                "Nikhil","Tanvi","Yash","Zara","Farhan","Aisha","Imran"]
last_names = ["Sharma","Verma","Gupta","Iyer","Nair","Reddy","Rao","Patel","Mehta",
               "Kumar","Singh","Das","Chatterjee","Bhatt","Joshi","Malhotra","Kapoor",
               "Chawla","Bose","Menon"]
specializations = {
    1: ["Emergency Medicine", "Trauma Care"], 2: ["Internal Medicine", "General Physician"],
    3: ["Cardiologist", "Interventional Cardiology"], 4: ["Orthopedic Surgeon", "Joint Replacement"],
    5: ["Pediatrician", "Neonatology"], 6: ["Neurologist", "Neurosurgery"],
    7: ["General Surgeon", "Laparoscopic Surgery"], 8: ["Radiologist", "Diagnostic Imaging"],
    9: ["Intensivist", "Critical Care"], 10: ["General Physician", "Consultant"]
}
shift_types = ["Day", "Night", "Rotational"]

doc_dept = rng.integers(1, 11, N_DOCTORS)
doctors = pd.DataFrame({
    "doctor_id": range(1, N_DOCTORS + 1),
    "doctor_name": ["Dr. " + rng.choice(first_names) + " " + rng.choice(last_names) for _ in range(N_DOCTORS)],
    "department_id": doc_dept,
    "specialization": [rng.choice(specializations[d]) for d in doc_dept],
    "experience_years": rng.integers(1, 35, N_DOCTORS),
    "shift_type": rng.choice(shift_types, N_DOCTORS, p=[0.45, 0.25, 0.30]),
})
doctors.to_csv(f"{OUT}/doctors.csv", index=False)

# ---------------------------------------------------------------------------
# 1b. PATIENTS
# ---------------------------------------------------------------------------
cities = ["Lucknow","Kanpur","Delhi","Mumbai","Bengaluru","Chennai","Pune","Jaipur",
          "Hyderabad","Ahmedabad","Bhopal","Patna","Varanasi","Nagpur","Indore"]
insurance_types = ["Government Scheme", "Private Insurance", "Corporate Insurance", "Self-Pay", "None"]
patient_categories = ["General", "Senior Citizen", "Child", "Maternity", "Chronic Care"]

ages = rng.integers(0, 96, N_PATIENTS)
genders = rng.choice(["Male", "Female", "Other"], N_PATIENTS, p=[0.49, 0.49, 0.02])
reg_offsets = rng.integers(0, TOTAL_DAYS, N_PATIENTS)
reg_dates = [START_DATE + timedelta(days=int(d)) for d in reg_offsets]

def categorize(age):
    if age < 15:
        return "Child"
    if age >= 60:
        return "Senior Citizen"
    return rng.choice(["General", "Maternity", "Chronic Care"], p=[0.7, 0.15, 0.15])

patients = pd.DataFrame({
    "patient_id": range(1, N_PATIENTS + 1),
    "age": ages,
    "gender": genders,
    "city": rng.choice(cities, N_PATIENTS),
    "insurance_type": rng.choice(insurance_types, N_PATIENTS, p=[0.35, 0.25, 0.15, 0.20, 0.05]),
    "patient_category": [categorize(a) for a in ages],
    "registration_date": [d.strftime("%Y-%m-%d") for d in reg_dates],
})
patients.to_csv(f"{OUT}/patients.csv", index=False)

print("departments, doctors, patients generated:",
      len(departments), len(doctors), len(patients))

# ---------------------------------------------------------------------------
# 2. ENCOUNTERS  (main fact table - EXACTLY 200,000 rows)
# ---------------------------------------------------------------------------
encounter_types = ["Emergency", "Outpatient", "Inpatient", "Follow-up"]
severities = ["Low", "Medium", "High", "Critical"]
outcomes = ["Recovered", "Referred", "Admitted", "Discharged", "Deceased"]

enc_patient = rng.integers(1, N_PATIENTS + 1, N_ENCOUNTERS)
enc_dept = rng.integers(1, 11, N_ENCOUNTERS)
enc_type = rng.choice(encounter_types, N_ENCOUNTERS, p=[0.35, 0.40, 0.15, 0.10])
enc_severity = rng.choice(severities, N_ENCOUNTERS, p=[0.40, 0.35, 0.20, 0.05])
enc_day_offset = rng.integers(0, TOTAL_DAYS, N_ENCOUNTERS)
enc_dates = np.array([START_DATE + timedelta(days=int(d)) for d in enc_day_offset])

# arrival time-of-day: emergency skews all hours, outpatient skews daytime
arrival_hour = np.where(
    enc_type == "Emergency",
    rng.integers(0, 24, N_ENCOUNTERS),
    rng.integers(8, 20, N_ENCOUNTERS)
)
arrival_minute = rng.integers(0, 60, N_ENCOUNTERS)
arrival_dt = [enc_dates[i] + timedelta(hours=int(arrival_hour[i]), minutes=int(arrival_minute[i]))
              for i in range(N_ENCOUNTERS)]

# journey stage gaps in minutes (vary with severity: critical -> faster triage)
severity_speed = {"Critical": 0.4, "High": 0.7, "Medium": 1.0, "Low": 1.3}
speed_factor = np.array([severity_speed[s] for s in enc_severity])

reg_gap = np.clip(rng.normal(8, 4, N_ENCOUNTERS) * speed_factor, 1, None)
triage_gap = np.clip(rng.normal(15, 8, N_ENCOUNTERS) * speed_factor, 2, None)
doc_gap = np.clip(rng.normal(35, 20, N_ENCOUNTERS) * speed_factor, 3, None)
invest_gap = np.clip(rng.normal(40, 25, N_ENCOUNTERS) * speed_factor, 0, None)
treat_gap = np.clip(rng.normal(50, 30, N_ENCOUNTERS) * speed_factor, 5, None)
discharge_gap = np.clip(rng.normal(25, 15, N_ENCOUNTERS) * speed_factor, 3, None)

registration_time = [arrival_dt[i] + timedelta(minutes=float(reg_gap[i])) for i in range(N_ENCOUNTERS)]
triage_time = [registration_time[i] + timedelta(minutes=float(triage_gap[i])) for i in range(N_ENCOUNTERS)]
doctor_start_time = [triage_time[i] + timedelta(minutes=float(doc_gap[i])) for i in range(N_ENCOUNTERS)]
investigation_start_time = [doctor_start_time[i] + timedelta(minutes=float(invest_gap[i])) for i in range(N_ENCOUNTERS)]
treatment_start_time = [investigation_start_time[i] + timedelta(minutes=float(treat_gap[i])) for i in range(N_ENCOUNTERS)]
discharge_time = [treatment_start_time[i] + timedelta(minutes=float(discharge_gap[i])) for i in range(N_ENCOUNTERS)]

wait_time_minutes = np.round(reg_gap + triage_gap + doc_gap, 1)
total_journey_minutes = np.round(
    [(discharge_time[i] - arrival_dt[i]).total_seconds() / 60 for i in range(N_ENCOUNTERS)], 1)

# admission flag: inpatient encounters + some emergency/high-severity outpatient escalate
admission_flag = np.where(
    (enc_type == "Inpatient") |
    ((enc_type == "Emergency") & np.isin(enc_severity, ["High", "Critical"]) & (rng.random(N_ENCOUNTERS) < 0.55)),
    1, 0
)

outcome = np.select(
    [admission_flag == 1,
     (enc_severity == "Critical") & (rng.random(N_ENCOUNTERS) < 0.06),
     enc_type == "Emergency"],
    ["Admitted", "Deceased", "Referred"],
    default="Recovered"
)
outcome = np.where((outcome == "Recovered") & (rng.random(N_ENCOUNTERS) < 0.5), "Discharged", outcome)

encounters = pd.DataFrame({
    "encounter_id": range(1, N_ENCOUNTERS + 1),
    "patient_id": enc_patient,
    "encounter_date": [d.strftime("%Y-%m-%d") for d in enc_dates],
    "encounter_type": enc_type,
    "department_id": enc_dept,
    "arrival_time": [d.strftime("%Y-%m-%d %H:%M:%S") for d in arrival_dt],
    "registration_time": [d.strftime("%Y-%m-%d %H:%M:%S") for d in registration_time],
    "triage_time": [d.strftime("%Y-%m-%d %H:%M:%S") for d in triage_time],
    "doctor_start_time": [d.strftime("%Y-%m-%d %H:%M:%S") for d in doctor_start_time],
    "investigation_start_time": [d.strftime("%Y-%m-%d %H:%M:%S") for d in investigation_start_time],
    "treatment_start_time": [d.strftime("%Y-%m-%d %H:%M:%S") for d in treatment_start_time],
    "discharge_time": [d.strftime("%Y-%m-%d %H:%M:%S") for d in discharge_time],
    "admission_flag": admission_flag,
    "severity": enc_severity,
    "wait_time_minutes": wait_time_minutes,
    "total_journey_minutes": total_journey_minutes,
    "outcome": outcome,
})
encounters.to_csv(f"{OUT}/encounters.csv", index=False)
print("encounters generated:", len(encounters), "| admitted:", int(admission_flag.sum()))

# ---------------------------------------------------------------------------
# 5. ADMISSIONS  (subset of encounters where admission_flag == 1)
# ---------------------------------------------------------------------------
adm_mask = admission_flag == 1
adm_encounter_ids = encounters.loc[adm_mask, "encounter_id"].values
adm_patient_ids = encounters.loc[adm_mask, "patient_id"].values
adm_dates = pd.to_datetime(encounters.loc[adm_mask, "encounter_date"]).values
N_ADM = len(adm_encounter_ids)

admission_types = ["Emergency", "Elective", "Transfer", "Maternity"]
discharge_statuses = ["Discharged", "Transferred", "Deceased", "Left Against Medical Advice"]

los_days = np.round(np.clip(rng.gamma(shape=2.0, scale=2.2, size=N_ADM), 0.5, 60), 1)
adm_discharge_dates = [pd.Timestamp(adm_dates[i]) + timedelta(days=float(los_days[i])) for i in range(N_ADM)]
discharge_delay_hours = np.round(np.clip(rng.exponential(4.5, N_ADM), 0, 96), 1)

admissions = pd.DataFrame({
    "admission_id": range(1, N_ADM + 1),
    "encounter_id": adm_encounter_ids,
    "patient_id": adm_patient_ids,
    "admission_date": pd.to_datetime(adm_dates).strftime("%Y-%m-%d"),
    "discharge_date": [d.strftime("%Y-%m-%d") for d in adm_discharge_dates],
    "length_of_stay": los_days,
    "admission_type": rng.choice(admission_types, N_ADM, p=[0.5, 0.3, 0.1, 0.1]),
    "discharge_status": rng.choice(discharge_statuses, N_ADM, p=[0.85, 0.08, 0.04, 0.03]),
    "discharge_delay_hours": discharge_delay_hours,
})
admissions.to_csv(f"{OUT}/admissions.csv", index=False)
print("admissions generated:", len(admissions))

# ---------------------------------------------------------------------------
# 6. CLINICAL_EVENTS  (multiple stage events per encounter)
# ---------------------------------------------------------------------------
event_type_names = ["Registration", "Triage", "Consultation", "Investigation",
                     "Treatment", "Medication", "Transfer", "Discharge"]
event_time_cols = {
    "Registration": "registration_time", "Triage": "triage_time",
    "Consultation": "doctor_start_time", "Investigation": "investigation_start_time",
    "Treatment": "treatment_start_time", "Discharge": "discharge_time",
}

# every encounter gets Registration, Triage, Consultation, Treatment, Discharge (5 core events)
# + probabilistic Investigation, Medication, Transfer
core_events = ["Registration", "Triage", "Consultation", "Treatment", "Discharge"]
doc_by_dept = doctors.groupby("department_id")["doctor_id"].apply(list).to_dict()

event_rows = []
enc_ids_arr = encounters["encounter_id"].values
enc_dept_arr = encounters["department_id"].values
enc_time_lookup = {
    "Registration": pd.to_datetime(encounters["registration_time"]).values,
    "Triage": pd.to_datetime(encounters["triage_time"]).values,
    "Consultation": pd.to_datetime(encounters["doctor_start_time"]).values,
    "Investigation": pd.to_datetime(encounters["investigation_start_time"]).values,
    "Treatment": pd.to_datetime(encounters["treatment_start_time"]).values,
    "Discharge": pd.to_datetime(encounters["discharge_time"]).values,
}

def pick_doctors(dept_array):
    out = np.empty(len(dept_array), dtype=int)
    for d in np.unique(dept_array):
        idx = np.flatnonzero(dept_array == d)
        choices = np.array(doc_by_dept.get(int(d), [1]), dtype=int)
        out[idx] = rng.choice(choices, size=len(idx))
    return out

chunks = []
eid_counter = 1
for etype in core_events:
    n = N_ENCOUNTERS
    depts = enc_dept_arr
    docids = pick_doctors(depts)
    chunks.append(pd.DataFrame({
        "event_type": etype,
        "event_time": enc_time_lookup[etype],
        "encounter_id": enc_ids_arr,
        "department_id": depts,
        "doctor_id": docids,
    }))

# probabilistic extra events
for etype, prob, base_col in [("Investigation", 0.65, "Investigation"),
                               ("Medication", 0.55, "Treatment"),
                               ("Transfer", 0.08, "Treatment")]:
    mask = rng.random(N_ENCOUNTERS) < prob
    depts = enc_dept_arr[mask]
    docids = pick_doctors(depts)
    chunks.append(pd.DataFrame({
        "event_type": etype,
        "event_time": enc_time_lookup[base_col][mask],
        "encounter_id": enc_ids_arr[mask],
        "department_id": depts,
        "doctor_id": docids,
    }))

clinical_events = pd.concat(chunks, ignore_index=True)
clinical_events = clinical_events.sort_values(["encounter_id", "event_time"]).reset_index(drop=True)
clinical_events.insert(0, "event_id", range(1, len(clinical_events) + 1))
clinical_events["event_time"] = pd.to_datetime(clinical_events["event_time"]).astype(str)
clinical_events = clinical_events[["event_id", "encounter_id", "event_type", "event_time", "department_id", "doctor_id"]]
clinical_events.to_csv(f"{OUT}/clinical_events.csv", index=False)
print("clinical_events generated:", len(clinical_events))

# ---------------------------------------------------------------------------
# 7. DISCHARGES  (aligned to admissions)
# ---------------------------------------------------------------------------
delay_reasons = ["Bed unavailable", "Pending investigation", "Doctor approval",
                  "Pharmacy delay", "Transport delay", "Insurance authorization",
                  "Administrative processing", "No delay"]

discharges = pd.DataFrame({
    "discharge_id": range(1, N_ADM + 1),
    "encounter_id": adm_encounter_ids,
    "patient_id": adm_patient_ids,
    "discharge_date": admissions["discharge_date"].values,
    "discharge_status": admissions["discharge_status"].values,
    "delay_reason": np.where(
        discharge_delay_hours < 1.0, "No delay",
        rng.choice(delay_reasons[:-1], N_ADM)
    ),
    "discharge_delay_hours": discharge_delay_hours,
})
discharges.to_csv(f"{OUT}/discharges.csv", index=False)
print("discharges generated:", len(discharges))

# ---------------------------------------------------------------------------
# 8. BEDS  (bed occupancy events, one per admission)
# ---------------------------------------------------------------------------
bed_types_by_dept = {
    1: "Emergency", 2: "General", 3: "Private", 4: "General", 5: "General",
    6: "Semi-Private", 7: "Private", 8: "General", 9: "ICU", 10: "General"
}
occupancy_statuses = ["Occupied", "Vacated", "Cleaning", "Reserved"]

adm_dept = encounters.set_index("encounter_id").loc[adm_encounter_ids, "department_id"].values
N_PHYSICAL_BEDS = int(departments["bed_capacity"].sum())  # ~285 physical beds

beds = pd.DataFrame({
    "bed_id": range(1, N_ADM + 1),
    "department_id": adm_dept,
    "bed_type": [bed_types_by_dept[d] for d in adm_dept],
    "occupancy_date": admissions["admission_date"].values,
    "occupancy_status": rng.choice(occupancy_statuses, N_ADM, p=[0.55, 0.35, 0.06, 0.04]),
    "admission_id": admissions["admission_id"].values,
})
beds.to_csv(f"{OUT}/beds.csv", index=False)
print("beds (occupancy records) generated:", len(beds), "| physical bed capacity (from departments):", N_PHYSICAL_BEDS)

# ---------------------------------------------------------------------------
# 9. APPOINTMENTS  (separate outpatient scheduling table)
# ---------------------------------------------------------------------------
N_APPT = 150_000
appt_types = ["New Consultation", "Follow-up", "Diagnostic", "Routine Checkup", "Specialist Referral"]
appt_statuses = ["Completed", "Cancelled", "No Show", "Rescheduled"]

appt_patient = rng.integers(1, N_PATIENTS + 1, N_APPT)
appt_dept = rng.integers(1, 11, N_APPT)
appt_doc = pick_doctors(appt_dept)
appt_day_offset = rng.integers(0, TOTAL_DAYS, N_APPT)
appt_dates = np.array([START_DATE + timedelta(days=int(d)) for d in appt_day_offset])
sched_hour = rng.integers(8, 19, N_APPT)
sched_minute = rng.choice([0, 15, 30, 45], N_APPT)
scheduled_dt = [appt_dates[i] + timedelta(hours=int(sched_hour[i]), minutes=int(sched_minute[i])) for i in range(N_APPT)]

status = rng.choice(appt_statuses, N_APPT, p=[0.72, 0.10, 0.10, 0.08])
delay_min = np.clip(rng.normal(18, 15, N_APPT), -10, 120)
actual_start_dt = [scheduled_dt[i] + timedelta(minutes=float(delay_min[i])) if status[i] == "Completed"
                    else scheduled_dt[i] for i in range(N_APPT)]
wait_time = np.where(status == "Completed", np.round(np.clip(delay_min, 0, None), 1), np.nan)

appointments = pd.DataFrame({
    "appointment_id": range(1, N_APPT + 1),
    "patient_id": appt_patient,
    "appointment_date": [d.strftime("%Y-%m-%d") for d in appt_dates],
    "department_id": appt_dept,
    "doctor_id": appt_doc,
    "appointment_type": rng.choice(appt_types, N_APPT, p=[0.25, 0.30, 0.20, 0.15, 0.10]),
    "scheduled_time": [d.strftime("%Y-%m-%d %H:%M:%S") for d in scheduled_dt],
    "actual_start_time": [d.strftime("%Y-%m-%d %H:%M:%S") for d in actual_start_dt],
    "appointment_status": status,
    "wait_time_minutes": wait_time,
})
appointments.to_csv(f"{OUT}/appointments.csv", index=False)
print("appointments generated:", len(appointments))

# ---------------------------------------------------------------------------
# 10. READMISSIONS  (derived from admissions: same patient, next admission <=30 days after prior discharge)
# ---------------------------------------------------------------------------
adm_sorted = admissions.copy()
adm_sorted["admission_date_dt"] = pd.to_datetime(adm_sorted["admission_date"])
adm_sorted["discharge_date_dt"] = pd.to_datetime(adm_sorted["discharge_date"])
adm_sorted = adm_sorted.sort_values(["patient_id", "admission_date_dt"]).reset_index(drop=True)

readmission_reasons = ["Infection recurrence", "Incomplete recovery", "Medication non-compliance",
                        "Post-surgical complication", "Chronic condition flare-up",
                        "Unrelated new condition", "Scheduled follow-up admission"]

records = []
rid = 1
for pid, grp in adm_sorted.groupby("patient_id"):
    grp = grp.reset_index(drop=True)
    for i in range(len(grp) - 1):
        prev_discharge = grp.loc[i, "discharge_date_dt"]
        next_admission = grp.loc[i + 1, "admission_date_dt"]
        gap_days = (next_admission - prev_discharge).days
        if 0 <= gap_days <= 45:  # capture near-term readmissions window
            flag = 1 if gap_days <= 30 else 0
            records.append({
                "readmission_id": rid,
                "patient_id": pid,
                "previous_encounter_id": grp.loc[i, "encounter_id"],
                "readmission_encounter_id": grp.loc[i + 1, "encounter_id"],
                "previous_discharge_date": prev_discharge.strftime("%Y-%m-%d"),
                "readmission_date": next_admission.strftime("%Y-%m-%d"),
                "days_between_visits": gap_days,
                "readmission_flag": flag,
                "readmission_reason": rng.choice(readmission_reasons) if flag == 1 else "Not a readmission (>30 days)",
            })
            rid += 1

readmissions = pd.DataFrame(records)
readmissions.to_csv(f"{OUT}/readmissions.csv", index=False)
print("readmissions generated:", len(readmissions), "| flagged readmissions (<=30 days):",
      int(readmissions["readmission_flag"].sum()) if len(readmissions) else 0)

print("\n=== RAW DATA GENERATION COMPLETE ===")
print("Tables created:", 10)
for f in sorted(os.listdir(OUT)):
    df = pd.read_csv(f"{OUT}/{f}")
    print(f"  {f:25s} -> {len(df):>8,} rows, {len(df.columns)} cols")
