import ecdsa, io, json, os
from eth_utils.crypto import keccak
from Crypto.Hash import keccak
from web3 import Web3
from ecdsa import VerifyingKey, SECP256k1


def get_bit_array(byte_list):
    bit_array = [bin(byte)[2:].zfill(8) for byte in byte_list]
    bit_string = "".join(bit_array)
    return [int(bit) for bit in bit_string]


def segment_into_chunks(bit_array, chunk_size):
    return [
        int("".join(map(str, bit_array[i : i + chunk_size])), 2)
        for i in range(0, len(bit_array), chunk_size)
    ]


def verify_signature(message, signature, public_key_hex):
    # Hash the message
    k = keccak.new(digest_bits=256)
    k.update(message.encode())
    message_hash = k.digest()

    # Load the public key
    vk = VerifyingKey.from_string(bytes.fromhex(public_key_hex), curve=SECP256k1)

    # Verify the signature
    try:
        is_valid = vk.verify(signature, message_hash)
        (
            print("Signature is valid!")
            if is_valid
            else print("Signature verification failed.")
        )
    except ecdsa.BadSignatureError:
        print("Signature verification failed.")


w3 = Web3()
private_key = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)
private_key_bytes = private_key.to_string()
private_key_hex = private_key_bytes.hex()
public_key = private_key.get_verifying_key()
public_key_hex = public_key.to_string("uncompressed").hex()

# exclude (prefix)
x_coordinate_bytes = list(bytes.fromhex(public_key_hex)[1:33])
x_coordinate_bits = get_bit_array(x_coordinate_bytes)

y_coordinate_bytes = list(bytes.fromhex(public_key_hex)[33:])
y_coordinate_bits = get_bit_array(y_coordinate_bytes)

message = "Hello,World!!!!!"

message_bytes = message.encode()
k = keccak.new(digest_bits=256)
k.update(message_bytes)
hash_result = k.hexdigest()
hash_bytes = bytes.fromhex(hash_result)
hash_bits = get_bit_array(hash_bytes)

signature = private_key.sign(hash_bytes)
order_size = private_key.curve.order.bit_length() // 8
r, s = ecdsa.util.sigdecode_string(signature, private_key.curve.order)

r_bytes = r.to_bytes(order_size, byteorder="big")
s_bytes = s.to_bytes(order_size, byteorder="big")
r_bits = get_bit_array(r_bytes)
s_bits = get_bit_array(s_bytes)


verify_signature(message, signature, public_key_hex)

# print the x coordinate (32 bytes)
print("x_coordinate: ", x_coordinate_bits)
print("x_coordinate len: ", len(x_coordinate_bits))

# print the y coordinate (32 bytes)
print("y_coordinate: ", y_coordinate_bits)
print("y_coordinate len: ", len(y_coordinate_bits))

# print the Signature (64 bytes)
print("signature: ", signature)
print("signature len: ", len(signature))

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
                "message": get_bit_array(list(message_bytes)),
                "r": segment_into_chunks(r_bits, 64),
                "s": segment_into_chunks(s_bits, 64),
                "pubkeyX": segment_into_chunks(x_coordinate_bits, 64),
                "pubkeyY": segment_into_chunks(y_coordinate_bits, 64),
            },
            f,
        )

    # os.system(
    #     "cd circuit/ecdsa_verify_cpp && ./ecdsa_verify ../input.json ../ecdsa_verify_witness.wtns"
    # )

    # with io.open("circuit/ecdsa_verify_cpp/output.json", "r") as f:
    #     return [int(s) for s in json.loads(f.read())]


verify()
