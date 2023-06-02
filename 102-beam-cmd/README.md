


## Run an example pipeline in Dataflow as a job

A common example pipeline for Apache Beam is WordCount, which counts the unique words in an input text file—in this case, Shakespeare's King Lear.



```bash
    python3 -m \
    apache_beam.examples.wordcount \
    --region us-central1 --input \
    gs://dataflow-samples/shakespeare/kinglear.txt \
    --output \
    gs://dataflow-apache-quickstart_devops-simple/results/output \
    --runner DataflowRunner \
    --project devops-simple \
    --temp_location \
    gs://dataflow-apache-quickstart_devops-simple/temp/
```

![result](./Screenshot%202023-06-02%20at%2021.00.57.png)