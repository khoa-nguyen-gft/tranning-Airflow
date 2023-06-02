import apache_beam as beam
from airflow import DAG
from datetime import timedelta



from airflow.utils.dates import days_ago

default_args = {
    'start_date': days_ago(1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'hello_beam_dag',
    default_args=default_args,
    description='A simple Apache Beam DAG',
    schedule_interval=None,
) as dag:

    def print_element(element):
        print(element)

    with beam.Pipeline() as pipeline:
        (
            pipeline
            | 'Create' >> beam.Create(['Hello', 'World'])
            | 'Print' >> beam.Map(print_element)
        )

    # beam_task = DataFlowPythonOperator(
    #     task_id='beam_task',
    #     py_file='hello_beam.py',
    #     gcp_conn_id='google_cloud_default',
    #     dataflow_default_options={
    #         'project': 'your-gcp-project',
    #         'region': 'us-central1',
    #         'temp_location': 'gs://your-bucket/temp',
    #         'staging_location': 'gs://your-bucket/staging',
    #     },
    # )

    # beam_task
