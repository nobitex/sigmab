import json, io
import os

security = 20
maxBlocks = 4
maxLowerLen = 256
maxPrefixLen = maxBlocks * 136 - maxLowerLen


def get_last_proof(salt, addressBytes, lowerLayerPrefix, lowerLayer):
    lowerLayerLen = len(lowerLayer)
    lowerLayerPrefixLen = len(lowerLayerPrefix)

    lowerLayer += (maxLowerLen - len(lowerLayer)) * b"\x00"
    lowerLayerPrefix += (maxPrefixLen - len(lowerLayerPrefix)) * b"\x00"

    with io.open("circuit/input.json", "w") as f:
        json.dump(
            {
                "salt": salt,
                "address": list(addressBytes),
                "lowerLayer": list(lowerLayer),
                "lowerLayerLen": lowerLayerLen,
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
