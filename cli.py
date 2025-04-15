import os
from main import main
from validator.loader import load_excel_file
from pathlib import Path

def run_with_custom_file():
    custom_path = input("Enter the full path to the recap Excel file: ").strip()
    if not os.path.exists(custom_path):
        print("❌ File not found.")
        return
    print(f"\n▶️ Running validation on: {custom_path}\n")
    # Temporarily overwrite sample_recap.xlsx with the custom file
    from shutil import copyfile
    copyfile(custom_path, "data/sample_recap.xlsx")
    main()

def view_file(path):
    # Display the contents of a given file if it exists
    if os.path.exists(path):
        with open(path, "r") as file:
            print("\n--- File Content ---\n")
            print(file.read())
    else:
        print("❌ File not found.")

def dry_run():
    # Run validation without generating any output files
    print("🧪 Performing dry run (no files will be written)...\n")
    from validator.loader import (
        load_recap_file, load_valid_accounts,
        load_contract_codes, load_broker_codes
    )
    from validator.checks import run_all_validations

    recap_df = load_recap_file()
    accounts_df = load_valid_accounts()
    contracts_df = load_contract_codes()
    brokers_df = load_broker_codes()

    if recap_df is None:
        print("❌ Recap file could not be loaded.")
        return

    validation_results = run_all_validations(recap_df, accounts_df, brokers_df, contracts_df)

    for i, result in enumerate(validation_results):
        print(f"\nRow {i+1}:")
        for check, passed in result.items():
            status = "✅" if passed else "❌"
            print(f"  {check}: {status}")

def clear_outputs_and_logs():
    # Delete all files inside 'output' and 'logs' folders after user confirmation
    folders = ["output", "logs"]
    confirm = input("Are you sure you want to delete all files in 'output' and 'logs'? (y/n): ").lower()
    if confirm != "y":
        print("Operation cancelled.")
        return
    for folder in folders:
        for file in Path(folder).glob("*"):
            try:
                file.unlink()
            except Exception as e:
                print(f"Could not delete {file}: {e}")
    print("🧹 All output and log files cleared.")

def cli():
    while True:
        # Display CLI menu options
        print("\n🔄 Welcome to the Broker Recap Validator")
        print("1. Run validation with default sample_recap.xlsx")
        print("2. Run validation with custom recap file")
        print("3. View latest summary log")
        print("4. View latest email summary")
        print("5. Run dry validation (no files created)")
        print("6. Clear output and log files")
        print("7. Exit")

        choice = input("\nEnter your choice (1-7): ")

        # Handle user choice
        if choice == "1":
            print("\n▶️ Running validation...\n")
            main()
        elif choice == "2":
            run_with_custom_file()
        elif choice == "3":
            view_file("logs/summary_log.txt")
        elif choice == "4":
            view_file("logs/email_summary.txt")
        elif choice == "5":
            dry_run()
        elif choice == "6":
            clear_outputs_and_logs()
        elif choice == "7":
            print("\n👋 Exiting. Goodbye!")
            break
        else:
            print("❗ Invalid option. Please choose between 1–7.")

if __name__ == "__main__":
    cli()