from circuits import AbstractCircuit
from eth_keys import keys
from eth_utils import keccak, encode_hex
from ecdsa import VerifyingKey, SECP256k1, util
import hashlib


class ECDSACircuit(AbstractCircuit):

    def _generate_witness(self, msg_hash, r, s, pubkey, salt):
        return super().generate_witness(
            msghash=msg_hash, r=r, s=s, pubkey=pubkey, salt=salt
        )

    def generate_witness(self, message, public_key, signature, salt):
        msg_hash = hashlib.sha256(message.encode("utf-8")).digest()        
        msg_hash = int.from_bytes(msg_hash, "big")

        vk = VerifyingKey.from_string(bytes.fromhex(public_key), curve=SECP256k1)
        pubkey = vk.pubkey.point
        curve_order = SECP256k1.order
        r, s = util.sigdecode_string(signature, curve_order)

        def b2a(n, k, x):
            mod = 2**n
            ret = []
            for _ in range(k):
                ret.append(str(x % mod))
                x = x // mod
            return ret

        r = b2a(64, 4, r)
        s = b2a(64, 4, s)
        msg_hash = b2a(64, 4, msg_hash)
        pub0 = b2a(64, 4, pubkey.x())
        pub1 = b2a(64, 4, pubkey.y())

        return self._generate_witness(msg_hash, r, s, [pub0, pub1], salt)
