import ecdsa, hashlib


private_key = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)

public_key = private_key.get_verifying_key()

public_key_hex_uncompressed = public_key.to_string("uncompressed").hex()

# exclude (prefix)
x_coordinate_bytes = list(bytes.fromhex(public_key_hex_uncompressed)[1:33])
y_coordinate_bytes = list(bytes.fromhex(public_key_hex_uncompressed)[33:])

message_hash = hashlib.sha256("Hello, World!".encode("utf-8")).hexdigest()
message_bytes = bytes.fromhex(message_hash)

signature = private_key.sign_deterministic(
    message_bytes,
    extra_entropy=b"",
    # hash the message hash (2x sha256)
    hashfunc=hashlib.sha256,
)

order_size = private_key.curve.order.bit_length() // 8

r, s = ecdsa.util.sigdecode_string(signature, private_key.curve.order)

r_bytes = r.to_bytes(order_size, "big")

s_bytes = s.to_bytes(order_size, "big")

# print the message input (32 bytes)
print("message_bytes: ", list(message_bytes))
# print the x coordinate (32 bytes)
print("x_coordinate: ", x_coordinate_bytes)
# print the y coordinate (32 bytes)
print("y_coordinate: ", y_coordinate_bytes)
# print the Signature (64 bytes)
print("signature: ", list(bytes.fromhex(signature.hex())))
# print the r component of signature (32 bytes)
print("r", list(r_bytes))
# print the s component of signature (32 bytes)
print("s", list(s_bytes))
