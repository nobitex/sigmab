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
SALT = 123

provider = "https://yolo-shy-fog.discover.quiknode.pro/97f7aeb00bc7a8d80c3d4834a16cd9c86b54b552/"


def generate_mpt_cicuit_inputs(account_address, counter):
    '''
    Generates the inputs for mpt last and mpt path circuit and saves them in coresponding files in circuit/temp.
    
    Args:
        signature_data: the list of company addresses,
        counter: the number used as iterator.
    ''' 
    get_account_eth_mpt_proof(account_address, provider)
    # rename mpt_last files according to the counter
    os.rename('circuit/temp/mpt_last/input_mpt_last.json', f'circuit/temp/mpt_last/input_mpt_last_{counter}.json')
    os.rename('circuit/temp/mpt_last/output_mpt_last.json', f'circuit/temp/mpt_last/output_mpt_last_{counter}.json')
    os.rename('circuit/temp/mpt_last/mpt_last_witness.wtns', f'circuit/temp/mpt_last/mpt_last_witness_{counter}.wtns')
    # rename mpt_path files according to the counter
    os.rename('circuit/temp/mpt_path/input_mpt_path.json', f'circuit/temp/mpt_path/input_mpt_path_{counter}.json')
    os.rename('circuit/temp/mpt_path/output_mpt_path.json', f'circuit/temp/mpt_path/output_mpt_path_{counter}.json')
    os.rename('circuit/temp/mpt_path/mpt_path_witness.wtns', f'circuit/temp/mpt_path/mpt_path_witness_{counter}.wtns')
    print("inputs, outputs and witness files generated successfully.")

        
        
def generate_proof(counter):
    '''
    Generates the proof and public inputs and output for mpt_last an mpt_path circuit and saves them in the circuit/temp path.
    
    Args:
        counter: the number used as iterator.
    ''' 
    print("Generating proof and verification for the account number:", counter+1)
    # mpt_last
    os.rename(f'circuit/temp/mpt_last/mpt_last_witness_{counter}.wtns', 'circuit/temp/mpt_last/mpt_last_witness.wtns')
    os.system("make gen_mpt_last_proof")
    os.system("make verify_mpt_last_proof")
    os.rename('circuit/temp/mpt_last/mpt_last_proof.json', f'circuit/temp/mpt_last/mpt_last_proof_{counter}.json')
    os.rename('circuit/temp/mpt_last/mpt_last_public.json', f'circuit/temp/mpt_last/mpt_last_public_{counter}.json')
    # mpt_path
    os.rename(f'circuit/temp/mpt_path/mpt_path_witness_{counter}.wtns', 'circuit/temp/mpt_path/mpt_path_witness.wtns')
    os.system("make gen_mpt_path_proof")
    os.system("make verify_mpt_path_proof")
    os.rename('circuit/temp/mpt_path/mpt_path_proof.json', f'circuit/temp/mpt_path/mpt_path_proof_{counter}.json')
    os.rename('circuit/temp/mpt_path/mpt_path_public.json', f'circuit/temp/mpt_path/mpt_path_public_{counter}.json')
    
    
    
def combine_mpt_last_files(counter):
    '''
    Generates the proof data to be verified by groth16.verify function in extention.
    
    Args:
        counter: the proof counts used as iterator.
    ''' 
    with open('circuit/temp/mpt_last/verification_key.json', 'r') as f:
        vk_data = json.load(f)
    
    # Combine data from proof_n.json and pub_n.json files
    mpt_last_proofs = {"vk": vk_data, "proofs": []}
    for i in range(counter):
        proof_file = f"circuit/temp/mpt_last/mpt_last_proof_{i}.json"
        pub_file = f"circuit/temp/mpt_last/mpt_last_public_{i}.json"
        
        if os.path.exists(proof_file) and os.path.exists(pub_file):
            with open(proof_file, 'r') as f:
                proof_data = json.load(f)
            with open(pub_file, 'r') as f:
                pub_data = json.load(f)
            
            mpt_last_proofs["proofs"].append({
                "proof": proof_data,
                "pub": pub_data
            })
    
    # Write combined data to a new JSON file
    with open("data/mpt_last_proofs.json", 'w') as f:
        json.dump(mpt_last_proofs, f, indent=4)
        
        
def combine_mpt_path_files(counter):
    '''
    Generates the proof data to be verified by groth16.verify function in extention.
    
    Args:
        counter: the proof counts used as iterator.
    ''' 
    with open('circuit/temp/mpt_path/verification_key.json', 'r') as f:
        vk_data = json.load(f)
    
    # Combine data from proof_n.json and pub_n.json files
    mpt_path_proofs = {"vk": vk_data, "proofs": []}
    for i in range(counter):
        proof_file = f"circuit/temp/mpt_path/mpt_path_proof_{i}.json"
        pub_file = f"circuit/temp/mpt_path/mpt_path_public_{i}.json"
        
        if os.path.exists(proof_file) and os.path.exists(pub_file):
            with open(proof_file, 'r') as f:
                proof_data = json.load(f)
            with open(pub_file, 'r') as f:
                pub_data = json.load(f)
            
            mpt_path_proofs["proofs"].append({
                "proof": proof_data,
                "pub": pub_data
            })
    
    # Write combined data to a new JSON file
    with open("data/mpt_path_proofs.json", 'w') as f:
        json.dump(mpt_path_proofs, f, indent=4)
        
        
        
        
def generate_mpt_proof_data(address_list):
    '''
    Generates the cicuit inputs the witness, the output files, the proof, and the public arguments for mpt circuits.
    
    Args:
        address_list: the list of company addresses.
    ''' 
    accounts_count = len(address_list)
    for i in range(accounts_count):
        generate_mpt_cicuit_inputs(address_list[i], i)
        generate_proof(i)
    combine_mpt_last_files(accounts_count)
    combine_mpt_path_files(accounts_count)
    print("proof json file generated successfully.")
    
    
# Example usage:
address_list = ["0x727d270cB6d427A431b0C5A88AD6491712c86061", "0x27A0cfeE639c8cd775FdD4E34210f148dDB041A1"] 
generate_mpt_proof_data(address_list)
