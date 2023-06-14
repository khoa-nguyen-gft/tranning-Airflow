import tink
from tink import daead

plaintext = b'your data...'
associated_data = b'context'

# Register all deterministic AEAD primitives
daead.register()

# 1. Get a handle to the key material.
keyset_handle = tink.new_keyset_handle(daead.deterministic_aead_key_templates.AES256_SIV)

# 2. Get the primitive.
daead_primitive = keyset_handle.primitive(daead.DeterministicAead)

# 3. Use the primitive.
ciphertext = daead_primitive.encrypt_deterministically(plaintext, associated_data)

print("ciphertext", ciphertext)