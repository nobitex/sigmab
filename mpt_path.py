import json
import os
import io


def get_mpt_path_proof(salt, lower, upper):
    MAX_BLOCKS = 4
    numLowerLayerBytes = len(lower)
    numUpperLayerBytes = len(upper)
    lowerLayer = list(lower) + (MAX_BLOCKS * 136 - len(lower)) * [0]
    upperLayer = list(upper) + (MAX_BLOCKS * 136 - len(upper)) * [0]

    with io.open("circuit/input.json", "w") as f:
        json.dump(
            {
                "salt": salt,
                "numLowerLayerBytes": numLowerLayerBytes,
                "numUpperLayerBytes": numUpperLayerBytes,
                "lowerLayerBytes": lowerLayer,
                "upperLayerBytes": upperLayer,
            },
            f,
        )

    os.system(
        "cd circuit/mpt_path_cpp && ./mpt_path ../input.json ../mpt_path_witness.wtns"
    )
    with io.open("circuit/mpt_path_cpp/output.json", "r") as f:
        return f.read()
