import datetime
import logging
import os
import tempfile
from os import path
import pandas as pd
from airflow.models import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.google.cloud.hooks.gcs import GCSHook
from airflow.operators.dummy import DummyOperator


dag = DAG(
    "gcp_movie_ranking",
    start_date=datetime.datetime(year=2023, month=5, day=31),
    end_date=datetime.datetime(year=2023, month=3, day=31),
    schedule_interval="@daily"
)

def _fetch_ratings(api_conn_id, gcp_conn_id, gcs_bucket, **context):
    year = context["execution_date"].year
    month = context["execution_date"].month

    logging.info(f"Fetching ratings for {year}/{month:02d}")

    gcs_hook = GCSHook(gcp_conn_id)
    gcs_hook.upload(
        bucket_name=gcs_bucket,
        object_name=f"your-file.csv",
        filename="data.csv",
    )

fetch_ratings = PythonOperator(
    task_id="fetch_ratings",
    python_callable=_fetch_ratings,
    op_kwargs={
        "api_conn_id": "movielens",
        "gcp_conn_id": "my_google_cloud_default",
        "gcs_bucket": "bucket",
    },
    dag=dag,
)

import_in_bigquery = DummyOperator(task_id = "fetch_wather_dorecast", dag = dag)


fetch_ratings >> import_in_bigquery