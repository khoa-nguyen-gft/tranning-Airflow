# Lab: BS Customer Invoice Chinook ETL

## Introduction

This lab demonstrates an Extract-Transform-Load (ETL) process using Airflow. The ETL process involves extracting data from a SQLite database, transforming it, and loading it into Google BigQuery. 

## Prerequisites

Before starting this lab, make sure you have the following:

1. Airflow installed and configured.
2. Access to a Google Cloud Platform (GCP) project.
3. SQLite database file named `chinook.db`.
4. Required variables configured in Airflow:
   - `DATASET_ID`: BigQuery dataset ID.
   - `BASE_PATH`: Base path for the lab project.
   - `BUCKET_NAME`: GCS bucket name for storing the extracted data.
   - `GOOGLE_CLOUD_CONN_ID`: Google Cloud connection ID for Airflow.

## Steps

### Step 1: Set up the Airflow DAG

1. Open the Airflow web UI.
2. Create a new DAG named `bs_customer_invoice_chinook_dag`.
3. Set the following DAG properties:
   - Owner: `okza`
   - Email: `datokza@gmail.com`
   - Email on Failure: `True`
   - Schedule Interval: `0 4 * * *` (to run every day at 4 AM)
   - Start Date: Select the appropriate start date for your lab
   - Tags: `sqlite`, `blank-space`, `music`

### Step 2: Define the `extract_transform` task

1. Define a Python function named `extract_transform`.
2. Inside the function, establish a connection to the SQLite database `chinook.db`.
3. Read the SQL query from the file `chinook.sql`.
4. Execute the query and retrieve the data as a Pandas DataFrame.
5. Save the DataFrame as a CSV file named `extract_transform_customer_invoice_chinook.csv` in the `data` directory.

### Step 3: Define the tasks for storing and loading the data

1. Define a task named `store_to_gcs` to store the extracted data in Google Cloud Storage (GCS).
   - Use the `LocalFilesystemToGCSOperator` to transfer the CSV file to GCS.
   - Set the source file path to the CSV file created in the previous step.
   - Set the destination file name to `extract_transform_customer_invoice_chinook.csv`.
   - Set the GCS bucket name using the `BUCKET_NAME` variable.

2. Define a task named `load_to_bigquery` to load the data from GCS to BigQuery.
   - Use the `GCSToBigQueryOperator` to load the data from GCS to BigQuery.
   - Set the GCS bucket name using the `BUCKET_NAME` variable.
   - Set the source object as `extract_transform_customer_invoice_chinook.csv`.
   - Set the destination project dataset table using the `DATASET_ID` and `BIGQUERY_TABLE_NAME` variables.
   - Define the schema fields for the destination table.

### Step 4: Define the DAG structure

1. Define the start and end tasks as `DummyOperator`.
2. Set the dependencies between the tasks as follows:
   - `start` >> `extract_transform` >> `store_to_gcs` >> `load_to_bigquery` >> `end`

### Step 5: Save and Trigger the DAG

1. Save the DAG configuration.
2. Trigger the DAG manually or wait for the scheduled time to start the ETL process.

## Conclusion

In this lab, you learned how to create an Airflow DAG for the BS Customer
