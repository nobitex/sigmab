# Proof of Liability Circuits

Proof of Liability is provided through a zkSNARKs circuit, proving existence of a merkle-leaf including a tuple of Id/Amount, in a Sparse-Merkle-Sum-Tree.

A Sparse-Merkle-Sum-Tree is a tree with a fixed depth (And thus fixed number of leaves, in our case \\(2^{30}\\)), where all leaves are \\((0, 0)\\) (Id: 0, Amount: 0) by default. Given a pair of leaves/nodes \\((id_a, amount_a)\\) and \\((id_b, amount_b)\\), the parent node is calculated using the formula below:

- \\(id_{parent} = h(h(id_a, amount_a), h(id_b, amount_b))\\)
- \\(amount_{parent} = amount_a + amount_b\\)

Where \\(h\\) is a arity-2 SNARK-friendly hash function. (In our case, MiMC7 hash function)

Assuming \\((id_{root}, amount_{root})\\) is the root-node of this tree, we would like to prove that \\(amount_{root} < amount_{solvency}\\).

The mentioned zkSNARK circuit will accept a Liability-tree commitment (Which is \\(h(id_{root}, amount_{root})\\)) and an obfuscated solvency-balance (Which is \\(h(amount_{solvency}, salt)\\)) as its public input, and will prove that a liability entry exists in the tree, which its root's balance is less than the obfuscated solvency balance.