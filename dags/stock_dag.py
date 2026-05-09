from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
import sys
sys.path.insert(0, "/opt/airflow")

from scripts.extract import fetch_all_stock
from scripts.load import (
    load_raw,
    load_daily_return,
    load_moving_average,
    load_volatility,
    load_volume_anomaly,
    load_sector_performance,
    load_correlation
)
# ============================================
# TASK FUNCTIONS
# ============================================
def task_extract():
    raw = fetch_all_stock()
    if raw is not None:
        load_raw(raw)
    else:
        raise ValueError("❌ No data fetched")

# ============================================
# DAG DEFINITION
# ============================================

default_args = {
    "owner": "wangushaonv",
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
    "email_on_failure" : True, #失败发邮件（需要配置 SMTP）
    "email": ["wangushaonv@gmail.com"],
}

with DAG(
    dag_id = "techpulse_etl",
    default_args=default_args,
    description="Fetch daily stock prices of the top 50 global tech companies",
    schedule_interval="0 18 * * 1-5", # Run at 18:00, Monday to Friday
    start_date=datetime(2024, 1, 1),
    catchup=False, # Don't backfill past runs
    tags=["stock", "tech", "finance"],
) as dag:
    
    # Task 1: Extract + Load raw
    t1_extract = PythonOperator(
        task_id = "extract_and_load_raw",
        python_callable=task_extract,
    )

    # Task 2: Transform + Load
    t2_daily_return = PythonOperator(
        task_id = "load_daily_return",
        python_callable = load_daily_return,
    )

    t2_moving_average= PythonOperator(
        task_id = "load_moving_average",
        python_callable = load_moving_average,
    )

    t2_volatility = PythonOperator(
        task_id = "load_volatility",
        python_callable = load_volatility,
    )

    t2_volume_anomaly = PythonOperator(
        task_id="load_volume_anomaly",
        python_callable=load_volume_anomaly,
    )

    t2_sector = PythonOperator(
        task_id="load_sector_performance",
        python_callable=load_sector_performance,
    )

    t2_correlation = PythonOperator(
        task_id="load_correlation",
        python_callable=load_correlation,
    )

    # Task dependencies
    _ = t1_extract >> [
        t2_daily_return,
        t2_moving_average,
        t2_volatility,
        t2_volume_anomaly,
        t2_sector,
        t2_correlation,
        ]

    