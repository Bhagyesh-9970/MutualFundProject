import pandas as pd

# Load dataset
df = pd.read_csv("data/raw/08_investor_transactions.csv")

# Display columns
print("\nColumns:")
print(df.columns)

# First 5 rows
print("\nFirst 5 Rows:")
print(df.head())

# Data types
print("\nData Types:")
print(df.dtypes)