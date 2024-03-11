import ecdsa, io, json
from eth_utils.crypto import keccak
from Crypto.Hash import keccak
from web3 import Web3
from ecdsa import VerifyingKey, SigningKey, SECP256k1, util


def int_to_big_endian(x, length=32):
    return x.to_bytes(length, byteorder="big")


def big_endian_to_int(x):
    return int.from_bytes(x, byteorder="big")


def bigint_to_array(n, k, x):
    mod = 2**n
    ret = []
    for _ in range(k):
        ret.append(x % mod)
        x = x // mod
    return ret


def get_bit_array(byte_list):
    bit_array = [bin(byte)[2:].zfill(8) for byte in byte_list]
    bit_string = "".join(bit_array)
    return [int(bit) for bit in bit_string]


def segment_into_chunks(bit_array, chunk_size):
    return [
        int("".join(map(str, bit_array[i : i + chunk_size])), 2)
        for i in range(0, len(bit_array), chunk_size)
    ]


def segment_into_chunks_as_bits(bit_array, chunk_size):
    return [bit_array[i : i + chunk_size] for i in range(0, len(bit_array), chunk_size)]


def reconstruct_bit_array_from_chunks(chunks, bits_per_chunk):
    reconstructed_bit_array = []
    for chunk in chunks:
        # Ensure chunk_bits is padded to match the original chunk size
        chunk_bits = bin(chunk)[2:].zfill(bits_per_chunk)
        reconstructed_bit_array.extend(int(bit) for bit in chunk_bits)
    return reconstructed_bit_array


def int_to_array(n, k, x):
    mod = 1
    for _ in range(n):
        mod *= 2

    ret = []
    x_temp = x
    for _ in range(k):
        ret.append(x_temp % mod)
        x_temp = x_temp // mod
    return ret


def chunks_to_string(chunks):
    return [str(chunk) for chunk in chunks]


def verify_signature(message, signature, public_key_hex):
    # Load the public key
    vk = VerifyingKey.from_string(bytes.fromhex(public_key_hex), curve=SECP256k1)

    # Verify the signature
    try:
        is_valid = vk.verify_digest(signature, message)
        (
            print("Signature is valid!")
            if is_valid
            else print("Signature verification failed.")
        )
    except ecdsa.BadSignatureError:
        print("Signature verification failed.")


def bigint_to_Uint8Array(x, length=32):
    return x.to_bytes(length, byteorder="big", signed=False)


def verify():
    priv = 88549154299169935420064281163296845505587953610183896504176354567359434168161
    msghash_bigint = 1234

    # Generate signing and verifying keys
    sk = SigningKey.from_secret_exponent(priv, curve=SECP256k1)
    vk = sk.verifying_key
    pubkey = vk.pubkey.point

    msghash = int_to_big_endian(msghash_bigint)

    # Signing
    signature = sk.sign_digest(msghash, sigencode=util.sigencode_string)

    # Extract r and s from signature
    r, s = util.sigdecode_string(signature, sk.curve.order)

    # Convert values
    r_array = bigint_to_array(64, 4, r)
    s_array = bigint_to_array(64, 4, s)
    msghash_array = bigint_to_array(64, 4, msghash_bigint)
    pub0_array = bigint_to_array(64, 4, pubkey.x())
    pub1_array = bigint_to_array(64, 4, pubkey.y())

    # Save to input file
    with io.open("circuit/temp/ecdsa_verify/input_ecdsa_verify.json", "w") as f:
        json.dump(
            {
                "msghash": chunks_to_string(msghash_array),
                "r": chunks_to_string(r_array),
                "s": chunks_to_string(s_array),
                "pubkey": [
                    chunks_to_string(pub0_array),
                    chunks_to_string(pub1_array),
                ],
            },
            f,
        )


w3 = Web3()
private_key = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)
private_key_bytes = private_key.to_string()
private_key_hex = private_key_bytes.hex()
public_key = private_key.get_verifying_key()
public_key_hex = public_key.to_string("uncompressed").hex()

# exclude (prefix)
x_coordinate_decimal = public_key.pubkey.point.x()
x_coordinate_array = int_to_array(64, 4, x_coordinate_decimal)


y_coordinate_decimal = public_key.pubkey.point.y()
y_coordinate_array = int_to_array(64, 4, y_coordinate_decimal)


message = [0, 1, 2, 3]

message_bytes = bytes()
for p in message:
    message_bytes += p.to_bytes(8, "big")

message_2 = segment_into_chunks(get_bit_array(list(message_bytes)), 64)
signature = private_key.sign_digest(message_bytes)
order_size = private_key.curve.order.bit_length() // 8
r, s = ecdsa.util.sigdecode_string(signature, private_key.curve.order)


r_array = int_to_array(64, 4, r)
s_array = int_to_array(64, 4, s)

r_bytes = r.to_bytes(order_size, byteorder="big")
s_bytes = s.to_bytes(order_size, byteorder="big")
r_bits = get_bit_array(r_bytes)
s_bits = get_bit_array(s_bytes)


verify_signature(message_bytes, signature, public_key_hex)


verify()
