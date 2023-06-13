import sqlite3
import pandas as pd

from airflow.decorators import dag, task
from airflow.utils.dates import days_ago
from airflow.models.variable import Variable
from airflow.operators.dummy import DummyOperator
from airflow.providers.google.cloud.transfers.local_to_gcs import LocalFilesystemToGCSOperator
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator
from airflow.providers.google.cloud.operators.dataflow import DataflowTemplatedJobStartOperator
from datetime import datetime, timedelta

BASE_PATH = Variable.get('BASE_PATH') or "/opt/airflow"
GOOGLE_CLOUD_CONN_ID = Variable.get("GOOGLE_CLOUD_CONN_ID")
BUCKET_NAME = Variable.get('BUCKET_NAME') or "23-06-05-final-test"
DATASET_ID = Variable.get("DATASET_ID") or "devops-simple.customer_invoice"
GOOGLE_OBJECT_NAME = Variable.get("GOOGLE_OBJECT_NAME") or "extract_transform_customer_invoice.csv"
PROJECT_ID = Variable.get("PROJECT_ID")
REGION_ID = Variable.get("REGION_ID")


INPUT_OBJECT_NAME = "invoice.db"
SQL_FILE = "query_invoice.sql"

DATA_PATH = f"{BASE_PATH}/data"
SQL_PATH = f"{BASE_PATH}/sql"
OUT_PATH = f"{BASE_PATH}/data/{GOOGLE_OBJECT_NAME}"
GOOGLE_OUT_PATH = f"data/{GOOGLE_OBJECT_NAME}"

BIGQUERY_TABLE_NAME = "bs_customer_invoice"

@dag(
    default_args={
        'owner': 'okza',
        'email': 'datokza@gmail.com',
        'email_on_failure': True
    },
    schedule_interval='0 4 * * *',
    start_date=days_ago(1),
    tags=['sqlite', 'customer']
)
def bs_customer_invoice_dag():

    start = DummyOperator(task_id='start')
    end = DummyOperator(task_id='end')

    @task()
    def extract_transform():
        print("extract transform")
        conn = sqlite3.connect(f"{DATA_PATH}/{INPUT_OBJECT_NAME}")
        with open(f"{SQL_PATH}/{SQL_FILE}") as query:
            df = pd.read_sql(query.read(), conn)
        df.to_csv(OUT_PATH, index=False, header=False)

    extract_transform_data = extract_transform()
    now = datetime.now()

    store_data_gcs = LocalFilesystemToGCSOperator(
        task_id='store_data_gcs',
        gcp_conn_id=GOOGLE_CLOUD_CONN_ID,
        src=OUT_PATH,
        dst=GOOGLE_OUT_PATH,
        bucket=BUCKET_NAME
    )
    
    start_pipline_invoice_template = DataflowTemplatedJobStartOperator(
        task_id='start_template_job',
        template=f'gs://{BUCKET_NAME}/template/customer_invoice_template',
        location=REGION_ID,
        project_id= PROJECT_ID,
        job_name='my-dataflow-job',  # Specify the desired job name here
        gcp_conn_id=GOOGLE_CLOUD_CONN_ID,
        wait_until_finished=True
    )

    start >> extract_transform_data >> store_data_gcs >>start_pipline_invoice_template >> end


bs_customer_invoice_dag_etl = bs_customer_invoice_dag()
