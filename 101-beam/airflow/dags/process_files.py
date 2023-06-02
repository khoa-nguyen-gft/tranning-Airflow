from datetime import datetime
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
import apache_beam as beam

# Define a Python function to process the input files using Apache Beam
def process_files():
    # Define the Apache Beam pipeline
    with beam.Pipeline() as pipeline:
        # Read input files
        input_files = ['file1.txt', 'file2.txt']
        lines = pipeline | beam.io.ReadFromText(input_files)

        # Apply transformations
        transformed_lines = lines | beam.Map(lambda line: line.upper())

        # Write output
        transformed_lines | beam.io.WriteToText('output.txt')

# Define the Airflow DAG
dag = DAG(
    'beam_pipeline',
    description='Apache Beam Pipeline in Airflow',
    schedule_interval=None,
    start_date=datetime(2023, 6, 1)
)

# Define a task that calls the process_files function
process_task = PythonOperator(
    task_id='process_task',
    python_callable=process_files,
    dag=dag
)

# Set task dependencies
process_task
