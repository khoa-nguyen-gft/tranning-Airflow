from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
from airflow.providers.google.cloud.transfers.local_to_gcs import LocalFilesystemToGCSOperator
from airflow.models import Variable
from airflow.utils.dates import days_ago
import pandas as pd

DATASET_ID = "my-project-95615-388109.my_first_bigquery"
BUCKET_NAME = Variable.get("BUCKET_NAME")
GOOGLE_CLOUD_CONN_ID = Variable.get("GOOGLE_CLOUD_CONN_ID")
BIGQUERY_TABLE_NAME = "bs_disaster"
GCS_OBJECT_NAME = "extract_disaster_data.csv"
DATA_PATH = "/opt/airflow/data"
OUT_PATH = f"{DATA_PATH}/{GCS_OBJECT_NAME}"


def extract_transform():
    df = pd.read_csv(f"{DATA_PATH}/disaster_data.csv")
    columns = ['text', 'location']
    for column in columns:
        df[column] = df[column].str.replace(r'\s{2,}', ' ', regex=True)
        df[column] = df[column].str.replace(r"[^a-zA-Z0-9\,]", ' ', regex=True)

    df.to_csv(OUT_PATH, index=False, header=False)


schedule_interval = '0 4 * * *'  # every 4AM

with DAG(
    'bs_disaster_dag',
    schedule_interval=schedule_interval,
    start_date=days_ago(1),
    tags=['csv', 'tweet', 'disaster', 'blank-space']
) as dag:
    start = EmptyOperator(task_id='start')
    end = EmptyOperator(task_id='end')

    extract_transform_task = PythonOperator(
        task_id='extract_transform',
        python_callable=extract_transform
    )

    stored_data_gcs = LocalFilesystemToGCSOperator(
        task_id="store_to_gcs",
        gcp_conn_id=GOOGLE_CLOUD_CONN_ID,
        src=OUT_PATH,
        dst=GCS_OBJECT_NAME,
        bucket=BUCKET_NAME
    )

    start >> extract_transform_task >> stored_data_gcs

bs_disaster_elt = dag
