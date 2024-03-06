from src.utils.field import Field
from src.utils.mimc7 import mimc7
from src.pol.smt import Proof
from src.pol.smt import LiabilityNode
from src.pol.smt import SparseMerkleSumTree
from src.pol.utils import FieldEncoder
from src.pol.utils import id_hash
from array import *
import io, json, os
import subprocess
import hashlib

    
def read_pol_data():
    '''
    Retrieves the proof of liability input data

    Returns:
        liabilitynodes: an array of liability nodes to create the smp.
        solvency_balance: the solvency_balance to complete the proof data.
        solvency_balance_salt: the solvency_balance_salt to complete the proof data.

    '''
    with open('src/pol/liabilities.json', 'r') as file:
        data = json.load(file)

    liabilities_data = data.get('liabilities', [])
    solvency_data = data.get('solvency_data', {})

    liabilitynodes = [LiabilityNode(Field(id_hash(item['id'])), Field(item['amount'])) for item in liabilities_data]

    solvency_balance = solvency_data.get('solvency_balance', 0)
    solvency_balance_salt = solvency_data.get('solvency_balance_salt', '')

    return liabilitynodes, solvency_balance, solvency_balance_salt


#  
def buildLiabilityTree(LiabilityNodes, depth) -> SparseMerkleSumTree:
    
    '''
    creates a sparse merkel sum tree using the SparseMerkleSumTree class
    
    Args:
        LiabilityNodes: an array of liabilities nodes.

    Returns:
        liabilityTree: the created merkle tree using input nodes.

    '''
    
    liabilityTree = SparseMerkleSumTree(depth)
    index = 0
    for node in LiabilityNodes:
        liabilityTree.addNode(index, node.id, node.amount)
        index += 1
    return liabilityTree


def generate_input_json(proof):
    '''
    creates a json file containing the pol input signals
    
    Args:
        proof: an instance of the proof class containing the pol data.

    '''
    ids = list(map(lambda node: node.id, proof.proof_nodes))
    amounts = list(map(lambda node: node.amount, proof.proof_nodes))  
    with io.open("circuit/input.json", "w") as f:
        json.dump(
            {
                "index": Field(proof.index),
                "unique_id": proof.id,
                "amount": testProof.amount,
                "proof_ids": ids,
                "proof_sums": amounts,
                "solvency_balance": proof.solvency_balance,
                "solvency_balance_salt": proof.solvency_balance_salt,
            },
            f,
            cls=FieldEncoder,
        )

# create the pol data
liabilitynodes, solvency_balance, solvency_balance_salt = read_pol_data()
solvency_balance = Field(solvency_balance)
solvency_balance_salt = Field(solvency_balance_salt)
# create the tree
liabilityTree = buildLiabilityTree(liabilitynodes, 10)
# create a test proof
testProof = liabilityTree.createProof(0, solvency_balance, solvency_balance_salt)
# check the hash function
if mimc7(Field(3), Field(11)) == Field(
    20873465551905417246270225393360073881989948543683254892256709153974136274798
):
    print("Hash function is OK!")

# check the test proof
print("Verified:", SparseMerkleSumTree.verifyNode(liabilityTree.root(), testProof))

# generate the cicuits input data
generate_input_json(testProof)