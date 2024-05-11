import tempfile
from typing import Union
import os
import json
import enum
import ast

from field import FieldEncoder


class ContextKeys(enum.Enum):
    LATEST_WITNESS_PATH = "LATEST_WITNESS_PATH"
    LATEST_PROOF_PATH = "LATEST_PROOF_PATH"
    LATEST_PUBLIC_VALUES = "LATEST_PUBLIC_VALUES"
    LATEST_VERIFICATION_KEY_DATA = "LATEST_VERIFICATION_KEY_DATA"


class AbstractCircuit:
    def __init__(
        self, witness_generator_path, prover_path, snarkjs_path, zk_params_path
    ):
        self.witness_generator_path = witness_generator_path
        self.prover_path = prover_path
        self.snarkjs_path = snarkjs_path
        self.zk_params_path = zk_params_path

        self.context = {}

    def generate_witness(self, **kwargs) -> str:
        with tempfile.NamedTemporaryFile() as f:
            data = json.dumps(kwargs, cls=FieldEncoder)
            f.write(data.encode())
            f.flush()

            with tempfile.NamedTemporaryFile(delete=False) as f_witness:
                os.system(f"{self.witness_generator_path} {f.name} {f_witness.name}")
                self.context[ContextKeys.LATEST_WITNESS_PATH] = f_witness.name
                return f_witness.name

    def export_verification_key(self) -> dict:
        with tempfile.NamedTemporaryFile() as f:
            os.system(
                f"{self.snarkjs_path} zkey export verificationkey {self.zk_params_path} {f.name}"
            )
            with open(f.name, "r") as f_vk:
                self.context[ContextKeys.LATEST_VERIFICATION_KEY_DATA] = json.load(f_vk)
            return self.context[ContextKeys.LATEST_VERIFICATION_KEY_DATA]

    def prove(self, witness_path: str) -> str:
        with tempfile.NamedTemporaryFile() as f_public, tempfile.NamedTemporaryFile(
            delete=False
        ) as f_proof:
            os.system(
                f"{self.prover_path} {self.zk_params_path} {witness_path} {f_proof.name} {f_public.name}"
            )
            f_public.seek(0)
            self.context[ContextKeys.LATEST_PUBLIC_VALUES] = ast.literal_eval(
                f_public.readlines()[0].decode()
            )
            self.context[ContextKeys.LATEST_PROOF_PATH] = f_proof.name
            return f_proof.name

    def verify(self, proof_path: str, verification_key_path: str) -> bool:
        with tempfile.NamedTemporaryFile() as f:
            os.system(
                f"{self.snarkjs_path} zkey verify {verification_key_path} {proof_path}"
            )
            return f.read() == "true"
