
pragma circom 2.1.5;

template IsZero() {
    signal input in;
    signal output out;

    signal inv;

    inv <-- in!=0 ? 1/in : 0;

    out <== -in*inv +1;
    in*out === 0;
}

template LessEqThan(n) {
    signal input in[2];
    signal output out;

    component lt = LessThan(n);

    lt.in[0] <== in[0];
    lt.in[1] <== in[1]+1;
    lt.out ==> out;
}

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
template GreaterEqThan(n) {
    signal input in[2];
    signal output out;

    component lt = LessThan(n);

    lt.in[0] <== in[1];
    lt.in[1] <== in[0]+1;
    lt.out ==> out;
}

template IsEqual() {
    signal input in[2];
    signal output out;

    component isz = IsZero();

    in[1] - in[0] ==> isz.in;

    isz.out ==> out;
}

template RangeCheck(n) {
    signal input inp;
    signal output out;

    signal select_conds[n+1];
    select_conds[0] <== 1;
    for(var i = 0; i < n; i++) {
        select_conds[i+1] <== select_conds[i] * (inp - i);
    }
    
    component isz = IsZero();
    isz.in <== select_conds[n];
    out <== isz.out;
}

template BitDecompose(N) {
    signal input num;
    signal output bits[N];
    var pow = 1;
    var i = 0;
    var total = 0;
    for(i=0; i<N; i++) {
        bits[i] <-- (num >> i) & 1;
        bits[i] * (bits[i] - 1) === 0;
        total += pow * bits[i];
        pow = pow * 2;
    }
    total === num;
}

template ByteDecompose(N) { 
    signal input num;
    signal output bytes[N];
    var pow = 1;
    var total = 0;
    component bd[N];
    for (var i = 0; i < N; i++) {
        bytes[i] <-- (num >> (8 * i)) & 0xFF;
        bd[i] = BitDecompose(8);
        bd[i].num <==  bytes[i];
        total += pow * bytes[i];
        pow = pow * 256; 
    }

    total === num; 
}

template GetRealByteLength(N) {
    signal input bytes[N];
    signal output len;

    component isZero[N];

    signal isZeroResult[N+1];
    isZeroResult[0] <== 1;

    for (var i = 0; i < N; i++) {
        isZero[i] = IsZero();
        isZero[i].in <== bytes[N-i-1];
        isZeroResult[i+1] <== isZero[i].out * isZeroResult[i];
    }
    
    var total = 0;
    
    for (var j = 1; j < N + 1; j++) {
        total = total + isZeroResult[j];
    }

    len <== N - total;
}

template IfThenElse() {
    signal input condition; 
    signal input ifTrue;
    signal input ifFalse;
    signal output out;


    signal intermediateTrue;
    signal intermediateFalse;

    intermediateTrue <== condition * ifTrue;
    intermediateFalse <== (1 - condition) * ifFalse;

    out <== intermediateTrue + intermediateFalse;
}