
```bash
# Create virtual Python environment
python3.8 -m venv .venv

# Activate virtual Python environment
. .venv/bin/activate


# Install Python requirements
#   Ignore expected warning: 'WARNING: You are using pip version 19.3.1; however, version 22.2.2 is available.'
python3.8 -m pip install -r requirements.txt

```


Example:
```bash
source ~/.bashrc
export SERVICE_ACCOUNT_KEY_PATH=$vi 
export PROJECT_ID="devops-simple"
export BUCKET_NAME="108-demo-gsutil"
export REGION="global"
export KEYRING_NAME=keyring-devops-simple
export LOCATION=global
export KEY_NAME=key-devops-simple
export TEST_UPLOAD_FILE_NAME_1="/Users/kany/project-local/data-home/tranning-Airflow/large-files/department-data.txt"
export FILE_NNAME="department-data_encript.txt"

# upload encrypted file (using wrapped gsutil)
./gsutil cp --client_side_encryption=gcp-kms://projects/${PROJECT_ID}/locations/${REGION}/keyRings/${KEYRING_NAME}/cryptoKeys/${KEY_NAME},${SERVICE_ACCOUNT_KEY_PATH} "${TEST_UPLOAD_FILE_NAME_1}" gs://${BUCKET_NAME}/${FILE_NNAME}




```
