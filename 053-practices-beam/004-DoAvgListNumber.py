import apache_beam as beam


class AvgFn(beam.CombineFn):
    def create_accumulator(self):
        return (0.0, 0)

    def add_input(self, sum_count, input):
        (sum, count) = sum_count
        return (sum + input, count + 1)
    
    def merge_accumulators(self, accumulators):
        ind_sum, ind_count = zip(*accumulators)
        return sum(ind_sum), sum(ind_count)
    
    def extract_output(self, accumulator):
        (sum, count) = accumulator
        return sum/count if count else float("N/A")
    

with beam.Pipeline() as pipeline :
    small_sum = (
        pipeline
        | beam.Create([15,5,7,7,9,23,13,5])
        | beam.CombineGlobally(AvgFn())
        | "output" >> beam.Map(print)

    )
