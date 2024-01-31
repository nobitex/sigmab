pragma circom 2.1.6;

include "./utils/hasher.circom";

template Bits2Num(len, startIndex, nBits) {
    signal input block[len];
    signal output out;

    var result = 0;
    for(var i = 0; i < nBits; i++) {
        result += (2**i) * block[startIndex + i];
    }

    out <== result;
}

template BitsToNums(numBits, bitsPerNum) {
    var cnt = numBits \ bitsPerNum + (numBits % bitsPerNum != 0 ? 1 : 0);

    signal input inp[numBits];
    signal output out[cnt];

    component converters[cnt];
    for(var i = 0; i < cnt; i++) {
        converters[i] = Bits2Num(numBits, i * bitsPerNum, numBits - i * bitsPerNum < bitsPerNum ? numBits - i * bitsPerNum : bitsPerNum);
        converters[i].block <== inp;
        out[i] <== converters[i].out;
    }
}

template HashBits(numBits, bitsPerNum) {
    signal input inp[numBits];
    signal output out;

    var cnt = numBits \ bitsPerNum + (numBits % bitsPerNum != 0 ? 1 : 0);

    component tonums = BitsToNums(numBits, bitsPerNum);
    tonums.inp <== inp;

    component hashers[cnt];
    signal commits[cnt+1];
    commits[0] <== 0;
    for(var i = 0; i < cnt; i++) {
        hashers[i] = Hasher();
        hashers[i].left <== commits[i];
        hashers[i].right <== tonums.out[i];
        commits[i+1] <== hashers[i].hash;
    }

    out <== commits[cnt];
}