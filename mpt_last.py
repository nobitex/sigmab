import json, io
import os

maxPrefixLen = 64
maxLowerLen = 256


def get_last_proof(salt, lowerLayerPrefix, lowerLayer):
    lowerLayerPrefixLen = len(lowerLayerPrefix)
    lowerLayerPrefix = lowerLayerPrefix + b"\x00" * (maxPrefixLen - lowerLayerPrefixLen)

    lowerLayer += (
        b"\x80" + b"\x00" * (270 - len(lowerLayerPrefix + lowerLayer)) + b"\x01"
    )
    lowerLayerLen = len(lowerLayer)

    lowerLayer += (maxLowerLen - len(lowerLayer)) * b"\x00"
    lowerLayerPrefix += (maxPrefixLen - len(lowerLayerPrefix)) * b"\x00"

    with io.open("circuit/input.json", "w") as f:
        json.dump(
            {
                "salt": salt,
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
        return f.read()
