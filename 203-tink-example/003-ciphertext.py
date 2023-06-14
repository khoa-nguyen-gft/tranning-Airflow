import tink
from tink import aead

plaintext = b'your data...'
associated_data = b'context'

# Register all AEAD primitives
aead.register()

# 1. Get a handle to the key material.
keyset_handle = tink.new_keyset_handle(aead.aead_key_templates.AES256_GCM)

# 2. Get the primitive.
aead_primitive = keyset_handle.primitive(aead.Aead)

# 3. Use the primitive.
ciphertext = aead_primitive.encrypt(plaintext, associated_data)

print("ciphertext", ciphertext)