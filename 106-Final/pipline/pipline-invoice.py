import logging
import argparse
import sys
from typing import Sequence
import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions

logging.basicConfig(level="INFO")

def run(args: Sequence):
    parser = argparse.ArgumentParser()
    
    parser.add_argument("--bucket_name",
                        required=True,
                        help='The name of the bucket ex:23-06-05-final-test')
    parser.add_argument("--dataset_id",
                        required=True,
                        help='The data set id ex: customer_invoice')
    parser.add_argument("--project_id",
                        required=True,
                        help='the project id ex: devops-simple')
    parser.add_argument("--table_id",
                        required=True,
                        help='The Table id ex: bs_customer_invoice')
    parser.add_argument("--country_codes", nargs="+", 
                        required=True, 
                        help='The list of country codesex: [India, USA]')
    
    parsed_args = parser.parse_known_args(args)[0]

    logging.info("List of args is: %s", parsed_args)

    BUCKET_NAME = parsed_args.bucket_name
    DATASET_ID = parsed_args.dataset_id
    PROJECT_ID = parsed_args.project_id 
    TABLE_ID =  parsed_args.table_id
    COUNTRY_CODES = parsed_args.country_codes

    # Set up the PipelineOptions with your desired options
    options = PipelineOptions(
        runner="DirectRunner",
        project=PROJECT_ID,  # Replace with your actual project ID
        temp_location=f"gs://{BUCKET_NAME}/tmp",
        region="us-central1"
    )

    for country_code in COUNTRY_CODES:
        COUNTRY_CODE = country_code
        TARGET_TABLE = f"{TABLE_ID}_{COUNTRY_CODE}".upper()

        # Create the Pipeline
        with beam.Pipeline(options=options) as p:
            # Read data from BigQuery
            query = f"""
                SELECT customer_id, 
                    full_name,
                    company,
                    billing_country,
                    total,
                FROM [{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}] 
                where UPPER(billing_country)  = UPPER('{COUNTRY_CODE}')
                """
            
            data = p | "Read from BigQuery" >> beam.io.ReadFromBigQuery(query=query)

            output_table = f"{PROJECT_ID}.{DATASET_ID}.{TARGET_TABLE}"

            schema = """
                    customer_id:INT64, 
                    full_name:STRING, 
                    company:STRING,
                    billing_country:STRING,
                    total:FLOAT64
                    """  # Specify the schema of the output table

            data | "Write to BigQuery" >> beam.io.WriteToBigQuery(
                output_table,
                schema=schema,
                create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED,
                write_disposition=beam.io.BigQueryDisposition.WRITE_TRUNCATE
            )

if __name__ == "__main__":
    run(sys.argv[1:])