pragma circom 2.1.5;

include "./utils/utils.circom";
include "./utils/concat.circom";


template Rlp() {
    signal input nonce;
    signal input balance; 
    signal input storage_hash[32];
    signal input code_hash[32];
    signal output rlp_encoded[99];
    signal output rlp_encoded_len;

    // Updated RLP lengths
    signal nonceRlpLen; 
    signal balanceRlpLen;
    var storageHashRlpLen = 33; // 32 bytes + 1 byte length prefix
    var codeHashRlpLen = 33; // 32 bytes + 1 byte length prefix

    // Placeholder signals for RLP encoded parts
    signal nonceRlpEncoded[10];
    signal rlpEncodedBalance[21];
    signal storageHashRlpEncoded[33];
    signal codeHashRlpEncoded[33];

    // RLP Encoding for nonce
    component bdNonce = ByteDecompose(10);
    bdNonce.num <== nonce;

    component byteln = GetRealByteLength(10);
    byteln.bytes <== bdNonce.bytes;

    component reverseNonce = ReverseArray(10);
    reverseNonce.bytes <== bdNonce.bytes;
    reverseNonce.realByteLen <== byteln.len;

    
    log("real bytes of nonce len ", byteln.len);
    
    signal nonceIsSingleByte;
    nonceIsSingleByte <-- (nonce < 0x80) ? 1 : 0;

    signal nonceRlpLenCalc;
    nonceRlpLenCalc <== (1 - nonceIsSingleByte) + byteln.len;

    signal isSingleNonceBytePrefix;
    signal extendedNoncePrefix;
    signal finalNoncePrefix;

    isSingleNonceBytePrefix <== nonceIsSingleByte * nonce;
    extendedNoncePrefix <== (1 - nonceIsSingleByte) * (0x80 + byteln.len);
    finalNoncePrefix <== isSingleNonceBytePrefix + extendedNoncePrefix;
    nonceRlpEncoded[0] <== finalNoncePrefix;

    var NONCE_MAX_LEN = 10; 
    component ngt[NONCE_MAX_LEN];

    for (var i = 1; i < NONCE_MAX_LEN; i++) {
        nonceRlpEncoded[i] <== (1 - nonceIsSingleByte) * reverseNonce.out[i-1];
    }

    nonceRlpLen <== nonceIsSingleByte + (1 - nonceIsSingleByte) * byteln.len;
     
    // RLP Encoding for balance
    component bdBalance = ByteDecompose(21);
    bdBalance.num <== balance;

    component bytelb = GetRealByteLength(21);
    bytelb.bytes <== bdBalance.bytes;

    log("the real bytes len for balance is", bytelb.len);

    component reverseBalance = ReverseArray(21);
    reverseBalance.bytes <== bdBalance.bytes;
    reverseBalance.realByteLen <== bytelb.len;

 
    signal balanceIsSingleByte;
    balanceIsSingleByte <-- (balance < 0x80) ? 1 : 0;

    signal balanceRlpLenCalc;
    balanceRlpLenCalc <== (1 - balanceIsSingleByte) + bytelb.len;

    signal isSingleBalanceBytePrefix;
    signal extendedBalancePrefix;
    signal finalBalancePrefix;

    isSingleBalanceBytePrefix <== balanceIsSingleByte * balance;
    extendedBalancePrefix <== (1 - balanceIsSingleByte) * (0x80 + bytelb.len);
    finalBalancePrefix <== isSingleBalanceBytePrefix + extendedBalancePrefix;
    rlpEncodedBalance[0] <== finalBalancePrefix;

    var BALANCE_MAX_LEN = 21; 
    component bgt[BALANCE_MAX_LEN];

    for (var i = 1; i < BALANCE_MAX_LEN; i++) {
         log("byte decompose balance ", reverseBalance.out[i]);
        rlpEncodedBalance[i] <== (1 - balanceIsSingleByte) * reverseBalance.out[i-1];
    }

    balanceRlpLen <== balanceIsSingleByte + (1 - balanceIsSingleByte) * bytelb.len + 1;

    // RLP Encoding for storage_hash
    storageHashRlpEncoded[0] <== 0x80 + 32;
    
    for (var i = 0; i < 32; i++) {
        storageHashRlpEncoded[i + 1] <== storage_hash[i]; 
    }

    // RLP Encoding for code_hash
    codeHashRlpEncoded[0] <== 0x80 + 32;
    
    for (var i = 0; i < 32; i++) {
        codeHashRlpEncoded[i + 1] <== code_hash[i];
    }

    // Concatenation Steps
    component concat1 = Concat(10, 21);
    concat1.a <== nonceRlpEncoded;
    concat1.aLen <== nonceRlpLen;
    concat1.b <== rlpEncodedBalance;
    concat1.bLen <== balanceRlpLen;

    component concat2 = Concat(31, 33);
    concat2.a <== concat1.out;
    concat2.aLen <== concat1.outLen;
    concat2.b <== storageHashRlpEncoded;
    concat2.bLen <== storageHashRlpLen;

    component concat3 = Concat(64, 33); 
    concat3.a <== concat2.out; 
    concat3.aLen <== concat2.outLen;
    concat3.b <== codeHashRlpEncoded;
    concat3.bLen <== codeHashRlpLen;

    var rlp_encoded_len_calc = nonceRlpLen + balanceRlpLen + codeHashRlpLen + storageHashRlpLen;

    signal final_rlp_prefix[2];

    final_rlp_prefix[0] <== 0xf8; 
    final_rlp_prefix[1] <== rlp_encoded_len_calc; 

    component concat4 = Concat(2, 97);
    concat4.a <== final_rlp_prefix;
    concat4.aLen <== 2;
    concat4.b <== concat3.out;
    concat4.bLen <== concat3.outLen;

    rlp_encoded <== concat4.out;
    rlp_encoded_len <== concat4.outLen;
}