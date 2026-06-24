import pandas as pd

fund_master = pd.read_csv("data/raw/01_fund_master.csv")
nav_history = pd.read_csv("data/raw/02_nav_history.csv")

master_codes = set(fund_master["amfi_code"])
nav_codes = set(nav_history["amfi_code"])

missing_codes = master_codes - nav_codes

print("\nCodes in fund_master :", len(master_codes))
print("Codes in nav_history :", len(nav_codes))

if len(missing_codes) == 0:
    print("\n✓ All AMFI codes are present in nav_history.")
else:
    print("\nMissing AMFI codes:")
    print(missing_codes)