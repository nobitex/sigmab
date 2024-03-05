.PHONY = all

trusted_setup:
	cd circuit && snarkjs powersoftau new bn128 21 pot12_0000.ptau -v
	cd circuit && snarkjs powersoftau contribute pot12_0000.ptau pot12_0001.ptau --entropy=1234 --name="first contribution" -v
	cd circuit && snarkjs powersoftau prepare phase2 pot12_0001.ptau pot12_final.ptau -v

mpt_first:
	cd circuit && circom mpt_first.circom --r1cs --wasm --sym --c

	mv circuit/mpt_first_cpp/main.cpp circuit/mpt_first_cpp/main.cpp.tmp
	python3 scripts/spit_output.py < circuit/mpt_first_cpp/main.cpp.tmp > circuit/mpt_first_cpp/main.cpp
	rm circuit/mpt_first_cpp/main.cpp.tmp
	cd circuit/mpt_first_cpp && make

mpt_first_zkey:
	cd circuit && snarkjs groth16 setup mpt_first.r1cs pot12_final.ptau mpt_first_0000.zkey
	cd circuit && snarkjs zkey contribute mpt_first_0000.zkey mpt_first_0001.zkey --entropy=1234 --name="second contribution" -v
	cd circuit && snarkjs zkey export verificationkey mpt_first_0001.zkey verification_key.json

gen_mpt_first_witness:
	cd circuit && ./mpt_first_cpp/mpt_first /tmp/input_mpt_first.json mpt_first_witness.wtns
	mv circuit/output.json /tmp/output_mpt_first.json

gen_mpt_first_proof:
	cd circuit && snarkjs groth16 prove mpt_first_0001.zkey mpt_first_witness.wtns mpt_first_proof.json mpt_first_public.json

mpt_path:
	cd circuit && circom mpt_path.circom --r1cs --wasm --sym --c

	mv circuit/mpt_path_cpp/main.cpp circuit/mpt_path_cpp/main.cpp.tmp
	python3 scripts/spit_output.py < circuit/mpt_path_cpp/main.cpp.tmp > circuit/mpt_path_cpp/main.cpp
	rm circuit/mpt_path_cpp/main.cpp.tmp
	cd circuit/mpt_path_cpp && make

mpt_path_zkey:
	cd circuit && snarkjs groth16 setup mpt_path.r1cs pot12_final.ptau mpt_path_0000.zkey
	cd circuit && snarkjs zkey contribute mpt_path_0000.zkey mpt_path_0001.zkey --entropy=1234 --name="second contribution" -v
	cd circuit && snarkjs zkey export verificationkey mpt_path_0001.zkey verification_key.json

gen_mpt_path_witness:
	cd circuit && ./mpt_path_cpp/mpt_path /tmp/input_mpt_path.json mpt_path_witness.wtns
	mv circuit/output.json /tmp/output_mpt_path.json

gen_mpt_path_proof:
	cd circuit && snarkjs groth16 prove mpt_path_0001.zkey mpt_path_witness.wtns mpt_path_proof.json mpt_path_public.json

mpt_last:
	cd circuit && circom mpt_last.circom --r1cs --wasm --sym --c

	mv circuit/mpt_last_cpp/main.cpp circuit/mpt_last_cpp/main.cpp.tmp
	python3 scripts/spit_output.py < circuit/mpt_last_cpp/main.cpp.tmp > circuit/mpt_last_cpp/main.cpp
	rm circuit/mpt_last_cpp/main.cpp.tmp
	cd circuit/mpt_last_cpp && make

mpt_last_zkey:
	cd circuit && snarkjs groth16 setup mpt_last.r1cs pot12_final.ptau mpt_last_0000.zkey
	cd circuit && snarkjs zkey contribute mpt_last_0000.zkey mpt_last_0001.zkey --entropy=1234 --name="second contribution" -v
	cd circuit && snarkjs zkey export verificationkey mpt_last_0001.zkey verification_key.json

gen_mpt_last_witness:
	cd circuit && ./mpt_last_cpp/mpt_last /tmp/input_mpt_last.json mpt_last_witness.wtns
	mv circuit/output.json /tmp/output_mpt_last.json

gen_mpt_last_proof:
	cd circuit && snarkjs groth16 prove mpt_last_0001.zkey mpt_last_witness.wtns mpt_last_proof.json mpt_last_public.json

stealth_balance_addition:
	cd circuit && circom stealth_balance_addition.circom --r1cs --wasm --sym --c

	mv circuit/stealth_balance_addition_cpp/main.cpp circuit/stealth_balance_addition_cpp/main.cpp.tmp
	python3 scripts/spit_output.py < circuit/stealth_balance_addition_cpp/main.cpp.tmp > circuit/stealth_balance_addition_cpp/main.cpp
	rm circuit/stealth_balance_addition_cpp/main.cpp.tmp
	cd circuit/stealth_balance_addition_cpp && make

stealth_balance_addition_zkey:
	cd circuit && snarkjs groth16 setup stealth_balance_addition.r1cs pot12_final.ptau stealth_balance_addition_0000.zkey
	cd circuit && snarkjs zkey contribute stealth_balance_addition_0000.zkey stealth_balance_addition_0001.zkey --entropy=1234 --name="second contribution" -v
	cd circuit && snarkjs zkey export verificationkey stealth_balance_addition_0001.zkey verification_key.json

gen_stealth_balance_addition_witness:
	cd circuit && ./stealth_balance_addition_cpp/stealth_balance_addition /tmp/input_stealth_balance_addition.json stealth_balance_addition_witness.wtns
	mv circuit/output.json /tmp/output_stealth_balance_addition.json

gen_stealth_balance_addition_proof:
	cd circuit && snarkjs groth16 prove stealth_balance_addition_0001.zkey stealth_balance_addition_witness.wtns stealth_balance_addition_proof.json stealth_balance_addition_public.json

clean:
	find . -type d -name '__pycache__' -exec rm -rf {} +
	rm -rf circuit/*.r1cs circuit/*.wasm circuit/*.sym circuit/*.json circuit/*.wtns circuit/mpt_last_cpp/ circuit/mpt_last_js/ circuit/mpt_last_cpp/ circuit/mpt_last_js/ circuit/mpt_path_cpp/ circuit/mpt_path_js/ circuit/mpt_first_cpp/ circuit/mpt_first_js/ circuit/stealth_balance_addition_cpp/ circuit/stealth_balance_addition_js/

clean_all: clean
	rm -rf circuit/*.zkey

install: clean mpt_first mpt_path mpt_last stealth_balance_addition