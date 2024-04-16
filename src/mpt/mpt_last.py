import json, io
import os

security = 20
maxBlocks = 4
maxLowerLen = 99
maxPrefixLen = maxBlocks * 136 - maxLowerLen


def get_last_proof(
    salt, addressBytes, lowerLayerPrefix, nonce, balance, storageHash, codeHash, ECDS_commitment
):
    lowerLayerPrefixLen = len(lowerLayerPrefix)
    lowerLayerPrefix += (maxPrefixLen - len(lowerLayerPrefix)) * b"\x00"
    
    with io.open("circuit/temp/mpt_last/input_mpt_last.json", "w") as f:

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
                "ECDSACommitmentHash": ECDS_commitment
            },
            f,
        )

    os.system(
        "make gen_mpt_last_witness"
    )


    with io.open("circuit/temp/mpt_last/output_mpt_last.json", "r") as f:
        data = json.load(f)
        return [data[0], data[1]]
            

