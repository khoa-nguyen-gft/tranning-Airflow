


``` bash

# Declare and assign values to variables
KEYRING_NAME=keyring-devops-simple
LOCATION=global
KEY_NAME=key-devops-simple
BUCKET_NAME=108-demo-gsutil
DATASET_ID=devops-simple.us
PROJECT_ID=devops-simple
REGION=asia-east2
SERVICE_ACCOUNT_NAME=bigquery-data-viewer

# Encrypt file
gsutil mb -c standard -p ${PROJECT_ID} -l ${REGION} gs://${BUCKET_NAME}

gsutil config -e

```

Certainly! Here are a few examples of gsutil commands:

1. List buckets:

```bash
gsutil ls

#Create a new bucket:
gsutil mb gs://new-bucket-name

#List objects in a bucket:
gsutil ls gs://bucket-name

#Copy a local file to a bucket:
gsutil cp local-file.txt gs://bucket-name

#Copy an object from a bucket to a local file:
gsutil cp gs://bucket-name/object-name local-file.txt

#Set the cache control metadata for an object:
gsutil setmeta -h "Cache-Control:public,max-age=3600" gs://bucket-name/object-name

```


2. Test upload 1GB to Google Cloud: 

    2.1. Encrypt the file using gcloud kms:

```bash
KEYRING_NAME=keyring-devops-simple
LOCATION=global
KEY_NAME=key-devops-simple

cat department-data.txt |\
    gcloud kms encrypt \
    --key $KEY_NAME \
    --keyring $KEYRING_NAME \
    --location $LOCATION \
    --plaintext-file=- --ciphertext-file=- |\
    base64 > encrypted.txt

```
    Upload the encrypted *.zip file to Google Cloud Storage using gsutil with a resumable upload:
```bash
    gsutil -o \
    "GSUtil:parallel_composite_upload_threshold=150M" \
    cp -r "/Users/kany/project-local/data-home/bigFiles/organizations-2000000.csv" \
    "gs://108-demo-gsutil/organizations-2000000.csv"

```



