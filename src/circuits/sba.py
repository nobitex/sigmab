from circuits import AbstractCircuit


class SBACircuit(AbstractCircuit):

    def generate_witness(self, balances, salts, sum_of_balances_salt, balance_commitments):
        return super().generate_witness(
            balances=[str(b) for b in balances],
            salts=[str(s) for s in salts],
            sumOfBalancesSalt=str(sum_of_balances_salt),
            balanceCommitments=[str(b) for b in balance_commitments],
        )
