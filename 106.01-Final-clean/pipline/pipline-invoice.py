import logging
import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions

logging.basicConfig(level="INFO")

BUCKET_NAME = 'gft-demo-gcs-bucket'
DATASET_ID = 'customer_invoice'
PROJECT_ID = 'devops-simple' 
TABLE_ID =  'bs_customer_invoice'
INPUT_FILE = f'gs://{BUCKET_NAME}/input/extract_transform_customer_invoice.csv'
TEMPALTE_NAME = 'customer_invoice_template'
REGION_ID = 'us-central1'


options = {
    'project': PROJECT_ID,
    'runner': 'DataflowRunner',
    'region': REGION_ID,
    'staging_location': f'gs://{BUCKET_NAME}/temp',
    'temp_location': f'gs://{BUCKET_NAME}/temp',
    'template_location': f'gs://{BUCKET_NAME}/template/{TEMPALTE_NAME}' 
}
    
pipeline_options = PipelineOptions.from_dictionary(options)

table_source = f'{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}'
logging.info("table_source: %s", table_source)

schema = """
        customer_id:STRING, 
        full_name:STRING,
        address:STRING
    """  # Specify the schema of the output table

# Transform the data as needed (optional)
# For example, you can split the lines and create dictionaries
def create_row(element):
    fields = element.split(',')
    print("field: ", fields)
    return {
        "customer_id": fields[0],
        "full_name": str(fields[1]) + " "+ str(fields[2]),
        "address": str(fields[3])
    }

# Create the Pipeline
with beam.Pipeline(options=pipeline_options) as p:

    # Read the input file
    records = (p 
              | 'Read From File' >> beam.io.ReadFromText(INPUT_FILE)
              | 'Create Data Rows' >> beam.Map(create_row)
    )

    writeTable = ( records
            | 'WriteToBigQuery' >> beam.io.WriteToBigQuery(
                table=table_source,
                schema=schema,
                create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED,
                write_disposition=beam.io.BigQueryDisposition.WRITE_TRUNCATE
            )
    )