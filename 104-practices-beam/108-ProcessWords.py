import apache_beam as beam


class ProcessWords(beam.DoFn):
    def process(self, element, cutoff_length, marker):
        name = element.split(",")[1]
        if name.startswith(marker):
            return [beam.pvalue.TaggedOutput('nameA', name)]

        if len(name) <= cutoff_length:
            return [beam.pvalue.TaggedOutput('sortName', name)]
        else:  
            return [beam.pvalue.TaggedOutput('longName', name)]
        
    


with beam.Pipeline() as p:
    result = (
        p 
        | beam.io.ReadFromText("input/department-data.txt")
        | beam.ParDo(ProcessWords(), cutoff_length=4, marker = 'A').with_outputs('sortName', 'longName', "nameA")
    )

    sortName = (
        result.sortName
        | "sortName" >> beam.Map(lambda it: print("sort name: ", it))
    )

    longName = (
        result.longName
        | "longName" >> beam.Map(lambda it: print("long name: ", it))
    )
    nameA = (
        result.nameA
        | "Name A" >> beam.Map(lambda it: print("A name: ", it))
    )

