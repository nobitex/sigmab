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
    lowerLayer = keccak_bits(lower)
    upperLayer = keccak_bits(upper)

    numLowerLayerBlocks = len(lowerLayer) // (136 * 8)
    numUpperLayerBlocks = len(upperLayer) // (136 * 8)
    lowerLayer += (MAX_BLOCKS * 8 * 136 - len(lowerLayer)) * [0]
    upperLayer += (MAX_BLOCKS * 8 * 136 - len(upperLayer)) * [0]

    with io.open("circuit/input.json", "w") as f:
        json.dump(
            {
                "salt": salt,
                "numLowerLayerBlocks": numLowerLayerBlocks,
                "numUpperLayerBlocks": numUpperLayerBlocks,
                "lowerLayer": lowerLayer,
                "upperLayer": upperLayer,
            },
            f,
        )

    os.system(
        "cd circuit/mpt_path_cpp && ./mpt_path ../input.json ../mpt_path_witness.wtns"
    )
    with io.open("circuit/mpt_path_cpp/output.json", "r") as f:
        return f.read()
