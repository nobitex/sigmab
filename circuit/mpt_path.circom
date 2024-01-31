pragma circom 2.1.6;

include "./utils/keccak/keccak.circom";
include "./utils/substring_finder.circom";
include "./utils/hasher.circom";
include "./hashbits.circom";

template KeccakLayerChecker(maxBlocks) {
    signal input numUpperLayerBlocks;
    signal input upperLayer[maxBlocks * 136 * 8];

    signal input numLowerLayerBlocks;
    signal input lowerLayer[maxBlocks * 136 * 8];

    signal input salt;

    signal output commitUpper;
    signal output commitLower;
    signal output result;

    // Commit to lowerLayer
    component hasherLower = HashBits(maxBlocks * 136 * 8, 250);
    hasherLower.inp <== lowerLayer;
    component commitLowerToBlocks = Hasher();
    commitLowerToBlocks.left <== hasherLower.out;
    commitLowerToBlocks.right <== numLowerLayerBlocks;
    component commitLowerToSalt = Hasher();
    commitLowerToSalt.left <== commitLowerToBlocks.hash;
    commitLowerToSalt.right <== salt;
    commitLower <== commitLowerToSalt.hash;

    // Commit to upperLayer
    component hasherUpper = HashBits(maxBlocks * 136 * 8, 250);
    hasherUpper.inp <== upperLayer;
    component commitUpperToBlocks = Hasher();
    commitUpperToBlocks.left <== hasherUpper.out;
    commitUpperToBlocks.right <== numUpperLayerBlocks;
    component commitUpperToSalt = Hasher();
    commitUpperToSalt.left <== commitUpperToBlocks.hash;
    commitUpperToSalt.right <== salt;
    commitUpper <== commitUpperToSalt.hash;

    // Check if keccak(lowerLayer) is in upperLayer
    signal keccakLowerLayer[32 * 8];
    component keccak = Keccak(maxBlocks);
    keccak.in <== lowerLayer;
    keccak.blocks <== numLowerLayerBlocks;
    keccakLowerLayer <== keccak.out;
    component checker = substringCheck(maxBlocks, 136 * 8, 32 * 8);
    checker.subInput <== keccakLowerLayer;
    checker.numBlocks <== numUpperLayerBlocks;
    checker.mainInput <== upperLayer;
    result <== checker.out;
 }

 component main = KeccakLayerChecker(4);