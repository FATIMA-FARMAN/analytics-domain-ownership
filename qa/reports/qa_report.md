# QA Report
- Generated: **2026-01-22 06:12 UTC**
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
[0m06:12:14  Running with dbt=1.11.2
[0m06:12:18  Registered adapter: bigquery=1.11.0
[0m06:12:18  Performance info: /Users/fatima/Desktop/analytics-domain-ownership/domains/people_analytics/target/perf_info.json
```

### ✅ PASS — dbt compile (mandatory)
```text
[0m06:12:21  Running with dbt=1.11.2
[0m06:12:24  Registered adapter: bigquery=1.11.0
[0m06:12:25  Found 6 models, 2 snapshots, 2 seeds, 13 data tests, 6 sources, 654 macros
[0m06:12:25  
[0m06:12:25  Concurrency: 4 threads (target='dev')
[0m06:12:25
```

### ✅ PASS — dbt test (select: test_type:generic) (mandatory)
```text
[0m06:12:28  Running with dbt=1.11.2
[0m06:12:32  Registered adapter: bigquery=1.11.0
[0m06:12:32  Found 6 models, 2 snapshots, 2 seeds, 13 data tests, 6 sources, 654 macros
[0m06:12:32  
[0m06:12:32  Concurrency: 4 threads (target='dev')
[0m06:12:32  
[0m06:12:34  1 of 13 START test accepted_values_fct_hiring_funnel_stage__applied__screened__interviewed__offered__hired__rejected  [RUN]
[0m06:12:34  3 of 13 START test not_null_dim_employee_scd2_is_current ....................... [RUN]
[0m06:12:34  4 of 13 START test not_null_dim_employee_scd2_valid_from ....................... [RUN]
[0m06:12:34  2 of 13 START test not_null_dim_employee_scd2_employee_id ...................... [RUN]
[0m06:12:36  1 of 13 PASS accepted_values_fct_hiring_funnel_stage__applied__screened__interviewed__offered__hired__rejected  [[32mPASS[0m in 2.44s]
[0m06:12:36  5 of 13 START test not_null_fct_hiring_funnel_application_id ................... [RUN]
[0m06:12:36  2 of 13 PASS not_null_dim_employee_scd2_employee_id ............................ [[32mPASS[0m in 2.53s]
[0m06:12:36  6 of 13 START test not_null_fct_hiring_funnel_stage ............................ [RUN]
[0m06:12:36  3 of 13 PASS not_null_dim_employee_scd2_is_current ............................. [[32mPASS[0m in 2.53s]
[0m06:12:36  7 of 13 START test not_null_int_employees_employee_id .......................... [RUN]
[0m06:12:36  4 of 13 PASS not_null_dim_employee_scd2_valid_from ............................. [[32mPASS[0m in 2.58s]
[0m06:12:36  8 of 13 START test not_null_stg_employees_department ........................... [RUN]
[0m06:12:38  6 of 13 PASS not_null_fct_hiring_funnel_stage .................................. [[32mPASS[0m in 2.23s]
[0m06:12:38  9 of 13 START test not_null_stg_employees_employee_id .......................... [RUN]
[0m06:12:39  5 of 13 PASS not_null_fct_hiring_funnel_application_id ......................... [[32mPASS[0m in 2.40s]
[0m06:12:39  10 of 13 START test not_null_stg_employees_hire_date ........................... [RUN]
[0m06:12:39  8 of 13 PASS not_null_stg_employees_department ................................. [[32mPASS[0m in 2.34s]
[0m06:12:39  11 of 13 START test unique_dim_employee_scd2__employee_id_valid_from_ .......... [RUN]
[0m06:12:39  7 of 13 PASS not_null_int_employees_employee_id ................................ [[32mPASS[0m in 2.49s]
[0m06:12:39  12 of 13 START test unique_int_employees_employee_id ........................... [RUN]
[0m06:12:41  9 of 13 PASS not_null_stg_employees_employee_id ................................ [[32mPASS[0m in 2.33s]
[0m06:12:41  13 of 13 START test unique_stg_employees_employee_id ........................... [RUN]
[0m06:12:41  10 of 13 PASS not_null_stg_employees_hire_date ................................. [[32mPASS[0m in 2.27s]
[0m06:12:41  11 of 13 PASS unique_dim_employee_scd2__employee_id_valid_from_ ................ [[32mPASS[0m in 2.38s]
[0m06:12:41  12 of 13 PASS unique_int_employees_employee_id ................................. [[32mPASS[0m in 2.50s]
[0m06:12:43  13 of 13 PASS unique_stg_employees_employee_id ................................. [[32mPASS[0m in 2.42s]
[0m06:12:43  
[0m06:12:43  Finished running 13 data tests in 0 hours 0 minutes and 10.75 seconds (10.75s).
[0m06:12:43  
[0m06:12:43  [32mCompleted successfully[0m
[0m06:12:43  
[0m06:12:43  Done. PASS=13 WARN=0 ERROR=0 SKIP=0 NO-OP=0 TOTAL=13
```
