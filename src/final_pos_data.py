from utils.utils import get_solvency_data
from utils.utils import combine_proof_files
from utils.ecdsa_proof import generate_signature_proof_verification_data
from utils.mpt_proof import generate_mpt_proof_data
from utils.sba_proof import generate_sba_proof_data
from utils.pol_proof import generate_pol_proof_data
import time
import random
import os
import sys
import io, json

# proof_of_liability_count = 360,000
# Generate a random integer between 0 and 10^5
# salt = random.randint(0, 10**5)
salt = 100

#starting time
start = time.time()

# get data
message, signature_data, address_array, num_accounts, balances = get_solvency_data()

# ecdsa_proof_data
generate_signature_proof_verification_data(None, signature_data, message, salt)

# mpt_proof_data
generate_mpt_proof_data(address_array, salt)

# sba_proof_data
generate_sba_proof_data(balances, salt)

# pol_proof_data
generate_pol_proof_data(salt)

# generate one single json file for all generated proofs
combine_proof_files()

# end time
end = time.time()

# total time taken
print("Execution time of the program is- ", end-start)
