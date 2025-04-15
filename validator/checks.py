import pandas as pd
from datetime import datetime

def validate_account(row, valid_accounts):
    return row['account'] in valid_accounts

def validate_broker(row, valid_brokers):
    return row['executing_broker'] in valid_brokers

def validate_contract_code(row, valid_contracts):
    return row['bloomberg_contract_code'] in valid_contracts

def validate_date(row):
    try:
        trade_date = pd.to_datetime(row['date'])
        return trade_date <= datetime.now()
    except:
        return False

def validate_instrument_type(row):
    return row['F/C/P'] in ["F", "C", "P"]

def run_all_validations(df, accounts_df, brokers_df, contracts_df):
    # should look at Account_Code not Portfolio_Code
    valid_accounts = set(accounts_df["Account_Code"].dropna())
    valid_brokers = set(brokers_df["Broker_Code"].dropna())
    valid_contracts = set(contracts_df["Contract_Code"].dropna())

    results = []
    for _, row in df.iterrows():
        validations = {
            "account": validate_account(row, valid_accounts),
            "broker": validate_broker(row, valid_brokers),
            "contract_code": validate_contract_code(row, valid_contracts),
            "date": validate_date(row),
            "instrument_type": validate_instrument_type(row)
        }
        results.append(validations)

    return results