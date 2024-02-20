import json, io
import os

security = 20
maxBlocks = 4
maxLowerLen = 79
maxPrefixLen = maxBlocks * 136 - maxLowerLen


def get_last_proof(
    salt, addressBytes, lowerLayerPrefix, nonce, balance, storageHash, codeHash
):
    lowerLayerPrefixLen = len(lowerLayerPrefix)
    lowerLayerPrefix += (maxPrefixLen - len(lowerLayerPrefix)) * b"\x00"

    with io.open("circuit/input.json", "w") as f:
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
        "cd circuit/mpt_last_cpp && ./mpt_last ../input.json ../mpt_last_witness.wtns"
    )

    with io.open("circuit/mpt_last_cpp/output.json", "r") as f:
        return [int(s) for s in json.loads(f.read())]
