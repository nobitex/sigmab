from circuits import MPTLastCircuit, MPTPathCircuit, ECDSACircuit, SBACircuit, ContextKeys
from consts import *
from web3 import Web3
import tqdm


def main():
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

    sba_circuit = get_sba_circuit(
        witness_gen_path=SBA_WITNESS_GEN_PATH,
        prover_path=PROVER_PATH,
        snarkjs_path=SNARKJS_PATH,
        zk_params_path=SBA_ZK_PARAMS_PATH,
    )

    import random
    # salt = random.randint(0, 10**5)
    salt = 100

    from utilss import load_solvency_data
    message, exchange_accounts_data = load_solvency_data("data/solvency_data.json")

    ### ECDSA Proof Generation
    ecdsa_progress = tqdm.tqdm(exchange_accounts_data, total=len(exchange_accounts_data), desc="ECDSA Progress")
    for exchange_account in ecdsa_progress:
        witness_path = ecdsa_circuit.generate_witness(message, exchange_account.pubkey, exchange_account.signature, salt)
        proof_path = ecdsa_circuit.prove(witness_path)

        exchange_account.set_value("ecdsa_witness_path", witness_path)
        exchange_account.set_value("ecdsa_proof_path", proof_path)
        exchange_account.set_value("ecdsa_public_outputs", ecdsa_circuit.context.get(ContextKeys.LATEST_PUBLIC_VALUES))
    
        ecdsa_progress.write(f"Generated proof for account: {exchange_account.address}")
        ecdsa_progress.write(f"Proof path: {proof_path}")
        ecdsa_progress.write(f"Public outputs: {ecdsa_circuit.context.get(ContextKeys.LATEST_PUBLIC_VALUES)}")

    ### MPT Proof Generation
    provider = Web3(Web3.HTTPProvider(PROVIDER))
    block_number = provider.eth.get_block_number()
    block = provider.eth.get_block(block_number)

    mpt_proof_progress = tqdm.tqdm(exchange_accounts_data, total=len(exchange_accounts_data), desc="MPT Proof Progress")
    for exchange_account in mpt_proof_progress:

        ecdsa_commitment = exchange_account.get_value("ecdsa_public_outputs")[1]

        account_proof = provider.eth.get_proof(exchange_account.address, [], block_number)
        exchange_account.set_value("account_proof", account_proof)
        exchange_account.set_value("account_proof_block_number", block_number)
        mpt_proof_progress.write(f"Generated proof for account: {exchange_account.address}")

        #### MPT Last Proof Generation
        witeness_path = mpt_last_circuit.generate_witness(exchange_account, block, ecdsa_commitment, salt)
        proof_path = mpt_last_circuit.prove(witeness_path)

        exchange_account.set_value("mpt_last_witness_path", witeness_path)
        exchange_account.set_value("mpt_last_proof_path", proof_path)
        exchange_account.set_value("mpt_last_public_outputs", mpt_last_circuit.context.get(ContextKeys.LATEST_PUBLIC_VALUES))

        mpt_proof_progress.write(f"Generated MPT Last proof for account: {exchange_account.address}")
        mpt_proof_progress.write(f"Proof path: {proof_path}")

        #### MPT Path Proof Generation
        rev_proof = account_proof.accountProof[::-1]

        witenss_paths = []
        proof_paths = []
        public_outputs = []
        for index, level in enumerate(rev_proof):
            mpt_proof_progress.write(f"Generating MPT Path proof for account: {exchange_account.address} | Level: {index + 1}/{len(rev_proof)}")
            if index == len(rev_proof) - 1:
                if Web3.keccak(level) != block.stateRoot:
                    raise Exception("Not verified!")
                witeness_path = mpt_path_circuit.generate_witness(salt, level, block.stateRoot, True)
                proof_path = mpt_path_circuit.prove(witeness_path)

                witenss_paths.append(witeness_path)
                proof_paths.append(proof_path)
                public_outputs.append(mpt_path_circuit.context.get(ContextKeys.LATEST_PUBLIC_VALUES))
            else:
                if Web3.keccak(level) not in rev_proof[index + 1]:
                    raise Exception("Not verified!")
                witeness_path = mpt_path_circuit.generate_witness(salt, level, rev_proof[index + 1], False)
                proof_path = mpt_path_circuit.prove(witeness_path)

                witenss_paths.append(witeness_path)
                proof_paths.append(proof_path)
                public_outputs.append(mpt_path_circuit.context.get(ContextKeys.LATEST_PUBLIC_VALUES))
    
        exchange_account.set_value("mpt_path_witness_paths", witenss_paths)
        exchange_account.set_value("mpt_path_proof_paths", proof_paths)
        exchange_account.set_value("mpt_path_public_outputs", public_outputs)

        mpt_proof_progress.write(f"Generated MPT Path proof for account: {exchange_account.address}")
        mpt_proof_progress.write(f"Proof paths: {proof_paths}")


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


if __name__ == "__main__":
    main()
