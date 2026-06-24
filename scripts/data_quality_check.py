import pandas as pd
import os

folder_path = "data/raw"

files = [f for f in os.listdir(folder_path) if f.endswith(".csv")]

for file in files:

    print("\n", "="*50)
    print(file)

    df = pd.read_csv(os.path.join(folder_path, file))

    print("\nMissing values:")
    print(df.isnull().sum())

    print("\nDuplicate rows:", df.duplicated().sum())