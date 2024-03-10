import json
import os
import io
from mimc7 import mimc7
from field import Field


def get_stealth_balance_addtion_proof(balances, salts, sumOfBalancesSalt):
    with io.open("/tmp/input_stealth_balance_addition.json", "w") as f:
        json.dump(
            {
                "balances": [str(b) for b in balances],
                "salts": [str(s) for s in salts],
                "sumOfBalancesSalt": str(sumOfBalancesSalt),
            },
            f,
        )

    os.system(
        "make gen_stealth_balance_addition_witness"
    )
    with io.open("/tmp/output_stealth_balance_addition.json", "r") as f:
        return f.read()

balances = [1, 2]
salts = [111, 222]
sumOfBalancesSalt = 333
proof = get_stealth_balance_addtion_proof(balances, salts, sumOfBalancesSalt)
print(proof)
for i in range(2):
    print(mimc7(Field(balances[i]), Field(salts[i])))

print(mimc7(Field(sum(balances)), Field(sumOfBalancesSalt)))