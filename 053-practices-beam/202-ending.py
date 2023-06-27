from typing import Dict


def schema_from_dict(schema_dict: Dict) -> Dict:
    parsing_schema = {}
    col_widths = schema_dict.get("columns")
    current_index = 0

    for col in col_widths:
        col_width = col.get("length")
        col_name = col.get("name")
        end_index = current_index + int(col_width)
        parsing_schema[col_name] = {'start': current_index, 'end': end_index}
        current_index = end_index

    print("current_index", current_index)
    print("parsing_schema", parsing_schema)
    return parsing_schema


schema = schema_from_dict(
    {
        "columns": [
            {
                "name": "Acct_Nbr",
                "length": "10"
            },
            {
                "name": "Appl_id",
                "length": "3"
            },
            {
                "name": "Control_Fields",
                "length": "8"
            },
            {
                "name": "dummy",
                "length": "1"
            }
        ]
    }
)


def drop_dummies_and_fillers(schema_def: Dict) -> Dict:
    clean_dict = {}
    for key, value in schema_def.items():
        if 'dummy' not in key.lower() and 'filler' not in key.lower():
            clean_dict[key] = value
    print("clean_dict: ", clean_dict)
    return clean_dict


drop_dump = drop_dummies_and_fillers(schema)

def bq_schema_from_col_names(col_names: Dict) -> str:
    bq_schema = ""
    print("col_names: ", col_names)
    for col_name in col_names:
        bq_schema += f'{col_name}:STRING,'
        print("bq_schema", bq_schema[:-5])
        print("bq_schema", bq_schema)

    return bq_schema[:-1]

#bq_schema Acct_Nbr:STRING,Appl_id:STRING,Control_Fields:STRING
bq_schema_from_col_names(drop_dump)