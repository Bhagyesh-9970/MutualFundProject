# 📊 Mutual Fund Analytics Dashboard (BlueStock Capstone)

## 📌 Project Overview

This project is a FinTech data analytics capstone that analyzes mutual fund industry data from 2022–2025 using Python, SQL, Pandas, and visualization libraries. It combines data cleaning, exploratory analysis, portfolio analytics, and reporting into a single workflow.

---

## 🎯 Objectives

- Analyze historical NAV performance of mutual funds
- Compare AUM growth across fund houses
- Study SIP inflow trends over time
- Explore investor behavior and fund categories
- Build portfolio analytics features such as efficient frontier and Monte Carlo simulation
- Generate automated weekly performance reports

---

## 🛠 Tech Stack

- Python
- Pandas
- NumPy
- Streamlit
- Plotly
- Matplotlib
- Seaborn
- SQLite
- SQL
- Jupyter Notebook
- Git & GitHub
- VS Code

---

## 📂 Project Structure

```text
MutualFundProject/
├── app.py
├── efficient_frontier.py
├── email_report.py
├── monte_carlo.py
├── requirements.txt
├── schedule_nav_etl.ps1
├── dashboard/
├── data/
│   ├── raw/
│   └── processed/
├── notebooks/
├── reports/
├── scripts/
├── sql/
├── tests/
└── README.md
```

---

## 📈 Dataset Overview

The project uses multiple financial datasets, including:

- Fund master data
- NAV history
- AUM by fund house
- Monthly SIP inflows
- Category inflows
- Industry folio count
- Scheme performance
- Investor transactions
- Portfolio holdings
- Benchmark indices

---

## ✅ Completed Features

### Core analytics
- EDA notebooks and analysis scripts
- SQLite database creation and SQL queries
- Summary and quality reports under the reports folder

### Bonus tasks implemented
- Streamlit dashboard for interactive fund analysis
- Monte Carlo simulation for NAV projection over 5 years
- Efficient frontier portfolio optimization for selected funds
- Automated HTML email report generation
- Scheduled NAV ETL workflow for weekdays at 8 PM

---

## ▶️ How to Run

### 1) Streamlit dashboard
```bash
.
\venv\Scripts\python.exe -m streamlit run app.py
```

### 2) Monte Carlo simulation
```bash
.
\venv\Scripts\python.exe monte_carlo.py
```

### 3) Efficient frontier analysis
```bash
.
\venv\Scripts\python.exe efficient_frontier.py
```

### 4) Weekly email report
```bash
.
\venv\Scripts\python.exe email_report.py
```

### 5) Scheduled NAV ETL
Run the PowerShell script below to register a weekday schedule for the NAV fetch job:
```powershell
powershell -ExecutionPolicy Bypass -File .\schedule_nav_etl.ps1
```

---

## 🧪 Verification

The bonus modules are covered by regression tests in the tests folder.

```bash
.
\venv\Scripts\python.exe -m pytest -q tests/test_bonus_modules.py
```

---

## 📌 Notes

- The project uses processed CSV files under the data folder as the primary input source.
- Database files are ignored by Git using the repository ignore rules.
- The dashboard instructions and Power BI assets are stored under the dashboard folder.

---

## 👨‍💻 Author

**Bhagyesh Mali**

Data Analyst Intern — BlueStock FinTech
