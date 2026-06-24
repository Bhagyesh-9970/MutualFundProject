import pandas as pd

# Read nav history dataset
df = pd.read_csv("data/raw/02_nav_history.csv")

# Print column names
print("\nColumns:")
print(df.columns)

# Print first 5 rows
print("\nFirst 5 rows:")
print(df.head())

# Print data types
print("\nData Types:")
print(df.dtypes)