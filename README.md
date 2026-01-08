
# Analytics Domain Ownership (dbt + BigQuery + Airflow)

Domain ownership portfolio demonstrating **analytics engineering patterns** across **People Analytics** and **Payments** domains: dbt modeling, BigQuery cost-aware materialization, Airflow orchestration, tests/contracts, and lineage documentation.

---

## What this project demonstrates

- **Domain ownership**: each domain lives under `domains/<domain>/` with a consistent, maintainable structure.
- **Warehouse modeling discipline**: `staging → intermediate → marts (dim/fct)` with intentional materialization choices.
- **Cost-aware BigQuery patterns**: avoid `SELECT *`, reuse intermediates for expensive joins, and plan for partitioning/clustering on large facts.
- **Operational workflows**: Airflow DAGs orchestrate dbt runs; repo is cleaned to avoid committing generated artifacts (venv/logs/target).
- **Data quality + governance**: dbt tests and schema definitions support reliable downstream consumption.
- **Documentation + lineage**: dbt docs/lineage used for model discovery and impact analysis.

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
      dbt_project.yml_


## Proof ✅

> Screenshots live in `docs/screenshots/`. Add/replace images there, then update filenames below if needed.

### Airflow orchestration (UI)
- **DAGs listed / loaded**
  - ![Airflow DAGs list](docs/screenshots/02_airflow_dags_list.png)
- **Successful DAG run**
  - ![Airflow run success](docs/screenshots/03_airflow_run_success.png)

### dbt execution
- **dbt execution proof**
  - ![dbt execution proof](docs/screenshots/04_dbt_run_graph.png)

### BigQuery deployment
- **Dataset models (tables/views)**
  - ![BigQuery dataset models](docs/screenshots/05_bigquery_dataset_models.png)

### Lineage & documentation (optional)
- **dbt docs lineage**
  - ![dbt docs lineage](docs/screenshots/06_dbt_docs_lineage.png)

## Quickstart (local)
```bash
# from repo root
cd domains/<domain>   # e.g., domains/people_analytics or domains/payments

python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

dbt deps
dbt debug
dbt run
dbt test

# Start Airflow → trigger the DAG from the UI


### Airflow orchestration (UI)
**DAGs listed / loaded**  
![Airflow DAGs list](docs/screenshots/02_airflow_dags_list.png)

**Successful DAG run**  
![Airflow run success](docs/screenshots/03_airflow_run_success.png)

### dbt execution
**dbt execution proof**  
![dbt execution proof](docs/screenshots/04_dbt_run_graph.png)

### BigQuery deployment
**Dataset models (tables/views)**  
![BigQuery dataset models](docs/screenshots/05_bigquery_dataset_models.png)

### Lineage & documentation (optional)
**dbt docs lineage**  
![dbt docs lineage](docs/screenshots/06_dbt_docs_lineage.png)

### Data contracts & tests (dbt)
- dbt tests passing (People Analytics)
  - ![dbt test people analytics](docs/screenshots/08_dbt_test_people_analytics.png)
- dbt tests passing (Payments)
  - ![dbt test payments](docs/screenshots/09_dbt_test_payments.png)




