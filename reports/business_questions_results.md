# Business Questions — Actual SQL Results

## Q1. Which departments receive the highest number of patients?
*Business area: Patient Volume & Demand*

```sql
SELECT d.department_name, COUNT(*) AS total_patients
FROM encounters e JOIN departments d ON e.department_id=d.department_id
GROUP BY d.department_name ORDER BY total_patients DESC
```

| department_name   |   total_patients |
|:------------------|-----------------:|
| Orthopedics       |            20169 |
| Emergency         |            20150 |
| Neurology         |            20099 |
| Pediatrics        |            20063 |
| Outpatient        |            19992 |
| General Medicine  |            19972 |
| ICU               |            19967 |
| Cardiology        |            19926 |
| Surgery           |            19913 |
| Radiology         |            19749 |


## Q2. What is the monthly patient volume trend?
*Business area: Patient Volume & Demand*

```sql
SELECT strftime('%Y-%m', encounter_date) AS month, COUNT(*) AS patient_volume
FROM encounters GROUP BY month ORDER BY month
```

| month   |   patient_volume |
|:--------|-----------------:|
| 2024-01 |             8434 |
| 2024-02 |             7953 |
| 2024-03 |             8548 |
| 2024-04 |             8156 |
| 2024-05 |             8338 |
| 2024-06 |             8335 |
| 2024-07 |             8545 |
| 2024-08 |             8576 |
| 2024-09 |             8223 |
| 2024-10 |             8636 |
| 2024-11 |             8228 |
| 2024-12 |             8464 |
| 2025-01 |             8560 |
| 2025-02 |             7726 |
| 2025-03 |             8499 |
| 2025-04 |             8049 |
| 2025-05 |             8474 |
| 2025-06 |             8166 |
| 2025-07 |             8489 |
| 2025-08 |             8446 |
| 2025-09 |             8259 |
| 2025-10 |             8425 |
| 2025-11 |             8290 |
| 2025-12 |             8181 |


## Q3. Which encounter type contributes the most to total hospital visits?
*Business area: Patient Volume & Demand*

```sql
SELECT encounter_type, COUNT(*) AS total_visits
FROM encounters GROUP BY encounter_type ORDER BY total_visits DESC
```

| encounter_type   |   total_visits |
|:-----------------|---------------:|
| Outpatient       |          80167 |
| Emergency        |          69813 |
| Inpatient        |          30124 |
| Follow-up        |          19896 |


## Q4. Which months have the highest patient volume?
*Business area: Patient Volume & Demand*

```sql
SELECT strftime('%Y-%m', encounter_date) AS month, COUNT(*) AS patient_volume
FROM encounters GROUP BY month ORDER BY patient_volume DESC LIMIT 5
```

| month   |   patient_volume |
|:--------|-----------------:|
| 2024-10 |             8636 |
| 2024-08 |             8576 |
| 2025-01 |             8560 |
| 2024-03 |             8548 |
| 2024-07 |             8545 |


## Q5. What percentage of encounters are emergency visits?
*Business area: Patient Volume & Demand*

```sql
SELECT ROUND(100.0*SUM(CASE WHEN encounter_type='Emergency' THEN 1 ELSE 0 END)/COUNT(*),2) AS emergency_visit_pct
FROM encounters
```

|   emergency_visit_pct |
|----------------------:|
|                 34.91 |


## Q6. Which department has the highest average patient waiting time?
*Business area: Waiting Time & Patient Flow*

```sql
SELECT d.department_name, ROUND(AVG(e.wait_time_minutes),1) AS avg_wait_minutes
FROM encounters e JOIN departments d ON e.department_id=d.department_id
GROUP BY d.department_name ORDER BY avg_wait_minutes DESC LIMIT 1
```

| department_name   |   avg_wait_minutes |
|:------------------|-------------------:|
| Neurology         |               60.8 |


## Q7. What is the average hospital-wide waiting time?
*Business area: Waiting Time & Patient Flow*

```sql
SELECT ROUND(AVG(wait_time_minutes),1) AS avg_wait_minutes FROM encounters
```

|   avg_wait_minutes |
|-------------------:|
|               60.4 |


## Q8. Which encounter type has the longest waiting time?
*Business area: Waiting Time & Patient Flow*

```sql
SELECT encounter_type, ROUND(AVG(wait_time_minutes),1) AS avg_wait_minutes
FROM encounters GROUP BY encounter_type ORDER BY avg_wait_minutes DESC LIMIT 1
```

| encounter_type   |   avg_wait_minutes |
|:-----------------|-------------------:|
| Follow-up        |               60.6 |


## Q9. How does waiting time vary by patient severity?
*Business area: Waiting Time & Patient Flow*

```sql
SELECT severity, ROUND(AVG(wait_time_minutes),1) AS avg_wait_minutes
FROM encounters GROUP BY severity ORDER BY avg_wait_minutes DESC
```

| severity   |   avg_wait_minutes |
|:-----------|-------------------:|
| Low        |               76.1 |
| Medium     |               58.8 |
| High       |               41.2 |
| Critical   |               24   |


## Q10. Which departments handle high patient volume with high waiting time?
*Business area: Waiting Time & Patient Flow*

```sql
WITH dept AS (
SELECT d.department_name, COUNT(*) AS volume, ROUND(AVG(e.wait_time_minutes),1) AS avg_wait
FROM encounters e JOIN departments d ON e.department_id=d.department_id
GROUP BY d.department_name
), thresholds AS (
SELECT AVG(volume) AS avg_volume, AVG(avg_wait) AS avg_wait_threshold FROM dept
)
SELECT dept.* FROM dept CROSS JOIN thresholds
WHERE volume > avg_volume AND avg_wait > avg_wait_threshold
ORDER BY volume DESC
```

| department_name   |   volume |   avg_wait |
|:------------------|---------:|-----------:|
| Neurology         |    20099 |       60.8 |


## Q11. Which departments have the highest average Length of Stay?
*Business area: Length of Stay*

```sql
SELECT d.department_name, ROUND(AVG(a.length_of_stay),2) AS avg_los_days
FROM admissions a JOIN encounters e ON a.encounter_id=e.encounter_id
JOIN departments d ON e.department_id=d.department_id
GROUP BY d.department_name ORDER BY avg_los_days DESC
```

| department_name   |   avg_los_days |
|:------------------|---------------:|
| General Medicine  |           4.48 |
| Surgery           |           4.47 |
| Pediatrics        |           4.47 |
| Cardiology        |           4.47 |
| Emergency         |           4.45 |
| Radiology         |           4.42 |
| Neurology         |           4.42 |
| ICU               |           4.42 |
| Outpatient        |           4.36 |
| Orthopedics       |           4.36 |


## Q12. What is the average Length of Stay for admitted patients?
*Business area: Length of Stay*

```sql
SELECT ROUND(AVG(length_of_stay),2) AS avg_los_days FROM admissions
```

|   avg_los_days |
|---------------:|
|           4.43 |


## Q13. How does Length of Stay vary by admission type?
*Business area: Length of Stay*

```sql
SELECT admission_type, ROUND(AVG(length_of_stay),2) AS avg_los_days, COUNT(*) AS admissions
FROM admissions GROUP BY admission_type ORDER BY avg_los_days DESC
```

| admission_type   |   avg_los_days |   admissions |
|:-----------------|---------------:|-------------:|
| Transfer         |           4.48 |         4015 |
| Maternity        |           4.44 |         3927 |
| Elective         |           4.44 |        11880 |
| Emergency        |           4.41 |        20035 |


## Q14. Which patient categories have longer hospital stays?
*Business area: Length of Stay*

```sql
SELECT p.patient_category, ROUND(AVG(a.length_of_stay),2) AS avg_los_days
FROM admissions a JOIN patients p ON a.patient_id=p.patient_id
GROUP BY p.patient_category ORDER BY avg_los_days DESC
```

| patient_category   |   avg_los_days |
|:-------------------|---------------:|
| Chronic Care       |           4.46 |
| Senior Citizen     |           4.45 |
| General            |           4.44 |
| Child              |           4.44 |
| Maternity          |           4.29 |


## Q15. Which departments have both high patient volume and high Length of Stay?
*Business area: Length of Stay*

```sql
WITH dept AS (
SELECT d.department_name, COUNT(DISTINCT e.encounter_id) AS volume, ROUND(AVG(a.length_of_stay),2) AS avg_los
FROM departments d JOIN encounters e ON d.department_id=e.department_id
JOIN admissions a ON e.encounter_id=a.encounter_id
GROUP BY d.department_name
), t AS (SELECT AVG(volume) avgv, AVG(avg_los) avglos FROM dept)
SELECT dept.* FROM dept CROSS JOIN t WHERE volume > avgv AND avg_los > avglos ORDER BY volume DESC
```

| department_name   |   volume |   avg_los |
|:------------------|---------:|----------:|
| Pediatrics        |     4181 |      4.47 |
| General Medicine  |     4029 |      4.48 |


## Q16. What is the overall hospital admission rate?
*Business area: Admissions & Bed Operations*

```sql
SELECT ROUND(100.0*SUM(admission_flag)/COUNT(*),2) AS admission_rate_pct FROM encounters
```

|   admission_rate_pct |
|---------------------:|
|                19.93 |


## Q17. Which departments have the highest admission rate?
*Business area: Admissions & Bed Operations*

```sql
SELECT d.department_name,
ROUND(100.0*SUM(e.admission_flag)/COUNT(*),2) AS admission_rate_pct
FROM encounters e JOIN departments d ON e.department_id=d.department_id
GROUP BY d.department_name ORDER BY admission_rate_pct DESC
```

| department_name   |   admission_rate_pct |
|:------------------|---------------------:|
| Pediatrics        |                20.84 |
| General Medicine  |                20.17 |
| Outpatient        |                19.96 |
| ICU               |                19.89 |
| Surgery           |                19.82 |
| Cardiology        |                19.81 |
| Neurology         |                19.76 |
| Orthopedics       |                19.72 |
| Emergency         |                19.72 |
| Radiology         |                19.59 |


## Q18. Which departments have the highest bed occupancy?
*Business area: Admissions & Bed Operations*

```sql
SELECT d.department_name,
ROUND(100.0*SUM(CASE WHEN b.occupancy_status='Occupied' THEN 1 ELSE 0 END)/COUNT(*),2) AS occupancy_rate_pct
FROM beds b JOIN departments d ON b.department_id=d.department_id
GROUP BY d.department_name ORDER BY occupancy_rate_pct DESC
```

| department_name   |   occupancy_rate_pct |
|:------------------|---------------------:|
| Neurology         |                56.26 |
| Radiology         |                55.56 |
| Pediatrics        |                55.56 |
| ICU               |                55.56 |
| Surgery           |                55.28 |
| Orthopedics       |                55.22 |
| General Medicine  |                55.2  |
| Emergency         |                53.55 |
| Outpatient        |                53.47 |
| Cardiology        |                53.46 |


## Q19. Which months show the highest bed utilization?
*Business area: Admissions & Bed Operations*

```sql
SELECT strftime('%Y-%m', occupancy_date) AS month,
ROUND(100.0*SUM(CASE WHEN occupancy_status='Occupied' THEN 1 ELSE 0 END)/COUNT(*),2) AS occupancy_rate_pct
FROM beds GROUP BY month ORDER BY occupancy_rate_pct DESC LIMIT 5
```

| month   |   occupancy_rate_pct |
|:--------|---------------------:|
| 2024-10 |                58.04 |
| 2024-08 |                57.27 |
| 2024-09 |                57.23 |
| 2024-03 |                56.81 |
| 2024-04 |                56.42 |


## Q20. Are high patient-volume departments also experiencing high bed utilization?
*Business area: Admissions & Bed Operations*

```sql
WITH volume AS (
SELECT department_id, COUNT(*) AS patient_volume FROM encounters GROUP BY department_id
), occupancy AS (
SELECT department_id, 100.0*SUM(CASE WHEN occupancy_status='Occupied' THEN 1 ELSE 0 END)/COUNT(*) AS occupancy_rate
FROM beds GROUP BY department_id
)
SELECT d.department_name, v.patient_volume, ROUND(o.occupancy_rate,2) AS occupancy_rate_pct
FROM volume v JOIN occupancy o ON v.department_id=o.department_id
JOIN departments d ON d.department_id=v.department_id
ORDER BY v.patient_volume DESC
```

| department_name   |   patient_volume |   occupancy_rate_pct |
|:------------------|-----------------:|---------------------:|
| Orthopedics       |            20169 |                55.22 |
| Emergency         |            20150 |                53.55 |
| Neurology         |            20099 |                56.26 |
| Pediatrics        |            20063 |                55.56 |
| Outpatient        |            19992 |                53.47 |
| General Medicine  |            19972 |                55.2  |
| ICU               |            19967 |                55.56 |
| Cardiology        |            19926 |                53.46 |
| Surgery           |            19913 |                55.28 |
| Radiology         |            19749 |                55.56 |


## Q21. What percentage of patients experience discharge delays?
*Business area: Discharge Operations*

```sql
SELECT ROUND(100.0*SUM(CASE WHEN discharge_delay_hours>0 THEN 1 ELSE 0 END)/COUNT(*),2) AS discharge_delay_rate_pct
FROM discharges
```

|   discharge_delay_rate_pct |
|---------------------------:|
|                       98.9 |


## Q22. What are the most common reasons for discharge delays?
*Business area: Discharge Operations*

```sql
SELECT delay_reason, COUNT(*) AS delayed_cases
FROM discharges WHERE delay_reason!='No delay'
GROUP BY delay_reason ORDER BY delayed_cases DESC
```

| delay_reason              |   delayed_cases |
|:--------------------------|----------------:|
| Pending investigation     |            4664 |
| Doctor approval           |            4664 |
| Bed unavailable           |            4640 |
| Transport delay           |            4617 |
| Insurance authorization   |            4566 |
| Administrative processing |            4525 |
| Pharmacy delay            |            4474 |


## Q23. Which departments have the highest discharge delay rate?
*Business area: Discharge Operations*

```sql
SELECT d.department_name,
ROUND(100.0*SUM(CASE WHEN x.discharge_delay_hours>0 THEN 1 ELSE 0 END)/COUNT(*),2) AS delay_rate_pct
FROM discharges x JOIN encounters e ON x.encounter_id=e.encounter_id
JOIN departments d ON e.department_id=d.department_id
GROUP BY d.department_name ORDER BY delay_rate_pct DESC
```

| department_name   |   delay_rate_pct |
|:------------------|-----------------:|
| Radiology         |            99.2  |
| ICU               |            99.12 |
| Cardiology        |            99.09 |
| Outpatient        |            98.97 |
| Pediatrics        |            98.9  |
| General Medicine  |            98.86 |
| Surgery           |            98.78 |
| Orthopedics       |            98.77 |
| Neurology         |            98.69 |
| Emergency         |            98.62 |


## Q24. What is the average discharge delay time?
*Business area: Discharge Operations*

```sql
SELECT ROUND(AVG(discharge_delay_hours),2) AS avg_discharge_delay_hours FROM discharges
```

|   avg_discharge_delay_hours |
|----------------------------:|
|                        4.44 |


## Q25. Which discharge delay reason contributes the most delay hours?
*Business area: Discharge Operations*

```sql
SELECT delay_reason, ROUND(SUM(discharge_delay_hours),2) AS total_delay_hours
FROM discharges WHERE delay_reason!='No delay'
GROUP BY delay_reason ORDER BY total_delay_hours DESC LIMIT 1
```

| delay_reason    |   total_delay_hours |
|:----------------|--------------------:|
| Doctor approval |             25538.9 |


## Q26. Which departments have the highest appointment no-show rate?
*Business area: Appointments*

```sql
SELECT d.department_name,
ROUND(100.0*SUM(CASE WHEN a.appointment_status='No Show' THEN 1 ELSE 0 END)/COUNT(*),2) AS no_show_rate_pct
FROM appointments a JOIN departments d ON a.department_id=d.department_id
GROUP BY d.department_name ORDER BY no_show_rate_pct DESC
```

| department_name   |   no_show_rate_pct |
|:------------------|-------------------:|
| Pediatrics        |              10.37 |
| Radiology         |              10.28 |
| Cardiology        |              10.26 |
| ICU               |              10.19 |
| General Medicine  |              10.12 |
| Outpatient        |               9.99 |
| Surgery           |               9.98 |
| Emergency         |               9.79 |
| Neurology         |               9.57 |
| Orthopedics       |               9.5  |


## Q27. Which departments have the longest appointment waiting time?
*Business area: Appointments*

```sql
SELECT d.department_name, ROUND(AVG(a.wait_time_minutes),1) AS avg_wait_minutes
FROM appointments a JOIN departments d ON a.department_id=d.department_id
WHERE a.appointment_status='Completed'
GROUP BY d.department_name ORDER BY avg_wait_minutes DESC
```

| department_name   |   avg_wait_minutes |
|:------------------|-------------------:|
| Radiology         |               19   |
| Pediatrics        |               19   |
| General Medicine  |               19   |
| Surgery           |               18.9 |
| Cardiology        |               18.9 |
| Orthopedics       |               18.8 |
| Neurology         |               18.8 |
| Emergency         |               18.8 |
| Outpatient        |               18.7 |
| ICU               |               18.7 |


## Q28. What is the overall patient readmission rate?
*Business area: Readmission & Patient Outcomes*

```sql
SELECT ROUND(100.0*SUM(r.readmission_flag)/(SELECT COUNT(*) FROM admissions),2) AS readmission_rate_pct
FROM readmissions r
```

|   readmission_rate_pct |
|-----------------------:|
|                   2.02 |


## Q29. Which patient categories have the highest readmission rate?
*Business area: Readmission & Patient Outcomes*

```sql
WITH admissions_by_cat AS (
SELECT p.patient_category, COUNT(*) AS admissions
FROM admissions a JOIN patients p ON a.patient_id=p.patient_id
GROUP BY p.patient_category
), readm_by_cat AS (
SELECT p.patient_category, SUM(r.readmission_flag) AS readmissions
FROM readmissions r JOIN patients p ON r.patient_id=p.patient_id
GROUP BY p.patient_category
)
SELECT a.patient_category, a.admissions, COALESCE(r.readmissions,0) AS readmissions,
ROUND(100.0*COALESCE(r.readmissions,0)/a.admissions,2) AS readmission_rate_pct
FROM admissions_by_cat a LEFT JOIN readm_by_cat r ON a.patient_category=r.patient_category
ORDER BY readmission_rate_pct DESC
```

| patient_category   |   admissions |   readmissions |   readmission_rate_pct |
|:-------------------|-------------:|---------------:|-----------------------:|
| General            |        12956 |            273 |                   2.11 |
| Child              |         6274 |            128 |                   2.04 |
| Chronic Care       |         2715 |             55 |                   2.03 |
| Senior Citizen     |        15020 |            302 |                   2.01 |
| Maternity          |         2892 |             46 |                   1.59 |


## Q30. Which departments have both high Length of Stay and high readmission rate?
*Business area: Readmission & Patient Outcomes*

```sql
WITH los AS (
SELECT e.department_id, AVG(a.length_of_stay) AS avg_los
FROM admissions a JOIN encounters e ON a.encounter_id=e.encounter_id
GROUP BY e.department_id
), readm AS (
SELECT e.department_id, 100.0*SUM(r.readmission_flag)/COUNT(*) AS readmission_rate
FROM readmissions r JOIN encounters e ON r.previous_encounter_id=e.encounter_id
GROUP BY e.department_id
), t AS (
SELECT AVG(avg_los) avglos FROM los
)
SELECT d.department_name, ROUND(l.avg_los,2) AS avg_los_days,
ROUND(COALESCE(r.readmission_rate,0),2) AS readmission_rate_pct
FROM los l JOIN departments d ON l.department_id=d.department_id
LEFT JOIN readm r ON l.department_id=r.department_id CROSS JOIN t
WHERE l.avg_los > t.avglos AND COALESCE(r.readmission_rate,0) > (SELECT AVG(readmission_rate) FROM readm)
ORDER BY l.avg_los DESC
```

| department_name   |   avg_los_days |   readmission_rate_pct |
|:------------------|---------------:|-----------------------:|
| General Medicine  |           4.48 |                  69.17 |
| Cardiology        |           4.47 |                  71.31 |

