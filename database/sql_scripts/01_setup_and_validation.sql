-- Database validation queries
SELECT name AS table_name
FROM sqlite_master
WHERE type = 'table'
ORDER BY name;

SELECT COUNT(*) AS encounter_count FROM encounters;

SELECT COUNT(*) AS patient_count FROM patients;

SELECT COUNT(*) AS admission_count FROM admissions;

SELECT COUNT(*) AS appointment_count FROM appointments;

SELECT COUNT(*) AS readmission_rows FROM readmissions;
