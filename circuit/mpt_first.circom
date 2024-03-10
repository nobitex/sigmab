pragma circom 2.1.5;

include "./utils/concat.circom";
include "./utils/padding.circom";
include "./utils/keccak/keccak.circom";
include "./utils/utils.circom";


template MptFirst(maxBlocks) {
    var KeccakSize = 136;
    var SplitSize = KeccakSize / 8;
    var maxPrefixLen = maxBlocks * SplitSize * 2;
    var maxPostfixLen = maxBlocks * SplitSize * 6 - 50;
    var maxCommitTopLen = 50;

    signal input numPrefixBytes;
    signal input prefixBytes[maxPrefixLen];

    signal input numPostfixBytes;
    signal input postfixBytes[maxPostfixLen];

    signal input numCommitTopBytes;
    signal input commitTopBytes[maxCommitTopLen];


    signal PrefixCommitTopBytes[maxPrefixLen + maxCommitTopLen];
    signal PrefixCommitTopBytesLen;

    component concat_prefix_commit_top = Concat(maxPrefixLen, maxCommitTopLen);
    concat_prefix_commit_top.a <== prefixBytes;
    concat_prefix_commit_top.aLen <== numPrefixBytes;
    concat_prefix_commit_top.b <== commitTopBytes;
    concat_prefix_commit_top.bLen <== numCommitTopBytes;
    PrefixCommitTopBytes <== concat_prefix_commit_top.out;
    PrefixCommitTopBytesLen <== concat_prefix_commit_top.outLen;

    signal PrefixCommitTopPostfixBytes[maxPrefixLen + maxCommitTopLen + maxPostfixLen];
    signal PrefixCommitTopPostfixBytesLen;

    component concat_prefix_commit_top_postfix = Concat(maxPrefixLen + maxCommitTopLen, maxPostfixLen);
    concat_prefix_commit_top_postfix.a <== PrefixCommitTopBytes;
    concat_prefix_commit_top_postfix.aLen <== PrefixCommitTopBytesLen;
    concat_prefix_commit_top_postfix.b <== postfixBytes;
    concat_prefix_commit_top_postfix.bLen <== numPostfixBytes;
    PrefixCommitTopPostfixBytes <== concat_prefix_commit_top_postfix.out;
    PrefixCommitTopPostfixBytesLen <== concat_prefix_commit_top_postfix.outLen;

    signal numHeaderBlocks;
    signal headerLayer[maxBlocks * KeccakSize * 8];

    component headerPadding = Padding(maxBlocks, KeccakSize);
    headerPadding.a <== PrefixCommitTopPostfixBytes;
    headerPadding.aLen <== PrefixCommitTopPostfixBytesLen;

    component headerBitConverter = BytesToBits(maxBlocks * KeccakSize);
    headerBitConverter.bytes <== headerPadding.out;
    headerLayer <== headerBitConverter.bits;
    numHeaderBlocks <== headerPadding.num_blocks;

    signal keccakHeaderLayer[32 * 8];
    component keccak = Keccak(maxBlocks);
    keccak.in <== headerLayer;
    keccak.blocks <== numHeaderBlocks;
    keccakHeaderLayer <== keccak.out;

    signal output blockHash;
    component bits2num = Bits2Num(32 * 8);
    bits2num.in <== keccakHeaderLayer;
    blockHash <== bits2num.out;
}

component main = MptFirst(5);