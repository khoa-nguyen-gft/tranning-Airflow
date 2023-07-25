import logging
import tempfile
from utils.encryption_util import encrypt_data, decrypt_data, decrypt_data_content

# Set up logging configuration
logging.basicConfig(level=logging.DEBUG)

# Test encrypt_data function
input_file = 'input/gcp_util.py'
output_file = 'output/encrypt_flights_sample.csv'
associated_data = b"associated_data"
keyset_path = 'config/keyset.json'

# encrypt_data(input_file, output_file, associated_data, keyset_path)

# Test decrypt_data function
decrypted_output_file = 'input/hello_beam_dag_dec.py'

# decrypt_data(output_file, decrypted_output_file, associated_data, keyset_path)

# # Compare the input file and the decrypted output file
# with open(input_file, 'rb') as file1, open(decrypted_output_file, 'rb') as file2:
#     content1 = file1.read()
#     content2 = file2.read()
#     if content1 == content2:
#         print("Decryption successful. The input file and the decrypted output file match.")
#     else:
#         print("Decryption failed. The input file and the decrypted output file do not match.")

result = decrypt_data_content(output_file, associated_data, keyset_path)

print(f'result: {result}')
