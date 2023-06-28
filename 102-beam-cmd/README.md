
## Apache Beam and Google Cloud Dataflow
 Apache Beam and Google Cloud Dataflow are two related but distinct concepts. Let me clarify:

![Alt text](images/Apache%20Beam%20and%20Google%20Cloud%20Dataflow.png)

# Apache Beam

Apache Beam is an open-source unified programming model for building data processing pipelines. It provides a high-level API that allows you to write data processing logic in a language-agnostic manner. With Apache Beam, you can write your data processing pipelines once and run them on different execution frameworks, including Google Cloud Dataflow.

# Google Cloud Dataflow

Google Cloud Dataflow is a fully managed service provided by Google Cloud Platform for executing Apache Beam pipelines. It allows you to run your Apache Beam pipelines without managing the underlying infrastructure. Dataflow provides scalability, automatic resource management, fault-tolerance, and integration with other Google Cloud services.

When you use Apache Beam with the Google Cloud Dataflow runner, you can take advantage of the features and benefits offered by Google Cloud Dataflow, such as:

- `Automatic scaling`: Dataflow dynamically scales resources up or down based on the workload.
- `Fault-tolerance`: Dataflow handles failures and ensures reliable execution of pipelines.
- `Integration with Google Cloud services`: Dataflow integrates seamlessly with other Google Cloud services like BigQuery, Pub/Sub, and Cloud Storage.
- `Monitoring and logging`: Dataflow provides monitoring dashboards, logs, and alerts for tracking pipeline progress and performance.
- `Job management`: Dataflow allows you to submit, monitor, and manage your pipeline jobs through the Google Cloud Console, command-line tools, or APIs.

To use Apache Beam with Google Cloud Dataflow, you typically write your pipeline code using Apache Beam's API and then submit the pipeline to Dataflow for execution. Dataflow takes care of the execution and management of the pipeline, ensuring efficient processing of your data at scale.

In summary, Apache Beam is the programming model and API, while Google Cloud Dataflow is the managed service provided by Google Cloud Platform for executing Apache Beam pipelines.


## Run an example pipeline in Dataflow as a job

A common example pipeline for Apache Beam is [WordCount](https://github.com/apache/beam/blob/master/sdks/python/apache_beam/examples/wordcount.py), which counts the unique words in an input text file—in this case, Shakespeare's King Lear.


```python
    python3 -m \
    apache_beam.examples.wordcount \
    --job_name my-wordcount-job \
    --runner DataflowRunner \
    --region us-central1 \
    --input \
    gs://dataflow-samples/shakespeare/kinglear.txt \
    --output \
    gs://gft-demo-gcs-bucket/results/output \
    --project devops-simple \
    --temp_location \
    gs://gft-demo-gcs-bucket/temp/


```


![Alt text](images/Run%20an%20example%20pipeline%20in%20Dataflow%20as%20a%20job.png)