pragma circom 2.1.6;

include "./circom-ecdsa/circuits/vocdoni-keccak/keccak.circom";
include "./circomlib/circuits/bitify.circom";
include "./circom-ecdsa/circuits/ecdsa.circom";


template VerifyMsgECDSA () {  

  // Declaration of signals.  
  signal input message[32];
  signal input r[4];
  signal input s[4];
  signal input pubkeyX[4];
  signal input pubkeyY[4];
  
  signal concatenatedValues[80]; // size = 80 = 16 + 64   
  // signal msghash[32];

  signal output verified;

  // Serialization and concatenation of inputs
  component message_bits = Num2Bits(64);
  message_bits.in <== FeeRatio;
  for (var i = 0; i < 64; i += 1) {
    concatenatedValues[0 + i] <== message_bits.out[i];
  }
  
  // compute SHA256 of the serialized values
  component keccak = Keccak(80, 256);
  for (var i = 0; i < 80 / 8; i += 1) {
    for (var j = 0; j < 8; j++) {
      keccak.in[8*i + j] <== concatenatedValues[8*i + (7-j)];
    }
  }
  
  // convert the last 256 bits (32 bytes) into the number corresponding to hash of
  // the output of keccak is 32 bytes. bytes are arranged from largest to smallest
  // but bytes themselves are little-endian bitstrings of 8 bits
  // we just want a little-endian bitstring of them.
  component bits2Num= Bits2Num(256);
  for (var i = 0; i < 32; i++) {
    for (var j = 0; j < 8; j++) {
      bits2Num.in[8*i + j] <== keccak.out[256 - 8*(i+1) + j];
    }
  }

  // orderHash <== bits2Num.out;

  // Prepare msghash as the input of the Verify Signature method
  component serial2BytesAray[4];
  for (var i = 0; i < 4; i++) {
    serial2BytesAray[i] = Bits2Num(64);
    for (var j = 0; j < 64; j++) {
      serial2BytesAray[i].in[j] <== keccak.out[256 - 64*(i+1) + j];
    }
  }

  // Build a VerifyECDSA circuit with the size of 256 bits = 32 bytes
  component verify = ECDSAVerifyNoPubkeyCheck(64, 4);
  for (var i = 0; i < 4; i++) {
    verify.r[i] <== r[i];
    verify.s[i] <== s[i];
    verify.msghash[i] <== serial2BytesAray[i].out;
    verify.pubkey[0][i] <== pubkeyX[i];
    verify.pubkey[1][i] <== pubkeyY[i];
  }
  
  verified <== verify.result;
}

component main = VerifyEthECDSA();