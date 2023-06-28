# Learning Path: Technical ETL, Airflow, Apache Beam,Tink, Kafka in Banking Domain

![image](./images/Screenshot%202023-06-07%20at%2008.58.26%20copy.png)


## Setup:
[Developer Starter](./00-install/README.md) contains everything needed in order to get started Data.


## Airflow:

- Airflow is commonly used as a platform for orchestrating and managing data workflows. It provides a way to define, schedule, and monitor complex workflows consisting of tasks that need to be executed in a specific order or on a specific schedule.


![Alt text](images/Airflow.png)

- [Why and when should I consider Airflow](./00-when/README.md)
- [First step with Airflow](./01-hello-airflow/README.md)
- [Basic concepts of Airflow(DAGs, Tasks, Operators, Task dependencies)](./00-concepts/README.md)
- [Example of an Airflow pipelines upload data Google Cloud Storage)](./02-gpc/README.md)
- [Example of an Airflow pipelines upload data Google Cloud Storage and extract data into BigQuery)](./03-gpc-bigquery/README.md)



## Apache Beam:
- Apache Beam is an open-source, unified programming model for building data processing pipelines. It provides a high-level API (Application Programming Interface) that allows developers to write data processing logic once and run it on various execution frameworks, such as Apache Spark, Apache Flink, and Google Cloud Dataflow.

- The main goal of Apache Beam is to abstract away the complexities of distributed data processing and provide a consistent model for both batch and stream processing. It enables developers to focus on the logic of their data pipelines rather than the underlying execution engine.

![Alt text](images/Apache%20Beam.png)
- [Why and when should I consider Apache Beam](./050-beam/README.md)
- [First step with Apache Beam](./051-hello-beam/README.md)
- [Basic concepts of Apache Beam(DAGs, Tasks, Operators, Task dependencies)](./052-beam-components/README.md)
- [Examples of Apache Beam to practice](./053-practices-beam/README.md)


## Google Cloud Dataflow:
- Google Cloud Dataflow is a fully managed service provided by Google Cloud Platform (GCP) for executing data processing pipelines. It is built on Apache Beam, which provides a unified programming model for writing data processing pipelines that can run on various execution engines.

![Alt text](images/Google%20Cloud%20Dataflow.png)
- [Apache Beam and Google Cloud Dataflow](./102-beam-cmd/README.md)
- [Create Google Cloud Template And Execute The Template](./103-beam-python/README.md)

