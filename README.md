# Analytics Domain Ownership  
**dbt · BigQuery · Airflow · CI · Data Contracts**

[![dbt CI (PR checks)](https://github.com/FATIMA-FARMAN/analytics-domain-ownership/actions/workflows/dbt-ci.yml/badge.svg)](https://github.com/FATIMA-FARMAN/analytics-domain-ownership/actions/workflows/dbt-ci.yml)

End-to-end analytics engineering portfolio demonstrating **domain ownership** across **People Analytics** and **Payments**.  
Focus areas include dbt modeling, cost-aware BigQuery patterns, Airflow orchestration, data contracts/tests, and lineage documentation.

---

## What this proves 

- Owns an analytics **domain end-to-end**
- Designs **staging → intermediate → marts (dim/fct)** intentionally
- Implements **incremental models** under BigQuery Sandbox constraints
- Enforces **data contracts & tests**
- Orchestrates dbt workflows with **Airflow**
- Ships **verifiable proof**, not claims

---

## What this project demonstrates

- **Domain ownership**  
  Each domain lives under `domains/<domain>/` with isolated models, tests, seeds, and DAGs.

- **Warehouse modeling discipline**  
  Clear separation of staging, intermediate, and marts with intentional materialization choices.

- **Cost-aware BigQuery patterns**  
  Avoid `SELECT *`, reuse intermediates for expensive joins, and plan partitioning/clustering for large facts.

- **Operational workflows**  
  Airflow DAGs orchestrate dbt runs; generated artifacts (venv/logs/target) are excluded from version control.

- **Data quality & governance**  
  Schema contracts and dbt tests ensure reliable downstream consumption.

- **Documentation & lineage**  
  dbt docs lineage and architecture diagrams support impact analysis and discovery.

---

## Proof / Evidence (recruiter scan)

- ✅ **Incremental compiled SQL proof (BigQuery Sandbox)**  
  - `assets/proof/compiled_fct_hiring_funnel_incremental.sql`  
  - ![Incremental compiled SQL proof](assets/proof/12_incremental_compiled_sql.png)

- ✅ **Fix incremental model casting and demo seed**  
  - `domains/people_analytics/models/marts/fct_hiring_funnel_incremental.sql`  
  - `domains/people_analytics/seeds/hiring_events_incremental_demo.csv`

- ✅ **Harden dbt contracts for SCD2 and hiring funnel marts**  
  - `models/marts/schema.yml` (key marts)

- ✅ **dbt test execution proof (PASS=13)**  
  - ![dbt test execution proof](assets/proof/10_dbt_test_people_analytics.png)

---

## Repository structure

```txt
analytics-domain-ownership/
  domains/
    people_analytics/
      dags/
      models/
      snapshots/
      seeds/
      tests/
      macros/
      packages.yml

## Cost-aware warehouse notes (BigQuery)

This repository is intentionally structured to demonstrate **cost-aware analytics engineering** on BigQuery—optimizing for **lower scan cost**, **predictable materialization**, and **fast iteration**.

### Incremental model note (BigQuery Sandbox)

The hiring funnel fact is implemented as a **dbt incremental model** with a timestamp-based filter.

BigQuery Sandbox (free tier) blocks DML operations required for incremental runs (e.g. **MERGE / INSERT**). As a result:

- `dbt compile` demonstrates correct incremental SQL generation  
- `dbt run --full-refresh` succeeds (DDL only)  
- Standard incremental runs require billing to execute  

This is a **warehouse limitation**, not a modeling issue.

---

### Materialization strategy

- **Staging (`stg_*`)** → materialized as **views**  
- **Intermediate (`int_*`)** → materialized as **tables** only when reused  
- **Marts (`dim_*`, `fct_*`)** → **views or tables** depending on access patterns and performance needs

---

### Query efficiency principles

- Avoid `SELECT *` in marts to reduce **bytes scanned**
- Centralize expensive joins and transformations in reusable intermediate models
- Optimize marts for **BI-friendly consumption** and interactive performance

---

### Partitioning & clustering (production pattern)

For large fact tables:

- **Partition** by a date column (e.g. `event_date`, `snapshot_date`)
- **Cluster** by common join or filter keys (e.g. `employee_id`, `department_id`)
- **Result:** lower scan cost and faster interactive queries

---

### CI as a cost guardrail

To avoid unnecessary warehouse spend on every change:

- GitHub Actions runs `dbt deps` + `dbt parse` as lightweight validation
- Targeted `dbt test` on key marts instead of full refreshes
flowchart TB

  subgraph ORCH["Airflow Orchestration"]
    DAG["dag_dbt_people_domain"] --> DEPS["dbt deps"] --> RUN["dbt run"] --> TEST["dbt test"]
  end

  subgraph SRC["Sources"]
    HRIS["HRIS"]
    ATS["ATS"]
    PERF["Performance"]
    COMP["Compensation"]
  end

  subgraph STG["Staging"]
    STG_HRIS["stg_hris_employees"]
    STG_ATS["stg_ats_candidates"]
    STG_PERF["stg_perf_reviews"]
    STG_COMP["stg_comp_salaries"]
  end

  subgraph INT["Intermediate"]
    INT_EMP["int_employee_enriched"]
    INT_FUN["int_hiring_funnel_steps"]
  end

  subgraph MART["Marts"]
    DIM_EMP["dim_employee"]
    FCT_FUN["fct_hiring_funnel"]
  end

  HRIS --> STG_HRIS
  ATS --> STG_ATS
  PERF --> STG_PERF
  COMP --> STG_COMP

  STG_HRIS --> INT_EMP --> DIM_EMP
  STG_ATS --> INT_FUN --> FCT_FUN
