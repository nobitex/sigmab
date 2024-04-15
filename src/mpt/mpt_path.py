import json
import os
import io


def get_mpt_path_proof(salt, lower, upper, is_top):
    MAX_BLOCKS = 4
    numLowerLayerBytes = len(lower)
    numUpperLayerBytes = len(upper)
    lowerLayer = list(lower) + (MAX_BLOCKS * 136 - len(lower)) * [0]
    upperLayer = list(upper) + (MAX_BLOCKS * 136 - len(upper)) * [0]

    with io.open("circuit/temp/mpt_path/input_mpt_path.json", "w") as f:
        json.dump(
            {
                "salt": str(salt),
                "numLowerLayerBytes": numLowerLayerBytes,
                "numUpperLayerBytes": 1 if is_top else numUpperLayerBytes,
                "lowerLayerBytes": lowerLayer,
                "upperLayerBytes": [0] * MAX_BLOCKS * 136 if is_top else upperLayer,
                "isTop": 1 if is_top else 0,
            },
            f,
        )

    os.system("make gen_mpt_path_witness")
    with io.open("circuit/temp/mpt_path/output_mpt_path.json", "r") as f:
        data = json.load(f)
        return [data[0], data[1]]
