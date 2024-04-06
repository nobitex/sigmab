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

  component pubHasher[7];

  pubHasher[0] = Hasher();
  pubHasher[1] = Hasher();
  pubHasher[2] = Hasher();
  pubHasher[3] = Hasher();
  pubHasher[4] = Hasher();
  pubHasher[5] = Hasher();
  pubHasher[6] = Hasher();
  
  pubHasher[0].left <== pubkey[0][0];
  pubHasher[0].right <==  pubkey[1][0];

  pubHasher[1].left  <==  pubkey[0][1];
  pubHasher[1].right <==  pubkey[1][1];        

  pubHasher[2].left <== pubkey[0][2];
  pubHasher[2].right <==  pubkey[1][2];
  
  pubHasher[3].left  <==  pubkey[0][3];
  pubHasher[3].right <==  pubkey[1][3];      


  pubHasher[4].left <== pubHasher[0].hash;
  pubHasher[4].right <== pubHasher[1].hash;

  pubHasher[5].left <== pubHasher[2].hash;
  pubHasher[5].right <== pubHasher[3].hash;

  pubHasher[6].left <== pubHasher[4].hash;
  pubHasher[6].right <== pubHasher[5].hash;


  component cHasher = Hasher();
  cHasher.left <== pubHasher[6].hash;
  cHasher.right <== salt;

  commit <== cHasher.hash;
}

component main = VerifyMsgECDSA();