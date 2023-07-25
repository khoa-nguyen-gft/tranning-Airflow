from configparser import ConfigParser
from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
from airflow.providers.google.cloud.transfers.local_to_gcs import (
    LocalFilesystemToGCSOperator,
)
from airflow.providers.google.cloud.operators.dataflow import (
    DataflowTemplatedJobStartOperator,
    DataflowStartFlexTemplateOperator,
)
from airflow.providers.google.cloud.hooks.gcs import GCSHook
from airflow.models import Variable
from airflow.utils.dates import days_ago
from apache_beam.io.gcp.bigquery_tools import parse_table_schema_from_json
from airflow.operators.bash import BashOperator
import pandas as pd
import os
import sys
from datetime import datetime

sys.path.insert(0, "/opt/airflow/template")
sys.path.insert(0, "/opt/airflow/utils")
import run_flight_schema
import encryption_util

DATASET_ID = Variable.get("DATASET_ID")  # "my-project-95615-388109.my_first_bigquery"
BASE_PATH = Variable.get("BASE_PATH")
BUCKET_NAME = Variable.get("BUCKET_NAME")
GOOGLE_CLOUD_CONN_ID = Variable.get("GOOGLE_CLOUD_CONN_ID")
BIGQUERY_TABLE_NAME = "flights_sample"
EXTRACT_FILE_NAME = "extract_flights_sample.csv"
EXTRACT_FILE_PATH = f"{BASE_PATH}/gcs_data/{EXTRACT_FILE_NAME}"
GCS_ENCRYPT_FILE_NAME = "encrypt_flights_sample.csv"
DATA_PATH = f"{BASE_PATH}/data/flights_sample.csv"  # "/opt/airflow/data"
GCS_ENCRYPT_FILE_PATH = f"{BASE_PATH}/gcs_data/{GCS_ENCRYPT_FILE_NAME}"
TABLE_ID = f"{DATASET_ID}.{BIGQUERY_TABLE_NAME}"
ASSOCIATED_DATA = b"associated_data"
KEYSET_PATH = "/opt/airflow/config/keyset.json"
schedule_interval = "0 0 * * *"  # every 4AM

GCP_PROJECT = "my-project-95615-388109"
DATASET = "my_first_bigquery"
TABLE = "flights_sample"
GCP_REGION = "asia-southeast1"
GCP_US_REGION = "us-central1"
TEMPLATE_NAME = "beam-flex-demo"
TEMPLATE_TAG = "0.1.0"
PROJECT_NUMBER = "647791208514"
GCS_PATH = f"gs://{GCP_PROJECT}-dataflow-{PROJECT_NUMBER}"
TEMPLATE_PATH = f"{GCS_PATH}/templates/{TEMPLATE_NAME}"
TEMPLATE_IMAGE = f"{GCP_REGION}-docker.pkg.dev/{GCP_PROJECT}/{TEMPLATE_NAME}/{TEMPLATE_NAME}:{TEMPLATE_TAG}"
JOB_NAME = f"beam-flex-demo-{datetime.now().strftime('%Y%m%d%H%M%S')}"


def get_env_file():
    # Get the path to the application.properties file
    current_dir = os.getcwd()
    env_file = os.path.join(current_dir, "config", "application.properties")
    config = ConfigParser()
    config.read(env_file)
    return config


def read_schema_file(config):
    output_schema_path = config.get("schema", "output_schema")
    # Read the schema from the file
    with open(output_schema_path, "r") as schema_file:
        schema_str = schema_file.read()
    try:
        return parse_table_schema_from_json(schema_str)
    except Exception as e:
        print("Error parsing table schema:", e)
        raise


def get_google_cloud_kms_key(config):
    return config.get("kms_secret", "kms_key")


def get_google_service_account_json(config):
    return config.get("service_account", "service_account_json")


def extract_transform():
    df = pd.read_csv(f"{DATA_PATH}")
    columns = ["Code", "Number", "Distance"]
    for column in columns:
        print(f"column: {column}   -df[column]: {df[column]}")
        df[column] = pd.to_numeric(df[column], errors="coerce").fillna(0)

    df.to_csv(EXTRACT_FILE_PATH, index=False, header=False)


def encrypt_file():
    encryption_util.encrypt_data(
        EXTRACT_FILE_PATH, GCS_ENCRYPT_FILE_PATH, ASSOCIATED_DATA, KEYSET_PATH
    )
    # Upload the encrypted file to GCS
    print("encrypt_file OK")
    gcs_hook = GCSHook(gcp_conn_id=GOOGLE_CLOUD_CONN_ID)
    gcs_hook.upload(
        bucket_name=BUCKET_NAME,
        object_name=GCS_ENCRYPT_FILE_NAME,
        filename=GCS_ENCRYPT_FILE_PATH,
    )


with DAG(
    "gcs_beam_bigquery_pipeline_dag",
    schedule_interval=schedule_interval,
    start_date=days_ago(1),
) as dag:
    start = EmptyOperator(task_id="start")
    end = EmptyOperator(task_id="end")
    config_env = get_env_file()

    extract_transform_task = PythonOperator(
        task_id="extract_transform", python_callable=extract_transform
    )

    stored_data_gcs = PythonOperator(
        task_id="store_to_gcs",
        python_callable=encrypt_file,
        op_kwargs={},
        provide_context=True,
    )

    TABLE_SCHEMA = read_schema_file(config_env)
    google_cloud_kms_key = get_google_cloud_kms_key(config_env)
    google_service_account_json = get_google_service_account_json(config_env)

    start_template_job = DataflowStartFlexTemplateOperator(
        task_id="start_template_job",
        location="us-central1",  # Specify the desired location
        body={
            "launchParameter": {
                "jobName": f"beam-flex-demo-{datetime.now().strftime('%Y%m%d%H%M%S')}",
                "parameters": {
                    "output_table": "my-project-95615-388109:my_first_bigquery.flights_sample"
                },
                "containerSpecGcsPath": "gs://my-project-95615-388109-dataflow-647791208514/templates/0.1.0/beam-flex-demo.json",
                "environment": {
                    "numWorkers": 10,
                    "maxWorkers": 20,
                    "diskSizeGb": 1024,
                    "machineType": "n2-highmem-8",
                },
            }
        },
        project_id="my-project-95615-388109",
        gcp_conn_id=GOOGLE_CLOUD_CONN_ID,
        impersonation_chain=None,  # Set to the desired impersonation chain if needed
        wait_until_finished=True,  # Set to the desired value
    )

    start >> extract_transform_task
    extract_transform_task >> stored_data_gcs
    stored_data_gcs >> start_template_job
    start_template_job >> end

gcs_beam_bigquery_pipeline = dag
