pragma circom 2.0.0;

include "./utils.circom";


template LessThan(n) {
    assert(n <= 252);
    signal input in[2];
    signal output out;

    component n2b = BitDecompose(n+1);

    n2b.num <== in[0]+ (1<<n) - in[1];

    out <== 1-n2b.bits[n];
}

// N is the number of bits the input  have.
// The MSF is the sign bit.
template LessEqThan(n) {
    signal input in[2];
    signal output out;

    component lt = LessThan(n);

    lt.in[0] <== in[0];
    lt.in[1] <== in[1]+1;
    lt.out ==> out;
}

template Mask(n) {
    signal input in[n];
    signal input ind;
    signal output out[n];

    signal eqs[n+1];
    eqs[0] <== 1;
    component eqcomps[n];
    for(var i = 0; i < n; i++) {
        eqcomps[i] = IsEqual();
        eqcomps[i].in[0] <== i;
        eqcomps[i].in[1] <== ind;
        eqs[i+1] <== eqs[i] * (1 - eqcomps[i].out);
    }

    for(var i = 0; i < n; i++) {
        out[i] <== in[i] * eqs[i+1];
    }
}

template Shift(n, maxShift) {
    signal input in[n];
    signal input count;
    signal output out[n + maxShift];

    var outsum[n + maxShift];

    component eqcomps[maxShift + 1];
    signal temps[maxShift + 1][n];
    for(var i = 0; i <= maxShift; i++) {
        eqcomps[i] = IsEqual();
        eqcomps[i].in[0] <== i;
        eqcomps[i].in[1] <== count;
        for(var j = 0; j < n; j++) {
            temps[i][j] <== eqcomps[i].out * in[j];
            outsum[i + j] += temps[i][j];
        }
    }

    for(var i = 0; i < n + maxShift; i++) {
        out[i] <== outsum[i];
    }
}

template Concat(maxLenA, maxLenB) {
    signal input a[maxLenA];
    signal input aLen;

    signal input b[maxLenB];
    signal input bLen;

    signal output out[maxLenA + maxLenB];
    signal output outLen;

    component aLenChecker = LessEqThan(10);
    aLenChecker.in[0] <== aLen;
    aLenChecker.in[1] <== maxLenA;
    aLenChecker.out === 1;

    component bLenChecker = LessEqThan(10);
    bLenChecker.in[0] <== bLen;
    bLenChecker.in[1] <== maxLenB;
    bLenChecker.out === 1;

    component aMasker = Mask(maxLenA);
    aMasker.in <== a;
    aMasker.ind <== aLen;

    component bMasker = Mask(maxLenB);
    bMasker.in <== b;
    bMasker.ind <== bLen;

    var outVals[maxLenA + maxLenB];

    component bShifter = Shift(maxLenB, maxLenA);
    bShifter.count <== aLen;
    bShifter.in <== bMasker.out;

    for(var i = 0; i < maxLenA; i++) {
        outVals[i] += aMasker.out[i];
    }

    for(var i = 0; i < maxLenA + maxLenB; i++) {
        outVals[i] += bShifter.out[i];
    }

    for(var i = 0; i < maxLenA + maxLenB; i++) {
        out[i] <== outVals[i];
    }

    outLen <== aLen + bLen;
}