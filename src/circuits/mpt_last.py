from circuits import AbstractCircuit


class MPTLastCircuit(AbstractCircuit):
    MAX_BLOCKS = 4
    MAX_LOWER_LENGTH = 99
    MAX_PREFIX_LENGTH = MAX_BLOCKS * 136 - MAX_LOWER_LENGTH

    def generate_witness(
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
