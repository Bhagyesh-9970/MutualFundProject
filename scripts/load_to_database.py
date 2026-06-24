import pandas as pd
from sqlalchemy import create_engine

# Create SQLite connection
engine = create_engine("sqlite:///bluestock_mf.db")

# ==========================
# Load Fund Master
# ==========================
fund_df = pd.read_csv("data/raw/01_fund_master.csv")
fund_df.to_sql("dim_fund", engine, if_exists="replace", index=False)

# ==========================
# Load NAV History
# ==========================
nav_df = pd.read_csv("data/processed/02_nav_history_cleaned.csv")
nav_df.to_sql("fact_nav", engine, if_exists="replace", index=False)

# ==========================
# Load Transactions
# ==========================
tx_df = pd.read_csv("data/processed/08_investor_transactions_cleaned.csv")
tx_df.to_sql("fact_transactions", engine, if_exists="replace", index=False)

# ==========================
# Load Scheme Performance
# ==========================
perf_df = pd.read_csv("data/processed/07_scheme_performance_cleaned.csv")
perf_df.to_sql("fact_performance", engine, if_exists="replace", index=False)

# ==========================
# Load AUM
# ==========================
aum_df = pd.read_csv("data/raw/03_aum_by_fund_house.csv")
aum_df.to_sql("fact_aum", engine, if_exists="replace", index=False)

print("All tables loaded successfully!")