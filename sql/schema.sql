-- Dimension Table
CREATE TABLE dim_fund (
    amfi_code INTEGER PRIMARY KEY,
    scheme_name TEXT,
    fund_house TEXT,
    category TEXT,
    sub_category TEXT,
    plan TEXT,
    fund_manager TEXT,
    risk_category TEXT,
    expense_ratio_pct REAL
);

-- Date Dimension
CREATE TABLE dim_date (
    date_id INTEGER PRIMARY KEY AUTOINCREMENT,
    date DATE UNIQUE,
    year INTEGER,
    month INTEGER,
    quarter INTEGER,
    is_weekday INTEGER
);

-- NAV Fact Table
CREATE TABLE fact_nav (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    amfi_code INTEGER,
    date DATE,
    nav REAL,
    FOREIGN KEY(amfi_code) REFERENCES dim_fund(amfi_code)
);

-- Transaction Fact Table
CREATE TABLE fact_transactions (
    tx_id INTEGER PRIMARY KEY AUTOINCREMENT,
    investor_id TEXT,
    transaction_date DATE,
    amfi_code INTEGER,
    transaction_type TEXT,
    amount_inr REAL,
    state TEXT,
    city TEXT,
    gender TEXT,
    kyc_status TEXT,
    FOREIGN KEY(amfi_code) REFERENCES dim_fund(amfi_code)
);

-- Performance Fact Table
CREATE TABLE fact_performance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    amfi_code INTEGER,
    return_1yr REAL,
    return_3yr REAL,
    return_5yr REAL,
    alpha REAL,
    beta REAL,
    sharpe_ratio REAL,
    sortino_ratio REAL,
    std_dev_ann REAL,
    max_drawdown_pct REAL,
    FOREIGN KEY(amfi_code) REFERENCES dim_fund(amfi_code)
);

-- AUM Table
CREATE TABLE fact_aum (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fund_house TEXT,
    year INTEGER,
    quarter INTEGER,
    aum_crore REAL
);