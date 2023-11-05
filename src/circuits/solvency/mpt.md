# Merkle-Patricia-Trie Proof Verifier

Instead of implementing all of the RLP-related logic in our Merkle-Patricia-Trie verifier circuit, we are applying a much simpler approach. The approach involves multiple circuits.

## #1 Layer Checker

We will commit to the data of two layers, using a zk-friendly hash function (Including a salt), and give it as the public input to the circuit. We will then prove that the keccak of one layer is within the upper layer.

### Substring check

We want to prove binary string \\(a\\) exists within binary string \\(b\\).

We can convert \\(a\\) to a field number \\(A=2^0a_0+2^1a_1+ \dots + 2^na_n\\)

- \\(B_{acc, 0} = 2^0b_0\\)
- \\(B_{acc, 1} = B_{acc, 0} + 2^1b_1\\)
- \\(B_{acc, 2} = B_{acc, 1} + 2^2b_2\\)
- \\(B_{acc, 3} = B_{acc, 2} + 2^3b_3\\)
- \\(B_{acc, n} = B_{acc, n-1} + 2^nb_n\\)

We should prove one of the following statements is true:

- \\(B_{acc,256} - B_{acc,0} = 2^0A\\)
- \\(B_{acc,257} - B_{acc,1} = 2^1A\\)
- \\(B_{acc,258} - B_{acc,2} = 2^2A\\)
- \\(B_{acc,259} - B_{acc,3} = 2^3A\\)
- \\(\dots\\)


Public Inputs:

```circom
signal input commitUpperLayer;
signal input commitLowerLayer;
```

## #2 Root Checker

Given commitment and a blockRoot as the public inputs, we will check if the commitment is a correct representation of the stateRoot within the block root.

Public Inputs:

```circom
signal input blockRoot;
signal input commitTopLayer;
```

## #3 Account Checker

We will check if the prover can sign a fresh message, for an account with an obfuscated balance. We will also check if the account exists in a layer given its commitment layer:

Public Inputs:

```circom
signal input commitBottomLayer;
signal input commitBalance;