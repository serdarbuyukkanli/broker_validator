from datetime import datetime

def generate_email_summary(total, valid, rejected):
    summary = f"""Subject: Recap Validation Summary - {datetime.now().strftime('%Y-%m-%d')}

Hi Team,

Here is the summary of today's broker recap validation:

- Total trades processed: {total}
- ✅ Valid trades: {valid}
- ❌ Rejected trades: {rejected}

Please find the attached files for:
- Cleaned trades (cleaned_trades.csv)
- Rejected trades (rejected_trades.csv)
- Summary log (summary_log.txt)

Best regards,  
Automated Recap Validator
"""
    return summary