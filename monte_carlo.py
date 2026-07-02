from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent
NAV_PATH = ROOT / 'data' / 'processed' / '02_nav_history_cleaned.csv'


def simulate_nav_growth(amfi_code: int, years: int = 5, simulations: int = 1000, annual_return: float | None = None, annual_volatility: float | None = None):
    nav = pd.read_csv(NAV_PATH)
    nav['date'] = pd.to_datetime(nav['date'])
    fund_nav = nav[nav['amfi_code'] == amfi_code].sort_values('date')
    if fund_nav.empty:
        raise ValueError('AMFI code not found')

    daily_returns = fund_nav['nav'].pct_change().dropna()
    if annual_return is None:
        annual_return = float(daily_returns.mean() * 252)
    if annual_volatility is None:
        annual_volatility = float(daily_returns.std() * np.sqrt(252))

    latest_nav = float(fund_nav['nav'].iloc[-1])
    steps = years * 252
    rng = np.random.default_rng(42)
    drift = np.log(1 + annual_return) - 0.5 * annual_volatility ** 2
    shocks = rng.normal(drift, annual_volatility / np.sqrt(252), size=(simulations, steps))
    log_paths = np.log(latest_nav) + np.cumsum(shocks, axis=1)
    paths = np.exp(log_paths)

    date_index = pd.date_range(fund_nav['date'].iloc[-1] + pd.Timedelta(days=1), periods=steps, freq='B')
    summary = pd.DataFrame(paths.T, index=date_index, columns=[f'sim_{i+1}' for i in range(simulations)])
    return summary


if __name__ == '__main__':
    result = simulate_nav_growth(100016, years=1, simulations=10)
    print(result.head())
