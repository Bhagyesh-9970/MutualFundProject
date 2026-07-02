# Setup Guide

## Prerequisites

- Python 3.10 or newer
- Windows PowerShell (for the scheduling script)
- Internet access for live NAV fetching

## Environment setup

```powershell
cd C:\Users\Bhagyesh\OneDrive\Desktop\MutualFundProject
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Run the project

- Streamlit dashboard: `.
\venv\Scripts\python.exe -m streamlit run app.py`
- Monte Carlo simulation: `.
\venv\Scripts\python.exe monte_carlo.py`
- Efficient frontier: `.
\venv\Scripts\python.exe efficient_frontier.py`
- Email report: `.
\venv\Scripts\python.exe email_report.py`

## Optional email configuration

Set these environment variables before running the email report:

```powershell
$env:SMTP_SERVER="smtp.example.com"
$env:SMTP_FROM="your-email@example.com"
```

## Scheduled ETL

```powershell
powershell -ExecutionPolicy Bypass -File .\schedule_nav_etl.ps1
```
