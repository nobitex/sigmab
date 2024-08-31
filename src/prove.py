from circuits import (
    MPTLastCircuit,
    MPTPathCircuit,
    ECDSACircuit,
    SBACircuit,
    POLCircuit,
    ContextKeys,
)
from config import *
from utils import (
    load_solvency_data,
    load_liability_data,
    build_liability_nodes,
    build_liability_tree,
)

from web3 import Web3
import tqdm
import random
import json


def main():
    salt = random.randint(0, 10**5)
    message, exchange_accounts_data = load_solvency_data("data/solvency_data.json")
    solveny_counts = len(exchange_accounts_data)
    mpt_last_circuit = get_mpt_last_circuit(
        witness_gen_path=MPT_LAST_WITNESS_GEN_PATH,
        prover_path=PROVER_PATH,
        snarkjs_path=SNARKJS_PATH,
        zk_params_path=MPT_LAST_ZK_PARAMS_PATH,
    )

    mpt_path_circuit = get_mpt_path_circuit(
        witness_gen_path=MPT_PATH_WITNESS_GEN_PATH,
        prover_path=PROVER_PATH,
        snarkjs_path=SNARKJS_PATH,
        zk_params_path=MPT_PATH_ZK_PARAMS_PATH,
    )

    ecdsa_circuit = get_ecdsa_circuit(
        witness_gen_path=ECDSA_WITNESS_GEN_PATH,
        prover_path=PROVER_PATH,
        snarkjs_path=SNARKJS_PATH,
        zk_params_path=ECDSA_ZK_PARAMS_PATH,
    )

    if solveny_counts > 1:
        sba_circuit = get_sba_circuit(
            witness_gen_path=SBA_WITNESS_GEN_PATH,
            prover_path=PROVER_PATH,
            snarkjs_path=SNARKJS_PATH,
            zk_params_path=SBA_ZK_PARAMS_PATH,
        )
    elif solveny_counts == 1:
        print("the SBA circuit is bypassed.")
    else:
        print("Insufficient data to generate SBA proof.")

    pol_circuit = get_pol_circuit(
        witness_gen_path=POL_WITNESS_GEN_PATH,
        prover_path=PROVER_PATH,
        snarkjs_path=SNARKJS_PATH,
        zk_params_path=POL_ZK_PARAMS_PATH,
    )

    ### ECDSA Proof Generation
    ecdsa_progress = tqdm.tqdm(
        exchange_accounts_data, total=len(exchange_accounts_data), desc="ECDSA Progress"
    )
    for exchange_account in ecdsa_progress:
        witness_path = ecdsa_circuit.generate_witness(
            message,
            exchange_account.pubkey,
            exchange_account.signature_r,
            exchange_account.signature_s,
            salt,
        )
        proof_path = ecdsa_circuit.prove(witness_path)

        exchange_account.set_value("ecdsa_witness_path", witness_path)
        exchange_account.set_value("ecdsa_proof_path", proof_path)
        exchange_account.set_value(
            "ecdsa_public_outputs",
            ecdsa_circuit.context.get(ContextKeys.LATEST_PUBLIC_VALUES),
        )

        ecdsa_progress.write(f"Generated proof for account: {exchange_account.address}")
        ecdsa_progress.write(f"Proof path: {proof_path}")

    ### MPT Proof Generation
    provider = Web3(Web3.HTTPProvider(PROVIDER))
    block_number = provider.eth.get_block_number()
    block = provider.eth.get_block(block_number)

    mpt_proof_progress = tqdm.tqdm(
        exchange_accounts_data,
        total=len(exchange_accounts_data),
        desc="MPT Proof Progress",
    )
    for exchange_account in mpt_proof_progress:
        account_proof = provider.eth.get_proof(
            exchange_account.address, [], block_number
        )
        exchange_account.set_value("account_proof", account_proof)
        exchange_account.set_value("account_proof_block_number", block_number)
        mpt_proof_progress.write(
            f"Generated proof for account: {exchange_account.address}"
        )

        #### MPT Last Proof Generation
        witeness_path = mpt_last_circuit.generate_witness(exchange_account, block, salt)
        proof_path = mpt_last_circuit.prove(witeness_path)

        exchange_account.set_value("mpt_last_witness_path", witeness_path)
        exchange_account.set_value("mpt_last_proof_path", proof_path)
        exchange_account.set_value(
            "mpt_last_public_outputs",
            mpt_last_circuit.context.get(ContextKeys.LATEST_PUBLIC_VALUES),
        )

        mpt_proof_progress.write(
            f"Generated MPT Last proof for account: {exchange_account.address}"
        )
        mpt_proof_progress.write(f"Proof path: {proof_path}")

        #### MPT Path Proof Generation
        rev_proof = account_proof.accountProof[::-1]

        witenss_paths = []
        proof_paths = []
        public_outputs = []
        for index, level in enumerate(rev_proof):
            mpt_proof_progress.write(
                f"Generating MPT Path proof for account: {exchange_account.address} | Level: {index + 1}/{len(rev_proof)}"
            )
            if index == len(rev_proof) - 1:
                if Web3.keccak(level) != block.stateRoot:
                    raise Exception("Not verified!")
                witeness_path = mpt_path_circuit.generate_witness(
                    salt, level, block.stateRoot, True
                )
                proof_path = mpt_path_circuit.prove(witeness_path)

                witenss_paths.append(witeness_path)
                proof_paths.append(proof_path)
                public_outputs.append(
                    mpt_path_circuit.context.get(ContextKeys.LATEST_PUBLIC_VALUES)
                )
            else:
                if Web3.keccak(level) not in rev_proof[index + 1]:
                    raise Exception("Not verified!")
                witeness_path = mpt_path_circuit.generate_witness(
                    salt, level, rev_proof[index + 1], False
                )
                proof_path = mpt_path_circuit.prove(witeness_path)

                witenss_paths.append(witeness_path)
                proof_paths.append(proof_path)
                public_outputs.append(
                    mpt_path_circuit.context.get(ContextKeys.LATEST_PUBLIC_VALUES)
                )

        exchange_account.set_value("mpt_path_witness_paths", witenss_paths)
        exchange_account.set_value("mpt_path_proof_paths", proof_paths)
        exchange_account.set_value("mpt_path_public_outputs", public_outputs)

        mpt_proof_progress.write(
            f"Generated MPT Path proof for account: {exchange_account.address}"
        )
        mpt_proof_progress.write(f"Proof paths: {proof_paths}")

    ### SBA Proof Generation
    balances = [exa.get_value("balance") for exa in exchange_accounts_data]

    if solveny_counts > 1:
        progress = tqdm.tqdm(
            range(1, len(balances)), total=len(balances) - 1, desc="SBA Progress"
        )

        sba_proofs_paths = []
        sba_witness_paths = []
        sba_public_inputs = []
        for idx in progress:
            if idx == 1:
                sba_witness_path = sba_circuit.generate_witness(
                    balances[idx - 1 : idx + 1], salt
                )
                sba_proof_path = sba_circuit.prove(sba_witness_path)
            else:
                sba_witness_path = sba_circuit.generate_witness(
                    [balances[idx], sum(balances[:idx])], salt
                )
                sba_proof_path = sba_circuit.prove(sba_witness_path)

            sba_witness_paths.append(sba_witness_path)
            sba_proofs_paths.append(sba_proof_path)
            sba_public_inputs.append(
                sba_circuit.context.get(ContextKeys.LATEST_PUBLIC_VALUES)
            )

        print(f"Generated SBA proof path: {sba_proof_path}")

    ### POL Proof Generation
    sum_balances = 0
    for exchange_account in exchange_accounts_data:
        sum_balances += exchange_account.get_value("balance")

    liability_data = load_liability_data("data/liability_data.json")
    liability_nodes = build_liability_nodes(liability_data)
    liability_tree = build_liability_tree(liability_nodes, 17)

    pol_proof_progress = tqdm.tqdm(
        liability_data, total=len(liability_data), desc="POL Progress"
    )
    for idx, item in enumerate(pol_proof_progress):
        merkle_proof = liability_tree.createProof(idx, sum_balances, salt)
        witness_path = pol_circuit.generate_witness(merkle_proof)
        proof_path = pol_circuit.prove(witness_path)

        liability_data[idx].set_value("pol_witness_path", witness_path)
        liability_data[idx].set_value("pol_proof_path", proof_path)
        liability_data[idx].set_value(
            "pol_public_outputs",
            pol_circuit.context.get(ContextKeys.LATEST_PUBLIC_VALUES),
        )

        pol_proof_progress.write(f"Generated POL proof for account: {item.id}")
        pol_proof_progress.write(f"Proof path: {proof_path}")

    # Combine all the files
    data = {}

    ecdsa_data = []
    for item in exchange_accounts_data:
        ecdsa_data.append(
            {
                "witness_path": item.get_value("ecdsa_witness_path"),
                "proof_path": item.get_value("ecdsa_proof_path"),
                "proof": json.load(open(item.get_value("ecdsa_proof_path"), "r")),
                "public_outputs": item.get_value("ecdsa_public_outputs"),
            }
        )
    data["ecdsa_data"] = ecdsa_data

    mpt_path_data = []
    for item in exchange_accounts_data:
        mpt_path_data.append(
            {
                "witness_paths": item.get_value("mpt_path_witness_paths"),
                "proof_paths": item.get_value("mpt_path_proof_paths"),
                "proofs": [
                    json.load(open(path, "r"))
                    for path in item.get_value("mpt_path_proof_paths")
                ],
                "public_outputs": item.get_value("mpt_path_public_outputs"),
            }
        )
    data["mpt_path_data"] = mpt_path_data

    mpt_last_data = []
    for item in exchange_accounts_data:
        mpt_last_data.append(
            {
                "witness_path": item.get_value("mpt_last_witness_path"),
                "proof_path": item.get_value("mpt_last_proof_path"),
                "proof": json.load(open(item.get_value("mpt_last_proof_path"), "r")),
                "public_outputs": item.get_value("mpt_last_public_outputs"),
            }
        )
    data["mpt_last_data"] = mpt_last_data

    if solveny_counts > 1:
        sba_data = {
            "witness_paths": sba_witness_paths,
            "proof_paths": sba_proofs_paths,
            "proofs": [json.load(open(proof_path)) for proof_path in sba_proofs_paths],
            "public_outputs": sba_public_inputs,
        }
        data["sba_data"] = sba_data

    pol_data = []
    for idx, item in enumerate(liability_data):
        pol_data.append(
            {
                "id": item.id,
                "witenss_path": item.get_value("pol_witness_path"),
                "proof_path": item.get_value("pol_proof_path"),
                "proof": json.load(open(item.get_value("pol_proof_path"), "r")),
                "public_outputs": item.get_value("pol_public_outputs"),
            }
        )
    data["pol_data"] = pol_data

    data["block_number"] = block_number

    with open("data/proofs.json", "w") as file:
        json.dump(data, file, indent=4)

    with open("data/liability_data.json", "r") as file:
        liability_data = json.load(file)

    liability_data["sum_balances"] = sum_balances
    liability_data["salt"] = salt

    with open("data/liability_data.json", "w") as file:
        json.dump(liability_data, file, indent=4)


def get_mpt_last_circuit(witness_gen_path, prover_path, snarkjs_path, zk_params_path):
    mpt_last_circuit = MPTLastCircuit(
        witness_generator_path=witness_gen_path,
        prover_path=prover_path,
        snarkjs_path=snarkjs_path,
        zk_params_path=zk_params_path,
    )
    return mpt_last_circuit


def get_mpt_path_circuit(witness_gen_path, prover_path, snarkjs_path, zk_params_path):
    mpt_path_circuit = MPTPathCircuit(
        witness_generator_path=witness_gen_path,
        prover_path=prover_path,
        snarkjs_path=snarkjs_path,
        zk_params_path=zk_params_path,
    )
    return mpt_path_circuit


def get_ecdsa_circuit(witness_gen_path, prover_path, snarkjs_path, zk_params_path):
    ecdsa_circuit = ECDSACircuit(
        witness_generator_path=witness_gen_path,
        prover_path=prover_path,
        snarkjs_path=snarkjs_path,
        zk_params_path=zk_params_path,
    )
    return ecdsa_circuit


def get_sba_circuit(witness_gen_path, prover_path, snarkjs_path, zk_params_path):
    sba_circuit = SBACircuit(
        witness_generator_path=witness_gen_path,
        prover_path=prover_path,
        snarkjs_path=snarkjs_path,
        zk_params_path=zk_params_path,
    )
    return sba_circuit


def get_pol_circuit(witness_gen_path, prover_path, snarkjs_path, zk_params_path):
    pol_circuit = POLCircuit(
        witness_generator_path=witness_gen_path,
        prover_path=prover_path,
        snarkjs_path=snarkjs_path,
        zk_params_path=zk_params_path,
    )
    return pol_circuit


if __name__ == "__main__":
    main()
