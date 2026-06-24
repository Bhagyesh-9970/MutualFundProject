# Data Dictionary

## 01_fund_master.csv

| Column | Data Type | Description |
|----------|----------|------------|
| amfi_code | int | AMFI Scheme Code |
| scheme_name | string | Mutual Fund Scheme Name |
| fund_house | string | AMC Name |
| category | string | Equity/Debt |
| expense_ratio_pct | float | Expense Ratio |
| risk_category | string | Risk Level |

---

## 02_nav_history.csv

| Column | Data Type | Description |
|----------|----------|------------|
| amfi_code | int | Scheme Code |
| date | date | NAV Date |
| nav | float | Net Asset Value |