import pandas as pd

def load_excel_file(file_path):
    """
    Generic Excel file loader.
    Returns None if file can't be read.
    """
    try:
        return pd.read_excel(file_path, engine='openpyxl')
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return None

def load_recap_file():
    """
    Loads the broker recap file.
    """
    return load_excel_file("data/sample_recap.xlsx")

def load_valid_accounts():
    """
    Loads the file containing valid account codes.
    """
    return load_excel_file("data/valid_accounts.xlsx")

def load_contract_codes():
    """
    Loads the file containing valid Bloomberg contract codes.
    """
    return load_excel_file("data/contract_codes.xlsx")

def load_broker_codes():
    """
    Loads the file containing valid broker codes.
    """
    return load_excel_file("data/broker_codes.xlsx")