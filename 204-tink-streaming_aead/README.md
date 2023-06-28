




Generate a keyset, encrypt and write it to encrypted-keyset.cfg, using credentials in credentials.json

```bash
#
#projects/devops-simple/locations/global/keyRings/keyring-devops-simple/cryptoKeys/key-devops-simple

tinkey create-keyset --key-template AES256_CTR_HMAC_SHA256_1MB --out streaming_aead_keyset-new-V2.json \
--out-format JSON \
--master-key-uri gcp-kms://projects/devops-simple/locations/global/keyRings/keyring-devops-simple/cryptoKeys/key-devops-simple \
--credential /Users/kany/google-keys/bigquery-data-viewer-57f9c6eff886.json


# List metadata of keys in an encrypted keyset, using credentials in credentials.json
tinkey list-keyset --in streaming_aead_keyset-new.json \
--master-key-uri gcp-kms://projects/devops-simple/locations/global/keyRings/keyring-devops-simple/cryptoKeys/key-devops-simple \
--credential /Users/kany/google-keys/bigquery-data-viewer-57f9c6eff886.json


tinkey create-keyset --key-template AES256_CTR_HMAC_SHA256_1MB --out-format JSON --out streaming_aead_keyset.json

```
You can then encrypt a file with:




```bash

# You can then encrypt a file with:
python 008-tink-solution.py \
    --mode encrypt \
    --keyset_path streaming_aead_keyset.json\
    --input_path /Users/kany/project-local/data-home/tranning-Airflow/large-files/CSV-2.3-MB.csv \
    --output_path output.bin

#And then decrypt the the output with:
python 008-tink-solution.py \
    --mode decrypt \
    --keyset_path streaming_aead_keyset.json\
    --input_path output.bin \
    --output_path testdata.txt.plaintext
```


