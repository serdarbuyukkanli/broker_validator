# 🧾 Broker Recap Validator

This project validates and formats broker recap Excel files received at the end of each trading day. It ensures that only clean and verified trade data is passed to downstream systems like portfolio management platforms.

---

## 🎯 Purpose

Broker recaps often contain human errors such as typos, incorrect codes, or inconsistent pricing. This tool:

- Loads and parses recap files (`.xlsx`)
- Validates each field using business rules and reference data
- Separates valid and invalid trades
- Outputs structured, cleaned data
- Generates summary logs and email-style reports
- Provides a user-friendly CLI interface

---

## 📦 Project Structure

```
broker_validator/
├── cli.py                       # Command-line interface with multiple options
├── main.py                      # Main script to run the validation flow
├── validator/                   # Core modules
│   ├── loader.py                # Loads input and reference Excel files
│   ├── checks.py                # Field-level validation logic
│   ├── formatter.py             # Formats valid trades for final output
│   └── utils.py                 # Logging and email summary helper
├── data/                        # Input files
│   ├── sample_recap.xlsx        # Example recap file
│   ├── valid_accounts.xlsx
│   ├── contract_codes.xlsx
│   └── broker_codes.xlsx
├── output/                      # Output CSV files
│   ├── cleaned_trades.csv
│   └── rejected_trades.csv
├── logs/                        # Summary & email logs
│   ├── summary_log.txt
│   └── email_summary.txt
├── requirements.txt             # Dependencies
└── README.md
```

---

## ⚙️ Setup

### 1. Create a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate        # On Windows: venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🚀 How to Use

### Option 1 — Run via CLI

```bash
python cli.py
```

#### CLI Menu Options:
1. ✅ Run validation with default `sample_recap.xlsx`  
2. 📁 Run validation with a custom recap file (enter full path)  
3. 📄 View latest validation summary log  
4. 📧 View latest email summary  
5. 🧪 Run in dry mode (validates but does not save output)  
6. 🧹 Clear all files in `output/` and `logs/`  
7. ❌ Exit  

### Option 2 — Run main process directly

```bash
python main.py
```

---

## 📤 Outputs

- `output/cleaned_trades.csv` — All valid, formatted trades  
- `output/rejected_trades.csv` — Trades with validation failures  
- `logs/summary_log.txt` — Summary of each run  
- `logs/email_summary.txt` — Copy-paste ready email report  

---

## ✅ Validation Rules (Full List)

| **Field**                  | **Validation Logic**                                                                                                                                     |
|----------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------|
| `date`                     | Must be a valid date and **not in the future** (must be today or earlier).                                                                              |
| `account`                  | Must exist in `valid_accounts.xlsx` under the column `Portfolio_Code`.                                                                                  |
| `quantity`                 | Must be a numeric (integer or float). Should not be zero. Optional range check can be added depending on commodity.                                     |
| `exec_price`              | Must be a numeric value.                                                                                                                                  |
| `bloomberg_contract_code` | Must exist in `contract_codes.xlsx` under the column `Contract_Code`.                                                                                    |
| `contract_mth`            | Must be one of the standard month codes: `["F", "G", "H", "J", "K", "M", "N", "Q", "U", "V", "X", "Z"]`.                                                  |
| `contract_yr`             | Must be numeric and must be this year or in the future (i.e., not a past year).                                                                          |
| `strike`                  | Must be numeric **only for options** (`F/C/P` = "C" or "P"); can be empty for futures (`F`).                                                             |
| `F/C/P`                   | Must be one of `"F"` (Future), `"C"` (Call), `"P"` (Put). If missing, warning is triggered, and default assumed as `"F"` during formatting.              |
| `executing_broker`        | Must exist in `broker_codes.xlsx` under the column `Broker_Code`.                                                                                        |

### 🧠 Composite / Combined Rules

| **Rule**                                | **Logic**                                                                                      |
|-----------------------------------------|-----------------------------------------------------------------------------------------------|
| **Row validity**                        | A row is only considered **valid** if **all core fields** above pass their checks.            |
| **Strike required for options**         | If `F/C/P` is `"C"` or `"P"`, then `strike` must be filled and numeric.                       |
| **PS_ID & Identifier generation**       | Only done for valid rows. Uses a combination of multiple fields (`code`, `month`, `year`, etc.). |

---

## 👨‍💻 Developer

Serdar Buyukkanli