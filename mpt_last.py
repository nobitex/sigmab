import json, io
import os
maxPrefixLen = 64
maxLowerLen = 128

def get_last_proof(salt, lowerLayerPrefix, lowerLayer):
    lowerLayerPrefixLen = len(lowerLayerPrefix)
    lowerLayerLen = len(lowerLayer)

    lowerLayerPrefix = lowerLayerPrefix + [0] * (maxPrefixLen - lowerLayerPrefixLen)
    lowerLayer = lowerLayer + [0] * (maxLowerLen - lowerLayerLen)

    with io.open('circuit/input.json', 'w') as f:
        json.dump({
            "salt": salt,
            "lowerLayer": lowerLayer,
            "lowerLayerLen": lowerLayerLen,
            "lowerLayerPrefix": lowerLayerPrefix,
            "lowerLayerPrefixLen": lowerLayerPrefixLen,
        }, f)
    
    os.system('cd circuit/mpt_last_cpp && ./mpt_last ../input.json ../mpt_last_witness.wtns')

    with io.open('circuit/mpt_last_cpp/output.json', 'r') as f:
        return f.read()
