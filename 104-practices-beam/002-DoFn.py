import apache_beam as beam
from apache_beam.testing.util import assert_that
from apache_beam.testing.util import equal_to


pipline = beam.Pipeline()

# Define a custom DoFn


class MultiplyByTwo(beam.DoFn):
    def process(self, element):
        yield element * 2


output = (
    pipline
    | 'Create number' >> beam.Create([1, 2, 3, 4, 5, 6, 7, 8])
    | 'Square Number' >> beam.ParDo(MultiplyByTwo())
    | 'Filter even numbers' >> beam.Filter(lambda x: x % 2 == 0)
    | "print" >> beam.Map(lambda x: print(x))
)


# Run the pipeline
result = pipline.run()
