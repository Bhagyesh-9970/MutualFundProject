from pathlib import Path

import numpy as np
import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parent
NAV_PATH = ROOT / 'data' / 'processed' / '02_nav_history_cleaned.csv'
SCHEME_PATH = ROOT / 'data' / 'processed' / '07_scheme_performance_cleaned.csv'

st.set_page_config(page_title='Mutual Fund Analytics', page_icon='📈', layout='wide')
st.title('Mutual Fund Analytics Dashboard')

nav = pd.read_csv(NAV_PATH)
schemes = pd.read_csv(SCHEME_PATH)

nav['date'] = pd.to_datetime(nav['date'])
nav = nav.sort_values(['amfi_code', 'date'])

with st.sidebar:
    st.header('Filters')
    category_options = sorted(schemes['category'].dropna().astype(str).unique().tolist())
    selected_category = st.multiselect('Category', category_options, default=category_options[:3])

    risk_options = sorted(schemes['risk_grade'].dropna().astype(str).unique().tolist())
    selected_risk = st.multiselect('Risk grade', risk_options, default=risk_options)

    min_date = nav['date'].min().date()
    max_date = nav['date'].max().date()
    selected_dates = st.slider('Date range', min_value=min_date, max_value=max_date, value=(min_date, max_date))

    scheme_options = sorted(schemes['scheme_name'].tolist())
    selected_schemes = st.multiselect('Select funds', scheme_options, default=scheme_options[:5])

filtered_schemes = schemes[
    schemes['scheme_name'].isin(selected_schemes)
    & schemes['category'].isin(selected_category)
    & schemes['risk_grade'].isin(selected_risk)
].copy()
selected_amfi = filtered_schemes['amfi_code'].tolist()

if selected_amfi:
    plot_data = nav[nav['amfi_code'].isin(selected_amfi)].copy()
    plot_data = plot_data[(plot_data['date'].dt.date >= selected_dates[0]) & (plot_data['date'].dt.date <= selected_dates[1])]
    plot_data['daily_return'] = plot_data.groupby('amfi_code')['nav'].pct_change()
    plot_data = plot_data.dropna(subset=['daily_return'])

    st.subheader('NAV trend')
    nav_chart = plot_data.pivot_table(index='date', columns='amfi_code', values='nav', aggfunc='last')
    st.line_chart(nav_chart)

    st.subheader('Rolling 90-day Sharpe')
    sharpe_df = []
    for code in selected_amfi:
        fund = plot_data[plot_data['amfi_code'] == code].copy()
        fund['rolling_sharpe'] = fund['daily_return'].rolling(90).mean() / fund['daily_return'].rolling(90).std(ddof=1) * np.sqrt(252)
        fund = fund.dropna(subset=['rolling_sharpe'])
        sharpe_df.append(pd.DataFrame({
            'date': fund['date'],
            'scheme_name': filtered_schemes.loc[filtered_schemes['amfi_code'] == code, 'scheme_name'].iloc[0],
            'rolling_sharpe': fund['rolling_sharpe'],
        }))

    sharpe_df = pd.concat(sharpe_df, ignore_index=True)
    st.line_chart(sharpe_df, x='date', y='rolling_sharpe', color='scheme_name')

    st.subheader('Risk summary')
    summary = filtered_schemes[['scheme_name', 'category', 'risk_grade', 'sharpe_ratio', 'return_3yr_pct']].copy()
    st.dataframe(summary, use_container_width=True)
else:
    st.info('Select at least one fund to view the dashboard.')
