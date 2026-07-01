import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SCHEME_PATH = ROOT / 'data' / 'processed' / '07_scheme_performance_cleaned.csv'


def recommend_funds(risk_appetite: str):
    schemes = pd.read_csv(SCHEME_PATH)
    risk_map = {
        'Low': ['Low'],
        'Moderate': ['Moderate', 'Moderately High'],
        'High': ['High', 'Very High'],
    }
    allowed = risk_map.get(risk_appetite.title(), ['Moderate', 'Moderately High'])
    filtered = schemes[schemes['risk_grade'].isin(allowed)].copy()
    filtered = filtered.sort_values(['sharpe_ratio', 'return_3yr_pct'], ascending=[False, False]).head(3)
    filtered = filtered[['amfi_code', 'scheme_name', 'fund_house', 'category', 'risk_grade', 'sharpe_ratio']].copy()
    filtered = filtered.rename(columns={'sharpe_ratio': 'sharpe_ratio'})
    return filtered.reset_index(drop=True)


if __name__ == '__main__':
    appetite = input('Enter risk appetite (Low / Moderate / High): ').strip().title()
    print(recommend_funds(appetite).to_string(index=False))
