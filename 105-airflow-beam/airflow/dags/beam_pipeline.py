import os
from datetime import datetime
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.dummy import DummyOperator


# Define the DAG
dag = DAG(
    'beam_pipeline',
    description='Simple Apache Beam pipeline example',
    start_date=datetime(2023, 6, 1),
    schedule_interval='@daily',
)

# Task 1: Data Ingestion
ingestion_task = BashOperator(
    task_id='data_ingestion',
    bash_command='python /opt/airflow/pipeline/001-department-pipline.py',
    dag=dag,
)

start = DummyOperator(task_id='start')
end = DummyOperator(task_id='end')

start >> ingestion_task >> end

