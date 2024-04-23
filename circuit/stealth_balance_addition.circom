pragma circom 2.1.5;

include "./utils/hasher.circom";


template StealthBalanceAddition(NUM_BALANCE) {
    signal input balances[NUM_BALANCE];
    signal input salts[NUM_BALANCE];
    signal output coins[NUM_BALANCE];

    component coinHasher[NUM_BALANCE];
    for(var i = 0; i < NUM_BALANCE; i++) {
        coinHasher[i] = Hasher();
        coinHasher[i].left <== balances[i];
        coinHasher[i].right <== salts[i];
        coins[i] <== coinHasher[i].hash;
    }

    signal input sumOfBalancesSalt;
    signal output sumOfBalancesCoin;

    var sum = 0;
    for(var i = 0; i < NUM_BALANCE; i++) {
        sum += balances[i];
    }

    component sumHasher = Hasher();
    sumHasher.left <== sum;
    sumHasher.right <== sumOfBalancesSalt;
    sumOfBalancesCoin <== sumHasher.hash;

    // check the balance commmitments generated match the ones from mpt_last
    signal input balanceCommitments[NUM_BALANCE];
    for(var i = 0; i < NUM_BALANCE; i++) {
        balanceCommitments[i] === coins[i];
    }



}

component main = StealthBalanceAddition(2);
