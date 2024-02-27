import ecdsa, io, json, os
from eth_utils.crypto import keccak
from Crypto.Hash import keccak
from web3 import Web3

w3 = Web3()

private_key = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)

private_key_bytes = private_key.to_string()

private_key_hex = private_key_bytes.hex()

public_key = private_key.get_verifying_key()

public_key_hex_uncompressed = public_key.to_string("uncompressed").hex()

# exclude (prefix)
x_coordinate_bytes = list(bytes.fromhex(public_key_hex_uncompressed)[1:33])
y_coordinate_bytes = list(bytes.fromhex(public_key_hex_uncompressed)[33:])


message = "Hello, World!"

message_bytes = message.encode()

k = keccak.new(digest_bits=256)

k.update(message_bytes)

hash_result = k.hexdigest()

signature_obj = w3.eth.account._sign_hash(
    bytes.fromhex(hash_result), private_key=private_key_hex
)

signature = signature_obj.signature

r_s_bytes_from_sign = signature[:-1]

order_size = private_key.curve.order.bit_length() // 8

r, s = ecdsa.util.sigdecode_string(r_s_bytes_from_sign, private_key.curve.order)

r_bytes = r.to_bytes(order_size, "big")

s_bytes = s.to_bytes(order_size, "big")

# print the message input (32 bytes)
print("message_bytes: ", list(message_bytes))
print("message_bytes len: ", len(list(message_bytes)))

# print the x coordinate (32 bytes)
print("x_coordinate: ", x_coordinate_bytes)
print("x_coordinate len: ", len(x_coordinate_bytes))

# print the y coordinate (32 bytes)
print("y_coordinate: ", y_coordinate_bytes)
print("y_coordinate len: ", len(y_coordinate_bytes))

# print the Signature (64 bytes)
print("signature: ", list(r_s_bytes_from_sign))
print("signature len: ", len(list(r_s_bytes_from_sign)))

# print the r component of signature (32 bytes)
print("r:", list(r_bytes))
print("r len:", len(list(r_bytes)))

# print the s component of signature (32 bytes)
print("s:", list(s_bytes))
print("s len:", len(list(s_bytes)))


def verify():
    with io.open("circuit/input.json", "w") as f:
        json.dump(
            {
                "message": list(message_bytes),
                "r": list(r_bytes),
                "s": list(s_bytes),
                "pubkeyX": "",
                "pubkeyY": "",
            },
            f,
        )

    os.system(
        "cd circuit/ecdsa_verify_cpp && ./ecdsa_verify ../input.json ../ecdsa_verify_witness.wtns"
    )

    with io.open("circuit/ecdsa_verify_cpp/output.json", "r") as f:
        return [int(s) for s in json.loads(f.read())]
