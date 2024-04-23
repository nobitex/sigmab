import json
import io
import os
import sys
# Add the path to project_root
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)
from utils.field import Field
from utils.mimc7 import mimc7


def get_stealth_balance_addtion_proof(balances, salts, sumOfBalancesSalt):
    with io.open("circuit/temp/stealth_balance_addition/input_stealth_balance_addition.json", "w") as f:
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
    with io.open("circuit/temp/stealth_balance_addition/output_stealth_balance_addition.json", "r") as f:
        return f.read()
    
def get_stealth_balance_addtion_proof_prod(balances, salts, sumOfBalancesSalt, account_conuts):
    balance_commitments = []
    for i in range(account_conuts):
        commitment = get_balance_commitment(i)
        balance_commitments.append(commitment)
    with io.open("circuit/temp/stealth_balance_addition/input_stealth_balance_addition.json", "w") as f:
        json.dump(
            {
                "balances": [str(b) for b in balances],
                "salts": [str(s) for s in salts],
                "sumOfBalancesSalt": str(sumOfBalancesSalt),
                "balanceCommitments": [str(b) for b in balance_commitments],
            },
            f,
        )

    os.system(
        "make gen_stealth_balance_addition_witness"
    )
    with io.open("circuit/temp/stealth_balance_addition/output_stealth_balance_addition.json", "r") as f:
        return f.read()


def get_balance_commitment(accounts_index):
    
    output_file = f"circuit/temp/mpt_last/output_mpt_last_{accounts_index}.json"
    if os.path.exists(output_file) :
            with open(output_file, 'r') as f:
                commitment = json.load(f)
    else:
        raise Exception("ERROR: commitment is not generated. ")
    return commitment[102]

