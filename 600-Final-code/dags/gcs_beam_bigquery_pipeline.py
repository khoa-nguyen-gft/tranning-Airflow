from airflow import DAG
from airflow.providers.google.cloud.operators.dataflow import (
    DataflowStartFlexTemplateOperator,
)
from airflow.providers.google.cloud.operators.bigquery import BigQueryInsertJobOperator
from airflow.models import Variable
from airflow.utils.dates import days_ago
from datetime import datetime
from utils.status_queries import (
    PROCESS_JOB_START_STATUS_QUERY,
    PROCESS_JOB_FAILURE_STATUS_QUERY,
    PROCESS_JOB_SUCCESS_STATUS_QUERY,
)
from airflow.utils.trigger_rule import TriggerRule

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
schedule_interval = "0 0 * * *"  # every 4AM
LOCATION = "asia-southeast1"

with DAG(
    "gcs_beam_bigquery_pipeline_dag",
    schedule_interval=schedule_interval,
    start_date=days_ago(1),
) as dag:
    start_job_status = BigQueryInsertJobOperator(
        task_id="start_job_status",
        gcp_conn_id=GOOGLE_CLOUD_CONN_ID,
        configuration={
            "query": {
                "query": PROCESS_JOB_START_STATUS_QUERY.format(
                    process_date=datetime.now().strftime("%Y%m%d:%H%M%S"),
                    context="flights_sample",
                    run_id="bigdata_pipeline_flights_sample",
                    process_name="bigdata_pipeline",
                ),
                "useLegacySql": False,
            }
        },
    )

    insert_dataflow_pipeline_succeed = BigQueryInsertJobOperator(
        task_id="insert_dataflow_pipeline_succeed",
        gcp_conn_id=GOOGLE_CLOUD_CONN_ID,
        configuration={
            "query": {
                "query": PROCESS_JOB_SUCCESS_STATUS_QUERY.format(
                    process_date=datetime.now().strftime("%Y%m%d"),
                    context="flights_sample",
                    run_id="bigdata_pipeline_flights_sample",
                    process_name="bigdata_pipeline",
                ),
                "useLegacySql": False,
            }
        },
    )

    insert_dataflow_pipeline_failed = BigQueryInsertJobOperator(
        task_id="insert_dataflow_pipeline_failed",
        gcp_conn_id=GOOGLE_CLOUD_CONN_ID,
        configuration={
            "query": {
                "query": PROCESS_JOB_FAILURE_STATUS_QUERY.format(
                    process_date=datetime.now().strftime("%Y%m%d"),
                    context="flights_sample",
                    run_id="bigdata_pipeline_flights_sample",
                    process_name="bigdata_pipeline",
                ),
                "useLegacySql": False,
            }
        },
        trigger_rule=TriggerRule.ONE_FAILED,
    )

    start_flex_template = DataflowStartFlexTemplateOperator(
        task_id="start_flex_template",
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

    (
        start_job_status
        >> start_flex_template
        >> [insert_dataflow_pipeline_succeed, insert_dataflow_pipeline_failed]
    )


gcs_beam_bigquery_pipeline = dag
