.PHONY = all
# trusted set up

trusted_setup:
	mkdir -p circuit/temp/setup
	cd circuit && snarkjs powersoftau new bn128 21 temp/setup/pot12_0000.ptau -v
	cd circuit && snarkjs powersoftau contribute temp/setup/pot12_0000.ptau temp/setup/pot12_0001.ptau --entropy=1234 --name="first contribution" -v
	cd circuit && snarkjs powersoftau prepare phase2 temp/setup/pot12_0001.ptau temp/setup/pot12_final.ptau -v

# mpt_first commands
mpt_first:
	mkdir -p circuit/temp/mpt_first
	cd circuit && circom mpt_first.circom --r1cs --wasm --sym --c
	mv circuit/mpt_first_cpp circuit/temp/mpt_first
	mv circuit/mpt_first_js circuit/temp/mpt_first
	mv circuit/temp/mpt_first/mpt_first_cpp/main.cpp circuit/temp/mpt_first/mpt_first_cpp/main.cpp.tmp
	python3 scripts/spit_output.py < circuit/temp/mpt_first/mpt_first_cpp/main.cpp.tmp > circuit/temp/mpt_first/mpt_first_cpp/main.cpp
	rm circuit/temp/mpt_first/mpt_first_cpp/main.cpp.tmp
	cd circuit/temp/mpt_first/mpt_first_cpp && make
	mv circuit/mpt_first.r1cs circuit/temp/mpt_first/mpt_first.r1cs
	mv circuit/mpt_first.sym circuit/temp/mpt_first/mpt_first.sym 

mpt_first_zkey:
	cd circuit && snarkjs groth16 setup temp/mpt_first/mpt_first.r1cs temp/setup/pot20_final.ptau mpt_first_0000.zkey
	mv circuit/mpt_first_0000.zkey circuit/temp/mpt_first/mpt_first_0000.zkey
	cd circuit && snarkjs zkey contribute temp/mpt_first/mpt_first_0000.zkey temp/mpt_first/mpt_first_0001.zkey --entropy=1234 --name="second contribution" -v
	cd circuit && snarkjs zkey export verificationkey temp/mpt_first/mpt_first_0001.zkey temp/mpt_first/verification_key.json

gen_mpt_first_witness:
	cd circuit/temp/mpt_first/mpt_first_cpp && ./mpt_first /tmp/input_mpt_first.json mpt_first_witness.wtns
	cd circuit/temp/pol/pol_cpp && ./pol ../input_pol.json pol_witness.wtns
	mv circuit/temp/mpt_first/mpt_first_cpp/mpt_first_witness.wtns circuit/temp/mpt_first/mpt_first_witness.wtns
	mv circuit/temp/mpt_first/mpt_first_cpp/output.json /tmp/output_mpt_first.json

gen_mpt_first_proof:
	cd circuit && snarkjs groth16 prove temp/mpt_first/mpt_first_0001.zkey temp/mpt_first/mpt_first_witness.wtns mpt_first_proof.json mpt_first_public.json
	snarkjs generatecall circuit/mpt_first_public.json circuit/mpt_first_proof.json > /tmp/pol_proof.json 
	mv circuit/mpt_first_proof.json circuit/temp/mpt_first/mpt_first_proof.json
	mv circuit/mpt_first_public.json circuit/temp/mpt_first/mpt_first_public.json

# mpt_path commands
mpt_path:
	mkdir -p circuit/temp/mpt_path
	cd circuit && circom mpt_path.circom --r1cs --wasm --sym --c
	mv circuit/mpt_path_cpp circuit/temp/mpt_path
	mv circuit/mpt_path_js circuit/temp/mpt_path
	mv circuit/temp/mpt_path/mpt_path_cpp/main.cpp circuit/temp/mpt_path/mpt_path_cpp/main.cpp.tmp
	python3 scripts/spit_output.py < circuit/temp/mpt_path/mpt_path_cpp/main.cpp.tmp > circuit/temp/mpt_path/mpt_path_cpp/main.cpp
	rm circuit/temp/mpt_path/mpt_path_cpp/main.cpp.tmp
	cd circuit/temp/mpt_path/mpt_path_cpp && make
	mv circuit/mpt_path.r1cs circuit/temp/mpt_path/mpt_path.r1cs
	mv circuit/mpt_path.sym circuit/temp/mpt_path/mpt_path.sym 

mpt_path_zkey:
	cd circuit && snarkjs groth16 setup temp/mpt_path/mpt_path.r1cs temp/setup/pot20_final.ptau mpt_path_0000.zkey
	mv circuit/mpt_path_0000.zkey circuit/temp/mpt_path/mpt_path_0000.zkey
	cd circuit && snarkjs zkey contribute temp/mpt_path/mpt_path_0000.zkey temp/mpt_path/mpt_path_0001.zkey --entropy=1234 --name="second contribution" -v
	cd circuit && snarkjs zkey export verificationkey temp/mpt_path/mpt_path_0001.zkey temp/mpt_path/verification_key.json

gen_mpt_path_witness:
	cd circuit/temp/mpt_path/mpt_path_cpp && ./mpt_path /tmp/input_mpt_path.json mpt_path_witness.wtns
	cd circuit/temp/pol/pol_cpp && ./pol ../input_pol.json pol_witness.wtns
	mv circuit/temp/mpt_path/mpt_path_cpp/mpt_path_witness.wtns circuit/temp/mpt_path/mpt_path_witness.wtns
	mv circuit/temp/mpt_path/mpt_path_cpp/output.json /tmp/output_mpt_path.json

gen_mpt_path_proof:
	cd circuit && snarkjs groth16 prove temp/mpt_path/mpt_path_0001.zkey temp/mpt_path/mpt_path_witness.wtns mpt_path_proof.json mpt_path_public.json
	snarkjs generatecall circuit/mpt_path_public.json circuit/mpt_path_proof.json > /tmp/mpt_path_proof.json 
	mv circuit/mpt_path_proof.json circuit/temp/mpt_path/mpt_path_proof.json
	mv circuit/mpt_path_public.json circuit/temp/mpt_path/mpt_path_public.json

# mpt_last commands
mpt_last:
	mkdir -p circuit/temp/mpt_last
	cd circuit && circom mpt_last.circom --r1cs --wasm --sym --c
	mv circuit/mpt_last_cpp circuit/temp/mpt_last
	mv circuit/mpt_last_js circuit/temp/mpt_last
	mv circuit/temp/mpt_last/mpt_last_cpp/main.cpp circuit/temp/mpt_last/mpt_last_cpp/main.cpp.tmp
	python3 scripts/spit_output.py < circuit/temp/mpt_last/mpt_last_cpp/main.cpp.tmp > circuit/temp/mpt_last/mpt_last_cpp/main.cpp
	rm circuit/temp/mpt_last/mpt_last_cpp/main.cpp.tmp
	cd circuit/temp/mpt_last/mpt_last_cpp && make
	mv circuit/mpt_last.r1cs circuit/temp/mpt_last/mpt_last.r1cs
	mv circuit/mpt_last.sym circuit/temp/mpt_last/mpt_last.sym 

mpt_last_zkey:
	cd circuit && snarkjs groth16 setup temp/mpt_last/mpt_last.r1cs temp/setup/pot20_final.ptau mpt_last_0000.zkey
	mv circuit/mpt_last_0000.zkey circuit/temp/mpt_last/mpt_last_0000.zkey
	cd circuit && snarkjs zkey contribute temp/mpt_last/mpt_last_0000.zkey temp/mpt_last/mpt_last_0001.zkey --entropy=1234 --name="second contribution" -v
	cd circuit && snarkjs zkey export verificationkey temp/mpt_last/mpt_last_0001.zkey temp/mpt_last/verification_key.json

gen_mpt_last_witness:
	cd circuit/temp/mpt_last/mpt_last_cpp && ./mpt_last /tmp/input_mpt_last.json mpt_last_witness.wtns
	cd circuit/temp/pol/pol_cpp && ./pol ../input_pol.json pol_witness.wtns
	mv circuit/temp/mpt_last/mpt_last_cpp/mpt_last_witness.wtns circuit/temp/mpt_last/mpt_last_witness.wtns
	mv circuit/temp/mpt_last/mpt_last_cpp/output.json /tmp/output_mpt_last.json

gen_mpt_last_proof:
	cd circuit && snarkjs groth16 prove temp/mpt_last/mpt_last_0001.zkey temp/mpt_last/mpt_last_witness.wtns mpt_last_proof.json mpt_last_public.json
	snarkjs generatecall circuit/mpt_last_public.json circuit/mpt_last_proof.json > /tmp/mpt_last_proof.json 
	mv circuit/mpt_last_proof.json circuit/temp/mpt_last/mpt_last_proof.json
	mv circuit/mpt_last_public.json circuit/temp/mpt_last/mpt_last_public.json
verify_mpt_last_proof:
	cd circuit && snarkjs groth16 verify temp/mpt_last/verification_key.json temp/mpt_last/mpt_last_public.json temp/mpt_last/mpt_last_proof.json


# stealth_balance_addition commands
stealth_balance_addition:
	mkdir -p circuit/temp/stealth_balance_addition
	cd circuit && circom stealth_balance_addition.circom --r1cs --wasm --sym --c
	mv circuit/stealth_balance_addition_cpp circuit/temp/stealth_balance_addition
	mv circuit/stealth_balance_addition_js circuit/temp/stealth_balance_addition
	mv circuit/temp/stealth_balance_addition/stealth_balance_addition_cpp/main.cpp circuit/temp/stealth_balance_addition/stealth_balance_addition_cpp/main.cpp.tmp
	python3 scripts/spit_output.py < circuit/temp/stealth_balance_addition/stealth_balance_addition_cpp/main.cpp.tmp > circuit/temp/stealth_balance_addition/stealth_balance_addition_cpp/main.cpp
	rm circuit/temp/stealth_balance_addition/stealth_balance_addition_cpp/main.cpp.tmp
	cd circuit/temp/stealth_balance_addition/stealth_balance_addition_cpp && make
	mv circuit/stealth_balance_addition.r1cs circuit/temp/stealth_balance_addition/stealth_balance_addition.r1cs
	mv circuit/stealth_balance_addition.sym circuit/temp/stealth_balance_addition/stealth_balance_addition.sym 

stealth_balance_addition_zkey:
	cd circuit && snarkjs groth16 setup temp/stealth_balance_addition/stealth_balance_addition.r1cs temp/setup/pot20_final.ptau stealth_balance_addition_0000.zkey
	mv circuit/stealth_balance_addition_0000.zkey circuit/temp/stealth_balance_addition/stealth_balance_addition_0000.zkey
	cd circuit && snarkjs zkey contribute temp/stealth_balance_addition/stealth_balance_addition_0000.zkey temp/stealth_balance_addition/stealth_balance_addition_0001.zkey --entropy=1234 --name="second contribution" -v
	cd circuit && snarkjs zkey export verificationkey temp/stealth_balance_addition/stealth_balance_addition_0001.zkey temp/stealth_balance_addition/verification_key.json

gen_stealth_balance_addition_witness:
	cd circuit/temp/stealth_balance_addition && ./stealth_balance_addition_cpp/stealth_balance_addition /tmp/input_stealth_balance_addition.json stealth_balance_addition_witness.wtns
	mv circuit/stealth_balance_addition_witness.wtns circuit/temp/stealth_balance_addition/stealth_balance_addition_witness.wtns
	mv circuit/temp/stealth_balance_addition/output.json /tmp/output_stealth_balance_addition.json

gen_stealth_balance_addition_proof:
	cd circuit && snarkjs groth16 prove temp/stealth_balance_addition/stealth_balance_addition_0001.zkey temp/stealth_balance_addition/stealth_balance_addition_witness.wtns stealth_balance_addition_proof.json stealth_balance_addition_public.json
	snarkjs generatecall circuit/stealth_balance_addition_public.json circuit/stealth_balance_addition_proof.json > /tmp/stealth_balance_addition_proof.json 
	mv circuit/stealth_balance_addition_proof.json circuit/temp/stealth_balance_addition/stealth_balance_addition_proof.json
	mv circuit/stealth_balance_addition_public.json circuit/temp/stealth_balance_addition/stealth_balance_addition_public.json

# pol commands
pol:
	mkdir -p circuit/temp/pol
	cd circuit && circom pol.circom --r1cs --wasm --sym --c
	mv circuit/pol_cpp circuit/temp/pol
	mv circuit/pol_js circuit/temp/pol

	mv circuit/temp/pol/pol_cpp/main.cpp circuit/temp/pol/pol_cpp/main.cpp.tmp
	python3 scripts/spit_output.py < circuit/temp/pol/pol_cpp/main.cpp.tmp > circuit/temp/pol/pol_cpp/main.cpp
	
	rm circuit/temp/pol/pol_cpp/main.cpp.tmp
	cd circuit/temp/pol/pol_cpp && make
	mv circuit/pol.r1cs circuit/temp/pol/pol.r1cs
	mv circuit/pol.sym circuit/temp/pol/pol.sym 


pol_zkey:
	cd circuit && snarkjs groth16 setup temp/pol/pol.r1cs temp/setup/pot20_final.ptau pol_0000.zkey
	mv circuit/pol_0000.zkey circuit/temp/pol/pol_0000.zkey
	cd circuit && snarkjs zkey contribute temp/pol/pol_0000.zkey temp/pol/pol_0001.zkey --entropy=1234 --name="second contribution" -v
	cd circuit && snarkjs zkey export verificationkey temp/pol/pol_0001.zkey temp/pol/verification_key.json


gen_pol_witness: 
	python3 src/pol/liability.py
	cd circuit/temp/pol/pol_cpp && ./pol ../input_pol.json pol_witness.wtns
	mv circuit/temp/pol/pol_cpp/pol_witness.wtns circuit/temp/pol/pol_witness.wtns 
	mv circuit/temp/pol/pol_cpp/output.json circuit/temp/pol/output_pol.json

gen_pol_proof:
	cd circuit && snarkjs groth16 prove temp/pol/pol_0001.zkey temp/pol/pol_witness.wtns pol_proof.json pol_public.json
	snarkjs generatecall circuit/pol_public.json circuit/pol_proof.json > /tmp/pol_proof.json 
	mv circuit/pol_proof.json circuit/temp/pol/pol_proof.json
	mv circuit/pol_public.json circuit/temp/pol/pol_public.json
verify_pol_proof:
	cd circuit && snarkjs groth16 verify temp/pol/verification_key.json temp/pol/pol_public.json temp/pol/pol_proof.json

ecdsa_verify:
	mkdir -p circuit/temp/ecdsa_verify
	cd circuit && circom ecdsa_verify.circom --r1cs --wasm --sym --c
	mv circuit/ecdsa_verify_cpp circuit/temp/ecdsa_verify
	mv circuit/ecdsa_verify_js circuit/temp/ecdsa_verify
	mv circuit/temp/ecdsa_verify/ecdsa_verify_cpp/main.cpp circuit/temp/ecdsa_verify/ecdsa_verify_cpp/main.cpp.tmp
	python3 scripts/spit_output.py < circuit/temp/ecdsa_verify/ecdsa_verify_cpp/main.cpp.tmp > circuit/temp/ecdsa_verify/ecdsa_verify_cpp/main.cpp
	rm circuit/temp/ecdsa_verify/ecdsa_verify_cpp/main.cpp.tmp
	cd circuit/temp/ecdsa_verify/ecdsa_verify_cpp && make
	mv circuit/ecdsa_verify.r1cs circuit/temp/ecdsa_verify/ecdsa_verify.r1cs
	mv circuit/ecdsa_verify.sym circuit/temp/ecdsa_verify/ecdsa_verify.sym 

ecdsa_verify_zkey:
	cd circuit && snarkjs groth16 setup temp/ecdsa_verify/ecdsa_verify.r1cs temp/setup/pot22_final.ptau ecdsa_verify_0000.zkey
	mv circuit/ecdsa_verify_0000.zkey circuit/temp/ecdsa_verify/ecdsa_verify_0000.zkey
	cd circuit && snarkjs zkey contribute temp/ecdsa_verify/ecdsa_verify_0000.zkey temp/ecdsa_verify/ecdsa_verify_0001.zkey --entropy=1234 --name="second contribution" -v
	cd circuit && snarkjs zkey export verificationkey temp/ecdsa_verify/ecdsa_verify_0001.zkey temp/ecdsa_verify/verification_key.json

gen_ecdsa_verify_witness:
	python3 src/ecdsa_verify.py
	cd circuit/temp/ecdsa_verify/ecdsa_verify_cpp && ./ecdsa_verify ../input_ecdsa_verify.json ecdsa_verify_witness.wtns
	mv circuit/temp/ecdsa_verify/ecdsa_verify_cpp/ecdsa_verify_witness.wtns circuit/temp/ecdsa_verify/ecdsa_verify_witness.wtns 
	mv circuit/temp/ecdsa_verify/ecdsa_verify_cpp/output.json circuit/temp/ecdsa_verify/output_ecdsa_verify.json


gen_ecdsa_verify_proof:
	cd circuit && snarkjs groth16 prove temp/ecdsa_verify/ecdsa_verify_0001.zkey temp/ecdsa_verify/ecdsa_verify_witness.wtns ecdsa_verify_proof.json ecdsa_verify_public.json
	snarkjs generatecall circuit/ecdsa_verify_public.json circuit/ecdsa_verify_proof.json > /tmp/ecdsa_verify_proof.json 
	mv circuit/ecdsa_verify_proof.json circuit/temp/ecdsa_verify/ecdsa_verify_proof.json
	mv circuit/ecdsa_verify_public.json circuit/temp/ecdsa_verify/ecdsa_verify_public.json
verify_ecdsa_verify_proof:
	cd circuit && snarkjs groth16 verify temp/ecdsa_verify/verification_key.json temp/ecdsa_verify/ecdsa_verify_public.json temp/ecdsa_verify/ecdsa_verify_proof.json


# utils
clean:
	find . -type d -name '__pycache__' -exec rm -rf {} +
	rm -rf circuit/*.r1cs circuit/*.wasm circuit/*.sym circuit/*.json circuit/*.wtns circuit/mpt_last_cpp/ circuit/mpt_last_js/ circuit/mpt_last_cpp/ circuit/mpt_last_js/ circuit/mpt_path_cpp/ circuit/mpt_path_js/ circuit/mpt_first_cpp/ circuit/mpt_first_js/ circuit/stealth_balance_addition_cpp/ circuit/stealth_balance_addition_js/

clean_all: clean
	rm -rf circuit/*.zkey

install: clean mpt_first mpt_path mpt_last stealth_balance_addition pol