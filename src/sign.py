import ecdsa, io, json, hashlib
from ecdsa import VerifyingKey, SECP256k1, util
from eth_keys import keys


def int_to_big_endian(x, length=32):
    return x.to_bytes(length, byteorder="big")


def string_to_int(string):
    # byte = string.encode("utf-8")
    return int.from_bytes(string, "big")


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


def sign_message_with_sha256(private_key_hex, message):

    # Convert the message to bytes if it's not already
    if not isinstance(message, bytes):
        message = message.encode("utf-8")

    message_hash = hashlib.sha256(message).digest()

    private_key_bytes = bytes.fromhex(private_key_hex)

    # Create an account object from the private key
    sk = ecdsa.SigningKey.from_string(private_key_bytes, curve=ecdsa.SECP256k1)

    # Sign the hash directly using the eth_keys library
    signature = sk.sign_digest(message_hash)

    return signature


def recover_raw_public_key(message, signature):
    signature_bytes = signature

    # Reconstruct the signature object with correct 'v' value
    sig = keys.Signature(
        vrs=(
            1,
            int.from_bytes(signature_bytes[:32], "big"),
            int.from_bytes(signature_bytes[32:64], "big"),
        )
    )

    # Encode the message
    if not isinstance(message, bytes):
        message = message.encode("utf-8")

    # Hash the message using sha-256
    message_hash = hashlib.sha256(message).digest()

    # Recover the public key
    public_key = sig.recover_public_key_from_msg_hash(message_hash)
    uncompressed_public_key_bytes = b"\x04" + public_key.to_bytes()
    uncompressed_public_key_hex = uncompressed_public_key_bytes.hex()

    return uncompressed_public_key_hex, public_key, sig, uncompressed_public_key_bytes


def verify_signature(message, signature, pub):
    # Verify the signature
    if not isinstance(message, bytes):
        message = message.encode("utf-8")

    # Hash the message using Keccak-256
    message_hash = hashlib.sha256(message).digest()
    is_valid = pub.verify_msg_hash(message_hash, signature)

    print("Pub verify_msg_hash: Signature is valid", is_valid)


def verify_signature_using_ecdsa(message, signature, pub):
    # Load the public key
    vk = VerifyingKey.from_string(pub, curve=SECP256k1)
    # Verify the signature
    message = message.encode("utf-8")
    message_hash = hashlib.sha256(message).digest()
    signature_bytes = signature

    try:
        is_valid = vk.verify_digest(
            signature_bytes,
            message_hash,
        )
        print(
            "ECDSA: Signature is valid!"
            if is_valid
            else "Signature verification failed."
        )
    except ecdsa.BadSignatureError:
        print("Bad Signature, Signature verification failed.")


def checkECDSA(message, public_key, signature):
    eth_encoded_msg = message.encode("utf-8")
    message_hash = hashlib.sha256(eth_encoded_msg).digest()
    msg = string_to_int(message_hash)

    vk = VerifyingKey.from_string(bytes.fromhex(public_key), curve=SECP256k1)
    pubkey = vk.pubkey.point
    curve_order = SECP256k1.order
    r, s = util.sigdecode_string(signature, curve_order)

    # Convert values
    r_array = bigint_to_array(64, 4, r)
    s_array = bigint_to_array(64, 4, s)
    msghash_array = bigint_to_array(64, 4, msg)
    pub0_array = bigint_to_array(64, 4, pubkey.x())
    pub1_array = bigint_to_array(64, 4, pubkey.y())

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


# Example usage
private_key_hex = "80711e79125489fe9c245784d6fe6fcbfe4eb57975d7b2add5f27048a7904b62"
message = "Hello, Ethereum!"
# Sign the message
signed_message = sign_message_with_sha256(private_key_hex, message)
print("Signed Message:", signed_message)

# Now recover the public key
uncompressed_public_key_hex, public_key, sig, uncompressed_public_key_bytes = (
    recover_raw_public_key(message, signed_message)
)
print("Recovered Public Key (Address):", uncompressed_public_key_hex)

verify_signature(message, sig, public_key)
verify_signature_using_ecdsa(message, signed_message, uncompressed_public_key_bytes)

checkECDSA(message, uncompressed_public_key_hex, signed_message)
