

```bash
   python3 attendance.py \
   --region us-central1 \
    --input \
    gs://dataflow-apache-read_file_devops-simple/data/dept_data.txt \
    --output \
    gs://dataflow-apache-read_file_devops-simple/output/ \
    --runner DataflowRunner \
    --project devops-simple \
    --job_name my-attendance-job \
    --temp_location \
    gs://dataflow-apache-read_file_devops-simple/temp/
```


```bash
   python3 attendance.py \
   --region us-central1 \
    --input \
    gs://23-06-05-final-test/extract_transform_customer_invoice.csv  \
    --output \
    gs://dataflow-apache-read_file_devops-simple/output/ \
    --runner DataflowRunner \
    --project devops-simple \
    --job_name my-attendance-job \
    --temp_location \
    gs://dataflow-apache-read_file_devops-simple/temp/
```


![image](./Screenshot%202023-06-02%20at%2022.07.56.png)