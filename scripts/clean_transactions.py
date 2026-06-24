import pandas as pd

# Load dataset
df = pd.read_csv("data/raw/08_investor_transactions.csv")

print("Original Shape:", df.shape)

# Convert transaction_date to datetime
df["transaction_date"] = pd.to_datetime(df["transaction_date"])

# Remove duplicates
duplicates = df.duplicated().sum()
print("Duplicate rows found:", duplicates)

df = df.drop_duplicates()

# Keep only positive amounts
df = df[df["amount_inr"] > 0]

# Standardize transaction types
df["transaction_type"] = (
    df["transaction_type"]
    .str.strip()
    .str.title()
)

# Valid transaction types
valid_types = ["Sip", "Lumpsum", "Redemption"]

df = df[df["transaction_type"].isin(valid_types)]

# Standardize KYC status
df["kyc_status"] = (
    df["kyc_status"]
    .str.strip()
    .str.title()
)

valid_kyc = ["Verified", "Pending"]

df = df[df["kyc_status"].isin(valid_kyc)]

# Reset index
df = df.reset_index(drop=True)

print("Final Shape:", df.shape)

# Save cleaned file
df.to_csv(
    "data/processed/08_investor_transactions_cleaned.csv",
    index=False
)

print("Cleaned transactions file saved successfully!")