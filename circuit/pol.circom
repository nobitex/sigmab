pragma circom 2.1.6;

include "./utils/hasher.circom";

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

template CSwap() {
    signal input a;
    signal input b;
    signal input swap;
    signal output l;
    signal output r;
    l <== (b - a) * swap + a;
    r <== (a - b) * swap + b;
}

template CombineNode() {
    signal input a_id;
    signal input a_sum;
    signal input b_id;
    signal input b_sum;
    signal output out_id;
    signal output out_sum;

    component a_hasher = Hasher();
    a_hasher.left <== a_id;
    a_hasher.right <== a_sum;

    component b_hasher = Hasher();
    b_hasher.left <== b_id;
    b_hasher.right <== b_sum;

    component id_calc = Hasher();
    id_calc.left <== a_hasher.hash;
    id_calc.right <== b_hasher.hash;
    out_id <== id_calc.hash;

    out_sum <== a_sum + b_sum;

    component range_check_a = BitDecompose(100);
    range_check_a.num <== a_sum;

    component range_check_b = BitDecompose(100);
    range_check_b.num <== b_sum;
}

template SmstProofVerifier(depth) {
    signal input index;
    signal input unique_id;
    signal input amount;

    signal input proof_ids[depth];
    signal input proof_sums[depth];

    signal input solvency_balance;
    signal input solvency_balance_salt;

    signal output commit_liability;
    signal output commit_solvency_balance;

    signal index_bits[depth];
    component index_decom = BitDecompose(depth);
    index_decom.num <== index;
    index_bits <== index_decom.bits;

    component combiners[depth];
    component id_swappers[depth];
    component sum_swappers[depth];
    signal ids[depth + 1];
    signal sums[depth + 1];
    ids[0] <== unique_id;
    sums[0] <== amount;
    for(var i = 0; i < depth; i++) {
        combiners[i] = CombineNode();

        id_swappers[i] = CSwap();
        id_swappers[i].a <== ids[i];
        id_swappers[i].b <== proof_ids[i];
        id_swappers[i].swap <== index_bits[i];

        sum_swappers[i] = CSwap();
        sum_swappers[i].a <== sums[i];
        sum_swappers[i].b <== proof_sums[i];
        sum_swappers[i].swap <== index_bits[i];

        combiners[i].a_id <== id_swappers[i].l;
        combiners[i].b_id <== id_swappers[i].r;
        combiners[i].a_sum <== sum_swappers[i].l;
        combiners[i].b_sum <== sum_swappers[i].r;
        ids[i+1] <== combiners[i].out_id;
        sums[i+1] <== combiners[i].out_sum;
    }

    component liability_commiter = Hasher();
    liability_commiter.left <== ids[depth];
    liability_commiter.right <== sums[depth];
    commit_liability <== liability_commiter.hash;

    component solvency_balance_commiter = Hasher();
    solvency_balance_commiter.left <== solvency_balance;
    solvency_balance_commiter.right <== solvency_balance_salt;
    commit_solvency_balance <== solvency_balance_commiter.hash;

    // Check if sums[depth] <= solvencyBalance
    component less_eq_checker = LessEqThan(252);
    less_eq_checker.in[0] <== sums[depth];
    less_eq_checker.in[1] <== solvency_balance;
    less_eq_checker.out === 1;
}

component main { public [unique_id, amount] } = SmstProofVerifier(10);