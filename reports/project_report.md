# Project Report

## 1. Problem Definition
Hospitals need visibility into patient flow, waiting times, capacity and discharge processes.

## 2. Data
The project uses 200,000 synthetic encounters and 10 relational tables covering patients, encounters, departments, doctors, admissions, clinical events, discharges, beds, appointments and readmissions.

## 3. Preparation
The raw generation process introduces controlled data-quality issues. Pandas then cleans duplicates, invalid values, missing fields and duration problems.

## 4. Analysis
SQL is used for the 30 business questions and operational KPIs. Python is used for EDA and visualization.

## 5. BI Layer
A Power BI-ready star schema is exported with dimension and fact files. Four dashboard previews summarize the results.

## 6. Findings
See `research/findings.md` and `reports/kpi_results.md`.

## 7. Recommendations
See `research/recommendations.md`.

## 8. Limitations
The data is synthetic and should not be interpreted as clinical evidence.
