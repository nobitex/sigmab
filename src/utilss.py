import json
from models import ExchangeAccountData

def load_solvency_data(solvency_data_path):
    data = json.load(open(solvency_data_path, 'r'))
    message = data.get('message')
    accounts = data.get('accounts', {})
    
    exchange_accounts_data = []
    for account_data in accounts.values():
        exchange_account_data = ExchangeAccountData.load(account_data)
        exchange_accounts_data.append(exchange_account_data)

    return message, exchange_accounts_data
