import json, io
import os

security = 20
maxBlocks = 4
maxLowerLen = 99
maxPrefixLen = maxBlocks * 136 - maxLowerLen


def get_last_proof(
    salt, addressBytes, lowerLayerPrefix, nonce, balance, storageHash, codeHash
):
    lowerLayerPrefixLen = len(lowerLayerPrefix)
    lowerLayerPrefix += (maxPrefixLen - len(lowerLayerPrefix)) * b"\x00"

    with io.open("/tmp/input_mpt_last.json", "w") as f:
        json.dump(
            {
                "salt": salt,
                "address": list(addressBytes),
                "nonce": str(nonce),
                "balance": str(balance),
                "storageHash": list(storageHash),
                "codeHash": list(codeHash),
                "lowerLayerPrefix": list(lowerLayerPrefix),
                "lowerLayerPrefixLen": lowerLayerPrefixLen,
            },
            f,
        )

    os.system(
        "make gen_mpt_last_witness"
    )

    with io.open("/tmp/output_mpt_last.json", "r") as f:
        return [int(s) for s in json.loads(f.read())]
