-- Core KPI queries
SELECT COUNT(*) AS total_encounters FROM encounters;

SELECT COUNT(*) AS total_patients FROM patients;

SELECT ROUND(100.0 * SUM(admission_flag) / COUNT(*), 2) AS admission_rate_pct
FROM encounters;

SELECT ROUND(AVG(wait_time_minutes), 1) AS average_wait_minutes
FROM encounters;

SELECT ROUND(AVG(total_journey_minutes), 1) AS average_journey_minutes
FROM encounters;

SELECT ROUND(AVG(length_of_stay), 2) AS average_los_days
FROM admissions;

SELECT ROUND(AVG(discharge_delay_hours), 2) AS average_discharge_delay_hours
FROM discharges;

SELECT ROUND(
    100.0 * SUM(CASE WHEN occupancy_status = 'Occupied' THEN 1 ELSE 0 END) / COUNT(*), 2
) AS bed_occupancy_rate_pct
FROM beds;

SELECT ROUND(
    100.0 * SUM(CASE WHEN appointment_status = 'No Show' THEN 1 ELSE 0 END) / COUNT(*), 2
) AS appointment_no_show_rate_pct
FROM appointments;

SELECT ROUND(
    100.0 * SUM(readmission_flag) / (SELECT COUNT(*) FROM admissions), 2
) AS readmission_rate_pct
FROM readmissions;
