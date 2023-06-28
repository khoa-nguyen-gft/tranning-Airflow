

# Encrypt the large file with Tink and KMS

To follow the given commands, please use the following guideline:

## Step 1: Generate a Keyset and Write it to encrypted-keyset.cfg

Run the following command in the terminal:

```bash
tinkey create-keyset \
--key-template AES256_CTR_HMAC_SHA256_1MB \
--out streaming_aead_keyset-new-V2.json \
--out-format JSON \
--master-key-uri gcp-kms://projects/devops-simple/locations/global/keyRings/keyring-devops-simple/cryptoKeys/key-devops-simple \
--credential /Users/kany/google-keys/bigquery-data-viewer-57f9c6eff886.json

# List metadata of keys in an encrypted keyset, using credentials in credentials.json

tinkey list-keyset --in streaming_aead_keyset-new.json \
--master-key-uri gcp-kms://projects/devops-simple/locations/global/keyRings/keyring-devops-simple/cryptoKeys/key-devops-simple \
--credential /Users/kany/google-keys/bigquery-data-viewer-57f9c6eff886.json

```

This command generates a keyset using the specified key template and writes it to the "streaming_aead_keyset-new-V2.json" file in JSON format.



# Step 2: Encrypt a File
You can encrypt a file using the following command:


```bash

# You can then encrypt a file with:
python 008-tink-solution.py \
    --mode encrypt \
    --keyset_path streaming_aead_keyset.json\
    --input_path /Users/kany/project-local/data-home/tranning-Airflow/large-files/CSV-2.3-MB.csv \
    --output_path output.bin
```

This command encrypts the file located at "/Users/kany/project-local/data-home/training-Airflow/large-files/CSV-2.3-MB.csv" using the keyset from "streaming_aead_keyset.json". The encrypted output is saved to "output.bin" file.


Step 3: Decrypt the Output File
You can decrypt the output file using the following command:



```bash
python 008-tink-solution.py \
    --mode decrypt \
    --keyset_path streaming_aead_keyset.json\
    --input_path output.bin \
    --output_path testdata.txt.plaintext
```

This command decrypts the encrypted file "output.bin" using the keyset from "streaming_aead_keyset.json". The decrypted output is saved to "testdata.txt.plaintext" file.

Please ensure that you replace the file paths and key URIs with the appropriate values based on your setup. Also, make sure you have the necessary dependencies and credentials properly configured.
