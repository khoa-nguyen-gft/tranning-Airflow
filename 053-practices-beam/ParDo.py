import apache_beam as beam

class MultiplyByTwo(beam.DoFn):
    def process(self, element):
        yield element * 2
        yield element * 3
        print("==========")

# Create a pipeline
pipeline = beam.Pipeline()

# Apply ParDo transform
output = (
    pipeline
    | 'Create input' >> beam.Create([1, 2, 3, 4, 5])
    | 'Multiply by Two' >> beam.ParDo(MultiplyByTwo())
)

# Print the output elements
output | 'Print Output' >> beam.Map(print)

# Run the pipeline
pipeline.run()
