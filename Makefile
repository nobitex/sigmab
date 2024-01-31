.PHONY = all

circuit/mpt_path.r1cs: circuit/mpt_path.circom circuit/utils/*.circom
	cd circuit && circom mpt_path.circom --r1cs --wasm --sym --c
circuit/mpt_last.r1cs: circuit/mpt_last.circom circuit/utils/*.circom
	cd circuit && circom mpt_last.circom --r1cs --wasm --sym --c

circuit/mpt_path_cpp/mpt_path: circuit/mpt_path.r1cs
	mv circuit/mpt_path_cpp/main.cpp circuit/mpt_path_cpp/main.cpp.tmp && python3 scripts/spit_output.py < circuit/mpt_path_cpp/main.cpp.tmp > circuit/mpt_path_cpp/main.cpp && rm circuit/mpt_path_cpp/main.cpp.tmp
	cd circuit/mpt_path_cpp && make
circuit/mpt_last_cpp/mpt_last: circuit/mpt_last.r1cs
	mv circuit/mpt_last_cpp/main.cpp circuit/mpt_last_cpp/main.cpp.tmp && python3 scripts/spit_output.py < circuit/mpt_last_cpp/main.cpp.tmp > circuit/mpt_last_cpp/main.cpp && rm circuit/mpt_last_cpp/main.cpp.tmp
	cd circuit/mpt_last_cpp && make

mpt_path_witness.wtns: circuit/mpt_path_cpp/mpt_path
	python3 mpt_path.py > circuit/input.json
	cd circuit/mpt_path_cpp && ./mpt_path ../input.json ../mpt_path_witness.wtns
	mv circuit/mpt_path_cpp/output.json .
mpt_last_witness.wtns: circuit/mpt_last_cpp/mpt_last
	python3 mpt_last.py > circuit/input.json
	cd circuit/mpt_last_cpp && ./mpt_last ../input.json ../mpt_last_witness.wtns
	mv circuit/mpt_last_cpp/output.json .
	cat output.json


circuit/mpt_path_0001.zkey: circuit/mpt_path.r1cs
	cd circuit && snarkjs groth16 setup mpt_path.r1cs ../pot20_final.ptau mpt_path_0000.zkey
	cd circuit && snarkjs zkey contribute mpt_path_0000.zkey mpt_path_0001.zkey --entropy=1234 --name="1st Contributor Name" -v
prove:
	@read -p "Enter the circuit name: " value; \
	cd build/circuits/$$value;\
	snarkjs wtns calculate $$value\_js/$$value.wasm input.json witness.wtns;\
	snarkjs groth16 prove 0001.zkey witness.wtns proof.json public.json;\
	echo "Proof generated at build/circuits/$$value/proof.json"

