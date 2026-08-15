# Data Dictionary

| Table           | Column                   | Description                                                                                          | Data Type   |
|:----------------|:-------------------------|:-----------------------------------------------------------------------------------------------------|:------------|
| admissions      | admission_id             | Unique admission identifier (primary key)                                                            | int64       |
| admissions      | encounter_id             | Foreign key to encounters                                                                            | int64       |
| admissions      | patient_id               | Foreign key to patients                                                                              | int64       |
| admissions      | admission_date           | Date of inpatient admission                                                                          | object      |
| admissions      | discharge_date           | Date the admission ended                                                                             | object      |
| admissions      | length_of_stay           | Inpatient length of stay in days                                                                     | float64     |
| admissions      | admission_type           | Emergency / Elective / Transfer / Maternity                                                          | object      |
| admissions      | discharge_status         | Discharged / Transferred / Deceased / Left Against Medical Advice                                    | object      |
| admissions      | discharge_delay_hours    | Hours between clinically-ready and actual discharge                                                  | float64     |
| appointments    | appointment_id           | Unique appointment identifier (primary key)                                                          | int64       |
| appointments    | patient_id               | Foreign key to patients                                                                              | int64       |
| appointments    | appointment_date         | Scheduled appointment date                                                                           | object      |
| appointments    | department_id            | Foreign key to departments                                                                           | int64       |
| appointments    | doctor_id                | Foreign key to doctors                                                                               | int64       |
| appointments    | appointment_type         | New Consultation / Follow-up / Diagnostic / Routine Checkup / Specialist Referral                    | object      |
| appointments    | scheduled_time           | Scheduled appointment timestamp                                                                      | object      |
| appointments    | actual_start_time        | Actual appointment start timestamp                                                                   | object      |
| appointments    | appointment_status       | Completed / Cancelled / No Show / Rescheduled                                                        | object      |
| appointments    | wait_time_minutes        | Minutes between scheduled and actual start (completed appointments only)                             | float64     |
| beds            | bed_id                   | Unique bed-occupancy event identifier (primary key)                                                  | int64       |
| beds            | department_id            | Foreign key to departments                                                                           | int64       |
| beds            | bed_type                 | General / ICU / Emergency / Private / Semi-Private                                                   | object      |
| beds            | occupancy_date           | Date the bed occupancy began                                                                         | object      |
| beds            | occupancy_status         | Occupied / Vacated / Cleaning / Reserved                                                             | object      |
| beds            | admission_id             | Foreign key to admissions                                                                            | int64       |
| clinical_events | event_id                 | Unique clinical event identifier (primary key)                                                       | int64       |
| clinical_events | encounter_id             | Foreign key to encounters                                                                            | int64       |
| clinical_events | event_type               | Registration / Triage / Consultation / Investigation / Treatment / Medication / Transfer / Discharge | object      |
| clinical_events | event_time               | Timestamp of the event                                                                               | object      |
| clinical_events | department_id            | Foreign key to departments                                                                           | int64       |
| clinical_events | doctor_id                | Foreign key to doctors                                                                               | int64       |
| departments     | department_id            | Unique department identifier (primary key)                                                           | int64       |
| departments     | department_name          | Department name (e.g., Emergency, Cardiology)                                                        | object      |
| departments     | department_type          | Category of department (Emergency Care/Inpatient/Specialty/etc.)                                     | object      |
| departments     | bed_capacity             | Total physical bed capacity of the department                                                        | int64       |
| departments     | operating_hours          | Department operating hours                                                                           | object      |
| discharges      | discharge_id             | Unique discharge identifier (primary key)                                                            | int64       |
| discharges      | encounter_id             | Foreign key to encounters                                                                            | int64       |
| discharges      | patient_id               | Foreign key to patients                                                                              | int64       |
| discharges      | discharge_date           | Date of discharge                                                                                    | object      |
| discharges      | discharge_status         | Discharged / Transferred / Deceased / Left Against Medical Advice                                    | object      |
| discharges      | delay_reason             | Reason for discharge delay (or 'No delay')                                                           | object      |
| discharges      | discharge_delay_hours    | Hours the discharge was delayed                                                                      | float64     |
| doctors         | doctor_id                | Unique doctor identifier (primary key)                                                               | int64       |
| doctors         | doctor_name              | Doctor's display name                                                                                | object      |
| doctors         | department_id            | Foreign key to departments                                                                           | int64       |
| doctors         | specialization           | Medical specialization                                                                               | object      |
| doctors         | experience_years         | Years of professional experience                                                                     | int64       |
| doctors         | shift_type               | Day / Night / Rotational                                                                             | object      |
| encounters      | encounter_id             | Unique encounter identifier (primary key)                                                            | int64       |
| encounters      | patient_id               | Foreign key to patients                                                                              | int64       |
| encounters      | encounter_date           | Calendar date of the encounter                                                                       | object      |
| encounters      | encounter_type           | Emergency / Outpatient / Inpatient / Follow-up                                                       | object      |
| encounters      | department_id            | Foreign key to departments                                                                           | int64       |
| encounters      | arrival_time             | Timestamp patient arrived at the hospital                                                            | object      |
| encounters      | registration_time        | Timestamp of front-desk registration                                                                 | object      |
| encounters      | triage_time              | Timestamp of triage assessment                                                                       | object      |
| encounters      | doctor_start_time        | Timestamp doctor consultation began                                                                  | object      |
| encounters      | investigation_start_time | Timestamp diagnostic investigation began                                                             | object      |
| encounters      | treatment_start_time     | Timestamp treatment began                                                                            | object      |
| encounters      | discharge_time           | Timestamp patient was discharged from this encounter                                                 | object      |
| encounters      | admission_flag           | 1 if the encounter resulted in inpatient admission, else 0                                           | int64       |
| encounters      | severity                 | Low / Medium / High / Critical                                                                       | object      |
| encounters      | wait_time_minutes        | Minutes from arrival to consultation start                                                           | float64     |
| encounters      | total_journey_minutes    | Minutes from arrival to discharge                                                                    | float64     |
| encounters      | outcome                  | Recovered / Referred / Admitted / Discharged / Deceased                                              | object      |
| patients        | patient_id               | Unique patient identifier (primary key)                                                              | int64       |
| patients        | age                      | Patient age in years (0-110, cleaned)                                                                | int64       |
| patients        | gender                   | Male / Female / Other                                                                                | object      |
| patients        | city                     | Patient's home city                                                                                  | object      |
| patients        | insurance_type           | Government Scheme / Private / Corporate / Self-Pay / None                                            | object      |
| patients        | patient_category         | General / Senior Citizen / Child / Maternity / Chronic Care                                          | object      |
| patients        | registration_date        | Date the patient first registered with the hospital                                                  | object      |
| readmissions    | readmission_id           | Unique readmission record identifier (primary key)                                                   | int64       |
| readmissions    | patient_id               | Foreign key to patients                                                                              | int64       |
| readmissions    | previous_encounter_id    | Foreign key to the prior encounter                                                                   | int64       |
| readmissions    | readmission_encounter_id | Foreign key to the subsequent encounter                                                              | int64       |
| readmissions    | previous_discharge_date  | Date of the prior discharge                                                                          | object      |
| readmissions    | readmission_date         | Date of the subsequent admission                                                                     | object      |
| readmissions    | days_between_visits      | Days between prior discharge and readmission                                                         | int64       |
| readmissions    | readmission_flag         | 1 if readmission occurred within 30 days, else 0                                                     | int64       |
| readmissions    | readmission_reason       | Reason for readmission (or 'Not a readmission' if outside window)                                    | object      |