from circuits import (
    MPTLastCircuit,
    MPTPathCircuit,
    ECDSACircuit,
    SBACircuit,
    POLCircuit,
    ContextKeys,
)
from config import *
import json


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

    pol_circuit = get_pol_circuit(
        witness_gen_path=POL_WITNESS_GEN_PATH,
        prover_path=PROVER_PATH,
        snarkjs_path=SNARKJS_PATH,
        zk_params_path=POL_ZK_PARAMS_PATH,
    )

    VKS = {
        "ECDSA_VK": ecdsa_circuit.export_verification_key(),
        "MPT_LAST_VK": mpt_last_circuit.export_verification_key(),
        "MPT_PATH_VK": mpt_path_circuit.export_verification_key(),
        "SBA_VK": sba_circuit.export_verification_key(),
        "POL_VK": pol_circuit.export_verification_key(),
    }
    VKS_PATH = "data/vks.json"

    with open(VKS_PATH, "w") as f:
        json.dump(VKS, f, indent=4)


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
