import pandas as pd

# Load dataset
df = pd.read_csv("data/raw/07_scheme_performance.csv")

print("Original Shape:", df.shape)

# Remove duplicates
duplicates = df.duplicated().sum()
print("Duplicate rows found:", duplicates)

df = df.drop_duplicates()

# Numeric columns
numeric_cols = [
    "return_1yr",
    "return_3yr",
    "return_5yr",
    "alpha",
    "beta",
    "sharpe_ratio",
    "sortino_ratio",
    "std_dev_ann",
    "max_drawdown_pct",
    "aum_crore",
    "expense_ratio_pct"
]

# Convert to numeric
for col in numeric_cols:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

# Expense ratio validation
anomalies = df[
    (df["expense_ratio_pct"] < 0.1) |
    (df["expense_ratio_pct"] > 2.5)
]

print("\nExpense ratio anomalies found:", len(anomalies))

# Save cleaned file
df.to_csv(
    "data/processed/07_scheme_performance_cleaned.csv",
    index=False
)

print("Final Shape:", df.shape)
print("Cleaned file saved successfully!")