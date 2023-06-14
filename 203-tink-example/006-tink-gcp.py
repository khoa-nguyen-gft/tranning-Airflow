import tink
import os
from tink.integration import gcpkms
from tink import aead, cleartext_keyset_handle, core, mac, tink_config
import logging
import sys

PROJECT_ID="devops-simple"
BUCKET_NAME="108-demo-gsutil"
REGION="asia-east2"
KEYRING_NAME="keyring-devops-simple"
LOCATION="global"
KEY_NAME="key-devops-simple"

os.environ["GRPC_DEFAULT_SSL_ROOTS_FILE_PATH"] = "/Users/kany/google-keys/roots.pem"

env_vars = os.environ

# Configure the key URI for the key you want to use
key_uri = f'gcp-kms://projects/{PROJECT_ID}/locations/{LOCATION}/keyRings/{KEYRING_NAME}/cryptoKeys/{KEY_NAME}'
gcp_credentials = env_vars.get("GOOGLE_APPLICATION_CREDENTIALS")
plaintext = b'your data...'
associated_data = b'context'

print("------------------------------------")
print("gcp_credentials: ", gcp_credentials)
print("key_uri: ", key_uri)
print("GRPC_DEFAULT_SSL_ROOTS_FILE_PATH: ", env_vars.get("GRPC_DEFAULT_SSL_ROOTS_FILE_PATH"))
print("------------------------------------")

  # Initialise Tink
try:
    aead.register()
    gcp_client = gcpkms.GcpKmsClient(key_uri, gcp_credentials)
    gcp_aead = gcp_client.get_aead(key_uri)
    key_template = aead.aead_key_templates.AES256_EAX
    env_aead = aead.KmsEnvelopeAead(key_template, gcp_aead)
except tink.TinkError as e:
    logging.error('Error initialising Tink: %s', e)
    os.exist(0)

# Use env_aead to encrypt data
try:
    ciphertext = env_aead.encrypt(plaintext, associated_data)
    print("Ciphertext:", ciphertext)
except tink.TinkError as e:
    logging.error('Error encrypting data: %s', e)
    sys.exit(1)