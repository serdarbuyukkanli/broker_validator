from validator.loader import (
    load_recap_file,
    load_valid_accounts,
    load_contract_codes,
    load_broker_codes
)
from validator.checks import run_all_validations
from validator.formatter import format_valid_trades
from validator.utils import generate_email_summary

import pandas as pd
from datetime import datetime

def main():
    recap_df = load_recap_file()
    accounts_df = load_valid_accounts()
    contracts_df = load_contract_codes()
    brokers_df = load_broker_codes()

    if recap_df is None or accounts_df is None or contracts_df is None or brokers_df is None:
        print("One or more input files could not be loaded.")
        return

    print("\nRunning validations...")
    validation_results = run_all_validations(recap_df, accounts_df, brokers_df, contracts_df)

    valid_rows = []
    rejected_rows = []

    for i, result in enumerate(validation_results):
        if all(result.values()):
            valid_rows.append(recap_df.iloc[i])
        else:
            rejected_rows.append(recap_df.iloc[i])
            print(f"\nRow {i+1} has validation issues:")
            for check, passed in result.items():
                if not passed:
                    print(f"  ❌ {check} failed")

    valid_df = pd.DataFrame(valid_rows)
    rejected_df = pd.DataFrame(rejected_rows)

    print(f"\nTotal valid rows: {len(valid_df)}")
    print(f"Total rejected rows: {len(rejected_df)}")

    # Save valid trades
    if not valid_df.empty:
        formatted_df = format_valid_trades(valid_df)
        formatted_df.to_csv("output/cleaned_trades.csv", index=False)
        print("\n✅ Cleaned trades written to output/cleaned_trades.csv")

    # Save rejected trades
    if not rejected_df.empty:
        rejected_df.to_csv("output/rejected_trades.csv", index=False)
        print("❌ Rejected trades written to output/rejected_trades.csv")
    else:
        print("✅ No rejected trades.")

    # Generate summary log file
    log_text = f"""--- Validation Summary ---
Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Total trades processed: {len(recap_df)}
Valid trades: {len(valid_df)}
Rejected trades: {len(rejected_df)}
"""

    with open("logs/summary_log.txt", "a") as log_file:
        log_file.write(log_text + "\n")

    print("\n🪵 Summary log written to logs/summary_log.txt")

    # Generate email summary
    email_text = generate_email_summary(len(recap_df), len(valid_df), len(rejected_df))
    # added encoding to avoid encoding issues
    with open("logs/email_summary.txt", "w",encoding="utf-8") as email_file:
        email_file.write(email_text)

    print("\n📬 Email summary written to logs/email_summary.txt")

if __name__ == "__main__":
    main()