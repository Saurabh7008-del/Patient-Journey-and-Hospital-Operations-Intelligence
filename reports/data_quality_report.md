# Data Quality & Cleaning Report

Generated automatically by `python/02_clean_data.py`.

| Table | Input Rows | Output Rows | Issues Fixed (breakdown) |
|---|---|---|---|
| patients | 78,150 | 78,000 | duplicates removed: 150, invalid ages fixed: 90, missing city filled: 399, gender values standardized: 78000 |
| encounters | 200,250 | 200,000 | duplicates removed: 250, orphan patient refs removed: 0, missing wait time filled: 499, negative journey time fixed: 120 |
| admissions | 39,857 | 39,857 | orphan encounter refs removed: 0, negative los fixed: 60 |
| clinical_events | 1,255,414 | 1,255,414 | orphan encounter id removed: 0 |
| discharges | 39,857 | 39,857 | orphan encounter id removed: 0 |
| beds | 39,857 | 39,857 | orphan admission id removed: 0 |
| appointments | 150,000 | 150,000 | orphan patient id removed: 0 |
| readmissions | 1,166 | 1,166 | orphan patient id removed: 0 |

## Summary of cleaning operations applied

- **Duplicate records**: removed based on primary key
- **Missing values**: numeric fields imputed with median, categorical fields filled with 'Unknown'
- **Invalid ages**: values outside 0-110 replaced with dataset median age
- **Inconsistent category casing**: standardized to Title Case
- **Negative durations**: length_of_stay and total_journey_minutes corrected (absolute value)
- **Orphan foreign keys**: rows referencing non-existent parent records removed to preserve referential integrity
