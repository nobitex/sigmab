from web3 import Web3
import rlp

import mpt_last
import mpt_path

SALT = 123


def get_account_eth_mpt_proof(account, provider):
    w3 = Web3(Web3.HTTPProvider(provider))

    num = w3.eth.get_block_number()

    b = w3.eth.get_block(num)
    p = w3.eth.get_proof(account, [], num)

    for index, level in enumerate(p.accountProof):
        if index == 0:
            if Web3.keccak(level) != b.stateRoot:
                raise Exception("Not verified!")
        if index >= 1:
            if Web3.keccak(level) not in p.accountProof[index - 1]:
                raise Exception("Not verified!")
            print(mpt_path.get_mpt_path_proof(SALT, level, p.accountProof[index - 1]))

    accountRlp = rlp.encode([p.nonce, p.balance, p.storageHash, p.codeHash])
    prefixAccountRlp = p.accountProof[-1][: -len(accountRlp)]

    if Web3.keccak(prefixAccountRlp + accountRlp) not in p.accountProof[-2]:
        raise Exception("Not verified!")

    print(mpt_last.get_last_proof(SALT, bytes(prefixAccountRlp), bytes(accountRlp)))


get_account_eth_mpt_proof(
    "0x71C7656EC7ab88b098defB751B7401B5f6d8976F",
    "https://yolo-shy-fog.discover.quiknode.pro/97f7aeb00bc7a8d80c3d4834a16cd9c86b54b552/",
)
print("OK!")
