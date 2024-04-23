import os
import sys
import io, json
# Add the path to project_root
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(project_root)
from web3 import Web3
import rlp
from mpt import mpt_last
from mpt import mpt_path
from prove import get_account_eth_mpt_proof


provider = "https://yolo-shy-fog.discover.quiknode.pro/97f7aeb00bc7a8d80c3d4834a16cd9c86b54b552/"

def get_solvency_data():
    with open('data/solvency_data.json', 'r') as file:
        data = json.load(file)
    message = data.get('message')
    accounts = data.get('accounts', {})
    signature_data = [[bytes.fromhex(account_data['signature']), account_data['pubkey']] for account_data in accounts.values()]
    # Extracting addresses into another array
    address_array = [account_data['address'] for account_data in accounts.values()]
    num_accounts = len(signature_data)
    w3 = Web3(Web3.HTTPProvider(provider))
    balances = []
    for i in range(num_accounts):
        balance_wei = w3.eth.get_balance(address_array[i])
        balances.append(balance_wei)
        
    return message, signature_data, address_array, num_accounts, balances


def combine_proof_files():
    '''
    Generates the proof data to be verified by groth16.verify function in extention.

    ''' 
    with open('data/ecdsa_proofs.json', 'r') as f:
        ecdsa_proofs = json.load(f)
    with open('data/mpt_last_proofs.json', 'r') as f:
        mpt_last_proofs = json.load(f)
    with open('data/mpt_path_proofs.json', 'r') as f:
        mpt_path_proofs = json.load(f)
    with open('data/pol_proofs.json', 'r') as f:
        pol_proofs = json.load(f)
    with open('data/stealth_balance_addition_proofs.json', 'r') as f:
        sba_proofs = json.load(f)
    
    # Combine data from proof_n.json and pub_n.json files
    proofs = {
        "ecdsa_proofs": ecdsa_proofs,
        "mpt_last_proofs": mpt_last_proofs,
        "mpt_path_proofs": mpt_path_proofs,
        "pol_proofs": pol_proofs,
        "sba_proofs": sba_proofs
        }
        
    # Write combined data to a new JSON file
    with open("data/proofs.json", 'w') as f:
        json.dump(proofs, f, indent=4)
        
    os.system("rm -rf data/ecdsa_proofs.json")
    os.system("rm -rf data/mpt_last_proofs.json")
    os.system("rm -rf data/mpt_path_proofs.json")
    os.system("rm -rf data/pol_proofs.json")
    os.system("rm -rf data/stealth_balance_addition_proofs.json")
            