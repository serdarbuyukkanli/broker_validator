import numpy as np
import pandas as pd

def format_valid_trades(df):
    df = df.copy()

    # Create fixed columns
    df['Source'] = 'GIVEUP'
    df['Trade_Date'] = df['date']
    df['Account'] = df['account']
    df['Quantity'] = df['quantity']
    df['Trade_Price'] = df['exec_price']
    df['Trade_Type'] = 0
    df['Internal'] = df['executing_broker'] + ' GIVEUP'
    df['Executing_Broker'] = df['executing_broker']
    df['Clearing_Firm'] = ''  # Placeholder for future logic
    df['Execution_Type'] = 'V'

    # If instrument type is missing, default to "F"
    df['F/C/P'] = df['F/C/P'].str.upper().fillna('F')

    # Generate Identifier field
    df['Identifier'] = (
        df['bloomberg_contract_code']
        + df['contract_mth'].str[0]
        + df['contract_yr'].astype(str).str[-1]
        + df['F/C/P']
        + ' ' + df['strike'].astype(str)
        + ' Comdty'
    )

    # Generate PS_ID field
    df['PS_ID'] = (
        df['bloomberg_contract_code']
        + '_' + df['contract_mth'].str[0]
        + '_' + df['contract_yr'].astype(str)
        + '_' + df['strike'].astype(str)
        + df['F/C/P']
    )

    # Return only the required columns in specific order
    return df[[
        'Source', 'Trade_Date', 'Account', 'Quantity', 'Trade_Price',
        'Identifier', 'PS_ID', 'Trade_Type', 'Internal',
        'Executing_Broker', 'Clearing_Firm', 'Execution_Type'
    ]]