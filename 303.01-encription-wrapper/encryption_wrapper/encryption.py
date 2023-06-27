#!/usr/bin/env python3

import os
import shutil
import stat
import logging
logging.basicConfig(level='INFO')

from encryption_wrapper.common import error_and_exit

import tink
from tink import aead
from tink.core import TinkError
from tink.integration import gcpkms
from tink import streaming_aead


_TMP_LOCATION = os.getenv('GSUTIL_TMP_LOCATION',
                          os.path.expanduser('~') + '/.gsutil-wrapper/')


class EncryptWithTink(object):
  """Perform local encryption and decryption with Tink."""

  def __init__(self, key_uri, creds, tmp_location=_TMP_LOCATION):

    self.tmp_location = tmp_location
    # Make the tmp dir if it doesn't exist
    if not os.path.isdir(self.tmp_location):
      # noinspection PyUnusedLocal
      try:
        os.makedirs(self.tmp_location)
      except FileExistsError:
        # This is ok because the directory already exists
        pass
      except OSError as os_error:
        error_and_exit(str(os_error))

    # Initialize Tink
    try:
      aead.register()      
      self.key_template = aead.aead_key_templates.AES256_EAX
      self.keyset_handle = tink.new_keyset_handle(self.key_template)
      gcp_client = gcpkms.GcpKmsClient(key_uri, creds)
      gcp_aead = gcp_client.get_aead(key_uri)
      self.env_aead = aead.KmsEnvelopeAead(self.key_template, gcp_aead)

      streaming_aead.register()

    except TinkError as tink_init_error:
      error_and_exit('tink initialization failed: ' + str(tink_init_error))

  def encrypt(self, filepath):
    print(">>>>>>>>>>> EncryptWithTink: encrypt: ", filepath)
    if os.path.isdir(filepath):
      error_and_exit('cannot encrypt a directory')
    elif stat.S_ISFIFO(os.stat(filepath).st_mode):
      error_and_exit('cannot encrypt a FIFO')

    filename = os.path.basename(filepath)
    encrypted_filepath = self.tmp_location + '/' + filename
    print(">>>>>>>>>>> EncryptWithTink: filename: ", filename)
    print(">>>>>>>>>>> EncryptWithTink: encrypted_filepath: ", encrypted_filepath)
    print(">>>>>>>>>>> EncryptWithTink: filepath: ", filepath)

    try:
      shutil.copyfile(filepath, encrypted_filepath)
    except OSError as copy_error:
      error_and_exit("EXCEPTION COPY",str(copy_error))

    try:
      with open(filepath, 'rb') as f:
        plaintext = f.read()
      ciphertext = self.env_aead.encrypt(plaintext, b'')
      with open(encrypted_filepath, 'wb') as f:
        f.write(ciphertext)
    except TinkError as encryption_error:
      error_and_exit("encryption_error", str(encryption_error))

    print(">>>>>>>>>>> DONE EncryptWithTink: filepath: ", filepath)

    return encrypted_filepath

  def decrypt(self, filepath):
    filename = os.path.basename(filepath)
    decrypted_filepath = self.tmp_location + '/' + filename

    try:
      with open(filepath, 'rb') as f:
        ciphertext = f.read()
      cleartext = self.env_aead.decrypt(ciphertext, b'')
      with open(decrypted_filepath, 'wb') as f:
        f.write(cleartext)
      shutil.copyfile(decrypted_filepath, filepath)
      os.unlink(decrypted_filepath)
    except TinkError as decryption_error:
      error_and_exit(str(decryption_error))

    return decrypted_filepath


  def stream_encrypt(self, filepath):
    print("stream_encrypt")
