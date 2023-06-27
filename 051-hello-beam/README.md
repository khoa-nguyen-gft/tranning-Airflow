# Lab Document: Department Data Analysis using Apache Beam

## Objective
The objective of this lab is to analyze the department data and calculate the attendance count for the 'Accounts' department using Apache Beam.

## Code

```python
import apache_beam as beam
import subprocess

p1 = beam.Pipeline()

attendance_count = (
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
```

## Explanation
The code performs the following steps:

1. Imports the necessary libraries, including Apache Beam (`apache_beam`) and subprocess.

2. Creates a Beam pipeline (`p1`) using `beam.Pipeline()`.

3. Reads the department data from the file `input/department-data.txt` using `beam.io.ReadFromText().`

4. Splits each record by comma using `beam.Map(lambda record: record.split(','))`.

5. Filters the records, selecting only those where the department is 'Accounts' using `beam.Filter(lambda record: record[3] == 'Accounts')`.

6. Maps each record to a key-value pair, where the key is the employee name (`record[1]`) and the value is 1, representing attendance.

7. Combines the attendance counts for each employee using `beam.CombinePerKey(sum)`.

8. Maps the resulting attendance counts to strings using `beam.Map(lambda employee_count: str(employee_count))`.

9. Writes the final result to the `'output/data'` file using `beam.io.WriteToText()`.

10. Executes the pipeline using `p1.run()` and waits until it finishes using `process.wait_until_finish()`.

11. Retrieves the first 20 lines of the output file using the shell command `head -n 20 output/data-00000-of-00001` and `subprocess.run()`.

12. Stores the output in the `output` variable and prints it using `print(output)`.

## Result Output
The execution of the code produced the following output:

```python 
('Marco', 31)
('Rebekah', 31)
('Itoe', 31)
('Edouard', 31)
('Kyle', 62)
('Kumiko', 31)
('Gaston', 31)
('Ayumi', 30)
```
