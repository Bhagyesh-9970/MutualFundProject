import pandas as pd
import os

# Path to raw data folder
folder_path = "data/raw"

# List all CSV files
files = [f for f in os.listdir(folder_path) if f.endswith(".csv")]

print("\nAvailable files:")
print(files)

for file in files:
    print("\n" + "="*60)
    print(f"FILE: {file}")

    path = os.path.join(folder_path, file)

    df = pd.read_csv(path)

    print("\nShape:")
    print(df.shape)

    print("\nData Types:")
    print(df.dtypes)

    print("\nFirst 5 Rows:")
    print(df.head())