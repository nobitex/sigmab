import os
import sys
import io, json
# Add the path to project_root
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(project_root)
from web3 import Web3
import rlp
from pol.liability import buildLiabilityTree
from pol.liability import generate_input_json
from pol.smt import LiabilityNode
from utils.field  import Field
from utils.mimc7 import mimc7
from pol.pol_utils import id_hash
SALT = 123

with open('src/pol/liabilities.json', 'r') as file:
    data = json.load(file)

liabilities_data = data.get('liabilities', [])
solvency_data = data.get('solvency_data', {})

liabilitynodes = [LiabilityNode(Field(id_hash(item['id'])), Field(item['amount'])) for item in liabilities_data]
liabilityNodeLength = len(liabilitynodes)

solvency_balance = solvency_data.get('solvency_balance', 0)
solvency_balance_salt = solvency_data.get('solvency_balance_salt', '')
# create the tree
liabilityTree = buildLiabilityTree(liabilitynodes, 10)


def generate_pol_cicuit_inputs(counter):
    '''
    Generates the inputs for pol last and pol path circuit and saves them in coresponding files in circuit/temp.
    
    Args:
        signature_data: the list of company addresses,
        counter: the number used as iterator.
    ''' 
    Proof = liabilityTree.createProof(counter, solvency_balance, solvency_balance_salt)
    generate_input_json(Proof)
    os.system("make gen_pol_witness")
    # rename pol files according to the counter
    os.rename('circuit/temp/pol/input_pol.json', f'circuit/temp/pol/input_pol_{counter}.json')
    os.rename('circuit/temp/pol/output_pol.json', f'circuit/temp/pol/output_pol_{counter}.json')
    os.rename('circuit/temp/pol/pol_witness.wtns', f'circuit/temp/pol/pol_witness_{counter}.wtns')


        
        
def generate_proof(counter):
    '''
    Generates the proof and public inputs and output for pol an pol_path circuit and saves them in the circuit/temp path.
    
    Args:
        counter: the number used as iterator.
    ''' 
    print("Generating proof and verification for the account number:", counter)
    # pol
    os.rename(f'circuit/temp/pol/pol_witness_{counter}.wtns', 'circuit/temp/pol/pol_witness.wtns')
    os.system("make gen_pol_proof")
    os.system("make verify_pol_proof")
    os.rename('circuit/temp/pol/pol_proof.json', f'circuit/temp/pol/pol_proof_{counter}.json')
    os.rename('circuit/temp/pol/pol_public.json', f'circuit/temp/pol/pol_public_{counter}.json')
    
    
def combine_pol_files(counter):
    '''
    Generates the proof data to be verified by groth16.verify function in extention.
    
    Args:
        counter: the proof counts used as iterator.
    ''' 
    with open('circuit/temp/pol/verification_key.json', 'r') as f:
        vk_data = json.load(f)
    
    # Combine data from proof_n.json and pub_n.json files
    pol_proofs = {"vk": vk_data, "proofs": []}
    for i in range(counter):
        proof_file = f"circuit/temp/pol/pol_proof_{i}.json"
        pub_file = f"circuit/temp/pol/pol_public_{i}.json"
        
        if os.path.exists(proof_file) and os.path.exists(pub_file):
            with open(proof_file, 'r') as f:
                proof_data = json.load(f)
            with open(pub_file, 'r') as f:
                pub_data = json.load(f)
            
            pol_proofs["proofs"].append({
                "proof": proof_data,
                "pub": pub_data
            })
    
    # Write combined data to a new JSON file
    with open("data/pol_proofs.json", 'w') as f:
        json.dump(pol_proofs, f, indent=4)
        
        
        
        
        
        
def generate_pol_proof_data():
    '''
    Generates the cicuit inputs the witness, the output files, the proof, and the public arguments for pol circuits.
    
    Args:
        address_list: the list of company addresses.
    ''' 
    for i in range(liabilityNodeLength):
        generate_pol_cicuit_inputs(i)
        generate_proof(i)
    combine_pol_files(liabilityNodeLength)
    print("proof json file generated successfully.")
    
    
# # Example usage:
# generate_pol_proof_data()
