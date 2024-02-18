
pragma circom 2.1.6;

template IsZero() {
    signal input in;
    signal output out;

    signal inv;

    inv <-- in!=0 ? 1/in : 0;

    out <== -in*inv +1;
    in*out === 0;
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

template GetByteLength(N) {
    signal input num;
    signal output len;

    signal realBytes[N + 1];
    var realBytesSize = 0;
    realBytes[0] <== 1;

    component byteDecompose = ByteDecompose(N);
    byteDecompose.num <== num;

    component isz[N];
    component isz2[N];
    
    for (var i = 0; i < N; i++) {
        isz[i] = IsZero();
        isz2[i] = IsZero();
        if (i == 0) {
            isz[i].in <== byteDecompose.bytes[N-1]; 
            isz2[i].in <== byteDecompose.bytes[N-i-1];
        } else {
            isz[i].in <== byteDecompose.bytes[N-i];
            isz2[i].in <== byteDecompose.bytes[N-i-1];
        }
        realBytes[i+1] <== 1 - (isz[i].out + isz2[i].out);
    }

    for (var j = 0; j < N; j++) {
        realBytesSize = realBytesSize + realBytes[j];
    }

    len <== realBytesSize;
}