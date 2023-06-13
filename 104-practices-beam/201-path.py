import pathlib
import os

def get_schemas_json_path():
    return pathlib.Path(__file__).parents

schemas_json_path = get_schemas_json_path()
print(schemas_json_path)

print("__file__:", __file__)
print("__name__:", __name__)
print("__package__:", __package__)
# print("__path__:", __path__)
print("__loader__:", __loader__)
print("__spec__:", __spec__)
print("Current directory:", os.getcwd())