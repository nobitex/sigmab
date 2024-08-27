import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import sys

file = sys.argv[1]
data = open(file, "rb").read()
while len(data) % 16 != 0:
    data += b" "

key = os.urandom(32)
iv = os.urandom(16)
cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
encryptor = cipher.encryptor()
ct = encryptor.update(data) + encryptor.finalize()

with open(file + ".enc", "wb") as f:
    f.write(ct)

print(f"key: {key.hex()}, iv: {iv.hex()}")
