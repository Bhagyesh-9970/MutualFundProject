import pandas as pd
import os

folder_path = "data/raw"

files = [f for f in os.listdir(folder_path) if f.endswith(".csv")]

print("\nTotal CSV files:", len(files))

for file in files:

    print("\n" + "="*70)
    print("FILE:", file)

    path = os.path.join(folder_path, file)

    df = pd.read_csv(path)

    print("\nShape:")
    print(df.shape)

    print("\nData Types:")
    print(df.dtypes)

    print("\nFirst 5 Rows:")
    print(df.head())

    print("\nMissing Values:")
    print(df.isnull().sum())