
# Create Google Cloud Template And Execute The Template

To implement the Google Cloud Dataflow training, follow the steps below:

## Step 1: Set up environment variables

```bash
export PROJECT_ID="devops-simple"
export BUCKET_NAME="gft-demo-gcs-bucket"
export REGION="us-central1"
```

## Step 2: Copy the department data file to a Google Cloud Storage bucket


```bash
gsutil cp department-data.txt gs://${BUCKET_NAME}/input/department-data.txt 
```

## Step 3: Create a template for the attendance job

```bash
python3 attendance.py \
    --runner DataflowRunner \
    --region ${REGION} \
    --job_name my-attendance-job \
    --project ${PROJECT_ID} \
    --input gs://${BUCKET_NAME}/input/department-data.txt \
    --output gs://${BUCKET_NAME}/output/ \
    --temp_location gs://${BUCKET_NAME}/temp \
    --template_location gs://${BUCKET_NAME}/template/customer_invoice_template_v2
```

![Alt text](images/Step%203%3A%20Create%20a%20template%20for%20the%20attendance%20job.png)

## Step 4: Execute the template for the attendance job


```bash
gcloud dataflow jobs run my-attendance-job  \
    --region ${REGION} \
    --gcs-location gs://${BUCKET_NAME}/template/customer_invoice_template_v2 \
    --project ${PROJECT_ID}
```

![Alt text](images/Step%204%3A%20Execute%20the%20template%20for%20the%20attendance%20job.png)

- Make sure to replace the values of PROJECT_ID, BUCKET_NAME, and REGION with your specific values. Also, ensure that you have the necessary permissions and configurations in your Google Cloud environment to perform these actions.

- The provided code defines a Dataflow pipeline that reads data from an input file, performs transformations and filtering operations, and writes the results to an output file. The pipeline counts the number of employees in the "Accounts" department and writes the count to the output file.

```csv
('Kyle', 62)
('Rebekah', 31)
('Gaston', 31)
('Itoe', 31)
('Kumiko', 31)
('Marco', 31)
('Edouard', 31)
('Ayumi', 30)
```