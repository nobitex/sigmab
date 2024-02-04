pragma circom 2.1.6;

include "./utils/concat.circom";
include "./utils/hasher.circom";
include "./hashbytes.circom";

template MptLast(maxBlocks, maxLowerLen) {

    var maxPrefixLen = maxBlocks * 136 - maxLowerLen;

    signal input lowerLayerPrefixLen;
    signal input lowerLayerPrefix[maxPrefixLen];

    signal input lowerLayerLen;
    signal input lowerLayer[maxLowerLen];

    signal input salt;

    signal output commitUpper;
    signal output commitLower;

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

 component main = MptLast(4, 256);