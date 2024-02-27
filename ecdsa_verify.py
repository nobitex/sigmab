import ecdsa, io, json, os
from eth_utils.crypto import keccak
from Crypto.Hash import keccak
from web3 import Web3


def get_bit_array(byte_list):
    bit_array = [bin(byte)[2:].zfill(8) for byte in byte_list]
    bit_string = "".join(bit_array)
    return [int(bit) for bit in bit_string]


w3 = Web3()
private_key = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)
private_key_bytes = private_key.to_string()
private_key_hex = private_key_bytes.hex()
public_key = private_key.get_verifying_key()
public_key_hex_uncompressed = public_key.to_string("uncompressed").hex()

# exclude (prefix)
x_coordinate_bytes = list(bytes.fromhex(public_key_hex_uncompressed)[1:33])
x_coordinate_bits = get_bit_array(x_coordinate_bytes)

y_coordinate_bytes = list(bytes.fromhex(public_key_hex_uncompressed)[33:])
y_coordinate_bits = get_bit_array(y_coordinate_bytes)


message = "Hello, World!"

message_bytes = message.encode()
k = keccak.new(digest_bits=256)
k.update(message_bytes)
hash_result = k.hexdigest()
hash_bytes = bytes.fromhex(hash_result)
hash_bits = get_bit_array(hash_bytes)

signature_obj = w3.eth.account._sign_hash(hash_bytes, private_key=private_key_hex)
signature = signature_obj.signature
r_s_bytes_from_sign = signature[:-1]
r_s_bits_from_sign = get_bit_array(r_s_bytes_from_sign)


order_size = private_key.curve.order.bit_length() // 8
r, s = ecdsa.util.sigdecode_string(r_s_bytes_from_sign, private_key.curve.order)
r_bytes = r.to_bytes(order_size, "big")
r_bits = get_bit_array(r_bytes)

s_bytes = s.to_bytes(order_size, "big")
s_bits = get_bit_array(s_bytes)


# print the message input (32 bytes)
print("message_hash_bits: ", hash_bits)
print("message_bytes len: ", len(hash_bits))

# print the x coordinate (32 bytes)
print("x_coordinate: ", x_coordinate_bits)
print("x_coordinate len: ", len(x_coordinate_bits))

# print the y coordinate (32 bytes)
print("y_coordinate: ", y_coordinate_bits)
print("y_coordinate len: ", len(y_coordinate_bits))

# print the Signature (64 bytes)
print("signature: ", r_s_bits_from_sign)
print("signature len: ", len(r_s_bits_from_sign))

# print the r component of signature (32 bytes)
print("r:", r_bits)
print("r len:", len(r_bits))

# print the s component of signature (32 bytes)
print("s:", s_bits)
print("s len:", len(s_bits))


def verify():
    with io.open("circuit/input.json", "w") as f:
        json.dump(
            {
                "message": hash_bits,
                "r": r_bits,
                "s": s_bits,
                "pubkeyX": x_coordinate_bits,
                "pubkeyY": y_coordinate_bits,
            },
            f,
        )

    os.system(
        "cd circuit/ecdsa_verify_cpp && ./ecdsa_verify ../input.json ../ecdsa_verify_witness.wtns"
    )

    with io.open("circuit/ecdsa_verify_cpp/output.json", "r") as f:
        return [int(s) for s in json.loads(f.read())]
