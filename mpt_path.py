import json
import os
import io


def to_binary(inp):
    bits = []
    for ch in inp:
        for _ in range(8):
            bits.append(ch % 2)
            ch = ch // 2
    return bits


def keccak_bits(block):
    bits = to_binary(block)

    # Padding
    if len(bits) % (8 * 136) != 0:
        bits.append(1)
        while len(bits) % (8 * 136) != 8 * 136 - 1:
            bits.append(0)
        bits.append(1)

    return bits


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
