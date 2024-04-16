pragma circom 2.1.6;

include "./utils/keccak/keccak.circom";
include "./utils/ecdsa/ecdsa.circom";
include "./utils/hasher.circom";
include "./utils/eth.circom";
include "./hashbytes.circom";

template VerifyMsgECDSA () {  
  signal input r[4];
  signal input s[4];
  signal input msghash[4];
  signal input pubkey[2][4];
  signal input salt;
  signal output verified;
  signal output commitmentHash;


  // Build a VerifyECDSA circuit with the size of 256 bits = 32 bytes
  component verifySignature = ECDSAVerifyNoPubkeyCheck(64, 4);
  for (var i = 0; i < 4; i++) {
      verifySignature.r[i] <== r[i];
      verifySignature.s[i] <== s[i];
      verifySignature.msghash[i] <== msghash[i];
      for (var j = 0; j < 2; j++) {
          verifySignature.pubkey[j][i] <== pubkey[j][i];
      }
  }
  verifySignature.result === 1;
  verified <== verifySignature.result;


  // flatten the public key chunks to 512 bits
  component flattenPub = FlattenPubkey(64, 4);
  for (var i = 0; i < 4; i++) {
      flattenPub.chunkedPubkey[0][i] <== pubkey[0][i];
      flattenPub.chunkedPubkey[1][i] <== pubkey[1][i];
  }

  // create address 20 bytes from 512 public key bits
  component pubToAddr = PubkeyToAddress();
    for (var i = 0; i < 512; i++) {
        pubToAddr.pubkeyBits[i] <== flattenPub.pubkeyBits[i];
    }
    
   // generate commitment hash from address bytes and salt
  component commitmentHasher = Hasher();
  commitmentHasher.left <== pubToAddr.address;
  commitmentHasher.right <== salt;

  commitmentHash <== commitmentHasher.hash;

}

component main = VerifyMsgECDSA();