import apache_beam as beam
import subprocess


p1 = beam.Pipeline();

attence_count = (
    p1
    | beam.io.ReadFromText('input/department-data.txt')
    | beam.Map(lambda record: record.split(','))
    | beam.Filter(lambda record: record[3] == 'Accounts')
    | beam.Map(lambda record: (record[1], 1))
    | beam.CombinePerKey(sum)
    | beam.Map(lambda employee_count: str(employee_count))
    | beam.io.WriteToText('output/data')
)

process = p1.run()
process.wait_until_finish()


command = 'head -n 20 output/data-00000-of-00001'
result = subprocess.run(command, shell=True, capture_output=True, text=True)

output = result.stdout
print(output)