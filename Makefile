.PHONY = all
# trusted set up


rapidsnark/package/bin/prover:
	cd circuit/rapidsnark && git submodule init
	cd circuit/rapidsnark && git submodule update
	cd circuit/rapidsnark && ./build_gmp.sh host
	cd circuit/rapidsnark && mkdir -p build_prover
	cd circuit/rapidsnark && cd build_prover && cmake .. -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=../package
	cd circuit/rapidsnark && cd build_prover && make -j4 && make install


extension:

	cd verifier && make all

	mkdir -p extensions

	cp -r verifier/extension/firefox/* extensions
	cp -r verifier/extension/common/* extensions
	cd extensions && zip -r ../Firefox-sigmab.zip . && cd ..
	rm -rf extensions/*

	cp -r verifier/extension/chrome/* extensions
	cp -r verifier/extension/common/* extensions
	cd extensions && zip -r ../Chrome-sigmab.zip . && cd ..
	rm -rf extensions/*

	mv Firefox-sigmab.zip extensions/Firefox-sigmab.xpi
	mv Chrome-sigmab.zip extensions/Chrome-sigmab.zip



trusted_setup:
	mkdir -p circuit/temp/setup
	cd circuit && snarkjs powersoftau new bn128 21 temp/setup/pot12_0000.ptau -v
	cd circuit && snarkjs powersoftau contribute temp/setup/pot12_0000.ptau temp/setup/pot12_0001.ptau --entropy=1234 --name="first contribution" -v
	cd circuit && snarkjs powersoftau prepare phase2 temp/setup/pot12_0001.ptau temp/setup/pot12_final.ptau -v


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

# ecdsa verify commands
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




# utils
clean:
	find . -type d -name '__pycache__' -exec rm -rf {} +
	rm -rf circuit/*.r1cs circuit/*.wasm circuit/*.sym circuit/*.json circuit/*.wtns circuit/mpt_last_cpp/ circuit/mpt_last_js/ circuit/mpt_last_cpp/ circuit/mpt_last_js/ circuit/mpt_path_cpp/ circuit/mpt_path_js/ circuit/stealth_balance_addition_cpp/ circuit/stealth_balance_addition_js/

clean_all: clean
	rm -rf circuit/*.zkey


# install: clean rapidsnark/package/bin/prover mpt_path mpt_path_zkey mpt_last mpt_last_zkey stealth_balance_addition stealth_balance_addition_zkey pol pol_zkey ecdsa_verify ecdsa_verify_zkey 
install: clean mpt_path mpt_path_zkey mpt_last mpt_last_zkey stealth_balance_addition stealth_balance_addition_zkey pol pol_zkey ecdsa_verify ecdsa_verify_zkey 

