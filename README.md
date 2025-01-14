# Learning Path: Technical ETL, Airflow, Apache Beam,Tink, Kafka in Banking Domain

![image](./images/Screenshot%202023-06-07%20at%2008.58.26%20copy.png)


## Setup:
[Developer Starter](./00-install/) contains everything needed in order to get started Data.


## Airflow:

- Airflow is commonly used as a platform for orchestrating and managing data workflows. It provides a way to define, schedule, and monitor complex workflows consisting of tasks that need to be executed in a specific order or on a specific schedule.


![Alt text](images/Airflow.png)

- [Why and when should I consider Airflow](./00-when/)
- [[Lab] First step with Airflow](./01-hello-airflow/)
- [Basic concepts of Airflow(DAGs, Tasks, Operators, Task dependencies)](./00-concepts/)
- [[Lab] Airflow pipelines upload data Google Cloud Storage](./02-gpc/)
- [[Lab] Airflow pipelines upload data Google Cloud Storage and BigQuery](./03-gpc-bigquery/)



## Apache Beam:
- Apache Beam is an open-source, unified programming model for building data processing pipelines. It provides a high-level API (Application Programming Interface) that allows developers to write data processing logic once and run it on various execution frameworks, such as Apache Spark, Apache Flink, and Google Cloud Dataflow.

- The main goal of Apache Beam is to abstract away the complexities of distributed data processing and provide a consistent model for both batch and stream processing. It enables developers to focus on the logic of their data pipelines rather than the underlying execution engine.

![Alt text](images/Apache%20Beam.png)

- [Why and when should I consider Apache Beam](./050-beam/)
- [[Lab]First step with Apache Beam](./051-hello-beam/)
- [Basic concepts of Apache Beam(Pipeline, PCollection, PTransform, ParDo, GroupByKey, I/O Connectors, Runners)](./052-beam-components/)
- [[Lab] Apache Beam to practice](./053-practices-beam/)


## Google Cloud Dataflow:
- Google Cloud Dataflow is a fully managed service provided by Google Cloud Platform (GCP) for executing data processing pipelines. It is built on Apache Beam, which provides a unified programming model for writing data processing pipelines that can run on various execution engines.

![Alt text](images/Google%20Cloud%20Dataflow.png)
- [Apache Beam and Google Cloud Dataflow](./102-beam-cmd/)
- [[Lab] Create Google Cloud Template And Execute The Template](./103-beam-python/)
- [[Lab Final] Full workflow Arflow, Apache Beam and Google Cloud Platform (GCP)](./106.01-Final-clean/)



## Google KMS and Goole Tink:
- Google Cloud Key Management Service (KMS) and Google Tink are both cryptographic tools provided by Google for secure data management and encryption. While they serve similar purposes, they have different functionalities and use cases.


    - `Google Cloud KMS`: is a cloud-based key management service that allows you to generate, use, rotate, and manage cryptographic keys for securing data and resources in Google Cloud Platform (GCP).

    - `Google Tink`: is an open-source, multi-language cryptographic library that provides a collection of cryptographic APIs and tools for developers. Tink is designed to simplify the process of implementing secure cryptographic operations and best practices.

    ![Alt text](images/Google%20KMS%20and%20Goole%20Tink.png)



- [[Lab] First step with Keyring and Key in Google KMS ](./107-kms/)
- [[Lab] Simple Tink AEAD Encryption Example](./203-tink-example/)
- [[Lab] Encrypt the large file with Tink and KMS](./204-tink-streaming_aead/)
- [[Lab] Resolve out of Memory issue](./205-apply-tink-streaming-to-client-source/): An issue arises when the client attempts to encrypt a large file for uploading it to the cloud or when the file is too large to decrypt and extract data into Google BigQuery


