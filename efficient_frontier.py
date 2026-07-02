from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent
NAV_PATH = ROOT / 'data' / 'processed' / '02_nav_history_cleaned.csv'


def compute_frontier(amfi_codes, risk_free_rate: float = 0.06):
    if not amfi_codes:
        raise ValueError('Provide at least one AMFI code')

    nav = pd.read_csv(NAV_PATH)
    nav['date'] = pd.to_datetime(nav['date'])
    nav = nav.sort_values(['amfi_code', 'date'])

    returns = []
    for code in amfi_codes:
        fund = nav[nav['amfi_code'] == code].sort_values('date')
        if fund.empty:
            raise ValueError(f'AMFI code {code} not found in NAV history')
        fund = fund[['date', 'nav']].copy()
        fund['ret'] = fund['nav'].pct_change()
        returns.append(fund.set_index('date')['ret'].dropna())

    ret_df = pd.concat(returns, axis=1).dropna()
    ret_df.columns = [str(code) for code in amfi_codes]

    mean_returns = ret_df.mean() * 252
    cov_matrix = ret_df.cov() * 252

    rng = np.random.default_rng(42)
    weights = rng.dirichlet(np.ones(len(amfi_codes)), size=3000)
    portfolio_returns = weights @ mean_returns.to_numpy()
    portfolio_volatility = np.sqrt(np.einsum('ij,jk,ik->i', weights, cov_matrix.to_numpy(), weights))
    sharpe_ratio = (portfolio_returns - risk_free_rate) / portfolio_volatility

    best_idx = int(np.argmax(sharpe_ratio))
    best_weights = weights[best_idx]
    best_return = float(portfolio_returns[best_idx])
    best_volatility = float(portfolio_volatility[best_idx])

    return {
        'mean_return': best_return,
        'volatility': best_volatility,
        'cov_matrix': cov_matrix,
        'weights': best_weights,
    }
