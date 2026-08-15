-- ============================================================================
-- Patient Journey and Hospital Operations Intelligence
-- Database Schema (10 core relational tables)
-- Engine: SQLite (portable, zero-config). Standard ANSI SQL - compatible
-- with MySQL/PostgreSQL with minor type-name adjustments.
-- ============================================================================

DROP TABLE IF EXISTS readmissions;
DROP TABLE IF EXISTS appointments;
DROP TABLE IF EXISTS beds;
DROP TABLE IF EXISTS discharges;
DROP TABLE IF EXISTS clinical_events;
DROP TABLE IF EXISTS admissions;
DROP TABLE IF EXISTS encounters;
DROP TABLE IF EXISTS doctors;
DROP TABLE IF EXISTS patients;
DROP TABLE IF EXISTS departments;

CREATE TABLE departments (
    department_id     INTEGER PRIMARY KEY,
    department_name   TEXT NOT NULL,
    department_type   TEXT,
    bed_capacity       INTEGER,
    operating_hours    TEXT
);

CREATE TABLE doctors (
    doctor_id          INTEGER PRIMARY KEY,
    doctor_name        TEXT NOT NULL,
    department_id      INTEGER REFERENCES departments(department_id),
    specialization     TEXT,
    experience_years   INTEGER,
    shift_type         TEXT
);

CREATE TABLE patients (
    patient_id         INTEGER PRIMARY KEY,
    age                INTEGER,
    gender             TEXT,
    city               TEXT,
    insurance_type     TEXT,
    patient_category   TEXT,
    registration_date  TEXT
);

CREATE TABLE encounters (
    encounter_id                INTEGER PRIMARY KEY,
    patient_id                  INTEGER REFERENCES patients(patient_id),
    encounter_date               TEXT,
    encounter_type               TEXT,
    department_id                INTEGER REFERENCES departments(department_id),
    arrival_time                  TEXT,
    registration_time             TEXT,
    triage_time                   TEXT,
    doctor_start_time             TEXT,
    investigation_start_time      TEXT,
    treatment_start_time          TEXT,
    discharge_time                 TEXT,
    admission_flag                 INTEGER,
    severity                       TEXT,
    wait_time_minutes              REAL,
    total_journey_minutes          REAL,
    outcome                        TEXT
);

CREATE TABLE admissions (
    admission_id            INTEGER PRIMARY KEY,
    encounter_id            INTEGER REFERENCES encounters(encounter_id),
    patient_id               INTEGER REFERENCES patients(patient_id),
    admission_date            TEXT,
    discharge_date             TEXT,
    length_of_stay             REAL,
    admission_type             TEXT,
    discharge_status           TEXT,
    discharge_delay_hours      REAL
);

CREATE TABLE clinical_events (
    event_id         INTEGER PRIMARY KEY,
    encounter_id     INTEGER REFERENCES encounters(encounter_id),
    event_type       TEXT,
    event_time       TEXT,
    department_id    INTEGER REFERENCES departments(department_id),
    doctor_id        INTEGER REFERENCES doctors(doctor_id)
);

CREATE TABLE discharges (
    discharge_id            INTEGER PRIMARY KEY,
    encounter_id            INTEGER REFERENCES encounters(encounter_id),
    patient_id               INTEGER REFERENCES patients(patient_id),
    discharge_date             TEXT,
    discharge_status           TEXT,
    delay_reason                TEXT,
    discharge_delay_hours      REAL
);

CREATE TABLE beds (
    bed_id            INTEGER PRIMARY KEY,
    department_id     INTEGER REFERENCES departments(department_id),
    bed_type          TEXT,
    occupancy_date    TEXT,
    occupancy_status  TEXT,
    admission_id      INTEGER REFERENCES admissions(admission_id)
);

CREATE TABLE appointments (
    appointment_id         INTEGER PRIMARY KEY,
    patient_id             INTEGER REFERENCES patients(patient_id),
    appointment_date        TEXT,
    department_id           INTEGER REFERENCES departments(department_id),
    doctor_id                INTEGER REFERENCES doctors(doctor_id),
    appointment_type         TEXT,
    scheduled_time            TEXT,
    actual_start_time         TEXT,
    appointment_status        TEXT,
    wait_time_minutes         REAL
);

CREATE TABLE readmissions (
    readmission_id             INTEGER PRIMARY KEY,
    patient_id                 INTEGER REFERENCES patients(patient_id),
    previous_encounter_id      INTEGER REFERENCES encounters(encounter_id),
    readmission_encounter_id   INTEGER REFERENCES encounters(encounter_id),
    previous_discharge_date     TEXT,
    readmission_date             TEXT,
    days_between_visits          INTEGER,
    readmission_flag             INTEGER,
    readmission_reason           TEXT
);
