from ledgereth.web3 import LedgerSignerMiddleware, get_accounts
import time, hashlib
from web3.auto import w3
import os
from dotenv import load_dotenv
from eth_account import Account
from utils import get_accounts_data, generate_ledger_signature, generate_pk_signature


def ledger_sign(message):
    print("Signing with ledger is selected.")
    print("Unlock your ledger.")
    data_input = input(
        "Enter a list of your account addresses for ledger sign (comma-separated & without space): "
    )
    account_counts = int(input("Enter the index of your last accounts: "))
    input_accounts = data_input.split(",")
    try:
        w3.middleware_onion.add(LedgerSignerMiddleware)
        print("loading ledger accounts ... ")
        accounts = get_accounts(count=account_counts + 1)
    except Exception as e:
        error_message = str(e)
        if "0x5515 UNKNOWN" in error_message:
            raise ValueError("Ledger locked due to error: 0x5515 UNKNOWN")
        else:
            raise ValueError(f"Error: {e}")

    accounts_list = get_accounts_data(accounts, input_accounts)
    for account in accounts_list:
        generate_ledger_signature(message, account)


def pk_sign(message):
    print("Signing with private key is selected.")
    print(
        "Make sure the accounts' private keys exist in the .env file like the example below:"
    )
    print('''PK0="your_first_private_key"\nPK1="your_second_private_key"''')

    load_dotenv()

    data_input = input(
        "Enter the accounts address you wish to sign with(comma-separated & without space): "
    )
    time.sleep(2)
    input_accounts = data_input.split(",")

    for i in range(0, len(input_accounts)):
        pk = os.getenv(f"PK{i}")
        if pk:
            if pk.startswith("0x"):
                pk = pk[2:]
            generate_pk_signature(message, pk, input_accounts[i])
        else:
            raise ValueError(f"The PK{i} does not exist.")


def main():
    message = "I am nobitex.ir!"
    message_hash = hashlib.sha256(message.encode("utf-8")).digest()

    print(f"The message: {message}")
    print(f"""Signing the message hash: \n{message_hash}""")
    print("1. Sign with ledger")
    print("2. Sign with private key")

    choice = input("Enter 1 or 2: ")
    if choice == "1":
        ledger_sign(message)
    elif choice == "2":
        pk_sign(message)
    else:
        print("Invalid choice. Please run the script again and choose 1 or 2.")


if __name__ == "__main__":
    main()
