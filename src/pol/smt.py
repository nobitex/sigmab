from utils.field import Field
from utils.mimc7 import mimc7

class LiabilityNode:
    def __init__(self, id, amount):
        self.id = id
        self.amount = amount

    def hash(self):
        return mimc7(self.id, self.amount)

    def combine(a, b):
        combined_id = mimc7(a.hash(), b.hash())
        combined_amount = a.amount + b.amount
        return LiabilityNode(combined_id, combined_amount)

    def __str__(self):
        return f"LiabilityNode(Id: {self.id}, Amount: {self.amount})"



class Proof:
    def __init__(self, index, id, amount, proof_nodes, solvency_balance, solvency_balance_salt):
        self.index = index
        self.id = id
        self.amount = amount
        self.proof_nodes = proof_nodes
        self.solvency_balance = solvency_balance
        self.solvency_balance_salt = solvency_balance_salt
    
    def __str__(self):
        nodes_str = ", ".join(str(node) for node in self.proof_nodes)
        return f"Proof (Index: {self.index}, Id: {self.id}, Amount: {self.amount}, Nodes: {nodes_str}, solvency_balance: {self.solvency_balance}, solvency_balance_salt: {self.solvency_balance_salt})"

class SparseMerkleSumTree:
    def __init__(self, depth):
        self.depth = depth
        self.levels = [dict() for _ in range(depth + 1)]
        self.defaults = [LiabilityNode(Field(0), Field(0))]
        for _ in range(depth):
            self.defaults.insert(0, LiabilityNode.combine(self.defaults[0], self.defaults[0]))
            
    def addNode(self, index, id, amount):
        layer = self.depth
        curr = LiabilityNode(id, amount)
        self.levels[layer][index] = curr
        for _ in range(self.depth):
            if index % 2 == 0:
                sibling = self.getNode(layer, index + 1)
                new_parent = LiabilityNode.combine(curr, sibling)
            else:
                sibling = self.getNode(layer, index - 1)
                new_parent = LiabilityNode.combine(sibling, curr)
            index //= 2
            layer -= 1
            curr = new_parent
            self.levels[layer][index] = new_parent

    def getNode(self, layer, index) -> LiabilityNode:
        return self.levels[layer].get(index, self.defaults[layer])

    def verifyNode(root: LiabilityNode, proof: Proof) -> bool:
        index = proof.index
        curr = LiabilityNode(proof.id, proof.amount)
        for i, proof_node in enumerate(proof.proof_nodes):
            if index % 2 == 0:
                curr = LiabilityNode.combine(curr, proof_node)
            else:
                curr = LiabilityNode.combine(proof_node, curr)
            index //= 2
        return curr.id == root.id and curr.amount == root.amount

    def createProof(self, index, solvency_balance, solvency_balance_salt) -> Proof:
        curr_index = index
        leaf = self.getNode(self.depth, curr_index)
        proof_nodes = []
        for i in range(self.depth):
            if curr_index % 2 == 0:
                sibling = self.getNode(self.depth - i, curr_index + 1)
            else:
                sibling = self.getNode(self.depth - i, curr_index - 1)
            proof_nodes.append(sibling)
            curr_index //= 2
        return Proof(index, leaf.id, leaf.amount, proof_nodes, solvency_balance, solvency_balance_salt)


    def root(self):
        return self.getNode(0, 0)
    
    def createCommitment(self):
        return mimc7(self.root().id, self.root().amount)