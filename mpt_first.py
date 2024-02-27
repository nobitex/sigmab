from web3 import Web3
import rlp
import json
import os
import io

maxBlocks = 5
KeccakSize = 136
SplitSize = int(KeccakSize / 8)
maxPrefixLen = maxBlocks * SplitSize * 2
maxPostfixLen = maxBlocks * SplitSize * 6 - 50
maxCommitTopLen = 50

def get_mpt_first_proof(block):
    hashes = [
        block.parentHash.hex(),
        block.sha3Uncles.hex(),
        block.miner,
        block.stateRoot.hex(),
        block.transactionsRoot.hex(),
        block.receiptsRoot.hex(),
        block.logsBloom.hex(),
        hex(block.difficulty),
        hex(block.number),
        hex(block.gasLimit),
        hex(block.gasUsed),
        hex(block.timestamp),
        block.extraData.hex(),
        block.mixHash.hex(),
        block.nonce.hex(),
        hex(block.baseFeePerGas),
        block.withdrawalsRoot.hex(),
    ]
    hashes = ["0x" if h == "0x0" else h for h in hashes]
    header = rlp.encode([Web3.to_bytes(hexstr=h) for h in hashes])

    start_idx = header.index(bytes(block.stateRoot))
    end_idx = start_idx + len(bytes(block.stateRoot))
    prefix = header[:start_idx]
    postfix = header[end_idx:]
    commit_top = header[start_idx:end_idx]

    with open("/tmp/input_mpt_first.json", "w") as f:
        json.dump(
            {
                "numPrefixBytes": len(prefix),
                "prefixBytes": list(prefix + (maxPrefixLen - len(prefix)) * b"\x00"),

                "numPostfixBytes": len(postfix),
                "postfixBytes": list(postfix + (maxPostfixLen - len(postfix)) * b"\x00"),

                "numCommitTopBytes": len(commit_top),
                "commitTopBytes": list(commit_top + (maxCommitTopLen - len(commit_top)) * b"\x00"),
            },
            f,
        )

    os.system(
        "make gen_mpt_first_witness"
    )

    with io.open("/tmp/output_mpt_first.json", "r") as f:
        return f.read()
