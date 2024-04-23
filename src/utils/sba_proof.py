import os
import sys
import io, json
# Add the path to project_root
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(project_root)
from web3 import Web3
import rlp
from mpt.stealth_balance_addition import get_stealth_balance_addtion_proof_prod



def generate_sba_cicuit_inputs(balances, account_conuts, salt):
    '''
    Generates the inputs for stealth_balance_addition circuit and saves them in coresponding files in circuit/temp.
    
    Args:
        signature_data: the list of company addresses,
        counter: the number used as iterator.
    ''' 
    salts = []
    for i in range(account_conuts):
        salts.append(salt)
    get_stealth_balance_addtion_proof_prod(balances, salts, salt*account_conuts ,account_conuts)
    print("inputs, outputs and witness files generated successfully.")

        
        
def generate_proof():
    '''
    Generates the proof and public inputs and output for stealth_balance_addition an stealth_balance_addition circuit and saves them in the circuit/temp path.
    
    Args:
        counter: the number used as iterator.
    ''' 
    print("Generating proof and verification.")
    # stealth_balance_addition
    os.system("make gen_stealth_balance_addition_proof")
    os.system("make verify_stealth_balance_addition_proof")

    
    
def combine_stealth_balance_addition_files():
    '''
    Generates the proof data to be verified by groth16.verify function in extention.
    
    Args:
        counter: the proof counts used as iterator.
    ''' 
    with open('circuit/temp/stealth_balance_addition/verification_key.json', 'r') as f:
        vk_data = json.load(f)
    
    # Combine data from proof_n.json and pub_n.json files
    stealth_balance_addition_proofs = {"vk": vk_data, "proofs": []}
    proof_file = f"circuit/temp/stealth_balance_addition/stealth_balance_addition_proof.json"
    pub_file = f"circuit/temp/stealth_balance_addition/stealth_balance_addition_public.json"
        
    if os.path.exists(proof_file) and os.path.exists(pub_file):
        with open(proof_file, 'r') as f:
            proof_data = json.load(f)
        with open(pub_file, 'r') as f:
            pub_data = json.load(f)
            
        stealth_balance_addition_proofs["proofs"].append({
            "proof": proof_data,
            "pub": pub_data
        })
    
    # Write combined data to a new JSON file
    with open("data/stealth_balance_addition_proofs.json", 'w') as f:
        json.dump(stealth_balance_addition_proofs, f, indent=4)
        
        
        
        
        
        
def generate_sba_proof_data(balances, salt):
    '''
    Generates the cicuit inputs the witness, the output files, the proof, and the public arguments for mpt circuits.
    
    Args:
        address_list: the list of company addresses.
    ''' 
    accounts_count = len(balances)
    generate_sba_cicuit_inputs(balances, accounts_count, salt)
    generate_proof()
    combine_stealth_balance_addition_files()
    print("proof json file generated successfully.")
    
    
