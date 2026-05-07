from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator

import sys
sys.path.insert(0, "/opt/airflow/scripts")


# DAG default params
default_args = {
    "owner": "wangushaonv",
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
    "email_on_failure" : True, #失败发邮件（需要配置 SMTP）
    "email": ["wangushaonv@gmail.com"],
}

# DAG definition
with DAG(
    dag_id = "stock_price",
    default_args=default_args,
    description="Fetch the daily stock prices of the top 50 global tech companies",
    schedule_interval="0 18 * * 1-5", # Run at 18:00, Monday to Friday
    start_date=datetime(2024, 1, 1),
    catchup=False, # Don't backfill past runs
    tags=["stock", "tech", "finance"],
) as dag:

    fetch_task = PythonOperator(
        task_id = "fetch_all_tech_stocks",
        python_callable=fetch_all_stocks,
    )
    