from ledgereth.web3 import LedgerSignerMiddleware
import time, hashlib
from web3.auto import w3
import os
from dotenv import load_dotenv
from eth_account import Account
from utils import (
    check_accounts,
    generate_ledger_signature,
    generate_pk_signature
)


def ledger_sign(message):
    print("Signing with ledger is selected.")
    print("Unlock your ledger.")
    data_input = input("Enter a list of your account addresses for ledger sign (comma-separated & without space): ")
    input_accounts = data_input.split(',')
    # ledger data
    try:
        w3.middleware_onion.add(LedgerSignerMiddleware)
        ledger_accounts = w3.eth.accounts
    except Exception as e:
        raise ValueError(f"Error: Locked ledger. ")

    
    # check validty of the input data
    check_accounts(ledger_accounts, input_accounts)    

    for account in input_accounts:
        generate_ledger_signature(message, account)
        

def pk_sign(message):
    print("Signing with private key is selected.") 
    print("Make sure the accounts' private keys exist in the .env file like the example below:")
    print('''PK0="your_first_private_key"\nPK1="your_second_private_key"''')
        
    load_dotenv()
        
    data_input = input("Enter the accounts address you wish to sign with(comma-separated & without space): ")
    time.sleep(2)
    input_accounts = data_input.split(',')
    
    for i in range(0, len(input_accounts)):  
        pk = os.getenv(f"PK{i}")
        if pk:
            if pk.startswith("0x"):
                pk = pk[2:]
            generate_pk_signature(message, pk, input_accounts[i])
        else:
            raise ValueError(f"The PK{i} does not exist.")

    
def main():
    
    message = 'I am Nobitex.'
    message_hash = hashlib.sha256(message.encode("utf-8")).digest()
    
    print(f"The message: {message}")
    print(f'''Signing the message hash: \n{message_hash}''')
    print("1. Sign with ledger")
    print("2. Sign with private key")
    
    choice = input("Enter 1 or 2: ")
    if choice == '1':
        ledger_sign(message)
    elif choice == '2':
        pk_sign(message)
    else:
        print("Invalid choice. Please run the script again and choose 1 or 2.")


if __name__ == "__main__":
    main()

