""" DAG demonstration the hello use case"""
from airflow import DAG
from airflow.utils import dates
from airflow.operators.dummy import DummyOperator

dag = DAG(
    dag_id = "01-hello",
    start_date= dates.days_ago(5),
    schedule_interval="@daily"
)

fetch_wather_dorecast = DummyOperator(task_id = "fetch_wather_dorecast", dag = dag)
clean_forecast_data = DummyOperator(task_id = "clean_forecast_data", dag = dag)

fetch_sales_data = DummyOperator(task_id = "fetch_sales_data", dag = dag)
clear_sales_data = DummyOperator(task_id = "clear_sales_date", dag = dag)

join_datasets = DummyOperator(task_id = "join_datasets", dag = dag)

train_ml_model = DummyOperator(task_id = "train_ml_model", dag = dag)
deploy_ml_model = DummyOperator(task_id = "deploy_ml_model", dag = dag)


# Set dependencies between all tasks
fetch_wather_dorecast >> clean_forecast_data
fetch_sales_data >> clear_sales_data
[clean_forecast_data, clear_sales_data] >> join_datasets
join_datasets >> train_ml_model >> deploy_ml_model

