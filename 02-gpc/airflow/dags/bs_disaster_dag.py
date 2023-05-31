from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
from airflow.providers.google.cloud.transfers.local_to_gcs import LocalFilesystemToGCSOperator
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator
from airflow.models import Variable
from airflow.utils.dates import days_ago
import pandas as pd

from airflow.providers.google.cloud.operators.bigquery import (
    BigQueryCreateEmptyDatasetOperator,
    BigQueryCreateExternalTableOperator,
    BigQueryDeleteDatasetOperator,
)

# DATASET_ID = Variable.get("DATASET_ID")
DATASET_ID = "my-project-95615-388109.my_first_bigquery"
# BASE_PATH = Variable.get("BASE_PATH")
BUCKET_NAME = Variable.get("BUCKET_NAME")
GOOGLE_CLOUD_CONN_ID = Variable.get("GOOGLE_CLOUD_CONN_ID")
BIGQUERY_TABLE_NAME = "bs_disaster"
GCS_OBJECT_NAME = "extract_disaster_data.csv"
# DATA_PATH = f"{BASE_PATH}/data"
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

    # loaded_data_bigquery = BigQueryCreateExternalTableOperator(
    #     task_id='load_to_bigquery',
    #     gcp_conn_id=GOOGLE_CLOUD_CONN_ID,
    #     bucket=BUCKET_NAME,
    #     source_objects=[GCS_OBJECT_NAME],
    #     destination_project_dataset_table=f"{DATASET_ID}.{BIGQUERY_TABLE_NAME}",
    #     schema_fields=[  # based on https://cloud.google.com/bigquery/docs/schemas
    #         {'name': 'id', 'type': 'INT64', 'mode': 'REQUIRED'},
    #         {'name': 'keyword', 'type': 'STRING', 'mode': 'NULLABLE'},
    #         {'name': 'location', 'type': 'STRING', 'mode': 'NULLABLE'},
    #         {'name': 'text', 'type': 'STRING', 'mode': 'NULLABLE'},
    #         {'name': 'target', 'type': 'INT64', 'mode': 'NULLABLE'},
    #     ]
    # )
    # loaded_data_bigquery = BigQueryCreateExternalTableOperator(
    #     task_id='load_to_bigquery',
    #     gcp_conn_id=GOOGLE_CLOUD_CONN_ID,
    #     bucket=BUCKET_NAME,
    #     source_objects=[GCS_OBJECT_NAME],
    #     destination_project_dataset_table='my-project-95615-388109.my_first_bigquery.my_table',
    #     schema_fields=[
    #         {'name': 'text', 'type': 'INT64', 'mode': 'NULLABLE'},
    #         {'name': 'keyword', 'type': 'STRING', 'mode': 'NULLABLE'},
    #     ]
    # )

    # loaded_data_bigquery = GCSToBigQueryOperator(
    #         task_id='load_to_bigquery',
    #         gcp_conn_id=GOOGLE_CLOUD_CONN_ID,
    #         bucket=BUCKET_NAME,
    #         source_objects=[GCS_OBJECT_NAME],
    #         destination_project_dataset_table=f"{DATASET_ID}.{BIGQUERY_TABLE_NAME}",
    #         schema_fields=[  #based on https://cloud.google.com/bigquery/docs/schemas
    #             {'name': 'id', 'type': 'INT64', 'mode': 'REQUIRED'},
    #             {'name': 'keyword', 'type': 'STRING', 'mode': 'NULLABLE'},
    #             {'name': 'location', 'type': 'STRING', 'mode': 'NULLABLE'},
    #             {'name': 'text', 'type': 'STRING', 'mode': 'NULLABLE'},
    #             {'name': 'target', 'type': 'INT64', 'mode': 'NULLABLE'},
    #         ],
    #         autodetect=False,
    #         write_disposition='WRITE_TRUNCATE', #If the table already exists - overwrites the table data
    # )

    start >> extract_transform_task
    extract_transform_task >> stored_data_gcs
    # stored_data_gcs >> loaded_data_bigquery
    # loaded_data_bigquery >> end

bs_disaster_elt = dag
