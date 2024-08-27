from ledgereth.web3 import LedgerSignerMiddleware
import time
from web3.auto import w3
from rlp import encode
from pathlib import Path
from ledgereth.accounts import find_account, get_accounts
from ledgereth.messages import sign_message
import os
from dotenv import load_dotenv
from eth_account.messages import encode_defunct, _hash_eip191_message
from eth_account._utils.signing import to_standard_signature_bytes
from ledgerblue.comm import getDongle
from web3 import Web3
from hexbytes import HexBytes
import base64
from eth_account import Account
from eth_utils import to_checksum_address
import ecdsa, io, json, hashlib
from ecdsa import VerifyingKey, SECP256k1, util
from eth_keys import keys
from ledgereth.comms import init_dongle


def get_accounts_data(base_accounts, given_accounts):
    address_to_path = {account.address: account.path for account in base_accounts}

    missing_items = [item for item in given_accounts if item not in address_to_path]
    if missing_items:
        raise ValueError(
            f"The following accounts do not exist in your accounts list: {', '.join(missing_items)}"
        )

    account_info = [
        {"address": account, "path": address_to_path[account]}
        for account in given_accounts
    ]
    return account_info


def read_existing_data(file_path):
    if os.path.exists(file_path):
        try:
            with open(file_path, "r") as file:
                return json.load(file)
        except (json.JSONDecodeError, IOError) as e:
            raise ValueError(f"Error reading data file: {e}")
    return None


def write_data_to_file(file_path, data):
    try:
        with open(file_path, "w") as file:
            json.dump(data, file, indent=4)
    except IOError as e:
        raise ValueError(f"Error writing to data file: {e}")


def check_account_in_data(data, account_address):
    for account in data.get("accounts", {}).values():
        if account["address"] == account_address:
            raise ValueError("The account address is already in the data file.")


def update_data_file(message, data_input, base64_representation, r, s):
    file_path = "solvency_script/solvency_data.json"
    data = read_existing_data(file_path)

    if data:
        if data.get("message") != message:
            raise ValueError(
                "The message in the data file does not match the provided message."
            )
        check_account_in_data(data, data_input)
        num_accounts = len(data.get("accounts", {}))
        next_index = f"account_{num_accounts + 1}"
    else:
        data = {"message": message, "accounts": {}}
        next_index = "account_0"

    new_account = {
        "address": data_input,
        "pubkey": base64_representation,
        "signature": {"r": r, "s": s},
    }
    data["accounts"][next_index] = new_account
    write_data_to_file(file_path, data)


def generate_ledger_signature(message, account):
    try:
        dongle = init_dongle(None)
    except Exception as e:
        raise ValueError(f"Error initializing ledegr: {e}")

    print("Signing with the account :", account["address"])
    print("Sign the message on your ledger...")

    try:
        message_hash = hashlib.sha256(message.encode("utf-8")).digest()
        signature = sign_message(message_hash, account["path"], dongle).signature
        signature = signature[2:]
        r = signature[:64]
        s = signature[64:128]

        # Recover public key from signature
        message_hash_hex = Web3.to_hex(message_hash)
        msg = encode_defunct(hexstr=message_hash_hex)
        message_hash = _hash_eip191_message(msg)
        hash_bytes = HexBytes(message_hash)
        signature_bytes = HexBytes(signature)
        signature_bytes_standard = to_standard_signature_bytes(signature_bytes)
        signature_obj = keys.Signature(signature_bytes=signature_bytes_standard)
        recovered_public_key = signature_obj.recover_public_key_from_msg_hash(
            hash_bytes
        )

        base64_representation = base64.b64encode(recovered_public_key._raw_key).decode(
            "utf-8"
        )

        update_data_file(
            message, account["address"], base64_representation, int(r, 16), int(s, 16)
        )
        print("Signature data generated successfully. ")

    except Exception as e:
        raise ValueError(f"Error generating ledger signature: {e}")


def generate_pk_signature(message, pk, input_address):
    account = Account.from_key(pk)
    pk_address = account.address
    public_key = account._key_obj.public_key
    if input_address != pk_address:
        raise ValueError("The given address does not match the private-key.")
    print("Signing with the account :", input_address)
    try:
        # Prepare the message for signing
        message_hash = hashlib.sha256(message.encode("utf-8")).digest()
        message_hash_hex = Web3.to_hex(message_hash)
        signable = encode_defunct(hexstr=message_hash_hex)
        hashed = _hash_eip191_message(signable)
        private_key_bytes = bytes.fromhex(pk)

        # Create an account object from the private key
        sk = ecdsa.SigningKey.from_string(private_key_bytes, curve=ecdsa.SECP256k1)
        # Sign the hash directly using the eth_keys library
        signature = sk.sign_digest(hashed, sigencode=util.sigencode_string)

        # Decode the signature
        curve_order = SECP256k1.order
        r, s = util.sigdecode_string(signature, curve_order)

        base64_representation = base64.b64encode(public_key.to_bytes()).decode("utf-8")

        update_data_file(message, input_address, base64_representation, r, s)
        print("Signature data generated successfully. ")
        time.sleep(2)
    except Exception as e:
        raise ValueError(f"Error generating PK signature: {e}")
