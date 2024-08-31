# Sigma-B

Sigma-B is a set of protocols and cryptographic tools that enable centralized cryptocurrency exchanges to provide **_«Private Proof of Reserves»_**. The private aspect of Sigma-B ensures that exchange addresses, user addresses, and related financial data (such as the total amount of liability) remain confidential. This document delves into the philosophy behind the Sigma-B protocol and its technical details.

## What is Proof of Reserves?

Proof of Reserves enables centralized (custodial) exchanges to prove to their users that **_they hold enough reserves to cover their liabilities to the users_**. Current Proof of Reserves protocols prove two things:

1. The exchange holds n units of a certain currency.
2. The total liabilities of the exchange to the users are less than n.

**_To prove the first part_**, exchanges had no choice but to publicly disclose their wallet addresses. Users can verify the balance of these addresses and sum them up to determine n. Sigma-B offers an innovative solution that allows exchanges to prove they own n units of currency without revealing their addresses.

To prove the second part, assume Nobitex has a list where each row contains a user ID and their custodial wallet balance. We call this the liability list , Nobitex can publicly release this list. Users can view the list and confirm their presence. Once confirmed, users can calculate the total assets in the list (total liability) and ensure this amount is less than the exchange's reserves (n).

- If the liability exceeds the reserves, Nobitex clearly fails in proving its reserves.
- If your name is not on the list, it means Nobitex has not accounted for your liability, raising the possibility that Nobitex does not hold enough reserves to cover its liability to users.

(Note: Users must also ensure that Nobitex's announced liability list remains constant over time and is not altered upon each inquiry. Otherwise, Nobitex could publish a list containing your name, convince you, and then replace your name with someone else's to convince them.)

## Privacy of the liability List

Clearly, publicly disclosing the liability list is not feasible as it would seriously infringe on the privacy of Nobitex's users. If the liability list were public, everyone could see the cryptocurrency balances of all users.

## Hash Function

A hash function is a mathematical function that takes an input of any size and produces a fixed-size output. This function has the following properties:

- The smallest change in the input causes a significant change in the output.
- Finding the input from the output is extremely difficult and almost impossible.

## Cryptographic Commitment

Suppose Alice and Bob want to play "rock-paper-scissors" over the phone. Unfortunately, there is always a possibility that Bob, upon hearing Alice's choice, quickly announces his own choice based on hers to always win. Bob could blame the delay in his announcement on the phone's audio delay.

Given the one-way nature of secure hash functions, Alice and Bob can commit to their choices without revealing them. For example:

Alice and Bob can hash their choices and announce these hash values to each other, committing to their choices. After exchanging commitments, they can reveal their actual choices without any concern, and the winner is determined. Alice and Bob can then hash their actual choices and compare them with the initial commitments to ensure they both stuck to their original choices. If either one deviates from their commitment, they are declared the loser.

## Zero-Knowledge Proof

Suppose f is a function that takes several inputs and produces one output. Zero-knowledge proofs are cryptographic protocols that allow us to prove we know inputs to f that yield a specific output. Using zero-knowledge proofs and cryptographic commitments, we can design a "private liability list."

## Private liability List

Suppose instead of publicly releasing the liability list, we hash it and publish the hash value. This way, we commit to the liability list. Now, assume we have a function f1 with the following specifications:

$`f_1(L, i) = (h(L), \sum_{k}{L[k]_{balance}}, L[i]_{id}, L[i]_{balance})`$

This function takes a liability list L and an index i as inputs and returns a four-tuple:

- $`h(L)`$ is the hash of the liability list.
- $`\sum_{k}{L[k]_{balance}}`$ is the sum of all liabilities in the list.
- $`L[i]_{id}`$ is the ID of the i-th user in the liability list.
- $`L[i]_{balance}`$ is the balance of the i-th user in the liability list.

Now, suppose Nobitex first creates the liability list L based on its user list and publicly announces its hash ($`C=h(L)`$). It then uses zero-knowledge proofs to demonstrate that it knows inputs to f1 that produces the output $`(C,T,K,V)`$. If the output $`C`$ matches the initially announced $`C`$, Nobitex has essentially proven that:

- Firstly: The sum of user balances is $`T`$
- Secondly: There is a person in the list with ID $`k`$.
- Thirdly: The balance of that person in the list is $`v`$.

Alice, by receiving this proof and verifying that $`C`$ matches the commitment Nobitex previously announced, is convinced that when Nobitex committed to the liability list, Alice (with ID $`K`$) and her $`V`$ units of cryptocurrency were also considered. Alice also realizes that the total liability announced by Nobitex is $`T`$.

Alice can compare $`T`$ with Nobitex's total reserves $`n`$.

## Privatizing Nobitex's Reserves

As mentioned earlier, Sigma-B's strength over other protocols lies in its ability to prove reserves without revealing exchange addresses.

## Account-based Blockchains

Bitcoin, the first cryptocurrency to introduce blockchain technology, follows the UTXO architecture. In this architecture, individuals do not own "accounts"; they own "coins" that can be split into smaller coins with different owners. In this model, a person can make a Bitcoin payment by splitting their coin into two smaller coins: one for the recipient and one for the remaining balance, which goes back to the payer.

After Bitcoin, other blockchains were introduced that used a different architecture: instead of individuals owning coins of varying values, each person has an account whose balance changes with transactions. Each account is also linked to a public key.

## Private Balance List

Some account-based blockchains (like Ethereum) also announce the hash of all existing accounts in their blocks. This value is published as stateRoot and can be considered a commitment to the balance list of all Ethereum accounts.

Consider the function $`f_2`$ with the following specifications:

$`f_2(A,i,sig) = (h(A), A[i]_{balance}, verifySig(A[i]_{pubkey}, \text{"I am nobitex.ir!"}, sig))`$

This function takes a list of public keys and balances of all Ethereum accounts ($`A`$), an index ($`i`$), and a signature ($`sig`$) as inputs, and returns a three-tuple:

- $`h(A)`$ is the hash of the balance list of all Ethereum accounts.
- $`A[i]_{balance}`$ is the balance of the i-th account.
- $`verifySig(A[i]_{pubkey}, \text{"I am nobitex.ir!"}, sig)`$ is a boolean value indicating whether the i-th account correctly signed the message $`\text{"I am nobitex.ir!"}`$ with $`sig`$.

Successfully proving knowledge of the inputs to $`f_2`$ that return the tuple $(C, B, 1)$ means that:

proving we own an account in Ethereum with a balance of $`B`$.

We also need to ensure that the value $`C`$ matches the stateRoot value published by Ethereum nodes.

Nobitex can generate several proofs, each showing that Nobitex owns B i units of cryptocurrency. Users can sum these proven balances to determine Nobitex's total holdings and check that this amount exceeds Nobitex's liabilities.

### Duplicate Accounts

The current protocol has a serious issue: Nobitex could generate multiple proofs for one of its accounts and claim that the balances belong to different accounts. Since account addresses are hidden, there's no way to ensure the accounts are unique. A clever solution to this problem involves modifying $`f_2`$ function as follows:

$`f_2(A,i,sig,salt) = (h(A), A[i]_{balance}, verifySig(A[i]_{pubkey}, \text{"I am nobitex.ir!"}, sig), h(A[i]_{pubkey}, salt))`$

We add a $`salt`$ value to the inputs and include the hash $`h(A[i]_{pubkey}, salt)`$ in the outputs. This value is fixed for each public key (we cannot generate different proofs for a fixed public key using f2 that produce different fourth outputs). This ensures we can detect duplicate accounts.

Due to the properties of hash functions, it's impossible to derive $`A[i]_{pubkey}`$ from $`h(A[i]_{pubkey}, salt)`$ (assuming `salt` is a random value). Thus, while preventing duplicate public keys, the public key remains private, provided the $`salt`$ value remains secret but consistent across all proofs. We can ensure this by including a cryptographic commitment of $`salt`$ in the outputs:

$`f_2(A,i,sig,salt) = (h(A), A[i]_{balance}, verifySig(A[i]_{pubkey}, \text{"I am nobitex.ir!"}, sig), h(A[i]_{pubkey}, salt), h(salt))`$

### Privatizing Balances

If you notice, in this protocol, while hiding the exchange addresses, the total assets of Nobitex are still disclosed. Various reasons could explain why Nobitex might not want to reveal its total assets. Just as we encrypted the public key, we can encrypt the balance as well. Instead of returning $`A[i]_{balance}`$ In the second output, we return $`h(A[i]_{balance},salt)`$ .

If we do this, the verifier can no longer sum the balances to determine the total, as they are encrypted values. We can introduce a third function, $`f_3`$, to prove the sum of the encrypted values $`a`$ and $`b`$ equals the encrypted value $`a+b`$:

$`f_3(a,b,salt) = (h(a, salt), h(b, salt), h(a + b, salt))`$

Using multiple proofs of f3, we can prove that the total Nobitex assets equal the encrypted value Bencoded.

Now we also return the encrypted total liability instead of the total liability. We can use a fourth function to ensure the encrypted assets are greater than the encrypted liability. **_In this way, Nobitex can prove it holds enough reserves to cover its liabilities without revealing the exact amount of its reserves or liabilities._**

## Trusted-Setup

Unfortunately, before zkSNARKs zero-knowledge protocols can be used to generate proofs, a series of "initial parameters" must be generated during a process known as Trusted-Setup. **_This process must be done by several independent people. If the initial parameters are produced by only one person, that person has the ability to create fake proof._**

During the process of participation in the production of initial parameters, an data is produced that must be destroyed after participation. **_For the protocol to be secure, at least one participant should dispose of their random entropy._** fake proofs can only be produced if all participants intentionally keep their random entropy, and generate the proofs together. This situation is very unlikely, unless the number of participants is small. Participants in this process can generate parameters in an isolated computer to further ensure that no entropy is exposed!

### Participants

List of people who participated in the Sigma-B Trusted-Setup process:

- [Keyvan Kambakhsh](https://github.com/keyvank)
- [Mohammadali Heydari](https://github.com/ostadgeorge)
- [Pardis Toolabi](https://github.com/toolabi)
- [Hamid Bateni](https://github.com/irnb)
- [Alireza Moftakhar](https://github.com/alirezamft)
- [Amirhossein Azarpoor](https://github.com/AmirH-A)
- [Amirhossein Hasanini](https://github.com/am1rh0ss3in)
- [Amirali Azarpoor](https://github.com/amalaz)
- [Mohammadsohrab Sameni](https://github.com/sohrabsameny)
- [Nima Yazdanmehr](https://github.com/n1rna)
- [Parisa Hassanizade](https://github.com/parizad1188)
- [Shahriar Ebrahimi](https://github.com/lovely-necromancer)
- [Siyavash tafazoli](https://github.com/SiavashTafazoli)
- [Pedram Mirshah](https://github.com/itsspedram)
- [Abbas Ashtiani](https://github.com/abbasashtiani)
- [Ali Maghsoudi](https://github.com/Alitelepromo)
- [Arash Fatahzade](https://github.com/iRhonin)
- [Omid Mesgarha](https://github.com/armagg)
