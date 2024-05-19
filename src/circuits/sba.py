from circuits import AbstractCircuit


class SBACircuit(AbstractCircuit):
    def generate_witness(
        self, balances, salt
    ):
        return super().generate_witness(
            balances=[str(b) for b in balances],
            salt=str(salt),
        )
