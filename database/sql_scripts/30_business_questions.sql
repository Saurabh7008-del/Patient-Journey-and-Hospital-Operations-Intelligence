-- Patient Journey & Hospital Operations Intelligence — 30 Business Questions

-- Q1 [Patient Volume & Demand]
-- Which departments receive the highest number of patients?
SELECT d.department_name, COUNT(*) AS total_patients
FROM encounters e JOIN departments d ON e.department_id=d.department_id
GROUP BY d.department_name ORDER BY total_patients DESC;


-- Q2 [Patient Volume & Demand]
-- What is the monthly patient volume trend?
SELECT strftime('%Y-%m', encounter_date) AS month, COUNT(*) AS patient_volume
FROM encounters GROUP BY month ORDER BY month;


-- Q3 [Patient Volume & Demand]
-- Which encounter type contributes the most to total hospital visits?
SELECT encounter_type, COUNT(*) AS total_visits
FROM encounters GROUP BY encounter_type ORDER BY total_visits DESC;


-- Q4 [Patient Volume & Demand]
-- Which months have the highest patient volume?
SELECT strftime('%Y-%m', encounter_date) AS month, COUNT(*) AS patient_volume
FROM encounters GROUP BY month ORDER BY patient_volume DESC LIMIT 5;


-- Q5 [Patient Volume & Demand]
-- What percentage of encounters are emergency visits?
SELECT ROUND(100.0*SUM(CASE WHEN encounter_type='Emergency' THEN 1 ELSE 0 END)/COUNT(*),2) AS emergency_visit_pct
FROM encounters;


-- Q6 [Waiting Time & Patient Flow]
-- Which department has the highest average patient waiting time?
SELECT d.department_name, ROUND(AVG(e.wait_time_minutes),1) AS avg_wait_minutes
FROM encounters e JOIN departments d ON e.department_id=d.department_id
GROUP BY d.department_name ORDER BY avg_wait_minutes DESC LIMIT 1;


-- Q7 [Waiting Time & Patient Flow]
-- What is the average hospital-wide waiting time?
SELECT ROUND(AVG(wait_time_minutes),1) AS avg_wait_minutes FROM encounters;


-- Q8 [Waiting Time & Patient Flow]
-- Which encounter type has the longest waiting time?
SELECT encounter_type, ROUND(AVG(wait_time_minutes),1) AS avg_wait_minutes
FROM encounters GROUP BY encounter_type ORDER BY avg_wait_minutes DESC LIMIT 1;


-- Q9 [Waiting Time & Patient Flow]
-- How does waiting time vary by patient severity?
SELECT severity, ROUND(AVG(wait_time_minutes),1) AS avg_wait_minutes
FROM encounters GROUP BY severity ORDER BY avg_wait_minutes DESC;


-- Q10 [Waiting Time & Patient Flow]
-- Which departments handle high patient volume with high waiting time?
WITH dept AS (
SELECT d.department_name, COUNT(*) AS volume, ROUND(AVG(e.wait_time_minutes),1) AS avg_wait
FROM encounters e JOIN departments d ON e.department_id=d.department_id
GROUP BY d.department_name
), thresholds AS (
SELECT AVG(volume) AS avg_volume, AVG(avg_wait) AS avg_wait_threshold FROM dept
)
SELECT dept.* FROM dept CROSS JOIN thresholds
WHERE volume > avg_volume AND avg_wait > avg_wait_threshold
ORDER BY volume DESC;


-- Q11 [Length of Stay]
-- Which departments have the highest average Length of Stay?
SELECT d.department_name, ROUND(AVG(a.length_of_stay),2) AS avg_los_days
FROM admissions a JOIN encounters e ON a.encounter_id=e.encounter_id
JOIN departments d ON e.department_id=d.department_id
GROUP BY d.department_name ORDER BY avg_los_days DESC;


-- Q12 [Length of Stay]
-- What is the average Length of Stay for admitted patients?
SELECT ROUND(AVG(length_of_stay),2) AS avg_los_days FROM admissions;


-- Q13 [Length of Stay]
-- How does Length of Stay vary by admission type?
SELECT admission_type, ROUND(AVG(length_of_stay),2) AS avg_los_days, COUNT(*) AS admissions
FROM admissions GROUP BY admission_type ORDER BY avg_los_days DESC;


-- Q14 [Length of Stay]
-- Which patient categories have longer hospital stays?
SELECT p.patient_category, ROUND(AVG(a.length_of_stay),2) AS avg_los_days
FROM admissions a JOIN patients p ON a.patient_id=p.patient_id
GROUP BY p.patient_category ORDER BY avg_los_days DESC;


-- Q15 [Length of Stay]
-- Which departments have both high patient volume and high Length of Stay?
WITH dept AS (
SELECT d.department_name, COUNT(DISTINCT e.encounter_id) AS volume, ROUND(AVG(a.length_of_stay),2) AS avg_los
FROM departments d JOIN encounters e ON d.department_id=e.department_id
JOIN admissions a ON e.encounter_id=a.encounter_id
GROUP BY d.department_name
), t AS (SELECT AVG(volume) avgv, AVG(avg_los) avglos FROM dept)
SELECT dept.* FROM dept CROSS JOIN t WHERE volume > avgv AND avg_los > avglos ORDER BY volume DESC;


-- Q16 [Admissions & Bed Operations]
-- What is the overall hospital admission rate?
SELECT ROUND(100.0*SUM(admission_flag)/COUNT(*),2) AS admission_rate_pct FROM encounters;


-- Q17 [Admissions & Bed Operations]
-- Which departments have the highest admission rate?
SELECT d.department_name,
ROUND(100.0*SUM(e.admission_flag)/COUNT(*),2) AS admission_rate_pct
FROM encounters e JOIN departments d ON e.department_id=d.department_id
GROUP BY d.department_name ORDER BY admission_rate_pct DESC;


-- Q18 [Admissions & Bed Operations]
-- Which departments have the highest bed occupancy?
SELECT d.department_name,
ROUND(100.0*SUM(CASE WHEN b.occupancy_status='Occupied' THEN 1 ELSE 0 END)/COUNT(*),2) AS occupancy_rate_pct
FROM beds b JOIN departments d ON b.department_id=d.department_id
GROUP BY d.department_name ORDER BY occupancy_rate_pct DESC;


-- Q19 [Admissions & Bed Operations]
-- Which months show the highest bed utilization?
SELECT strftime('%Y-%m', occupancy_date) AS month,
ROUND(100.0*SUM(CASE WHEN occupancy_status='Occupied' THEN 1 ELSE 0 END)/COUNT(*),2) AS occupancy_rate_pct
FROM beds GROUP BY month ORDER BY occupancy_rate_pct DESC LIMIT 5;


-- Q20 [Admissions & Bed Operations]
-- Are high patient-volume departments also experiencing high bed utilization?
WITH volume AS (
SELECT department_id, COUNT(*) AS patient_volume FROM encounters GROUP BY department_id
), occupancy AS (
SELECT department_id, 100.0*SUM(CASE WHEN occupancy_status='Occupied' THEN 1 ELSE 0 END)/COUNT(*) AS occupancy_rate
FROM beds GROUP BY department_id
)
SELECT d.department_name, v.patient_volume, ROUND(o.occupancy_rate,2) AS occupancy_rate_pct
FROM volume v JOIN occupancy o ON v.department_id=o.department_id
JOIN departments d ON d.department_id=v.department_id
ORDER BY v.patient_volume DESC;


-- Q21 [Discharge Operations]
-- What percentage of patients experience discharge delays?
SELECT ROUND(100.0*SUM(CASE WHEN discharge_delay_hours>0 THEN 1 ELSE 0 END)/COUNT(*),2) AS discharge_delay_rate_pct
FROM discharges;


-- Q22 [Discharge Operations]
-- What are the most common reasons for discharge delays?
SELECT delay_reason, COUNT(*) AS delayed_cases
FROM discharges WHERE delay_reason!='No delay'
GROUP BY delay_reason ORDER BY delayed_cases DESC;


-- Q23 [Discharge Operations]
-- Which departments have the highest discharge delay rate?
SELECT d.department_name,
ROUND(100.0*SUM(CASE WHEN x.discharge_delay_hours>0 THEN 1 ELSE 0 END)/COUNT(*),2) AS delay_rate_pct
FROM discharges x JOIN encounters e ON x.encounter_id=e.encounter_id
JOIN departments d ON e.department_id=d.department_id
GROUP BY d.department_name ORDER BY delay_rate_pct DESC;


-- Q24 [Discharge Operations]
-- What is the average discharge delay time?
SELECT ROUND(AVG(discharge_delay_hours),2) AS avg_discharge_delay_hours FROM discharges;


-- Q25 [Discharge Operations]
-- Which discharge delay reason contributes the most delay hours?
SELECT delay_reason, ROUND(SUM(discharge_delay_hours),2) AS total_delay_hours
FROM discharges WHERE delay_reason!='No delay'
GROUP BY delay_reason ORDER BY total_delay_hours DESC LIMIT 1;


-- Q26 [Appointments]
-- Which departments have the highest appointment no-show rate?
SELECT d.department_name,
ROUND(100.0*SUM(CASE WHEN a.appointment_status='No Show' THEN 1 ELSE 0 END)/COUNT(*),2) AS no_show_rate_pct
FROM appointments a JOIN departments d ON a.department_id=d.department_id
GROUP BY d.department_name ORDER BY no_show_rate_pct DESC;


-- Q27 [Appointments]
-- Which departments have the longest appointment waiting time?
SELECT d.department_name, ROUND(AVG(a.wait_time_minutes),1) AS avg_wait_minutes
FROM appointments a JOIN departments d ON a.department_id=d.department_id
WHERE a.appointment_status='Completed'
GROUP BY d.department_name ORDER BY avg_wait_minutes DESC;


-- Q28 [Readmission & Patient Outcomes]
-- What is the overall patient readmission rate?
SELECT ROUND(100.0*SUM(r.readmission_flag)/(SELECT COUNT(*) FROM admissions),2) AS readmission_rate_pct
FROM readmissions r;


-- Q29 [Readmission & Patient Outcomes]
-- Which patient categories have the highest readmission rate?
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
ORDER BY readmission_rate_pct DESC;


-- Q30 [Readmission & Patient Outcomes]
-- Which departments have both high Length of Stay and high readmission rate?
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
ORDER BY l.avg_los DESC;

