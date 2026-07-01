import pandas as pd
import os
files=['data/processed/02_nav_history_cleaned.csv','data/processed/07_scheme_performance_cleaned.csv','data/processed/08_investor_transactions_cleaned.csv','data/raw/09_portfolio_holdings.csv','data/raw/01_fund_master.csv']
for path in files:
    print('\nFILE', path)
    if os.path.exists(path):
        df=pd.read_csv(path)
        print(df.head(2).to_string())
        print('\nCOLUMNS:', list(df.columns))
        print('ROWS:', len(df))
    else:
        print('MISSING')
