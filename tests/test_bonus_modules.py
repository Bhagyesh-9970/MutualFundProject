import importlib
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent


def test_compute_frontier_returns_expected_keys():
    efficient_frontier = importlib.import_module('efficient_frontier')
    amfi_codes = [100016, 100033, 120503]
    result = efficient_frontier.compute_frontier(amfi_codes)

    assert set(result.keys()) == {'mean_return', 'volatility', 'cov_matrix', 'weights'}
    assert len(result['weights']) == len(amfi_codes)
    assert result['cov_matrix'].shape == (len(amfi_codes), len(amfi_codes))


def test_simulate_nav_growth_returns_expected_shape():
    monte_carlo = importlib.import_module('monte_carlo')
    result = monte_carlo.simulate_nav_growth(100016, years=1, simulations=10)

    assert isinstance(result, pd.DataFrame)
    assert result.shape[0] == 252
    assert result.shape[1] == 10


def test_send_weekly_report_creates_message_without_crashing(tmp_path):
    import email_report

    message_path = tmp_path / 'summary.txt'
    message_path.write_text('weekly summary', encoding='utf-8')

    email_report.ROOT = tmp_path
    email_report.send_weekly_report('recipient@example.com')
