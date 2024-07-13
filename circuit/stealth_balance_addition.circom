pragma circom 2.1.5;

include "./utils/hasher.circom";


template StealthBalanceAddition(NUM_BALANCE) {
    signal input balances[NUM_BALANCE];
    signal input salt;
    signal output coins[NUM_BALANCE];

    component range_checkers[NUM_BALANCE];
    component coinHasher[NUM_BALANCE];
    for(var i = 0; i < NUM_BALANCE; i++) {
        coinHasher[i] = Hasher();
        coinHasher[i].left <== balances[i];
        coinHasher[i].right <== salt;
        coins[i] <== coinHasher[i].hash;

        range_checkers[i] = BitDecompose(100);
        range_checkers[i].num <== balances[i];
    }

    signal output sumOfBalancesCoin;

    var sum = 0;
    for(var i = 0; i < NUM_BALANCE; i++) {
        sum += balances[i];
    }

    component sumHasher = Hasher();
    sumHasher.left <== sum;
    sumHasher.right <== salt;
    sumOfBalancesCoin <== sumHasher.hash;
}

component main = StealthBalanceAddition(2);
