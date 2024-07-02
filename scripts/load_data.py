import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import sys

enc_file = sys.argv[1]
key = bytes.fromhex(sys.argv[2])
iv = bytes.fromhex(sys.argv[3])

cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
decryptor = cipher.decryptor()

ct = open(enc_file, 'rb').read()
print(decryptor.update(ct) + decryptor.finalize())
