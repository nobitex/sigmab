.PHONY = all

trusted_setup:
	cd circuit && snarkjs powersoftau new bn128 21 pot12_0000.ptau -v
	cd circuit && snarkjs powersoftau contribute pot12_0000.ptau pot12_0001.ptau --entropy=1234 --name="first contribution" -v
	cd circuit && snarkjs powersoftau prepare phase2 pot12_0001.ptau pot12_final.ptau -v

circuit/mpt_path.r1cs: circuit/mpt_path.circom circuit/utils/*.circom
	cd circuit && circom mpt_path.circom --r1cs --wasm --sym --c
circuit/mpt_last.r1cs: circuit/mpt_last.circom circuit/utils/*.circom
	cd circuit && circom mpt_last.circom --r1cs --wasm --sym --c
circuit/pol.r1cs: circuit/pol.circom circuit/utils/*.circom
	cd circuit && circom pol.circom --r1cs --wasm --sym --c

circuit/mpt_path_cpp/mpt_path: circuit/mpt_path.r1cs
	mv circuit/mpt_path_cpp/main.cpp circuit/mpt_path_cpp/main.cpp.tmp && python3 scripts/spit_output.py < circuit/mpt_path_cpp/main.cpp.tmp > circuit/mpt_path_cpp/main.cpp && rm circuit/mpt_path_cpp/main.cpp.tmp
	cd circuit/mpt_path_cpp && make
circuit/mpt_last_cpp/mpt_last: circuit/mpt_last.r1cs
	mv circuit/mpt_last_cpp/main.cpp circuit/mpt_last_cpp/main.cpp.tmp && python3 scripts/spit_output.py < circuit/mpt_last_cpp/main.cpp.tmp > circuit/mpt_last_cpp/main.cpp && rm circuit/mpt_last_cpp/main.cpp.tmp
	cd circuit/mpt_last_cpp && make
circuit/pol_cpp/pol: circuit/pol.r1cs
	mv circuit/pol_cpp/main.cpp circuit/pol_cpp/main.cpp.tmp && python3 scripts/spit_output.py < circuit/pol_cpp/main.cpp.tmp > circuit/pol_cpp/main.cpp && rm circuit/pol_cpp/main.cpp.tmp
	cd circuit/pol_cpp && make

mpt_path_witness.wtns: circuit/mpt_path_cpp/mpt_path
	python3 mpt_path.py > circuit/input.json
	cd circuit/mpt_path_cpp && ./mpt_path ../input.json ../mpt_path_witness.wtns
	mv circuit/mpt_path_cpp/output.json .
mpt_last_witness.wtns: circuit/mpt_last_cpp/mpt_last
	python3 mpt_last.py > circuit/input.json
	cd circuit/mpt_last_cpp && ./mpt_last ../input.json ../mpt_last_witness.wtns
	mv circuit/mpt_last_cpp/output.json .
	cat output.json


pol_zkey: circuit/pol.r1cs
	cd circuit && snarkjs groth16 setup pol.r1cs pot20_final.ptau pol_0000.zkey
	cd circuit && snarkjs zkey contribute pol_0000.zkey pol_0001.zkey --entropy=1234 --name="second contribution" -v
	cd circuit && snarkjs zkey export verificationkey pol_0001.zkey verification_key.json

pol_witness.wtns: circuit/pol_cpp/pol
	python3 liability.py
	cd circuit/pol_cpp && ./pol ../input.json ../pol_witness.wtns
	mv circuit/pol_cpp/output.json .

gen_pol_proof:
	cd circuit && snarkjs groth16 prove pol_0001.zkey pol_witness.wtns pol_proof.json pol_public.json
	snarkjs generatecall circuit/pol_public.json circuit/pol_proof.json > /tmp/pol_proof.json 

verify_pol_proof:
	cd circuit && snarkjs groth16 verify verification_key.json pol_public.json pol_proof.json


circuit/mpt_path_0001.zkey: circuit/mpt_path.r1cs
	cd circuit && snarkjs groth16 setup mpt_path.r1cs ../pot20_final.ptau mpt_path_0000.zkey
	cd circuit && snarkjs zkey contribute mpt_path_0000.zkey mpt_path_0001.zkey --entropy=1234 --name="1st Contributor Name" -v


gen_pol_verifier: pol_zkey
	cd circuit && snarkjs zkey export solidityverifier pol_0001.zkey ../../src/PolVerifier.sol
	sed -i 's/Groth16Verifier/PolVerifier/' ../src/PolVerifier.sol


pol:
	make circuit/pol.r1cs
	make circuit/pol_cpp/pol
	make pol_witness.wtns
	make gen_pol_proof
	make verify_pol_proof

prove:
	@read -p "Enter the circuit name: " value; \
	cd build/circuits/$$value;\
	snarkjs wtns calculate $$value\_js/$$value.wasm input.json witness.wtns;\
	snarkjs groth16 prove 0001.zkey witness.wtns proof.json public.json;\
	echo "Proof generated at build/circuits/$$value/proof.json"

