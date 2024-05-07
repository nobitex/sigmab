from circuits import AbstractCircuit
import rlp


class MPTLastCircuit(AbstractCircuit):
    MAX_BLOCKS = 4
    MAX_LOWER_LENGTH = 99
    MAX_PREFIX_LENGTH = MAX_BLOCKS * 136 - MAX_LOWER_LENGTH

    def generate_witness(self, exchange_account, block, ecdsa_commitment, salt):
        proof = exchange_account.get_value("account_proof")
        rev_proof = proof.accountProof[::-1]
        layers = []
        account_rlp = rlp.encode(
            [proof.nonce, proof.balance, proof.storageHash, proof.codeHash]
        )
        address_bytes = bytes.fromhex(str(proof.address)[2:])
        prefix_account_rlp = proof.accountProof[-1][: -len(account_rlp)]

        return self._generate_witness(
            salt,
            address_bytes,
            bytes(prefix_account_rlp),
            proof.nonce,
            proof.balance,
            proof.storageHash,
            proof.codeHash,
            ecdsa_commitment,
        )

    def _generate_witness(
        self,
        salt,
        addressBytes,
        lowerLayerPrefix,
        nonce,
        balance,
        storageHash,
        codeHash,
        ecdsa_commitment,
    ):
        lowerLayerPrefixLen = len(lowerLayerPrefix)
        lowerLayerPrefix += (self.MAX_PREFIX_LENGTH - len(lowerLayerPrefix)) * b"\x00"

        return super().generate_witness(
            salt=salt,
            address=list(addressBytes),
            nonce=str(nonce),
            balance=str(balance),
            storageHash=list(storageHash),
            codeHash=list(codeHash),
            lowerLayerPrefix=list(lowerLayerPrefix),
            lowerLayerPrefixLen=lowerLayerPrefixLen,
            ECDSACommitmentHash=ecdsa_commitment,
        )
