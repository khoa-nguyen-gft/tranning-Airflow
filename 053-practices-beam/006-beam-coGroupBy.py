import apache_beam as beam


def retTuple(element):
   thisTupple = element.split(',')
   return (thisTupple[0],thisTupple[1:])

def deduplicate(pcollection):
    return pcollection | beam.RemoveDuplicates()

with beam.Pipeline() as p1:
    dep_rows = (
        p1
        | "reading file 1" >> beam.io.ReadFromText("input/department-data.txt")
        | "pair eahc employee with key" >> beam.Map(retTuple) 
        
    )

    loc_rows = (
        p1
        | "reading file 2" >> beam.io.ReadFromText("input/location.txt")
        | "pair eahc loc with key" >> beam.Map(retTuple)
    )


    result = (
        {"dep_rows": dep_rows, "location_rows": dep_rows}
        | beam.CoGroupByKey()
        | beam.Map(print)
    )

