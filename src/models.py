from web3 import Web3
from consts import PROVIDER
import os


class ExchangeAccountData:
    address: str
    pubkey: str
    signature: str
    context: dict

    def __init__(self, address: str, pubkey: str, signature: str):
        self.address = address
        self.pubkey = pubkey
        self.signature = signature

        self.context = {}

    def set_value(self, key, value):
        self.context[key] = value

    def get_value(self, key):
        return self.context[key]        

    @classmethod
    def load(cls, account_data):
        obj = cls(account_data['address'], account_data['pubkey'], bytes.fromhex(account_data['signature']))
        provider = Web3(Web3.HTTPProvider(PROVIDER))
        balance_wei = provider.eth.get_balance(obj.address)
        obj.set_value('balance', balance_wei)
        return obj

    def __hash__(self):
        return hash(self.address)
