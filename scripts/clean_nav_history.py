import pandas as pd

# Load dataset
df = pd.read_csv("data/raw/02_nav_history.csv")

print("Original Shape:", df.shape)

# Convert date column to datetime
df["date"] = pd.to_datetime(df["date"])

# Sort by amfi_code and date
df = df.sort_values(by=["amfi_code", "date"])

# Remove duplicate rows
duplicates = df.duplicated().sum()
print("Duplicate rows found:", duplicates)

df = df.drop_duplicates()

# Remove invalid NAV values
df = df[df["nav"] > 0]

# Forward-fill missing NAV values within each scheme
df["nav"] = df.groupby("amfi_code")["nav"].ffill()

# Reset index
df = df.reset_index(drop=True)

print("Final Shape:", df.shape)

# Save cleaned dataset
df.to_csv(
    "data/processed/02_nav_history_cleaned.csv",
    index=False
)

print("Cleaned file saved successfully!")