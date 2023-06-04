

```bash
   python3 attendance.py \
   --region us-central1 \
    --input \
    gs://dataflow-apache-read_file_devops-simple/data/dept_data.txt \
    --output \
    gs://dataflow-apache-read_file_devops-simple/output/ \
    --runner DataflowRunner \
    --project devops-simple \
    --temp_location \
    gs://dataflow-apache-read_file_devops-simple/temp/
```

![image](./Screenshot%202023-06-02%20at%2022.07.56.png)


* Execute update apt-get with root user

```bash
    docker exec -it airflow-webserver /bin/bash
    docker exec -u 0 airflow-webserver apt-get update -y
```

* Create file Dockerfile

```bash
    FROM apache/airflow:2.6.1

    USER root

    RUN apt-get update && apt-get install -y libgeos-dev

    USER airflow
```