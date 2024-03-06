import os
import sys
# Add the path to project_root
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)
from web3 import Web3
import rlp
import mpt_last
import mpt_path

SALT = 123


def verify_proof(proof, block):
    for index, level in enumerate(proof.accountProof):
        if index == 0:
            if Web3.keccak(level) != block.stateRoot:
                raise Exception("Not verified!")
        if index >= 1:
            if Web3.keccak(level) not in proof.accountProof[index - 1]:
                raise Exception("Not verified!")
            print(
                mpt_path.get_mpt_path_proof(SALT, level, proof.accountProof[index - 1])
            )

    account_rlp = rlp.encode(
        [proof.nonce, proof.balance, proof.storageHash, proof.codeHash]
    )
    address_bytes = bytes.fromhex(str(proof.address)[2:])
    prefix_account_rlp = proof.accountProof[-1][: -len(account_rlp)]

    if Web3.keccak(prefix_account_rlp + account_rlp) not in proof.accountProof[-2]:
        raise Exception("Not verified!")

    return account_rlp, address_bytes, prefix_account_rlp


def print_results(proof, expected_account_rlp, result):
    print("balance", proof.balance)
    print("nonce", proof.nonce)
    print("storage hash", list(proof.storageHash))
    print("code hash", list(proof.codeHash))

    print("===================================")

    print("Expected len", len(expected_account_rlp))
    print("Expected result", list(expected_account_rlp))

    print("===================================")

    print("Hex expected result", bytes(list(expected_account_rlp)).hex())
    print("Hex circuit result", bytes(result[3:]).hex())

    print("===================================")

    print("Circuit result len", result[2])
    print("Circuit result", result[3 : result[2] + 3])

    print("===================================")

    print("Equality", result[3 : result[2] + 3] == list(expected_account_rlp))

    print(result[:2])


def get_account_eth_mpt_proof(account, provider):
    # import ipdb; ipdb.set_trace()
    w3 = Web3(Web3.HTTPProvider(provider))

    num = w3.eth.get_block_number()

    block = w3.eth.get_block(num)
    proof = w3.eth.get_proof(account, [], num)

    account_rlp, address_bytes, prefix_account_rlp = verify_proof(proof, block)

    result = mpt_last.get_last_proof(
        SALT,
        address_bytes,
        bytes(prefix_account_rlp),
        proof.nonce,
        proof.balance,
        proof.storageHash,
        proof.codeHash,
    )

    print_results(proof, account_rlp, result)


get_account_eth_mpt_proof(
    "0x71C7656EC7ab88b098defB751B7401B5f6d8976F",
    "https://yolo-shy-fog.discover.quiknode.pro/97f7aeb00bc7a8d80c3d4834a16cd9c86b54b552/",
)
print("OK!")
