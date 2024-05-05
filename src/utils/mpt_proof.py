import os
import sys
import io, json

# Add the path to project_root
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(project_root)
from web3 import Web3
import rlp
from mpt import mpt_last
from mpt import mpt_path

# from prove import get_account_eth_mpt_proof
from utils.ecdsa_proof import get_ECDSA_ommitment

provider = "https://yolo-shy-fog.discover.quiknode.pro/97f7aeb00bc7a8d80c3d4834a16cd9c86b54b552/"


def verify_proof(proof, block, ECDS_commitment, salt, account_index):
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
        ECDS_commitment,
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

        os.rename(
            "circuit/temp/mpt_path/input_mpt_path.json",
            f"circuit/temp/mpt_path/input_mpt_path_{account_index}_{index}.json",
        )
        os.rename(
            "circuit/temp/mpt_path/output_mpt_path.json",
            f"circuit/temp/mpt_path/output_mpt_path_{account_index}_{index}.json",
        )
        os.rename(
            "circuit/temp/mpt_path/mpt_path_witness.wtns",
            f"circuit/temp/mpt_path/mpt_path_witness_{account_index}_{index}.wtns",
        )

    if Web3.keccak(prefix_account_rlp + account_rlp) not in proof.accountProof[-2]:
        raise Exception("Not verified!")

    return account_rlp, address_bytes, prefix_account_rlp, len(rev_proof)


def gen_account_eth_mpt_proof(account, provider, index, salt):
    ECDS_commitment = get_ECDSA_ommitment(index)
    w3 = Web3(Web3.HTTPProvider(provider))

    num = w3.eth.get_block_number()
    block = w3.eth.get_block(num)
    proof = w3.eth.get_proof(account, [], num)

    (_, _, _, l) = verify_proof(proof, block, ECDS_commitment, salt, index)
    return l


def generate_mpt_cicuit_inputs(account_address, counter, salt):
    """
    Generates the inputs for mpt last and mpt path circuit and saves them in coresponding files in circuit/temp.

    Args:
        signature_data: the list of company addresses,
        counter: the number used as iterator.
    """
    l = gen_account_eth_mpt_proof(account_address, provider, counter, salt)
    # rename mpt_last files according to the counter
    os.rename(
        "circuit/temp/mpt_last/input_mpt_last.json",
        f"circuit/temp/mpt_last/input_mpt_last_{counter}.json",
    )
    os.rename(
        "circuit/temp/mpt_last/output_mpt_last.json",
        f"circuit/temp/mpt_last/output_mpt_last_{counter}.json",
    )
    os.rename(
        "circuit/temp/mpt_last/mpt_last_witness.wtns",
        f"circuit/temp/mpt_last/mpt_last_witness_{counter}.wtns",
    )
    return l


def generate_proof(counter, proof_length):
    """
    Generates the proof and public inputs and output for mpt_last an mpt_path circuit and saves them in the circuit/temp path.

    Args:
        counter: the number used as iterator.
    """
    print("Generating proof and verification for the account number:", counter)
    # mpt_last
    os.rename(
        f"circuit/temp/mpt_last/mpt_last_witness_{counter}.wtns",
        "circuit/temp/mpt_last/mpt_last_witness.wtns",
    )
    os.system("make gen_mpt_last_proof")
    os.system("make verify_mpt_last_proof")
    os.rename(
        "circuit/temp/mpt_last/mpt_last_proof.json",
        f"circuit/temp/mpt_last/mpt_last_proof_{counter}.json",
    )
    os.rename(
        "circuit/temp/mpt_last/mpt_last_public.json",
        f"circuit/temp/mpt_last/mpt_last_public_{counter}.json",
    )

    # mpt_path
    for i in range(proof_length):
        os.rename(
            f"circuit/temp/mpt_path/mpt_path_witness_{counter}_{i}.wtns",
            "circuit/temp/mpt_path/mpt_path_witness.wtns",
        )
        os.system("make gen_mpt_path_proof")
        os.system("make verify_mpt_path_proof")
        os.rename(
            "circuit/temp/mpt_path/mpt_path_proof.json",
            f"circuit/temp/mpt_path/mpt_path_proof_{counter}_{i}.json",
        )
        os.rename(
            "circuit/temp/mpt_path/mpt_path_public.json",
            f"circuit/temp/mpt_path/mpt_path_public_{counter}_{i}.json",
        )


def combine_mpt_last_files(counter):
    """
    Generates the proof data to be verified by groth16.verify function in extention.

    Args:
        counter: the proof counts used as iterator.
    """
    with open("circuit/temp/mpt_last/verification_key.json", "r") as f:
        vk_data = json.load(f)

    # Combine data from proof_n.json and pub_n.json files
    mpt_last_proofs = {"vk": vk_data, "proofs": []}
    for i in range(counter):
        proof_file = f"circuit/temp/mpt_last/mpt_last_proof_{i}.json"
        pub_file = f"circuit/temp/mpt_last/mpt_last_public_{i}.json"

        if os.path.exists(proof_file) and os.path.exists(pub_file):
            with open(proof_file, "r") as f:
                proof_data = json.load(f)
            with open(pub_file, "r") as f:
                pub_data = json.load(f)

            mpt_last_proofs["proofs"].append({"proof": proof_data, "pub": pub_data})

    # Write combined data to a new JSON file
    with open("data/mpt_last_proofs.json", "w") as f:
        json.dump(mpt_last_proofs, f, indent=4)


def combine_mpt_path_files(counter, proof_length):
    """
    Generates the proof data to be verified by groth16.verify function in extention.

    Args:
        counter: the proof counts used as iterator.
    """
    with open("circuit/temp/mpt_path/verification_key.json", "r") as f:
        vk_data = json.load(f)

    # Combine data from proof_n.json and pub_n.json files
    mpt_path_proofs = {"vk": vk_data, "proofs": []}
    for i in range(counter):
        account_proofs = []
        for j in range(proof_length):
            proof_file = f"circuit/temp/mpt_path/mpt_path_proof_{i}_{j}.json"
            pub_file = f"circuit/temp/mpt_path/mpt_path_public_{i}_{j}.json"

            if os.path.exists(proof_file) and os.path.exists(pub_file):
                with open(proof_file, "r") as f:
                    proof_data = json.load(f)
                with open(pub_file, "r") as f:
                    pub_data = json.load(f)
            account_proofs.append({"proof": proof_data, "pub": pub_data})    

        mpt_path_proofs["proofs"].append(account_proofs)

    # Write combined data to a new JSON file
    with open("data/mpt_path_proofs.json", "w") as f:
        json.dump(mpt_path_proofs, f, indent=4)


def generate_mpt_proof_data(address_list, salt):
    """
    Generates the cicuit inputs the witness, the output files, the proof, and the public arguments for mpt circuits.

    Args:
        address_list: the list of company addresses.
    """
    accounts_count = len(address_list)
    for i in range(accounts_count):
        proof_length = generate_mpt_cicuit_inputs(address_list[i], i, salt)
        generate_proof(i, proof_length)
    combine_mpt_last_files(accounts_count)
    combine_mpt_path_files(accounts_count, proof_length)
    print("proof json file generated successfully.")
