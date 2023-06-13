
# Run Test In Local Machine: 

* Example: to call the code

    ```bash
    python3 pipline-invoice.py \
        --bucket_name=23-06-05-final-test \
        --dataset_id=customer_invoice \
        --project_id=devops-simple \
        --table_id=bs_customer_invoice \
        --country_codes Canada India USA \
        --input=gs://23-06-05-final-test/extract_transform_customer_invoice.csv
    ```

    ```bash
    gcloud config set project devops-simple
    ```

# Register the delivery pipeline and targets

    ```bash
    python3 pipline-invoice.py \
        --job_name pipline-invoice-job \
        --region us-central1 \
        --runner DataflowRunner \
        --project devops-simple \
        --temp_location \
          gs://23-06-05-final-test/temp/ \
        --template_location \
          gs://23-06-05-final-test/template/pipline-invoice-template \
        --bucket_name=23-06-05-final-test \
        --dataset_id=customer_invoice \
        --project_id=devops-simple \
        --table_id=bs_customer_invoice \
        --country_codes Canada India USA \
        --input=gs://23-06-05-final-test/extract_transform_customer_invoice.csv
    ```

    ```bash
    python3 pipline-move-file.py \
        --job_name pipline-invoice-job \
        --region us-central1 \
        --runner DataflowRunner \
        --project devops-simple \
        --temp_location \
          gs://23-06-05-final-test/temp/ \
        --template_location \
          gs://23-06-05-final-test/template/pipline-invoice-template \
        --bucket_name=23-06-05-final-test \
        --dataset_id=customer_invoice \
        --project_id=devops-simple \
        --table_id=bs_customer_invoice \
        --country_codes Canada India USA \
        --input=gs://23-06-05-final-test/extract_transform_customer_invoice.csv
    ```



