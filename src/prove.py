import os, json
import sys

# Add the path to project_root
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(project_root)
from web3 import Web3
import rlp
from mpt import mpt_last
from mpt import mpt_path
from dotenv import load_dotenv
dotenv_path = os.path.join(project_root, '.env')
load_dotenv(dotenv_path)




def verify_proof(proof, block, ECDS_commitment, salt):
    rev_proof = proof.accountProof[::-1]
    layers = []
    account_rlp = rlp.encode(
        [proof.nonce, proof.balance, proof.storageHash, proof.codeHash]
    )
    address_bytes = bytes.fromhex(str(proof.address)[2:])
    prefix_account_rlp = proof.accountProof[-1][: -len(account_rlp)]

    last_proof, last_proof_upper_commit = mpt_last.get_last_proof(
        salt,
        address_bytes,
        bytes(prefix_account_rlp),
        proof.nonce,
        proof.balance,
        proof.storageHash,
        proof.codeHash,
        ECDS_commitment
    )
    layers.append(last_proof_upper_commit)
    root_proof = None
    path_proofs = []

    for index, level in enumerate(rev_proof):
        if index == len(rev_proof) - 1:
            if Web3.keccak(level) != block.stateRoot:
                raise Exception("Not verified!")
            root_proof, _ = mpt_path.get_mpt_path_proof(
                salt, level, block.stateRoot, True
            )
        else:
            if Web3.keccak(level) not in rev_proof[index + 1]:
                raise Exception("Not verified!")
            mpt_path_proof, mpt_path_upper_commit = mpt_path.get_mpt_path_proof(
                salt, level, rev_proof[index + 1], False
            )
            path_proofs.append(mpt_path_proof)
            layers.append(mpt_path_upper_commit)



    if Web3.keccak(prefix_account_rlp + account_rlp) not in proof.accountProof[-2]:
        raise Exception("Not verified!")

    return account_rlp, address_bytes, prefix_account_rlp


# def print_results(proof, expected_account_rlp, result):
#     print("balance", proof.balance)
#     print("nonce", proof.nonce)
#     print("storage hash", list(proof.storageHash))
#     print("code hash", list(proof.codeHash))

#     print("===================================")

#     print("Expected len", len(expected_account_rlp))
#     print("Expected result", list(expected_account_rlp))

#     print("===================================")

#     print("Hex expected result", bytes(list(expected_account_rlp)).hex())
#     print("Hex circuit result", bytes(result[3:]).hex())

#     print("===================================")

#     print("Circuit result len", result[2])
#     print("Circuit result", result[3 : result[2] + 3])

#     print("===================================")

#     print("Equality", result[3 : result[2] + 3] == list(expected_account_rlp))

#     print(result[:2])


def get_account_eth_mpt_proof(account, provider, index, salt):
    ECDS_commitment = get_ECDSA_ommitment(index)
    # import ipdb; ipdb.set_trace()
    w3 = Web3(Web3.HTTPProvider(provider))

    num = w3.eth.get_block_number()
    print("generating proof for block number: ", num)

    block = w3.eth.get_block(num)
    proof = w3.eth.get_proof(account, [], num)

    account_rlp, address_bytes, prefix_account_rlp = verify_proof(proof, block, ECDS_commitment, salt)
    
    result = mpt_last.get_last_proof(
        salt,
        address_bytes,
        bytes(prefix_account_rlp),
        proof.nonce,
        proof.balance,
        proof.storageHash,
        proof.codeHash,
        ECDS_commitment
    )

    # print_results(proof, account_rlp, result)

def get_ECDSA_ommitment(accounts_index):
    
    output_file = f"circuit/temp/ecdsa_verify/output_ecdsa_verify_{accounts_index}.json"
    if os.path.exists(output_file) :
            with open(output_file, 'r') as f:
                commitment = json.load(f)
    else:
        raise Exception("ERROR: ECDSA commitment is not generated. ")
    return commitment[1]

print("OK!")
