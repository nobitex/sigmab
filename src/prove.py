from circuits import MPTLastCircuit, MPTPathCircuit, ECDSACircuit, SBACircuit
import os

MPT_LAST_WITNESS_GEN_PATH = os.environ.get(
    "MPT_LAST_WITNESS_GEN_PATH",
    "/home/ostadgeorge/work/nobitex/sigmab/circuit/temp/mpt_last/mpt_last_cpp/mpt_last",
)
MPT_LAST_ZK_PARAMS_PATH = os.environ.get(
    "MPT_LAST_ZK_PARAMS_PATH",
    "/home/ostadgeorge/work/nobitex/sigmab/circuit/temp/mpt_last/mpt_last_0001.zkey",
)

MPT_PATH_WITNESS_GEN_PATH = os.environ.get(
    "MPT_PATH_WITNESS_GEN_PATH",
    "/home/ostadgeorge/work/nobitex/sigmab/circuit/temp/mpt_path/mpt_path_cpp/mpt_path",
)
MPT_PATH_ZK_PARAMS_PATH = os.environ.get(
    "MPT_PATH_ZK_PARAMS_PATH",
    "/home/ostadgeorge/work/nobitex/sigmab/circuit/temp/mpt_path/mpt_path_0001.zkey",
)

ECDSA_WITNESS_GEN_PATH = os.environ.get(
    "ECDSA_WITNESS_GEN_PATH",
    "/home/ostadgeorge/work/nobitex/sigmab/circuit/temp/ecdsa_verify/ecdsa_verify_cpp/ecdsa_verify",
)
ECDSA_ZK_PARAMS_PATH = os.environ.get(
    "ECDSA_ZK_PARAMS_PATH",
    "/home/ostadgeorge/work/nobitex/sigmab/circuit/temp/ecdsa_verify/ecdsa_verify_0001.zkey",
)

SBA_WITNESS_GEN_PATH = os.environ.get(
    "SBA_WITNESS_GEN_PATH",
    "/home/ostadgeorge/work/nobitex/sigmab/circuit/temp/stealth_balance_addition/stealth_balance_addition_cpp/stealth_balance_addition",
)
SBA_ZK_PARAMS_PATH = os.environ.get(
    "SBA_ZK_PARAMS_PATH",
    "/home/ostadgeorge/work/nobitex/sigmab/circuit/temp/stealth_balance_addition/stealth_balance_addition_0001.zkey",
)

PROVER_PATH = os.environ.get(
    "PROVER_PATH",
    "/home/ostadgeorge/work/nobitex/sigmab/circuit/rapidsnark/package/bin/prover",
)
SNARKJS_PATH = os.environ.get(
    "SNARKJS_PATH", "/home/ostadgeorge/.nvm/versions/node/v20.12.1/bin/snarkjs"
)


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

    from utils.utils import get_solvency_data
    message, signature_data, address_array, num_accounts, balances = get_solvency_data()

    witness_path = ecdsa_circuit.generate_witness(message, signature_data[0][1], signature_data[0][0], salt)
    proof_path = ecdsa_circuit.prove(witness_path)
    print(witness_path, proof_path)
    print(ecdsa_circuit.context)

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
