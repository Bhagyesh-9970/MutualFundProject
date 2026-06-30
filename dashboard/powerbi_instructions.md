Power BI connection and dashboard build instructions

1) Create SQLite DB

- From the repo root run:

```powershell
python scripts\create_sqlite_from_csv.py
```

- This writes `dashboard/bluestock_mf.db` containing all processed CSVs (processed files take precedence).

2) Connect Power BI

- Option A — Direct CSV import: use `Get data -> Text/CSV` and import the cleaned CSVs from `data/processed`.
- Option B — SQLite ODBC: use `Get data -> More -> Other -> ODBC` and connect to the `dashboard/bluestock_mf.db` file using the `SQLite ODBC` driver (install if needed).

3) Verify tables

- Ensure the following tables (examples) are present: `02_nav_history_cleaned`, `07_scheme_performance_cleaned`, `08_investor_transactions_cleaned`. If additional cleaned tables are expected, run or add cleaning scripts in `scripts/`.

4) Relationships

- Create relationships on `amfi_code` between scheme performance and NAV/history tables.
- Create relationships on date columns between time-series tables (e.g., nav history date <-> calendar date if used).

5) Theme and logo

- Import theme: `View -> Themes -> Browse for themes` and select `dashboard/bluestock_theme.json`.
- Add the logo image to the report header using `Insert -> Image` and choose `dashboard/bluestock_logo.svg`.

6) Page-by-page guidance (high-level)

- Page 1 — Industry Overview:
  - KPI cards: Total AUM (use aggregated `aum_crore`), SIP Inflows (sum of `amount_inr` where transaction_type='Sip'), Folios (distinct folio count), Schemes (count of schemes).
  - Line chart: industry AUM trend using `date` (2022–2025) and sum of AUM.
  - Bar chart: AUM by AMC (`fund_house` or `amc_name`).

- Page 2 — Fund Performance:
  - Scatter: X=return (e.g., `return_1yr`), Y=`std_dev_ann`, Size=`aum_crore`.
  - Table: sortable fund scorecard using performance metrics.
  - NAV line vs benchmark: use `02_nav_history_cleaned` and `10_benchmark_indices` if available.
  - Slicers: fund house, category, plan.

- Page 3 — Investor Analytics:
  - Bar: transaction amount by state.
  - Donut: split by `transaction_type`.
  - Bar: age group vs avg SIP.
  - Line: monthly transaction volume using `transaction_date`.
  - Slicers: state, age group, city tier.

- Page 4 — SIP & Market Trends:
  - Dual-axis chart: SIP inflow (bar) and Nifty 50 (line) 2022–2025.
  - Heatmap: category inflow vs month.
  - Top 5 categories by net inflow FY25 (use measure and Top N filter).

7) Interactivity

- Add drill-through: create a NAV detail page and enable drill-through field on the fund identifier (e.g., `amfi_code`).
- Add report/page tooltips: use `Page information -> Tooltip` and design custom tooltip pages.

8) Export

- Save the report as `bluestock_mf_dashboard.pbix` using `File -> Save as`.
- Export to PDF: `File -> Export -> PDF`.
- Export each page to PNG: `File -> Export -> Power BI visuals` or use `Export to PDF` then extract pages, or use `File -> Export -> Power BI Desktop -> Export current page as PNG` for each page.

Notes

- I cannot run Power BI Desktop from this environment. I prepared the `dashboard/bluestock_mf.db` generator and theme/logo so you can open Power BI and complete the visual build and exports.
