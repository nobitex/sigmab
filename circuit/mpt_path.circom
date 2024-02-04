pragma circom 2.1.6;

include "./utils/keccak/keccak.circom";
include "./utils/substring_finder.circom";
include "./utils/hasher.circom";
include "./utils/padding.circom";
include "./hashbits.circom";

template KeccakLayerChecker(maxBlocks) {

    signal input numUpperLayerBytes;
    signal input upperLayerBytes[maxBlocks * 136];

    signal input numLowerLayerBytes;
    signal input lowerLayerBytes[maxBlocks * 136];

    signal numUpperLayerBlocks;
    signal upperLayer[maxBlocks * 136 * 8];

    signal numLowerLayerBlocks;
    signal lowerLayer[maxBlocks * 136 * 8];

    component upperPadding = Padding(maxBlocks, 136);
    upperPadding.a <== upperLayerBytes;
    upperPadding.aLen <== numUpperLayerBytes;
    component upperBitConverter = BytesToBits(maxBlocks * 136);
    upperBitConverter.bytes <== upperPadding.out;
    upperLayer <== upperBitConverter.bits;
    numUpperLayerBlocks <== upperPadding.num_blocks;

    component lowerPadding = Padding(maxBlocks, 136);
    lowerPadding.a <== lowerLayerBytes;
    lowerPadding.aLen <== numLowerLayerBytes;
    component lowerBitConverter = BytesToBits(maxBlocks * 136);
    lowerBitConverter.bytes <== lowerPadding.out;
    lowerLayer <== lowerBitConverter.bits;
    numLowerLayerBlocks <== lowerPadding.num_blocks;

    signal input salt;

    signal output commitUpper;
    signal output commitLower;
    signal output result;

    // Commit to lowerLayer
    component hasherLower = HashBits(maxBlocks * 136 * 8, 250);
    hasherLower.inp <== lowerLayer;
    component commitLowerToLen = Hasher();
    commitLowerToLen.left <== hasherLower.out;
    commitLowerToLen.right <== numLowerLayerBlocks * 136 * 8;
    component commitLowerToSalt = Hasher();
    commitLowerToSalt.left <== commitLowerToLen.hash;
    commitLowerToSalt.right <== salt;
    commitLower <== commitLowerToSalt.hash;

    // Commit to upperLayer
    component hasherUpper = HashBits(maxBlocks * 136 * 8, 250);
    hasherUpper.inp <== upperLayer;
    component commitUpperToLen = Hasher();
    commitUpperToLen.left <== hasherUpper.out;
    commitUpperToLen.right <== numUpperLayerBlocks * 136 * 8;
    component commitUpperToSalt = Hasher();
    commitUpperToSalt.left <== commitUpperToLen.hash;
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