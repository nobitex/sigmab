import json
import os
import io


def get_mpt_path_proof(salt, lower, upper):
    MAX_BLOCKS = 4
    numLowerLayerBytes = len(lower)
    numUpperLayerBytes = len(upper)
    lowerLayer = list(lower) + (MAX_BLOCKS * 136 - len(lower)) * [0]
    upperLayer = list(upper) + (MAX_BLOCKS * 136 - len(upper)) * [0]

    with io.open("/tmp/input_mpt_path.json", "w") as f:
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
        "make gen_mpt_path_witness"
    )
    with io.open("/tmp/output_mpt_path.json", "r") as f:
        return f.read()
