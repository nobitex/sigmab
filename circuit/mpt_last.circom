pragma circom 2.1.6;

include "./utils/concat.circom";
include "./utils/hasher.circom";
include "./utils/keccak/keccak.circom";
include "./hashbytes.circom";

template HashAddress() {
    signal input address[20];
    signal output hash_address[32];

    component addr_decomp[20];
    signal hashed_address_bits[32 * 8];
    signal keccak_input[136 * 8];
    for(var i = 0; i < 136; i++) {
        if(i < 20) {
            addr_decomp[i] = BitDecompose(8);
            addr_decomp[i].num <== address[i];
            for(var j = 0; j < 8; j++) {
                keccak_input[8 * i + j] <== addr_decomp[i].bits[j];
            }
        } else {
            if(i == 20) {
                for(var j = 0; j < 8; j++) {
                    keccak_input[8 * i + j] <== (0x01 >> j) & 1;
                }
            } else if(i == 135) {
                for(var j = 0; j < 8; j++) {
                    keccak_input[8 * i + j] <== (0x80 >> j) & 1;
                }
            } else {
                for(var j = 0; j < 8; j++) {
                    keccak_input[8 * i + j] <== 0;
                }
            }
        }
    }
    component keccak = Keccak(1);
    keccak.in <== keccak_input;
    keccak.blocks <== 1;
    hashed_address_bits <== keccak.out;
    for(var i = 0; i < 32; i++) {
        var sum = 0;
        for(var j = 0; j < 8; j++) {
            sum += (2 ** j) * hashed_address_bits[i * 8 + j];
        }
        hash_address[i] <== sum;
    }
}

template MptLast(maxBlocks, maxLowerLen, security) {

    var maxPrefixLen = maxBlocks * 136 - maxLowerLen;

    signal input address[20];

    signal input lowerLayerPrefixLen;
    signal input lowerLayerPrefix[maxPrefixLen];

    signal input lowerLayerLen;
    signal input lowerLayer[maxLowerLen];

    signal input salt;

    signal output commitUpper;
    signal output commitLower;

    signal hash_address[32];
    component addr_hasher = HashAddress();
    addr_hasher.address <== address;
    hash_address <== addr_hasher.hash_address;

    signal output expected_prefix[security + 2];
    for(var i = 0; i < security; i++) {
        expected_prefix[i] <== hash_address[32 - security + i];
    }
    expected_prefix[security] <== 1 + 0x80 + 55;
    expected_prefix[security + 1] <== lowerLayerLen;

    signal upperLayerBytes[maxPrefixLen + maxLowerLen];
    signal upperLayerBytesLen;

    component concat = Concat(maxPrefixLen, maxLowerLen);
    concat.a <== lowerLayerPrefix;
    concat.aLen <== lowerLayerPrefixLen;
    concat.b <== lowerLayer;
    concat.bLen <== lowerLayerLen;
    upperLayerBytes <== concat.out;
    upperLayerBytesLen <== concat.outLen;

    signal upperLayer[maxBlocks * 136 * 8];
    signal upperLayerLen;
    upperLayerLen <== 8 * upperLayerBytesLen;
    component decomps[maxPrefixLen + maxLowerLen];
    for(var i = 0; i < maxBlocks * 136; i++) {
        if(i < maxPrefixLen + maxLowerLen) {
            decomps[i] = BitDecompose(8);
            decomps[i].num <== upperLayerBytes[i];
            for(var j = 0; j < 8; j++) {
                upperLayer[8*i + j] <== decomps[i].bits[j];
            }
        } else {
            for(var j = 0; j < 8; j++) {
                upperLayer[8*i + j] <== 0;
            }
        }
    }

    // Commit to lowerLayer
    component hasherLower = HashBytes(maxLowerLen, 31);
    hasherLower.inp <== lowerLayer;
    component commitLowerToBlocks = Hasher();
    commitLowerToBlocks.left <== hasherLower.out;
    commitLowerToBlocks.right <== lowerLayerLen;
    component commitLowerToSalt = Hasher();
    commitLowerToSalt.left <== commitLowerToBlocks.hash;
    commitLowerToSalt.right <== salt;
    commitLower <== commitLowerToSalt.hash;

    // Commit to upperLayer
    component hasherUpper = HashBytes(maxBlocks * 136, 31);
    hasherUpper.inp <== upperLayerBytes;
    component commitUpperToBlocks = Hasher();
    commitUpperToBlocks.left <== hasherUpper.out;
    commitUpperToBlocks.right <== upperLayerBytesLen;
    component commitUpperToSalt = Hasher();
    commitUpperToSalt.left <== commitUpperToBlocks.hash;
    commitUpperToSalt.right <== salt;
    commitUpper <== commitUpperToSalt.hash;
 }

 component main = MptLast(4, 256, 20);