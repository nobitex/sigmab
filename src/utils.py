import json
from models import ExchangeAccountData, UserAccountData
from tree import SparseMerkleSumTree, LiabilityNode
from field import Field


def load_solvency_data(solvency_data_path):
    data = json.load(open(solvency_data_path, "r"))
    message = data.get("message")
    accounts = data.get("accounts", {})

    exchange_accounts_data = []
    for account_data in accounts.values():
        exchange_account_data = ExchangeAccountData.load(account_data)
        exchange_accounts_data.append(exchange_account_data)

    return message, exchange_accounts_data


def load_liability_data(liability_data_path=None, data=None):
    if data is None:
        with open(liability_data_path, "r") as file:
            data = json.load(file)

    liabilities_data = data.get("liabilities", [])
    res = []
    for idx, item in enumerate(liabilities_data):
        amount = int(item["amount"]) 
        user = UserAccountData(item["id"], amount)
        user.set_value("tree_index", idx)
        res.append(user)

    return res


def build_liability_nodes(liabilities_data):
    liability_nodes = [
        LiabilityNode(
            Field(item.id),
            Field(item.amount),
        )
        for item in liabilities_data
    ]
    return liability_nodes


def build_liability_tree(liability_nodes, depth):
    liability_tree = SparseMerkleSumTree(depth)
    index = 0
    for node in liability_nodes:
        liability_tree.addNode(index, node.id, node.amount)
        index += 1
    return liability_tree
