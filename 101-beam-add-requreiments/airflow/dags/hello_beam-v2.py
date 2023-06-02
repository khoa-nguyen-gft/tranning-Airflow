from datetime import datetime
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from apache_beam.options.pipeline_options import PipelineOptions
import apache_beam as beam

def run_beam_pipeline():
    # Define your Apache Beam pipeline logic here
    with beam.Pipeline(options=PipelineOptions()) as p:
        (p
         | 'Create' >> beam.Create(['Hello', 'Beam'])
         | 'Concatenate' >> beam.CombineGlobally(lambda elements: ' '.join(elements))
         | 'Print' >> beam.Map(print))

dag = DAG(
    'hello_beam',
    description='Example DAG for running a simple Beam pipeline in Airflow',
    schedule_interval=None,
    start_date=datetime(2023, 6, 2),
    catchup=False,
)

run_beam_task = PythonOperator(
    task_id='run_beam_pipeline',
    python_callable=run_beam_pipeline,
    dag=dag,
)
