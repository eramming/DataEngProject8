from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    "owner": "rohan",
    "depends_on_past": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="mls_ingest_pipeline",
    default_args=default_args,
    description="Weekly ingestion pipeline for the full MLS project",
    schedule="@weekly",
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=["mls", "data-engineering"],
) as dag:

    run_ingest_pipeline = BashOperator(
        task_id="run_ingest_pipeline",
        bash_command="cd /opt/sportsapp && python3 ingest/ingest_pipeline.py",
    )

    run_ingest_pipeline