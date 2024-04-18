import os
import sys
import subprocess
import ecdsa, io, json, hashlib
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(project_root)
from eth_utils.crypto import keccak
from Crypto.Hash import keccak
from web3 import Web3
from eth_account import Account
from ecdsa import VerifyingKey, SigningKey, SECP256k1, util
from ecdsa.curves import SECP256k1
from ecdsa import NIST384p, SigningKey
from ecdsa.util import randrange_from_seed__trytryagain
from utils.sign import sign_message_with_sha256, checkECDSA
from dotenv import load_dotenv
dotenv_path = os.path.join(project_root, '.env')
load_dotenv(dotenv_path)




def generate_sks_hex(num_sks):
    
    '''
    Generates a list of secret_key and public_key from env file in hex format.
    
    Args:`
        num_sks: number of needed secret_key and public_key pairs.

    Returns:
        accounts: an array of generated secret_key and public_keys.

    '''
    accounts = []
    for i in range(num_sks):
        sk_hex = os.getenv(f"PK{i}")
        private_key_bytes = bytes.fromhex(sk_hex)

        # Create a signing key from the private key bytes
        signing_key = SigningKey.from_string(private_key_bytes, curve=SECP256k1)

        # Get the corresponding verifying key (public key)
        verifying_key = signing_key.get_verifying_key()

        # The hexadecimal representation of the public key
        public_key_hex = verifying_key.to_string().hex()
        accounts.append([sk_hex, public_key_hex])
    return accounts

 
def generate_signature_data(num_sks, message):
    '''
    Generates the signature from a given secret key and a pre_defined message.
    
    Args:
        num_sks: number of needed secret_key and public_key pairs.

    Returns:
        data: an array of generated signatures and related public_keys.

    ''' 
    generated_accounts = generate_sks_hex(num_sks)
    data=[]
    for i in range(num_sks): 
        signature = sign_message_with_sha256(generated_accounts[i][0], message)
        data.append([signature, generated_accounts[i][1]])  
    return data


def generate_ecdsa_cicuit_input(signature_data, message, salt, counter):
    '''
    Generates the inputs for ECDSA_verify circuit and saves them  in the circuit/temp/ecdsa_verify path.
    
    Args:
        signature_data: the list of user signatures and related public_keys.
        message: the message to be signed and verified using the procided circiut.
        salt: the salt which is the input of the ecdsa circuit.
        counter: the number used as iterator.
    ''' 
    checkECDSA(message, signature_data[counter][1], signature_data[counter][0],salt, counter)
    
def generate_witness(counter):
    '''
    Generates the witness and outputs for ECDSA_verify circuit and saves them  in the circuit/temp/ecdsa_verify path.
    
    Args:
        counter: the number used as iterator.
    ''' 
    os.rename(f'circuit/temp/ecdsa_verify/input_ecdsa_verify_{counter}.json', 'circuit/temp/ecdsa_verify/input_ecdsa_verify.json')
    os.system("make gen_ecdsa_verify_witness")
    os.rename('circuit/temp/ecdsa_verify/input_ecdsa_verify.json', f'circuit/temp/ecdsa_verify/input_ecdsa_verify_{counter}.json')
    os.rename('circuit/temp/ecdsa_verify/output_ecdsa_verify.json', f'circuit/temp/ecdsa_verify/output_ecdsa_verify_{counter}.json')
    os.rename('circuit/temp/ecdsa_verify/ecdsa_verify_witness.wtns', f'circuit/temp/ecdsa_verify/ecdsa_verify_witness_{counter}.wtns')
        
        
def generate_proof(counter):
    '''
    Generates the proof and public inputs and output for ECDSA_verify circuit and saves them  in the circuit/temp/ecdsa_verify path.
    
    Args:
        counter: the number used as iterator.
    ''' 
    print("Generating proof and verification for the account number:", counter+1)
    os.rename(f'circuit/temp/ecdsa_verify/ecdsa_verify_witness_{counter}.wtns', 'circuit/temp/ecdsa_verify/ecdsa_verify_witness.wtns')
    os.system("make gen_ecdsa_verify_proof")
    os.system("make verify_ecdsa_verify_proof")
    os.rename('circuit/temp/ecdsa_verify/ecdsa_verify_proof.json', f'circuit/temp/ecdsa_verify/ecdsa_verify_proof_{counter}.json')
    os.rename('circuit/temp/ecdsa_verify/ecdsa_verify_public.json', f'circuit/temp/ecdsa_verify/ecdsa_verify_public_{counter}.json')
    
    
    
def combine_files(counter):
    '''
    Generates the proof data to be verified by groth16.verify function in extention.
    
    Args:
        counter: the proof counts used as iterator.
    ''' 
    with open('circuit/temp/ecdsa_verify/verification_key.json', 'r') as f:
        vk_data = json.load(f)
    
    # Combine data from proof_n.json and pub_n.json files
    ecdsa_proofs = {"vk": vk_data, "proofs": []}
    for i in range(counter):
        proof_file = f"circuit/temp/ecdsa_verify/ecdsa_verify_proof_{i}.json"
        pub_file = f"circuit/temp/ecdsa_verify/ecdsa_verify_public_{i}.json"
        
        if os.path.exists(proof_file) and os.path.exists(pub_file):
            with open(proof_file, 'r') as f:
                proof_data = json.load(f)
            with open(pub_file, 'r') as f:
                pub_data = json.load(f)
            
            ecdsa_proofs["proofs"].append({
                "proof": proof_data,
                "pub": pub_data
            })
    
    # Write combined data to a new JSON file
    with open("data/ecdsa_proofs.json", 'w') as f:
        json.dump(ecdsa_proofs, f, indent=4)
        
        
        
        
        
def generate_signature_proof_verification_data(signature_data, message, salt):
    '''
    Generates the cicuit inputs the witness, the output files, the proof, and the public arguments for ECDSA_verify circuit.
    
    Args:
        signature_data: the list of user signatures and related public_keys.
        message: the message to be signed and verified using the procided circiut.
        salt: the salt which is the input of the ecdsa circuit.
    ''' 
    accounts_count = len(signature_data)
    for i in range(accounts_count):
        generate_ecdsa_cicuit_input(signature_data, message, salt, i)
        generate_witness(i)
        generate_proof(i)
    combine_files(accounts_count)
    print("proof json file generated successfully.")
   



