import tink
import os
from tink.integration import gcpkms
from tink import aead
import logging
import sys

PROJECT_ID = "devops-simple"
BUCKET_NAME = "108-demo-gsutil"
REGION = "asia-east2"
KEYRING_NAME = "keyring-devops-simple"
LOCATION = "global"
KEY_NAME = "key-devops-simple"
FILE_NAME = "department-data.txt"


os.environ["GRPC_DEFAULT_SSL_ROOTS_FILE_PATH"] = "/Users/kany/google-keys/roots.pem"

env_vars = os.environ

# Configure the key URI for the key you want to use
key_uri = f'gcp-kms://projects/{PROJECT_ID}/locations/{LOCATION}/keyRings/{KEYRING_NAME}/cryptoKeys/{KEY_NAME}'
gcp_credentials = env_vars.get("GOOGLE_APPLICATION_CREDENTIALS")

parent_folder = os.path.dirname(os.getcwd())

plaintext_file = f"{parent_folder}/large-files/{FILE_NAME}"  # Path to the large file you want to encrypt
associated_data = b'context'
decrypted_output_file_path = f"./decrypted_{FILE_NAME}"
encrypted_output_file_path = f"./encrypted_{FILE_NAME}.bin"

print("------------------------------------")
print("gcp_credentials: ", gcp_credentials)
print("key_uri: ", key_uri)
print("GRPC_DEFAULT_SSL_ROOTS_FILE_PATH: ", env_vars.get("GRPC_DEFAULT_SSL_ROOTS_FILE_PATH"))
print("Input plaintext file: ", plaintext_file)
print("Encrypted output file path: ", encrypted_output_file_path)
print("Decrypted output file path: ", decrypted_output_file_path)

print("------------------------------------")

# Initialize Tink

try:
    aead.register()
    gcp_client = gcpkms.GcpKmsClient(key_uri, gcp_credentials)
    gcp_aead = gcp_client.get_aead(key_uri)
    key_template = aead.aead_key_templates.AES256_EAX
    env_aead = aead.KmsEnvelopeAead(key_template, gcp_aead)
except tink.TinkError as e:
    logging.error('Error initializing Tink: %s', e)
    sys.exit(1)


# Encrypt the large file in chunks
chunk_size = 1 * 1024  # Set the chunk size (1MB in this example)
ciphertext = bytearray()

try:
    with open(plaintext_file, "rb") as file:
        while True:
            chunk = file.read(chunk_size)
            if not chunk:
                break
            encrypted_chunk = env_aead.encrypt(chunk, associated_data)
            ciphertext.extend(encrypted_chunk)
except tink.TinkError as e:
    logging.error('Error encrypting data: %s', e)
    sys.exit(1)

# Write the ciphertext to the output file
with open(encrypted_output_file_path, "wb") as output_file:
    output_file.write(ciphertext)

print("Encrypted data written to:", encrypted_output_file_path)


# Read the encrypted data from the input file
with open(encrypted_output_file_path, "rb") as input_file:
    ciphertext = input_file.read()

print("length ciphertext:", len(ciphertext))

# Use env_aead to decrypt data
try:
    decrypted_chunks = []
    for i in range(0, len(ciphertext), chunk_size):
        print("i:", i, "i+chunk_size:", i+chunk_size)

        encrypted_chunk = ciphertext[i:i+chunk_size]
        decrypted_chunk = env_aead.decrypt(encrypted_chunk, associated_data)
        print("decrypted_chunk: ", decrypted_chunk)
        decrypted_chunks.append(decrypted_chunk)

    cleartext = b"".join(decrypted_chunks)

    # Write the decrypted data to the output file
    with open(decrypted_output_file_path, "wb") as output_file:
        output_file.write(cleartext)

    print("Decrypted data written to:", decrypted_output_file_path)

except tink.TinkError as e:
    logging.error('Error decrypting data: %s', e)
    sys.exit(1)



