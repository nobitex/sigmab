from utils.ecdsa_proof import generate_signature_data
from utils.ecdsa_proof import generate_signature_proof_verification_data
from utils.mpt_proof import generate_mpt_proof_data
from utils.sba_proof import generate_sba_proof_data
from utils.pol_proof import generate_pol_proof_data


salt = 123
message = "Nobitex"
address_list = ["0x727d270cB6d427A431b0C5A88AD6491712c86061", "0x27A0cfeE639c8cd775FdD4E34210f148dDB041A1"] 
num_sks = len(address_list)

# ecdsa_proof_data
signature_data = generate_signature_data(num_sks)
generate_signature_proof_verification_data(signature_data, message, salt)

# mpt_proof_data
generate_mpt_proof_data(address_list)

# sba_proof_data

balances = [90313886187000, 518994566333498]
generate_sba_proof_data(balances)

# pol_proof_data
generate_pol_proof_data()
