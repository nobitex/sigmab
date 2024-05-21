import os


PROVIDER = os.environ.get(
    "PROVIDER",
    "https://yolo-shy-fog.discover.quiknode.pro/97f7aeb00bc7a8d80c3d4834a16cd9c86b54b552/",
)

MPT_LAST_WITNESS_GEN_PATH = os.environ.get(
    "MPT_LAST_WITNESS_GEN_PATH",
    "circuit/temp/mpt_last/mpt_last_cpp/mpt_last",
)
MPT_LAST_ZK_PARAMS_PATH = os.environ.get(
    "MPT_LAST_ZK_PARAMS_PATH",
    "circuit/temp/mpt_last/mpt_last_0001.zkey",
)

MPT_PATH_WITNESS_GEN_PATH = os.environ.get(
    "MPT_PATH_WITNESS_GEN_PATH",
    "circuit/temp/mpt_path/mpt_path_cpp/mpt_path",
)
MPT_PATH_ZK_PARAMS_PATH = os.environ.get(
    "MPT_PATH_ZK_PARAMS_PATH",
    "circuit/temp/mpt_path/mpt_path_0001.zkey",
)

ECDSA_WITNESS_GEN_PATH = os.environ.get(
    "ECDSA_WITNESS_GEN_PATH",
    "circuit/temp/ecdsa_verify/ecdsa_verify_cpp/ecdsa_verify",
)
ECDSA_ZK_PARAMS_PATH = os.environ.get(
    "ECDSA_ZK_PARAMS_PATH",
    "circuit/temp/ecdsa_verify/ecdsa_verify_0001.zkey",
)

SBA_WITNESS_GEN_PATH = os.environ.get(
    "SBA_WITNESS_GEN_PATH",
    "circuit/temp/stealth_balance_addition/stealth_balance_addition_cpp/stealth_balance_addition",
)
SBA_ZK_PARAMS_PATH = os.environ.get(
    "SBA_ZK_PARAMS_PATH",
    "circuit/temp/stealth_balance_addition/stealth_balance_addition_0001.zkey",
)

POL_WITNESS_GEN_PATH = os.environ.get(
    "POL_WITNESS_GEN_PATH",
    "circuit/temp/pol/pol_cpp/pol",
)
POL_ZK_PARAMS_PATH = os.environ.get(
    "POL_ZK_PARAMS_PATH",
    "circuit/temp/pol/pol_0001.zkey",
)

PROVER_PATH = os.environ.get(
    "PROVER_PATH",
    "circuit/rapidsnark/package/bin/prover",
)
SNARKJS_PATH = os.environ.get("SNARKJS_PATH", ".nvm/versions/node/v20.12.1/bin/snarkjs")
