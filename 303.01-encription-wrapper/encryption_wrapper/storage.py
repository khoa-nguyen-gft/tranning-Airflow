import os
import random
import shutil
import string

from encryption_wrapper import encryption

from google.cloud import storage


_GSUTIL = os.getenv('GSUTIL_ACTUAL')
_TMP_LOCATION = os.getenv('GSUTIL_TMP_LOCATION',
                          os.path.expanduser('~') + '/.gsutil-wrapper/')


class Client(storage.Client):

  def __init__(self, key_uri, creds, tmp_location=_TMP_LOCATION):
    self.key_uri = key_uri
    self.creds = creds
    random_str = ''.join(
        (random.choice(string.ascii_letters + string.digits) for i in range(8)))
    self.tmp_location = tmp_location + random_str + '/'
    super().__init__()

  def bucket(self, bucket_name, user_project=None):
    return Bucket(
        client=self,
        name=bucket_name,
        user_project=user_project,
        key_uri=self.key_uri,
        creds=self.creds)


class Bucket(storage.Bucket):

  def __init__(self, client, name, user_project, key_uri, creds):
    self.key_uri = key_uri
    self.creds = creds
    super().__init__(client, name, user_project)

  def blob(self,
           blob_name,
           chunk_size=None,
           encryption_key=None,
           kms_key_name=None,
           generation=None):

    return Blob(
        blob_name=blob_name,
        bucket=self,
        chunk_size=chunk_size,
        encryption_key=encryption_key,
        kms_key_name=kms_key_name,
        generation=generation,
        key_uri=self.key_uri,
        creds=self.creds)


class Blob(storage.Blob):

  def __init__(self,
               blob_name,
               bucket,
               chunk_size=None,
               encryption_key=None,
               kms_key_name=None,
               generation=None,
               key_uri=None,
               creds=None):
    self.key_uri = key_uri
    self.creds = creds
    self.e = encryption.EncryptWithTink(self.key_uri, self.creds)
    super().__init__(blob_name, bucket, chunk_size, encryption_key,
                     kms_key_name, generation)

  def upload_from_filename(self,
                           file_obj,
                           rewind=False,
                           size=None,
                           content_type=None,
                           num_retries=None,
                           client=None,
                           predefined_acl=None,
                           if_generation_match=None,
                           if_generation_not_match=None,
                           if_metageneration_match=None,
                           if_metageneration_not_match=None,
                           timeout=60,
                           checksum=None):

    encrypted_file_obj = self.e.encrypt(file_obj)

    super().upload_from_filename(
        encrypted_file_obj,
        content_type,
        client,
        predefined_acl,
        if_generation_match,
        if_generation_not_match,
        if_metageneration_match,
        if_metageneration_not_match,
        timeout=60,
        checksum='md5')

    metadata_client = storage.Client()
    metadata_bucket = metadata_client.get_bucket(self.bucket.name)
    metadata_blob = metadata_bucket.get_blob(self.name)
    metadata = {'client-side-encrypted': 'true'}
    metadata_blob.metadata = metadata
    metadata_blob.patch(client=metadata_client)

    shutil.rmtree(_TMP_LOCATION)

  def download_to_filename(self,
                           filename,
                           client=None,
                           start=None,
                           end=None,
                           raw_download=False,
                           if_generation_match=None,
                           if_generation_not_match=None,
                           if_metageneration_match=None,
                           if_metageneration_not_match=None,
                           timeout=60,
                           checksum='md5'):

    super().download_to_filename(filename, client, start, end, raw_download,
                                 if_generation_match, if_generation_not_match,
                                 if_metageneration_match,
                                 if_metageneration_not_match, timeout, checksum)

    self.e.decrypt(filename)

    shutil.rmtree(_TMP_LOCATION)





