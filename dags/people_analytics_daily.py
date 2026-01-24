"""
People Analytics Daily Refresh DAG

Orchestrates dbt runs for the people_analytics domain.
Runs daily at 6 AM UTC.
"""

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago

default_args = {
    'owner': 'data-engineering',
    'depends_on_past': False,
    'email': ['data-team@company.com'],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
}

DBT_DIR = '/opt/airflow/dbt/people_analytics'

with DAG(
    'people_analytics_daily',
    default_args=default_args,
    description='Daily refresh of People Analytics models',
    schedule_interval='0 6 * * *',  # 6 AM UTC daily
    start_date=days_ago(1),
    catchup=False,
    tags=['dbt', 'people_analytics', 'daily'],
) as dag:

    # Task 1: Load new seed data
    dbt_seed = BashOperator(
        task_id='dbt_seed',
        bash_command=f'cd {DBT_DIR} && dbt seed --select people_analytics',
    )

    # Task 2: Run staging models
    dbt_run_staging = BashOperator(
        task_id='dbt_run_staging',
        bash_command=f'cd {DBT_DIR} && dbt run --select people_analytics.staging',
    )

    # Task 3: Run intermediate models
    dbt_run_intermediate = BashOperator(
        task_id='dbt_run_intermediate',
        bash_command=f'cd {DBT_DIR} && dbt run --select people_analytics.intermediate',
    )

    # Task 4: Run marts (incremental)
    dbt_run_marts = BashOperator(
        task_id='dbt_run_marts',
        bash_command=f'cd {DBT_DIR} && dbt run --select people_analytics.marts',
    )

    # Task 5: Run tests
    dbt_test = BashOperator(
        task_id='dbt_test',
        bash_command=f'cd {DBT_DIR} && dbt test --select people_analytics',
    )

    # Task 6: Generate documentation
    dbt_docs = BashOperator(
        task_id='dbt_docs_generate',
        bash_command=f'cd {DBT_DIR} && dbt docs generate',
    )

    # Task 7: Check source freshness
    dbt_source_freshness = BashOperator(
        task_id='dbt_source_freshness',
        bash_command=f'cd {DBT_DIR} && dbt source freshness',
    )

    # Define dependencies
    dbt_source_freshness >> dbt_seed >> dbt_run_staging >> dbt_run_intermediate >> dbt_run_marts
    dbt_run_marts >> dbt_test >> dbt_docs
