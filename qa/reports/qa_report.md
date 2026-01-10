# QA Report
- Generated: **2026-01-10 22:56 UTC**
- Summary: **4/4 checks passed**

## Results
### ✅ PASS — preflight (paths + dbt version) (mandatory)
```text
DBT_BIN=/Users/fatima/Desktop/analytics-domain-ownership/.venv/bin/dbt
DBT_PROJECT_DIR=/Users/fatima/Desktop/analytics-domain-ownership/domains/people_analytics
DBT_PROFILES_DIR=/Users/fatima/.dbt
```

### ✅ PASS — dbt parse (mandatory)
```text
[0m22:55:25  Running with dbt=1.11.2
[0m22:55:29  Registered adapter: bigquery=1.11.0
[0m22:55:29  Performance info: /Users/fatima/Desktop/analytics-domain-ownership/domains/people_analytics/target/perf_info.json
```

### ✅ PASS — dbt compile (mandatory)
```text
[0m22:55:31  Running with dbt=1.11.2
[0m22:55:35  Registered adapter: bigquery=1.11.0
[0m22:55:35  Found 6 models, 2 snapshots, 2 seeds, 13 data tests, 6 sources, 654 macros
[0m22:55:35  
[0m22:55:35  Concurrency: 2 threads (target='dev')
[0m22:55:35
```

### ✅ PASS — dbt test (select: test_type:generic) (mandatory)
```text
[0m22:55:39  Running with dbt=1.11.2
[0m22:55:42  Registered adapter: bigquery=1.11.0
[0m22:55:42  Found 6 models, 2 snapshots, 2 seeds, 13 data tests, 6 sources, 654 macros
[0m22:55:42  
[0m22:55:42  Concurrency: 2 threads (target='dev')
[0m22:55:42  
[0m22:55:44  1 of 13 START test accepted_values_fct_hiring_funnel_stage__applied__screened__interviewed__offered__hired__rejected  [RUN]
[0m22:55:44  2 of 13 START test not_null_dim_employee_scd2_employee_id ...................... [RUN]
[0m22:55:46  1 of 13 PASS accepted_values_fct_hiring_funnel_stage__applied__screened__interviewed__offered__hired__rejected  [[32mPASS[0m in 2.63s]
[0m22:55:46  2 of 13 PASS not_null_dim_employee_scd2_employee_id ............................ [[32mPASS[0m in 2.63s]
[0m22:55:46  3 of 13 START test not_null_dim_employee_scd2_is_current ....................... [RUN]
[0m22:55:46  4 of 13 START test not_null_dim_employee_scd2_valid_from ....................... [RUN]
[0m22:55:49  3 of 13 PASS not_null_dim_employee_scd2_is_current ............................. [[32mPASS[0m in 2.63s]
[0m22:55:49  4 of 13 PASS not_null_dim_employee_scd2_valid_from ............................. [[32mPASS[0m in 2.64s]
[0m22:55:49  5 of 13 START test not_null_fct_hiring_funnel_application_id ................... [RUN]
[0m22:55:49  6 of 13 START test not_null_fct_hiring_funnel_stage ............................ [RUN]
[0m22:55:51  5 of 13 PASS not_null_fct_hiring_funnel_application_id ......................... [[32mPASS[0m in 2.35s]
[0m22:55:51  7 of 13 START test not_null_int_employees_employee_id .......................... [RUN]
[0m22:55:52  6 of 13 PASS not_null_fct_hiring_funnel_stage .................................. [[32mPASS[0m in 2.68s]
[0m22:55:52  8 of 13 START test not_null_stg_employees_department ........................... [RUN]
[0m22:55:54  8 of 13 PASS not_null_stg_employees_department ................................. [[32mPASS[0m in 2.29s]
[0m22:55:54  9 of 13 START test not_null_stg_employees_employee_id .......................... [RUN]
[0m22:55:54  7 of 13 PASS not_null_int_employees_employee_id ................................ [[32mPASS[0m in 2.72s]
[0m22:55:54  10 of 13 START test not_null_stg_employees_hire_date ........................... [RUN]
[0m22:55:57  9 of 13 PASS not_null_stg_employees_employee_id ................................ [[32mPASS[0m in 2.68s]
[0m22:55:57  10 of 13 PASS not_null_stg_employees_hire_date ................................. [[32mPASS[0m in 2.60s]
[0m22:55:57  11 of 13 START test unique_dim_employee_scd2__employee_id_valid_from_ .......... [RUN]
[0m22:55:57  12 of 13 START test unique_int_employees_employee_id ........................... [RUN]
[0m22:55:59  11 of 13 PASS unique_dim_employee_scd2__employee_id_valid_from_ ................ [[32mPASS[0m in 2.51s]
[0m22:55:59  13 of 13 START test unique_stg_employees_employee_id ........................... [RUN]
[0m22:55:59  12 of 13 PASS unique_int_employees_employee_id ................................. [[32mPASS[0m in 2.67s]
[0m22:56:01  13 of 13 PASS unique_stg_employees_employee_id ................................. [[32mPASS[0m in 2.31s]
[0m22:56:01  
[0m22:56:01  Finished running 13 data tests in 0 hours 0 minutes and 19.18 seconds (19.18s).
[0m22:56:01  
[0m22:56:01  [32mCompleted successfully[0m
[0m22:56:01  
[0m22:56:01  Done. PASS=13 WARN=0 ERROR=0 SKIP=0 NO-OP=0 TOTAL=13
```
