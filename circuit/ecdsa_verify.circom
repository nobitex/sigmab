pragma circom 2.1.6;

include "./utils/keccak/keccak.circom";
include "./utils/ecdsa/ecdsa.circom";
include "./utils/hasher.circom";

template VerifyMsgECDSA () {  
  signal input r[4];
  signal input s[4];
  signal input msghash[4];
  signal input pubkey[2][4];
  signal input salt;
  signal output verified;
  signal output commit;

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

  component pubHasher = Hasher();

  pubHasher.left <== pubkey[0];
  pubHasher.right <== pubkey[1];

  component cHasher = Hasher();
  
  cHasher.left <== pubHasher.hash;
  cHasher.right <== salt;

  commit <== cHasher.hash;
}

component main = VerifyMsgECDSA();