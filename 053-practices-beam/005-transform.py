

import apache_beam as beam
import subprocess

class MyTransform(beam.PTransform):
    def expand(self, input_colum):
        result = (
            input_colum
            | "group by sum" >> beam.CombinePerKey(sum)
            | "count filter" >> beam.Filter(filter_on_count)
            | "Format display" >> beam.Map(format_output)
        )
        return result
        

def filter_on_count(element):
    (name, count) = element
    if count > 30:
        return element

def format_output(element): 
    (name, count) = element
    return ', '.join((str(name.encode("ascii")), str(count), 'Regular Employee'))

with beam.Pipeline() as p1:
    input_collection =(
        p1
        | "read data from text" >> beam.io.ReadFromText("./input/department-data.txt")
        | "split data"          >> beam.Map(lambda x: x.split(','))
    )

    accounts_count = (
        input_collection
        | "get All accounts department person"  >> beam.Filter(lambda x: x[3] == 'Accounts')
        | "Pair each account employee with 1 Account" >> beam.Map(lambda x: ('Accounts, ' + x[1], 1))
        | "call compose transform Account" >> MyTransform()
        # | "group by sum Account"                      >> beam.CombinePerKey(sum)
        # | "write result to file Account"              >> beam.io.WriteToText("output/Accounts") 
    )

    hr_count = (
        input_collection
        | "get All HR department person"  >> beam.Filter(lambda x: x[3] == 'HR')
        | "Pair each account employee with 1 HR" >> beam.Map(lambda x: ('HR, '+ x[1], 1))
        | "call compose transform HR" >> MyTransform()

        # | "group by sum HR"                      >> beam.CombinePerKey(sum)
        # | "write result to file HR"              >> beam.io.WriteToText("output/HR") 
    )

    both = (
        (accounts_count, hr_count)
        | beam.Flatten()
        | beam.io.WriteToText("output/both")
    )
