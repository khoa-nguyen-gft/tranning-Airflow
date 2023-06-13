import apache_beam as beam



side_list = list()
with open("input/exclude_ids.txt") as my_file:
    for line in my_file:
        side_list.append(line)


class FilterUsingLength(beam.DoFn):
    def process(self, element, side_list, lower_bound, upper_bound=float('inf')):
        element_list = element.split(',')
        id = element_list[0]
        name = element_list[1]
        # id = id.decode('utf-8', 'ignore').encode('utf-8')
        if(lower_bound <= len(name) <= upper_bound) and id not in side_list:
            return [element_list]


with beam.Pipeline() as p:
    small_names = (
        p
        | "Read from text file" >> beam.io.ReadFromText('input/department-data.txt')
        | "Pardo" >> beam.ParDo(FilterUsingLength(), side_list, 2, 10)
        | beam.Map(lambda record: (record[0] + " " + record[1], 1))
        | beam.CombinePerKey(sum)
        | "Print" >> beam.Map(print)

    )


