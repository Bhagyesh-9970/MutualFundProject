import os
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import nbformat as nbf
from pathlib import Path

ROOT = Path(__file__).resolve().parent
NAV_PATH = ROOT / 'data' / 'processed' / '02_nav_history_cleaned.csv'
SCHEME_PATH = ROOT / 'data' / 'processed' / '07_scheme_performance_cleaned.csv'
TX_PATH = ROOT / 'data' / 'processed' / '08_investor_transactions_cleaned.csv'
HOLDINGS_PATH = ROOT / 'data' / 'raw' / '09_portfolio_holdings.csv'


def load_data():
    nav = pd.read_csv(NAV_PATH)
    nav['date'] = pd.to_datetime(nav['date'])
    nav = nav.sort_values(['amfi_code', 'date']).reset_index(drop=True)

    schemes = pd.read_csv(SCHEME_PATH)
    schemes['amfi_code'] = pd.to_numeric(schemes['amfi_code'], errors='coerce')

    tx = pd.read_csv(TX_PATH)
    tx['transaction_date'] = pd.to_datetime(tx['transaction_date'])
    tx = tx.sort_values(['investor_id', 'transaction_date']).reset_index(drop=True)

    holdings = pd.read_csv(HOLDINGS_PATH)
    holdings['portfolio_date'] = pd.to_datetime(holdings['portfolio_date'])
    return nav, schemes, tx, holdings


def compute_var_cvar(nav, schemes):
    nav = nav.copy()
    nav['daily_return'] = nav.groupby('amfi_code')['nav'].pct_change()
    returns = nav.dropna(subset=['daily_return'])

    var_rows = []
    for code, group in returns.groupby('amfi_code'):
        ret = group['daily_return'].dropna()
        if len(ret) < 30:
            continue
        threshold = ret.quantile(0.05)
        cvar = ret[ret <= threshold].mean()
        var_rows.append({
            'amfi_code': int(code),
            'var_95_pct': round(float(-threshold) * 100, 2),
            'cvar_95_pct': round(float(-cvar) * 100, 2),
            'daily_return_count': int(len(ret)),
        })

    var_df = pd.DataFrame(var_rows)
    var_df = var_df.merge(schemes[['amfi_code', 'scheme_name', 'fund_house', 'risk_grade', 'category']], on='amfi_code', how='left')
    var_df = var_df.sort_values('var_95_pct', ascending=False).reset_index(drop=True)
    return var_df


def plot_rolling_sharpe(nav, schemes):
    key_funds = {
        'SBI Bluechip': 119551,
        'HDFC Top 100': 100016,
        'ICICI Bluechip': 120503,
        'Nippon Large Cap': 118632,
        'HDFC Mid-Cap': 100033,
    }
    fig, ax = plt.subplots(figsize=(12, 6))
    for label, code in key_funds.items():
        fund_nav = nav.loc[nav['amfi_code'] == code].copy().sort_values('date')
        if fund_nav.empty:
            continue
        fund_nav['daily_return'] = fund_nav['nav'].pct_change()
        sharpe = fund_nav['daily_return'].rolling(90).mean() / fund_nav['daily_return'].rolling(90).std(ddof=1) * np.sqrt(252)
        sharpe = sharpe.dropna()
        if sharpe.empty:
            continue
        ax.plot(sharpe.index, sharpe.values, label=label, linewidth=1.8)

    ax.set_title('Rolling 90-Day Sharpe Ratio for 5 Key Funds')
    ax.set_xlabel('Trading Days')
    ax.set_ylabel('Sharpe Ratio')
    ax.axhline(0, color='black', linewidth=0.8, linestyle='--')
    ax.legend()
    ax.grid(alpha=0.25)
    fig.tight_layout()
    output_path = ROOT / 'rolling_sharpe_chart.png'
    fig.savefig(output_path, dpi=200)
    plt.close(fig)
    return output_path


def compute_cohort_analysis(tx, schemes):
    tx = tx.copy()
    tx['first_transaction_year'] = tx.groupby('investor_id')['transaction_date'].transform('min').dt.year

    investment_tx = tx[tx['transaction_type'].isin(['Sip', 'Lumpsum'])].copy()
    sip_tx = tx[tx['transaction_type'] == 'Sip'].copy()

    investor_metrics = investment_tx.groupby('investor_id').agg(
        total_invested=('amount_inr', 'sum'),
        investment_count=('amount_inr', 'count'),
    )
    sip_metrics = sip_tx.groupby('investor_id').agg(
        avg_sip_amount=('amount_inr', 'mean'),
    )

    top_fund_counts = investment_tx.groupby(['investor_id', 'amfi_code']).size().reset_index(name='count')
    top_fund_counts = top_fund_counts.sort_values(['investor_id', 'count'], ascending=[True, False]).drop_duplicates('investor_id')

    investor_profile = investor_metrics.join(sip_metrics, how='left').join(top_fund_counts[['investor_id', 'amfi_code']], how='left')
    investor_profile = investor_profile.reset_index()
    investor_profile['first_transaction_year'] = tx.groupby('investor_id')['first_transaction_year'].first().values

    cohort_summary = investor_profile.groupby('first_transaction_year').agg(
        investors=('investor_id', 'nunique'),
        avg_sip_amount=('avg_sip_amount', 'mean'),
        total_invested=('total_invested', 'sum'),
    ).reset_index()

    preference = investor_profile.groupby(['first_transaction_year', 'amfi_code']).size().reset_index(name='count')
    preference = preference.sort_values(['first_transaction_year', 'count'], ascending=[True, False]).drop_duplicates('first_transaction_year')
    preference = preference.merge(schemes[['amfi_code', 'scheme_name']], on='amfi_code', how='left')
    cohort_summary = cohort_summary.merge(preference[['first_transaction_year', 'scheme_name', 'count']], on='first_transaction_year', how='left')
    cohort_summary = cohort_summary.rename(columns={'scheme_name': 'top_fund_preference'})
    return cohort_summary


def compute_sip_continuity(tx):
    sip_tx = tx[tx['transaction_type'] == 'Sip'].copy()
    sip_tx = sip_tx.sort_values(['investor_id', 'transaction_date'])

    def gap_stats(group):
        gaps = group['transaction_date'].diff().dropna().dt.days
        return pd.Series({
            'sip_count': len(group),
            'avg_gap_days': float(gaps.mean()) if not gaps.empty else np.nan,
        })

    continuity = sip_tx.groupby('investor_id').apply(gap_stats).reset_index()
    eligible = continuity[continuity['sip_count'] >= 6].copy()
    eligible['at_risk'] = eligible['avg_gap_days'] > 35
    continuity_rate = 1 - eligible['at_risk'].mean()
    return eligible, continuity_rate


def compute_sector_hhi(holdings, schemes):
    latest_holdings = holdings.sort_values(['amfi_code', 'portfolio_date']).groupby('amfi_code').tail(1).copy()
    sector_weights = latest_holdings.groupby(['amfi_code', 'sector'])['weight_pct'].sum().reset_index()
    sector_hhi = (
        sector_weights.groupby('amfi_code')['weight_pct']
        .apply(lambda s: ((s / 100) ** 2).sum())
        .reset_index(name='sector_hhi')
    )
    sector_hhi = sector_hhi.merge(schemes[['amfi_code', 'scheme_name', 'fund_house', 'risk_grade', 'category']], on='amfi_code', how='left')
    sector_hhi['concentration_flag'] = sector_hhi['sector_hhi'] > 0.25
    sector_hhi = sector_hhi.sort_values('sector_hhi', ascending=False).reset_index(drop=True)
    return sector_hhi


def write_notebook(var_df, cohort_df, continuity_df, hhi_df, continuity_rate, recommend_table):
    nb = nbf.v4.new_notebook()

    cells = []
    cells.append(nbf.v4.new_markdown_cell('# Advanced Analytics + Risk Metrics\n\nThis notebook extends the mutual fund project with VaR/CVaR, rolling Sharpe analysis, investor cohort insights, SIP continuity monitoring, sector concentration analysis, and a simple fund recommender.'))
    cells.append(nbf.v4.new_code_cell("""import pandas as pd\nimport numpy as np\nimport matplotlib\nmatplotlib.use('Agg')\nimport matplotlib.pyplot as plt\nfrom pathlib import Path\n\nROOT = Path.cwd()\nnav = pd.read_csv(ROOT / 'data' / 'processed' / '02_nav_history_cleaned.csv')\nnav['date'] = pd.to_datetime(nav['date'])\nschemes = pd.read_csv(ROOT / 'data' / 'processed' / '07_scheme_performance_cleaned.csv')\ntx = pd.read_csv(ROOT / 'data' / 'processed' / '08_investor_transactions_cleaned.csv')\ntx['transaction_date'] = pd.to_datetime(tx['transaction_date'])\nholdings = pd.read_csv(ROOT / 'data' / 'raw' / '09_portfolio_holdings.csv')\nholdings['portfolio_date'] = pd.to_datetime(holdings['portfolio_date'])\n"""))
    cells.append(nbf.v4.new_code_cell("""nav = nav.sort_values(['amfi_code', 'date']).reset_index(drop=True)\nnav['daily_return'] = nav.groupby('amfi_code')['nav'].pct_change()\nreturns = nav.dropna(subset=['daily_return'])\n\nvar_rows = []\nfor code, group in returns.groupby('amfi_code'):\n    ret = group['daily_return'].dropna()\n    threshold = ret.quantile(0.05)\n    cvar = ret[ret <= threshold].mean()\n    var_rows.append({\n        'amfi_code': int(code),\n        'var_95_pct': round(float(-threshold) * 100, 2),\n        'cvar_95_pct': round(float(-cvar) * 100, 2),\n    })\n\nvar_df = pd.DataFrame(var_rows).merge(schemes[['amfi_code', 'scheme_name', 'fund_house', 'risk_grade']], on='amfi_code', how='left')\nvar_df = var_df.sort_values('var_95_pct', ascending=False).reset_index(drop=True)\nvar_df.head()\n"""))
    cells.append(nbf.v4.new_code_cell("""var_df.to_csv(ROOT / 'var_cvar_report.csv', index=False)\nvar_df.head(10)\n"""))
    cells.append(nbf.v4.new_code_cell("""key_funds = {\n    'SBI Bluechip': 119551,\n    'HDFC Top 100': 100016,\n    'ICICI Bluechip': 120503,\n    'Nippon Large Cap': 118632,\n    'HDFC Mid-Cap': 100033,\n}\n\nfig, ax = plt.subplots(figsize=(12, 6))\nfor label, code in key_funds.items():\n    fund_nav = nav.loc[nav['amfi_code'] == code].copy().sort_values('date')\n    fund_nav['daily_return'] = fund_nav['nav'].pct_change()\n    sharpe = fund_nav['daily_return'].rolling(90).mean() / fund_nav['daily_return'].rolling(90).std(ddof=1) * np.sqrt(252)\n    sharpe = sharpe.dropna()\n    ax.plot(sharpe.index, sharpe.values, label=label)\n\nax.set_title('Rolling 90-Day Sharpe Ratio for 5 Key Funds')\nax.set_xlabel('Trading Days')\nax.set_ylabel('Sharpe Ratio')\nax.axhline(0, color='black', linestyle='--', linewidth=0.8)\nax.legend()\nax.grid(alpha=0.25)\nfig.tight_layout()\nfig.savefig(ROOT / 'rolling_sharpe_chart.png', dpi=200)\nplt.close(fig)\n"""))
    cells.append(nbf.v4.new_code_cell("""tx['first_transaction_year'] = tx.groupby('investor_id')['transaction_date'].transform('min').dt.year\n\ninvestment_tx = tx[tx['transaction_type'].isin(['Sip', 'Lumpsum'])].copy()\nsip_tx = tx[tx['transaction_type'] == 'Sip'].copy()\n\ninvestor_metrics = investment_tx.groupby('investor_id').agg(total_invested=('amount_inr', 'sum'))\nsip_metrics = sip_tx.groupby('investor_id').agg(avg_sip_amount=('amount_inr', 'mean'))\n\ntop_fund_counts = investment_tx.groupby(['investor_id', 'amfi_code']).size().reset_index(name='count')\ntop_fund_counts = top_fund_counts.sort_values(['investor_id', 'count'], ascending=[True, False]).drop_duplicates('investor_id')\n\ninvestor_profile = investor_metrics.join(sip_metrics, how='left').join(top_fund_counts[['investor_id', 'amfi_code']], how='left').reset_index()\ninvestor_profile['first_transaction_year'] = tx.groupby('investor_id')['first_transaction_year'].first().values\n\ncohort_df = investor_profile.groupby('first_transaction_year').agg(\n    investors=('investor_id', 'nunique'),\n    avg_sip_amount=('avg_sip_amount', 'mean'),\n    total_invested=('total_invested', 'sum'),\n).reset_index()\n\npreference = investor_profile.groupby(['first_transaction_year', 'amfi_code']).size().reset_index(name='count')\npreference = preference.sort_values(['first_transaction_year', 'count'], ascending=[True, False]).drop_duplicates('first_transaction_year')\npreference = preference.merge(schemes[['amfi_code', 'scheme_name']], on='amfi_code', how='left')\ncohort_df = cohort_df.merge(preference[['first_transaction_year', 'scheme_name']], on='first_transaction_year', how='left')\ncohort_df.rename(columns={'scheme_name': 'top_fund_preference'}, inplace=True)\ncohort_df\n"""))
    cells.append(nbf.v4.new_code_cell("""def gap_stats(group):\n    gaps = group['transaction_date'].diff().dropna().dt.days\n    return pd.Series({'sip_count': len(group), 'avg_gap_days': float(gaps.mean()) if not gaps.empty else np.nan})\n\nsip_only = tx[tx['transaction_type'] == 'Sip'].copy().sort_values(['investor_id', 'transaction_date'])\ncontinuity = sip_only.groupby('investor_id').apply(gap_stats).reset_index()\neligible = continuity[continuity['sip_count'] >= 6].copy()\neligible['at_risk'] = eligible['avg_gap_days'] > 35\neligible.head()\n"""))
    cells.append(nbf.v4.new_code_cell("""latest_holdings = holdings.sort_values(['amfi_code', 'portfolio_date']).groupby('amfi_code').tail(1).copy()\nsector_weights = latest_holdings.groupby(['amfi_code', 'sector'])['weight_pct'].sum().reset_index()\nsector_hhi = sector_weights.groupby('amfi_code')['weight_pct'].apply(lambda s: ((s / 100) ** 2).sum()).reset_index(name='sector_hhi')\nsector_hhi = sector_hhi.merge(schemes[['amfi_code', 'scheme_name', 'fund_house', 'risk_grade']], on='amfi_code', how='left')\nsector_hhi['concentration_flag'] = sector_hhi['sector_hhi'] > 0.25\nsector_hhi.sort_values('sector_hhi', ascending=False).head(10)\n"""))
    cells.append(nbf.v4.new_code_cell("""from recommender import recommend_funds\nrecommend_table = recommend_funds('Moderate')\nrecommend_table\n"""))
    cells.append(nbf.v4.new_markdown_cell("""## Advanced Insights\n\n1. The fund with the highest estimated downside risk is {highest_var_fund} with a 95% VaR of {highest_var:.2f}% and a CVaR of {highest_cvar:.2f}%.\n2. The strongest investor cohort is {cohort_year}, which contributed the highest total investment amount of ₹{cohort_investment:,.0f}.\n3. SIP continuity remains {continuity_status} with {continuity_rate:.1%} of eligible investors staying within a healthy gap profile.\n4. The most concentrated equity portfolio is {highest_hhi_fund} with a sector HHI of {highest_hhi:.3f}, indicating tighter sector concentration.\n5. For a moderate risk appetite, the recommended funds are {recommend_names}.\n""".format(
        highest_var_fund=var_df.loc[0,'scheme_name'],
        highest_var=var_df.loc[0,'var_95_pct'],
        highest_cvar=var_df.loc[0,'cvar_95_pct'],
        cohort_year=int(cohort_df['first_transaction_year'].iloc[cohort_df['total_invested'].idxmax()]),
        cohort_investment=cohort_df['total_invested'].max(),
        continuity_status='healthy' if continuity_rate >= 0.7 else 'mixed',
        continuity_rate=continuity_rate,
        highest_hhi_fund=hhi_df.loc[0,'scheme_name'],
        highest_hhi=hhi_df.loc[0,'sector_hhi'],
        recommend_names=', '.join(recommend_table['scheme_name'].tolist()),
    )))

    nb['cells'] = cells
    nb['metadata'] = {
        'kernelspec': {'display_name': 'Python 3', 'language': 'python', 'name': 'python3'},
        'language_info': {'name': 'python', 'version': '3.13'},
    }
    with open(ROOT / 'Advanced_Analytics.ipynb', 'w', encoding='utf-8') as fh:
        nbf.write(nb, fh)


def main():
    nav, schemes, tx, holdings = load_data()
    var_df = compute_var_cvar(nav, schemes)
    var_df.to_csv(ROOT / 'var_cvar_report.csv', index=False)
    plot_rolling_sharpe(nav, schemes)
    cohort_df = compute_cohort_analysis(tx, schemes)
    eligible, continuity_rate = compute_sip_continuity(tx)
    hhi_df = compute_sector_hhi(holdings, schemes)
    from recommender import recommend_funds
    recommend_table = recommend_funds('Moderate')
    write_notebook(var_df, cohort_df, eligible, hhi_df, continuity_rate, recommend_table)

    print('Generated outputs:')
    print(' -', ROOT / 'Advanced_Analytics.ipynb')
    print(' -', ROOT / 'var_cvar_report.csv')
    print(' -', ROOT / 'recommender.py')
    print(' -', ROOT / 'rolling_sharpe_chart.png')


if __name__ == '__main__':
    main()
