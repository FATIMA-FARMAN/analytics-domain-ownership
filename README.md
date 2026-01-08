
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
