from circuits import AbstractCircuit
from field import Field


class POLCircuit(AbstractCircuit):

    def generate_witness(self, merkle_proof):
        ids = list(map(lambda node: node.id, merkle_proof.proof_nodes))
        amounts = list(map(lambda node: node.amount, merkle_proof.proof_nodes))

        return self._generate_witness(
            index=merkle_proof.index,
            unique_id=merkle_proof.id,
            amount=merkle_proof.amount,
            proof_ids=ids,
            proof_sums=amounts,
            solvency_balance=merkle_proof.solvency_balance,
            solvency_balance_salt=merkle_proof.solvency_balance_salt,
        )

    def _generate_witness(
        self,
        index,
        unique_id,
        amount,
        proof_ids,
        proof_sums,
        solvency_balance,
        solvency_balance_salt,
    ):
        return super().generate_witness(
            index=index,
            unique_id=unique_id,
            amount=amount,
            proof_ids=[p for p in proof_ids],
            proof_sums=[p for p in proof_sums],
            solvency_balance=solvency_balance,
            solvency_balance_salt=solvency_balance_salt,
        )
