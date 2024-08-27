from circuits import AbstractCircuit
from eth_keys import keys
from eth_utils import keccak, encode_hex
from ecdsa import VerifyingKey, SECP256k1, util
from web3 import Web3
from eth_account.messages import encode_defunct, _hash_eip191_message
import hashlib
import base64


class ECDSACircuit(AbstractCircuit):
    def _generate_witness(self, msg_hash, r, s, pubkey, salt):
        return super().generate_witness(
            msghash=msg_hash, r=r, s=s, pubkey=pubkey, salt=salt
        )

    def generate_witness(self, message, public_key, signature_r, signature_s, salt):
        eth_encoded_msg = message.encode("utf-8")
        message_hash = hashlib.sha256(eth_encoded_msg).digest()
        message_hash_hex = Web3.to_hex(message_hash)
        signable = encode_defunct(hexstr=message_hash_hex)
        hashed = _hash_eip191_message(signable)
        msg = int.from_bytes(hashed, "big")

        public_key = base64.b64decode(public_key.encode("utf-8"))
        vk = VerifyingKey.from_string(public_key, curve=SECP256k1)
        pubkey = vk.pubkey.point

        def b2a(n, k, x):
            mod = 2**n
            ret = []
            for _ in range(k):
                ret.append(str(x % mod))
                x = x // mod
            return ret

        r = b2a(64, 4, signature_r)
        s = b2a(64, 4, signature_s)
        msg_hash = b2a(64, 4, msg)
        pub0 = b2a(64, 4, pubkey.x())
        pub1 = b2a(64, 4, pubkey.y())

        return self._generate_witness(msg_hash, r, s, [pub0, pub1], salt)
