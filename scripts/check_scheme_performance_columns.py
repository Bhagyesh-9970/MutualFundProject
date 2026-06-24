import pandas as pd

df = pd.read_csv("data/raw/07_scheme_performance.csv")

print("\nColumns:")
print(df.columns)

print("\nFirst 5 Rows:")
print(df.head())

print("\nData Types:")
print(df.dtypes)